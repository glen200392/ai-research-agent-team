"""
AI Research Agent Team — Universal Runner
==========================================
Single entry point for all three teams and utilities.

Usage:
  python run.py team-a [--month YYYY-MM] [--dry-run]
  python run.py team-b [--report PATH]
  python run.py team-c [--report PATH]
  python run.py all   [--month YYYY-MM]
  python run.py detect
  python run.py setup
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _console():
    try:
        from rich.console import Console
        return Console()
    except ImportError:
        class _FallbackConsole:
            def print(self, msg, **_):
                import re
                print(re.sub(r"\[/?[^\]]+\]", "", str(msg)))
        return _FallbackConsole()


def _load_config(config_path: str = "config/config.yaml") -> dict:
    import yaml
    with open(config_path) as f:
        return yaml.safe_load(f)


# ── Sub-commands ──────────────────────────────────────────────────────────────

def cmd_detect(args):
    """Print available LLM providers and search APIs."""
    from core.env_detector import detect_and_report
    detect_and_report()


def cmd_team_a(args):
    """Run Team A: monthly AI research report generation."""
    console = _console()

    # Validate --month
    if args.month != "auto" and not re.fullmatch(r"\d{4}-\d{2}", args.month):
        console.print(f"[red]Error: Invalid --month '{args.month}'. Use YYYY-MM or 'auto'.[/red]")
        sys.exit(1)

    config = _load_config(args.config)
    if args.month != "auto":
        config["report"]["target_month"] = args.month

    if args.dry_run:
        console.print("[green]Config OK — dry run complete (Team A)[/green]")
        console.print(json.dumps(config, indent=2, ensure_ascii=False))
        return

    try:
        from rich.panel import Panel
        console.print(Panel.fit(
            "[bold cyan]AI Research Agent Team — Team A[/bold cyan]\n"
            "[dim]Monthly Intelligence Report[/dim]",
            border_style="cyan"
        ))
    except Exception:
        console.print("=== Team A: Monthly Intelligence Report ===")

    from frameworks.langgraph.graph import build_research_graph

    console.print(f"[yellow]Target month: {config['report']['target_month']}[/yellow]")
    graph = build_research_graph()

    initial_state = {
        "pipeline_run_id": "",
        "target_month": config["report"]["target_month"],
        "time_range_start": "",
        "time_range_end": "",
        "config": config,
        "intel_collection": None,
        "tech_analysis": None,
        "market_analysis": None,
        "content_package": None,
        "qa_report": None,
        "revision_number": 0,
        "delivery_report": None,
        "errors": [],
        "orchestration_log": [],
    }

    result = graph.invoke(initial_state)

    console.print("\n[bold green]Team A Complete![/bold green]")
    console.print(f"Run ID:    {result.get('pipeline_run_id')}")
    console.print(f"QA Score:  {result.get('qa_report', {}).get('total_score', 'N/A')}")
    console.print(f"Delivery:  {result.get('delivery_report', {}).get('overall_status', 'N/A')}")

    if result.get("errors"):
        console.print(f"[yellow]Errors: {result['errors']}[/yellow]")

    file_path = (
        result.get("delivery_report", {})
              .get("channels", {})
              .get("file_storage", {})
              .get("file_path")
    )
    if file_path:
        console.print(f"Report: [cyan]{file_path}[/cyan]")


def cmd_team_b(args):
    """Run Team B: Evolution Chronicle update."""
    console = _console()

    try:
        from rich.panel import Panel
        console.print(Panel.fit(
            "[bold magenta]AI Research Agent Team — Team B[/bold magenta]\n"
            "[dim]Evolution Chronicle[/dim]",
            border_style="magenta"
        ))
    except Exception:
        console.print("=== Team B: Evolution Chronicle ===")

    config = _load_config(args.config)

    if args.dry_run:
        console.print("[green]Config OK — dry run complete (Team B)[/green]")
        return

    from frameworks.langgraph.graph_team_b import build_team_b_graph

    graph = build_team_b_graph()
    initial_state = {
        "pipeline_run_id": "",
        "config": config,
        "source_report_path": args.report or "",
        "source_report_content": "",
        "evolution_graph": {},
        "archaeology_results": None,
        "chronicle_updates": None,
        "errors": [],
        "orchestration_log": [],
    }

    result = graph.invoke(initial_state)

    console.print("\n[bold green]Team B Complete![/bold green]")
    console.print(f"Run ID: {result.get('pipeline_run_id')}")
    if result.get("errors"):
        console.print(f"[yellow]Errors: {result['errors']}[/yellow]")

    last_log = result.get("orchestration_log", [{}])[-1]
    files = last_log.get("files_written", [])
    if files:
        console.print(f"Files written: {len(files)}")
        for f in files:
            console.print(f"  [cyan]{f}[/cyan]")


def cmd_team_c(args):
    """Run Team C: Pedagogy Federation lesson generation."""
    console = _console()

    try:
        from rich.panel import Panel
        console.print(Panel.fit(
            "[bold yellow]AI Research Agent Team — Team C[/bold yellow]\n"
            "[dim]Pedagogy Federation[/dim]",
            border_style="yellow"
        ))
    except Exception:
        console.print("=== Team C: Pedagogy Federation ===")

    config = _load_config(args.config)

    if args.dry_run:
        console.print("[green]Config OK — dry run complete (Team C)[/green]")
        return

    from frameworks.langgraph.graph_team_c import build_team_c_graph

    graph = build_team_c_graph()
    initial_state = {
        "pipeline_run_id": "",
        "config": config,
        "source_report_path": args.report or "",
        "source_report_content": "",
        "evolution_context": "",
        "lesson_content": None,
        "quiz_content": None,
        "lesson_file_path": None,
        "errors": [],
        "orchestration_log": [],
    }

    result = graph.invoke(initial_state)

    console.print("\n[bold green]Team C Complete![/bold green]")
    console.print(f"Run ID: {result.get('pipeline_run_id')}")
    if result.get("lesson_file_path"):
        console.print(f"Lesson: [cyan]{result['lesson_file_path']}[/cyan]")
    if result.get("errors"):
        console.print(f"[yellow]Errors: {result['errors']}[/yellow]")


def cmd_all(args):
    """Run all three teams in sequence: A → B → C."""
    console = _console()
    console.print("[bold]Running all teams in sequence: A → B → C[/bold]")

    cmd_team_a(args)
    console.print("\n")
    cmd_team_b(args)
    console.print("\n")
    cmd_team_c(args)


def cmd_setup(args):
    """Interactive environment setup assistant."""
    console = _console()
    console.print("[bold cyan]AI Research Agent Team — Setup[/bold cyan]")
    console.print("")

    # Check for .env
    env_path = Path(".env")
    example_path = Path("env.example")
    if not env_path.exists() and example_path.exists():
        console.print("[yellow].env not found. Copying from env.example...[/yellow]")
        env_path.write_text(example_path.read_text())
        console.print("[green]Created .env — please edit it with your API keys.[/green]")
    elif not env_path.exists():
        console.print("[red].env not found and env.example missing. Please create .env manually.[/red]")
        sys.exit(1)

    # Check deps
    try:
        import langchain_core  # noqa
        console.print("[green]✓ Dependencies installed[/green]")
    except ImportError:
        console.print("[yellow]Installing dependencies...[/yellow]")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    # Detect providers
    console.print("")
    from core.env_detector import detect_and_report, check_minimum_viable
    detect_and_report()

    issues = check_minimum_viable()
    if issues:
        console.print("\n[bold red]Action required before running:[/bold red]")
        for issue in issues:
            console.print(f"  [red]• {issue}[/red]")
    else:
        console.print("\n[bold green]✓ Environment ready. Run: python run.py team-a[/bold green]")


# ── CLI Definition ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="AI Research Agent Team — Universal Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py team-a                          # Run Team A (last month)
  python run.py team-a --month 2026-02          # Run Team A for specific month
  python run.py team-b                          # Run Team B (uses latest report)
  python run.py team-b --report reports/AI_Tech_Report_2026_02.md
  python run.py team-c                          # Run Team C
  python run.py all --month 2026-02             # Run all teams
  python run.py detect                          # Show available providers
  python run.py setup                           # First-time setup
        """,
    )

    parser.add_argument("--config", default="config/config.yaml", help="Config file path")

    sub = parser.add_subparsers(dest="command", required=True)

    # team-a
    p_a = sub.add_parser("team-a", help="Run Team A: monthly research report")
    p_a.add_argument("--month", default="auto", help="YYYY-MM or 'auto'")
    p_a.add_argument("--dry-run", action="store_true")

    # team-b
    p_b = sub.add_parser("team-b", help="Run Team B: evolution chronicle")
    p_b.add_argument("--report", default="", help="Path to Team A report (optional, auto-detects latest)")
    p_b.add_argument("--dry-run", action="store_true")

    # team-c
    p_c = sub.add_parser("team-c", help="Run Team C: pedagogy lesson generation")
    p_c.add_argument("--report", default="", help="Path to Team A report (optional, auto-detects latest)")
    p_c.add_argument("--dry-run", action="store_true")

    # all
    p_all = sub.add_parser("all", help="Run Team A → B → C in sequence")
    p_all.add_argument("--month", default="auto", help="YYYY-MM or 'auto'")
    p_all.add_argument("--report", default="")
    p_all.add_argument("--dry-run", action="store_true")

    # detect
    sub.add_parser("detect", help="Detect available LLM providers")

    # setup
    sub.add_parser("setup", help="Interactive first-time setup")

    args = parser.parse_args()

    dispatch = {
        "team-a": cmd_team_a,
        "team-b": cmd_team_b,
        "team-c": cmd_team_c,
        "all": cmd_all,
        "detect": cmd_detect,
        "setup": cmd_setup,
    }

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
