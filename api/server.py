"""
AI Research Agent Team — REST API Server
=========================================
Exposes all three team pipelines over HTTP.

Usage:
  uvicorn api.server:app --host 0.0.0.0 --port 8080
  uvicorn api.server:app --host 0.0.0.0 --port 8080 --reload   # dev mode

API Endpoints:
  GET  /                       → welcome + docs link
  GET  /health                 → system health + available providers
  GET  /providers              → list available LLM providers
  POST /pipeline/team-a        → run Team A (monthly report)
  POST /pipeline/team-b        → run Team B (evolution chronicle)
  POST /pipeline/team-c        → run Team C (pedagogy lesson)
  POST /pipeline/all           → run all three teams in sequence
  GET  /pipeline/{run_id}      → check job status / result
  GET  /reports                → list generated reports
  GET  /reports/{filename}     → download a specific report
  GET  /lessons                → list generated pedagogy lessons
"""

import asyncio
import datetime
import os
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="AI Research Agent Team",
    description="Automated AI intelligence system with three specialized agent teams.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_BASE = Path(__file__).parent.parent
_executor = ThreadPoolExecutor(max_workers=2)  # Limit concurrent pipeline runs
JOB_TIMEOUT_SECONDS = int(os.getenv("JOB_TIMEOUT_SECONDS", "3600"))  # 1 hour default

# ── In-memory job store ───────────────────────────────────────────────────────
# { run_id: { status, team, started_at, completed_at, result, error } }
_jobs: dict = {}


def _load_config() -> dict:
    with open(_BASE / "config" / "config.yaml") as f:
        return yaml.safe_load(f)


# ── Request/Response schemas ──────────────────────────────────────────────────

class TeamARequest(BaseModel):
    month: str = "auto"
    config_overrides: dict = {}


class TeamBRequest(BaseModel):
    report_path: str = ""
    config_overrides: dict = {}


class TeamCRequest(BaseModel):
    report_path: str = ""
    evolution_context: str = ""
    config_overrides: dict = {}


class AllTeamsRequest(BaseModel):
    month: str = "auto"
    config_overrides: dict = {}


# ── Job execution helpers ─────────────────────────────────────────────────────

def _run_in_thread(run_id: str, team: str, fn, *args):
    """Execute a pipeline function in the thread pool and track the result."""
    _jobs[run_id] = {
        "run_id": run_id,
        "team": team,
        "status": "running",
        "started_at": datetime.datetime.utcnow().isoformat(),
        "completed_at": None,
        "result": None,
        "error": None,
    }

    def _task():
        try:
            result = fn(*args)
            _jobs[run_id]["status"] = "completed"
            _jobs[run_id]["result"] = _summarize_result(result, team)
        except Exception as e:
            _jobs[run_id]["status"] = "failed"
            _jobs[run_id]["error"] = str(e)
        finally:
            _jobs[run_id]["completed_at"] = datetime.datetime.utcnow().isoformat()

    future = _executor.submit(_task)

    def _watchdog():
        try:
            future.result(timeout=JOB_TIMEOUT_SECONDS)
        except FuturesTimeoutError:
            if _jobs[run_id]["status"] == "running":
                _jobs[run_id]["status"] = "timeout"
                _jobs[run_id]["error"] = f"Job exceeded {JOB_TIMEOUT_SECONDS}s timeout"
                _jobs[run_id]["completed_at"] = datetime.datetime.utcnow().isoformat()
        except Exception:
            pass  # Already handled in _task

    threading.Thread(target=_watchdog, daemon=True).start()
    return {"run_id": run_id, "status": "running", "team": team}


def _summarize_result(result: dict, team: str) -> dict:
    """Extract the key output fields from a pipeline result."""
    if team == "team-a":
        return {
            "pipeline_run_id": result.get("pipeline_run_id"),
            "qa_score": result.get("qa_report", {}).get("total_score"),
            "delivery_status": result.get("delivery_report", {}).get("overall_status"),
            "report_path": (
                result.get("delivery_report", {})
                      .get("channels", {})
                      .get("file_storage", {})
                      .get("file_path")
            ),
            "errors": result.get("errors", []),
        }
    if team == "team-b":
        logs = result.get("orchestration_log", [])
        last = logs[-1] if logs else {}
        return {
            "pipeline_run_id": result.get("pipeline_run_id"),
            "files_written": last.get("files_written", []),
            "errors": result.get("errors", []),
        }
    if team == "team-c":
        return {
            "pipeline_run_id": result.get("pipeline_run_id"),
            "lesson_file_path": result.get("lesson_file_path"),
            "errors": result.get("errors", []),
        }
    return result


def _exec_team_a(month: str, config_overrides: dict) -> dict:
    from frameworks.langgraph.graph import build_research_graph

    cfg = _load_config()
    cfg.update(config_overrides)
    if month != "auto":
        cfg["report"]["target_month"] = month

    graph = build_research_graph()
    return graph.invoke({
        "pipeline_run_id": "",
        "target_month": cfg["report"]["target_month"],
        "time_range_start": "",
        "time_range_end": "",
        "config": cfg,
        "intel_collection": None,
        "tech_analysis": None,
        "market_analysis": None,
        "content_package": None,
        "qa_report": None,
        "revision_number": 0,
        "delivery_report": None,
        "errors": [],
        "orchestration_log": [],
    })


def _exec_team_b(report_path: str, config_overrides: dict) -> dict:
    from frameworks.langgraph.graph_team_b import build_team_b_graph

    cfg = _load_config()
    cfg.update(config_overrides)
    graph = build_team_b_graph()
    return graph.invoke({
        "pipeline_run_id": "",
        "config": cfg,
        "source_report_path": report_path,
        "source_report_content": "",
        "evolution_graph": {},
        "archaeology_results": None,
        "chronicle_updates": None,
        "errors": [],
        "orchestration_log": [],
    })


def _exec_team_c(report_path: str, evolution_context: str, config_overrides: dict) -> dict:
    from frameworks.langgraph.graph_team_c import build_team_c_graph

    cfg = _load_config()
    cfg.update(config_overrides)
    graph = build_team_c_graph()
    return graph.invoke({
        "pipeline_run_id": "",
        "config": cfg,
        "source_report_path": report_path,
        "source_report_content": "",
        "evolution_context": evolution_context,
        "lesson_content": None,
        "quiz_content": None,
        "lesson_file_path": None,
        "errors": [],
        "orchestration_log": [],
    })


def _exec_all(month: str, config_overrides: dict) -> dict:
    a = _exec_team_a(month, config_overrides)
    report_path = (
        a.get("delivery_report", {})
         .get("channels", {})
         .get("file_storage", {})
         .get("file_path", "")
    )
    b = _exec_team_b(report_path, config_overrides)
    c = _exec_team_c(report_path, "", config_overrides)
    return {"team_a": _summarize_result(a, "team-a"),
            "team_b": _summarize_result(b, "team-b"),
            "team_c": _summarize_result(c, "team-c")}


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
def root():
    return {
        "service": "AI Research Agent Team",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", summary="System health + provider status")
def health():
    from core.providers import list_available_providers

    running = sum(1 for j in _jobs.values() if j["status"] == "running")
    return {
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "active_jobs": running,
        "providers": list_available_providers(),
    }


@app.get("/providers", summary="List available LLM providers")
def providers():
    from core.providers import list_available_providers
    return {"available": list_available_providers()}


@app.post("/pipeline/team-a", summary="Run Team A: monthly AI research report")
def run_team_a(req: TeamARequest):
    run_id = f"a-{uuid.uuid4().hex[:8]}"
    return _run_in_thread(run_id, "team-a", _exec_team_a, req.month, req.config_overrides)


@app.post("/pipeline/team-b", summary="Run Team B: evolution chronicle update")
def run_team_b(req: TeamBRequest):
    run_id = f"b-{uuid.uuid4().hex[:8]}"
    return _run_in_thread(run_id, "team-b", _exec_team_b, req.report_path, req.config_overrides)


@app.post("/pipeline/team-c", summary="Run Team C: pedagogy lesson generation")
def run_team_c(req: TeamCRequest):
    run_id = f"c-{uuid.uuid4().hex[:8]}"
    return _run_in_thread(run_id, "team-c", _exec_team_c,
                          req.report_path, req.evolution_context, req.config_overrides)


@app.post("/pipeline/all", summary="Run all three teams in sequence (A → B → C)")
def run_all(req: AllTeamsRequest):
    run_id = f"all-{uuid.uuid4().hex[:8]}"
    return _run_in_thread(run_id, "all", _exec_all, req.month, req.config_overrides)


@app.get("/pipeline/{run_id}", summary="Check job status")
def job_status(run_id: str):
    if run_id not in _jobs:
        raise HTTPException(status_code=404, detail=f"Job '{run_id}' not found")
    return _jobs[run_id]


@app.get("/pipeline", summary="List all jobs")
def list_jobs():
    return {"jobs": list(_jobs.values())}


@app.get("/reports", summary="List generated Team A reports")
def list_reports():
    reports_dir = _BASE / "reports"
    reports = []
    for f in sorted(reports_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        stat = f.stat()
        reports.append({
            "filename": f.name,
            "size_bytes": stat.st_size,
            "created_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "url": f"/reports/{f.name}",
        })
    return {"reports": reports, "count": len(reports)}


@app.get("/reports/{filename}", summary="Download a specific report")
def get_report(filename: str):
    # Prevent path traversal
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    path = _BASE / "reports" / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Report '{filename}' not found")
    return FileResponse(path, media_type="text/markdown", filename=filename)


@app.get("/lessons", summary="List generated Team C lessons")
def list_lessons():
    lessons_dir = _BASE / "pedagogy" / "weekly-lessons"
    lessons = []
    for d in sorted(lessons_dir.iterdir(), reverse=True):
        if d.is_dir():
            lesson_file = d / "complete-lesson.md"
            if lesson_file.exists():
                stat = lesson_file.stat()
                lessons.append({
                    "date": d.name,
                    "file": "complete-lesson.md",
                    "size_bytes": stat.st_size,
                    "url": f"/lessons/{d.name}",
                })
    return {"lessons": lessons, "count": len(lessons)}


@app.get("/lessons/{date}", summary="Download a specific lesson")
def get_lesson(date: str):
    if ".." in date or "/" in date:
        raise HTTPException(status_code=400, detail="Invalid date")
    path = _BASE / "pedagogy" / "weekly-lessons" / date / "complete-lesson.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Lesson for '{date}' not found")
    return FileResponse(path, media_type="text/markdown", filename=f"lesson-{date}.md")


@app.get("/evolution", summary="Return the current evolution graph JSON")
def get_evolution_graph():
    import json
    path = _BASE / "docs" / "evolution-chronicle" / "evolution-graph.json"
    if not path.exists():
        return {"nodes": [], "edges": []}
    with open(path) as f:
        return json.load(f)
