# AI Research Agent Team 🤖

**A production-ready multi-agent system for automated AI technology intelligence reports.**

> Clone it. Add your API keys. Run it. Get a comprehensive AI research report every month — automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework Support](https://img.shields.io/badge/frameworks-LangGraph%20%7C%20CrewAI%20%7C%20AutoGen%20%7C%20Nebula-green.svg)]()

---

## 📖 What This Does

This project automates the creation of monthly AI technology development reports by coordinating a team of 7 specialized AI agents. Each agent has a distinct role — from gathering intelligence across 6 parallel search streams, to writing and fact-checking the final report, to delivering it via email and file storage.

**Output example:** A 2,500-word research report covering model releases, open-source developments, technical breakthroughs, hardware landscape, agent architecture trends, and competitive dynamics — sourced, fact-checked, and formatted for multiple platforms.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  RESEARCH ORCHESTRATOR                       │
│         Task dispatch · Progress monitoring · Integration    │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────▼───────────────┐
           │         INTEL COLLECTOR        │
           │   6 parallel search streams    │
           │  A:arXiv B:Labs C:OSS D:HW    │
           │      E:Breakthroughs F:Biz     │
           └───────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌─────────────────┐       ┌─────────────────┐
    │  TECH ANALYST   │       │ MARKET ANALYST  │
    │ Architecture ·  │       │ Funding · M&A · │
    │ Benchmarks ·    │       │ Regulation ·    │
    │ OSS vs Closed   │       │ Geo-strategy    │
    └────────┬────────┘       └────────┬────────┘
             └──────────┬─────────────┘
                        ▼
             ┌─────────────────────┐
             │  CONTENT SYNTHESIZER │
             │  Long-form · LinkedIn│
             │  Email digest (ZH-TW)│
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │    QUALITY GATE     │
             │ Fact-check · Score  │
             │ >= 85/100 to pass   │
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │   DELIVERY AGENT    │
             │  Email · File · API │
             └─────────────────────┘
```

### The 7 Agents

| Agent | Role | Key Responsibility |
|-------|------|-------------------|
| `ResearchOrchestrator` | Commander | Coordinates all agents, integrates results |
| `IntelCollector` | Gatherer | 6-stream parallel web intelligence collection |
| `TechAnalyst` | Analyst | Deep technical analysis of models & architectures |
| `MarketAnalyst` | Strategist | Competitive dynamics, funding, regulation |
| `ContentSynthesizer` | Writer | Multi-format content in Traditional Chinese |
| `QualityGate` | Reviewer | 100-point fact-check & editorial QA |
| `DeliveryAgent` | Publisher | Multi-channel delivery (email, file, API) |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-research-agent-team.git
cd ai-research-agent-team
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API keys

```bash
cp .env.example .env
# Edit .env with your keys (see Configuration section below)
```

### 4. Choose your framework and run

**LangGraph (recommended):**
```bash
python frameworks/langgraph/run.py --month 2026-02
```

**CrewAI:**
```bash
python frameworks/crewai/run.py --month 2026-02
```

**AutoGen:**
```bash
python frameworks/autogen/run.py --month 2026-02
```

**Nebula (no-code):**
See `frameworks/nebula/TASK.md` — import directly into Nebula.

---

## 🔑 Configuration

### Required API Keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
# LLM Provider (choose one or multiple)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Search (required for Intel Collector)
TAVILY_API_KEY=tvly-...        # Recommended
# OR
SERPER_API_KEY=...             # Alternative

# Delivery (optional — configure what you use)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASSWORD=...
REPORT_EMAIL_RECIPIENT=your@email.com
```

### Report Configuration

Edit `config/config.yaml`:

```yaml
report:
  language: "zh-TW"           # zh-TW | en | ja
  target_month: "auto"        # "auto" = last month, or "2026-02"
  output_formats:
    - long_form                # 2000-3000 word report
    - linkedin_post            # 600-900 words
    - email_digest             # 400-500 words

delivery:
  email:
    enabled: true
    recipient: "your@email.com"
  file:
    enabled: true
    output_dir: "./reports/"
  
quality:
  min_score: 85               # 0-100, reports below this are revised
  max_revisions: 2
```

---

## 📁 Project Structure

```
ai-research-agent-team/
├── README.md
├── .env.example
├── requirements.txt
├── config/
│   └── config.yaml               # Main configuration
├── prompts/                      # All 7 agent system prompts
│   ├── 01_research_orchestrator.md
│   ├── 02_intel_collector.md
│   ├── 03_tech_analyst.md
│   ├── 04_market_analyst.md
│   ├── 05_content_synthesizer.md
│   ├── 06_quality_gate.md
│   └── 07_delivery_agent.md
├── frameworks/                   # Framework-specific implementations
│   ├── langgraph/
│   │   ├── run.py
│   │   ├── graph.py              # State graph definition
│   │   ├── nodes.py              # Each agent as a node
│   │   └── state.py              # Shared state schema
│   ├── crewai/
│   │   ├── run.py
│   │   ├── agents.py             # Agent definitions
│   │   ├── tasks.py              # Task definitions
│   │   └── crew.py               # Crew assembly
│   ├── autogen/
│   │   ├── run.py
│   │   ├── agents.py
│   │   └── groupchat.py
│   └── nebula/
│       └── TASK.md               # Nebula recipe (import directly)
├── tools/                        # Shared tool implementations
│   ├── search.py                 # Web search wrapper
│   ├── scrape.py                 # Web scraping
│   ├── extract.py                # Structured extraction
│   └── deliver.py                # Email & file delivery
├── schemas/                      # JSON schemas for agent communication
│   ├── intel_collection.json
│   ├── tech_analysis.json
│   ├── market_analysis.json
│   ├── content_package.json
│   └── qa_report.json
├── reports/                      # Generated reports (gitignored)
│   └── .gitkeep
└── examples/
    └── 2026-02-sample-report.md  # Example output
```

---

## 🔬 How the Research Pipeline Works

### Phase 1 — Intelligence Collection (Parallel)

The `IntelCollector` runs 6 search streams simultaneously:

| Stream | Topic | Primary Sources |
|--------|-------|----------------|
| A | Academic papers | arxiv.org (cs.AI, cs.CL, cs.LG) |
| B | Lab announcements | openai.com, anthropic.com, deepmind.google |
| C | Open-source | HuggingFace, GitHub, paperswithcode |
| D | Hardware | NVIDIA, AMD, TSMC, cloud providers |
| E | Breakthroughs | nature.com, science.org, MIT News |
| F | Business | Crunchbase, Reuters, TechCrunch |

Each item is scored: `Relevance (0-10) × Credibility (0-10) × Freshness (0-10)` — items below 18/30 are discarded.

### Phase 2 — Analysis (Parallel)

`TechAnalyst` and `MarketAnalyst` run in parallel:
- Tech: model architectures, benchmarks, OSS vs. closed gap
- Market: funding flows, M&A, regulation, competitive positioning

### Phase 3 — Content Generation

`ContentSynthesizer` produces 3 format variants simultaneously:
- **Long-form** (2,000–3,000 words): full report with 6 chapters
- **LinkedIn post** (600–900 words): hook + numbered insights + CTA
- **Email digest** (400–500 words): what happened / why it matters / what's next

### Phase 4 — Quality Gate

100-point scoring system:
- **Factual Accuracy** (40 pts): every number traced to source
- **Structural Completeness** (30 pts): all 6 dimensions covered
- **Editorial Quality** (30 pts): readability, consistency, attribution

Score ≥ 85 → deliver. Score 75–84 → revise once. Score < 75 → reject and restart synthesis.

### Phase 5 — Delivery

Parallel delivery to all configured channels: email, local file, external APIs.

---

## 🌐 Framework Comparison

| Feature | LangGraph | CrewAI | AutoGen | Nebula |
|---------|-----------|--------|---------|--------|
| Parallel execution | ✅ Native | ✅ Async | ✅ GroupChat | ✅ Native |
| State persistence | ✅ Built-in | ⚠️ Manual | ⚠️ Manual | ✅ Built-in |
| Human-in-the-loop | ✅ Interrupt | ⚠️ Limited | ✅ Human proxy | ✅ Built-in |
| Setup complexity | Medium | Low | Medium | Very Low |
| Best for | Production | Rapid prototype | Research | No-code |

---

## 📊 Example Output

See `examples/2026-02-sample-report.md` for a full example report generated by this system.

**Typical report structure:**
1. 月度核心主題 (Monthly Theme Summary)
2. 模型發佈 (Model Releases)
3. 開源生態 (Open Source Ecosystem)
4. 跨領域技術突破 (Cross-Domain Breakthroughs)
5. 硬體與基礎設施 (Hardware & Infrastructure)
6. AI Agent 架構演進 (Agent Architecture Evolution)
7. 競爭格局分析 (Competitive Dynamics)
8. 未來 30-60 天展望 (30-60 Day Outlook)

---

## 🗓️ Scheduling (Automated Monthly Reports)

### Cron (Linux/Mac)

```bash
# Run on the 1st of every month at 8:00 AM
0 8 1 * * cd /path/to/ai-research-agent-team && python frameworks/langgraph/run.py --month auto
```

### GitHub Actions

```yaml
# .github/workflows/monthly-report.yml
on:
  schedule:
    - cron: '0 0 1 * *'   # 1st of month at 00:00 UTC
```

See `.github/workflows/monthly-report.yml` for the full configuration.

---

## 🤝 Contributing

Contributions welcome! Key areas:
- Adding new search sources to Intel Collector
- Supporting additional output languages
- New delivery channels (Slack, Notion, Medium API)
- Additional framework implementations

Please read `CONTRIBUTING.md` before submitting PRs.

---

## 📄 License

MIT License — use freely, attribution appreciated.

---

## 🙏 Acknowledgments

System design based on real-world AI research workflows. Sample report data from publicly available sources. Built to make high-quality AI intelligence accessible to everyone.
