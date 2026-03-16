"""Conversion orchestration around the readpst CLI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess


class ConversionError(RuntimeError):
    """Raised when PST conversion cannot proceed."""


@dataclass(frozen=True)
class ConversionResult:
    """Result metadata for a conversion operation."""

    source: Path
    output_dir: Path
    command: list[str]
    dry_run: bool


def convert_pst(source: Path, output_dir: Path, dry_run: bool = False) -> ConversionResult:
    """Convert a PST file using readpst into the provided output directory."""
    source = source.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()

    if source.suffix.lower() != ".pst":
        raise ConversionError(f"Expected a .pst file, got: {source}")

    if not source.exists():
        raise ConversionError(f"Source PST does not exist: {source}")

    readpst_path = shutil.which("readpst")
    if readpst_path is None:
        raise ConversionError("readpst is not installed or not in PATH")

    output_dir.mkdir(parents=True, exist_ok=True)

    command = [readpst_path, "-o", str(output_dir), "-D", "-M", str(source)]

    if not dry_run:
        completed = subprocess.run(command, capture_output=True, text=True)
        if completed.returncode != 0:
            raise ConversionError(
                f"readpst failed with exit code {completed.returncode}: {completed.stderr.strip()}"
            )

    return ConversionResult(
        source=source,
        output_dir=output_dir,
        command=command,
        dry_run=dry_run,
    )
