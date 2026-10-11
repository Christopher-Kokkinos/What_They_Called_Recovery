# SC001 v0.14 shared upper-body preparation

Author authorised correction of the v0.13 hybrid attachment/support failure. Opening frames 1–888 now have one joint authority: elias_articulation.opening_joints. The old motion pass no longer solves opening arms; it retains later kitchen/paper/carry handling.

## Root-cause correction

An orthonormal chest basis drives torso twist, shoulders, elbow poles, wrists, head orientation and a new neck bridge. Shoulders sit on the chest side surface rather than following the former independent root transform. Upper arms/forearms remain 0.36/0.34 m. Resting arms follow the chest throughout the staged rise, transition into right-hand left-rib support, then approach/close/release the drawer. Head orientation no longer combines the older root rotation with independently overridden head position. Neck bridges the former visible gap.

The support wrist sits 0.19 m in front of the torso plane. Forearm centreline checks retain at least 0.18 m clearance versus torso half-depth 0.125 m plus forearm half-width 0.055 m. This addresses the identified buried support forearm; it does not certify every upper-arm/palm collision or final grip. The fixed planted-ankle/leg plan is retained.

## Validation

All 888 planned opening frames pass fixed arm/leg/spine lengths, bounded arm reach and orthonormal chest axes. Right support forearm surface checks pass frames 350–750 at eleven line samples each. Existing custody, later-handling reach and workspace checks pass; all automation parses and diff check passes.

The desktop script now asserts evaluated upper-arm shoulder/elbow and forearm elbow/wrist endpoint errors below 0.00001 m across all 888 opening source frames, and retains twelve evaluated foot/leg records. Maximum attachment error is included in validation.json. This checks actual mesh transforms against common joint targets, not only numerical reach. No agent-side Blender execution occurred.

## Desktop gate

Run full --render-shot-review --render-motion-preview. Inspect SH001 arm/chest attachment and head/neck during waking, SH002 support hand on the outside of left ribs, SH003 approach/closure/release and full label/two empty cells. A changing camera radial may result from new arm geometry; inspect the selected camera rather than assuming v0.13's 195° survives. Check later shots for regressions and final custody.

Remaining limitations: staged rise remains a proxy rather than an anatomical roll; no armature/skinning, collision solver, finger grip, breathing, clothing or walk cycle. Source-frame endpoint checks do not establish subframe contact or acting. Final appearance/performance/pacing remain pending; no finished-slice gate passed. No canonical/publication changes; unrelated existing binaries excluded.
