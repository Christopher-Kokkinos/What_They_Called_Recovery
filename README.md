# What They Called Recovery

Controlled working repository for the novel, its Amazon KDP publication workflow, and the animated-film adaptation.

## Current project status
- **Kindle ebook:** the repository's Phase 5 report records a PASS for Kindle Create build, KPF export and 46/46 chapter checks on 16 August 2026. Store publication was reported by the author on 27 September 2026; the repository does not yet contain a store-publication receipt/report.
- **First-edition book work:** paperback publication remains. Once that is complete, the first-edition publication work can be closed.
- **Animated movie:** `animated-movie` is the active development branch, separate from `main`, which remains the accepted novel/KDP state. The film is in adaptation preparation; descriptive source decomposition covers all 46 chapters (230 units). A whole-story source-map audit is documented in `Reports/Film/2026-09-27_whole_story_source_audit.md` for review. Treatment and sequence outline are next. No screenplay or vertical-slice scene has been approved yet.

## Production domains
- **Book / KDP** — the existing publication authority chain remains unchanged. `Reports/Phase5/WTCR_KDP_Phase5_Kindle_Create_Report.txt` documents the latest completed phase in this repository. `Active/Controls/WTCR_KDP_Workflow_Status.txt` is stale: it still lists Phase 5 as NEXT and has not been reconciled with the Phase 5 PASS or reported store release.
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
