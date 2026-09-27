# Film agent entrypoint

Read the repository `AGENTS.md` and the task-specific film rule/workflow before editing. Start with `00_Control/00.40_project_state/README.md` for current phase and next gate. The canonical novel remains in `Active/Production/`; `Reference/` and `Archive/` are protected.

Choose the target by artifact, not by tool:

| Artifact | Authoritative location |
|---|---|
| Film governance, decisions, project state, schemas | `00_Control/` |
| Source map, treatment, sequences, adaptation decisions, screenplay | `01_Adaptation/` and its existing register in `00_Control/` |
| Character dossiers and film-specific continuity | `10_Characters/` |
| Whole-story dependencies, timeline, reveal logic | `20_Story_System/` |
| Visual designs and approved references | `02_Design/` |
| Reusable Blender assets and their IDs | `03_Assets/` and `00_Control/asset_register.csv` |
| Shot-specific `.blend` sources and versioned `bpy` automation | `04_Scenes/` |
| Evidence and validation outputs | `Reports/Film/` at repository root |

Character dossiers and story-system notes are working film interpretations. Record an authoritative novel fact with a chapter/source-unit reference in the canon register; record an adaptation invention as a film decision. Do not create a competing manuscript canon, screenplay master, asset registry or scene registry.

Before a broad Blender operation, checkpoint the `.blend`, identify the exact scene/objects affected, run the script or bounded MCP operation, and inspect the result. Keep generated renders and caches under ignored `Active/Film/_local/`. Update the project state only after the relevant validation and decision evidence exists.
