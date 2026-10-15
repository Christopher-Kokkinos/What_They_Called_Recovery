# DEC-0068 — Bounded first-drink motion review

2026-10-15. Latest mug_20261015_160053_a546fe41.zip all14 images reviewed, hashes match, six-pose rig readback passes. Assistant provisionally passes blockout grip; author agrees to proceed to motion test. This is not final scene/contact acceptance.

Add optional --motion-preview to existing checkpoint-based mug builder. Keep DEC-0067 hand/handle and source path/timing unchanged. Bake/read back every integer frame1400–1539 (140 poses, ~5.83 seconds at24 fps): initial lift, drink hold, return towards table. Starts with formed grip and ends before release; approach/release, exact final placement at1540 and later carry not validated. No full-scene bake.

Render48 images at640x360 with one fixed orthographic camera/scale framing the union of hand, left arm, torso anchors and evaluated mug bounds across all140 frames. Every third source frame plus1539; camera binding guard retained. Fixed framing avoids apparent movement from auto-fit changes; occlusion remains visual review. Existing14-still default remains available.

Generate local motion_preview.html with play/pause/scrub and source-frame labels using recorded timestamps, avoiding encoder/new software dependencies. Manifest preserves source24 fps, sample8 fps and final shorter interval. Save new mug_motion_ folder and validated .blend before renders, original checkpoint retained. Integer rig and actual mug position/orientation readback gates run before saving. No physics/contact force claim.

Pure246-frame mug contract and48-frame preview schedule PASS, workspace/syntax/diff PASS. Blender execution, fixed-camera visibility and motion/skin review pending. Remaining thumb/crease surface polish and wrist seam remain logged; paper/dials/keys changes queued separately.
