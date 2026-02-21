# Weekly AI Research + Post Generator (v2 — with Evolution Chronicle)

**Schedule:** Every Monday 08:00 CST (cron: `0 8 * * 1`)  
**Pipeline:** Team A (Current Intelligence) + Team B (Evolution Chronicle)  
**Output:** Structured weekly report + evolution narrative + social post → Email to Glennn

---

## Pipeline Steps

### Step 1 — arXiv Search (read-only)
- **Action:** `web-search`
- **Query:** `AI agent architecture multi-agent LLM reasoning multimodal site:arxiv.org published after:$7d_ago|date`
- **Citations:** true

### Step 2 — Big Three Model Updates (read-only)
- **Action:** `web-search`
- **Query:** `OpenAI Anthropic Google DeepMind AI model release platform update $7d_ago|date to $today|date`
- **Citations:** true

### Step 3 — Tech Breakthrough Search (read-only)
- **Action:** `web-search`
- **Query:** `AI technology breakthrough innovation milestone $7d_ago|date healthcare science hardware open-source industry`
- **Citations:** true

### Step 4 — Industry News Search (read-only)
- **Action:** `web-search`
- **Query:** `AI industry news funding acquisition regulation competition $7d_ago|date site:techcrunch.com OR site:venturebeat.com OR site:theverge.com`
- **Citations:** true

### Step 5 — AI Research Advisor: Synthesize Weekly Report (agent: ai-research-advisor)
Integrates Steps 1-4 into structured weekly report with sections:
1. Key Papers (3-5, with relevance score 1-10)
2. Model & Platform Updates (OpenAI/Anthropic/Google with impact assessment)
3. Tech Breakthrough Highlights (medical, science, hardware, open-source)
4. Industry Dynamics (funding, competition, regulation)
5. Architecture Insights (new patterns worth adopting)
6. Recommended Actions (1-3 concrete suggestions)
7. Next Week Watch List

**Also outputs JSON block:**
```json
{"focus_tech": "tech name", "tech_domain": "agent/reasoning/architecture/training/protocol", "why_important": "one sentence"}
```

### Step 6 — Team B Evolution Chronicle (agent: ai-research-advisor)
Based on `focus_tech` from Step 5, writes evolution narrative:

```markdown
## 技術演進溯源：[tech name] 的歷史脈絡
**起點（YYYY）：** original problem + pioneer
**關鍵突破（YYYY）：** what paper/release made it take off
**演進分叉（YYYY）：** different development directions
**與本週新聞的連結：** which evolution line does this week's news extend?
**預期下一步：** predicted next breakthrough based on evolution pattern
```
Length: 500-800 words, Traditional Chinese, historical depth required.

### Step 7 — Compose Social Post + Save (agent: nebula)
Combines Step 5 report + Step 6 evolution narrative into a complete Traditional Chinese social post (LinkedIn/Medium/Threads style). Saves as `docs/weekly_post_$today|date.md`.

Post structure:
1. Attention-grabbing title (with emoji)
2. Top 3-4 AI developments this week
3. Key numbers & milestones
4. [Evolution Perspective] 150-200 words from Step 6
5. Practical insights for practitioners
6. Action recommendations for readers
7. Interactive closing question
8. Tags: #AIAgent #多智能體 #LLM #AI架構 #AIBreakthrough

Length: 1200-1800 words, professional but approachable.

### Step 8 — Email Delivery (agent: nebula, action: send-nebula-email)
Subject: `🤖 Weekly AI Report + Evolution Chronicle — $today|date`

Email sections:
- Part 1: Weekly Research Summary (from Step 5)
- Part 2: Tech Evolution Narrative (from Step 6)  
- Part 3: Social Post ready to publish (from Step 7)
- Part 4: Sources used this week

Recipient: glen200392@gmail.com

---

## Portability Notes

| Environment | Compatibility | Notes |
|-------------|--------------|-------|
| Nebula (native) | Full | All steps run natively |
| LangGraph | High | Steps 5-6 map to ReAct nodes; Steps 1-4 as tool calls |
| AutoGen v0.4 | High | Steps 5-6 as AssistantAgents; web-search as FunctionTool |
| CrewAI | Medium | Steps 5-6 as Agents with Tasks; web-search as custom Tool |
| n8n / Zapier | Low | Steps 1-4 feasible; AI steps require external LLM API |

**Dependencies:** Web search API, LLM API (GPT-4 class), email delivery  
**Fallback:** If web-search fails on any step, agent uses cached results from previous week  
**Idempotency:** Step 7 file save uses date-stamped filename — safe to retry