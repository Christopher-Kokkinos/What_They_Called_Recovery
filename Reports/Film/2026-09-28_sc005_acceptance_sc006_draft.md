# SC005 acceptance and SC006 draft check — 2026-09-28

DEC-0016 records the author's acceptance of SC005 screenplay direction. SC002 remains draft. SC006 proposes Zoe's first negotiation with Elias and the lift passage, using SRC-C02-03/04. The earlier combined pass had introduced a rabbit handoff and broader call agreement that were not in the Chapter 2 source; this draft restores the source's repaired-rabbit conversation and the unresolved boundaries. The combined and standalone SC006 texts match. This is a film-only change, with no claim that production details are final.

Checks: `python tools/verify_film_screenplay_draft.py` PASS (12 sequences, 57 scenes, 230 units); `python tools/verify_film_source_map.py` PASS (46 chapters, 230 units); `python tools/verify_film_workspace.py` PASS; `python tools/verify_workspace.py` PASS; `git diff --check` PASS. An unrelated locally modified archived PDF remained untouched and unstaged.
