# WTCR Film Production

This subtree contains the screen adaptation and animation-production system for *What They Called Recovery*.

## Current phase
**Adaptation preparation.** Source decomposition covers all 46 chapters; the whole-story source-map audit is documented in `Reports/Film/2026-09-27_whole_story_source_audit.md` for review. The next gate is treatment and sequence outline before adaptation dispositions, screenplay scenes and selection of a representative 2–5 minute vertical slice.

## Hard constraint
Production software, services and externally acquired assets default to **£0 cash cost**. Existing hardware and the creator's own labour/time are the available production resources.

## Structure
- `00_Control/` — production manifest, registers, conventions and decision controls.
- `01_Adaptation/` — screenplay and scene-level adaptation.
- `02_Design/` — visual language, character/location design and reference boards.
- `03_Assets/` — reusable production assets and asset documentation.
- `04_Scenes/` — Blender scenes and shot work.
- `05_Capture/` — body/facial/performance capture work.
- `06_Audio/` — dialogue, Foley, SFX, ambience and music.
- `07_Post/` — editorial, compositing, grade and titles.
- `08_Deliverables/` — approved review/final outputs.
- `10_Characters/` — source-backed character dossiers and knowledge continuity; designs/assets remain in their existing domains.
- `20_Story_System/` — cross-chapter timeline, relationships, reveals and continuity working models.

Read `AGENTS.md` in this film subtree for agent routing. `00_Control/00.10_governance/` through `00.50_schemas/` organise the controls without replacing the existing manifest or registers. Versioned Blender scripts belong in `04_Scenes/Automation/` when a specified scene requires them.

Generated renders, caches, proxies and raw capture belong in ignored local working directories unless explicitly promoted as evidence or deliverables.

See `docs/rules/film.md` before film-production work.
