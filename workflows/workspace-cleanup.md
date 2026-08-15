# Workspace cleanup workflow

Read `docs/rules/workspace.md` and `docs/rules/git.md`.

1. Inventory root and `Active/`.
2. Move superseded items to `Archive/` without altering contents.
3. Move logs/reports/evidence to `Reports/`.
4. Leave locked validation sources in `Reference/`.
5. Do not delete historical evidence.
6. Run `python tools/verify_workspace.py`.
7. Report moves and any ambiguous items requiring human decision.
