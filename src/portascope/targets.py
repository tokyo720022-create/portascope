"""Explicit destination-platform assumptions used by portability rules."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TargetProfile:
    name: str
    case_sensitive: bool
    windows_filename_rules: bool
    max_path_chars: int | None
    description: str


# These profiles model common defaults, not every filesystem configuration.
TARGET_PROFILES: dict[str, TargetProfile] = {
    "windows": TargetProfile(
        name="windows",
        case_sensitive=False,
        windows_filename_rules=True,
        max_path_chars=260,
        description=(
            "Windows-compatible names; 260 characters is a conservative legacy-path warning "
            "threshold, not a guarantee of failure."
        ),
    ),
    "linux": TargetProfile(
        name="linux",
        case_sensitive=True,
        windows_filename_rules=False,
        max_path_chars=None,
        description="Case-sensitive Linux-style names; filesystem behaviour can vary.",
    ),
    "macos": TargetProfile(
        name="macos",
        case_sensitive=False,
        windows_filename_rules=False,
        max_path_chars=None,
        description=(
            "Models the common case-insensitive macOS volume default; case-sensitive volumes "
            "also exist."
        ),
    ),
}


def get_target_profile(name: str) -> TargetProfile:
    """Get a target profile, raising a helpful error for unsupported names."""
    normalized = name.strip().lower()
    try:
        return TARGET_PROFILES[normalized]
    except KeyError as exc:
        supported = ", ".join(sorted(TARGET_PROFILES))
        raise ValueError(f"Unknown target {name!r}. Supported targets: {supported}.") from exc
