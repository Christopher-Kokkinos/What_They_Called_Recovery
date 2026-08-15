# Workspace rules

The repository root is operational, not historical.

- `Active/`: only current work or planned near-future work.
- `Reference/`: locked sources still required for validation; read-only.
- `Reports/`: logs, manifests, diffs, QA evidence, audit outputs.
- `Archive/`: superseded/historical files; immutable.

When a file is superseded, move it from Active to Archive rather than deleting it. Do not duplicate large binaries merely for convenience. Git history is not a substitute for the explicit Archive when a historical artifact is part of the publication evidence chain.
