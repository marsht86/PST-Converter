from pathlib import Path

import pytest

from pst_converter import cli
from pst_converter.converter import ConversionError, ConversionResult


def test_cli_convert_success(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path):
    def fake_convert(source: Path, output_dir: Path, dry_run: bool = False) -> ConversionResult:
        return ConversionResult(
            source=source,
            output_dir=output_dir,
            command=["readpst", "-o", str(output_dir), str(source)],
            dry_run=dry_run,
        )

    monkeypatch.setattr(cli, "convert_pst", fake_convert)

    code = cli.main(["convert", "mail.pst", "--output-dir", str(tmp_path), "--dry-run"])

    captured = capsys.readouterr()
    assert code == 0
    assert "[dry-run]" in captured.out


def test_cli_convert_error(monkeypatch: pytest.MonkeyPatch):
    def fake_convert(source: Path, output_dir: Path, dry_run: bool = False) -> ConversionResult:
        raise ConversionError("bad pst")

    monkeypatch.setattr(cli, "convert_pst", fake_convert)

    with pytest.raises(SystemExit) as err:
        cli.main(["convert", "mail.pst", "--output-dir", "out"])

    assert err.value.code == 2
