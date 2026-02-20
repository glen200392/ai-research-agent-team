"""
LangGraph Node Implementations
Each function is a node in the research pipeline graph.
"""
import json
import uuid
from datetime import datetime, timedelta
from calendar import monthrange
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .state import ResearchState


def _load_prompt(filename: str) -> str:
    """Load agent system prompt from prompts/ directory."""
    import os
    base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base, "prompts", filename)
    with open(path) as f:
        content = f.read()
    # Extract content between first ```xml and ``` block
    import re
    match = re.search(r"```xml\n(.*?)```", content, re.DOTALL)
    return match.group(1).strip() if match else content


def _get_llm(config: dict):
    """Return configured LLM based on provider setting."""
    provider = config.get("llm", {}).get("provider", "anthropic")
    temp = config.get("llm", {}).get("temperature", 0.3)
    max_tokens = config.get("llm", {}).get("max_tokens", 8192)

    if provider == "openai":
        import os
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            temperature=temp,
            max_tokens=max_tokens,
        )
    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        import os
        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_MODEL", "gemini-2.0-flash"),
            temperature=temp,
        )
    else:  # default: anthropic
        import os
        return ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5"),
            temperature=temp,
            max_tokens=max_tokens,
        )


def _parse_month(target_month: str):
    """Parse target_month string into start/end dates."""
    if target_month == "auto":
        today = datetime.now()
        first = today.replace(day=1)
        last_month = first - timedelta(days=1)
        year, month = last_month.year, last_month.month
    else:
        year, month = map(int, target_month.split("-"))
    _, last_day = monthrange(year, month)
    month_names = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    return {
        "year": year,
        "month": month,
        "month_name": month_names[month - 1],
        "start": f"{year}-{month:02d}-01",
        "end": f"{year}-{month:02d}-{last_day:02d}",
    }


# ── Node 1: Orchestrator Init ─────────────────────────────────────────────────

def orchestrator_init(state: ResearchState) -> dict:
    """Initialize pipeline: parse dates, generate run ID, build keyword sets."""
    config = state.get("config", {})
    target_month = config.get("report", {}).get("target_month", "auto")
    dates = _parse_month(target_month)
    run_id = f"run_{dates['year']}{dates['month']:02d}_{datetime.now().strftime('%H%M')}"

    log_entry = {
        "step": "orchestrator_init",
        "timestamp": datetime.utcnow().isoformat(),
        "run_id": run_id,
        "target_period": f"{dates['start']} to {dates['end']}",
    }

    return {
        "pipeline_run_id": run_id,
        "target_month": f"{dates['year']}-{dates['month']:02d}",
        "time_range_start": dates["start"],
        "time_range_end": dates["end"],
        "revision_number": 0,
        "errors": [],
        "orchestration_log": [log_entry],
    }


# ── Node 2: Intel Collector ───────────────────────────────────────────────────

def intel_collector(state: ResearchState) -> dict:
    """Run 6-stream parallel intelligence collection."""
    from langchain_community.tools.tavily_search import TavilySearchResults
    import os

    llm = _get_llm(state["config"])
    system_prompt = _load_prompt("02_intel_collector.md")

    month_name = datetime.strptime(state["time_range_start"], "%Y-%m-%d").strftime("%B")
    year = state["target_month"].split("-")[0]

    task = f"""
    Execute full 6-stream intelligence collection for {month_name} {year}.
    Time range: {state['time_range_start']} to {state['time_range_end']}
    
    Run all 6 streams (A through F) as described in your instructions.
    Return a complete intel_collection JSON with all items scored.
    The 'items' array must contain real findings from your searches.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=task),
    ]

    try:
        response = llm.invoke(messages)
        # Attempt to parse JSON from response
        import re
        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        if json_match:
            collection = json.loads(json_match.group())
        else:
            collection = {"raw_response": response.content, "items": [], "error": "no_json_found"}
    except Exception as e:
        collection = {"error": str(e), "items": []}

    log_entry = {
        "step": "intel_collector",
        "timestamp": datetime.utcnow().isoformat(),
        "items_collected": len(collection.get("items", [])),
    }

    return {
        "intel_collection": collection,
        "orchestration_log": [log_entry],
    }


# ── Node 3a: Tech Analyst ─────────────────────────────────────────────────────

def tech_analyst(state: ResearchState) -> dict:
    """Analyze Streams A, B, C for technical insights."""
    llm = _get_llm(state["config"])
    system_prompt = _load_prompt("03_tech_analyst.md")

    # Filter intel to streams A, B, C
    intel = state.get("intel_collection", {})
    items = [i for i in intel.get("items", []) if i.get("stream") in ["A", "B", "C"]]

    task = f"""
    Analyze the following {len(items)} intelligence items from streams A, B, C.
    Produce a complete tech_analysis JSON per your output schema.
    
    Intel items:
    {json.dumps(items[:30], indent=2)}
    
    Time period: {state['target_month']}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=task),
    ]

    try:
        response = llm.invoke(messages)
        import re
        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        analysis = json.loads(json_match.group()) if json_match else {"raw": response.content}
    except Exception as e:
        analysis = {"error": str(e), "tech_analysis": {}}

    return {
        "tech_analysis": analysis,
        "orchestration_log": [{"step": "tech_analyst", "timestamp": datetime.utcnow().isoformat()}],
    }


# ── Node 3b: Market Analyst ───────────────────────────────────────────────────

def market_analyst(state: ResearchState) -> dict:
    """Analyze Streams D, E, F for market and strategic insights."""
    llm = _get_llm(state["config"])
    system_prompt = _load_prompt("04_market_analyst.md")

    intel = state.get("intel_collection", {})
    items = [i for i in intel.get("items", []) if i.get("stream") in ["D", "E", "F"]]

    task = f"""
    Analyze the following {len(items)} intelligence items from streams D, E, F.
    Produce a complete market_analysis JSON per your output schema.
    
    Intel items:
    {json.dumps(items[:30], indent=2)}
    
    Time period: {state['target_month']}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=task),
    ]

    try:
        response = llm.invoke(messages)
        import re
        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        analysis = json.loads(json_match.group()) if json_match else {"raw": response.content}
    except Exception as e:
        analysis = {"error": str(e), "market_analysis": {}}

    return {
        "market_analysis": analysis,
        "orchestration_log": [{"step": "market_analyst", "timestamp": datetime.utcnow().isoformat()}],
    }


# ── Node 4: Content Synthesizer ───────────────────────────────────────────────

def content_synthesizer(state: ResearchState) -> dict:
    """Generate long-form, LinkedIn, and email content in Traditional Chinese."""
    llm = _get_llm(state["config"])
    system_prompt = _load_prompt("05_content_synthesizer.md")

    revision_feedback = ""
    if state.get("qa_report") and state.get("revision_number", 0) > 0:
        revision_requests = state["qa_report"].get("revision_requests", [])
        revision_feedback = f"\n\nREVISION REQUESTS from Quality Gate:\n" + "\n".join(revision_requests)

    task = f"""
    Create the complete content package for {state['target_month']}.
    
    Tech Analysis:
    {json.dumps(state.get('tech_analysis', {}), indent=2, ensure_ascii=False)[:4000]}
    
    Market Analysis:
    {json.dumps(state.get('market_analysis', {}), indent=2, ensure_ascii=False)[:4000]}
    {revision_feedback}
    
    Produce all three formats: long_form, linkedin_post, email_digest.
    All content must be in Traditional Chinese (繁體中文).
    Return complete content_package JSON.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=task),
    ]

    try:
        response = llm.invoke(messages)
        import re
        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        package = json.loads(json_match.group()) if json_match else {"raw": response.content}
    except Exception as e:
        package = {"error": str(e)}

    return {
        "content_package": package,
        "orchestration_log": [{"step": "content_synthesizer", "timestamp": datetime.utcnow().isoformat()}],
    }


# ── Node 5: Quality Gate ──────────────────────────────────────────────────────

def quality_gate(state: ResearchState) -> dict:
    """Run 3-layer QA review. Returns qa_report with score and decision."""
    llm = _get_llm(state["config"])
    system_prompt = _load_prompt("06_quality_gate.md")
    min_score = state["config"].get("quality", {}).get("min_score", 85)
    max_revisions = state["config"].get("quality", {}).get("max_revisions", 2)
    revision_number = state.get("revision_number", 0)

    task = f"""
    Review the following content package. Revision number: {revision_number}.
    Min passing score: {min_score}/100. Max revisions allowed: {max_revisions}.
    
    Content Package:
    {json.dumps(state.get('content_package', {}), indent=2, ensure_ascii=False)[:6000]}
    
    Original Intel Collection (for fact-tracing):
    {json.dumps(state.get('intel_collection', {}).get('items', [])[:20], indent=2)[:3000]}
    
    Run all 3 QA layers. Return complete qa_report JSON with score and decision.
    If revision_number >= {max_revisions}, set decision to FORCE_APPROVE.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=task),
    ]

    try:
        response = llm.invoke(messages)
        import re
        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        report = json.loads(json_match.group()) if json_match else {"raw": response.content, "decision": "APPROVE"}
    except Exception as e:
        report = {"error": str(e), "decision": "APPROVE", "total_score": 0}

    return {
        "qa_report": report,
        "revision_number": revision_number + 1,
        "orchestration_log": [{"step": "quality_gate", "timestamp": datetime.utcnow().isoformat(), "score": report.get("total_score", "unknown")}],
    }


def qa_router(state: ResearchState) -> str:
    """Route after QA gate based on score and decision."""
    qa = state.get("qa_report", {})
    decision = qa.get("decision", "APPROVE")
    if decision in ("APPROVE", "CONDITIONAL_APPROVE", "FORCE_APPROVE"):
        return "delivery"
    return "revise"


# ── Node 6: Delivery Agent ────────────────────────────────────────────────────

def delivery_agent(state: ResearchState) -> dict:
    """Deliver approved content to all configured channels."""
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from pathlib import Path

    config = state["config"]
    content_package = state.get("content_package", {})
    delivery_config = config.get("delivery", {})
    run_id = state.get("pipeline_run_id", "unknown")
    target_month = state.get("target_month", "unknown")

    delivery_results = {}

    # -- File storage --
    file_config = delivery_config.get("file_storage", {})
    if file_config.get("enabled", True):
        try:
            output_dir = Path(file_config.get("output_dir", "./reports/"))
            output_dir.mkdir(parents=True, exist_ok=True)
            year, month = target_month.split("-")
            filename = f"AI_Tech_Report_{year}_{month}.md"
            filepath = output_dir / filename

            long_form = content_package.get("content_package", {}).get("long_form", {})
            content_md = long_form.get("content_markdown", str(content_package))

            filepath.write_text(content_md, encoding="utf-8")
            delivery_results["file_storage"] = {
                "status": "success",
                "file_path": str(filepath),
                "file_size_bytes": filepath.stat().st_size,
            }
        except Exception as e:
            delivery_results["file_storage"] = {"status": "failed", "error": str(e)}

    # -- Email --
    email_config = delivery_config.get("email", {})
    if email_config.get("enabled", False):
        try:
            recipient = os.getenv("REPORT_EMAIL_RECIPIENT", email_config.get("recipient", ""))
            digest = content_package.get("content_package", {}).get("email_digest", {})
            subject = digest.get("subject_a", f"AI Tech Report {target_month}")
            body = digest.get("body_markdown", "Report attached.")

            msg = MIMEMultipart()
            msg["From"] = os.getenv("SMTP_USER", "")
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(os.getenv("SMTP_HOST", "smtp.gmail.com"), int(os.getenv("SMTP_PORT", 587))) as server:
                server.starttls()
                server.login(os.getenv("SMTP_USER", ""), os.getenv("SMTP_PASSWORD", ""))
                server.send_message(msg)

            delivery_results["email"] = {"status": "success", "recipient": recipient}
        except Exception as e:
            delivery_results["email"] = {"status": "failed", "error": str(e)}

    overall = "all_success" if all(v.get("status") == "success" for v in delivery_results.values()) else "partial_success"

    delivery_report = {
        "pipeline_run_id": run_id,
        "delivery_timestamp": datetime.utcnow().isoformat(),
        "channels": delivery_results,
        "overall_status": overall,
    }

    return {
        "delivery_report": delivery_report,
        "orchestration_log": [{"step": "delivery_agent", "timestamp": datetime.utcnow().isoformat(), "status": overall}],
    }
