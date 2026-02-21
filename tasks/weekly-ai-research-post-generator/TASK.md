---
slug: weekly-ai-research-post-generator-v2-with-evolution-chronicle
title: Weekly AI Research + Post Generator (v2 — with Evolution Chronicle)
version: "2.1.0"
standard: McKinsey Intelligence Standard
last_updated: "2026-02-21"
owner: AI Research Federation — Team A & Team B
sla: every Monday 08:00 Asia/Taipei
kpi_targets:
  coverage_score: 85
  synthesis_min_words: 800
  sources_minimum: 12
  delivery_sla_minutes: 45
steps:

# =============================================================================
# PHASE 1 — INTELLIGENCE GATHERING (Parallel, Steps 1-4)
# MECE Coverage: Academic | Industry Leaders | Breakthrough Applications | Market
# =============================================================================

- description: "[GATHER-1] arXiv 學術前沿：搜尋過去 7 天 Agent 架構、多模態、推理、安全等最新論文"
  action_key: web-search
  action_props:
    query: "AI agent architecture multi-agent LLM reasoning multimodal safety site:arxiv.org published after:$7d_ago|date"
    citations: true
    num_results: 5

- description: "[GATHER-2] 三大廠動態：搜尋 OpenAI、Anthropic、Google DeepMind 過去 7 天模型與平台發布"
  action_key: web-search
  action_props:
    query: "OpenAI Anthropic Google DeepMind AI model release platform update $7d_ago|date to $today|date"
    citations: true
    num_results: 5

- description: "[GATHER-3] 技術突破：搜尋本週醫療、科學發現、硬體、開源模型、產業應用等跨域突破"
  action_key: web-search
  action_props:
    query: "AI technology breakthrough innovation milestone $7d_ago|date healthcare science hardware open-source industry application"
    citations: true
    num_results: 5

- description: "[GATHER-4] 產業情報：搜尋本週融資、併購、監管、競爭格局等結構性市場變化"
  action_key: web-search
  action_props:
    query: "AI industry news funding acquisition regulation competition $7d_ago|date site:techcrunch.com OR site:venturebeat.com OR site:theverge.com OR site:reuters.com"
    citations: true
    num_results: 5

# =============================================================================
# PHASE 2 — SYNTHESIS & INSIGHT (Steps 5-6)
# McKinsey Standard: MECE structure, Pyramid Principle, Actionable Recommendations
# =============================================================================

- description: "[SYNTHESIZE] Team A — AI Research Advisor 整合四路情報，生成 McKinsey 標準結構化週報與焦點技術 JSON"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation 的首席研究顧問（McKinsey Intelligence Standard）。
    整合 $step.1（arXiv論文）、$step.2（三大廠更新）、$step.3（技術突破）、$step.4（產業新聞），
    使用「金字塔原則（Pyramid Principle）」與「MECE 框架」生成結構化週報。

    ## Executive Summary（必須首先呈現）
    用 3 句話回答：本週 AI 最重要的事是什麼？對從業者意味著什麼？行動建議是什麼？

    ## 本週關鍵發現（MECE 四象限）
    ### 1. 學術前沿（arXiv）
    - 最重要論文 Top 3（標題、核心創新、生態影響分 1-10、實作難度）
    ### 2. 三大廠動態（OpenAI / Anthropic / Google）
    - 每家各一段，含：發布內容、實際影響、競爭意涵
    ### 3. 跨域技術突破
    - 醫療、科學、硬體、開源各一條（若本週有），標明影響程度：高/中/低
    ### 4. 產業結構變化
    - 融資/併購/監管：各條含金額或規模量化指標

    ## 架構洞察（McKinsey Insight Layer）
    - 本週出現的新技術模式或設計原則（不只整理新聞，要有洞察）
    - 與上週趨勢的連貫性或突破點

    ## KPI 自評（本次搜尋品質）
    | 指標 | 數值 | 目標 | 達標 |
    |------|------|------|------|
    | 來源總數 | N | ≥12 | ✅/❌ |
    | 覆蓋領域數 | N | ≥4 | ✅/❌ |
    | 論文數量 | N | ≥3 | ✅/❌ |
    | 量化指標數 | N | ≥5 | ✅/❌ |

    ## 行動建議（Actionable Recommendations）
    列出 3 條具體建議，每條含：對象（工程師/研究者/管理者）、行動、預期效益

    ## 下週觀察清單
    3-5 個需持續追蹤的訊號

    ---
    最後額外輸出 JSON 區塊（必須通過 output-schemas.json#/definitions/focus_tech_block 驗證）：
    ```json
    {"focus_tech": "技術名稱", "tech_domain": "agent|reasoning|architecture|training|protocol|multimodal|safety|hardware|infrastructure", "why_important": "一句話說明", "confidence_score": 0.0-1.0}
    ```

    格式：繁體中文 Markdown，目標 1000-1400 字，語調：專業顧問報告風格。

- description: "[CHRONICLE] Team B — 演進史官追溯本週焦點技術歷史脈絡，更新 Evolution Chronicle"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation 的首席演進史官（Evolution Chronicle Team B）。
    根據 $prev 輸出中的 focus_tech 與 tech_domain，撰寫「技術演進溯源」報告。

    ## 技術演進溯源：[技術名稱] 的歷史脈絡

    ### 起源（YYYY）
    這個技術最初要解決什麼問題？誰首先提出？原始論文或產品是什麼？

    ### 關鍵突破時刻（YYYY-YYYY）
    按時間軸列出 3-5 個里程碑事件，每個含：年份、事件、核心創新、影響程度（High/Medium/Low）

    ### 演進分叉（技術樹）
    出現了哪些不同的發展方向？用樹狀結構呈現：
    - 主幹：主流路線
    - 分支 A：替代路線（解決什麼不同問題）
    - 分支 B：融合路線（與其他技術交叉）

    ### 本週連結
    本週的發展是哪條演進線的延伸？意味著演進到了哪個階段？
    用一句話標記位置：「我們現在站在 [演進階段] 的 [起點/中期/成熟期]」

    ### 下一步預測（Evidence-Based）
    基於過去的演進模式，接下來 6-12 個月最可能出現的突破是什麼？
    給出 3 個預測，每個含信心度（High/Medium/Low）與依據

    ### Evolution Graph 更新指令
    ```json
    {
      "new_nodes": [],
      "new_edges": [],
      "update_nodes": []
    }
    ```

    字數：600-900 字，繁體中文，有歷史縱深感，引用具體年份與事件。

# =============================================================================
# PHASE 3 — CONTENT PRODUCTION & DELIVERY (Steps 7-8)
# McKinsey Standard: Executive-ready deliverable, multi-channel distribution
# =============================================================================

- description: "[PUBLISH] 撰寫 McKinsey 標準繁體中文社群貼文並儲存（整合週報摘要 + 演進溯源）"
  agent_slug: nebula
  format_guide: |
    使用 $step.5 的週報內容與 $step.6 的演進溯源，撰寫一篇 McKinsey 標準繁體中文社群貼文，
    儲存為 docs/weekly_post_$today|date.md。

    貼文結構（Pyramid Principle：結論先行）：

    ## [本週最重要的 AI 突破，一句話版本] 🤖

    ### 核心結論（Executive Summary — 三句話）
    讀者在第一段就知道本週最重要的事、影響、以及他們該怎麼做。

    ### 本週關鍵發展（MECE — 四象限各一條）
    - 🔬 學術前沿：[論文亮點 + 核心創新]
    - 🏢 三大廠動態：[發布 + 競爭意涵]
    - ⚡ 技術突破：[跨域應用 + 量化影響]
    - 📊 產業變局：[融資/監管 + 結構意涵]

    ### 量化里程碑
    本週 3-5 個值得記錄的具體數字（模型大小、性能提升%、融資金額等）

    ### 【演進視角】站在哪條歷史線上？
    使用 $step.6 的內容，150-200 字，讓讀者理解本週突破不是孤立事件，
    而是一條更長歷史演進線上的節點。

    ### 對你的實際影響
    按角色分類：工程師 / 研究者 / 產品人 / 管理者，各一條具體影響

    ### 行動建議
    本週就可以做的 3 件事（具體、可執行、有時間框架）

    ### 互動問題
    一個能引發討論的開放性問題

    #AIAgent #多智能體 #LLM #AI架構 #AIResearch #AIBreakthrough #人工智慧

    字數：1200-1800 字，語調：專業顧問但親切可讀，有洞察深度，不只是新聞整理。

- description: "[DELIVER] Email 發送 McKinsey 標準週報（Executive Summary + 週報 + 演進溯源 + 貼文）給 Glennn"
  agent_slug: nebula
  action_key: send-nebula-email
  format_guide: |
    發送 Email，主旨：「🤖 Weekly AI Intelligence Report — $today|date | McKinsey Standard」

    Email 結構：

    ---
    ## EXECUTIVE BRIEF（60 秒閱讀版）
    本週三大核心發現（各一句話，結論先行）
    KPI 達標狀態：來源 N/12 | 覆蓋域 N/4 | 洞察深度評分 N/10

    ---
    ## 本週研究摘要
    [插入 $step.5 的完整週報，含 KPI 自評表格]

    ---
    ## 技術演進溯源
    [插入 $step.6 的演進溯源段落]

    ---
    ## 本週社群貼文（可直接發佈）
    [插入 $step.7 的完整貼文]

    ---
    ## 資料來源清單
    條列本次搜尋的所有來源 URL

    ---
    收件人：glen200392@gmail.com
---

每週一 08:00 自動執行（Asia/Taipei）。
McKinsey Intelligence Standard v2.1：MECE 四象限情報採集 → 金字塔原則合成 → KPI 自評 →
Team B 演進溯源 → 社群貼文生成 → Email 交付。
目標 SLA：45 分鐘內完成全流程，覆蓋分 ≥85，來源 ≥12。
