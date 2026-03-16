"""Command-line interface for pst-converter."""

from __future__ import annotations

import argparse
from pathlib import Path

from .converter import ConversionError, convert_pst


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pst-converter", description="PST conversion helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser("convert", help="Convert a PST file")
    convert_parser.add_argument("source", type=Path, help="Path to .pst file")
    convert_parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for extracted content",
    )
    convert_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print command without executing readpst",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "convert":
        try:
            result = convert_pst(args.source, args.output_dir, dry_run=args.dry_run)
        except ConversionError as err:
            parser.exit(status=2, message=f"Error: {err}\n")

        mode = "[dry-run]" if result.dry_run else "[done]"
        print(f"{mode} command: {' '.join(result.command)}")
        print(f"source: {result.source}")
        print(f"output: {result.output_dir}")
        return 0

    parser.exit(status=2, message="Unknown command\n")


if __name__ == "__main__":
    raise SystemExit(main())
