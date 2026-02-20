"""
CrewAI Task Definitions
Sequential task pipeline with context dependencies.
"""
from crewai import Task


def build_tasks(agents: dict, target_month: str) -> list:
    collection_task = Task(
        description=f"""
        Execute complete 6-stream intelligence collection for {target_month}.
        Run all streams A through F as specified in your instructions.
        Return structured intel_collection JSON with all items scored.
        Each item must have: id, stream, title, url, date_published, key_claims, composite_score.
        """,
        expected_output="Complete intel_collection JSON with items from all 6 streams",
        agent=agents["intel"],
    )

    tech_task = Task(
        description=f"""
        Analyze intelligence from Streams A, B, C for {target_month}.
        Focus on: model architecture innovations, benchmark analysis, OSS vs closed gap.
        Return complete tech_analysis JSON per output schema.
        """,
        expected_output="tech_analysis JSON with model releases, capability gap assessment, technical narrative",
        agent=agents["tech"],
        context=[collection_task],
    )

    market_task = Task(
        description=f"""
        Analyze intelligence from Streams D, E, F for {target_month}.
        Focus on: hardware landscape, cross-domain breakthroughs, funding, regulation.
        Return complete market_analysis JSON per output schema.
        """,
        expected_output="market_analysis JSON with hardware landscape, investment activity, competitive dynamics",
        agent=agents["market"],
        context=[collection_task],
    )

    synthesis_task = Task(
        description=f"""
        Create complete content package for {target_month} in Traditional Chinese (繁體中文).
        Produce all 3 formats: long_form (2000-3000 words), linkedin_post (600-900), email_digest (400-500).
        Use the tech_analysis and market_analysis from previous tasks.
        """,
        expected_output="content_package JSON with long_form, linkedin_post, and email_digest in Traditional Chinese",
        agent=agents["content"],
        context=[tech_task, market_task],
    )

    qa_task = Task(
        description=f"""
        Review the content package from the synthesis task.
        Run all 3 QA layers: factual accuracy (40pts), structural completeness (30pts), editorial quality (30pts).
        Return qa_report JSON with total score, decision, and specific revision_requests if needed.
        """,
        expected_output="qa_report JSON with score 0-100, APPROVE/CONDITIONAL_APPROVE/REJECT decision",
        agent=agents["qa"],
        context=[synthesis_task, collection_task],
    )

    delivery_task = Task(
        description=f"""
        Deliver the approved content to all configured channels.
        Save long_form to ./reports/AI_Tech_Report_{target_month.replace('-', '_')}.md
        Send email digest if SMTP is configured.
        Return delivery_report JSON confirming all channel statuses.
        """,
        expected_output="delivery_report JSON with status for each delivery channel",
        agent=agents["delivery"],
        context=[synthesis_task, qa_task],
    )

    return [collection_task, tech_task, market_task, synthesis_task, qa_task, delivery_task]
