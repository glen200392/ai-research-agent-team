"""
LangGraph Runner — Entry point for the research pipeline.
Usage: python -m frameworks.langgraph.run --month 2026-02
"""
import argparse
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import yaml
from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()


def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="AI Research Agent Team — LangGraph Runner")
    parser.add_argument("--month", default="auto", help="Target month (e.g. 2026-02) or 'auto' for last month")
    parser.add_argument("--config", default="config/config.yaml", help="Config file path")
    parser.add_argument("--dry-run", action="store_true", help="Validate config only, don't execute")
    args = parser.parse_args()

    console.print(Panel.fit(
        "[bold cyan]AI Research Agent Team[/bold cyan]\n"
        "[dim]LangGraph Pipeline Runner[/dim]",
        border_style="cyan"
    ))

    # Validate --month format before loading anything else
    import re as _re
    if args.month != "auto" and not _re.fullmatch(r"\d{4}-\d{2}", args.month):
        console.print(
            f"[red]Error: Invalid --month value '{args.month}'. "
            "Use 'YYYY-MM' (e.g. '2026-02') or 'auto'.[/red]"
        )
        sys.exit(1)

    # Load config
    config = load_config(args.config)
    if args.month != "auto":
        config["report"]["target_month"] = args.month

    if args.dry_run:
        console.print("[green]Config loaded successfully. Dry run complete.[/green]")
        console.print(json.dumps(config, indent=2))
        return

    # Build and run graph
    from .graph import build_research_graph

    console.print(f"[yellow]Starting pipeline for: {config['report']['target_month']}[/yellow]")

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

    # Print summary
    console.print("\n[bold green]Pipeline Complete![/bold green]")
    console.print(f"Run ID: {result.get('pipeline_run_id')}")
    console.print(f"QA Score: {result.get('qa_report', {}).get('total_score', 'N/A')}")
    console.print(f"Delivery: {result.get('delivery_report', {}).get('overall_status', 'N/A')}")

    if result.get("delivery_report", {}).get("channels", {}).get("file_storage", {}).get("file_path"):
        path = result["delivery_report"]["channels"]["file_storage"]["file_path"]
        console.print(f"Report saved: [cyan]{path}[/cyan]")


if __name__ == "__main__":
    main()
