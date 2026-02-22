"""
Unit tests for _extract_json() — the JSON extraction utility shared by all node files.
No API calls needed.
"""
import pytest
from frameworks.langgraph.nodes import _extract_json


def test_extracts_json_code_block():
    text = 'Here is the result:\n```json\n{"key": "value"}\n```\n'
    assert _extract_json(text) == {"key": "value"}


def test_extracts_bare_json():
    text = 'Some prefix text {"foo": 42} some suffix text'
    result = _extract_json(text)
    assert result == {"foo": 42}


def test_returns_none_on_no_json():
    assert _extract_json("no json here at all") is None


def test_handles_nested_braces():
    text = '{"outer": {"inner": "value"}}'
    result = _extract_json(text)
    assert result is not None
    assert result["outer"]["inner"] == "value"


def test_handles_string_containing_braces():
    text = '{"message": "use {curly} braces"}'
    result = _extract_json(text)
    assert result is not None
    assert result["message"] == "use {curly} braces"


def test_prefers_json_code_block_over_bare():
    # If both a code block and bare JSON are present, code block wins
    text = '{"bare": true}\n```json\n{"block": true}\n```'
    result = _extract_json(text)
    assert result == {"block": True}


def test_returns_none_on_empty_string():
    assert _extract_json("") is None


def test_handles_json_with_array_values():
    text = '```json\n{"items": [1, 2, 3]}\n```'
    result = _extract_json(text)
    assert result is not None
    assert result["items"] == [1, 2, 3]
