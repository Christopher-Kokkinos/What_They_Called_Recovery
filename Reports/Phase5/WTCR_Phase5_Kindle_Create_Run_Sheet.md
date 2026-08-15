# WTCR Phase 5 — Kindle Create Run Sheet

Branch: `agent/phase-5-kindle-create`
Source: `Active/Production/What_They_Called_Recovery_KDP_Publication_Phase4.docx`
Workflow: `workflows/phase-5-kindle-create.md`
Rules: `docs/rules/kdp.md`

## Codex prompt

> Execute the Phase 5 Kindle Create preparation workflow for this repository. Read `AGENTS.md`, `workflows/phase-5-kindle-create.md`, and `docs/rules/kdp.md` only, plus any directly referenced active control file needed for the task. Do not alter manuscript wording. Run all deterministic repository checks that can be run locally. Guide/record the Kindle Create steps that require the desktop application. Save all Phase 5 evidence under `Reports/Phase5/`. Any wording drift or structural loss is a FAIL.

## Before Kindle Create
- [ ] Confirm current branch is `agent/phase-5-kindle-create`.
- [ ] Confirm active publication source exists.
- [ ] Run repository/workspace verifier.
- [ ] Run manuscript structural verifier.
- [ ] Generate/sync deterministic text mirror if required by tools.

## Kindle Create session
- [ ] Record Kindle Create version.
- [ ] Import Phase 4 publication DOCX as reflowable ebook.
- [ ] Confirm 46 chapter titles detected.
- [ ] Confirm chapter order 01–46.
- [ ] Confirm front matter.
- [ ] Confirm interactive TOC/navigation.
- [ ] Inspect representative early/middle/late chapter openings.
- [ ] Inspect representative scene breaks.
- [ ] Inspect italics.
- [ ] Inspect monospaced/notebook material.
- [ ] Confirm no unintended cover embedded in manuscript.
- [ ] Save editable Kindle Create project (`.kcb` and associated project data as produced by Kindle Create).
- [ ] Export KPF.

## Regression / evidence
- [ ] Run post-conversion manuscript/text checks available locally.
- [ ] Record any Kindle Create warnings or conversion interventions.
- [ ] Confirm manuscript wording changes authorised during Phase 5: NONE.
- [ ] Place screenshots/check results/tool version notes under `Reports/Phase5/`.

## Pass gate
Phase 5 may be marked PASS only when the actual Kindle Create application/output has been used and:
1. 46 chapters and correct order are confirmed.
2. TOC/navigation is confirmed.
3. Front matter and representative formatting are visually confirmed.
4. Editable Kindle Create project is saved.
5. KPF is exported.
6. No unexplained manuscript wording drift or structural loss exists.

Status: IN PROGRESS
