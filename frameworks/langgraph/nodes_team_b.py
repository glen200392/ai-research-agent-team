"""
LangGraph Node Implementations — Team B: Evolution Chronicle
Agents: Archaeology Agent → Evolution Linker → Chronicle Writer (file I/O)
"""
import json
import uuid
from datetime import datetime
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from .state_team_b import EvolutionState
from .nodes import _load_prompt, _extract_json   # reuse shared helpers


def _get_llm_b(config: dict, agent_name: str):
    """Use the universal provider factory."""
    from core.providers import get_llm
    return get_llm(config, agent_name=agent_name)


def _load_evolution_graph() -> dict:
    base = Path(__file__).parent.parent.parent
    graph_path = base / "docs" / "evolution-chronicle" / "evolution-graph.json"
    if graph_path.exists():
        with open(graph_path, encoding="utf-8") as f:
            return json.load(f)
    return {"nodes": [], "edges": []}


def _find_latest_report() -> tuple[str, str]:
    """Return (path, content) of the most recently modified Team A report."""
    base = Path(__file__).parent.parent.parent
    reports_dir = base / "reports"
    reports = sorted(reports_dir.glob("AI_Tech_Report_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not reports:
        return "", ""
    path = reports[0]
    return str(path), path.read_text(encoding="utf-8")


# ── Node 0: Initialise Team B pipeline ───────────────────────────────────────

def team_b_init(state: EvolutionState) -> dict:
    """Load source report and evolution graph into state."""
    run_id = f"teamb_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Load report
    report_path = state.get("source_report_path", "")
    if report_path and Path(report_path).exists():
        report_content = Path(report_path).read_text(encoding="utf-8")
    else:
        report_path, report_content = _find_latest_report()

    # Load evolution graph
    evolution_graph = _load_evolution_graph()

    log_entry = {
        "step": "team_b_init",
        "timestamp": datetime.utcnow().isoformat(),
        "run_id": run_id,
        "report": report_path,
        "graph_nodes": len(evolution_graph.get("nodes", [])),
    }

    return {
        "pipeline_run_id": run_id,
        "source_report_path": report_path,
        "source_report_content": report_content,
        "evolution_graph": evolution_graph,
        "errors": [],
        "orchestration_log": [log_entry],
    }


# ── Node 1: Archaeology Agent ─────────────────────────────────────────────────

def archaeology_agent(state: EvolutionState) -> dict:
    """Trace the historical origins of AI technologies found in the report."""
    llm = _get_llm_b(state["config"], "archaeology_agent")
    system_prompt = _load_prompt("team_b/08_archaeology_agent.md")

    graph_summary = json.dumps({
        "node_count": len(state["evolution_graph"].get("nodes", [])),
        "existing_ids": [n["id"] for n in state["evolution_graph"].get("nodes", [])],
    })

    task = f"""
    Analyse this monthly AI research report and trace the evolution of all key technologies.

    EXISTING EVOLUTION GRAPH SUMMARY:
    {graph_summary}

    FULL GRAPH (for reference):
    {json.dumps(state["evolution_graph"], indent=2, ensure_ascii=False)[:4000]}

    MONTHLY REPORT TO ANALYSE:
    {state["source_report_content"][:6000]}

    Produce archaeology_result JSON following your output schema.
    Mark each technology as already_in_graph: true/false based on the existing_ids list.
    Propose new_edges_proposed for any lineage connections not yet in the graph.
    """

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=task)]

    try:
        response = llm.invoke(messages)
        parsed = _extract_json(response.content)
        results = parsed if parsed else {"raw": response.content, "technologies_found": [], "new_edges_proposed": []}
    except Exception as e:
        results = {"error": str(e), "technologies_found": [], "new_edges_proposed": []}

    log_entry = {
        "step": "archaeology_agent",
        "timestamp": datetime.utcnow().isoformat(),
        "technologies_found": len(results.get("archaeology_result", results).get("technologies_found", [])),
    }

    return {
        "archaeology_results": results,
        "orchestration_log": [log_entry],
    }


# ── Node 2: Evolution Linker ──────────────────────────────────────────────────

def evolution_linker(state: EvolutionState) -> dict:
    """Turn archaeology findings into graph updates and chronicle markdown."""
    llm = _get_llm_b(state["config"], "evolution_linker")
    system_prompt = _load_prompt("team_b/09_evolution_linker.md")

    task = f"""
    Transform these archaeology findings into structured graph updates and chronicle entries.

    ARCHAEOLOGY RESULTS:
    {json.dumps(state.get("archaeology_results", {}), indent=2, ensure_ascii=False)[:5000]}

    CURRENT EVOLUTION GRAPH:
    {json.dumps(state["evolution_graph"], indent=2, ensure_ascii=False)[:3000]}

    Produce chronicle_updates JSON following your output schema.
    - Add new graph nodes for technologies not yet in the graph
    - Add new edges for newly discovered lineage connections
    - Write chronicle markdown entries in Traditional Chinese
    - Include a by-period entry for this month
    """

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=task)]

    try:
        response = llm.invoke(messages)
        parsed = _extract_json(response.content)
        updates = parsed if parsed else {"raw": response.content, "chronicle_updates": {}}
    except Exception as e:
        updates = {"error": str(e), "chronicle_updates": {}}

    log_entry = {
        "step": "evolution_linker",
        "timestamp": datetime.utcnow().isoformat(),
    }

    return {
        "chronicle_updates": updates,
        "orchestration_log": [log_entry],
    }


# ── Node 3: Chronicle Writer (file I/O) ───────────────────────────────────────

def chronicle_writer(state: EvolutionState) -> dict:
    """Write all chronicle updates to the filesystem."""
    base = Path(__file__).parent.parent.parent
    chronicle_dir = base / "docs" / "evolution-chronicle"
    graph_path = chronicle_dir / "evolution-graph.json"
    period_dir = chronicle_dir / "by-period"
    tech_dir = chronicle_dir / "by-technology"

    period_dir.mkdir(parents=True, exist_ok=True)
    tech_dir.mkdir(parents=True, exist_ok=True)

    updates_wrapper = state.get("chronicle_updates", {})
    updates = updates_wrapper.get("chronicle_updates", updates_wrapper)

    files_written = []

    try:
        # 1. Update evolution-graph.json
        graph = state["evolution_graph"].copy()
        existing_ids = {n["id"] for n in graph.get("nodes", [])}

        for node in updates.get("graph_nodes_add", []):
            if node.get("id") and node["id"] not in existing_ids:
                graph.setdefault("nodes", []).append(node)
                existing_ids.add(node["id"])

        for patch in updates.get("graph_nodes_update", []):
            for existing_node in graph.get("nodes", []):
                if existing_node.get("id") == patch.get("id"):
                    existing_node.update(patch.get("fields_to_update", {}))
                    break

        existing_edge_pairs = {
            # Existing graph uses "relation"; new edges from LLM may use "relationship"
            (e.get("from"), e.get("to"), e.get("relationship") or e.get("relation"))
            for e in graph.get("edges", [])
        }
        for edge in updates.get("graph_edges_add", []):
            # Normalise key name: accept both "relationship" and "relation" from LLM output
            rel = edge.get("relationship") or edge.get("relation")
            key = (edge.get("from"), edge.get("to"), rel)
            if key not in existing_edge_pairs:
                # Store with canonical key "relation" to match existing graph schema
                normalised = {**edge, "relation": rel}
                normalised.pop("relationship", None)
                graph.setdefault("edges", []).append(normalised)
                existing_edge_pairs.add(key)

        graph_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
        files_written.append(str(graph_path))

        # 2. Write by-technology chronicles
        for entry in updates.get("by_technology_entries", []):
            file_path = base / entry.get("file_path", "")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            content = entry.get("content_markdown", "")
            if entry.get("action") == "append" and file_path.exists():
                existing = file_path.read_text(encoding="utf-8")
                file_path.write_text(existing + "\n\n---\n\n" + content, encoding="utf-8")
            else:
                file_path.write_text(content, encoding="utf-8")
            files_written.append(str(file_path))

        # 3. Write by-period entry
        period_entry = updates.get("by_period_entry", {})
        if period_entry.get("file_path"):
            period_path = base / period_entry["file_path"]
            period_path.parent.mkdir(parents=True, exist_ok=True)
            period_path.write_text(period_entry.get("content_markdown", ""), encoding="utf-8")
            files_written.append(str(period_path))

        status = "success"
        error = None

    except Exception as e:
        status = "failed"
        error = str(e)

    log_entry = {
        "step": "chronicle_writer",
        "timestamp": datetime.utcnow().isoformat(),
        "files_written": files_written,
        "status": status,
    }

    errors = [f"chronicle_writer: {error}"] if error else []

    return {
        "errors": errors,
        "orchestration_log": [log_entry],
    }
