"""
CrewAI Agent Definitions
All 7 agents with their roles, goals, and tool assignments.
"""
import os
from pathlib import Path
from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool


def _load_prompt(filename: str) -> str:
    base = Path(__file__).parent.parent.parent
    path = base / "prompts" / filename
    import re
    content = path.read_text()
    match = re.search(r"```xml\n(.*?)```", content, re.DOTALL)
    return match.group(1).strip() if match else content


def build_agents(llm):
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

    research_orchestrator = Agent(
        role="Research Orchestrator",
        goal="Coordinate the AI research pipeline to produce a comprehensive monthly report",
        backstory=_load_prompt("01_research_orchestrator.md")[:2000],
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )

    intel_collector = Agent(
        role="Intel Collector",
        goal="Gather comprehensive raw intelligence from 6 parallel search streams",
        backstory=_load_prompt("02_intel_collector.md")[:2000],
        verbose=True,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm,
    )

    tech_analyst = Agent(
        role="Tech Analyst",
        goal="Produce rigorous technical analysis of AI model releases and innovations",
        backstory=_load_prompt("03_tech_analyst.md")[:2000],
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm,
    )

    market_analyst = Agent(
        role="Market Analyst",
        goal="Analyze competitive dynamics, funding flows, and industry structure",
        backstory=_load_prompt("04_market_analyst.md")[:2000],
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm,
    )

    content_synthesizer = Agent(
        role="Content Synthesizer",
        goal="Transform analysis into compelling Traditional Chinese content in 3 formats",
        backstory=_load_prompt("05_content_synthesizer.md")[:2000],
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    quality_gate = Agent(
        role="Quality Gate Reviewer",
        goal="Ensure factual accuracy, structural completeness, and editorial quality",
        backstory=_load_prompt("06_quality_gate.md")[:2000],
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm,
    )

    delivery_agent = Agent(
        role="Delivery Agent",
        goal="Deliver the approved report to all configured channels without modification",
        backstory=_load_prompt("07_delivery_agent.md")[:2000],
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    return {
        "orchestrator": research_orchestrator,
        "intel": intel_collector,
        "tech": tech_analyst,
        "market": market_analyst,
        "content": content_synthesizer,
        "qa": quality_gate,
        "delivery": delivery_agent,
    }
