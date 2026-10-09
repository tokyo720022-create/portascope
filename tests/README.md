PortaScope Test Suite

This directory contains automated tests for PortaScope's portability rules.

Planned Coverage

- Filename collisions across operating-system profiles
- Reserved names and invalid filename characters
- Path-length warnings
- Read-only scanning behaviour
- Markdown and JSON report output

Testing Principles

- Use temporary directories and synthetic filenames.
- Never modify or delete files in a user's scanned project.
- Test target operating systems through explicit, deterministic profiles.
- Include both problematic and safe examples for every rule.

The test suite will expand alongside the implementation. A rule is not considered implemented until executable tests verify its behaviour.
