# SC021 source development — 2026-10-10

## Scope and evidence

Expanded SC021 after the author authorised continuation from the desktop checkpoint ec46c49. Read the Chapter 17 text mirror, SC020/SC022 handoffs, adaptation register and applicable film workflow. The individual Fountain body and combined screenplay are synchronized. The paired review documents the four mapped source units, retained functions, shortened material, proposed staging and uncertainty boundaries.

Key changes: explicit room/escape boundaries; Elias's accountability for the tracker and Mac; first observation exercise without a notebook; specific recognition of Zoe's observation; pre-dawn shared car sweep. Corrected ADP0084's unsupported notebook carrier without changing IDs, disposition, target or provisional status. The queue, scene index and project state now identify SC021 as source-developed and SC022 as next. DEC-0018 remains the existing working-direction approval; this revision's detail is pending author review. No production manifest gate changed.

## Validation

- `python tools/verify_film_screenplay_draft.py`: PASS — 12 sequences, 57 scenes, 230 source units, standalone bodies mirrored.
- `python tools/verify_film_source_map.py`: PASS — 46 chapters, 230 units, zero errors.
- `python tools/verify_film_workspace.py`: PASS.
- `python tools/verify_workspace.py`: PASS.
- `git diff --check`: PASS.

These checks establish navigation, coverage and structural consistency. Source fidelity and character interpretation were assessed manually against Chapter 17, as recorded in the paired review. Runtime 7–9 minutes is an estimate pending animatic timing.

## Protected material

Two binary modifications were already present before this task: the publication `resources/book.kdf` and archived continuation-plan PDF. Neither was edited or staged by this task. All committed changes are film derivatives/control text or this report; no manuscript prose, reference or archive change is included.
