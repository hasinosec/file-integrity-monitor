"""Tests for the SHA-256 file-integrity monitor."""

from __future__ import annotations

from pathlib import Path

from file_integrity_monitor import check_baseline, create_baseline, scan, sha256


def _write(directory: Path, name: str, content: str) -> Path:
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_sha256_matches_known_value(tmp_path):
    path = _write(tmp_path, "a.txt", "hello")
    # SHA-256 of "hello"
    assert sha256(path) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_scan_includes_nested_files_and_skips_baseline(tmp_path):
    _write(tmp_path, "top.txt", "1")
    _write(tmp_path, "sub/deep.txt", "2")
    _write(tmp_path, "baseline.json", "{}")
    result = scan(tmp_path)
    assert set(result) == {"top.txt", str(Path("sub/deep.txt"))}


def test_clean_check_reports_no_changes(tmp_path, capsys):
    _write(tmp_path, "config.txt", "environment=production")
    baseline = tmp_path / "baseline.json"
    create_baseline(tmp_path, baseline)
    check_baseline(tmp_path, baseline)
    assert "OK: no file-integrity changes detected." in capsys.readouterr().out


def test_modified_file_is_flagged_high(tmp_path, capsys):
    target = _write(tmp_path, "config.txt", "admin_access=restricted")
    baseline = tmp_path / "baseline.json"
    create_baseline(tmp_path, baseline)
    target.write_text("admin_access=everyone", encoding="utf-8")
    check_baseline(tmp_path, baseline)
    out = capsys.readouterr().out
    assert "ALERT [HIGH] Modified file: config.txt" in out
    assert "1 integrity change(s) detected." in out


def test_new_and_deleted_files_are_flagged(tmp_path, capsys):
    _write(tmp_path, "keep.txt", "a")
    removed = _write(tmp_path, "gone.txt", "b")
    baseline = tmp_path / "baseline.json"
    create_baseline(tmp_path, baseline)
    removed.unlink()
    _write(tmp_path, "added.txt", "c")
    check_baseline(tmp_path, baseline)
    out = capsys.readouterr().out
    assert "ALERT [HIGH] Deleted file: gone.txt" in out
    assert "ALERT [MEDIUM] New file: added.txt" in out
    assert "2 integrity change(s) detected." in out


def test_check_without_baseline_returns_error_code(tmp_path, capsys):
    _write(tmp_path, "x.txt", "x")
    rc = check_baseline(tmp_path, tmp_path / "missing.json")
    assert rc == 1
    assert "No baseline found." in capsys.readouterr().out
