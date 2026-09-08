# Film production rules

## Objective
Build a feature-capable production system for *What They Called Recovery* while first proving the workflow with a finished 2–5 minute vertical slice.

## Cost constraint
Default production budget for software, services and assets is £0. Use free/open-source/local tools and existing hardware. Do not introduce a paid dependency without an explicit project decision.

## Story authority
- `Active/Production/` remains the publication master authority.
- `Reference/` remains read-only.
- Screenplay, scene breakdown and shot adaptation may transform source material for the film, but those transformations belong only in `Active/Film/`.
- Never back-propagate a film adaptation choice into manuscript prose without a separate explicitly authorised editorial task.

## Film workspace
- `00_Control/` — production rules, manifest, scene/asset/licence registers.
- `01_Adaptation/` — screenplay, scene breakdowns and adaptation notes.
- `02_Design/` — visual bible, character/location design and reference decisions.
- `03_Assets/` — reusable characters, sets, props, materials, rigs and asset documentation.
- `04_Scenes/` — Blender scene/shot source and shot-specific production files.
- `05_Capture/` — motion, facial and performance-reference capture workflows.
- `06_Audio/` — dialogue, Foley, ambience, SFX and music production.
- `07_Post/` — edit, compositing, grade, titles and mastering work.
- `08_Deliverables/` — approved review/final outputs only.

## Source-of-truth and reuse
Blender is the controlled 3D scene source of truth unless a task explicitly defines another source. Build reusable assets rather than recreating the same production element twice.

Suggested IDs:
- Scenes: `SC###`
- Shots: `SC###_SH###`
- Characters: `CHR_Name`
- Sets: `SET_Name`
- Props: `PRP_Name`

## Git and large-file discipline
Commit production-control text, scripts and reasonably sized canonical source assets. Do not commit generated render sequences, simulation caches, proxies, raw capture dumps, autosaves or reproducible temporary material by default. Use `Active/Film/_local/` for high-volume local working material and record anything operationally important in the control registers.

## Licensing
Every third-party asset, texture, HDRI, model, font, sound or code dependency used in production must have its source and licence recorded before final use. Prefer assets with clear commercial-use permission. "Free to download" is not sufficient evidence of reuse rights.

## Vertical-slice gate
Do not scale to feature production until one representative 2–5 minute scene has been completed through adaptation, layout/animatic, assets, animation, lighting/render, audio, edit and final review. Record bottlenecks and reusable improvements before expanding scope.

## Completion gate
When applicable:
1. Update the control registers/manifest.
2. Run `python tools/verify_film_workspace.py`.
3. Place QA/audit evidence in `Reports/Film/`.
4. Confirm no canonical manuscript or publication file changed unless explicitly authorised.
