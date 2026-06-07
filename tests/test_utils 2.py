"""Smoke tests for PDF utilities."""

import re

from utils import search_for_text, ACTIONS


def test_search_for_text_finds_case_insensitive_match():
    lines = ["Invoice Number: ABC123", "Total due: 500"]
    matches = list(search_for_text(lines, r"abc\d+"))
    assert matches == ["ABC123"]


def test_actions_include_expected_values():
    assert "Highlight" in ACTIONS
    assert "Redact" in ACTIONS
    assert "Remove" in ACTIONS
