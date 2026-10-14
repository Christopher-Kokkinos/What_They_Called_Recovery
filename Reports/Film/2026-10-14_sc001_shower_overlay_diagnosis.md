# SC001 frame 1213 — author review and overlay diagnosis

Date: 2026-10-14

Author reports a major improvement, corrected rib/hand support and major posture issues resolved. Conditional pass pending a right-arm graphical glitch at frame 1213. Letter hold is too long, furniture is misplaced in places and remaining small issues exist; author explicitly defers these to later timing/visual production. This is author feedback, not an independently inspected new ZIP or physics simulation result. No scene/finished-slice completion inferred.

## Evidence

Pure state and exact upper-arm/forearm mesh bases are identical at source frames 1210–1216. Therefore no planned transform discontinuity at 1213 was found. The render helper creates an opaque Workbench box `REVIEW_ShowerWater` at (12.9, 0.65, 1.5), dimensions (0.4, 0.04, 1.0), which becomes visible at 1210. Oriented-box intersection at 1213 confirms overlap with right upper arm; forearm and palm do not overlap this box. Previous obstacle checks cover set/furniture/drawer, not this graphical overlay.

This is a concrete render-overlay defect and a plausible explanation of the author's observation. It is not proof of the exact observed artifact without the rendered frame. No incoming frame/validation ZIP was supplied with this feedback.

## Bounded correction

Exclude the solid diagnostic water box from all renders; retain a wireframe viewport guide, visible while water is on. Keep the existing cold cue. No anatomy or choreography changes. Add `--render-shower-review` for six source-frame stills (1195, 1207, 1213, 1225, 1237, 1285) and evaluated-frame readback. This preserves accepted motion and supports a small visual check.

## Checks and remaining gate

Python compilation: PASS. Film-workspace verifier: PASS. `git diff --check`: PASS. Arm plan was inspected mechanically; overlay intersection reproduced. Full-frame posture/geometry tests from the prior preparation remain applicable because their math modules are unchanged. Blender execution and rendered confirmation pending. The conditional pass remains conditional until the author confirms frame 1213.
