# AI Research Federation — 環境可攜性審查報告
**審查日期：** 2026-02-21  
**審查範圍：** 三個 Pipeline Recipes + Evolution Chronicle 資料結構  
**審查員：** Nebula Meta Harness  

---

## 一、審查方法論

針對每個 Pipeline 的每個步驟，逐一驗證以下四個維度：

| 維度 | 說明 |
|------|------|
| **相依性（Dependencies）** | 該步驟需要哪些外部服務、API、或運行時？ |
| **環境相容性（Compatibility）** | 在哪些環境可以原生執行？哪些需要適配？ |
| **容錯機制（Fault Tolerance）** | 步驟失敗時的降級策略是什麼？ |
| **冪等性（Idempotency）** | 重複執行是否安全？輸出是否可預測？ |

---

## 二、共用基礎設施審查

### 2.1 外部服務相依性清單

| 服務 | 用途 | 可替換方案 | 風險等級 |
|------|------|-----------|---------|
| Web Search API | Steps 1-4 資訊採集 | Bing Search API / SerpAPI / Tavily | 低 |
| LLM API (GPT-4 class) | 所有 Agent 步驟 | Claude 3.5 / Gemini 1.5 Pro | 低 |
| Email Delivery | 最終通知 | SMTP / SendGrid / Mailgun | 低 |
| File System Write | 儲存 Markdown 輸出 | S3 / GCS / GitHub commit | 中 |
| GitHub API | 月報上傳 | GitLab API / 本地 Git | 低 |

### 2.2 無狀態 vs 有狀態步驟分析

| 步驟類型 | 說明 | 可攜性 |
|---------|------|--------|
| Web Search (read-only) | 完全無狀態，任何環境均可直接執行 | 極高 |
| LLM Agent Synthesis | 無狀態（輸入 = prompt + 前一步輸出） | 高 |
| File Save | 需要 write 權限，路徑需環境適配 | 中 |
| Email Send | 需要 SMTP/API 憑證 | 中 |
| GitHub Upload | 需要 GitHub token + repo 存取 | 中 |

---

## 三、Pipeline A — Weekly AI Research + Post Generator v2

### 步驟逐一審查

| 步驟 | 說明 | 環境相容性 | 容錯機制 | 冪等性 |
|------|------|-----------|---------|--------|
| Step 1: arXiv Search | web-search，read-only | 全環境 | 失敗時使用空結果，Step 5 仍可執行 | ✅ 是 |
| Step 2: 三大廠更新 | web-search，read-only | 全環境 | 同上 | ✅ 是 |
| Step 3: 技術突破 | web-search，read-only | 全環境 | 同上 | ✅ 是 |
| Step 4: 產業新聞 | web-search，read-only | 全環境 | 同上 | ✅ 是 |
| Step 5: AI Research Advisor 合成 | LLM Agent | Nebula/LangGraph/AutoGen/CrewAI | 若 Steps 1-4 部分失敗，仍可基於可用資料合成 | ✅ 是（輸出確定性由 LLM 溫度控制） |
| Step 6: Team B 演進溯源 | LLM Agent | Nebula/LangGraph/AutoGen/CrewAI | 若 Step 5 無 focus_tech，使用上週焦點技術作為 fallback | ✅ 是 |
| Step 7: 撰寫貼文 + 儲存 | LLM Agent + File Write | Nebula (native) / 需適配 | 檔名含日期，重試安全；檔案系統路徑需環境變數化 | ✅ 是（date-stamped） |
| Step 8: Email 發送 | Email API | Nebula (native) / SMTP 適配 | 失敗時記錄 log，下次手動重送 | ✅ 是（重送不重複，收件人不變） |

**跨環境映射：**

```
Nebula:      Steps 1-8 原生執行
LangGraph:   Steps 1-4 → ToolNode; Steps 5-6 → ReAct Agent Node; 
             Step 7 → FileWrite Node; Step 8 → EmailSend Node
AutoGen v0.4: Steps 1-4 → FunctionTool; Steps 5-6 → AssistantAgent;
              Step 7-8 → 自定義 Actor
CrewAI:      Steps 5-6 → Agent with Task; Steps 1-4 → Tool;
             Step 7-8 → custom Tool
n8n:         Steps 1-4 → HTTP Request Node; Steps 5-6 → OpenAI Node;
             Step 7 → Write File Node; Step 8 → Email Node
```

**關鍵風險：**
- Step 7 的 `$today|date` 時間變數需在非 Nebula 環境中替換為環境變數 `$TODAY`
- Step 6 的 focus_tech JSON block 解析依賴 Step 5 的格式穩定性

---

## 四、Pipeline C — Team C Pedagogy Weekly Lesson

### 步驟逐一審查

| 步驟 | 說明 | 環境相容性 | 容錯機制 | 冪等性 |
|------|------|-----------|---------|--------|
| Step 1: 來源搜尋 | web-search，read-only | 全環境 | 失敗時使用前週 focus_tech hardcode | ✅ 是 |
| Step 2: Level 1 入門教材 | LLM Agent | 全主流框架 | 若 Step 1 失敗，仍可基於 hardcode topic 生成 | ✅ 是 |
| Step 3: Level 2 進階教材 | LLM Agent | 全主流框架 | 同上 | ✅ 是 |
| Step 4: Level 3 專業教材 | LLM Agent | 全主流框架 | 同上 | ✅ 是 |
| Step 5: Quiz 生成 | LLM Agent + JSON output | 全主流框架 | JSON 解析失敗時降級為純文字問答 | ✅ 是 |
| Step 6: 整合儲存 | LLM Agent + File Write | Nebula native / 需適配 | 目錄不存在時自動建立；重試覆蓋安全 | ✅ 是（date-stamped dir） |
| Step 7: Email 摘要 | Email API | Nebula / SMTP 適配 | 同 Pipeline A Step 8 | ✅ 是 |

**特殊考量：**
- Steps 2-5 可並行執行（LangGraph parallel nodes / AutoGen concurrent agents）
- 三難度教材共用同一 topic，確保主題一致性是核心設計要求
- Step 5 的 JSON schema 需要嚴格驗證，建議加入 JSON schema validator 中間層

**跨環境映射：**

```
Nebula:      Steps 1-7 原生執行，Steps 2-5 可由 nebula 內部並行
LangGraph:   Steps 2-5 → ParallelNode (4 concurrent ReAct agents)
             Step 6 → AggregatorNode → FileWriteNode
AutoGen v0.4: Steps 2-5 → 4 AssistantAgents in parallel via Runtime
             Step 6 → GroupChat Summarizer
CrewAI:      Steps 2-5 → 4 Agents, parallel=True in Crew config
```

---

## 五、Pipeline L4 — Meta Harness Monthly Evaluation

### 步驟逐一審查

| 步驟 | 說明 | 環境相容性 | 容錯機制 | 冪等性 |
|------|------|-----------|---------|--------|
| Step 1: 上月 AI 研究基準 | web-search，read-only | 全環境 | 失敗時使用 LLM 知識庫作為近似基準 | ✅ 是 |
| Step 2: AI 教育最佳實踐 | web-search，read-only | 全環境 | 同上 | ✅ 是 |
| Step 3: Team A 品質評審 | LLM Agent + JSON | 全主流框架 | JSON 解析失敗時請求重新生成 | ✅ 是 |
| Step 4: Team B 品質評審 | LLM Agent + JSON | 全主流框架 | 同上 | ✅ 是 |
| Step 5: Team C 品質評審 | LLM Agent + JSON | 全主流框架 | 同上 | ✅ 是 |
| Step 6: 整合分析報告 | LLM Agent | 全主流框架 | Steps 3-5 若部分失敗，仍可基於可用評審生成部分報告 | ✅ 是 |
| Step 7: 儲存 + HITL Email | File Write + Email | Nebula / SMTP 適配 | 儲存失敗時仍發送 Email；Email 失敗時儲存報告供手動查閱 | ✅ 是（date-stamped） |

**Steps 3-5 可完全並行執行（三隊獨立評審，無相依性）**

**HITL 機制可攜性：**

| 環境 | HITL 實作方式 |
|------|-------------|
| Nebula | Email 回覆觸發 manage_agents 更新 |
| LangGraph | `interrupt()` + Human node，等待外部 input |
| AutoGen v0.4 | `UserProxyAgent` 攔截，等待 human_input_mode |
| 手動流程 | Email 審批 → 人工更新 prompt → 下月生效 |

---

## 六、Evolution Chronicle 資料結構可攜性

### evolution-graph.json

| 維度 | 評估 |
|------|------|
| 格式 | 純 JSON，無特殊相依 — 任何環境均可讀寫 |
| 版本控制 | 已存入 GitHub，完整歷史追蹤 |
| 擴展性 | nodes/edges 結構支援無限累積，schema_version 可向後相容 |
| 可視化 | 可直接匯入 D3.js / Cytoscape.js / Neo4j 做圖形展示 |
| 跨環境讀取 | Python `json.load()` / JavaScript `JSON.parse()` / 任何語言均支援 |

### by-technology/*.md

| 維度 | 評估 |
|------|------|
| 格式 | 純 Markdown，無特殊相依 |
| 可讀性 | 人類可直接閱讀，無需工具 |
| 自動更新 | Team B agent 每週追加，使用 git commit 版本控制 |
| 搜尋性 | 可用 grep / 全文搜尋 / 向量嵌入做語意搜尋 |

---

## 七、綜合環境相容性矩陣

| Pipeline / 環境 | Nebula | LangGraph | AutoGen v0.4 | CrewAI | n8n | GitHub Actions |
|----------------|--------|-----------|--------------|--------|-----|---------------|
| Weekly AI Research v2 | ✅ Full | ✅ High | ✅ High | ⚠️ Medium | ⚠️ Low | ❌ Not suitable |
| Team C Pedagogy | ✅ Full | ✅ High | ✅ High | ⚠️ Medium | ❌ Low | ❌ Not suitable |
| Meta Harness Eval | ✅ Full | ✅ High | ✅ High | ⚠️ Medium | ❌ Low | ⚠️ Medium |
| Evolution Chronicle | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full |

**凡例：**
- ✅ Full：原生支援，無需修改
- ✅ High：需少量適配（< 1 天工作量）
- ⚠️ Medium：需中等適配（1-3 天工作量）
- ⚠️ Low：需大量適配（3-7 天工作量）
- ❌ Not suitable：不建議，架構不匹配

---

## 八、可攜性風險識別與緩解

### 高優先風險

| 風險 | 影響 | 緩解措施 |
|------|------|---------|
| 時間變數 `$today|date` 硬綁 Nebula | 非 Nebula 環境無法解析 | 抽取為環境變數 `REPORT_DATE`，pipeline 啟動時注入 |
| Agent ID 硬綁 (`agt_xxx`) | 跨系統無法複用 | 改用 agent_slug，各環境自行映射 slug → 實作 |
| 檔案路徑假設本地 FS | 雲端環境無本地 FS | 抽取 `OUTPUT_BACKEND` 環境變數（local/s3/gcs/github） |
| Email 收件人硬編碼 | 不同部署者需修改代碼 | 抽取為 `NOTIFY_EMAIL` 環境變數 |

### 中優先風險

| 風險 | 影響 | 緩解措施 |
|------|------|---------|
| JSON 解析依賴 LLM 格式穩定性 | 偶發解析失敗 | 加入 JSON schema 驗證 + retry with stricter prompt |
| Steps 3-5 並行無順序保證 | Meta Harness 結果順序不穩定 | Step 6 整合時用 team key 索引，不依賴順序 |
| web-search citation 格式差異 | 跨搜尋引擎來源格式不統一 | Step 5 agent 負責格式化，對上游格式寬容 |

---

## 九、遷移至其他環境的標準 SOP

若要將本系統遷移至 LangGraph 或 AutoGen 環境，建議遵循：

```
Step 1: 複製 docs/recipes/*.md 作為設計文件
Step 2: 設定環境變數
        OPENAI_API_KEY=...
        SEARCH_API_KEY=...
        NOTIFY_EMAIL=glen200392@gmail.com
        OUTPUT_BACKEND=local|s3|github
        REPORT_DATE=$(date +%Y-%m-%d)

Step 3: 映射 Nebula action_key 到目標框架
        web-search     → 目標框架的 web search tool
        send-nebula-email → SMTP / SendGrid tool
        nebula agent   → 目標框架的 LLM agent

Step 4: 保留 evolution-graph.json 和 by-technology/*.md 不變
        （純 JSON/Markdown，無框架相依）

Step 5: 驗證 Steps 1-4 搜尋結果可正確傳入 Step 5
Step 6: 執行一次完整 pipeline，確認輸出格式符合預期
Step 7: 設定 HITL checkpoint（LangGraph interrupt / AutoGen UserProxy）
```

---

## 十、審查結論

| 項目 | 評分 | 說明 |
|------|------|------|
| 整體可攜性 | **8.5/10** | 核心邏輯框架無關，少量 Nebula 特定語法需適配 |
| 容錯設計 | **8/10** | 每個步驟有明確 fallback，HITL checkpoint 完整 |
| 冪等性 | **9/10** | 所有輸出均 date-stamped，重試安全 |
| 文件完整性 | **9/10** | recipes 文件含 Portability Notes，可作為遷移指南 |
| 資料結構可攜性 | **10/10** | JSON + Markdown，完全框架無關 |

**整體評級：A（生產就緒，可攜性強）**

**主要改進建議（優先順序）：**
1. 將 `$today|date`、收件人 email、檔案路徑抽取為環境變數（1 天）
2. 在 Step 5/6 加入 JSON schema 驗證層（半天）
3. 建立 `env.example` 模板，方便其他環境部署（2 小時）

---

*本報告由 Nebula Meta Harness 自動生成，供 Glennn 審閱。*  
*下次審查時間：2026-03-01（Meta Harness 月度評估時一併執行）*
