---
slug: japan-ai-investment-pipeline-daily-pdf-email-report-2200-tst
title: Japan AI Investment Pipeline — Daily PDF Email Report (22:00 TST)
steps:
- description: 'Stage 0.5 — 日本總體環境評分 (Japan Macro Scoring): 抓取日本總體指標：(1) yfinance
    抓取 Nikkei 225 (^N225)、TOPIX (^TOPX)、日圓/美元匯率 (JPY=X)、VIX；(2) web_search 查詢日本最新
    CPI、日銀 BOJ 利率政策方向、PMI、貸幣增長率；(3) 計算日本 Macro Score (0-10) 與 Japan Macro Regime (RISK-ON/NEUTRAL/RISK-OFF)，特別註意日圓貨幣趨勢對日本出口商的影響；(4)
    輸出結構化 JSON 給後續所有 Stage 使用。'
  agent_id: agt_0699ef74e08b7ce480001ac84958d0db
  agent_slug: macro-score-pipeline-stage
  format_guide: '輸出 JSON：{macro_score: float, macro_regime: string, indicators: {nikkei_trend,
    topix_trend, jpy_usd: {value, trend, impact_on_exporters}, boj_policy: {direction,
    signal}, japan_cpi, japan_pmi}, sector_outlook: {ai_semiconductor, industrial_robot,
    cloud_software, exporters}, pipeline_instruction: string}。繁體中文總體環境摘要（2-3句），說明日元趨勢及
    BOJ 政策對日本 AI/半導體股的影響。'
- description: 'Stage 1 — 動態篩選 + 市場研究 (Japan AI Screener + Market Research): 分兩軌執行：(A)
    動態篩選：使用 yfinance 抓取核心標的池（TEL/8035、信越化學/4063、Sony/6758、村田/6981、SoftBank/9984、Fujitsu/6702、NEC/6701、Hitachi/6501、Renesas/6723、Keyence/6861）過去
    20 交易日漲幅，篩出漲幅 ≥20% 的標的；同時 web_search 識別日本 AI 概念強勢標的，組合成 10-12 檔分析清單；(B) 市場研究：搜尋日本
    AI/半導體市場最新發展、政府 AI 投資政策、BOJ 政策對股市影響、法人外資動向。'
  agent_id: agt_0697b528d8ff7d4580007a1fa9e54a9e
  agent_slug: market-research-analyst
  format_guide: '輸出：(1) 漲幅篩選結果表（ticker、公司名、20日漲幅%、篩選狀態），(2) 市場研究摘要（繁體中文），(3) 日本 AI
    主題流影鏈清單，(4) 建議分析標的 JSON：[{ticker, name, exchange: TSE, sector, 20d_return_pct,
    momentum_flag, reason, jpy_sensitivity: HIGH/MED/LOW}]。'
- description: 'Stage 1.5 — 情緒分析 (Japan Sentiment Analysis): 對 Stage 1 篩選後的日本標的，整合日文與英文情緒來源：日經、Bloomberg
    Japan、Reuters Japan、Nikkei Asia 新聞標題、法人報告等。計算每檔 Sentiment Score (0-10)、情緒動能與日本市場整體情緒讀數。'
  agent_id: agt_0699ef88cbe779d380004859b6076cb1
  agent_slug: sentiment-aggregation-analyzer
  format_guide: '輸出 JSON：{market_sentiment: {score, regime, label, japan_specific_notes},
    stocks: [{ticker, name, sentiment_score, sentiment_label, sentiment_momentum,
    confidence, risk_flags, key_headlines}]}。繁體中文情緒摘要，特別說明日元影響及外資動向。'
- description: 'Stage 2 — 技術分析 (Japan Technical Analysis): 對篩選日本標的執行完整技術分析：SMA/EMA、RSI、MACD、布林帶、ATR、Fibonacci
    層、體制偵測、型態識別。註意日本市場漸允機構特性（外資流入流出對日股的影響）。輸出 Technical Score (0-10)、進出場區間、止損位、目標價。'
  agent_id: agt_0697b541706f7e628000b0a73cb957eb
  agent_slug: technical-analysis-expert
  format_guide: '輸出 JSON：{stocks: [{ticker, exchange: TSE, regime, technical_score,
    entry_zone, targets:[T1,T2,T3], stop_loss, atr, rr_ratio, pattern, signal_type,
    foreign_flow_signal: INFLOW/OUTFLOW/NEUTRAL}]}。繁體中文技術分析摘要表格。'
- description: 'Stage 3 — 基本面摘要 (Japan Fundamental Snapshot): 對篩選日本標的執行基本面分析：P/E（參考日本市場平均市盈率）、EV/EBITDA、ROE、毛利率趨勢、海外營收佔比（日圓敏感度）、AI
    相關投資計劃能見度、競爭護城河。輸出 Fundamental Score (0-10) 及投資建護。'
  agent_id: agt_0697b55daeb9751b800061ba767d1167
  agent_slug: fundamental-analysis-advisor
  format_guide: '輸出 JSON：{stocks: [{ticker, fundamental_score, valuation: {pe, ev_ebitda,
    roe_pct, overseas_revenue_pct}, moat_rating, ai_exposure: HIGH/MEDIUM/LOW, jpy_risk:
    HIGH/MED/LOW, key_strengths, key_risks, recommendation: BUY|HOLD|AVOID}]}。繁體中文基本面摘要，特別說明日元貨幣風險。'
- description: 'Stage 4 — 四維度整合評分 + Kelly Criterion 倉位 (Japan Portfolio Coordinator):
    整合上游輸出，執行四維度評分矩陣：Macro 25% + Sentiment 20% + Technical 30% + Fundamental 25%。計算
    Composite Score (0-10)，使用 0.5x Fractional Kelly Criterion 計算倉位。日元風險修正：日元貨幣趨剴（USD/JPY
    下降）且海外營收佔比 >50% 的標的，對 Fundamental Score 自動下調 0.5。漲幅 ≥20% 加分 0.5（最多 +1）。'
  agent_id: agt_0697b57e7d3e7b3e8000ae9d0b00238b
  agent_slug: investment-report-coordinator
  format_guide: '輸出：(1) 每股四維度評分表，(2) Kelly 倉位表，(3) 日元風險修正說明，(4) 三情境分析。JSON：{stocks:
    [{ticker, composite_score, macro_s, sentiment_s, technical_s, fundamental_s, jpy_adjustment,
    momentum_bonus, kelly_half, suggested_pct, entry, stop_loss, regime}], total_invested_pct,
    cash_pct}。繁體中文輸出。'
- description: 'Stage 5 — 風控評估 + CVaR 驗證 (Japan Risk Management): 對 Stage 4 倉位建護執行
    CVaR（95%/99%）計算。壓力測試情境：(1) 日元急送上漲（BOJ 激進加息），(2) 山虫隨 AI 投資失誘，(3) 中日貿易絊紛，(4) 日本漸允機構大幅撤資。依波動率體制調整倉位乘數，對每檔輸出
    APPROVED / REDUCED / REJECTED 裁決。'
  agent_id: agt_0697b56ef4077e078000f5b423297f82
  agent_slug: portfolio-risk-management-advisor
  format_guide: 輸出：(1) CVaR 摘要表，(2) 壓力測試結果（四個日本特定情境），(3) 波動率體制旗標，(4) 最終核准倉位表，(5) 每股風控判決。繁體中文輸出
    + 最終 JSON。
- description: 'Stage 6 — 整合 PDF 報告生成 + 合併 Email 寄送 (Japan Daily Report + Combined
    Email): 接收所有上游 Stage 的繁體中文輸出，整合為單一完整 PDF 日股 AI 投資日報。報告結構：(1) 封面；(2) 目錄；(3) 第一章：日本總體環境（Nikkei、BOJ、日元趨勢）；(4)
    第二章：動能篩選結果；(5) 第三章：情緒與技術分析；(6) 第四章：基本面摘要；(7) 第五章：投資組合建護；(8) 第六章：風控報告。報告完成後，將日股
    PDF 儲存為 reports/japan_ai_daily_{YYYYMMDD}.pdf，並以 Email 寄送 PDF 至 glen200392@gmail.com，主旨：【日股
    AI 日報】YYYY-MM-DD — Nikkei 體制: {regime} | Top Pick: {ticker}，Email 正文包含當日日本市場核心摘要：BOJ
    政策訊號、日元趨勢對出口商影響、前三大推薦及倉位%。'
  agent_slug: nebula
  format_guide: '步驟：(1) 將所有 Stage 繁體中文輸出依章節合併，加入封面、目錄；(2) text_editor create 儲存為 reports/japan_ai_daily_{YYYYMMDD}.pdf；(3)
    send_email 寄送至 glen200392@gmail.com，主旨格式：【日股 AI 日報】{YYYY-MM-DD} — Nikkei 體制: {regime}
    | Top Pick: {ticker}。'
---

日股 AI 投資日報自動化 Pipeline，每日 22:00（Asia/Taipei）與美股報告同步執行。核心標的池：東京威力科創（TEL/8035）、信越化學（4063）、索尼（6758）、村田製作所（6981）、SoftBank Group（9984）、Fujitsu（6702）、NEC（6701）、Hitachi（6501）、Renesas（6723）、Keyence（6861）。加上動態篩選近期漲幅 20%+ 的日本 AI 概念股。最終整合為單一 PDF，與美股報告合併在同一封 Email 寄送至 glen200392@gmail.com。