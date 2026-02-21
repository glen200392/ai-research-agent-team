---
slug: team-c-pedagogy-federation-weekly-lesson-generator
title: Team C — Pedagogy Federation Weekly Lesson Generator
version: "2.1.0"
standard: McKinsey Learning Excellence Standard
last_updated: "2026-02-21"
owner: AI Research Federation — Team C Pedagogy Federation
sla: every Monday 10:00 Asia/Taipei
kpi_targets:
  level1_min_words: 400
  level2_min_words: 1000
  level3_min_words: 2000
  quiz_questions: 10
  level_distribution: "3 beginner / 4 intermediate / 3 advanced"
  schema_validation: strict
steps:

# =============================================================================
# PHASE 1 — TOPIC INTELLIGENCE (Step 1)
# Source: Weekly AI Research Report + fresh search for pedagogical framing
# =============================================================================

- description: "[INTELLIGENCE] 搜尋本週 AI 焦點技術最新資訊，確立教學主題與三難度學習目標"
  action_key: web-search
  action_props:
    query: "AI agent LLM multi-agent reasoning breakthrough $7d_ago|date site:arxiv.org OR site:openai.com OR site:anthropic.com OR site:deepmind.google"
    citations: true
    num_results: 5

# =============================================================================
# PHASE 2 — THREE-LEVEL CONTENT GENERATION (Steps 2-5)
# McKinsey Learning Design: Bloom's Taxonomy × Feynman Technique
# Schema: Must pass output-schemas.json validation before Step 6
# Note: Steps 2-4 share the same topic — consistency is a core design requirement
# =============================================================================

- description: "[LEVEL-1] 入門教材：Feynman 技法，生活化類比，零術語，400-500 字"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation Team C 教學聯盟的入門教材設計師。
    根據 $prev 的搜尋結果，選出本週最重要的一個 AI 技術突破。

    使用「費曼技法（Feynman Technique）」：如果你無法用簡單語言解釋，你就還不夠了解它。

    ## 教材設計原則
    - 目標讀者：完全不懂 AI 的一般大眾（Bloom's Level 1-2：記憶與理解）
    - 零技術術語，若必須使用，立即用日常語言解釋
    - 每個概念搭配一個生活類比
    - Q&A 結構：設想讀者最自然會問的問題，然後回答

    ## 格式要求
    開頭：「這週 AI 世界發生了一件有趣的事...」
    結構：
    1. 一段話：這是什麼（用類比）
    2. Q&A 3-4 組（讀者最想問的問題）
    3. 結尾：「這對你的日常生活意味著什麼」（具體且正面）

    字數：400-500 字，繁體中文，語調輕鬆親切。

    ## 必須輸出 JSON（通過 output-schemas.json#/definitions/lesson_level1 驗證）
    ```json
    {"topic": "技術主題名稱（2-100字）", "level1_content": "完整教材內容", "target_audience": "general_public", "word_count": 整數}
    ```

- description: "[LEVEL-2] 進階教材：術語+原理+Python代碼，1000-1500 字，含延伸資源"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation Team C 教學聯盟的進階教材設計師。
    根據 $step.2 中的 topic，撰寫 Level 2 進階教材。

    目標讀者：了解基本 AI 概念、想深入學習的工程師或研究生（Bloom's Level 3-4：應用與分析）

    ## 教材結構（McKinsey 結構化呈現）
    ### 1. 概念定位（Why it matters — 結論先行）
    先說清楚：這個技術解決了什麼問題？在 AI 生態中處於什麼位置？

    ### 2. 核心原理（How it works）
    - 關鍵術語（第一次出現時括號中文解釋）
    - 運作機制（步驟化，可視化描述）
    - 與前代技術的比較（用表格）

    ### 3. 實際應用案例（Where it's used）
    2-3 個真實應用場景，含量化效益

    ### 4. 動手實作（Python 示意代碼）
    ```python
    # 10-20 行，有完整注釋，展示核心概念
    # 不需要可執行，但邏輯要正確
    ```

    ### 5. 延伸學習資源
    - 原始論文（APA 格式）
    - 推薦入門資源 2-3 個

    字數：1000-1500 字，繁體中文，術語搭配中文解釋。

    ## 必須輸出 JSON（通過 output-schemas.json#/definitions/lesson_level2 驗證）
    ```json
    {"topic": "技術主題名稱", "level2_content": "完整教材內容", "has_code_example": true, "word_count": 整數}
    ```

- description: "[LEVEL-3] 專業教材：論文引用+架構細節+Benchmark+開放問題，2000+ 字"
  agent_slug: ai-research-advisor
  format_guide: |
    你是 AI Research Federation Team C 教學聯盟的專業教材設計師。
    根據 $step.2 中的 topic，撰寫 Level 3 專業教材。

    目標讀者：AI 研究者或資深工程師（Bloom's Level 5-6：評估與創造）

    ## 教材結構（學術論文標準 × McKinsey 可讀性）
    ### 1. 研究背景與動機
    - 前驅工作（Pre-cursor work）：列出 2-3 篇奠基論文
    - 核心問題陳述（Problem Statement）
    - 研究空白（Research Gap）

    ### 2. 技術細節
    - 形式化定義（數學符號或偽代碼描述核心機制）
    - 架構圖文字描述（清晰到讀者能重建架構）
    - 關鍵設計決策（Design Decisions）及其 trade-offs

    ### 3. 實驗結果與 Benchmark 比較
    | 方法 | Benchmark A | Benchmark B | 參數量 | 訓練成本 |
    |------|-------------|-------------|--------|---------|
    | 本技術 | | | | |
    | Baseline 1 | | | | |
    | Baseline 2 | | | | |

    ### 4. 侷限性分析（Honest Assessment）
    至少 3 個已知侷限，含可能的緩解方案

    ### 5. 開放研究問題（Open Problems）
    3 個具體的、值得研究的開放問題，每個含：
    - 問題描述
    - 為何重要
    - 可能的研究方向

    ### 6. 關鍵論文引用（APA 格式）
    至少 5 篇，含 arXiv 連結

    字數：2000+ 字，繁體中文，學術嚴謹且可讀。

    ## 必須輸出 JSON（通過 output-schemas.json#/definitions/lesson_level3 驗證）
    ```json
    {"topic": "技術主題名稱", "level3_content": "完整教材內容", "citation_count": 整數, "has_comparison_table": true, "word_count": 整數}
    ```

- description: "[QUIZ] 生成 McKinsey 評量標準測驗題（10題 Bloom's Taxonomy 分層，含答案解析）"
  agent_slug: ai-research-advisor
  format_guide: |
    根據 $step.2 的 topic 與三個難度的教材（$step.2, $step.3, $step.4），
    生成一份符合 McKinsey Learning Assessment Standard 的 10 題測驗。

    ## 測驗設計原則
    - Bloom's Taxonomy 分層：beginner（記憶/理解）、intermediate（應用/分析）、advanced（評估/創造）
    - 鑑別度：每題應能區分已學習者與未學習者
    - 解析品質：解釋不只是「正確答案是 X」，而是說明為什麼，以及常見誤解

    ## 題型分配
    - 3 題 beginner：選擇題（4 選 1）
    - 4 題 intermediate：選擇題（4 選 1）或是非題
    - 3 題 advanced：簡答題（要求推理，不只是記憶）

    ## 必須輸出 JSON（嚴格通過 output-schemas.json#/definitions/quiz_output 驗證）
    ```json
    {
      "topic": "技術主題名稱",
      "week": "$today|date",
      "questions": [
        {
          "id": 1,
          "level": "beginner",
          "type": "multiple_choice",
          "question": "題目",
          "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
          "answer": "A",
          "explanation": "解析說明（2-3句，說明為什麼正確且解釋常見誤解）"
        }
      ],
      "level_distribution": {"beginner": 3, "intermediate": 4, "advanced": 3}
    }
    ```
    確保恰好 10 題，level_distribution 嚴格符合 3/4/3。

# =============================================================================
# PHASE 3 — INTEGRATION & DELIVERY (Steps 6-7)
# McKinsey Deliverable Standard: Complete, self-contained, immediately usable
# =============================================================================

- description: "[INTEGRATE] 整合三難度教材與測驗，儲存為完整課程 Markdown 檔案，含品質檢查表"
  agent_slug: nebula
  format_guide: |
    將以下內容整合並儲存為 docs/pedagogy/weekly-lessons/$today|date/complete-lesson.md。

    完整檔案結構：

    ---
    # 本週 AI 學習課程 — $today|date
    **主題：** [來自 $step.2 的 topic]
    **生成時間：** $today|date
    **品質標準：** McKinsey Learning Excellence Standard v2.1
    **涵蓋難度：** Level 1（入門）｜ Level 2（進階）｜ Level 3（專業）

    ## 課程品質檢查表（自動驗證）
    | 項目 | 要求 | 實際 | 狀態 |
    |------|------|------|------|
    | Level 1 字數 | ≥400 | [word_count from $step.2] | ✅/❌ |
    | Level 2 字數 | ≥1000 | [word_count from $step.3] | ✅/❌ |
    | Level 3 字數 | ≥2000 | [word_count from $step.4] | ✅/❌ |
    | 代碼範例 | 必須有 | [has_code_example from $step.3] | ✅/❌ |
    | 論文引用 | ≥3 篇 | [citation_count from $step.4] | ✅/❌ |
    | 比較表格 | 必須有 | [has_comparison_table from $step.4] | ✅/❌ |
    | 測驗題數 | 10 題 | 10 | ✅ |
    | 測驗分層 | 3/4/3 | [from $step.5] | ✅/❌ |

    ---
    ## Level 1 — 入門篇（給所有人）
    [插入 $step.2 的 level1_content]

    ---
    ## Level 2 — 進階篇（給工程師與研究生）
    [插入 $step.3 的 level2_content]

    ---
    ## Level 3 — 專業篇（給研究者）
    [插入 $step.4 的 level3_content]

    ---
    ## 本週測驗（10 題，Bloom's Taxonomy 分層）
    [將 $step.5 的 JSON 測驗題轉為可讀 Markdown 格式：
     每題顯示：題號、難度標籤、題目、選項（換行）、答案、解析]

    ---
    *本課程由 AI Research Federation — Team C 教學聯盟自動生成*
    *品質標準：McKinsey Learning Excellence Standard v2.1*
    *下一步：Meta Harness 將於月底評審本課程品質*

    完成後輸出：{"file_path": "docs/pedagogy/weekly-lessons/$today|date/complete-lesson.md", "quality_check_passed": true/false, "failed_checks": []}

- description: "[DELIVER] Email 發送本週三難度教材 Executive Brief 給 Glennn"
  agent_slug: nebula
  action_key: send-nebula-email
  format_guide: |
    發送 Email，主旨：「📚 Weekly AI Lesson — $today|date | 三難度教材已就緒 | McKinsey Standard」

    Email 結構：

    ## EXECUTIVE BRIEF（30 秒閱讀版）
    本週學習主題：[topic]
    為何選此主題：[來自 $step.2 的選題理由，一句話]
    課程品質狀態：[來自 $step.6 的 quality_check_passed]

    ## 品質檢查結果
    [插入 $step.6 的品質檢查表]

    ## 三難度教材摘要
    **Level 1 入門篇（給所有人）**
    [前 150 字摘要]→ 完整內容見附件

    **Level 2 進階篇（給工程師與研究生）**
    [前 150 字摘要，含代碼範例片段]→ 完整內容見附件

    **Level 3 專業篇（給研究者）**
    [前 150 字摘要，含引用論文列表]→ 完整內容見附件

    ## 本週測驗預覽（前 3 題）
    [列出第 1-3 題題目（不含答案），邀請 Glennn 挑戰]

    ## 完整課程位置
    docs/pedagogy/weekly-lessons/$today|date/complete-lesson.md

    收件人：glen200392@gmail.com
---

每週一 10:00 自動執行（Asia/Taipei，在 Team A+B 週報完成後觸發）。
McKinsey Learning Excellence Standard v2.1：
Feynman 技法（Level 1）× 結構化原理（Level 2）× 學術嚴謹（Level 3）× Bloom's Taxonomy 評量。
所有 JSON 輸出須通過 docs/config/output-schemas.json 嚴格驗證後才進入整合步驟。
