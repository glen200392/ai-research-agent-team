# US AI Investment Pipeline

Daily automated analysis of US AI stocks. Runs at **22:00 TST** every day (after US market close).

## Stock Universe

### Core Pool (Always Screened)
| Ticker | Name | Category |
|--------|------|----------|
| NVDA | NVIDIA | AI Chips |
| MSFT | Microsoft | Cloud + AI Platform |
| GOOGL | Alphabet | AI Search + Cloud |
| META | Meta Platforms | AI Social + LLM |
| AMZN | Amazon | Cloud (AWS) |
| AAPL | Apple | Consumer AI |
| SMCI | Super Micro Computer | AI Server |
| DELL | Dell Technologies | AI Server |
| AMD | Advanced Micro Devices | AI Chips |
| AVGO | Broadcom | AI Networking |
| QCOM | Qualcomm | Edge AI |
| INTC | Intel | AI PC + Data Center |

### Dynamic Screener
Stocks with **+20% return over past 20 trading days** are added to analysis list (momentum bonus +0.5 to composite score).

## Pipeline Stages

```
Stage 0.5  → US Macro Score (FRED + yfinance SPY/QQQ/DXY/VIX + CPI/PCE news)
Stage 1    → Dynamic Screener (20-day momentum filter) + Market Research
Stage 1.5  → Sentiment Analysis
Stage 2    → Technical Analysis + Regime Detection
Stage 3    → Fundamental Snapshot (P/E, Forward P/E, EV/EBITDA, AI CapEx exposure)
Stage 4    → 4-Factor Scoring (Macro 25% + Sentiment 20% + Technical 30% + Fundamental 25%) + Kelly + Momentum Bonus
Stage 5    → CVaR Risk (95%/99%) + 4 stress scenarios (recession, Fed re-hike, AI CapEx cut, geopolitical)
Stage 5.5  → 6 charts: radar, Kelly pie, CVaR bar, momentum ranking, K-line, sentiment scatter
Stage 6a   → PDF generation
Stage 6b   → HTML email + PDF attachment
```

## Output Format
- **PDF:** 7-chapter report in Traditional Chinese + Chapter 7 Global Perspective (EN)
- **Email subject:** `【美股 AI 日報】YYYY-MM-DD — Macro: X/10 | Top Pick: TICKER +X%`
- **Filename:** `us_ai_daily_YYYYMMDD.pdf`

## Global Perspective (EN) Fields
Each stock includes English-language fields from institutional sources:
- `institutional_flows` — GS/MS/JPM institutional positioning
- `wall_street_consensus` — Buy/Hold/Sell ratio from Bloomberg consensus
- `earnings_revision_trend` — EPS estimate revision direction
- `index_weight` — S&P 500 / NASDAQ 100 weight and ETF flows
- `macro_tail_risk_en` — Fed policy tail risk estimate

## Notes
- Dynamic screener runs fresh each day — universe expands when AI momentum is strong
- Momentum bonus capped at +1.0 to composite score
- Stress scenario: AI CapEx large-scale reduction is highest-probability tail risk
