# DEC-0053 — Elias SC001 rig motion test

Date: 2026-10-14. Author approves all ten rig gallery poses and authorises continuous SC001 testing.

Reuse the shared armature/skin constructor in both gallery and scene builders. Add an opt-in `--rig-test` to the connected-room builder; output into a separate `rig_scene_...` folder. Preserve accepted choreography, props, shot timing and cameras. Render skin instead of body boxes; retain boxes for the established contact checks and comparison in Blender.

Bake exact FK targets at every source frame, without changing limb lengths. Read back keyed bone endpoints/scale and finite evaluated skin vertices over all 3,168 integer frames. These checks do not establish skin collision clearance or fractional-frame correctness. Hands remain provisional and grip retargeting may require a later revision.

Author gallery visual pass is scoped to the neutral mannequin prototype, not final character design or whole-scene acceptance. Bedroom support, drawer, shower, mug, two-handed letter sequence, keys and departure require new skin visual review. Existing timing/furniture polish remains deferred.
