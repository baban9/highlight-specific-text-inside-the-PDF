"""Legacy import compatibility."""

from utils import ACTIONS, process_pdf, search_for_text


def test_legacy_utils_exports():
    assert "Highlight" in ACTIONS


def test_legacy_search_helper():
    lines = ["Invoice Number: ABC123"]
    assert list(search_for_text(lines, r"abc\d+")) == ["ABC123"]


def test_legacy_process_pdf_signature(sample_pdf, tmp_path):
    output_pdf = tmp_path / "legacy.pdf"
    result = process_pdf(
        str(sample_pdf),
        str(output_pdf),
        search_str=r"ABC123",
        action="Highlight",
    )
    assert result.matches == 1
    assert output_pdf.exists()
