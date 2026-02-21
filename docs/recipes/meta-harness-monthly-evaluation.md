# Meta Harness — Monthly Quality Evaluation & Evolution Report

**Schedule:** 1st of every month, 09:00 CST (cron: `0 9 1 * *`)  
**Layer:** 4 — Meta Harness (Vertical Integration & Coordination)  
**Purpose:** Self-evaluation of all three teams + HITL upgrade approval  
**Output:** Cross-team insight report → saved to `docs/meta-harness/` + Email to Glennn for HITL

---

## Pipeline Steps

### Step 1 — Last Month AI Research Baseline (read-only)
- **Action:** `web-search`
- **Query:** `AI agent LLM major breakthroughs research milestones last month $30d_ago|date to $today|date`
- **Citations:** true
- **Purpose:** Establishes ground truth for evaluating Team A's coverage accuracy

### Step 2 — AI Education Best Practices Baseline (read-only)
- **Action:** `web-search`
- **Query:** `AI education best practices explainable AI knowledge transfer pedagogy 2026`
- **Citations:** true
- **Purpose:** Establishes benchmark for evaluating Team C's pedagogy quality

### Step 3 — Team A Quality Review (agent: ai-research-advisor)
Evaluates Team A (Current Intelligence) against Step 1 baseline.

**Output JSON:**
```json
{
  "team": "Team A — Current Intelligence",
  "evaluation_month": "$today|date",
  "scores": {
    "coverage_breadth": {"score": 0-100, "comment": "which domains covered, which missed"},
    "technical_accuracy": {"score": 0-100, "comment": "accuracy of technical descriptions"},
    "insight_depth": {"score": 0-100, "comment": "depth beyond news aggregation"},
    "actionability": {"score": 0-100, "comment": "how actionable the recommendations are"}
  },
  "overall_score": 0-100,
  "strengths": ["strength1", "strength2"],
  "improvement_areas": ["area1", "area2"],
  "upgrade_needed": true/false,
  "upgrade_suggestion": "if upgrade_needed, specific upgrade direction"
}
```

### Step 4 — Team B Quality Review (agent: ai-research-advisor)
Evaluates Team B (Evolution Chronicle) against Step 1 baseline.

**Output JSON:**
```json
{
  "team": "Team B — Evolution Chronicle",
  "evaluation_month": "$today|date",
  "scores": {
    "historical_depth": {"score": 0-100, "comment": "time depth and completeness of tracing"},
    "connection_accuracy": {"score": 0-100, "comment": "accuracy of tech evolution links"},
    "narrative_quality": {"score": 0-100, "comment": "how engaging the storytelling is"},
    "predictive_value": {"score": 0-100, "comment": "accuracy of future evolution predictions"}
  },
  "overall_score": 0-100,
  "strengths": ["strength1", "strength2"],
  "improvement_areas": ["area1", "area2"],
  "upgrade_needed": true/false,
  "upgrade_suggestion": "if upgrade_needed, specific upgrade direction"
}
```

### Step 5 — Team C Quality Review (agent: ai-research-advisor)
Evaluates Team C (Pedagogy Federation) against Step 2 baseline.

**Output JSON:**
```json
{
  "team": "Team C — Pedagogy Federation",
  "evaluation_month": "$today|date",
  "scores": {
    "level_appropriateness": {"score": 0-100, "comment": "how well 3 levels serve target audiences"},
    "conceptual_accuracy": {"score": 0-100, "comment": "accuracy of teaching content"},
    "pedagogy_quality": {"score": 0-100, "comment": "teaching design and knowledge transfer effectiveness"},
    "quiz_quality": {"score": 0-100, "comment": "quiz quality and discrimination power"}
  },
  "overall_score": 0-100,
  "strengths": ["strength1", "strength2"],
  "improvement_areas": ["area1", "area2"],
  "upgrade_needed": true/false,
  "upgrade_suggestion": "if upgrade_needed, specific upgrade direction"
}
```

### Step 6 — Meta Harness Integrated Analysis (agent: ai-research-advisor)
Synthesizes Steps 3-5 into the monthly system evolution report.

**Output format (Traditional Chinese Markdown):**
```markdown
# AI Research Federation — 月度 Meta Harness 評估報告
**評估月份：** $today|date

## 一、三團隊綜合評分
| 團隊 | 總分 | 最強項 | 最弱項 |
|------|------|--------|--------|
| Team A | X/100 | ... | ... |
| Team B | X/100 | ... | ... |
| Team C | X/100 | ... | ... |

## 二、本月最大亮點
（top 2-3 commendable performances across all teams）

## 三、跨團隊協同分析
（how teams reinforce each other; strongest and weakest handoff points）

## 四、系統瓶頸識別
（biggest performance bottleneck in the entire Federation）

## 五、進化建議（需 HITL 確認）
（all upgrade_needed: true items with problem description, upgrade direction, expected impact, difficulty level）

## 六、下月重點觀察指標
（3-5 specific quality metrics to track next evaluation）
```

### Step 7 — Save Report + Email HITL (agent: nebula, action: send-nebula-email)
Saves full report as `docs/meta-harness/evaluation-$today|date.md`

Subject: `🧠 Meta Harness 月度評估報告 — $today|date（需您審閱）`

Email includes:
- Three-team score summary table
- Full "Evolution Suggestions" section
- HITL action checklist:
  - ✅ Approve upgrade → agent executes prompt optimization
  - ❌ Defer upgrade → continue monitoring for one month
  - 🔄 Need discussion → reply in Nebula

Recipient: glen200392@gmail.com

---

## HITL Upgrade Threshold

| Score | Action |
|-------|--------|
| >= 85 | No action needed, continue monitoring |
| 70-84 | Flag for review, suggest minor prompt tuning |
| < 70  | `upgrade_needed: true` — HITL approval required |

---

## Portability Notes

| Environment | Compatibility | Notes |
|-------------|--------------|-------|
| Nebula (native) | Full | All steps run natively, HITL via email |
| LangGraph | High | Steps 3-5 as parallel evaluation nodes; Step 6 as aggregator |
| AutoGen v0.4 | High | Each team review as separate AssistantAgent; Orchestrator for Step 6 |
| CrewAI | Medium | 3 Critic Agents + 1 Synthesizer Agent |
| GitHub Actions | Medium | Steps 1-2 as HTTP actions; Steps 3-6 require LLM API integration |

**Dependencies:** Web search API, LLM API (GPT-4 class), file system write access, email delivery  
**Idempotency:** Step 7 uses date-stamped filename — safe to retry  
**HITL checkpoint:** Email approval required before any prompt modifications are applied  
**Evolution Engine:** Approved upgrades trigger Nebula agent prompt updates via manage_agents API