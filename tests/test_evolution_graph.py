"""
Tests that verify the evolution-graph.json file is internally consistent.
No API calls needed — purely validates the static JSON data file.
"""
import json
from pathlib import Path

import pytest

GRAPH_PATH = Path(__file__).parent.parent / "docs/evolution-chronicle/evolution-graph.json"


@pytest.fixture(scope="module")
def graph_data():
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def test_evolution_graph_file_exists():
    assert GRAPH_PATH.exists(), f"evolution-graph.json not found at {GRAPH_PATH}"


def test_evolution_graph_has_required_top_level_keys(graph_data):
    assert "nodes" in graph_data, "Missing 'nodes' key"
    assert "edges" in graph_data, "Missing 'edges' key"


def test_all_nodes_have_required_fields(graph_data):
    for node in graph_data["nodes"]:
        assert "id" in node, f"Node missing 'id': {node}"
        assert "name" in node, f"Node {node.get('id')} missing 'name'"
        assert "year" in node, f"Node {node.get('id')} missing 'year' (use integer year)"
        assert "domain" in node, f"Node {node.get('id')} missing 'domain'"
        assert "tier" in node, f"Node {node.get('id')} missing 'tier'"


def test_node_year_is_integer(graph_data):
    for node in graph_data["nodes"]:
        year = node.get("year")
        assert isinstance(year, int), (
            f"Node {node.get('id')}: 'year' must be int, got {type(year).__name__} ({year!r})"
        )


def test_all_node_ids_are_unique(graph_data):
    ids = [n["id"] for n in graph_data["nodes"]]
    assert len(ids) == len(set(ids)), "Duplicate node IDs found in evolution-graph.json"


def test_all_edge_endpoints_exist(graph_data):
    node_ids = {n["id"] for n in graph_data["nodes"]}
    for edge in graph_data["edges"]:
        assert edge.get("from") in node_ids, (
            f"Edge 'from' references unknown node: {edge.get('from')}"
        )
        assert edge.get("to") in node_ids, (
            f"Edge 'to' references unknown node: {edge.get('to')}"
        )


def test_edges_use_canonical_relation_key(graph_data):
    for edge in graph_data["edges"]:
        assert "relation" in edge, (
            f"Edge {edge.get('from')} → {edge.get('to')} missing 'relation' key "
            f"(use 'relation', not 'relationship')"
        )
