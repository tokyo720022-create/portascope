# PortaScope

**Find cross-platform project portability risks before they break somewhere else.**

PortaScope is a proposed, local-first portability auditor for project folders and source trees. Its goal is to help developers identify files, paths, metadata, and selected operating-system assumptions that may behave differently across Windows, Linux, and macOS—before transferring, archiving, or publishing a project.

> **Project status: pre-alpha / design stage.** The README describes the intended direction, not features that are already implemented. The scanner, rules, command-line interface, and reports are planned work.

## Why PortaScope?

A project can work on one operating system and still run into portability problems elsewhere. Examples include:

- Two paths that differ only by letter case, such as `Config.json` and `config.json`.
- Filenames that are invalid or reserved on a target operating system.
- Paths that exceed a target environment's practical limits.
- Symlinks, executable bits, or other filesystem metadata that may not survive a transfer as expected.
- Source code that relies on operating-system-specific paths or commands.

PortaScope aims to make these risks visible in one explainable preflight report.

## Design goals

- **Read-only by default:** inspect files without renaming, deleting, or rewriting them.
- **Target-aware:** evaluate a project against a selected destination profile rather than only the host machine.
- **Explainable findings:** show the affected path, target platform, severity, reason, and suggested next step.
- **Local-first:** make core scans possible without uploading project contents to a server.
- **Machine-readable output:** support structured reports for later automation and CI workflows.
- **Testable rules:** use small fixtures and regression tests for each portability rule.

## Planned capabilities

The following are roadmap items; they are not implemented yet.

### First milestone

- Scan a chosen directory.
- Provide initial target profiles for Windows, Linux, and macOS.
- Detect selected filename collisions and invalid or reserved names.
- Flag configurable path-length risks.
- Report selected metadata concerns, such as symlinks and executable permissions.
- Export a readable Markdown report and structured JSON.
- Include sample projects and automated tests for every rule.

### Later milestones

- Inspect supported archives without extracting them to disk.
- Add opt-in source-code checks for selected platform-specific assumptions.
- Add configurable severity levels, exclusions, and project-specific rules.
- Integrate with CI systems, including GitHub Actions.
- Offer an optional HTML report and baseline comparison between scans.

## Example report (illustrative only)

The following is an example of the kind of finding PortaScope is intended to produce. It is not output from a working scanner.

```text
Target: Windows

[WARNING] Potential case-insensitive path collision
  Path A: src/Config.json
  Path B: src/config.json
  Why: These names may refer to the same path on a case-insensitive target filesystem.
  Suggested action: Rename one path and update references before transferring.
```

## Proposed command-line experience

The eventual CLI may look like this:

```bash
portascope scan ./my-project --target windows --format markdown
portascope scan ./my-project --target linux --format json --output report.json
```

These commands are design examples only and will not work until the CLI is implemented.

## Principles and non-goals

PortaScope is intended to **identify and explain risks**, not silently modify a project. It will not automatically rename files or rewrite source code during a scan. Any future fix or repair operation should be an explicit, separate action with a preview and a clear record of changes.

A clean report will not guarantee that a project runs correctly on another operating system. Runtime behaviour can depend on dependencies, configuration, environment variables, external services, and other factors that static checks cannot fully predict.

## Development roadmap

- [ ] Document the initial portability rules and supported target profiles.
- [ ] Design the rule/result data model.
- [ ] Implement the read-only directory scanner.
- [ ] Add filename, path, and metadata checks with automated tests.
- [ ] Implement Markdown and JSON reporters.
- [ ] Add CLI options, examples, and packaging.
- [ ] Add CI examples and expand the rule set based on real-world test cases.

## Contributing

The project is in its design stage, so early contributions should focus on well-defined portability cases, reproducible examples, rule proposals, and tests. A useful report should explain **what may fail, on which target, why it matters, and how a developer can investigate it**.

Contribution guidelines and a code of conduct will be added as the project matures.

---

**PortaScope — portability problems, spotted before the move.**

📬 Contact & Connect

Have questions, suggestions, or want permission to use PortaScope? Get in touch.

- Email: "lisabp720@gmail.com" (mailto:lisabp720@gmail.com)
- Discord: "orewatokyo720_47200"
- Discord Profile: To be added

For permission requests, please describe your intended use, including any plans to modify or redistribute the project.
