# Monthly AI Tech Research Report — Nebula Recipe

## Overview
Automated monthly AI technology intelligence report using Nebula's native agent system.
Import this TASK.md directly into Nebula to create the automation.

## Trigger
- Type: cron
- Schedule: 0 8 1 * * (1st of every month at 08:00)
- Timezone: Asia/Taipei

## Steps

### Step 1: Intelligence Collection
- Agent: ai-research-advisor
- Task: Search for AI technology developments from the previous month across 6 streams:
  Stream A: arXiv papers (cs.AI, cs.CL, cs.LG)
  Stream B: Major lab announcements (OpenAI, Anthropic, Google DeepMind, Meta, Mistral)
  Stream C: Open-source ecosystem (HuggingFace, GitHub, Chinese models)
  Stream D: Hardware & infrastructure (NVIDIA, AMD, cloud providers)
  Stream E: Cross-domain breakthroughs (medical, scientific, robotics, video)
  Stream F: Industry & business (funding, M&A, regulation)
  
  For each stream, run 3-5 searches and collect the top results.
  Score each item: Relevance + Credibility + Freshness (max 30).
  Return structured collection with all scored items.

### Step 2: Technical Analysis
- Agent: ai-research-advisor
- Depends on: Step 1
- Task: Analyze Streams A, B, C from the intel collection.
  Identify: model releases, architecture innovations, benchmark improvements, OSS vs closed gap.
  Produce tech_analysis with: model_releases, capability_gap_assessment, technical_narrative.

### Step 3: Market Analysis
- Agent: market-research-analyst
- Depends on: Step 1 (runs in parallel with Step 2)
- Task: Analyze Streams D, E, F from the intel collection.
  Identify: hardware landscape shifts, cross-domain breakthroughs, funding flows, regulatory changes.
  Produce market_analysis with: hardware_landscape, investment_activity, competitive_dynamics, 6_month_outlook.

### Step 4: Content Synthesis
- Agent: presentation-content-strategist
- Depends on: Step 2, Step 3
- Task: Generate complete content package in Traditional Chinese (繁體中文).
  Produce 3 formats:
  1. Long-form report (2000-3000 words, 6 chapters)
  2. LinkedIn post (600-900 words)
  3. Email digest (400-500 words) with 2 subject line variants
  All content must be accurate, sourced, and written to professional standard.

### Step 5: Quality Review
- Agent: qa-testing-specialist
- Depends on: Step 4
- Task: Review content package with 3-layer QA:
  Layer 1 (40pts): Factual accuracy — trace all numbers to sources
  Layer 2 (30pts): Structural completeness — all 6 chapters present
  Layer 3 (30pts): Editorial quality — readability, attribution, consistency
  Score >= 85: Approve. Score 75-84: Request specific revisions. Score < 75: Reject.
  Return qa_report with score, decision, and revision_requests.

### Step 6: Delivery
- Agent: nebula (orchestrator)
- Depends on: Step 5
- Task: If QA approved, deliver the report:
  1. Save long_form to docs/AI_Tech_Report_{YYYY}_{MM}.md
  2. Send email digest to configured recipient
  3. Post summary to #ai-development channel
  Return delivery confirmation for all channels.

## Configuration
Edit these values before activating:
- Email recipient: set REPORT_EMAIL_RECIPIENT in environment
- Min QA score: 85 (adjust in Step 5 task description)
- Output directory: docs/ (adjust in Step 6 task description)
