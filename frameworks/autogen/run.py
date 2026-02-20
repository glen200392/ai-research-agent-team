"""
AutoGen Runner — Multi-agent group chat pipeline.
Usage: python -m frameworks.autogen.run --month 2026-02
"""
import argparse
import os
from pathlib import Path
import re
from dotenv import load_dotenv
import yaml
import autogen
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()


def _load_prompt(filename: str) -> str:
    base = Path(__file__).parent.parent.parent
    path = base / "prompts" / filename
    content = path.read_text()
    match = re.search(r"```xml\n(.*?)```", content, re.DOTALL)
    return match.group(1).strip() if match else content


def main():
    parser = argparse.ArgumentParser(description="AI Research Agent Team — AutoGen Runner")
    parser.add_argument("--month", default="auto")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    target_month = args.month if args.month != "auto" else config["report"]["target_month"]
    provider = config.get("llm", {}).get("provider", "anthropic")

    if provider == "openai":
        llm_config = {
            "config_list": [{"model": os.getenv("OPENAI_MODEL", "gpt-4o"), "api_key": os.getenv("OPENAI_API_KEY")}]
        }
    else:
        llm_config = {
            "config_list": [{"model": os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5"), "api_key": os.getenv("ANTHROPIC_API_KEY"), "api_type": "anthropic"}]
        }

    console.print(Panel.fit(
        "[bold cyan]AI Research Agent Team[/bold cyan]\n[dim]AutoGen Runner[/dim]",
        border_style="cyan"
    ))

    # Define agents
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=20,
        is_termination_msg=lambda x: "PIPELINE_COMPLETE" in (x.get("content") or ""),
        code_execution_config={"work_dir": "tmp/autogen", "use_docker": False},
    )

    orchestrator = autogen.AssistantAgent(
        name="ResearchOrchestrator",
        system_message=_load_prompt("01_research_orchestrator.md"),
        llm_config=llm_config,
    )

    intel_agent = autogen.AssistantAgent(
        name="IntelCollector",
        system_message=_load_prompt("02_intel_collector.md"),
        llm_config=llm_config,
    )

    tech_agent = autogen.AssistantAgent(
        name="TechAnalyst",
        system_message=_load_prompt("03_tech_analyst.md"),
        llm_config=llm_config,
    )

    market_agent = autogen.AssistantAgent(
        name="MarketAnalyst",
        system_message=_load_prompt("04_market_analyst.md"),
        llm_config=llm_config,
    )

    content_agent = autogen.AssistantAgent(
        name="ContentSynthesizer",
        system_message=_load_prompt("05_content_synthesizer.md"),
        llm_config=llm_config,
    )

    qa_agent = autogen.AssistantAgent(
        name="QualityGate",
        system_message=_load_prompt("06_quality_gate.md"),
        llm_config=llm_config,
    )

    delivery_agent = autogen.AssistantAgent(
        name="DeliveryAgent",
        system_message=_load_prompt("07_delivery_agent.md"),
        llm_config=llm_config,
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, orchestrator, intel_agent, tech_agent, market_agent, content_agent, qa_agent, delivery_agent],
        messages=[],
        max_round=30,
        speaker_selection_method="auto",
    )

    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Kick off
    user_proxy.initiate_chat(
        manager,
        message=f"""
        Execute the complete AI technology research pipeline for {target_month}.
        
        Pipeline steps:
        1. IntelCollector: Run 6-stream parallel search for {target_month}
        2. TechAnalyst + MarketAnalyst: Analyze results in parallel
        3. ContentSynthesizer: Generate Traditional Chinese report in 3 formats
        4. QualityGate: Review and score (min 85/100 to approve)
        5. DeliveryAgent: Save report to ./reports/ and send email if configured
        
        When complete, reply with: PIPELINE_COMPLETE
        """
    )


if __name__ == "__main__":
    main()
