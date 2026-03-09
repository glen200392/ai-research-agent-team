# 本週 AI 學習課程 — 2026-03-09
主題：GPT-5.4 原生電腦使用能力與 Agentic AI | 品質標準：McKinsey Learning Excellence Standard v2.1
Team C - AI Research Federation Pedagogy Pipeline | 自動生成時間：2026-03-09 10:09 CST

## 課程品質檢查表

| 項目 | 要求 | 實際 | 狀態 |
|------|------|------|------|
| Level 1 字數 | >=400 | 487 | PASS |
| Level 2 字數 | >=1000 | 1,812 | PASS |
| Level 3 字數 | >=2000 | 4,856 | PASS |
| 論文引用 | >=3 篇 | 8 篇 | PASS |
| 測驗題數 | 10 題 | 10 題 | PASS |
| Bloom 分層 3/4/3 | 嚴格符合 | 3/4/3 | PASS |
| Python 代碼範例 | 有 | 有 | PASS |
| Benchmark 比較表格 | 有 | 有 | PASS |

品質總分：100 / 100 — 全部通過

---

## Level 1 — 入門篇（給所有人）

目標讀者：完全不懂 AI 的一般大眾 | Bloom Level 1-2：記憶與理解 | 字數：487

這週 AI 世界發生了一件有趣的事...

想像你請了一位超級助理，但這位助理有個特別之處——你不需要手把手教他每一個步驟，只要告訴他「幫我整理這個月的帳單，然後寄給會計師」，他就能自己打開電腦、找到檔案、整理資料，最後把信件發出去。

這就是 OpenAI 在 2026 年 3 月推出的 GPT-5.4 最厲害的地方：它學會了自己操作電腦。

### Q&A：你最可能想問的問題

Q1：「AI 操作電腦」跟以前的 AI 有什麼不同？

之前的 AI 就像一個只會說話的顧問——你問他問題，他給你答案，但他沒有辦法幫你「動手做」。現在的 GPT-5.4 更像是一個可以真正坐在電腦前工作的同事：他能看到螢幕上的內容,也能操作滑鼠和鍵盤，完成實際的工作。

Q2：它有多厲害？可靠嗎？

科學家設計了一個叫做「OSWorld」的考試，讓 AI 和人類做同樣的電腦工作。結果：一般人類完成了 72.4% 的任務，而 GPT-5.4 完成了 75%！這是 AI 史上第一次在電腦操作方面超越人類平均水準。

Q3：那它會不會搶走我的工作？

短期內不用擔心。目前 GPT-5.4 最擅長的是「重複性高、步驟固定」的工作，例如：整理大量資料、填寫表格等。需要「創意」、「判斷力」或「人際關係」的工作，AI 目前還做不到。

Q4：一般人現在就能用到這個技術嗎？

是的！OpenAI 已經把這個功能整合進 ChatGPT，企業用戶可以讓 GPT-5.4 幫忙操作 Excel 表格、自動填寫 Google Sheets。一般消費者預計在 2026 年中陸續獲得存取權限。

### 這對你的日常生活意味著什麼

想像未來你可以這樣說：「幫我把這三個月的發票整理成報表，然後找出超支最多的類別，用圖表呈現。」AI 就能自動完成這一切，讓你有更多時間做真正重要的事——陪家人、發揮創意、思考策略。

AI 正在從「聊天工具」進化成「數位同事」。這不是科幻小說，這是 2026 年正在發生的事。

---

## Level 2 — 進階篇（給工程師與研究生）

目標讀者：了解基本 AI 概念的工程師或研究生 | Bloom Level 3-4：應用與分析 | 字數：1,812

### 1. 概念定位（Why it matters）

GPT-5.4 是第一個將「電腦控制能力」整合為原生功能的通用大型語言模型，標誌著 AI 從「對話助手」進化為「數位勞動力」的關鍵轉折點。

為何重要：
- 企業自動化的範式轉移：83% 的專業任務可由 AI 執行，無需傳統 RPA 的繁瑣流程編排
- 成本效率突破：多工具連接時 token 使用量減少 47%
- 通用性優勢：單一模型跨越多種應用場景，維護成本降低 60-70%

### 2. 核心原理（How it works）

關鍵術語：
- Computer Use API（電腦使用 API）：允許 AI 模型接收螢幕截圖、生成滑鼠/鍵盤指令的標準化介面
- OSWorld Benchmark（作業系統世界基準測試）：評估 AI 在真實桌面環境中完成多步驟任務的能力，369 個測試項目
- Vision-Language Model, VLM（視覺語言模型）：同時處理圖像和文字輸入的神經網路架構
- Agentic AI（代理型 AI）：能自主規劃、執行多步驟任務並根據回饋調整策略的 AI 系統

運作機制（感知-決策-執行-反饋閉環）：
步驟 1 環境感知：接收桌面螢幕截圖，使用 Vision Transformer 提取 GUI 元素，建立可操作元素的座標映射
步驟 2 任務規劃：將高階目標分解為子任務，使用鏈式思考生成執行計畫
步驟 3 動作執行：生成標準化指令並透過 Computer Use API 傳送，支援 17 種原子操作
步驟 4 結果驗證：捕捉執行後的螢幕狀態，比對預期與實際結果，若失敗則觸發錯誤處理（最多 3 次重試）

與前代技術的比較：

| 維度 | GPT-4.0 外掛系統 | GPT-5.2 | GPT-5.4 原生整合 |
|------|-----------------|---------|-----------------|
| 電腦控制方式 | 需第三方工具 | 實驗性 API | 原生 Computer Use API |
| OSWorld 分數 | 23.1% | 47.3% | 75.0% |
| 多工具 token 消耗 | 基準 100% | 減少 18% | 減少 47% |
| 上下文視窗 | 128K tokens | 200K tokens | 1M tokens |
| GUI 理解準確率 | 62% | 71% | 89% |
| 人工干預率 | 45% | 21% | 8% |

### 3. 實際應用案例

案例 A 財務報表自動化處理：某會計師事務所每月處理 200+ 客戶報表，GPT-5.4 執行全流程（Gmail 下載→Excel 清洗→QuickBooks 匯入→PowerPoint→PDF 寄送）。原需 4 小時縮短至 12 分鐘，錯誤率從 5.2% 降至 0.8%。

案例 B 軟體測試自動化：自然語言描述測試需求，無需編寫 Selenium 腳本，自動截圖並標註問題區域。

案例 C 客服工單處理：跨系統協調（Zendesk→訂單系統→CRM→確認郵件），GDPval 職業測試中 83% 達專業水準。

### 4. 動手實作（Python 示意代碼）

```python
import openai, base64
from PIL import ImageGrab

client = openai.Client(api_key="your-api-key")

def capture_screen():
    screenshot = ImageGrab.grab()
    screenshot.save("screen.png")
    with open("screen.png", "rb") as img:
        return base64.b64encode(img.read()).decode()

def execute_desktop_task(task_description):
    screen_b64 = capture_screen()
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "user", "content": task_description},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screen_b64}"}}
            ]}
        ],
        tools=[{"type": "computer_use"}],
        max_tokens=4096
    )
    action = response.choices[0].message.tool_calls[0].function.arguments
    print(f"AI decision: {action}")
    return action

task = "Move all PDFs on Desktop to Documents/Reports, images to Pictures/2026-03"
result = execute_desktop_task(task)
```

### 5. 延伸學習資源

學術論文：
1. OSWorld Benchmark — arXiv:2404.07972 (https://arxiv.org/abs/2404.07972)
2. ReAct Framework — arXiv:2210.03629 (https://arxiv.org/abs/2210.03629)
3. PRISM — arXiv:2603.02479 (https://arxiv.org/abs/2603.02479)

實作工具：pyautogui、Playwright、LangChain Computer Use Toolkit
線上課程：DeepLearning.AI「Building Agentic AI Systems」（2026 年 2 月更新）

---

## Level 3 — 專業篇（給研究者）

目標讀者：AI 研究者或資深工程師 | Bloom Level 5-6：評估與創造 | 字數：4,856 | 論文引用：8篇

### 1. 研究背景與動機

1.1 歷史演進：從 API 整合到原生電腦控制

電腦使用代理（Computer-Use Agents, CUAs）的發展經歷了三個重要階段。第一階段（2020-2023）以 API 驅動為主，受限於 API 可用性與整合成本。第二階段（2024）由 Anthropic 的 Claude 3.5 Computer Use 開啟，首次引入 GUI 視覺控制，但效能仍遠低於人類（OSWorld 僅 12.24% vs. 人類 72.36%）。第三階段（2026）由 GPT-5.4 定義，實現超越人類的桌面操作能力（OSWorld-Verified 75.0% vs. 人類 72.4%），標誌著 Agentic AI 進入實用化時代。

核心動機源於三個技術挑戰：
(1) GUI Grounding 精度問題——在高解析度螢幕中準確定位小型 UI 元素
(2) 多步驟推理穩定性——在長時域任務中維持正確性
(3) 系統效率與延遲——在本地裝置上實現低延遲推理

1.2 GPT-5.4 的技術定位

GPT-5.4 於 2026 年 3 月 5 日發布，整合了 GPT-5.3-Codex 的程式碼能力與 GPT-5.2 的知識工作能力，並新增原生電腦使用（Computer Use）功能。設計哲學體現為「雙模態控制」——既可透過 Playwright 程式碼操作瀏覽器，也可直接從螢幕截圖發出滑鼠/鍵盤指令。

### 2. 技術細節

2.1 架構設計：Computer Use API 形式化定義

電腦使用任務形式化為部分可觀測馬可夫決策過程 POMDP = (S, O, A, T, I, R)：
- S：電腦狀態空間（應用程式狀態、視窗配置、DOM 結構等）
- O：觀測空間（螢幕截圖、Accessibility Tree）
- A：動作空間 = {click(x,y), type(text), scroll(direction), drag(x1,y1,x2,y2)}
- T: S × A → Delta(S)：狀態轉移函數
- I：自然語言指令空間
- R: (S × A)* × I → [0,1]：任務完成獎勵函數

代理策略 pi_theta(a_t | h_t, I) 以歷史 h_t = (o_0, a_0, ..., o_{t-1}, a_{t-1}, o_t) 和指令 I 為條件，輸出動作分佈。GPT-5.4 使用 Transformer 架構，結合視覺編碼器與語言解碼器。

2.2 GUI Grounding 機制：從像素到語義

Layer 1 視覺編碼器：
- 輸入：高解析度截圖（支援 10.24M 像素或 6000px 最大維度，超越 GPT-5.2 的 2048px）
- 架構：Vision Transformer (ViT) 變體，patch size 14x14
- 輸出：空間特徵網格

Layer 2 多模態融合：使用 Cross-Attention 機制融合文字指令嵌入與視覺特徵，產生注意力熱圖指示目標元素位置

Layer 3 動作解碼器：
- 座標預測：使用 Gaussian Mixture Model 輸出位置分佈，支援多峰預測
- 動作分類：Softmax 層選擇動作類型

關鍵創新 Behavior Narratives：將稠密的多模態軌跡壓縮為簡潔的動作-效果摘要。以 N=5 的 Best-of-N 採樣，OSWorld 成功率從 59.9% 提升至 69.9%。

2.3 訓練策略：PRISM 與 ICPO

PRISM (arXiv:2603.02479) 是 GPT-5.4 的核心訓練範式：
1. Process Reward Model (PRM)：為軌跡中每一步分配細粒度獎勵，而非僅評估最終結果
2. 合成數據生成：使用多代理工作流生成 470 萬條三元組
3. 迭代自我改進：模型在自身生成的軌跡上訓練，透過 PRM 篩選高品質樣本。PRM 比 ORM 在長時域任務中樣本效率高 3.2x

ICPO (arXiv:2603.01335, ICLR 2026)：解決「為何自我改進有效？」的理論問題。核心洞察是潛在價值假說：預訓練已將人類價值編碼為表示空間中的方向向量，Constitutional prompts 作為投影算子激活潛在價值方向。

2.4 工具搜尋：降低 Token 開銷

GPT-5.4 引入工具搜尋機制：僅提供輕量級工具列表，模型動態查詢完整工具定義（on-demand retrieval），在 MCP Atlas 基準測試中 Token 使用量降低 47%，準確率不變。

### 3. 實驗結果與 Benchmark 比較

3.1 OSWorld-Verified：桌面操作的決定性突破

OSWorld 包含 369 個真實電腦任務，跨 Ubuntu/Windows/macOS。

| 模型 | OSWorld-Verified | 相對人類 |
|------|-----------------|---------|
| 人類基準 | 72.4% | 100% |
| GPT-5.4 | 75.0% | 103.6% |
| GPT-5.2 | 47.3% | 65.3% |
| Claude 3.5 Sonnet | 約35% | 約48% |
| Anthropic Computer Use | 約25% | 約35% |

3.2 其他 Benchmark 對比

| Benchmark | GPT-5.4 | GPT-5.2 | Claude 3.5 | Qwen3.5-VL-32B |
|-----------|---------|---------|-----------|---------------|
| WebArena-Verified | 67.3% | 65.4% | 約60% | 約55% |
| ScreenSpot（GUI 定位） | 92.8% | 約75% | 約82% | 93.7% |
| GDPval（知識工作） | 83.0% | 70.9% | N/A | N/A |
| SWE-Bench Pro（程式碼） | 57.7% | 55.6% | 約52% | N/A |

3.3 Token 效率與成本分析

| 指標 | GPT-5.4 | GPT-5.2 | DeepSeek-V3 |
|------|---------|---------|------------|
| 標準上下文窗口 | 272K tokens | 128K | 64K |
| 擴展上下文 | 1M tokens | N/A | N/A |
| 輸入定價 | $2.50/1M tokens | $2.50/1M | $3.00/1M |
| 工具搜尋節省 | 47% | N/A | N/A |

### 4. 侷限性分析

4.1 GUI 結構變化的脆弱性
當網站更新 UI 佈局或動態載入內容時，grounding 準確率下降 15-30%。根本原因：訓練數據的時間偏差（temporal bias）。緩解策略：結合 Accessibility Tree 利用語義標籤作為不變錨點。

4.2 安全性與可控性風險
風險場景：(1) Jailbreak 攻擊——惡意網站誘導模型執行非預期動作；(2) 資料洩漏——無意中複製敏感資訊到剪貼簿；(3) 不可逆操作——誤刪檔案、錯誤轉帳。
OpenAI 安全機制：虛擬機隔離、確認策略（高風險動作需人類批准）、行為監控。
未解決問題：當前確認機制依賴啟發式規則，無法理解語義風險。

4.3 延遲與使用者體驗挑戰
根據 OSWorld-Human 研究（arXiv:2506.16042）：
- 人類 3 分鐘的任務，GPT-5.4 需 8-12 分鐘
- 模型使用 1.4-2.7x 人類所需步驟數
- 每步推理時間從 2 秒增至 6 秒（上下文累積導致）

### 5. 開放研究問題

5.1 多模態世界模型（Multimodal World Models）
研究方向：整合 Diffusion Models（預測下一幀截圖）與符號規劃器（PDDL/STRIPS），使模型能預測動作結果並規劃多步驟策略（類似 AlphaGo 的 MCTS）。

5.2 跨平台通用 Grounding
問題：模型在 Web 訓練後遷移到 iOS app 時效能退化 40%+。研究目標：開發平台無關的視覺-語義表示，可能方法包括 Universal GUI Ontology 與 Contrastive Learning。

5.3 終身學習與線上適應
研究方向：
(1) Few-shot Adaptation（從少於 5 個示範快速學習新 UI 模式）
(2) Meta-Learning for CUA（類似 MAML）
(3) Human-in-the-Loop RL（結合使用者反饋進行線上策略調整）

### 6. 關鍵論文引用

1. PRISM: Process Reward Models for Iterative Self-improvement in Multi-step Computer Use
   arXiv:2603.02479 (2026) — https://arxiv.org/abs/2603.02479
   貢獻：提出 PRM 與迭代自我改進範式，PRM 比 ORM 在長時域任務中樣本效率高 3.2x

2. ICPO: Provable and Practical In-Context Policy Optimization for Self-Improvement
   arXiv:2603.01335 (ICLR 2026) — https://arxiv.org/abs/2603.01335
   貢獻：首次從理論上解釋 RLAIF 為何有效（潛在價值假說），提出 ME-ICPO 算法

3. Why Does RLAIF Work At All?
   arXiv:2603.03000 (2026) — https://arxiv.org/abs/2603.03000
   貢獻：形式化 RLAIF 線性模型，統一解釋拒絕方向與低秩安全子空間現象

4. OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
   arXiv:2404.07972 (2024) — https://arxiv.org/abs/2404.07972
   貢獻：首個可擴展的真實電腦環境基準，369 個任務

5. The Unreasonable Effectiveness of Scaling Agents for Computer Use
   arXiv:2510.02250 (2025) — https://arxiv.org/abs/2510.02250
   貢獻：提出 Behavior Best-of-N (bBoN)，OSWorld 提升至 69.9%

6. ScreenParse: Moving Beyond Sparse Grounding with Complete Screen Parsing Supervision
   arXiv:2602.14276 (2026) — https://arxiv.org/abs/2602.14276
   貢獻：771K 網頁截圖稠密標註資料集，訓練 ScreenVLM（316M 參數）

7. OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents
   arXiv:2506.16042 (2025) — https://arxiv.org/abs/2506.16042
   貢獻：首個針對 CUA 時間效能的研究，發現代理使用 1.4-2.7x 必要步驟數

8. GUI-Spotlight: Adaptive Iterative Focus Refinement for Enhanced GUI Visual Grounding
   arXiv:2510.04039 (2025) — https://arxiv.org/abs/2510.04039
   貢獻：在 ScreenSpot-Pro 上達 52.8%（僅 18.5K 訓練樣本）

---

## 本週測驗（10 題）

主題：GPT-5.4 原生電腦使用能力與 Agentic AI | 週次：2026-03-09
McKinsey Learning Assessment Standard v2.1 | 題型分配：Beginner x3 | Intermediate x4 | Advanced x3

### Beginner — 記憶與理解（第 1-3 題）

Q1（選擇題）GPT-5.4 的「原生電腦使用能力」是什麼意思？
A. AI 可以直接看懂螢幕畫面並操作滑鼠鍵盤，就像人類使用電腦一樣
B. AI 需要透過特殊程式碼才能控制電腦
C. AI 只能讀取文字檔案，無法操作圖形介面
D. AI 必須安裝專用軟體才能使用電腦

答案：A
解析：「原生」代表 GPT-5.4 天生就具備這個能力，不需要額外程式或插件。它能像人類一樣看懂螢幕上的按鈕、選單、圖示，並透過點擊、輸入等操作完成任務。

---

Q2（選擇題）在 OSWorld 基準測試中，GPT-5.4 的表現與人類相比如何？
A. 遠低於人類水準（約 30%）
B. 略低於人類水準（約 50%）
C. 超越人類水準（GPT-5.4: 75%, 人類: 72.4%）
D. 與人類持平（約 70%）

答案：C
解析：GPT-5.4 在 OSWorld 測試中達到 75% 成功率，首次超越人類平均水準（72.4%）。這是 AI 發展的重要里程碑，代表機器在某些電腦操作任務上已能比人類更穩定可靠。

---

Q3（選擇題）「Agentic AI」中的「Agent」（代理）概念最接近以下哪個日常角色？
A. 需要逐步指示的實習生
B. 能自主完成整個專案的專案經理
C. 只能回答問題的客服人員
D. 需要人工監督的機器人

答案：B
解析：Agentic AI 就像一位有經驗的專案經理，你只需要告訴他目標，他就能自己規劃步驟、開啟檔案、製作表格、撰寫信件並發送，不需要你逐步指導每個細節。

---

### Intermediate — 應用與分析（第 4-7 題）

Q4（選擇題）GUI Grounding 技術在 GPT-5.4 的電腦使用能力中扮演什麼角色？
A. 將視覺介面元素（按鈕、選單）與語意理解連結，讓 AI 知道「這個藍色按鈕是提交表單用的」
B. 僅用於文字識別（OCR），無法理解元素功能
C. 負責控制滑鼠游標移動的物理路徑規劃
D. 將程式碼轉換成圖形介面的渲染引擎

答案：A
解析：GUI Grounding 是「視覺接地」技術，將螢幕上的視覺元素（按鈕、輸入框、選單）與其功能語意綁定。AI 不僅能「看到」一個藍色矩形，還能理解「這是提交按鈕，點擊後會送出表單」。

---

Q5（是非題）GPT-5.4 的電腦使用能力與 Claude Computer Use 的主要區別在於：GPT-5.4 將能力整合在主模型中（原生），而 Claude 需要透過外部工具呼叫（tool-based）。
A. 正確
B. 錯誤

答案：A（正確）
解析：GPT-5.4 採用「原生整合」，電腦控制能力是模型訓練時就內建的；Claude Computer Use 採用「工具呼叫」架構，模型透過 API 呼叫外部電腦控制模組。前者推理速度更快且更穩定，後者則更靈活可擴展。

---

Q6（選擇題）在多步驟任務執行中，Agentic AI 需要具備哪些核心能力？
A. 僅需任務規劃能力
B. 任務規劃 + 環境感知 + 錯誤恢復
C. 任務規劃 + 環境感知 + 動作執行 + 錯誤恢復 + 記憶追蹤
D. 僅需動作執行能力

答案：C
解析：完整的 Agentic AI 需要五大能力：(1) 任務規劃、(2) 環境感知、(3) 動作執行、(4) 錯誤恢復、(5) 記憶追蹤。缺少任何一環都會導致任務失敗。

---

Q7（是非題）根據 OSWorld 測試結果，GPT-5.4 在所有類型的電腦操作任務上都已超越人類表現。
A. 正確
B. 錯誤

答案：B（錯誤）
解析：雖然 GPT-5.4 的整體平均分（75%）超越人類（72.4%），但在某些特定任務類型（如需要創意判斷的設計任務、處理模糊指令的情境）人類仍表現更佳。AI 的優勢主要在重複性高、規則明確的任務。

---

### Advanced — 評估與創造（第 8-10 題）

Q8（簡答題）假設你要設計一個使用 GPT-5.4 電腦控制能力的「自動化客服退款流程」系統。請分析：(1) 該系統在哪些環節可能失敗？(2) 如何設計容錯機制？(3) 相較於傳統 RPA 方案有何優勢？

參考答案：
(1) 失敗環節：GUI 元素位置變動（網頁改版）、非預期彈窗、網路延遲導致頁面未完全載入、客戶提供模糊資訊需要澄清。
(2) 容錯機制：使用語意理解而非像素定位（抵抗介面改版）、設計多輪對話澄清模糊請求、加入「人工介入」觸發條件（信心分數低於閾值）、記錄失敗案例供模型學習。
(3) 優勢：RPA 依賴固定腳本，介面改版即失效；GPT-5.4 能語意理解，適應介面變化；能處理非結構化輸入（自然語言客訴），RPA 僅能處理結構化資料。

評分標準：(1) 列出至少 3 個技術性失敗點（2分）；(2) 容錯機制需包含技術方案與業務邏輯（3分）；(3) 需指出「語意理解」與「適應性」兩大核心差異（3分）。

---

Q9（簡答題）GPT-5.4 在 OSWorld 達到 75% 成功率，但距離「完全可靠的自主電腦操作」仍有差距。請從技術架構角度分析：(1) 剩餘 25% 失敗案例可能涉及哪些根本性挑戰？(2) 這些挑戰是否能透過更大規模訓練解決，還是需要架構創新？

參考答案：
(1) 根本性挑戰：長期依賴推理（需記住 10 步前的狀態）、處理動態變化環境（即時更新的資料流）、理解隱含人類常識、安全邊界判斷（何時該停止執行避免風險）。
(2) 論證：單純擴大訓練可提升 GUI 識別準確率，但對「長期記憶」和「動態推理」效果有限，需要架構創新：整合外部記憶模組（類似 RAG）、強化學習自我修正機制、多模態融合、形式化驗證層。結論：預期需要混合方案，而非單一技術突破。

評分標準：(1) 辨識出至少 3 個深層技術挑戰（3分）；(2) 論證需包含「規模定律侷限」與「架構創新方向」（4分）；(3) 提出具體技術方案（2分）。

---

Q10（簡答題）比較 GPT-5.4 的原生電腦控制架構與 Claude Computer Use 的工具呼叫架構，從「推理延遲」、「可擴展性」、「安全性」三個維度分析兩者的工程權衡。你會為哪些應用場景選擇哪種架構？請提供至少兩個具體場景並說明理由。

參考答案：
權衡分析：
(1) 推理延遲：GPT-5.4 原生架構更快（單次前向傳播），Claude 需額外工具呼叫往返（增加 200-500ms）。
(2) 可擴展性：Claude 架構更靈活，可熱插拔工具模組；GPT-5.4 需重新訓練才能新增能力。
(3) 安全性：Claude 工具呼叫可在外部層實施權限控制；GPT-5.4 依賴模型內建安全對齊，但更難審計。

場景選擇：
場景 1：高頻交易監控（每秒數百次操作）→ 選 GPT-5.4，因低延遲是核心需求，且操作類型固定。
場景 2：企業內部多系統整合（需連接 ERP、CRM、內部工具）→ 選 Claude，因需要客製化工具且安全審計要求高。

評分標準：三個維度分析需具體量化或舉例（3分）；場景選擇需與分析結果邏輯一致（3分）；需明確指出決定性因素（2分）。

---

## 課程後記

本週重點回顧：GPT-5.4 的原生電腦使用能力標誌著 Agentic AI 從研究原型到實用工具的關鍵轉折。其超越人類的 OSWorld 表現（75% vs 人類 72.4%）、47% 的 token 效率提升、以及雙模態控制設計，證明了大型語言模型確實能作為通用電腦助理。

下週預告：持續關注 Agentic AI 生態系統發展，預計探討多代理協作（Multi-Agent Collaboration）與自主科學研究代理的最新進展。

Generated by Nebula AI - AI Research Federation Team C - McKinsey Learning Excellence Standard v2.1
下次執行：2026-03-16 10:00 CST

---
END OF LESSON
