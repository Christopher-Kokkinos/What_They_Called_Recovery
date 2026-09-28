# SC006 acceptance and SC007 draft check — 2026-09-28

DEC-0017 records the author's acceptance of SC006 direction. SC007 draws on SRC-C02-05/C03-01/C03-02, restoring the lock reversal, no-contact stop, attendant inquiry and Zoe's constrained choice. The combined and standalone texts match. SC002 remains open; SC007–SC057 are drafts. The earlier compact pass's assertion that a child lock caught was corrected: Zoe successfully tests the unlocked door before Elias briefly triggers and reverses the central lock.

Checks: `python tools/verify_film_screenplay_draft.py` PASS; `python tools/verify_film_source_map.py` PASS; `python tools/verify_film_workspace.py` PASS; `python tools/verify_workspace.py` PASS; `git diff --check` PASS. Unrelated modified archived PDF remains untouched and unstaged.
