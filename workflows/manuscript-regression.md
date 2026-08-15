# Manuscript regression workflow

Read `docs/rules/regression.md` and `docs/rules/canon.md`.

1. Identify current active master and accepted baseline.
2. Run `python tools/extract_manuscript.py` for each DOCX as needed.
3. Run `python tools/diff_manuscript.py BASE CURRENT --output Reports/Diffs/<name>.diff`.
4. Run `python tools/verify_manuscript.py CURRENT`.
5. Inspect all differences. Do not edit manuscript during this workflow.
6. Write a concise PASS/FAIL report under `Reports/` with exact counts and unexplained differences.
