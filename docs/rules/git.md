# Git workflow rules

- `main` represents the last accepted project state.
- New phases/infrastructure work should use a focused branch.
- Commit only task-related changes.
- Do not force-push accepted history.
- Use clear phase/task commit messages.
- Before merge, run applicable deterministic checks and place evidence in `Reports/`.
- Prefer a reviewable PR for structural, manuscript-affecting or release changes.
- Binary DOCX/KPF files must be accompanied by deterministic text/diff evidence when manuscript text could have changed.
