"""Tests for pdfmark search utilities."""

from pdfmark.models import Action
from pdfmark.search import search_for_text


def test_search_for_text_finds_case_insensitive_match():
    lines = ["Invoice Number: ABC123", "Total due: 500"]
    matches = list(search_for_text(lines, r"abc\d+"))
    assert matches == ["ABC123"]


def test_action_enum_values():
    assert Action.HIGHLIGHT.value == "Highlight"
    assert Action.REDACT.value == "Redact"
    assert "Remove" in Action.choices()


def test_action_from_value_is_case_insensitive():
    assert Action.from_value("highlight") == Action.HIGHLIGHT
    assert Action.from_value("REDACT") == Action.REDACT
