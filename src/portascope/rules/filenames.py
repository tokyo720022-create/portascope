"""Filename and relative-path portability checks."""

import re
from collections import defaultdict
from collections.abc import Iterable

from portascope.models import Finding
from portascope.targets import TargetProfile

_WINDOWS_DEVICE_BASE = re.compile(r"^(?:CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])$", re.IGNORECASE)
_WINDOWS_INVALID_CHARS = frozenset('<>:"\\|?*')


def _components(path: str) -> list[str]:
    """Split scanner-style relative paths, preserving backslashes inside POSIX names."""
    return path.split("/")


def check_case_collisions(paths: Iterable[str], target: TargetProfile) -> list[Finding]:
    """Find distinct paths that collapse to the same case-folded name on the target."""
    if target.case_sensitive:
        return []

    groups: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        groups[path.casefold()].add(path)

    findings: list[Finding] = []
    for colliding_paths in groups.values():
        ordered = tuple(sorted(colliding_paths, key=lambda item: (item.casefold(), item)))
        if len(ordered) > 1:
            findings.append(
                Finding(
                    rule_id="CASE-COLLISION-001",
                    severity="error",
                    target=target.name,
                    paths=ordered,
                    message="Distinct paths differ only by letter case on this target profile.",
                    recommendation="Rename one path so every path remains unique without relying on case.",
                )
            )
    return findings


def _is_windows_device_name(component: str) -> bool:
    # Windows reserves device names even when a conventional extension is present.
    trimmed = component.rstrip(" .")
    base = trimmed.split(".", maxsplit=1)[0]
    return bool(_WINDOWS_DEVICE_BASE.fullmatch(base))


def check_windows_component_rules(paths: Iterable[str], target: TargetProfile) -> list[Finding]:
    """Check each path component against common Windows naming constraints."""
    if not target.windows_filename_rules:
        return []

    findings: list[Finding] = []
    for path in sorted(set(paths), key=lambda item: (item.casefold(), item)):
        for component in _components(path):
            if component in {"", ".", ".."}:
                continue

            if _is_windows_device_name(component):
                findings.append(
                    Finding(
                        rule_id="WIN-NAME-001",
                        severity="error",
                        target=target.name,
                        paths=(path,),
                        message=f"Path component {component!r} uses a reserved Windows device name.",
                        recommendation="Rename the component to a non-reserved name, such as 'device-output'.",
                    )
                )

            invalid = [
                character
                for character in component
                if character in _WINDOWS_INVALID_CHARS or ord(character) < 32
            ]
            if invalid:
                rendered = ", ".join(repr(character) for character in sorted(set(invalid)))
                findings.append(
                    Finding(
                        rule_id="WIN-CHAR-001",
                        severity="error",
                        target=target.name,
                        paths=(path,),
                        message=f"Path component {component!r} contains Windows-invalid character(s): {rendered}.",
                        recommendation="Replace the invalid character(s) with letters, digits, hyphens, or underscores.",
                    )
                )

            if component.endswith((" ", ".")):
                findings.append(
                    Finding(
                        rule_id="WIN-TRAIL-001",
                        severity="warning",
                        target=target.name,
                        paths=(path,),
                        message=f"Path component {component!r} ends with a space or dot.",
                        recommendation="Remove trailing spaces and dots from the component.",
                    )
                )
    return findings


def check_path_lengths(paths: Iterable[str], target: TargetProfile) -> list[Finding]:
    """Warn when a relative path exceeds a profile's conservative length threshold."""
    if target.max_path_chars is None:
        return []

    findings: list[Finding] = []
    for path in sorted(set(paths), key=lambda item: (item.casefold(), item)):
        if len(path) > target.max_path_chars:
            findings.append(
                Finding(
                    rule_id="PATH-LENGTH-001",
                    severity="warning",
                    target=target.name,
                    paths=(path,),
                    message=(
                        f"Relative path is {len(path)} characters long, exceeding the profile's "
                        f"conservative {target.max_path_chars}-character threshold. Actual behaviour "
                        "depends on Windows configuration, APIs, and the destination filesystem."
                    ),
                    recommendation="Review directory depth and verify long-path support on the destination.",
                )
            )
    return findings


def check_filename_portability(paths: Iterable[str], target: TargetProfile) -> list[Finding]:
    """Run the initial filename rules for an explicit target profile."""
    materialized = tuple(paths)
    findings = [
        *check_case_collisions(materialized, target),
        *check_windows_component_rules(materialized, target),
        *check_path_lengths(materialized, target),
    ]
    return sorted(
        findings,
        key=lambda finding: (
            finding.rule_id,
            tuple((path.casefold(), path) for path in finding.paths),
            finding.message,
        ),
    )
