# Regression rules

Goal: prove that a transformation introduced only authorised differences.

1. Generate deterministic chapter text from the active DOCX.
2. Compare against the accepted baseline text mirror or explicitly named baseline.
3. Produce a unified diff in `Reports/Diffs/`.
4. Classify each difference as approved, structural/format-derived, or unexplained.
5. Any unexplained manuscript wording change = FAIL.
6. Validate chapter count/order and scene-break count.
7. Do not repair failures during an audit unless the task explicitly includes repair.
8. Report exact counts; never substitute qualitative claims for deterministic results.
