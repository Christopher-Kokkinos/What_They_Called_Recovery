# Film Production Control

This directory is the operational control plane for the film project.

Maintain:
- `production_manifest.json` — phase, constraint and vertical-slice state.
- `scene_register.csv` — canonical scene IDs and production status.
- `asset_register.csv` — reusable asset IDs, type and status.
- `licence_register.csv` — third-party source/licence evidence.
- `adaptation_register.csv` — source-unit film dispositions once approved.

Control subfolders: `00.10_governance/` for authority and gates; `00.20_canon_register/` for cited continuity claims; `00.30_decision_log/` for dated material decisions; `00.40_project_state/` for a short human-readable handoff; `00.50_schemas/` for future validated exchange formats. The original top-level registers and manifest retain their existing paths.

No production asset is considered final merely because it exists. Finality is established through the relevant register/status and review evidence.
