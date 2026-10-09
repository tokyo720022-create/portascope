# PortaScope

**Find cross-platform project portability risks before they break somewhere else.**

PortaScope is an offline-first portability auditor for project folders and source trees. It identifies selected filename and path risks before you move a project between Windows, Linux, and macOS.

> **Status: early implementation.** The scanner, initial filename rules, and Markdown/JSON CLI reports are implemented in this starter. Fix previews, applying fixes, metadata checks, archive scanning, and source-code analysis remain planned work.

## Principles

- **Read-only scanning:** the scanner never renames, writes, or deletes files in the scanned tree.
- **Offline-first:** core scans run locally and make no network requests.
- **Target-aware:** select an explicit destination profile.
- **Explainable:** findings include a rule ID, severity, path, reason, and recommendation.
- **Safe fixes:** fixes are planned for v1, but scanning itself will remain read-only. Any future apply operation must be separate, explicit, confirmed, and revalidated.
- **No AI in v1:** checks use deterministic rules.

## Current checks

- Case-insensitive path collisions for case-insensitive target profiles
- Windows reserved device names, including names with extensions
- Windows-invalid filename characters
- Windows filenames ending in spaces or dots
- A conservative Windows relative-path length warning

The profiles model common behaviours, not every filesystem configuration. macOS volumes may be case-sensitive or case-insensitive. The 260-character Windows threshold is an advisory warning and is not a guarantee that a path will fail.

## Requirements

Python 3.11 or newer.

## Install for development

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -e ".[dev]"
pytest
```

## Usage

Scan a project for risks when targeting Windows:

```bash
portascope scan ./my-project --target windows
```

Produce JSON for tools or scripts:

```bash
portascope scan ./my-project --target linux --format json
```

Supported target profiles are `windows`, `linux`, and `macos`. Output formats are `markdown` (the default) and `json`. The command returns exit code `1` when error-severity findings exist, `0` when no errors are found, and `2` when scanning fails.

## Repository layout

```text
src/portascope/       CLI, scanner, target profiles, and rules
 tests/               Automated tests using temporary synthetic projects
 docs/                 Architecture and rule specifications
```

## Roadmap

- [x] Define initial findings and target-profile models
- [x] Implement read-only path scanning without following symlinks
- [x] Add initial filename and path rules
- [x] Add Markdown and JSON CLI reports
- [x] Add automated tests for the first scanning slice
- [ ] Add fix suggestions and a preview/diff workflow
- [ ] Add a separate, confirmed apply-fixes workflow with revalidation
- [ ] Add metadata checks for symlinks and executable permissions
- [ ] Inspect supported archives without extracting them
- [ ] Add opt-in source-code checks and CI integration

## Limitations

A clean report does not guarantee an application will run on another operating system. Runtime behaviour can depend on environment, dependencies, configuration, filesystem settings, and transfer tools. Findings are advisory where destination behaviour depends on configuration.

## License

See [LICENSE](LICENSE). PortaScope uses a custom permission-required license; it is source-available and is not presented as an OSI-approved open-source project.

## Contact

- Email: [lisabp720@gmail.com](mailto:lisabp720@gmail.com)
- Discord username: `orewatokyo720_47200`
- Discord profile link: to be added

For permission requests, describe the intended use and whether you plan to modify or redistribute the project.

---

**PortaScope — portability problems, spotted before the move.**
