# Workspace rules

The repository root is operational, not historical.

- `Active/`: only current work or planned near-future work.
- `Reference/`: locked sources still required for validation; read-only.
- `Reports/`: logs, manifests, diffs, QA evidence, audit outputs.
- `Archive/`: superseded/historical files; immutable.

## Active production domains
The existing KDP authority chain remains in `Active/Controls/`, `Active/Editorial/`, and `Active/Production/`. Do not relocate those folders merely to make room for film work; existing manifests, tools, and publication evidence depend on their stable paths.

Film production lives under `Active/Film/` as a separate domain. Film work may reference canonical story material but must not alter publication authority by side effect.

When a file is superseded, move it from Active to Archive rather than deleting it. Do not duplicate large binaries merely for convenience. Git history is not a substitute for the explicit Archive when a historical artifact is part of the publication evidence chain.

Generated renders, caches, proxies, raw capture dumps and other reproducible/high-volume film intermediates are local working material by default and should not be committed unless a specific evidence or release requirement justifies it.
