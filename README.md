# PDF Text Search and Annotation

Production-style utility for searching PDF documents and applying highlights, underlines, redactions, or bounding boxes using PyMuPDF.

## Problem

Manually finding and marking sensitive or important text in large PDF corpora is slow and error-prone.

## Approach

1. Extract page text line by line
2. Match user-supplied regex patterns (case insensitive)
3. Apply annotation action per match: Highlight, Squiggly, Underline, Strikeout, Redact, Frame, or Remove

Core logic lives in `utils.py` with a CLI for batch processing.

## Repository structure

```
utils.py                              Reusable PDF processing library
highlight textual values in PDF.ipynb Interactive exploration
requirements.txt                      Dependencies
```

## Reproducibility

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make setup
```

CLI:

```bash
python utils.py input.pdf output.pdf --search "PATTERN" --action Highlight
python utils.py input.pdf output.pdf --search "invoice" --action Redact --pages 0 2
```

Run tests:

```bash
make test
```

## Tech stack

Python 3, PyMuPDF (fitz)

## Limitations and next steps

- Add batch mode for directory of PDFs
- Support password-protected PDFs with explicit unlock flow
- Publish as installable package with pytest coverage per action type
