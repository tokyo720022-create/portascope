from pathlib import Path

import pytest

from portascope.scanner import ScanError, scan_relative_paths


def test_scan_returns_sorted_relative_paths_and_does_not_change_contents(tmp_path: Path) -> None:
    root = tmp_path / "project"
    nested = root / "src"
    nested.mkdir(parents=True)
    source = nested / "main.py"
    source.write_text("print('hello')\n", encoding="utf-8")
    readme = root / "README.md"
    readme.write_text("sample\n", encoding="utf-8")
    before = {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}

    result = scan_relative_paths(root)

    assert result == sorted(result, key=lambda item: (item.casefold(), item))
    assert set(result) == {"README.md", "src", "src/main.py"}
    after = {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    assert after == before


def test_scan_rejects_a_file_as_root(tmp_path: Path) -> None:
    source = tmp_path / "not-a-directory.txt"
    source.write_text("content", encoding="utf-8")
    with pytest.raises(ScanError, match="not a directory"):
        scan_relative_paths(source)


def test_scan_does_not_follow_directory_symlinks_when_supported(tmp_path: Path) -> None:
    root = tmp_path / "project"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (outside / "secret.txt").write_text("not traversed", encoding="utf-8")
    link = root / "linked-dir"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Directory symlinks are unavailable in this environment")

    result = scan_relative_paths(root)
    assert "linked-dir" in result
    assert "linked-dir/secret.txt" not in result
