"""PDF search, highlight, redact, and annotation utilities."""

from __future__ import annotations

import argparse
import re
from io import BytesIO
from typing import Iterable, Optional, Sequence

import fitz


ACTIONS = ("Redact", "Frame", "Highlight", "Squiggly", "Underline", "Strikeout", "Remove")


def extract_info(input_file: str) -> tuple[bool, dict]:
    pdf_doc = fitz.open(input_file)
    output = {
        "File": input_file,
        "Encrypted": "True" if pdf_doc.is_encrypted else "False",
    }
    if not pdf_doc.is_encrypted:
        output.update(pdf_doc.metadata)
    pdf_doc.close()
    return True, output


def search_for_text(lines: Iterable[str], search_str: str) -> Iterable[str]:
    for line in lines:
        for result in re.findall(search_str, line, re.IGNORECASE):
            yield result


def redact_matching_data(page, matched_values: Iterable[str]) -> int:
    matches_found = 0
    for value in matched_values:
        matches_found += 1
        for area in page.search_for(value):
            page.add_redact_annot(area, text=" ", fill=(0, 0, 0))
    page.apply_redactions()
    return matches_found


def frame_matching_data(page, matched_values: Iterable[str]) -> int:
    matches_found = 0
    for value in matched_values:
        matches_found += 1
        for area in page.search_for(value):
            annot = page.add_rect_annot(area)
            annot.set_colors(stroke=fitz.utils.getColor("red"))
            annot.update()
    return matches_found


def highlight_matching_data(page, matched_values: Iterable[str], action: str) -> int:
    matches_found = 0
    for value in matched_values:
        matches_found += 1
        area = page.search_for(value)
        if action == "Squiggly":
            highlight = page.add_squiggly_annot(area)
        elif action == "Underline":
            highlight = page.add_underline_annot(area)
        elif action == "Strikeout":
            highlight = page.add_strikeout_annot(area)
        else:
            highlight = page.add_highlight_annot(area)
        highlight.update()
    return matches_found


def remove_highlight(input_file: str, output_file: str, pages: Optional[Sequence[str]] = None) -> int:
    pdf_doc = fitz.open(input_file)
    output_buffer = BytesIO()
    annot_found = 0

    for page_index in range(pdf_doc.page_count):
        if pages and str(page_index) not in pages:
            continue
        page = pdf_doc[page_index]
        annot = page.first_annot
        while annot:
            annot_found += 1
            page.delete_annot(annot)
            annot = annot.next

    pdf_doc.save(output_buffer)
    pdf_doc.close()
    with open(output_file, "wb") as handle:
        handle.write(output_buffer.getbuffer())
    return annot_found


def process_pdf(
    input_file: str,
    output_file: str,
    search_str: str,
    action: str = "Highlight",
    pages: Optional[Sequence[str]] = None,
) -> int:
    if action == "Remove":
        return remove_highlight(input_file, output_file, pages)

    if action not in ACTIONS:
        raise ValueError(f"Unsupported action: {action}. Choose from {ACTIONS}")

    pdf_doc = fitz.open(input_file)
    output_buffer = BytesIO()
    total_matches = 0

    for page_index in range(pdf_doc.page_count):
        if pages and str(page_index) not in pages:
            continue
        page = pdf_doc[page_index]
        page_lines = page.get_text("text").split("\n")
        matched_values = list(search_for_text(page_lines, search_str))
        if not matched_values:
            continue

        if action == "Redact":
            total_matches += redact_matching_data(page, matched_values)
        elif action == "Frame":
            total_matches += frame_matching_data(page, matched_values)
        else:
            total_matches += highlight_matching_data(page, matched_values, action)

    pdf_doc.save(output_buffer)
    pdf_doc.close()
    with open(output_file, "wb") as handle:
        handle.write(output_buffer.getbuffer())
    return total_matches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search and annotate PDF text.")
    parser.add_argument("input_file", help="Path to source PDF")
    parser.add_argument("output_file", help="Path to write annotated PDF")
    parser.add_argument("--search", required=True, help="Regex pattern to match")
    parser.add_argument(
        "--action",
        default="Highlight",
        choices=ACTIONS,
        help="Annotation action",
    )
    parser.add_argument(
        "--pages",
        nargs="*",
        help="Optional page indexes to process (0-based strings)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    matches = process_pdf(
        args.input_file,
        args.output_file,
        args.search,
        action=args.action,
        pages=args.pages,
    )
    print(f"Processed {matches} matches into {args.output_file}")


if __name__ == "__main__":
    main()
