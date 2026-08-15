# What They Called Recovery — Codex Instructions

This repository contains an unpublished novel and its controlled Amazon KDP publication workflow.

## Non-negotiable rules
1. `Active/Production/` contains the authoritative current production master.
2. Never rewrite, paraphrase, modernise, shorten, expand, or otherwise alter manuscript prose unless the current task explicitly authorises prose changes.
3. Any unexplained manuscript-text difference is a FAIL.
4. `Reference/` is read-only unless the task explicitly authorises a reference update.
5. `Archive/` is immutable. Never edit archived files in place; promote/copy material out if it becomes active again.
6. Logs, diffs, validation evidence, and audit outputs belong in `Reports/`.
7. Never delete historical evidence unless explicitly authorised.
8. Do not declare PASS from inspection alone when a deterministic validation command exists. Run it and report the result.
9. Read only the task-specific rule/workflow files needed for the current task; do not preload all repository guidance.

## Task routing
- Editorial/prose work → `docs/rules/editorial.md`
- Canon/authority questions → `docs/rules/canon.md`
- Manuscript regression/diffs → `docs/rules/regression.md`
- Kindle/KDP preparation → `docs/rules/kdp.md`
- Workspace organisation → `docs/rules/workspace.md`
- Git/branch/release operations → `docs/rules/git.md`
- Repeatable procedures → `workflows/`
- Mechanical validation → `tools/`

## Default completion gate
Before marking a manuscript-affecting task complete, generate/sync the deterministic text mirror, run the relevant verifier, inspect the resulting diff, and place evidence in `Reports/`.
