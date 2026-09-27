# Source decomposition checkpoint — Chapters 6–10

Scope: 23 descriptive source units in `Active/Film/01_Adaptation/Source_Decomposition/Chapters_06-10.md`, continuing the 26 units in Chapters 1–5. Source navigation: deterministic chapter text mirrors 06–10 under the locked Phase 7 PDF story baseline. Chapters 11–46 remain unmapped. No screenplay, treatment, source disposition or scene selection is approved.

Checks run:

```text
python tools/verify_film_workspace.py
python tools/verify_workspace.py
python -m json.tool Active/Film/00_Control/production_manifest.json
git diff --check
```

All four commands passed: the film verifier reported `result=PASS`, workspace verifier reported `result=PASS`, the manifest parsed, and `git diff --check` was silent. Changed paths are restricted to the film source map, its coverage/status indicators, the root README coverage line and this report. The manuscript, KDP production artifacts, locked references and archive remained untouched. Interpretive completeness is not established by mechanical validation; forward dependencies need review against the remaining chapters.
