# Initial Architecture

## Implemented in this starter

- Python CLI for local scanning
- Read-only directory traversal without following symlinks
- Target profiles for Windows, Linux, and common default macOS behaviour
- Deterministic filename/path checks
- Markdown and JSON reports

## Pipeline

1. **CLI** accepts a scan root, target profile, and report format.
2. **Scanner** returns sorted relative paths without reading file contents or following symlinks.
3. **Rule engine** evaluates paths against the chosen target profile.
4. **Finding model** records rule ID, severity, affected paths, explanation, and recommendation.
5. **Reporter** produces Markdown or JSON output.
6. **Fix planner** will propose a preview; a future apply command must be separate, explicit, confirmed, and revalidated.

## Proposed package layout

```text
src/portascope/
  cli.py
  engine.py
  models.py
  scanner.py
  targets.py
  rules/filenames.py
```

## Dependencies

Zero runtime dependencies. Pytest and Ruff are development-only tools.

## Non-goals for the initial slice

- AI analysis
- Network access, cloud scans, or telemetry
- Modifying scanned files during scanning
- Guaranteeing the exact behaviour of every filesystem or transfer utility
- Running code from scanned projects
