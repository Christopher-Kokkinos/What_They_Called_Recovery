# What They Called Recovery

Controlled working repository for the novel, its Amazon KDP publication workflow, and the animated-film adaptation.

## Current project status
- **Kindle ebook:** published on the Amazon Kindle store (author-reported, 27 September 2026).
- **First-edition book work:** paperback publication remains. Once that is complete, the first-edition publication work can be closed.
- **Animated movie:** `animated-movie` is the active development branch, separate from `main`, which remains the accepted novel/KDP state. The film is in adaptation preparation; source decomposition currently covers Chapters 1–5 of 46. No screenplay or vertical-slice scene has been approved yet.

## Production domains
- **Book / KDP** — the existing publication authority chain remains unchanged. `Active/Controls/WTCR_KDP_Workflow_Status.txt` records an earlier production-phase snapshot and has not yet been reconciled with the reported Kindle release.
- **Film** — adaptation work lives in `Active/Film/`. A finished 2–5 minute vertical slice is the first production milestone after enough whole-story mapping to choose it responsibly. Software, services and acquired assets have a zero-cash default constraint.

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
