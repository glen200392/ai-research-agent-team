"""
LangGraph Graph — Team C: Pedagogy Federation
Pipeline: init → lesson_designer → quiz_generator → lesson_packager
"""
from langgraph.graph import StateGraph, END

from .state_team_c import PedagogyState
from .nodes_team_c import (
    team_c_init,
    lesson_designer,
    quiz_generator,
    lesson_packager,
)


def build_team_c_graph():
    """Build and compile the Team C pedagogy pipeline."""
    workflow = StateGraph(PedagogyState)

    workflow.add_node("team_c_init", team_c_init)
    workflow.add_node("lesson_designer", lesson_designer)
    workflow.add_node("quiz_generator", quiz_generator)
    workflow.add_node("lesson_packager", lesson_packager)

    workflow.set_entry_point("team_c_init")
    workflow.add_edge("team_c_init", "lesson_designer")
    workflow.add_edge("lesson_designer", "quiz_generator")
    workflow.add_edge("quiz_generator", "lesson_packager")
    workflow.add_edge("lesson_packager", END)

    return workflow.compile()
