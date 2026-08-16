#!/usr/bin/env python3
"""Respectful job-opportunity collector for public RSS/Atom feeds and public search pages.

The script reads sources.csv, fetches only the configured public URLs, filters records by
source-specific keywords, and saves normalized job rows to CSV. It does not log in, solve
CAPTCHAs, evade access controls, open individual adverts, or retry blocked sources.

Usage:
  python3 job_crawler.py --sources sources.csv --output-dir output
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import shutil
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

USER_AGENT = "HK-AI-Job-Research-Crawler/1.0 (public feed reader; respectful rate limits)"
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_SLEEP_SECONDS = 2.0
DEFAULT_LIMIT_PER_SOURCE = 30

OUTPUT_COLUMNS = [
    "source_id",
    "source_name",
    "source_type",
    "country_scope",
    "location_hint",
    "job_title",
    "company",
    "posted_at_raw",
    "summary",
    "job_url",
    "source_url",
    "matched_keywords",
    "collected_at_utc",
]
ERROR_COLUMNS = ["source_id", "source_name", "source_url", "error", "collected_at_utc"]


@dataclass(frozen=True)
class Source:
    source_id: str
    source_name: str
    source_type: str
    country_scope: str
    url: str
    location_hint: str
    keywords: tuple[str, ...]
    active: bool
    notes: str


@dataclass
class JobRow:
    source_id: str
    source_name: str
    source_type: str
    country_scope: str
    location_hint: str
    job_title: str
    company: str
    posted_at_raw: str
    summary: str
    job_url: str
    source_url: str
    matched_keywords: str
    collected_at_utc: str

    def to_dict(self) -> dict[str, str]:
        return {column: str(getattr(self, column)) for column in OUTPUT_COLUMNS}


def clean_text(value: str | None, max_length: int = 900) -> str:
    """Collapse whitespace and limit text so the CSV remains readable."""
    text = re.sub(r"\s+", " ", html.unescape(value or "")).strip()
    return text[:max_length]


def plain_text(value: str | None, max_length: int = 900) -> str:
    """Convert HTML fragments commonly found in RSS descriptions into plain text."""
    fragment = BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True)
    return clean_text(fragment, max_length)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_sources(path: Path) -> list[Source]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "source_id",
            "source_name",
            "source_type",
            "country_scope",
            "url",
            "location_hint",
            "keywords",
            "active",
            "notes",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"sources CSV is missing columns: {', '.join(sorted(missing))}")

        sources: list[Source] = []
        for row in reader:
            active = row["active"].strip().lower() in {"yes", "true", "1", "y"}
            keywords = tuple(
                clean_text(item).lower()
                for item in row["keywords"].split("|")
                if clean_text(item)
            )
            sources.append(
                Source(
                    source_id=clean_text(row["source_id"]),
                    source_name=clean_text(row["source_name"]),
                    source_type=clean_text(row["source_type"]).lower(),
                    country_scope=clean_text(row["country_scope"]),
                    url=clean_text(row["url"]),
                    location_hint=clean_text(row["location_hint"]),
                    keywords=keywords,
                    active=active,
                    notes=clean_text(row["notes"]),
                )
            )
    return sources


def fetch_public_url(url: str, timeout: int) -> tuple[bytes, str]:
    """Fetch one public URL with a transparent user agent; do not retry blocked requests."""
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/html;q=0.9, */*;q=0.1",
            "Accept-Language": "en-US,en;q=0.8,zh-HK;q=0.6",
        },
    )
    with urlopen(request, timeout=timeout) as response:  # nosec B310: URLs are user-configured public sources
        content_type = response.headers.get_content_type()
        return response.read(), content_type


def keyword_matches(text: str, keywords: Iterable[str]) -> list[str]:
    """Match complete Latin terms where possible; support multi-word phrases."""
    haystack = clean_text(text).lower()
    matched: list[str] = []
    for keyword in keywords:
        if not keyword:
            continue
        # Alpha-numeric keywords such as AI/LLM should match word boundaries, while
        # punctuation or CJK keywords are matched as literal phrases.
        if re.fullmatch(r"[a-z0-9+#.\- ]+", keyword, flags=re.IGNORECASE):
            pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
            if re.search(pattern, haystack, flags=re.IGNORECASE):
                matched.append(keyword)
        elif keyword in haystack:
            matched.append(keyword)
    return matched


def xml_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return clean_text(" ".join(element.itertext()))


def first_element_text(element: ET.Element, names: Iterable[str]) -> str:
    accepted = set(names)
    for child in element.iter():
        if child.tag.rsplit("}", 1)[-1] in accepted:
            value = xml_text(child)
            if value:
                return value
    return ""


def first_link(element: ET.Element) -> str:
    for child in element.iter():
        if child.tag.rsplit("}", 1)[-1] != "link":
            continue
        href = clean_text(child.attrib.get("href", ""))
        if href:
            return href
        if clean_text(child.text):
            return clean_text(child.text)
    return ""


def parse_feed(source: Source, content: bytes, collected_at: str) -> list[JobRow]:
    """Parse RSS 2.0 or Atom without third-party feed libraries."""
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise ValueError(f"invalid XML feed: {exc}") from exc

    root_name = root.tag.rsplit("}", 1)[-1].lower()
    if root_name == "rss":
        entries = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "item"]
    elif root_name == "feed":
        entries = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "entry"]
    else:
        entries = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] in {"item", "entry"}]

    rows: list[JobRow] = []
    for entry in entries:
        title = first_element_text(entry, {"title"})
        summary = plain_text(first_element_text(entry, {"description", "summary", "content"}))
        company = first_element_text(entry, {"author", "creator", "company"})
        posted = first_element_text(entry, {"pubDate", "published", "updated", "date"})
        link = first_link(entry)
        matched = keyword_matches(" ".join((title, summary, company)), source.keywords)
        if not title or not link or not matched:
            continue
        rows.append(
            JobRow(
                source_id=source.source_id,
                source_name=source.source_name,
                source_type=source.source_type,
                country_scope=source.country_scope,
                location_hint=source.location_hint,
                job_title=title,
                company=company,
                posted_at_raw=posted,
                summary=summary,
                job_url=urljoin(source.url, link),
                source_url=source.url,
                matched_keywords="|".join(matched),
                collected_at_utc=collected_at,
            )
        )
    return rows


def nearby_text(anchor, max_length: int = 1100) -> str:
    """Select a compact ancestor text block rather than crawling individual job pages."""
    node = anchor
    fallback = clean_text(anchor.get_text(" ", strip=True), max_length)
    for _ in range(6):
        node = getattr(node, "parent", None)
        if node is None:
            break
        text = clean_text(node.get_text(" ", strip=True), max_length)
        if 80 <= len(text) <= max_length:
            return text
        if text:
            fallback = text
    return fallback


def extract_company_from_card(card, title: str) -> str:
    """Best-effort company extraction for common public job-card attributes."""
    selectors = [
        "[data-testid*='company']",
        "[class*='company']",
        "a[href*='/company/']",
        "a[href*='-jobs']",
    ]
    for selector in selectors:
        candidate = card.select_one(selector) if hasattr(card, "select_one") else None
        if candidate:
            value = clean_text(candidate.get_text(" ", strip=True), 180)
            if value and value.lower() != title.lower():
                return value
    return ""


def public_job_anchors(soup: BeautifulSoup, source: Source):
    host = urlparse(source.url).netloc.lower()
    if "jobsdb" in host:
        anchors = soup.select("a[id^='job-title-']")
        if anchors:
            return anchors
    if "indeed" in host:
        anchors = soup.select("a[id^='job_']")
        if anchors:
            return anchors
    if "linkedin" in host:
        anchors = soup.select("a[href*='/jobs/view/']")
        if anchors:
            return anchors

    # Conservative fallback: only links whose own title text matches configured terms.
    return [
        anchor
        for anchor in soup.select("a[href]")
        if keyword_matches(anchor.get_text(" ", strip=True), source.keywords)
    ]


def parse_html_search(source: Source, content: bytes, collected_at: str) -> list[JobRow]:
    soup = BeautifulSoup(content, "html.parser")
    rows: list[JobRow] = []
    seen_urls: set[str] = set()
    for anchor in public_job_anchors(soup, source):
        title = clean_text(anchor.get_text(" ", strip=True), 300)
        href = clean_text(anchor.get("href", ""))
        if not title or not href:
            continue
        job_url = urljoin(source.url, href)
        if job_url in seen_urls:
            continue
        card_text = nearby_text(anchor)
        matched = keyword_matches(" ".join((title, card_text)), source.keywords)
        if not matched:
            continue
        seen_urls.add(job_url)
        card = anchor
        for _ in range(4):
            card = getattr(card, "parent", card)
        company = extract_company_from_card(card, title)
        posted_match = re.search(
            r"(?:Posted\s*)?(?:more than\s+)?\d+\s*(?:days?|日)\s*(?:ago|前)|(?:today|just posted|今日)",
            card_text,
            flags=re.IGNORECASE,
        )
        rows.append(
            JobRow(
                source_id=source.source_id,
                source_name=source.source_name,
                source_type=source.source_type,
                country_scope=source.country_scope,
                location_hint=source.location_hint,
                job_title=title,
                company=company,
                posted_at_raw=posted_match.group(0) if posted_match else "",
                summary=card_text,
                job_url=job_url,
                source_url=source.url,
                matched_keywords="|".join(matched),
                collected_at_utc=collected_at,
            )
        )
    return rows


def crawl_source(source: Source, timeout: int, limit: int) -> list[JobRow]:
    collected_at = utc_now()
    content, _content_type = fetch_public_url(source.url, timeout)
    if source.source_type == "rss":
        rows = parse_feed(source, content, collected_at)
    elif source.source_type == "html_search":
        rows = parse_html_search(source, content, collected_at)
    else:
        raise ValueError(f"unsupported source_type '{source.source_type}'")
    return rows[:limit]


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def deduplicate(rows: Iterable[JobRow]) -> list[JobRow]:
    unique: list[JobRow] = []
    seen: set[str] = set()
    for row in rows:
        key = row.job_url.split("?")[0].rstrip("/").lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def run(args: argparse.Namespace) -> int:
    sources_path = Path(args.sources).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    sources = [source for source in read_sources(sources_path) if source.active]
    if args.source_id:
        wanted = set(args.source_id)
        sources = [source for source in sources if source.source_id in wanted]
    if args.only_type:
        sources = [source for source in sources if source.source_type == args.only_type]
    if not sources:
        print("No active sources matched the selected filters.", file=sys.stderr)
        return 2

    all_rows: list[JobRow] = []
    errors: list[dict[str, str]] = []
    for index, source in enumerate(sources, start=1):
        print(f"[{index}/{len(sources)}] Fetching {source.source_name} ({source.source_type})")
        try:
            rows = crawl_source(source, args.timeout, args.limit_per_source)
            all_rows.extend(rows)
            print(f"  matched {len(rows)} records")
        except HTTPError as exc:
            message = f"HTTP {exc.code}: {exc.reason}"
            errors.append(
                {
                    "source_id": source.source_id,
                    "source_name": source.source_name,
                    "source_url": source.url,
                    "error": message,
                    "collected_at_utc": utc_now(),
                }
            )
            print(f"  skipped: {message}", file=sys.stderr)
        except (URLError, TimeoutError, ValueError, OSError) as exc:
            message = clean_text(str(exc), 500)
            errors.append(
                {
                    "source_id": source.source_id,
                    "source_name": source.source_name,
                    "source_url": source.url,
                    "error": message,
                    "collected_at_utc": utc_now(),
                }
            )
            print(f"  skipped: {message}", file=sys.stderr)
        if index < len(sources):
            time.sleep(args.sleep)

    unique_rows = deduplicate(all_rows)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    jobs_path = output_dir / f"jobs_{stamp}.csv"
    errors_path = output_dir / f"errors_{stamp}.csv"
    write_csv(jobs_path, OUTPUT_COLUMNS, (row.to_dict() for row in unique_rows))
    write_csv(errors_path, ERROR_COLUMNS, errors)
    shutil.copyfile(jobs_path, output_dir / "jobs_latest.csv")
    shutil.copyfile(errors_path, output_dir / "errors_latest.csv")

    print(f"\nSaved {len(unique_rows)} matched records: {jobs_path}")
    print(f"Saved {len(errors)} source errors: {errors_path}")
    print("Reminder: verify every listing on its original URL before applying.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect matching jobs from public RSS/Atom feeds and public search pages.")
    parser.add_argument("--sources", default="sources.csv", help="Path to source configuration CSV (default: sources.csv)")
    parser.add_argument("--output-dir", default="output", help="Directory for generated CSV files (default: output)")
    parser.add_argument("--source-id", action="append", help="Run only this source_id; repeat the option to select several sources")
    parser.add_argument("--only-type", choices=["rss", "html_search"], help="Run only one source type")
    parser.add_argument("--limit-per-source", type=int, default=DEFAULT_LIMIT_PER_SOURCE, help="Maximum matched rows from each source")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Network timeout in seconds")
    parser.add_argument("--sleep", type=float, default=DEFAULT_SLEEP_SECONDS, help="Delay between sources in seconds")
    return parser


if __name__ == "__main__":
    try:
        sys.exit(run(build_parser().parse_args()))
    except KeyboardInterrupt:
        print("Stopped by user.", file=sys.stderr)
        sys.exit(130)
