# Japan AI Investment Pipeline

Daily automated analysis of Japan AI stocks. Runs at **22:00 TST** every day (parallel with US pipeline).

## Stock Universe

### Core Pool
| Ticker | Name | Category |
|--------|------|----------|
| 8035 | Tokyo Electron (TEL) | Semiconductor Equipment |
| 4063 | Shin-Etsu Chemical | Silicon Wafer |
| 6758 | Sony Group | AI Sensors + Entertainment |
| 6981 | Murata Manufacturing | Electronic Components |
| 9984 | SoftBank Group | AI Investment / ARM |
| 6702 | Fujitsu | AI Enterprise IT |
| 6701 | NEC Corporation | AI Government IT |
| 6501 | Hitachi | AI Industrial |
| 6723 | Renesas Electronics | Automotive AI Chips |
| 6861 | Keyence | Factory Automation / AI Vision |

Dynamic screener adds stocks with +20% momentum over 20 trading days.

## Pipeline Stages

```
Stage 0.5  → Japan Macro Score (Nikkei/TOPIX/JPY/VIX + BOJ policy + CPI/PMI news)
Stage 1    → Dynamic Screener + Market Research (TSE foreign flow + global supply chain)
Stage 1.5  → Sentiment Analysis (Japanese + English sources)
Stage 2    → Technical Analysis + JPY impact overlay
Stage 3    → Fundamental Analysis + JPY earnings sensitivity (EPS per 1 JPY move)
Stage 4    → 4-Factor Scoring + JPY Risk Adjustment (USD/JPY ↓ + overseas revenue >50% → Fundamental -0.5) + Kelly
Stage 5    → CVaR Risk + 4 JPY-specific stress scenarios
Stage 5.5  → 6 charts: radar (with JPY risk flag), Kelly pie, CVaR bar, JPY sensitivity scatter, K-line, sentiment scatter
Stage 6a   → PDF generation
Stage 6b   → HTML email + PDF attachment
```

## JPY Risk Adjustment (Unique Feature)
When **USD/JPY falls** (JPY strengthens) AND a stock has **overseas revenue > 50%**:
- Fundamental Score automatically reduced by 0.5
- This reflects export earnings headwind from JPY appreciation

## Stress Scenarios
1. **JPY rapid appreciation** — extreme scenario: USD/JPY drops to 130, impact on export earnings
2. **BOJ aggressive rate hike** — 3-hike scenario, portfolio drawdown estimate
3. **China AI demand slowdown** — impact on Japan component suppliers (Murata, Renesas, TEL)
4. **International institutional withdrawal** — TSE foreign investor net selling scenario

## Global Perspective (EN) Fields
- `foreign_net_buying` — TSE foreign investor net buy/sell in JPY billion
- `boj_policy_risk_en` — BOJ rate hike path and estimated portfolio drawdown
- `jpy_earnings_sensitivity` — EPS impact per 1 JPY move vs USD
- `msci_japan_weight` — MSCI Japan index weight and recent rebalancing
- `carry_trade_risk_en` — JPY carry unwind risk and estimated portfolio impact

## Output Format
- **PDF:** 7-chapter report in Traditional Chinese + Chapter 7 Global Perspective (EN)
- **Email subject:** `【日股 AI 日報】YYYY-MM-DD — Macro: X/10 | Top Pick: TICKER`
- **Filename:** `japan_ai_daily_YYYYMMDD.pdf`

## Notes
- All prices in JPY; PDF reports converted context to TWD/USD where relevant
- TEL (8035) is the key bellwether — tracks global semiconductor equipment cycle
- SoftBank (9984) has high beta to ARM/AI theme; weight carefully with Kelly criterion
