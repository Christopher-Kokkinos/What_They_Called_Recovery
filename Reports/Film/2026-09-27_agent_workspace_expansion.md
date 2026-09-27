# Agent workspace expansion — 27 September 2026

Scope: film-only structure on `animated-movie`. `Active/Film/00_Control/` was extended with governance, cited canon, decision log, project state and schema-policy folders. `10_Characters/` has eleven named dossier placeholders and a common template. `20_Story_System/` holds four working-model areas. `04_Scenes/Automation/` reserves a location for reproducible Blender scripts. `Active/Film/AGENTS.md` routes future agents to the existing authority chain and artifacts.

Architecture decisions: preserve existing manifest and CSV paths; keep novel publication authority under `Active/Production/`; distinguish character dossiers from visual designs and reusable Blender assets; reserve schema/script implementation until a real consumer or shot specification exists. The requested “cannon” concept is named **canon**. Folders do not approve source interpretations or change the current adaptation gate.

Validation: `python tools/verify_film_workspace.py` and `python tools/verify_workspace.py` pass. The production manifest parses. The staged diff is checked for whitespace errors before commit. No manuscript, KDP master, locked reference, archive, or root production-control file changed. The new canon register contains only a header; no novel facts were asserted without source review.
