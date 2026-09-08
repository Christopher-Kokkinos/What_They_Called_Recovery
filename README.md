# What They Called Recovery

Controlled working repository for the novel, its Amazon KDP publication workflow, and the film-adaptation production system.

## Production domains
- **Book / KDP** — the existing publication authority chain remains unchanged. Use `Active/Controls/WTCR_KDP_Workflow_Status.txt` for current workflow status rather than inferring status from folder names.
- **Film** — preproduction begins in `Active/Film/`, with a 2–5 minute vertical slice as the first production objective and a zero-cash software/services constraint.

## Workspace
- `Active/` — current production, editorial, control, and film material.
- `Active/Film/` — film adaptation, design, assets, Blender scenes, capture, audio, post and deliverables.
- `Reference/` — locked read-only validation sources.
- `Reports/` — logs, diffs, audit evidence and validation outputs.
- `Archive/` — superseded/historical material; immutable.
- `docs/rules/` — task-specific governance loaded only when needed.
- `workflows/` — repeatable task procedures.
- `tools/` — deterministic extraction, diff and workspace validation scripts.

The film workflow does not replace or relocate the KDP authority chain. Canonical manuscript prose remains protected by the existing manuscript rules.

Read `AGENTS.md` before using an agent on this repository.
