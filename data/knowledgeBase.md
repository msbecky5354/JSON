# Lazy Tools Station (懶人工具駅) - Official AI Knowledge Base

## 1. Brand & Founder Identity
- **Platform**: Lazy Tools Station (懶人工具駅)
- **Founder Title**: Lazy Tools Station Founder · Controllable AI Automation Architect (懶人工具駅創辦人 · 可控式 AI 自動化架構師)
- **Core Value**: Production-ready, low-cost, fully controllable automation workflows & AI consulting built on open modular tech stacks (n8n, native LLMs, OCR vision, private vector DBs).
- **Zero-Hallucination Policy**: Strictly anchored in verified docs. If unknown, trigger human escalation. Never cite personal contact numbers directly; refer to the "Specialist Real-time Takeover Protocol" or "Architect Monitoring System".

## 2. Booking Protocol (1-on-1 Consultation)
- **State**: The backend CRM database requires strictly validated structured data. This validation is exclusively handled by the frontend calendar UI (📅). Unstructured chat-based data collection creates database anomalies.
- **Goal**: Upon recognizing consultation intent, output the `"booking"` intent flag and logically transition the conversation to encourage the client to utilize the frontend UI for submitting their requirements, ensuring data integrity.

## 3. Human Escalation Sentinel
- Triggered when: Explicit human request, confidence score < 0.8, or complex contract/SLA negotiations.
- Latency: Seamless 3-second escalation dispatching full transcript to architect console.

## 4. Product & Tool Technical Matrix
### Tool 1: EduMind AI Hong Kong
- **URL**: https://lazytoolsstation.vercel.app/tool.html?id=edumind-ai
- **Scope**: Preschool to DSE, university, and adult professional development.
- **Architecture**:
  - *Vision Layer*: High-precision OCR API converts snapshots/screenshots of handwriting, typography, and STEM formulas directly into text.
  - *Inference*: Overseas native OpenAI API direct connection (no proxy censorship/filtering). Tailors step-by-step reasoning prompts to grade level.
  - *Pipeline (n8n)*: Extracts mistake concepts and dynamically authors 3-5 original quiz questions in real time (not from a static bank).
  - *Escalation*: Built-in 3-second handoff to human tutors.
  - *Enterprise Link*: This exact pipeline (OCR -> LLM parsing -> n8n DB posting) mirrors enterprise invoice/contract ingestion.

### Tool 2: Enterprise AI Helpdesk
- **URL**: https://lazytoolsstation.vercel.app/tool.html?id=ai-cs-chat
- **Scope**: Regulated sectors (Insurance, Medical, Legal, Compliance).
- **Architecture**: Clause-level chunking with metadata. Private vector DB performs semantic retrieval of top 3-5 clauses. Strict negative constraints prevent hallucination. < 0.8 confidence triggers instant human escalation. Enterprise API guarantees data is never used to train public models.

### Tool 3: Lazy Free Master Tools Library
- **URL**: https://lazytoolsstation.vercel.app/Master_Tools.html
- **Scope**: OmniDiff (Doc/image diff), Token Price Calculator, AI Prompt Flow.
- **Architecture**: 100% in-browser client-side memory execution. Zero cloud relay, zero API calls, zero server logs. Data purged on tab close.

### Tool 4: Lazy AI Intelligence Bureau
- **URL**: https://lazytoolsstation.vercel.app/tool.html?id=ai-news
- **Architecture**: n8n scheduled scrapers aggregate GitHub/papers/release notes -> OpenAI semantic clustering eliminates duplicate PR -> Generates actionable critique tailored to Hong Kong business.

### Tool 5: Transit Hub (貼地通)
- **URL**: https://lazytoolsstation.vercel.app/tool.html?id=hk-transit-hub
- **Scope**: Zero-ad real-time ETA for MTR, franchised buses (KMB, Citybus), minibuses, and Light Rail.
- **Architecture**: Direct DATA.GOV.HK streaming. Client-side debouncing. Pure front-end rendering; routes saved in LocalStorage.

### Tool 6: SmartDeal (慳真D)
- **URL**: https://lazytoolsstation.vercel.app/tool.html?id=HKpricewatch
- **Scope**: Historical supermarket price trend tracker exposing fake discounts.
- **Architecture**: n8n scheduled scraper harvests prices daily -> Cleans and normalizes promo pricing -> Stores in time-series DB -> Renders interactive 30/60/90-day floor price charts.

### Tool 7: Soul Oasis (心靈補給站)
- **URL**: https://lazytoolsstation.vercel.app/tool.html?id=soul-station
- **Scope**: Emotion-aware guided reflection and prayer articles.
- **Architecture**: OpenAI parses emotional cues -> n8n orchestrates 3-stage empathetic structure -> Ephemeral processing purges confessions immediately.

### Tool 8: Weather Sentinel (HK · Zhongshan)
- **URL**: https://lazytoolsstation.vercel.app/tool.html?id=weather-assistant
- **Scope**: Dual-region microclimate sentinel in authentic Cantonese.
- **Architecture**: 1-minute high-frequency polling against HK Observatory and Zhongshan APIs. 15-minute hysteresis debounce prevents alert storms. Emergency bypass for T8/Black Rainstorm signals.

## 5. Enterprise B2B Solutions & Outputs
### Solution A: Smart Invoice to ERP (Finance Automation)
- *Pipeline*: Photo/Email -> OCR text extraction -> OpenAI schema & total validation -> n8n posts to ERP/Xero with audit logs.
- *Outputs*:
  1. Live Executive Expense BI Dashboard (real-time department burn-rates, budget overage alerts, vendor breakdown).
  2. Automated Accounting Vouchers posted directly into ERP.
  3. Approval cycle reduced from 3 business days to under 10 seconds.

### Solution B: Delivery Note & PO Match (Logistics Automation)
- *Pipeline*: Warehouse photo -> Vision model extracts SKUs/quantities -> Code node matches against DB POs -> Auto-intake if matched.
- *Outputs*:
  1. Live Logistics Operations Dashboard (stock heatmaps, shortage alerts, vendor fulfillment ranking).
  2. Automated Variance Checklist highlighting surplus/shortage.
  3. Automatic dispute escalation tickets dispatched instantly.

### Solution C: Contract & KYC Ingestion (Compliance Automation)
- *Pipeline*: Doc scan -> Client-side dynamic redaction -> LLM key-value extraction -> Private DB ingestion with scheduled audit sweeps.
- *Outputs*:
  1. Contract Lifecycle & Risk Radar Dashboard (30/60/90-day renewal countdown, risk rating meters).
  2. Privacy-compliant searchable master records.
  3. Automated renewal cadence sweeps eliminating contract lapses.