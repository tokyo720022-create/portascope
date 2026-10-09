"""Coordinate a read-only scan and deterministic portability rules."""

from portascope.models import Finding
from portascope.rules.filenames import check_filename_portability
from portascope.scanner import PathLike, scan_relative_paths
from portascope.targets import TargetProfile, get_target_profile


def analyze_directory(root: PathLike, target: str | TargetProfile) -> tuple[list[str], list[Finding]]:
    """Scan a directory and analyze its relative paths without changing it."""
    profile = get_target_profile(target) if isinstance(target, str) else target
    paths = scan_relative_paths(root)
    return paths, check_filename_portability(paths, profile)
