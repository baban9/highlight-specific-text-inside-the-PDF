"""Backward-compatible shim for legacy imports."""

from pdfmark import Action, PDFAnnotator, ProcessResult, annotate_pdf, extract_info, search_for_text
from pdfmark.models import Action as ActionEnum

ACTIONS = Action.choices()


def process_pdf(
    input_file,
    output_file,
    search_str,
    action: str = "Highlight",
    pages=None,
    password=None,
):
    """Legacy function signature kept for notebook compatibility."""
    return annotate_pdf(
        input_file=input_file,
        output_file=output_file,
        pattern=search_str,
        action=action,
        pages=pages,
        password=password,
    )


def build_parser():
    from pdfmark.cli import build_parser as _build_parser

    return _build_parser()


def main():
    from pdfmark.cli import main as _main

    raise SystemExit(_main())


__all__ = [
    "ACTIONS",
    "ActionEnum",
    "PDFAnnotator",
    "ProcessResult",
    "annotate_pdf",
    "build_parser",
    "extract_info",
    "main",
    "process_pdf",
    "search_for_text",
]
