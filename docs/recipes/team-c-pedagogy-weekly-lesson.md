# Team C — Pedagogy Federation Weekly Lesson Generator

**Schedule:** Every Monday 10:00 CST (cron: `0 10 * * 1`, after Team A+B completes at 08:00)  
**Pipeline:** Team C (Pedagogy Federation)  
**Input:** Team A weekly report + Team B evolution narrative  
**Output:** 3-level lesson materials + 10-question quiz → saved to `docs/pedagogy/` + Email to Glennn

---

## Pipeline Steps

### Step 1 — Source Content Search (read-only)
- **Action:** `web-search`
- **Query:** `AI agent LLM multi-agent reasoning breakthrough $7d_ago|date site:arxiv.org OR site:openai.com OR site:anthropic.com`
- **Citations:** true

### Step 2 — Level 1 Beginner Material (agent: ai-research-advisor)
**Target audience:** Complete non-technical public  
**Format:** Q&A style, zero jargon, life analogies  
**Length:** 400-500 words, Traditional Chinese  
**Opening:** "這週 AI 世界發生了一件有趣的事..."  
**Closing:** One sentence on daily life implications  
**Output JSON:** `{"topic": "tech topic name", "level1_content": "full material"}`

### Step 3 — Level 2 Intermediate Material (agent: ai-research-advisor)
**Target audience:** Engineers and graduate students with basic AI knowledge  
**Format:** Concept → Core Principles (with terminology) → Real Applications → Python pseudocode (10-15 lines) → Further Reading  
**Length:** 1000-1500 words, Traditional Chinese  
**Code blocks:** Use ` ```python ` markers  
**Output JSON:** `{"topic": "tech topic name", "level2_content": "full material"}`

### Step 4 — Level 3 Advanced Material (agent: ai-research-advisor)
**Target audience:** AI researchers and senior engineers  
**Format:** Research background → Technical details (formulas/architecture) → Key paper citations (APA) → Benchmark comparisons (Markdown table) → Limitations → 3 Open Research Questions  
**Length:** 2000+ words, Traditional Chinese  
**Citations format:** `Author et al. (YYYY). Title. Venue.`  
**Output JSON:** `{"topic": "tech topic name", "level3_content": "full material"}`

### Step 5 — Quiz Generator (agent: ai-research-advisor)
Generates 10-question quiz in JSON format:
```json
{
  "topic": "tech topic",
  "week": "$today|date",
  "questions": [
    {
      "id": 1,
      "level": "beginner|intermediate|advanced",
      "type": "multiple_choice|true_false|short_answer",
      "question": "question text",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "A",
      "explanation": "2-3 sentence explanation"
    }
  ]
}
```
Distribution: 3 beginner (MCQ), 4 intermediate (MCQ + T/F), 3 advanced (short answer). Traditional Chinese.

### Step 6 — Integrate & Save (agent: nebula)
Combines all materials into `docs/pedagogy/weekly-lessons/$today|date/complete-lesson.md`:

```markdown
# 本週 AI 學習課程 — $today|date
**主題：** [topic from Step 2]

## Level 1 — 入門篇（給所有人）
[level1_content]

## Level 2 — 進階篇（給工程師與研究生）
[level2_content]

## Level 3 — 專業篇（給研究者）
[level3_content]

## 本週測驗
[quiz questions in readable Markdown]

*本課程由 AI Research Federation — Team C 教學聯盟自動生成*
```

### Step 7 — Email Delivery (agent: nebula, action: send-nebula-email)
Subject: `📚 Weekly AI Lesson — $today|date（三難度教材已就緒）`

Email sections:
- Part 1: This week's learning topic (why this topic was chosen)
- Part 2: Three-level summaries (first 100 words each + "see full content in docs/")
- Part 3: Quiz preview (first 3 questions out of 10)

Recipient: glen200392@gmail.com

---

## Portability Notes

| Environment | Compatibility | Notes |
|-------------|--------------|-------|
| Nebula (native) | Full | All steps run natively |
| LangGraph | High | Steps 2-5 as parallel nodes; Step 6 as aggregator node |
| AutoGen v0.4 | High | Each level as separate AssistantAgent; GroupChat aggregation |
| CrewAI | Medium | 4 Agents (L1, L2, L3, Quiz) with sequential Tasks |
| Standalone Python | Medium | Each step as async function; requires OpenAI API + file I/O |

**Dependencies:** Web search API, LLM API (GPT-4 class), file system write access, email delivery  
**Trigger dependency:** Designed to run 2 hours after Weekly AI Research pipeline (08:00 → 10:00)  
**Fallback:** If Step 1 search fails, agents use hardcoded topic from previous week's focus_tech  
**Idempotency:** Step 6 uses date-stamped directory — safe to retry