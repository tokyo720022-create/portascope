# Initial Architecture

## Goals

A small, offline-first Python CLI that scans a directory, evaluates target-platform rules, and emits explainable findings without modifying the inspected files.

## Pipeline

1. **CLI** parses the source path, target profile, output format, and optional fix-preview request.
2. **Scanner** walks the tree without following symlinks by default and records relative paths and relevant metadata.
3. **Rule engine** runs deterministic checks against explicit target profiles.
4. **Finding model** normalizes rule ID, severity, paths, target, explanation, and remediation.
5. **Reporter** writes Markdown or JSON to stdout or a user-selected destination outside the scanned tree by default.
6. **Fix planner** proposes a preview/diff only. A future apply command must be separate, opt-in, and guarded by confirmation.

## Proposed package layout

```text
src/portascope/
  __init__.py
  cli.py
  scanner.py
  models.py
  targets.py
  engine.py
  rules/
    __init__.py
    filenames.py
    paths.py
    metadata.py
  reporters/
    __init__.py
    markdown.py
    json_report.py
  fixes/
    __init__.py
    planner.py
```

Only create modules when the corresponding milestone starts; avoid empty placeholder modules that suggest unimplemented functionality exists.

## Dependencies

Keep runtime dependencies at zero initially. Use pytest and Ruff as development-only tools.

## Non-goals for v1

- AI analysis
- Cloud scanning or telemetry
- Automatic modifications during scanning
- Guaranteeing exact behaviour of every filesystem or sync tool
- Running code from the scanned project
