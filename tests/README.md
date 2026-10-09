# PortaScope Test Suite

Automated tests for portability rules and the safety contract.

Current coverage includes case collisions, reserved Windows device names, invalid filename characters, trailing spaces/dots, conservative path-length warnings, a read-only scan, symlink-safe traversal, and Markdown/JSON CLI output.

Tests use temporary directories and synthetic filenames. Target-profile tests should remain deterministic across host operating systems. Every new rule should include both positive and negative examples. Do not mark planned behaviour as implemented until executable tests pass.
