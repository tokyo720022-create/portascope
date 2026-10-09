"""Command-line interface for the initial PortaScope scanner."""

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from portascope import __version__
from portascope.engine import analyze_directory
from portascope.models import Finding
from portascope.scanner import ScanError
from portascope.targets import TARGET_PROFILES, get_target_profile


def _markdown_report(target: str, paths: list[str], findings: list[Finding]) -> str:
    counts = {"error": 0, "warning": 0, "info": 0}
    for finding in findings:
        counts[finding.severity] += 1

    lines = [
        "# PortaScope Report",
        "",
        f"- **Version:** {__version__}",
        f"- **Target profile:** {target}",
        f"- **Scanned entries:** {len(paths)}",
        f"- **Findings:** {len(findings)} ({counts['error']} errors, {counts['warning']} warnings, {counts['info']} info)",
        "",
    ]
    if not findings:
        lines.append("No findings for the selected target profile.")
        return "\n".join(lines) + "\n"

    lines.extend(["## Findings", ""])
    for finding in findings:
        path_list = ", ".join("`" + path + "`" for path in finding.paths)
        lines.extend(
            [
                f"### [{finding.severity.upper()}] {finding.rule_id}",
                "",
                f"- **Path(s):** {path_list}",
                f"- **Issue:** {finding.message}",
                f"- **Suggested resolution:** {finding.recommendation}",
                "",
            ]
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="portascope",
        description="Offline-first, read-only cross-platform portability auditing.",
    )
    parser.add_argument("--version", action="version", version=f"PortaScope {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("scan", help="Scan a directory for portability risks")
    scan.add_argument("root", type=Path, help="Directory to inspect (read-only)")
    scan.add_argument(
        "--target",
        required=True,
        choices=sorted(TARGET_PROFILES),
        help="Destination platform profile to check",
    )
    scan.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Report format (default: markdown)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "scan":  # Defensive guard for future subcommands.
        parser.error("Unsupported command")

    try:
        profile = get_target_profile(args.target)
        paths, findings = analyze_directory(args.root, profile)
    except (ScanError, ValueError) as exc:
        print(f"portascope: error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        document = {
            "tool": "PortaScope",
            "version": __version__,
            "target": profile.name,
            "scanned_entries": len(paths),
            "findings": [finding.to_dict() for finding in findings],
        }
        print(json.dumps(document, indent=2, ensure_ascii=False))
    else:
        print(_markdown_report(profile.name, paths, findings), end="")

    return 1 if any(finding.severity == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
