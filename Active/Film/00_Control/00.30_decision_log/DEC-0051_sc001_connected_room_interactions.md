# DEC-0051 — Correct anatomy and rebuild contacts in connected rooms

Date: 2026-10-14
Status: implementation prepared; desktop Blender and visual review pending

Author scope: correct elbows and bed support, then drawer, shower, mug, letter and keys in the larger rooms. Author described the new layout as much better; it is a working foundation, not evidence that a supplied Blender ZIP has been inspected.

## Diagnoses

Previous elbow reach/length checks did not constrain anatomical bend direction, excessive flexion or reflected body bases. Shower reach used a root-relative fictional point. The old choreography was tied to a partition-free floor and independent stage coordinates. Static furniture placement alone did not reserve the real moving drawer/knee volume.

## Judgments and implementation

- Keep old v0.26 builder as checkpoint; implement `build_sc001_room_performance.py`, driven by the accepted working layout and new versioned performance specification. Human/prop scale stays unchanged.
- Share fixed-length joints and exact orthonormal mesh transforms. Prefer a lowered elbow plane, limit diagnostic flexion to 160°, and distinguish ground direction from torso lean.
- Keep sleeping feet inside bed and supported on mattress. Move side seat toward the bed foot to clear drawer sweep while preserving supported thighs, feet on floor and the earlier right-arm rib support. Left hand operates drawer; this is a production judgment, not a new novel fact.
- Wrist approaches the actual drawer handle through a clear waypoint; small ten-cell blister strip, two empty, remains in drawer. No medication consumption added.
- Use visible rear-wall shower controls; shoes stand on the tray. Cold response begins three seconds after water starts. Diagnostic water block/cue remain proxies.
- Mug handle follows the left grip. Elias rises for the first drink instead of folding the elbow almost completely into the shoulder. Mug is set down before paper work.
- A4-size paper (0.21 × 0.297 m) fits the table, folds along its long dimension and enters a C5-like envelope (0.22 × 0.17 m). Sizes are prop judgments; source specifies no paper dimensions. Left hand follows moving fold, then supports envelope; right inserts letter and pockets packet. Envelope has an open mouth, thin front/back faces and closing flap. Exact notice wording retained.
- Keys lie flat on the table and rotate to a relaxed hanging carry. Keys are retrieved before the mug; no simultaneous one-handed paper work and mug hold.
- Stable living-area clutter/cupboard placement; wardrobe is torso colour, without a separate floating jacket block. Clock remodel remains deferred.
- Route goes around the bed, through bedroom doorway and hall, then onto landing. Extend exit by 12 seconds (total 132 seconds) for the real path. Retain indoor pan, exterior cut, fixed shared departure scale, pigeon close and peck. Specific camera placements are new proposals.

## Limits and review

No final skin, finger rig, natural pain acting, door operation, final light/grain/audio or scene acceptance. Initial envelope opening before reading still needs refinement; this revision rebuilds the author-requested folding/insertion/pocket sequence. Generated scene uses low diagnostic walls; math tests full-height partitions. Readback validates selected evaluated meshes/support/packet bounds; full rendered visual review is still necessary.

Evidence and validation: `Reports/Film/2026-10-14_sc001_connected_room_performance_preparation.md`. Run instructions: `SC001_Room_Performance_Run_Guide.md`.

Follow-up 2026-10-14: Author conditionally passes major mechanical/posture improvements, pending graphical glitch at 1213; timing/furniture polish deferred. Confirmed solid water overlay intersects upper arm, while planned pose is constant. Remove overlay from renders and retain viewport wire guide; targeted review prepared. Exact observed-artifact diagnosis remains pending render inspection. See Reports/Film/2026-10-14_sc001_shower_overlay_diagnosis.md.
