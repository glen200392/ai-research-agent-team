# AI Investment Pipeline — Three-Market Daily Report System

> Automated AI-assisted investment analysis for Taiwan, US, and Japan equity markets.
> Generates structured PDF reports with macro scoring, technical analysis, fundamental analysis,
> Kelly Criterion position sizing, and CVaR risk management — delivered daily by email.

---

## Quick Start (3 Steps)

### Step 1 — Clone & Install
```bash
git clone https://github.com/glen200392/ai-research-agent-team.git
cd ai-research-agent-team
pip install -r requirements.txt
```

### Step 2 — Configure
```bash
cp env.example .env
# Edit .env: add FRED_API_KEY (free), OPENAI_API_KEY or ANTHROPIC_API_KEY, REPORT_EMAIL
```

### Step 3 — Run (choose your mode)

**Option A: Nebula Cloud (recommended — no infrastructure needed)**
- Import the TASK.md files into your Nebula workspace
- Set up cron triggers (07:00 TST for Taiwan, 22:00 TST for US/Japan)
- Reports arrive in your inbox automatically

**Option B: Local execution**
```bash
# Taiwan pipeline
python -c "from tasks.taiwan import run; run()"

# US pipeline  
python -c "from tasks.us import run; run()"

# Japan pipeline
python -c "from tasks.japan import run; run()"
```

---

## Three Pipeline Overview

| Market | Schedule (TST) | Stock Universe | Output |
|--------|---------------|----------------|--------|
| **Taiwan** | 07:00 daily | 2330 TSMC, 2317 Hon Hai, 3711 ASE, 6669 Wiwynn, 2382 Quanta, 2454 MediaTek, 2308 Delta, 2303 UMC + Supply Chain 15 stocks | PDF (繁中) + HTML email |
| **US** | 22:00 daily | NVDA, MSFT, GOOGL, META, AMZN, AAPL, SMCI, DELL, AMD, AVGO, QCOM, INTC + dynamic momentum screener (20-day +20%) | PDF (繁中) + HTML email |
| **Japan** | 22:00 daily | 8035 TEL, 4063 Shin-Etsu, 6758 Sony, 6981 Murata, 9984 SoftBank, 6702 Fujitsu, 6701 NEC, 6501 Hitachi + dynamic screener | PDF (繁中) + HTML email |

---

## Pipeline Architecture (9 Stages)

```
Stage 0.5  Macro Scoring      — FRED yield curve, Fed rate, DXY, VIX → Macro Score (0-10)
Stage 0.3  Supply Chain Temp  — [Taiwan only] MOPS monthly revenue → SC Temperature Score
Stage 1    Market Research    — News, analyst calls, NLP transcript scoring
Stage 1.5  Sentiment Analysis — News + social + institutional → Sentiment Score (0-10)
Stage 2    Technical Analysis — SMA/EMA/RSI/MACD/Bollinger/ATR + regime detection
Stage 3    Fundamental        — P/E, EV/EBITDA, DCF, moat, customer concentration
Stage 4    Composite Scoring  — Weighted multi-factor + Kelly Criterion position sizing
Stage 5    Risk Management    — CVaR 95%/99%, stress tests, APPROVED/REDUCED/REJECTED
Stage 5.5  Chart Generation   — 6 chart types: radar, Kelly pie, CVaR bar, market-specific, K-line, sentiment scatter
Stage 6a   PDF Generation     — pdf_report_generator.py → structured PDF with 7 chapters
Stage 6b   Email Delivery     — HTML email + PDF attachment → REPORT_EMAIL
```

---

## PDF Report Structure (7 Chapters)

| Chapter | Content |
|---------|---------||
| 1 | Multi-factor Radar Chart (composite score breakdown) |
| 2 | Kelly Criterion position allocation + approved position table |
| 3 | CVaR risk management (95%/99%) + stress test results |
| 4 | Market-specific chart (TW: supply chain heatmap / US: momentum ranking / JP: JPY sensitivity) |
| 5 | Technical analysis K-line charts (Top 3 picks) |
| 6 | Sentiment scatter plot |
| 7 | **Global Perspective (EN)** — foreign broker ratings, institutional flows, global AI positioning |

---

## Repository Structure

```
ai-research-agent-team/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── env.example                        # Environment variable template
├── code/
│   └── pdf_report_generator.py        # PDF generation engine (v2, CJK support)
├── tasks/
│   ├── taiwan-ai-investment-pipeline-v5-full-9-stage-analysis.../TASK.md
│   ├── us-ai-investment-pipeline-daily-pdf-email-report-2200-tst/TASK.md
│   └── japan-ai-investment-pipeline-daily-pdf-email-report-2200-tst/TASK.md
├── pipelines/
│   ├── taiwan-ai-investment-pipeline-v5/README.md
│   ├── us-ai-investment-pipeline/README.md
│   └── japan-ai-investment-pipeline/README.md
└── docs/
    ├── README_v2.md                   # Detailed architecture documentation
    └── architecture_design.md         # System design specifications
```

---

## Key Dependencies

| Package | Purpose |
|---------|---------||
| `reportlab>=4.0` | PDF generation with CJK font support |
| `yfinance>=0.2` | Market data (prices, indicators) |
| `fredapi>=0.5` | FRED macro data (yield curve, Fed rate) |
| `plotly>=5.18` + `kaleido` | Interactive charts → PNG export |
| `mplfinance>=0.12` | K-line / candlestick charts |
| `matplotlib>=3.8` + `seaborn>=0.13` | Statistical charts |

---

## Scheduling

| Trigger | Cron | Market | Notes |
|---------|------|--------|-------|
| Taiwan Daily | `0 7 * * *` (07:00 TST) | 台股 | Runs before Taiwan market open |
| US + Japan Daily | `0 22 * * *` (22:00 TST) | 美股 + 日股 | Runs after US market close |

---

## Investment Disclaimer

> This system is for **informational purposes only** and does not constitute investment advice.
> 本系統產生的報告僅供參考，不構成投資建議。投資涉及風險，過去績效不代表未來表現。
> AI-generated analysis may contain errors. Always verify with primary sources before making investment decisions.

---

*Powered by Nebula AI Pipeline v2.1 | Last updated: 2026-03-04*
