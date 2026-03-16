from pathlib import Path

import pytest

from pst_converter.converter import ConversionError, convert_pst


def test_convert_requires_pst_extension(tmp_path: Path):
    not_pst = tmp_path / "message.txt"
    not_pst.write_text("nope", encoding="utf-8")

    with pytest.raises(ConversionError, match="Expected a .pst file"):
        convert_pst(not_pst, tmp_path / "out", dry_run=True)


def test_convert_requires_existing_file(tmp_path: Path):
    missing = tmp_path / "missing.pst"

    with pytest.raises(ConversionError, match="does not exist"):
        convert_pst(missing, tmp_path / "out", dry_run=True)


def test_convert_requires_readpst(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source = tmp_path / "archive.pst"
    source.write_text("placeholder", encoding="utf-8")

    monkeypatch.setattr("shutil.which", lambda _: None)

    with pytest.raises(ConversionError, match="readpst is not installed"):
        convert_pst(source, tmp_path / "out", dry_run=True)


def test_convert_dry_run_returns_command(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source = tmp_path / "archive.pst"
    source.write_text("placeholder", encoding="utf-8")

    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/readpst")

    result = convert_pst(source, tmp_path / "out", dry_run=True)

    assert result.dry_run is True
    assert result.command[0] == "/usr/bin/readpst"
    assert result.command[-1] == str(source.resolve())
    assert (tmp_path / "out").exists()
