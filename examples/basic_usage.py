"""Basic pdfmark usage example."""

from pdfmark import PDFAnnotator, annotate_pdf
from pdfmark.models import Action


def highlight_invoice(input_pdf: str, output_pdf: str) -> None:
    result = annotate_pdf(
        input_file=input_pdf,
        output_file=output_pdf,
        pattern=r"Invoice\s+Number:\s+\w+",
        action=Action.HIGHLIGHT,
    )
    print(result)


def redact_sensitive_ids(input_pdf: str, output_pdf: str) -> None:
    annotator = PDFAnnotator(pattern=r"ID:\s+\w+", action=Action.REDACT)
    result = annotator.annotate(input_pdf, output_pdf)
    print(result)


if __name__ == "__main__":
    highlight_invoice("input.pdf", "highlighted.pdf")
    redact_sensitive_ids("input.pdf", "redacted.pdf")
