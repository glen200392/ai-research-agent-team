"""
LangGraph Graph — Team B: Evolution Chronicle
Pipeline: init → archaeology → linker → writer
"""
from langgraph.graph import StateGraph, END

from .state_team_b import EvolutionState
from .nodes_team_b import (
    team_b_init,
    archaeology_agent,
    evolution_linker,
    chronicle_writer,
)


def build_team_b_graph():
    """Build and compile the Team B evolution chronicle pipeline."""
    workflow = StateGraph(EvolutionState)

    workflow.add_node("team_b_init", team_b_init)
    workflow.add_node("archaeology_agent", archaeology_agent)
    workflow.add_node("evolution_linker", evolution_linker)
    workflow.add_node("chronicle_writer", chronicle_writer)

    workflow.set_entry_point("team_b_init")
    workflow.add_edge("team_b_init", "archaeology_agent")
    workflow.add_edge("archaeology_agent", "evolution_linker")
    workflow.add_edge("evolution_linker", "chronicle_writer")
    workflow.add_edge("chronicle_writer", END)

    return workflow.compile()
