from portascope.rules.filenames import check_filename_portability
from portascope.targets import get_target_profile


def test_case_collision_is_reported_for_windows() -> None:
    findings = check_filename_portability(["Config.json", "config.json"], get_target_profile("windows"))
    assert any(finding.rule_id == "CASE-COLLISION-001" for finding in findings)


def test_case_collision_is_not_reported_for_linux() -> None:
    findings = check_filename_portability(["Config.json", "config.json"], get_target_profile("linux"))
    assert not any(finding.rule_id == "CASE-COLLISION-001" for finding in findings)


def test_windows_reserved_device_name_with_extension_is_reported() -> None:
    findings = check_filename_portability(["reports/CON.txt"], get_target_profile("windows"))
    assert any(finding.rule_id == "WIN-NAME-001" for finding in findings)


def test_similar_non_reserved_name_is_safe() -> None:
    findings = check_filename_portability(["reports/console.txt"], get_target_profile("windows"))
    assert not any(finding.rule_id == "WIN-NAME-001" for finding in findings)


def test_windows_invalid_characters_are_reported() -> None:
    findings = check_filename_portability(["report?.txt"], get_target_profile("windows"))
    assert any(finding.rule_id == "WIN-CHAR-001" for finding in findings)


def test_trailing_dot_or_space_is_reported() -> None:
    findings = check_filename_portability(["reports/final. "], get_target_profile("windows"))
    assert any(finding.rule_id == "WIN-TRAIL-001" for finding in findings)


def test_long_path_warning_is_advisory() -> None:
    path = "/".join(["a" * 80, "b" * 80, "c" * 80, "d" * 20])
    findings = check_filename_portability([path], get_target_profile("windows"))
    match = [finding for finding in findings if finding.rule_id == "PATH-LENGTH-001"]
    assert len(match) == 1
    assert match[0].severity == "warning"
    assert "depends on Windows configuration" in match[0].message


def test_windows_only_filename_rules_do_not_run_for_linux() -> None:
    findings = check_filename_portability(["invalid?.txt", "CON"], get_target_profile("linux"))
    rule_ids = {finding.rule_id for finding in findings}
    assert "WIN-CHAR-001" not in rule_ids
    assert "WIN-NAME-001" not in rule_ids
