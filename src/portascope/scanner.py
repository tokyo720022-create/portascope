"""Read-only directory traversal that never follows symlinks."""

import os
from pathlib import Path
from typing import TypeAlias

PathLike: TypeAlias = str | os.PathLike[str]


class ScanError(OSError):
    """Raised when a directory cannot be inspected safely."""


def scan_relative_paths(root: PathLike) -> list[str]:
    """Return all entries below *root* as sorted, relative POSIX paths.

    The scanner reads directory entries only; it does not open file contents, write to the
    scanned tree, or follow symlinks. Directories are included as well as files so that
    directory-name conflicts can be detected.
    """
    try:
        root_path = Path(root).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ScanError(f"Cannot resolve scan root {root!r}: {exc}") from exc

    if not root_path.is_dir():
        raise ScanError(f"Scan root is not a directory: {root_path}")

    found: list[str] = []
    pending = [root_path]

    while pending:
        current = pending.pop()
        try:
            with os.scandir(current) as iterator:
                entries = sorted(iterator, key=lambda entry: (entry.name.casefold(), entry.name))
        except OSError as exc:
            raise ScanError(f"Cannot inspect directory {current}: {exc}") from exc

        for entry in entries:
            entry_path = Path(entry.path)
            relative_path = entry_path.relative_to(root_path).as_posix()
            found.append(relative_path)
            try:
                if entry.is_dir(follow_symlinks=False):
                    pending.append(entry_path)
            except OSError as exc:
                raise ScanError(f"Cannot inspect entry {entry_path}: {exc}") from exc

    return sorted(found, key=lambda item: (item.casefold(), item))
