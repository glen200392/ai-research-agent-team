---
slug: meta-harness-monthly-quality-evaluation-evolution-report
title: Meta Harness — Monthly Quality Evaluation & Evolution Report
version: "2.1.0"
standard: McKinsey Organizational Excellence Standard
last_updated: "2026-02-21"
owner: AI Research Federation — Meta Harness L4
sla: 1st of every month 09:00 Asia/Taipei
kpi_targets:
  team_a_min_score: 75
  team_b_min_score: 75
  team_c_min_score: 75
  upgrade_trigger_threshold: 70
  report_min_words: 1500
  hitl_response_sla_days: 3
steps:

# =============================================================================
# PHASE 1 — BENCHMARK INTELLIGENCE (Parallel, Steps 1-2)
# MECE: External AI Research Standards | External Pedagogy Standards
# =============================================================================

- description: "[BENCHMARK-A] 搜尋上月 AI 研究領域重大發展，建立 Team A/B 評估外部基準"
  action_key: web-search
  action_props:
    query: "AI agent LLM major breakthroughs research milestones last month $30d_ago|date to $today|date site:arxiv.org OR site:openai.com OR site:deepmind.google OR site:anthropic.com"
    citations: true
    num_results: 5

- description: "[BENCHMARK-C] 搜尋上月 AI 教育最佳實踐與知識傳播標準，建立 Team C 評估外部基準"
  action_key: web-search
  action_props:
    query: "AI education best practices explainable AI knowledge transfer learning design pedagogy Bloom's Taxonomy 2026"
    citations: true
    num_results: 5

# =============================================================================
# PHASE 2 — PARALLEL TEAM EVALUATIONS (Steps 3-5)
# McKinsey Standard: Independent, evidence-based, scored against external benchmarks
# All three evaluations run in parallel — indexed by team key, not order
# =============================================================================

- description: "[EVAL-A] Meta Harness 評審 Team A：研究覆蓋廣度、準確性、洞察深度、可行動性"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation Meta Harness 的品質評審委員（McKinsey Organizational Excellence Standard）。
    根據 $step.1 的上月重大 AI 發展作為外部基準，評估 Team A（現況研究團隊）的月度表現。

    ## 評估方法論
    使用 McKinsey 評估框架：Impact × Rigor × Relevance
    - 與外部基準對比（$step.1 發現了哪些，Team A 覆蓋了哪些？）
    - 定量評分，每項有具體依據
    - 改進建議須具體、可執行、有優先順序

    ## 必須輸出 JSON（通過 output-schemas.json#/definitions/team_evaluation 驗證）
    ```json
    {
      "team": "Team A — Current Intelligence",
      "evaluation_month": "$today|date",
      "scores": {
        "coverage_breadth": {"score": 0-100, "comment": "覆蓋了哪些領域，遺漏了哪些（對比 $step.1）"},
        "technical_accuracy": {"score": 0-100, "comment": "技術描述的準確程度，有無事實錯誤"},
        "insight_depth": {"score": 0-100, "comment": "超越新聞整理的洞察深度，是否有原創分析"},
        "actionability": {"score": 0-100, "comment": "建議的可行動程度，是否具體可執行"},
        "kpi_compliance": {"score": 0-100, "comment": "是否達到 sources≥12、synthesis≥800字等 KPI 要求"}
      },
      "overall_score": 0-100,
      "strengths": ["具體優點1（含例子）", "具體優點2（含例子）"],
      "improvement_areas": ["具體改進點1（含建議）", "具體改進點2（含建議）"],
      "upgrade_needed": true/false,
      "upgrade_suggestion": "若 upgrade_needed 為 true：具體升級方向、預期效益、實施步驟",
      "kpi_trend": {"previous_score": null, "delta": null, "trend": "stable"}
    }
    ```

- description: "[EVAL-B] Meta Harness 評審 Team B：歷史深度、連結準確性、敘事品質、預測價值"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation Meta Harness 的品質評審委員（McKinsey Organizational Excellence Standard）。
    根據 $step.1 的上月重大 AI 發展作為外部基準，評估 Team B（演進史官）的月度表現。

    ## 評估方法論
    Team B 的核心價值：讓當下的技術發展有歷史縱深。評估維度聚焦於史料準確性與預測有效性。

    ## 必須輸出 JSON（通過 output-schemas.json#/definitions/team_evaluation 驗證）
    ```json
    {
      "team": "Team B — Evolution Chronicle",
      "evaluation_month": "$today|date",
      "scores": {
        "historical_depth": {"score": 0-100, "comment": "演進追溯的時間深度與完整性（是否真的追到起源？）"},
        "connection_accuracy": {"score": 0-100, "comment": "技術演進連結的準確性（因果關係是否正確？）"},
        "narrative_quality": {"score": 0-100, "comment": "敘事的引人入勝程度（讀者是否能感受到技術的演進張力？）"},
        "predictive_value": {"score": 0-100, "comment": "對未來演進的預測有效性（上月預測本月是否應驗？）"},
        "graph_maintenance": {"score": 0-100, "comment": "evolution-graph.json 更新的頻率與品質"}
      },
      "overall_score": 0-100,
      "strengths": ["具體優點1（含例子）", "具體優點2（含例子）"],
      "improvement_areas": ["具體改進點1（含建議）", "具體改進點2（含建議）"],
      "upgrade_needed": true/false,
      "upgrade_suggestion": "若 upgrade_needed 為 true：具體升級方向",
      "kpi_trend": {"previous_score": null, "delta": null, "trend": "stable"}
    }
    ```

- description: "[EVAL-C] Meta Harness 評審 Team C：三難度適切性、準確性、教學設計品質、測驗鑑別度"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation Meta Harness 的品質評審委員（McKinsey Organizational Excellence Standard）。
    根據 $step.2 的 AI 教育最佳實踐作為外部基準，評估 Team C（教學聯盟）的月度表現。

    ## 評估方法論
    Team C 的核心價值：同樣的 AI 突破，讓不同層次的讀者都能學到對自己有用的東西。
    重點評估「層次差異化」是否做到位。

    ## 必須輸出 JSON（通過 output-schemas.json#/definitions/team_evaluation 驗證）
    ```json
    {
      "team": "Team C — Pedagogy Federation",
      "evaluation_month": "$today|date",
      "scores": {
        "level_appropriateness": {"score": 0-100, "comment": "三難度版本對目標讀者的適切性（L1 是否真的零術語？L3 是否真的學術嚴謹？）"},
        "conceptual_accuracy": {"score": 0-100, "comment": "教材內容的準確性（對比 $step.2 的最新研究成果）"},
        "pedagogy_quality": {"score": 0-100, "comment": "教學設計與知識傳遞效果（Bloom's Taxonomy 覆蓋度）"},
        "quiz_quality": {"score": 0-100, "comment": "測驗題的品質與鑑別度（3/4/3 分層是否合理）"},
        "schema_compliance": {"score": 0-100, "comment": "JSON schema 驗證通過率（output-schemas.json 嚴格模式）"}
      },
      "overall_score": 0-100,
      "strengths": ["具體優點1（含例子）", "具體優點2（含例子）"],
      "improvement_areas": ["具體改進點1（含建議）", "具體改進點2（含建議）"],
      "upgrade_needed": true/false,
      "upgrade_suggestion": "若 upgrade_needed 為 true：具體升級方向",
      "kpi_trend": {"previous_score": null, "delta": null, "trend": "stable"}
    }
    ```

# =============================================================================
# PHASE 3 — SYSTEM SYNTHESIS & EVOLUTION (Step 6)
# McKinsey Pyramid Principle: System-level insight, not just sum of parts
# =============================================================================

- description: "[SYNTHESIZE] Meta Harness 整合三團隊評估，生成 McKinsey 標準系統進化報告"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 Meta Harness 的系統進化引擎（McKinsey Organizational Excellence Standard）。
    整合 $step.3（Team A）、$step.4（Team B）、$step.5（Team C）的評估結果，
    使用「金字塔原則」生成完整月度系統進化報告。

    ## 報告結構（繁體中文 Markdown）

    # AI Research Federation — 月度 Meta Harness 評估報告
    **評估月份：** $today|date
    **標準：** McKinsey Organizational Excellence Standard v2.1
    **評審委員：** Meta Harness L4 自動評估系統

    ---

    ## EXECUTIVE SUMMARY（60 秒閱讀版）
    用 3 句話回答：聯邦系統本月整體表現如何？最大亮點是什麼？最需要改進的是什麼？

    ---

    ## 一、三團隊 KPI 儀表板

    | 指標 | Team A | Team B | Team C | 系統平均 | 目標 | 狀態 |
    |------|--------|--------|--------|---------|------|------|
    | 總分 | X/100 | X/100 | X/100 | X/100 | ≥75 | ✅/❌ |
    | 最強維度 | ... | ... | ... | - | - | - |
    | 最弱維度 | ... | ... | ... | - | - | - |
    | 升級需求 | ✅/❌ | ✅/❌ | ✅/❌ | - | - | - |

    月度趨勢圖（文字版）：
    - Team A：[上月分數] → [本月分數]（+/-N，趨勢）
    - Team B：[上月分數] → [本月分數]（+/-N，趨勢）
    - Team C：[上月分數] → [本月分數]（+/-N，趨勢）

    ---

    ## 二、本月最大亮點（跨團隊，Top 3）
    [結論先行，具體例子支撐，說明為何這是亮點]

    ---

    ## 三、跨團隊協同分析（MECE）
    ### A→B 銜接（Team A 週報 → Team B 演進溯源）
    - 順暢度評分：X/10
    - 分析：focus_tech 傳遞是否準確？Team B 能否從 Team A 輸出快速定位追溯目標？
    - 改進建議：

    ### B→C 銜接（Team B 演進溯源 → Team C 教材）
    - 順暢度評分：X/10
    - 分析：Team C 是否有效利用 Team B 的歷史脈絡豐富教材？
    - 改進建議：

    ### A→C 銜接（Team A 週報 → Team C 教材）
    - 順暢度評分：X/10
    - 分析：Team C 的 topic 選擇是否與 Team A 的 focus_tech 一致？
    - 改進建議：

    ---

    ## 四、系統瓶頸識別（Root Cause Analysis）
    列出本月整個 Federation 效能最大的 1-2 個瓶頸：
    - 瓶頸描述（現象）
    - 根本原因（5 Whys 分析）
    - 影響範圍（哪個/哪些團隊受影響）
    - 緩解方案（短期 vs 長期）

    ---

    ## 五、進化建議清單（HITL 確認項目）
    對所有 upgrade_needed: true 的項目，按優先級排列：

    ### 高優先（本月執行）
    | # | 問題 | 建議升級方向 | 預期影響 | 難度 | 工時估算 |
    |---|------|------------|---------|------|---------|

    ### 中優先（下月規劃）
    | # | 問題 | 建議升級方向 | 預期影響 | 難度 | 工時估算 |

    ---

    ## 六、下月重點觀察指標（Leading Indicators）
    | 指標 | 測量方式 | 目標值 | 若未達標的行動 |
    |------|---------|--------|--------------|
    [3-5 個具體、可量化的指標]

    ---

    ## 七、系統健康評分（Balanced Scorecard）
    | 維度 | 評分 | 說明 |
    |------|------|------|
    | 研究品質（Team A） | X/100 | |
    | 歷史深度（Team B） | X/100 | |
    | 教學品質（Team C） | X/100 | |
    | 跨團隊協同 | X/100 | |
    | 系統可攜性 | X/100 | |
    | **整體系統健康** | **X/100** | |

    字數：1500-2500 字，專業且具可操作性，McKinsey 報告風格。

# =============================================================================
# PHASE 4 — DELIVERY & HITL (Step 7)
# Human-in-the-Loop: Glennn approves all upgrade_needed items before execution
# =============================================================================

- description: "[DELIVER] 儲存月度評估報告並 Email 通知 Glennn 進行 HITL 審批（3 天 SLA）"
  agent_slug: nebula
  action_key: send-nebula-email
  format_guide: |
    將 $step.6 的完整月度評估報告儲存為 docs/meta-harness/evaluation-$today|date.md，
    然後發送 HITL 審批 Email。

    主旨：「🧠 Meta Harness 月度系統評估 — $today|date | McKinsey Standard | 需您審閱」

    Email 結構：

    ## EXECUTIVE SUMMARY
    [插入 $step.6 的 Executive Summary 三句話]

    ## 系統 KPI 儀表板
    [插入 $step.6 的三團隊 KPI 儀表板表格]

    ## 進化建議（需您決定）
    [插入 $step.6 的高優先進化建議表格]

    ---
    ## 📋 HITL 行動清單（請在 3 個工作天內回覆）

    對每個高優先升級項目，請回覆：
    ✅ **批准執行** — 我將立即執行 prompt 優化，預計本週完成
    ❌ **暫緩** — 繼續觀察一個月，下次評估時重新評估
    🔄 **需要討論** — 請在 Nebula 中進一步說明您的考量

    **SLA：請在 $today|date + 3 工作天內回覆，逾期視為「暫緩」**

    ---
    完整報告已儲存：docs/meta-harness/evaluation-$today|date.md
    下次評估：下月 1 日 09:00 Asia/Taipei

    收件人：glen200392@gmail.com
---

每月 1 日 09:00 自動執行（Asia/Taipei）。
McKinsey Organizational Excellence Standard v2.1：
外部基準對比 → MECE 三團隊並行評審（通過 output-schemas.json 驗證）→
金字塔原則系統合成 → Balanced Scorecard → HITL Email 審批（3 天 SLA）。
體現 Meta Harness 的自我評估與系統進化機制。
