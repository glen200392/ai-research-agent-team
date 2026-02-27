---
slug: us-ai-investment-pipeline-daily-pdf-email-report-2200-tst
title: US AI Investment Pipeline — Daily PDF Email Report (22:00 TST)
steps:
- description: 'Stage 0.5 — 美國總體環境評分 (US Macro Scoring): 抓取美國總體指標：(1) FRED CSV 抓取
    T10Y2Y 殖利率利差、FEDFUNDS 利率方向；(2) yfinance 抓取 DXY、VIX、SPY、QQQ；(3) web_search 查詢最新
    CPI、PCE、就業市場數據、Fed 會議記錄信號；(4) 計算美國 Macro Score (0-10) 與 US Macro Regime (RISK-ON/NEUTRAL/RISK-OFF)。輸出結構化
    JSON 給後續所有 Stage 使用。'
  agent_id: agt_0699ef74e08b7ce480001ac84958d0db
  agent_slug: macro-score-pipeline-stage
  format_guide: '輸出 JSON：{macro_score: float, macro_regime: string, indicators: {yield_curve,
    fed_policy, dxy, vix, us_cpi, us_employment}, sector_outlook: {ai_hardware, ai_software,
    cloud, semiconductors}, pipeline_instruction: string}。同時輸出繁體中文總體環境摘要（2-3句），說明當前美國
    Macro Regime 及對 AI 股市的影響。'
- description: 'Stage 1 — 動態篩選 + 市場研究 (Dynamic Screener + Market Research): 分兩軌執行：(A)
    動態篩選：使用 yfinance 抓取核心標的池（NVDA、MSFT、GOOGL、META、AMZN、AAPL、SMCI、DELL、AMD、AVGO、QCOM、INTC）過去
    20 交易日漲幅，篩出漲幅 ≥20% 的標的；同時 web_search 查詢「US AI stocks up 20% past month」、「AI momentum
    stocks 2026」等識別即時強勢標的，組合成 12-15 檔分析清單；(B) 市場研究：搜尋 AI 市場最新發展、法人研究報告、產業催化劑（AI CapEx、法說季度、新品發佈等）。'
  agent_id: agt_0697b528d8ff7d4580007a1fa9e54a9e
  agent_slug: market-research-analyst
  format_guide: '輸出：(1) 漲幅篩選結果表（ticker、公司名、20日漲幅%、篩選狀態: MOMENTUM/WATCHLIST），(2) 市場研究摘要（繁體中文），(3)
    本週 AI 主題催化劑清單，(4) 建議分析標的 JSON 清單：[{ticker, name, sector, 20d_return_pct, momentum_flag,
    reason}]。'
- description: 'Stage 1.5 — 情緒分析 (Sentiment Analysis): 對 Stage 1 篩選後的標的，從新聞標題、法人報告、社群媒體公司句集計情緒訊號。計算每檔
    Sentiment Score (0-10)、情緒動能與市場整體情緒讀數。'
  agent_id: agt_0699ef88cbe779d380004859b6076cb1
  agent_slug: sentiment-aggregation-analyzer
  format_guide: '輸出 JSON：{market_sentiment: {score, regime, label}, stocks: [{ticker,
    name, sentiment_score, sentiment_label, sentiment_momentum, confidence, risk_flags,
    key_headlines}]}。繁體中文情緒摘要。'
- description: 'Stage 2 — 技術分析 (Technical Analysis): 對篩選標的執行完整技術分析：SMA/EMA、RSI、MACD、布林帶、ATR、Fibonacci
    層、體制偵測（Bull/Bear/Choppy）、型態識別。輸出 Technical Score (0-10)、進出場區間、止損位、目標價。'
  agent_id: agt_0697b541706f7e628000b0a73cb957eb
  agent_slug: technical-analysis-expert
  format_guide: '輸出 JSON：{stocks: [{ticker, regime, technical_score, entry_zone, targets:[T1,T2,T3],
    stop_loss, atr, rr_ratio, pattern, signal_type}]}。繁體中文技術分析摘要表格。'
- description: 'Stage 3 — 基本面摘要 (Fundamental Snapshot): 對篩選標的執行快速基本面分析：P/E、Forward
    P/E、EV/EBITDA、毛利率趨勢、ROE、科技幾何成長（AI 投資計劃能見度）、競爭護城河。輸出 Fundamental Score (0-10) 及投資建議。'
  agent_id: agt_0697b55daeb9751b800061ba767d1167
  agent_slug: fundamental-analysis-advisor
  format_guide: '輸出 JSON：{stocks: [{ticker, fundamental_score, valuation: {pe, forward_pe,
    ev_ebitda, revenue_growth_pct}, moat_rating, ai_capex_exposure: HIGH/MEDIUM/LOW,
    key_strengths, key_risks, recommendation: BUY|HOLD|AVOID}]}。繁體中文基本面摘要。'
- description: 'Stage 4 — 四維度整合評分 + Kelly Criterion 倉位 (US Portfolio Coordinator):
    整合上游輸出，執行四維度評分矩陣：Macro 25% + Sentiment 20% + Technical 30% + Fundamental 25%。計算
    Composite Score (0-10)，使用 0.5x Fractional Kelly Criterion 計算倉位。納入動能篩選加成：漲幅 ≥20%
    的標的額外加分 0.5（最多 +1）。'
  agent_id: agt_0697b57e7d3e7b3e8000ae9d0b00238b
  agent_slug: investment-report-coordinator
  format_guide: '輸出：(1) 每股四維度評分表，(2) Kelly 倉位表（p值、b值、Full Kelly f*、0.5x 建議倉位%），(3)
    動能篩選加分說明，(4) 三情境分析（Bull/Base/Bear），(5) JSON：{stocks: [{ticker, composite_score,
    macro_s, sentiment_s, technical_s, fundamental_s, momentum_bonus, kelly_half,
    suggested_pct, entry, stop_loss, regime}], total_invested_pct, cash_pct}。繁體中文輸出。'
- description: 'Stage 5 — 風控評估 + CVaR 驗證 (US Risk Management): 對 Stage 4 倉位建議執行 CVaR（95%/99%）計算（歷史模擬
    + 參數法 + Monte Carlo）。壓力測試情境：(1) 美國送入衰退，(2) Fed 重新升息衽擊，(3) AI CapEx 大幅削減，(4) 地緣政治風險。依波動率體制調整倉位乘數，對每檔輸出
    APPROVED / REDUCED / REJECTED 裁決。'
  agent_id: agt_0697b56ef4077e078000f5b423297f82
  agent_slug: portfolio-risk-management-advisor
  format_guide: 輸出：(1) CVaR 摘要表，(2) 壓力測試結果，(3) 波動率體制旗標，(4) 最終核准倉位表，(5) 每股風控判決。繁體中文輸出
    + 最終 JSON。
- description: 'Stage 6 — 整合 PDF 報告生成 + Email 寄送 (US Daily Report): 接收所有上游 Stage 的繁體中文輸出，整合為單一完整
    PDF 美股 AI 投資日報。報告結構：(1) 封面；(2) 目錄；(3) 第一章：美國總體環境；(4) 第二章：動能篩選結果（漲幅 20%+ 標的）；(5)
    第三章：情緒與技術分析；(6) 第四章：基本面摘要；(7) 第五章：投資組合建議（Kelly 倉位）；(8) 第六章：風控報告（CVaR + 壓力測試）。以
    Email 寄送 PDF 至 glen200392@gmail.com，主旨：【美股 AI 日報】YYYY-MM-DD — Macro: {score}/10
    | Top Pick: {ticker} +{return}%。'
  agent_slug: nebula
  format_guide: 步驟：(1) 將所有 Stage 繁體中文輸出依章節合併，加入封面、目錄；(2) text_editor create 儲存為 reports/us_ai_daily_{YYYYMMDD}.pdf；(3)
    send_email 寄送至 glen200392@gmail.com，Email 正文包含當日美股核心摘要：市場體制、漲幅 20%+ 標的名單、前三大推薦及倉位%、最大風險提示。
---

美股 AI 投資日報自動化 Pipeline，每日 22:00（Asia/Taipei）執行。動態篩選近期漲幅 20%+ 的 AI 相關標的，結合 Macro Score、NLP 情緒、技術分析、基本面、Kelly 倉位、CVaR 風控，最終整合為單一 PDF 寄送至 glen200392@gmail.com。核心標的池：NVDA、MSFT、GOOGL、META、AMZN、AAPL、SMCI、DELL、AMD、AVGO、QCOM、INTC，加上動態篩選近期漲幅 20%+ 的 AI 概念股。