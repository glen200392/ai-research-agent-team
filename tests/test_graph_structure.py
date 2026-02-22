"""
Tests that verify all three LangGraph pipelines compile correctly.
No API calls are made — graph compilation is a pure in-memory operation.
"""


def test_team_a_graph_compiles():
    from frameworks.langgraph.graph import build_research_graph
    graph = build_research_graph()
    assert graph is not None


def test_team_b_graph_compiles():
    from frameworks.langgraph.graph_team_b import build_team_b_graph
    graph = build_team_b_graph()
    assert graph is not None


def test_team_c_graph_compiles():
    from frameworks.langgraph.graph_team_c import build_team_c_graph
    graph = build_team_c_graph()
    assert graph is not None
