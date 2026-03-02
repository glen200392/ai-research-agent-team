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
    stocks 2026」等識別即時強勢標的，組合成 12-15 檔分析清單；(B) 市場研究：搜尋 AI 市場最新發展、法人研究報告、產業催化劑（AI CapEx、法說季度、新品發布等）。'
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
    P/E、EV/EBITDA、毛利率趨勢、ROE、科技幾何成長（AI 投資計畫能見度）、競爭護城河。輸出 Fundamental Score (0-10) 及投資建議。'
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
    + 參數法 + Monte Carlo）。壓力測試情境：(1) 美國送入衰退，(2) Fed 重新升息衝擊，(3) AI CapEx 大幅削減，(4) 地緣政治風險。依波動率體制調整倉位乘數，對每檔輸出
    APPROVED / REDUCED / REJECTED 裁決。'
  agent_id: agt_0697b56ef4077e078000f5b423297f82
  agent_slug: portfolio-risk-management-advisor
  format_guide: '輸出：(1) CVaR 摘要表，(2) 壓力測試結果，(3) 波動率體制旗標，(4) 最終核准倉位表，(5) 每股風控判決。同時輸出完整
    JSON：{cvar_95: float, cvar_99: float, stress_tests: [{scenario, portfolio_impact,
    verdict}], decisions: [{ticker, verdict, final_pct, note}]}。繁體中文輸出。'
- description: 'Stage 5.5 — 圖表生成 (US Chart Generation): 接收 Stage 0.5~Stage 5 所有結構化
    JSON 輸出，使用 Python（plotly、matplotlib、mplfinance）生成六類投資視覺化圖表並儲存為 PNG，供 Stage 6a
    PDF 嵌入。圖表清單：(1) 四維度雷達圖（每檔股票 Composite Score 四維分解）；(2) Kelly 倉位圓餅圖（核准標的倉位分配）；(3)
    CVaR 風險長條圖（各股 95%/99% CVaR 對比）；(4) 動能篩選排行圖（20日漲幅橫向長條，MOMENTUM 標的高亮顯示）；(5) 技術面多股走勢圖（Top
    3 標的 K 線 + RSI + MACD，使用 mplfinance）；(6) 情緒動能散佈圖（Sentiment Score vs Composite
    Score，size=suggested_pct，color=regime）。'
  agent_id: agt_0698f0e814287d378000c45869797931
  agent_slug: code-agent
  format_guide: "執行步驟：\n1. 從 $step.1~$step.7 讀取各 Stage JSON 輸出，解析所需欄位\n2. 安裝必要套件：pip\
    \ install plotly matplotlib mplfinance kaleido yfinance\n3. 生成六張圖表（繁體中文標題）：\n\
    \   - radar_chart.png：plotly Scatterpolar，四維度（Macro/Sentiment/Technical/Fundamental）\n\
    \   - kelly_pie.png：plotly Pie，APPROVED 標的倉位分配\n   - cvar_bar.png：plotly Bar，grouped\
    \ bar（95% vs 99% CVaR）\n   - momentum_bar.png：plotly Bar，20日漲幅橫向排行，MOMENTUM 標的標記橘色\n\
    \   - technical_chart.png：mplfinance mpf.plot，Top 3 ticker K線+RSI+MACD，style='yahoo'\n\
    \   - sentiment_scatter.png：plotly Scatter，x=sentiment_score，y=composite_score，size=suggested_pct\n\
    4. 所有圖表儲存至 /home/user/files/reports/charts_us_{YYYYMMDD}/\n5. 回傳 JSON：{charts_dir:\
    \ string, files: {radar, kelly_pie, cvar_bar, momentum_bar, technical, sentiment_scatter},\
    \ generated_count: int, errors: []}"
- description: 'Stage 6a — 生成美股 AI 投資日報 PDF (US PDF Generator): 整合所有上游 Stage 輸出（含
    Stage 5.5 圖表），用 exec() 方式載入 pdf_report_generator.py（避免 .pyc cache 問題），將六張圖表嵌入對應章節，生成一份完整格式化
    PDF。'
  agent_id: agt_0698f0e814287d378000c45869797931
  agent_slug: code-agent
  format_guide: "執行步驟：\n1. 從 $step.1~$step.8 取得各 Stage 的資料；從 $prev（Stage 5.5）取得 charts_dir\
    \ 和 files 路徑\n2. 組裝 report_data dict（符合 build_report() 規格），額外加入 charts 欄位：{charts:\
    \ {radar: path, kelly_pie: path, cvar_bar: path, momentum_bar: path, technical:\
    \ path, sentiment_scatter: path}}\n3. 用以下方式執行（必須用 exec，不能用 import）：\n\n   import\
    \ os\n   from datetime import datetime\n   script_path = '/home/user/files/code/pdf_report_generator.py'\n\
    \   with open(script_path, 'r', encoding='utf-8') as f:\n       src = f.read()\n\
    \   ns = {'__file__': script_path}\n   exec(src, ns)\n   date_str = datetime.now().strftime('%Y%m%d')\n\
    \   output_path = f'/home/user/files/reports/us_ai_daily_{date_str}.pdf'\n   os.makedirs('/home/user/files/reports',\
    \ exist_ok=True)\n   result = ns['build_report'](report_data, output_path)\n \
    \  print(f'PDF saved: {result}')\n\n4. 回傳 output_path 字串（格式：/home/user/files/reports/us_ai_daily_YYYYMMDD.pdf）"
- description: 'Stage 6b — 美股日報 HTML Email + PDF 附件寄送 (US Email Delivery): 接收 Stage
    6a 產生的 PDF 路徑，組裝 HTML 格式 Email 正文（含當日核心摘要），以 PDF 作為附件寄送至 glen200392@gmail.com。'
  agent_slug: nebula
  format_guide: "執行步驟：\n1. 從 $prev 取得 PDF 檔案路徑（格式：/home/user/files/reports/us_ai_daily_YYYYMMDD.pdf）\n\
    \   注意：附件路徑需轉換為相對路徑 reports/us_ai_daily_YYYYMMDD.pdf\n2. 從上游 Stage 取得核心摘要資料：macro_regime、macro_score、top\
    \ 3 推薦標的（ticker + composite_score + suggested_pct%）、最大風險提示\n3. 組裝 HTML Email 正文（使用\
    \ <table> 標籤排版，不要用 Markdown）：\n   - 頂部：深藍色橫幅，白字標題「【美股 AI 日報】YYYY-MM-DD」\n   -\
    \ 摘要卡片區：用 <table> 呈現 Macro Score / Regime / 總投入% / 現金%\n   - 今日精選標的：用 <table>\
    \ 呈現 Top 3 ticker、評分、建議倉位\n   - 風險提示：橘色背景 <div>，列出最大風險\n   - 頁尾：灰色小字「Powered by\
    \ Nebula AI Pipeline」\n4. 呼叫 send_email：\n   - recipient: glen200392@gmail.com\n\
    \   - subject: 【美股 AI 日報】{YYYY-MM-DD} — Macro: {score}/10 | Top Pick: {ticker}\
    \ +{return}%\n   - body: 上述 HTML 內容\n   - attachments: [reports/us_ai_daily_YYYYMMDD.pdf]\n\
    5. 確認寄送成功"
---

美股 AI 投資日報自動化 Pipeline，每日 22:00（Asia/Taipei）執行。動態篩選近期漲幅 20%+ 的 AI 相關標的，結合 Macro Score、NLP 情緒、技術分析、基本面、Kelly 倉位、CVaR 風控，最終整合為單一 PDF 寄送至 glen200392@gmail.com。核心標的池：NVDA、MSFT、GOOGL、META、AMZN、AAPL、SMCI、DELL、AMD、AVGO、QCOM、INTC，加上動態篩選近期漲幅 20%+ 的 AI 概念股。