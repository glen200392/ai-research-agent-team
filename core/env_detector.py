"""
Environment Detection & Setup Assistant
========================================
Scans the current environment for available LLM providers and search APIs,
then prints a human-readable readiness report.
"""

import os
from pathlib import Path


def detect_and_report() -> dict:
    """Print a formatted readiness report and return the providers dict."""
    from core.providers import list_available_providers

    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        console = Console()
        _rich = True
    except ImportError:
        _rich = False

    providers = list_available_providers()
    search_keys = _check_search_apis()
    issues = _collect_issues(providers, search_keys)

    if _rich:
        _print_rich(console, providers, search_keys, issues)
    else:
        _print_plain(providers, search_keys, issues)

    return {"providers": providers, "search": search_keys, "issues": issues}


def check_minimum_viable() -> list[str]:
    """
    Return a list of blocking issues. Empty list means environment is ready to run.
    """
    from core.providers import list_available_providers
    return _collect_issues(list_available_providers(), _check_search_apis())


# ── Internal ──────────────────────────────────────────────────────────────────

def _check_search_apis() -> dict:
    keys = {}
    if os.getenv("TAVILY_API_KEY"):
        keys["tavily"] = "ready"
    if os.getenv("SERPER_API_KEY"):
        keys["serper"] = "ready"
    if os.getenv("BRAVE_SEARCH_API_KEY"):
        keys["brave"] = "ready"
    return keys


def _collect_issues(providers: dict, search_keys: dict) -> list:
    issues = []
    if not providers:
        issues.append(
            "No LLM provider detected. "
            "Set ANTHROPIC_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY, "
            "or start Ollama (ollama serve) / LM Studio."
        )
    if not search_keys:
        issues.append(
            "No search API key detected. "
            "Set TAVILY_API_KEY (recommended), SERPER_API_KEY, or BRAVE_SEARCH_API_KEY. "
            "Intel collection will be degraded without a search key."
        )
    return issues


def _print_rich(console, providers, search_keys, issues):
    from rich.table import Table
    from rich.panel import Panel

    # LLM providers table
    tbl = Table(title="LLM Providers", show_header=True, header_style="bold cyan")
    tbl.add_column("Provider")
    tbl.add_column("Status")
    tbl.add_column("Details")
    for name, info in providers.items():
        status = info.get("status", "?")
        details = (
            info.get("model")
            or (f"{len(info.get('models',[]))} models @ {info.get('host','')}" if "models" in info else "")
            or info.get("url", "")
        )
        color = "green" if status == "ready" else "yellow"
        tbl.add_row(name, f"[{color}]{status}[/{color}]", details)

    if not providers:
        tbl.add_row("[red]none detected[/red]", "", "")

    console.print(tbl)

    # Search APIs
    search_status = ", ".join(search_keys.keys()) if search_keys else "[red]none[/red]"
    console.print(f"\nSearch APIs: {search_status}")

    # Issues
    if issues:
        for issue in issues:
            console.print(f"[red]⚠  {issue}[/red]")
    else:
        console.print("\n[bold green]✓ Environment ready[/bold green]")


def _print_plain(providers, search_keys, issues):
    print("=== LLM Providers ===")
    for name, info in providers.items():
        print(f"  {name}: {info.get('status', '?')}")
    if not providers:
        print("  (none detected)")

    print(f"\nSearch APIs: {list(search_keys.keys()) or 'none'}")

    if issues:
        for issue in issues:
            print(f"ISSUE: {issue}")
    else:
        print("\nEnvironment ready.")
