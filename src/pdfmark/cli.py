"""Command-line interface for pdfmark."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pdfmark import __version__
from pdfmark.annotator import annotate_pdf, batch_annotate
from pdfmark.models import Action
from pdfmark.search import extract_info


def _build_annotate_parser(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("annotate", help="Annotate one PDF file")
    parser.add_argument("input_file", help="Source PDF path")
    parser.add_argument("output_file", help="Output PDF path")
    parser.add_argument("--search", required=True, help="Regex pattern to match")
    parser.add_argument(
        "--action",
        default=Action.HIGHLIGHT.value,
        choices=Action.choices(),
        help="Annotation action",
    )
    parser.add_argument(
        "--pages",
        nargs="*",
        type=int,
        help="Optional 0-based page indexes",
    )
    parser.add_argument("--password", help="Password for encrypted PDFs")
    return parser


def _build_batch_parser(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("batch", help="Annotate all PDFs in a folder")
    parser.add_argument("input_dir", help="Directory containing PDF files")
    parser.add_argument("output_dir", help="Directory for annotated PDFs")
    parser.add_argument("--search", required=True, help="Regex pattern to match")
    parser.add_argument(
        "--action",
        default=Action.HIGHLIGHT.value,
        choices=Action.choices(),
        help="Annotation action",
    )
    parser.add_argument("--password", help="Password for encrypted PDFs")
    return parser


def _build_info_parser(subparsers) -> argparse.ArgumentParser:
    parser = subparsers.add_parser("info", help="Show PDF metadata")
    parser.add_argument("input_file", help="Source PDF path")
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdfmark",
        description="Search and annotate text inside PDF files.",
    )
    parser.add_argument("--version", action="version", version=f"pdfmark {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    _build_annotate_parser(subparsers)
    _build_batch_parser(subparsers)
    _build_info_parser(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.command == "annotate":
            result = annotate_pdf(
                input_file=args.input_file,
                output_file=args.output_file,
                pattern=args.search,
                action=args.action,
                pages=args.pages,
                password=args.password,
            )
            print(result)
            return 0

        if args.command == "batch":
            results = batch_annotate(
                input_dir=args.input_dir,
                output_dir=args.output_dir,
                pattern=args.search,
                action=args.action,
                password=args.password,
            )
            if not results:
                print(f"No PDF files found in {Path(args.input_dir)}")
                return 1
            for result in results:
                print(result)
            return 0

        info = extract_info(args.input_file)
        for key, value in info.items():
            print(f"{key}: {value}")
        return 0
    except (FileNotFoundError, PermissionError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
