---
slug: japan-ai-investment-pipeline-daily-pdf-email-report-2200-tst
title: Japan AI Investment Pipeline — Daily PDF Email Report (22:00 TST)
steps:
- description: 'Stage 0.5 — 日本總體環境評分 (Japan Macro Scoring): 抓取日本總體指標：(1) yfinance
    抓取 Nikkei 225 (^N225)、TOPIX (^TOPX)、日圓/美元匯率 (JPY=X)、VIX；(2) web_search 查詢日本最新
    CPI、日銀 BOJ 利率政策方向、PMI、貨幣增長率；(3) 計算日本 Macro Score (0-10) 與 Japan Macro Regime。'
  agent_id: agt_0699ef74e08b7ce480001ac84958d0db
  agent_slug: macro-score-pipeline-stage
  format_guide: '輸出 JSON：{macro_score: float, macro_regime: string, indicators: {nikkei_trend,
    topix_trend, jpy_usd, boj_policy, japan_cpi, japan_pmi}, sector_outlook: {ai_semiconductor,
    industrial_robot, cloud_software, exporters}}。繁體中文總體環境摘要。'
- description: 'Stage 1 — 動態篩選 + 市場研究 (Japan AI Screener): 篩選日本 AI 標的：8035、4063、6758、6981、9984、6702、6701、6501、6723、6861。按
    20日漲幅篩選，結合 web_search 識別即時強勢日本 AI 標的。'
  agent_id: agt_0697b528d8ff7d4580007a1fa9e54a9e
  agent_slug: market-research-analyst
  format_guide: '輸出：篩選結果表 + 市場研究摘要 + JSON：[{ticker, name, exchange: TSE, 20d_return_pct,
    momentum_flag, jpy_sensitivity}]。額外輸出 en_global_perspective 欄位（純英文）：{foreign_net_buying:
    string（TSE foreign investor net buy/sell in JPY billion this week），analyst_calls: [{firm,
    ticker, action, target_price_jpy}]（rating changes from foreign brokers: CLSA/Nomura/Daiwa/MS），
    global_supply_chain_en: string（Japan company role in global AI supply chain vs TSMC/ASML/AMAT），
    boj_impact_en: string（BOJ rate policy impact on export-heavy AI stocks in English）}'
- description: 'Stage 1.5 — 情緒分析 (Japan Sentiment): 整合日文與英文情緒來源，計算 Sentiment Score
    (0-10)。'
  agent_id: agt_0699ef88cbe779d380004859b6076cb1
  agent_slug: sentiment-aggregation-analyzer
  format_guide: '輸出 JSON：{market_sentiment: {score, regime, label}, stocks: [{ticker,
    sentiment_score, sentiment_label, key_headlines}]}。'
- description: 'Stage 2 — 技術分析 (Japan Technical Analysis): 對日本標的執行完整技術分析，包含外資流向訊號。'
  agent_id: agt_0697b541706f7e628000b0a73cb957eb
  agent_slug: technical-analysis-expert
  format_guide: '輸出 JSON：{stocks: [{ticker, regime, technical_score, entry_zone, targets,
    stop_loss, rr_ratio, foreign_flow_signal,
    en_global_perspective: {foreign_flow_en: string（TSE foreign net flow direction and magnitude），
    jpy_technical_impact: string（how JPY/USD movement amplifies or dampens price action），
    nikkei_relative_strength: string（stock RS vs Nikkei225 and global AI peers），
    options_market_en: string（Nikkei options / individual stock put-call ratio signal）}}]}。'
- description: 'Stage 3 — 基本面摘要 (Japan Fundamental): 對日本標的執行基本面分析，特別注意日圓貨幣風險。'
  agent_id: agt_0697b55daeb9751b800061ba767d1167
  agent_slug: fundamental-analysis-advisor
  format_guide: '輸出 JSON：{stocks: [{ticker, fundamental_score, valuation, moat_rating,
    ai_exposure, jpy_risk, recommendation,
    en_global_perspective: {foreign_broker_rating: string（CLSA/Nomura International/MS Japan latest rating and PT in JPY），
    consensus_eps_jpy: string（sell-side consensus EPS in JPY with range），
    jpy_earnings_sensitivity: string（estimated EPS impact per 1 JPY move vs USD），
    global_peer_comparison_en: string（valuation vs global peers: e.g. TEL vs AMAT/LRCX P/E gap）}}]}。'
- description: 'Stage 4 — 四維度整合 + Kelly 倉位 (Japan Portfolio): 日圓風險修正：USD/JPY 下降 +
    海外營收 >50% 的標的 Fundamental Score 自動-0.5。'
  agent_id: agt_0697b57e7d3e7b3e8000ae9d0b00238b
  agent_slug: investment-report-coordinator
  format_guide: '輸出 JSON：{stocks: [{ticker, composite_score, kelly_half, suggested_pct,
    jpy_adjustment,
    en_global_perspective: {msci_japan_weight: string（MSCI Japan index weight and recent rebalancing），
    foreign_ownership_pct: string（TSE foreign ownership % and 4-week trend），
    global_ai_theme_fit: string（how stock fits global AI theme: robotics/semiconductor/cloud/5G），
    carry_trade_risk_en: string（JPY carry unwind risk and estimated portfolio impact）}}],
    total_invested_pct, cash_pct}。'
- description: 'Stage 5 — 風控 + CVaR (Japan Risk): 壓力測試日圓急速上漲、全球 AI 失敘、中日貿易紛爭、國際機構撤資四情境。'
  agent_id: agt_0697b56ef4077e078000f5b423297f82
  agent_slug: portfolio-risk-management-advisor
  format_guide: '輸出 JSON：{cvar_95, cvar_99, stress_tests, decisions: [{ticker, verdict,
    final_pct, note}],
    en_global_perspective: {jpy_tail_risk_en: string（extreme JPY appreciation scenario impact on export earnings），
    boj_policy_risk_en: string（BOJ rate hike path and estimated portfolio drawdown），
    china_demand_risk_en: string（China AI/tech demand slowdown impact on Japan component makers），
    hedge_tools_en: string（suggested hedges: JPY futures / Nikkei put / USD-denominated assets）}}。'
- description: 'Stage 5.5 — 圖表生成 (Japan Chart Generation): 接收 Stage 0.5~Stage 5 所有結構化
    JSON 輸出，使用 Python（plotly、matplotlib、mplfinance）生成六類投資視覺化圖表並儲存為 PNG，供 Stage 6a
    PDF 嵌入。圖表清單：(1) 四維度雷達圖（每檔股票 Composite Score 四維分解）；(2) Kelly 倉位圓餅圖（核准標的倉位分配）；(3)
    CVaR 風險長條圖（各股 95%/99% CVaR 對比）；(4) 日圓匯率敏感度矩陣圖（各股 JPY sensitivity vs AI exposure
    散佈圖）；(5) 技術面多股走勢圖（Top 3 標的 K 線 + RSI + MACD，使用 mplfinance）；(6) 情緒動能散佈圖（Sentiment
    Score vs Composite Score，size=suggested_pct）。'
  agent_id: agt_0698f0e814287d378000c45869797931
  agent_slug: code-agent
  format_guide: "執行步驟：\n1. 從 $step.1~$step.7 讀取各 Stage JSON 輸出，解析所需欄位\n2. 安裝必要套件：pip\
    \ install plotly matplotlib mplfinance kaleido yfinance\n3. 生成六張圖表（繁體中文標題）：\n\
    \   - radar_chart.png：plotly Scatterpolar，四維度（Macro/Sentiment/Technical/Fundamental），加入\
    \ JPY 風險標記\n   - kelly_pie.png：plotly Pie，APPROVED 標的倉位分配\n   - cvar_bar.png：plotly\
    \ Bar，grouped bar（95% vs 99% CVaR）\n   - jpy_scatter.png：plotly Scatter，x=jpy_sensitivity，y=ai_exposure，size=composite_score，高風險標的標紅\n\
    \   - technical_chart.png：mplfinance mpf.plot，Top 3 ticker K線+RSI+MACD，style='yahoo'\n\
    \   - sentiment_scatter.png：plotly Scatter，x=sentiment_score，y=composite_score，size=suggested_pct\n\
    4. 所有圖表儲存至 /home/user/files/reports/charts_japan_{YYYYMMDD}/\n5. 回傳 JSON：{charts_dir:\
    \ string, files: {radar, kelly_pie, cvar_bar, jpy_scatter, technical, sentiment_scatter},\
    \ generated_count: int, errors: []}"
- description: 'Stage 6a — 生成日股 AI 投資日報 PDF (Japan PDF Generator): 整合所有上游 Stage 輸出（含
    Stage 5.5 圖表），用 exec() 方式載入 pdf_report_generator.py（避免 .pyc cache），將六張圖表嵌入對應章節，生成日股
    PDF。'
  agent_id: agt_0698f0e814287d378000c45869797931
  agent_slug: code-agent
  format_guide: "執行步驟：\n1. 從 $step.1~$step.8 取得各 Stage 資料；從 $prev（Stage 5.5）取得 charts_dir\
    \ 和 files 路徑\n2. 組裝 report_data，meta.title='【日股 AI 日報】{YYYY-MM-DD}'，meta.subtitle='AI\
    \ Investment Pipeline — Japan Edition'，額外加入 charts 欄位：{charts: {radar: path, kelly_pie:\
    \ path, cvar_bar: path, jpy_scatter: path, technical: path, sentiment_scatter:\
    \ path}}\n3. 用 exec() 執行：\n\n   import os\n   from datetime import datetime\n\
    \   script_path = '/home/user/files/code/pdf_report_generator.py'\n   with open(script_path,\
    \ 'r', encoding='utf-8') as f:\n       src = f.read()\n   ns = {'__file__': script_path}\n\
    \   exec(src, ns)\n   date_str = datetime.now().strftime('%Y%m%d')\n   output_path\
    \ = f'/home/user/files/reports/japan_ai_daily_{date_str}.pdf'\n   os.makedirs('/home/user/files/reports',\
    \ exist_ok=True)\n   result = ns['build_report'](report_data, output_path)\n \
    \  print(f'PDF saved: {result}')\n\n4. 回傳 output_path 字串"
- description: 'Stage 6b — 日股日報 HTML Email + PDF 附件寄送 (Japan Email Delivery): 接收 Stage
    6a 產生的 PDF 路徑，組裝 HTML Email，以 PDF 作為附件寄送至 glen200392@gmail.com。'
  agent_slug: nebula
  format_guide: "執行步驟：\n1. 從 $prev 取得 PDF 路徑 (/home/user/files/reports/japan_ai_daily_YYYYMMDD.pdf)\n\
    \   附件用相對路徑: reports/japan_ai_daily_YYYYMMDD.pdf\n2. HTML Email 正文（<table> 排版，不用\
    \ Markdown）：\n   - 頂部深藍色橫幅：「【日股 AI 日報】YYYY-MM-DD」\n   - 摘要卡片：Macro Score / Nikkei\
    \ 體制 / JPY 趨勢 / 總投入% / 現金%\n   - Top 3 標的表格：ticker + 評分 + 建議倉位 + JPY 風險\n   -\
    \ 風險提示區：BOJ 政策 + 日圓 + 外資動向\n   - 頁尾: 'Powered by Nebula AI Pipeline'\n3. send_email:\
    \ recipient=glen200392@gmail.com, subject=【日股 AI 日報】{YYYY-MM-DD} — Nikkei:{regime}|Top:{ticker},\
    \ attachments=[reports/japan_ai_daily_YYYYMMDD.pdf]\n4. 確認寄送成功"
---

日股 AI 投資日報自動化 Pipeline，每日 22:00（Asia/Taipei）與美股報告同步執行。核心標的池：東京威力科創（TEL/8035）、信越化學（4063）、索尼（6758）、村田製作所（6981）、SoftBank Group（9984）、Fujitsu（6702）、NEC（6701）、Hitachi（6501）、Renesas（6723）、Keyence（6861）。加上動態篩選近期漲幅 20%+ 的日本 AI 概念股。最終整合為單一 PDF，與美股報告合併在同一封 Email 寄送至 glen200392@gmail.com。