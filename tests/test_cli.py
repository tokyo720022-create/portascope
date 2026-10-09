import json
from pathlib import Path

from portascope.cli import main


def test_cli_emits_json_report(capsys, tmp_path: Path) -> None:
    (tmp_path / "CON.txt").write_text("placeholder", encoding="utf-8")
    exit_code = main(["scan", str(tmp_path), "--target", "windows", "--format", "json"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert output["target"] == "windows"
    assert any(item["rule_id"] == "WIN-NAME-001" for item in output["findings"])


def test_cli_reports_clean_project_in_markdown(capsys, tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    exit_code = main(["scan", str(tmp_path), "--target", "linux"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "No findings" in output
