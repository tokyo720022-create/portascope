# PortaScope v0.1.0 initial implementation slice

Included in this starter bundle:

- Target profiles for Windows, Linux, and common default macOS behaviour
- Read-only path scanner that includes directories and files but does not follow symlinks
- Filename rules for case collisions, Windows device names, invalid characters, trailing spaces/dots, and a conservative Windows path-length warning
- CLI output in Markdown or JSON
- Automated tests for the first scanning/rule slice

This is an early implementation. Fix suggestions and a confirmed apply-fixes workflow are planned next and are not implemented in this slice. Scanning itself is read-only and the core code makes no network requests.

## Run locally

```bash
python -m venv .venv
# Activate the environment
python -m pip install -e ".[dev]"
pytest
portascope scan /path/to/project --target windows
portascope scan /path/to/project --target linux --format json
```
