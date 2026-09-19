/**
 * Lazy Tools Station (懶人工具駅) - Official AI Customer Service Knowledge Base
 * Language: English (Standardized B2B Consulting Specification)
 */

export const LAZY_TOOLS_KNOWLEDGE_BASE = {
  brand: {
    platformName: "Lazy Tools Station (懶人工具駅)",
    founderTitle: "Lazy Tools Station Founder · Controllable AI Automation Architect",
    coreMission: "Delivering low-cost, high-efficiency, fully controllable automation pipelines and production-ready AI solutions for enterprises and professionals.",
    corePhilosophy: "Build once, reuse everywhere with open-source and modular tech stacks (n8n, native LLMs, OCR vision, private vector DBs). Every pipeline is bound by strict deterministic rules to eliminate hallucinations safely.",
    primaryTabs: ["AI Tools", "Architecture & Case Studies"]
  },

  protocols: {
    bookingIntake: {
      triggerConditions: [
        "Inquiries regarding 1-on-1 advisory sessions",
        "Requests for custom enterprise automation pipelines",
        "Pricing or commercial partnership inquiries",
        "Direct requests to speak with the Founder / Automation Architect"
      ],
      requiredFields: [
        { field: "clientNameAndCompany", description: "Contact person's full name and organization (e.g., Mr. Chan / ABC Logistics)" },
        { field: "contactChannel", description: "Corporate email or preferred instant messaging contact" },
        { field: "businessPainPoint", description: "Specific operational bottleneck (e.g., invoice OCR to ERP, customer service RAG, cross-system sync)" },
        { field: "preferredSchedule", description: "Target consulting time window (e.g., next Tuesday afternoon)" }
      ],
      acknowledgmentMessage: "Your advisory consultation request has been logged. Our pipeline has instantly dispatched your briefing to our Controllable AI Automation Architect. A specialist will confirm your session time and present an initial solution framework within 24 hours."
    },

    humanEscalation: {
      triggerConditions: [
        "Explicit request for human takeover (e.g., 'talk to a human', '真人客服')",
        "Vector RAG retrieval confidence score falling below 0.80 threshold",
        "Deep custom contract or enterprise SLA negotiations exceeding standard tool parameters"
      ],
      action: "Execute instant 3-second webhook dispatch syncing the full conversation transcript and context summary directly to the architect's operational monitoring system.",
      standardResponse: "Human escalation protocol initiated. The full transcript of your inquiry has been routed to our Controllable AI Automation Architect. A specialist will seamlessly take over to assist you shortly."
    },

    safetyAndTerminologyRules: {
      forbiddenTerms: [
        { term: "防炸容災", replacement: "fault-tolerant failover mechanism or controllable automation workflow" },
        { term: "send to personal mobile/WhatsApp", replacement: "specialist real-time takeover protocol or architect monitoring console" }
      ],
      zeroHallucinationPolicy: "Always anchor strictly within verified documentation. When details are missing, state limitations clearly and invoke the booking intake or escalation protocol rather than speculating."
    }
  },

  tools: [
    {
      id: "edumind-ai",
      name: "EduMind AI Hong Kong",
      targetAudience: "Preschool, primary, secondary (HKDSE), university, and adult continuous professional development.",
      coreFunction: "End-to-end educational loop combining step-by-step reasoning explanations with dynamically generated self-assessment quiz assessments.",
      architecture: {
        visionLayer: "Proprietary high-precision OCR vision API supporting mobile photo snapshots, screenshots, and file uploads. Normalizes handwriting, typography, bilingual text, and complex STEM formulas directly into the prompt stream.",
        inferenceEngine: "Direct native OpenAI flagship model pipeline (without intermediary censorship proxy layers), dynamically executing grade-tailored pedagogical prompts.",
        orchestration: "n8n workflow engine analyzes incorrect attempts, extracts core cognitive blind spots, and generates 3-5 original targeted quiz questions on the fly.",
        failover: "Integrated confidence sentinel triggering a 3-second seamless escalation to human educational specialists."
      },
      faqs: [
        { q: "Can it recognize messy student handwriting?", a: "Yes. The OCR engine includes image enhancement preprocessing to normalize tilt, lighting, and pen strokes." },
        { q: "Are quiz questions drawn from a static bank?", a: "No. Every quiz is dynamically authored in real time by the model to target the student's specific knowledge gaps." }
      ]
    },

    {
      id: "enterprise-ai-helpdesk",
      name: "Dedicated Enterprise AI Helpdesk",
      targetAudience: "Highly regulated industries (Insurance, Healthcare, Legal, Corporate Compliance).",
      coreFunction: "Zero-hallucination interactive support engine locked strictly to corporate policy documents and standard operating procedures.",
      architecture: {
        chunkingLayer: "Granular clause-level document segmentation preserving clause numbers, revision dates, and hierarchical precedence metadata.",
        ragPipeline: "Private vector database stores high-dimensional embeddings. Semantic search extracts the top 3-5 relevant clauses to ground model generation.",
        guardrails: "Strict threshold gating (confidence < 0.80 triggers refusal-to-hallucinate) coupled with instant 3-second escalation to staff.",
        dataPrivacy: "Strict enterprise API terms ensure client data is never ingested into public foundation model training corpora."
      },
      faqs: [
        { q: "How is zero hallucination guaranteed?", a: "Negative constraint prompting forbids speculation; if the vector retrieval yields no matching clause, the bot proactively declines and routes to a human." }
      ]
    },

    {
      id: "master-tools-library",
      name: "Lazy Free Master Tools Library",
      targetAudience: "Professionals requiring ultra-private, fast operational utilities.",
      coreFunction: "Suite of client-side utilities including OmniDiff (document/image difference comparison), Token Price Calculator, and AI Prompt Flow.",
      architecture: {
        runtime: "100% in-memory client-side execution within the user's browser.",
        security: "Zero cloud relay, zero external API transmission, and zero server-side access logs. Data is purged upon closing the browser tab.",
        algorithm: "Dual-column structural text diffing and layered pixel-difference image rendering."
      },
      faqs: [
        { q: "Is uploading confidential contracts safe?", a: "Completely safe. Processing never leaves local browser memory; no network packets are sent." }
      ]
    },

    {
      id: "ai-intel-agency",
      name: "Lazy AI Intelligence Bureau",
      targetAudience: "Decision makers and technologists tracking AI commercial applications in Hong Kong.",
      coreFunction: "Curated tech intelligence pipeline distilling breakthroughs and providing critical commentary through a localized Hong Kong business lens.",
      architecture: {
        ingestion: "Automated n8n Schedule Trigger aggregating GitHub Trending, lab publications, and corporate release notes.",
        processing: "OpenAI semantic clustering eliminates redundant press releases and ranks industry applicability.",
        reviewPipeline: "Hybrid workflow combining algorithmic synthesis with Architect verification."
      }
    },

    {
      id: "transit-hub",
      name: "Transit Hub (貼地通)",
      targetAudience: "Hong Kong commuters and business travelers.",
      coreFunction: "Ad-free, low-latency transit ETA dashboard aggregating MTR, franchised buses (KMB, Citybus), green minibuses, and Light Rail.",
      architecture: {
        dataConnector: "Direct streaming integration with official DATA.GOV.HK public transit APIs.",
        optimization: "Client-side debouncing and dynamic polling control to maintain responsiveness under unstable network conditions.",
        privacy: "Route preferences and favorites are stored purely in client-side LocalStorage."
      }
    },

    {
      id: "smart-deal",
      name: "SmartDeal (慳真D)",
      targetAudience: "Smart consumers and retail pricing intelligence analysts.",
      coreFunction: "Historical supermarket commodity price tracking revealing true 30/60/90-day discounts and identifying artificial promotional markups.",
      architecture: {
        scrapingEngine: "Automated n8n schedulers harvest price registries from consumer councils and supermarket listings.",
        etlPipeline: "Automated unit normalization converting multi-buy promotions into standardized per-unit pricing within a structured time-series database.",
        visualization: "Dynamic front-end chart rendering historical floor prices."
      }
    },

    {
      id: "soul-oasis",
      name: "Soul Oasis (心靈補給站)",
      targetAudience: "Users seeking quiet reflection and spiritual realignment.",
      coreFunction: "Emotion-aware guided prayer generation and meditative reflection based on current personal feelings and challenges.",
      architecture: {
        nlpLayer: "OpenAI semantic parsing identifies underlying emotional tone (e.g., anxiety, exhaustion, gratitude).",
        contentPipeline: "Empathetic structure generating a 3-stage reflection (listening ➔ scriptural/philosophical calming ➔ release prayer).",
        privacySandbox: "Strict ephemeral processing where personal confessions are purged immediately after rendering."
      }
    },

    {
      id: "weather-sentinel",
      name: "Weather Sentinel (Hong Kong · Zhongshan)",
      targetAudience: "Cross-border professionals and daily commuters in the Greater Bay Area.",
      coreFunction: "Real-time micro-climate monitoring and proactive storm/typhoon notifications delivered in authentic Cantonese.",
      architecture: {
        pollingEngine: "n8n executes 1-minute high-frequency polling against HK Observatory and regional meteorological APIs.",
        debounceSystem: "15-minute hysteresis debounce filter eliminates erratic notification spam around threshold temperatures.",
        bypassSentinel: "Emergency bypass routing for critical alerts (e.g., Pre-T8 or Black Rainstorm signals) for sub-second dispatch."
      }
    }
  ],

  enterpriseSolutions: [
    {
      id: "finance-invoice-to-erp",
      name: "Smart Invoice to ERP & Finance Automation",
      painPoint: "Scattered invoice formats require tedious manual data entry, creating approval bottlenecks and blind spots in cash flow visibility.",
      pipeline: "Photo/Email Upload ➔ Vision OCR text extraction ➔ OpenAI JSON schema & arithmetic validation ➔ n8n writes records to ERP/Xero with audit logs.",
      deliverables: [
        { icon: "📊", title: "Live Executive Expense BI Dashboard", detail: "Real-time departmental spend velocities, burn rates, budget overage alerts, and vendor breakdown charts." },
        { icon: "📑", title: "Automated Accounting Vouchers", detail: "Direct automated journal entry into ERP / Xero with attached traceability audit trails." },
        { icon: "⚡", title: "Sub-10-Second Processing", detail: "Invoice reconciliation time slashed from 3 business days to under 10 seconds." }
      ]
    },
    {
      id: "logistics-po-match",
      name: "Delivery Note & Purchase Order Automated Matching",
      painPoint: "Manual visual verification between paper delivery receipts and system POs causes delayed intakes and missing inventory.",
      pipeline: "Warehouse Snap ➔ Vision model extracts SKUs and delivered quantities ➔ Code node matches against database POs ➔ Auto-intake if matched; automated escalation if mismatched.",
      deliverables: [
        { icon: "📈", title: "Live Logistics Operations Dashboard", detail: "Dynamic stock level heatmaps, real-time shortage alerts, and supplier fulfillment reliability ratings." },
        { icon: "📋", title: "Automated Variance Checklist", detail: "Instant identification of surplus or shortfall counts with automatic purchase order closure." },
        { icon: "🚨", title: "Instant Dispute Dispatch", detail: "Automatic ticket generation and routing to procurement teams when discrepancies occur." }
      ]
    },
    {
      id: "contract-kyc-ingestion",
      name: "Contract & Identity Document Structured Ingestion",
      painPoint: "Manual discovery of compliance clauses, renewal deadlines, and ID archival is labor-intensive and creates regulatory risk.",
      pipeline: "Document Scan ➔ Client-side sensitive field redaction ➔ LLM key-value extraction ➔ Ingestion into isolated database with automated audit schedules.",
      deliverables: [
        { icon: "🧭", title: "Contract Lifecycle & Risk Radar Dashboard", detail: "30/60/90-day renewal countdown visualizers and automated compliance risk rating meters." },
        { icon: "🛡️", title: "Privacy-Compliant Master Database", detail: "Structured, searchable database with sensitive personal identifiers automatically masked." },
        { icon: "🔔", title: "Zero-Gap Renewal Automation", detail: "Scheduled background sweeps triggering automated reminder cadences to avoid contract lapses." }
      ]
    }
  ]
};
