# SC001 blockout automation preparation

Scope: versioned diagnostic builder, desktop run guide, DEC-0023 and current-state/manifest updates. No manuscript, source mapping, screenplay, final assets or scene acceptance changed.

Validation performed in agent environment:
- Python compilation passed.
- Actual SC001 specification passed continuity/hash validation (LF-normalised for Windows checkout).
- Deliberately invalid frame gap, duplicate shot ID, source hash and duration were each rejected.
- Film workspace verifier PASS.
- Film screenplay verifier PASS: 12 sequences, 57 scenes, 230 source units.
- git diff --check passed.

Code review: no deletion, no network/external asset access; new background-only scene and unique ignored run folder; source hash gate; ten camera markers; shared pigeon geometry/two instances; required-object/settings assertions; save existence check and optional still checks. Diagnostic labels include exact notice, clock at eight/alarm off and prescription/two empty cells. Cutaway geometry and camera choices are film inventions logged in DEC-0023.

Execution limitation: no Blender executable or bpy module available here. Compilation and spec validation do not certify Blender 5.2 API execution, render success, framing or visual readability. Run guide provides a fresh background desktop test; validation.json is emitted only after requested operations succeed. Failed partial runs must be retained as failures. No generated .blend/PNG or performance benchmark is claimed.

Production limitations: discrete standing proxy placements only; no sleeping/pain performance, prop transfer, drawer/fold animation, bird animation, sound or final look. Review stills and correct framing before detailed modelling. Finished vertical-slice gate remains false.

Protected pre-existing working-tree changes (KDP book.kdf and archived roadmap PDF) were left untouched and excluded from this task.
