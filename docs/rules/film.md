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
- The screenplay is authoritative for the film adaptation only; it never supersedes the novel as publication canon.

## Required production order
Do not translate novel prose directly into Blender shots.

The controlled chain is:

```text
canonical manuscript
        ↓
source decomposition
        ↓
adaptation register
        ↓
screenplay
        ↓
production scene packets
        ↓
shot specifications
        ↓
Blender production
```

Use `workflows/film-adaptation-preparation.md` for the adaptation stage.

## Adaptation decisions
Every meaningful source unit that is changed or excluded from the screen version must be explicitly classified. Approved dispositions are:
- `KEEP`
- `COMPRESS`
- `MERGE`
- `OMIT`
- `RELOCATE`
- `VISUALISE`
- `VOICEOVER`
- `SPLIT`

No omission or structural change is silent. If narrative information remains necessary after compression/omission/merge, record where that information is transferred.

## Film workspace
- `00_Control/` — production rules, manifest, scene/asset/licence/adaptation registers.
- `01_Adaptation/` — screenplay, scene breakdowns, scene packets and adaptation notes.
- `02_Design/` — visual bible, character/location design and reference decisions.
- `03_Assets/` — reusable characters, sets, props, materials, rigs and asset documentation.
- `04_Scenes/` — Blender scene/shot source and shot-specific production files.
- `05_Capture/` — motion, facial and performance-reference capture workflows.
- `06_Audio/` — dialogue, Foley, ambience, SFX and music production.
- `07_Post/` — edit, compositing, grade, titles and mastering work.
- `08_Deliverables/` — approved review/final outputs only.

## Blender dual-execution SOP
Codex/VS Code may operate Blender through two complementary routes.

### Route A — versioned `bpy`
Use committed Python for reproducible, repeatable, structural, batch or validation work.

### Route B — live Blender MCP
Use MCP for scene inspection, diagnosis and bounded interactive/artistic changes to the active Blender session.

Use the most reproducible practical route. If an MCP operation becomes repetitive or production-critical, promote it into versioned Python.

The binding operating procedure is `workflows/blender-dual-execution-sop.md`.

## Blender execution safety
- Treat MCP Python execution as privileged execution.
- Checkpoint before broad/destructive live changes.
- Do not allow Blender agents to modify canonical manuscript/KDP material.
- Do not operate on the only copy of a production scene.
- Validate the resulting scene state after significant operations.
- Generated Python must not access unrelated filesystem/network locations unless explicitly authorised.

## Source-of-truth and reuse
Blender is the controlled 3D scene source of truth unless a task explicitly defines another source. Build reusable assets rather than recreating the same production element twice.

Suggested IDs:
- Adaptation units: `ADP####`
- Scenes: `SC###`
- Shots: `SC###_SH###`
- Characters: `CHR_Name`
- Sets: `SET_Name`
- Props: `PRP_Name`

## Git and large-file discipline
Commit production-control text, scripts and reasonably sized canonical source assets. Do not commit generated render sequences, simulation caches, proxies, raw capture dumps, autosaves or reproducible temporary material by default. Use `Active/Film/_local/` for high-volume local working material and record anything operationally important in the control registers.

## Licensing
Every third-party asset, texture, HDRI, model, font, sound, code dependency or AI-generated production dependency used in production must have its source and licence recorded before final use. Prefer assets with clear commercial-use permission. "Free to download" is not sufficient evidence of reuse rights.

## Adaptation gate
Do not select or build the vertical slice from raw novel prose alone. First decompose enough of the story to understand candidate scenes' setup, payoff and continuity dependencies.

## Vertical-slice gate
Do not scale to feature production until one representative 2–5 minute scene has been completed through adaptation, layout/animatic, assets, animation, lighting/render, audio, edit and final review. Record bottlenecks and reusable improvements before expanding scope.

## Completion gate
When applicable:
1. Update the control registers/manifest.
2. Run `python tools/verify_film_workspace.py`.
3. Place QA/audit evidence in `Reports/Film/`.
4. Confirm no canonical manuscript or publication file changed unless explicitly authorised.
