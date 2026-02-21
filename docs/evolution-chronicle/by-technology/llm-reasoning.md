# LLM 推理能力演進史
**最後更新：** 2026-02-21 | **維護：** Team B Evolution Chronicle

---

## 演進總覽

```
CoT Prompting (2022) → Self-Consistency (2022) → Tree-of-Thought (2023) → ReAct (2023)
→ o1 Inference-time Scaling (2024) → o3 Extended Thinking (2025) → Reasoning Federation (2026)
```

---

## 2022：Chain-of-Thought — 讓 LLM 「說出思考過程」

**問題起點：** GPT-3 等大模型在多步數學/邏輯問題上頻繁出錯，即使答案在訓練資料中存在。  
**突破：** Wei et al. (Google Brain) 發現：只需在 few-shot 範例中加入「思考步驟」，模型準確率大幅提升。  
**核心機制：** `問題 → 思考步驟 1 → 思考步驟 2 → ... → 答案`  
**關鍵發現：** 能力在 ~100B 參數以上才顯現（湧現能力 Emergent Ability）。  
**影響：** 開啟「推理時計算」研究方向，成為後續所有推理框架的基礎。

---

## 2022：Self-Consistency — 多路推理投票

**問題起點：** 單一 CoT 路徑不穩定，同一問題不同隨機種子結果不同。  
**突破：** 生成多條獨立 CoT 路徑，對最終答案做多數投票（Majority Voting）。  
**影響：** 準確率再提升 5-15%；成為後來「辯論式多 Agent」架構的理論基礎。

---

## 2023：Tree-of-Thought — 推理空間的系統探索

**問題起點：** CoT 是線性路徑，遇到需要回溯的問題（如謎題、規劃）則失敗。  
**突破：** Yao et al. 將推理建模為樹狀搜索：`生成候選步驟 → 評估 → 選擇 → 繼續/回溯`  
**核心機制：** BFS 或 DFS 搜索推理樹，LLM 同時扮演「生成者」與「評估者」。  
**影響：** 證明 LLM 可做自我評估（Self-Evaluation），為後來的 Critic Agent 奠基。

---

## 2023：Program-of-Thought / Tool-Augmented Reasoning

**突破：** 讓 LLM 生成程式碼（Python）代替自然語言計算，再執行取得精確答案。  
**影響：** 數學/科學推理準確率大幅提升；成為 Code Interpreter 的前身。

---

## 2024：o1 — 推理時計算的典範轉移

**問題起點：** 過去靠「更大模型 + 更多訓練資料」提升能力，邊際效益遞減。  
**突破：** OpenAI o1 引入 Inference-time Scaling：允許模型在回答前「想更久」，消耗更多計算。  
**核心機制：** 內部 CoT（不對用戶顯示）+ 強化學習訓練推理過程。  
**關鍵數據：**
- AIME（數學競賽）：GPT-4o 13% → o1 83%
- PhD-level 科學題：GPT-4 水準 → 博士生水準

**典範轉移：** 從「訓練時計算（Scaling Laws）」→「推理時計算（Inference Scaling）」  
**影響：** 開啟全新的能力提升路徑，不再需要更大模型，而是更聰明的推理策略。

---

## 2024：Extended Thinking / Thinking Tokens

**突破：** Anthropic Claude 3.7 Sonnet 引入可調節的「思考預算」（Thinking Budget）。  
**核心機制：** `thinking_level` 參數控制推理深度；思考過程以 `<think>` token 標記，可選擇性顯示。  
**影響：** 用戶可根據任務複雜度動態調配推理計算，平衡成本與準確率。

---

## 2025：o3 — 推理能力的新高峰

**突破：** OpenAI o3 在 ARC-AGI 測試達到 87.5%（人類平均 85%），首次超越人類水準。  
**關鍵能力：**
- 代碼生成與除錯的推理深度大幅提升
- 科學發現類任務（蛋白質結構、數學證明）突破性表現
- 推理時計算可精細控制（low/medium/high compute）

**影響：** 「通用推理」不再是遙遠目標；引發 AGI 里程碑討論。

---

## 2025-2026：推理與 Agent 的融合

**當前趨勢：** 推理能力不再是模型的獨立特性，而是與 Agent 框架深度整合。  
**主要形式：**
1. **Reasoning Agents：** o3/Extended Thinking 作為 Agent 的「決策核心」
2. **Critic-in-the-Loop：** 獨立 Critic Agent 對執行中的推理路徑進行即時評估
3. **Multi-Agent Debate：** 多個 Agent 以辯論形式收斂到更準確答案（Self-Consistency 的分散式版本）
4. **Metacognitive Layer：** Agent 可評估自身推理置信度，決定何時尋求人類確認

---

## 關鍵演進規律

1. **計算投入點的轉移：** 訓練時計算 → 推理時計算 → 兩者並重優化。
2. **自我評估能力的湧現：** 從單純生成 → 能評估自身輸出 → 能主動搜索更好路徑。
3. **推理與行動的融合：** CoT（純推理）→ ReAct（推理+行動）→ Reasoning Agent（深度推理驅動複雜行動）。
4. **成本彈性化：** 從固定計算 → 動態推理預算，按任務重要性分配計算資源。

---

*下次更新目標：* 追蹤 Gemini 3.1 的多模態推理能力 + 2026 Q1 推理 benchmark 最新結果。