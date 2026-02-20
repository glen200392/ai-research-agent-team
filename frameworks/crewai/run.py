"""
CrewAI Runner — Entry point for the research pipeline.
Usage: python -m frameworks.crewai.run --month 2026-02
"""
import argparse
import os
from dotenv import load_dotenv
import yaml
from rich.console import Console
from rich.panel import Panel
from crewai import Crew, Process
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from .agents import build_agents
from .tasks import build_tasks

load_dotenv()
console = Console()


def get_llm(config: dict):
    provider = config.get("llm", {}).get("provider", "anthropic")
    if provider == "openai":
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.3)
    return ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5"), temperature=0.3)


def main():
    parser = argparse.ArgumentParser(description="AI Research Agent Team — CrewAI Runner")
    parser.add_argument("--month", default="auto")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    target_month = args.month if args.month != "auto" else config["report"]["target_month"]

    console.print(Panel.fit(
        "[bold cyan]AI Research Agent Team[/bold cyan]\n[dim]CrewAI Runner[/dim]",
        border_style="cyan"
    ))
    console.print(f"[yellow]Target month: {target_month}[/yellow]")

    llm = get_llm(config)
    agents = build_agents(llm)
    tasks = build_tasks(agents, target_month)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    console.print("\n[bold green]Pipeline Complete![/bold green]")
    console.print(str(result))


if __name__ == "__main__":
    main()
