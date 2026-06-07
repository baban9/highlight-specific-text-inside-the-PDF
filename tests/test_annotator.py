"""Integration tests for pdfmark annotation."""

from pathlib import Path

import fitz

from pdfmark import PDFAnnotator, annotate_pdf
from pdfmark.models import Action


def test_annotate_pdf_highlights_matches(sample_pdf: Path, tmp_path: Path):
    output_pdf = tmp_path / "highlighted.pdf"
    result = annotate_pdf(
        input_file=sample_pdf,
        output_file=output_pdf,
        pattern=r"ABC123",
        action=Action.HIGHLIGHT,
    )

    assert output_pdf.exists()
    assert result.matches == 1
    assert result.pages_processed == 1

    doc = fitz.open(output_pdf)
    assert doc[0].first_annot is not None
    doc.close()


def test_pdf_annotator_class(sample_pdf: Path, tmp_path: Path):
    output_pdf = tmp_path / "framed.pdf"
    annotator = PDFAnnotator(pattern=r"XYZ\d+", action=Action.FRAME)
    result = annotator.annotate(sample_pdf, output_pdf)

    assert result.matches == 1
    assert output_pdf.exists()


def test_batch_annotate_processes_directory(sample_pdf: Path, tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    target = input_dir / "copy.pdf"
    target.write_bytes(sample_pdf.read_bytes())

    from pdfmark import batch_annotate

    results = batch_annotate(
        input_dir=input_dir,
        output_dir=output_dir,
        pattern=r"Invoice",
        action=Action.UNDERLINE,
    )

    assert len(results) == 1
    assert (output_dir / "copy.pdf").exists()


def test_remove_annotations(sample_pdf: Path, tmp_path: Path):
    highlighted = tmp_path / "marked.pdf"
    annotate_pdf(sample_pdf, highlighted, pattern=r"ABC123", action=Action.HIGHLIGHT)

    cleaned = tmp_path / "clean.pdf"
    result = annotate_pdf(highlighted, cleaned, pattern="", action=Action.REMOVE)

    doc = fitz.open(cleaned)
    assert doc[0].first_annot is None
    doc.close()
    assert result.action == Action.REMOVE
