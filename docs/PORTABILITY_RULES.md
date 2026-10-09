# Portability Rules (Draft)

This document defines the initial rules before implementation. Findings are advisory unless a rule can establish a direct conflict.

## Finding format

Each finding should include:

- Stable rule ID (for example, `WIN-NAME-001`)
- Severity: `error`, `warning`, or `info`
- Relative path(s) affected
- Target profile
- Plain-language explanation
- Suggested resolution
- Whether the finding is certain or heuristic

## Initial rules

| Rule ID | Target | Condition | Default severity |
|---|---|---|---|
| `CASE-COLLISION-001` | Case-insensitive target | Two relative paths collide after case folding | error |
| `WIN-NAME-001` | Windows | A path component uses a reserved device name | error |
| `WIN-CHAR-001` | Windows | A filename contains a disallowed character | error |
| `WIN-TRAIL-001` | Windows | A filename component ends in a space or dot | warning |
| `PATH-LENGTH-001` | Configurable | A path exceeds the selected profile threshold | warning |
| `META-SYMLINK-001` | Transfer-dependent | A symlink may not be preserved by the chosen transfer method | info |
| `META-EXEC-001` | Transfer-dependent | Executable-bit metadata may not be preserved | info |

## Safety contract

1. Scanning must not write into, rename, or delete anything in the scanned tree.
2. Tests must use temporary directories and synthetic fixtures.
3. Fix generation must be preview-only by default.
4. Applying a fix must be a separate explicit operation, require confirmation, and revalidate that the affected file has not changed since the preview.
5. Do not claim a target will definitely fail when the outcome depends on filesystem or transfer configuration.
6. The core scanner must not make network requests.

## Target profiles

Profiles describe expected destination behaviour; they do not imply every installation uses identical settings. Start with conservative Windows, Linux, and macOS profiles, and make configurable assumptions explicit in reports.
