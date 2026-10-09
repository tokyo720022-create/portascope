# Initial Portability Rules

Findings are advisory unless a rule establishes a direct naming conflict.

| Rule ID | Target | Condition | Default severity |
|---|---|---|---|
| `CASE-COLLISION-001` | Case-insensitive target | Two relative paths collide after case folding | error |
| `WIN-NAME-001` | Windows | A path component uses a reserved device name | error |
| `WIN-CHAR-001` | Windows | A filename contains a disallowed character | error |
| `WIN-TRAIL-001` | Windows | A filename component ends in a space or dot | warning |
| `PATH-LENGTH-001` | Windows profile | A relative path exceeds the conservative threshold | warning |

## Safety contract

1. Scanning must not write into, rename, or delete anything in the scanned tree.
2. Tests use temporary directories and synthetic fixtures.
3. Future fix generation is preview-only by default.
4. Applying a fix is a separate explicit operation, requires confirmation, and revalidates the affected file.
5. Reports must not claim failure when the outcome depends on filesystem or transfer configuration.
6. Core scanning must not make network requests.

Profiles model common destination behaviours, not every filesystem configuration. macOS volumes can be case-sensitive or case-insensitive. The 260-character Windows path threshold is a warning, not a guarantee of failure.
