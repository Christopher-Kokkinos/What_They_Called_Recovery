# Source decomposition checkpoint — Chapters 1–5

Scope: descriptive mapping of 26 source units in `Active/Film/01_Adaptation/Source_Decomposition/Chapters_01-05.md`. Sources navigated with `Reports/Manuscript_Text/Chapter_01.txt`–`Chapter_05.txt`, under `Reference/Locked_Phase7_Manuscript/` story authority. No adaptation disposition or screenplay scene has been approved; Chapters 6–46 remain to be mapped.

Validation in clean local checkout of `animated-movie`:

```text
python tools/verify_film_workspace.py
missing_dirs=[] missing_files=[] reports_film=True film_rule=True vertical_slice_workflow=True adaptation_workflow=True dual_execution_sop=True result=PASS

python tools/verify_workspace.py
missing=[] root_binary_clutter=[] result=PASS

python -m json.tool Active/Film/00_Control/production_manifest.json
PASS

git diff --check
PASS
```

Changed paths are limited to the film source map, its README, this report and the film manifest status. No manuscript, publication master, locked reference or archive file was changed. The adaptation register deliberately remains empty until whole-film planning. These mechanical checks do not prove interpretive completeness; later chapters may change the reading of early clues.
