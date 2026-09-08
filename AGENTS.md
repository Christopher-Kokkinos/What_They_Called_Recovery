# What They Called Recovery — Agent Instructions

This repository contains an unpublished novel, its controlled Amazon KDP publication workflow, and a controlled film-adaptation production system.

## Non-negotiable rules
1. `Active/Production/` contains the authoritative current publication master.
2. Never rewrite, paraphrase, modernise, shorten, expand, or otherwise alter manuscript prose unless the current task explicitly authorises prose changes.
3. Any unexplained manuscript-text difference is a FAIL.
4. `Reference/` is read-only unless the task explicitly authorises a reference update.
5. `Archive/` is immutable. Never edit archived files in place; promote/copy material out if it becomes active again.
6. Logs, diffs, validation evidence, and audit outputs belong in `Reports/`.
7. Never delete historical evidence unless explicitly authorised.
8. Do not declare PASS from inspection alone when a deterministic validation command exists. Run it and report the result.
9. Read only the task-specific rule/workflow files needed for the current task; do not preload all repository guidance.
10. Film adaptation work may transform story material into screenplay/shot form, but it must never silently modify the canonical manuscript or publication master.
11. Film production is zero-cash by default: no paid software, subscriptions, services, assets, render farms, or hired labour without an explicit project decision changing that constraint.

## Task routing
- Editorial/prose work → `docs/rules/editorial.md`
- Canon/authority questions → `docs/rules/canon.md`
- Manuscript regression/diffs → `docs/rules/regression.md`
- Kindle/KDP preparation → `docs/rules/kdp.md`
- Film/Blender/adaptation production → `docs/rules/film.md`
- Workspace organisation → `docs/rules/workspace.md`
- Git/branch/release operations → `docs/rules/git.md`
- Repeatable procedures → `workflows/`
- Mechanical validation → `tools/`

## Default completion gates
For manuscript-affecting work: generate/sync the deterministic text mirror, run the relevant verifier, inspect the resulting diff, and place evidence in `Reports/`.

For film-only structural/production work: run `python tools/verify_film_workspace.py` when applicable, keep film control registers current, and place meaningful QA/audit evidence in `Reports/Film/`. If manuscript files were not changed, do not manufacture a manuscript diff.
