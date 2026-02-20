"""
LangGraph Pipeline Graph Definition
Assembles all nodes into the research pipeline with parallel execution.
"""
from langgraph.graph import StateGraph, END

from .state import ResearchState
from .nodes import (
    orchestrator_init,
    intel_collector,
    tech_analyst,
    market_analyst,
    content_synthesizer,
    quality_gate,
    qa_router,
    delivery_agent,
)


def build_research_graph():
    """Build and compile the full research pipeline graph."""
    workflow = StateGraph(ResearchState)

    # Add all nodes
    workflow.add_node("orchestrator_init", orchestrator_init)
    workflow.add_node("intel_collector", intel_collector)
    workflow.add_node("tech_analyst", tech_analyst)
    workflow.add_node("market_analyst", market_analyst)
    workflow.add_node("content_synthesizer", content_synthesizer)
    workflow.add_node("quality_gate", quality_gate)
    workflow.add_node("delivery_agent", delivery_agent)

    # Entry point
    workflow.set_entry_point("orchestrator_init")

    # Linear: init -> collection
    workflow.add_edge("orchestrator_init", "intel_collector")

    # Parallel: collection -> both analysts simultaneously
    workflow.add_edge("intel_collector", "tech_analyst")
    workflow.add_edge("intel_collector", "market_analyst")

    # Join: both analysts -> synthesizer
    workflow.add_edge("tech_analyst", "content_synthesizer")
    workflow.add_edge("market_analyst", "content_synthesizer")

    # QA with conditional routing
    workflow.add_edge("content_synthesizer", "quality_gate")
    workflow.add_conditional_edges(
        "quality_gate",
        qa_router,
        {
            "delivery": "delivery_agent",
            "revise": "content_synthesizer",
        }
    )

    # Delivery -> end
    workflow.add_edge("delivery_agent", END)

    return workflow.compile()
