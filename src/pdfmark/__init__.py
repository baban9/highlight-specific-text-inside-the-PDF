"""Search and annotate text inside PDF documents."""

from pdfmark.annotator import PDFAnnotator, annotate_pdf, batch_annotate
from pdfmark.models import Action, ProcessResult
from pdfmark.search import extract_info, search_for_text

__all__ = [
    "Action",
    "PDFAnnotator",
    "ProcessResult",
    "annotate_pdf",
    "batch_annotate",
    "extract_info",
    "search_for_text",
]
__version__ = "1.0.0"
