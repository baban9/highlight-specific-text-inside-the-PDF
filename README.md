# PDF Text Search and Annotation (`pdfmark`)

Installable Python package for searching PDF documents and applying highlights, underlines, redactions, frames, or removing existing annotations.

## Install

```bash
pip install pymupdf
pip install git+https://github.com/baban9/highlight-specific-text-inside-the-PDF.git
```

Local development:

```bash
git clone https://github.com/baban9/highlight-specific-text-inside-the-PDF.git
cd highlight-specific-text-inside-the-PDF
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI

Annotate one file:

```bash
pdfmark annotate input.pdf output.pdf --search "Invoice" --action Highlight
pdfmark annotate input.pdf output.pdf --search "SSN" --action Redact --pages 0 2
pdfmark annotate input.pdf output.pdf --search "" --action Remove
```

Batch process a folder:

```bash
pdfmark batch ./input_pdfs ./output_pdfs --search "CONFIDENTIAL" --action Redact
```

Inspect metadata:

```bash
pdfmark info input.pdf
```

### Supported actions

| Action | Description |
|--------|-------------|
| `Highlight` | Yellow highlight (default) |
| `Squiggly` | Squiggly underline |
| `Underline` | Straight underline |
| `Strikeout` | Strikethrough |
| `Redact` | Black out matched text |
| `Frame` | Red bounding box |
| `Remove` | Delete all annotations on selected pages |

## Python API

```python
from pdfmark import PDFAnnotator, annotate_pdf, batch_annotate
from pdfmark.models import Action

result = annotate_pdf(
    input_file="input.pdf",
    output_file="output.pdf",
    pattern=r"ABC123",
    action=Action.HIGHLIGHT,
)
print(result.matches)

annotator = PDFAnnotator(pattern=r"invoice", action=Action.UNDERLINE)
annotator.annotate("input.pdf", "underlined.pdf")

results = batch_annotate("input_dir/", "output_dir/", pattern=r"secret", action=Action.REDACT)
```

## Project layout

```
src/pdfmark/          Package source
  annotator.py        Core annotation engine
  cli.py              pdfmark command-line tool
  models.py           Action enum and ProcessResult
  search.py           Regex search helpers
examples/             Usage samples
tests/                Pytest suite
utils.py              Legacy import shim
```

## Development

```bash
make setup
make test
make build
```

## Requirements

- Python 3.9+
- PyMuPDF

## License

MIT
