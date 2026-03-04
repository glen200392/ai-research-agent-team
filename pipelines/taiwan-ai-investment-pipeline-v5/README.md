# Taiwan AI Investment Pipeline v5

Daily automated analysis of Taiwan AI supply chain stocks. Runs at **07:00 TST** every day.

## Stock Universe

### Core Targets (Always Analyzed)
| Ticker | Name | Category |
|--------|------|----------|
| 2330 | TSMC | Foundry |
| 2317 | Hon Hai / Foxconn | AI Server Assembly |
| 3711 | ASE Technology | Packaging & Testing |
| 6669 | Wiwynn | AI Server ODM |
| 2382 | Quanta Computer | Cloud Server ODM |
| 2454 | MediaTek | Fabless SoC |
| 2308 | Delta Electronics | Power Management |
| 2303 | UMC | Foundry |

### Supply Chain Temperature (Stage 0.3) — 15 Companies
**Upstream:** 6488 GlobalWafers, 3016 Episil, 3680 Favite, 6196 Simplo, 2404 Han Tang
**Midstream:** 2303 UMC, 3711 ASE, 2449 KYEC, 3264 Unimos, 8150 Nan Mao
**Downstream:** 6669 Wiwynn, 2356 Inventec, 2382 Quanta, 3231 Wistron, 2059 Chuan Hu

## Pipeline Stages (9 Stages)

```
Stage 0.5  → Macro Score (FRED + yfinance + IMF + PMI)
Stage 0.3  → Supply Chain Temperature (MOPS monthly revenue scraping)
Stage 1    → Market Research + Earnings Call NLP
Stage 1.5  → Sentiment Analysis (news + PTT + institutional)
Stage 2    → Technical Analysis + Regime Detection (Bull/Bear/Choppy)
Stage 3    → Fundamental Analysis (P/E, DCF, customer concentration)
Stage 4    → 5-Factor Scoring (Macro 20% + SC 20% + Sentiment 20% + Technical 25% + Fundamental 15%) + Kelly
Stage 5    → CVaR Risk (95%/99%) + 4 stress scenarios + SC contraction auto-tighten 20%
Stage 5.5  → 6 charts: radar, Kelly pie, CVaR bar, SC heatmap, K-line, sentiment scatter
Stage 6a   → PDF generation (pdf_report_generator.py)
Stage 6b   → HTML email + PDF attachment
```

## Output Format
- **PDF:** 7-chapter report in Traditional Chinese + Chapter 7 Global Perspective (EN)
- **Email:** HTML summary with macro score, SC temperature, top 3 picks, risk warnings
- **Filename:** `taiwan_ai_daily_YYYYMMDD.pdf`

## Special Features
- **Supply Chain Temperature Score:** Unique 3-layer (upstream/midstream/downstream) revenue momentum scoring
- **NLP Transcript Scoring:** TSMC earnings call keyword extraction (demand signals, inventory signals, pricing signals)
- **SC Regime Auto-adjustment:** CVaR threshold tightens 20% when SUPPLY_CONTRACTION detected
- **5-Factor Weighting:** Macro Regime dynamically adjusts factor weights

## Notes
- MOPS data available after 10th of each month (monthly revenue)
- FRED data is free but requires API key: https://fred.stlouisfed.org/docs/api/api_key.html
- Supply Chain Temperature uses web_scrape on MOPS; fallback to web_search if scraping fails
