# AI Agent 框架演進史
**最後更新：** 2026-02-21 | **維護：** Team B Evolution Chronicle

---

## 演進總覽

```
ReAct (2023) → AutoGen v1 (2023) → LangGraph (2024) → Agents SDK / AutoGen v0.4 / HaaS (2025) → Federation Architecture (2026)
```

---

## 2023：ReAct — Agent 推理的基石

**問題起點：** LLM 會思考（CoT），也會呼叫工具，但無法交替進行。  
**突破：** Shunyu Yao et al. 提出 ReAct，將推理（Reasoning）與行動（Acting）交錯循環。  
**核心機制：** `Thought → Action → Observation → Thought → ...`  
**影響：** 所有現代 Agent 框架的基礎原語，無論是 LangChain Agent、AutoGen 還是 OpenAI Function Calling，都基於此模式。

---

## 2023：AutoGen v1 — 多 Agent 對話的先行者

**問題起點：** 單一 Agent 處理複雜任務容易幻覺，缺乏自我校正能力。  
**突破：** Microsoft 推出 AutoGen，讓多個 Agent 以對話形式互相審查、迭代改善。  
**核心機制：** `UserProxy ↔ AssistantAgent` 對話循環，支援 GroupChat 多方辯論。  
**設計模式：** Multi-Agent Debate（辯論式）、Sequential Workflow（序列式）、Group Chat（群聊式）。  
**局限：** 基於同步對話，難以處理長時間非同步任務；狀態管理薄弱。

---

## 2024：LangGraph — 狀態圖治理的崛起

**問題起點：** AutoGen 的對話式協調缺乏可控性，無法保證執行路徑的確定性。  
**突破：** LangChain 推出 LangGraph，以有向圖（DAG + 循環）定義 Agent 工作流，狀態顯式管理。  
**核心機制：** `StateGraph + Nodes + Conditional Edges + Checkpointer`  
**關鍵創新：**
- Human-in-the-Loop 原生支援（暫停、審批、繼續）
- 持久化狀態（工作流中斷後可恢復）
- Supervisor 節點模式（一個節點負責路由決策）

**影響：** 成為 2024-2025 年企業 Agent 工作流的主流選擇。

---

## 2024：MCP — 工具協議標準化

**問題起點：** 每個 Agent 框架自定義工具介面，無法互操作。  
**突破：** Anthropic 發布 Model Context Protocol（MCP），定義 LLM ↔ 工具的標準 JSON-RPC 協議。  
**影響：** 工具生態系統爆發，第三方工具可跨框架使用。

---

## 2025：AutoGen v0.4 — Actor-Model 非同步運行時

**問題起點：** AutoGen v1 的同步對話無法支援大規模並行 Agent。  
**突破：** 完全重寫為 Actor-Model 架構（類似 Erlang/Akka），每個 Agent 是獨立 Actor，透過訊息傳遞非同步通訊。  
**核心機制：** `AgentRuntime + Pub-Sub Topic + Message Protocol`  
**新增模式：** GraphFlow（有向圖控制流）、StateFlow（有限狀態機）、Mixture-of-Agents（多層 Worker + Orchestrator）  
**影響：** 真正的分散式 Agent 系統成為可能。

---

## 2025：OpenAI Agents SDK — Swarm 的生產級繼承者

**問題起點：** OpenAI Swarm（2024）是教育性框架，無法用於生產。  
**突破：** Agents SDK 提供生產就緒的 Supervisor + Guardrails + Parallel Execution。  
**核心機制：** `Agent(instructions, tools) + handoff() + Runner.run()`  
**關鍵創新：**
- Guardrails（輸入/輸出護欄）
- SQLiteSession 持久對話記憶
- Tracing & Observability 內建
- Agents-as-Tools（Agent 可作為工具被其他 Agent 呼叫）

---

## 2025：Harness-as-a-Service（HaaS）— 基礎設施的典範轉移

**問題起點：** Agent 本身越來越強，但「圍繞 Agent 的運行環境」成為瓶頸。  
**突破：** Anthropic 提出 Harness 概念，將 Agent 的監控、評估、狀態管理、人類介入抽象為獨立基礎設施層。  
**核心思想：** 「2025 年是 Agent 普及的一年；2026 年是 Harness 成為核心基礎設施的一年。」  
**組成：** Orchestration Runtime + Quality Evaluation + HITL Checkpoint + Long-running Task Manager  
**影響：** 框架設計從「Agent 優先」轉向「Harness 優先」。

---

## 2025：LangGraph v1.0 + Supervisor-of-Supervisors

**突破：** LangGraph 正式穩定版，引入 `create_supervisor()` API 與分層 Supervisor 模式。  
**核心創新：** 子 Supervisor 管理子領域，主 Supervisor 做跨域協調，支援 50+ Agent 規模。  
**關鍵 API：** `create_supervisor(agents, model)` + `create_react_agent(model, tools, name)`

---

## 2025：Google A2A Protocol — Agent 間通訊標準化

**問題起點：** MCP 解決了 LLM ↔ 工具的通訊，但 Agent ↔ Agent 之間仍無標準。  
**突破：** Google 發布 A2A（Agent-to-Agent）Protocol，基於 JSON-RPC 定義 Agent 間任務委派格式。  
**影響：** 跨框架、跨廠商的 Agent 聯邦成為可能。

---

## 2026：AI Federation Architecture — 聯邦化治理

**問題起點：** 單一 Supervisor 架構在 100+ Agent 規模下出現瓶頸；各團隊知識無法共享。  
**突破：** 多層聯邦架構：Team Supervisor → Domain Supervisor → Meta Harness，結合 A2A 跨團隊通訊與 Knowledge Graph 共享知識。  
**設計原則：** Specialization（專業化）+ Accumulation（累積）+ Evaluation-Driven Evolution（評估驅動升級）  
**當前狀態：** 本系統（AI Research Federation）正在實作此架構。

---

## 關鍵演進規律

1. **控制 vs 靈活性 的鐘擺：** 每隔 1-2 年，架構在「更靈活的對話式」與「更可控的圖式」之間擺盪。
2. **抽象層上移：** 每個世代都在更高層次抽象（工具 → Agent → Harness → Federation）。
3. **協議先行：** 每次大規模採用前，都有標準協議先出現（MCP → A2A）。
4. **評估滯後：** 每個新架構誕生後約 6-12 個月，評估框架才成熟。

---

*下次更新目標：* 追蹤 2026 Q1 各框架的 Federation 支援進度。