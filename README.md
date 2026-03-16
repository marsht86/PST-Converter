# PST Converter

A Python-first baseline for converting Microsoft Outlook PST archives into structured outputs.

## Approach

This scaffold uses a two-step conversion strategy:

1. Extraction: call the `readpst` command-line tool (from `libpst`) to extract mailbox content.
2. Post-processing: Python code to validate inputs, orchestrate extraction, and write metadata about the run.

## Requirements

- Python 3.11+
- `readpst` available in `PATH`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Convert a PST

```bash
pst-converter convert samples/archive.pst --output-dir out/
```

### Dry run

```bash
pst-converter convert samples/archive.pst --output-dir out/ --dry-run
```

## Run tests

```bash
python -m pytest
```

## Notes

- This scaffold intentionally focuses on orchestration and testability.
- Real PST conversion quality depends on `readpst` and any future post-processing logic.
