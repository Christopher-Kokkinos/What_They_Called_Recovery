# Inner-pocket elbow/contact-view preparation

Baseline evidence: inner_pocket_20261021_091221_5f748865.zip passed runtime and140 image hashes, but contact view was nearly edge-on and left elbow elevated.

## Changes and local verification

- Left elbow pole blend20% toward body-relative(-.30,.12,.20). Across70 poses, elbow lowered28.38–113.18mm relative to the old pose and remains at least20mm below shoulder in body-up coordinates.
- Direct comparison with previous committed provider confirms exact equality for both hand plans/origins, packet positions/basis, all pocket control metadata and right arm in all70 poses.
- Fixed50-bone lengths and wrist-angle/continuity checks pass: maximum wrist angle59.3101degrees (right), maximum frame steps left wrist41.975mm, left elbow40.310mm. No final skin collision claim.
- Inner-pocket cameras use packet-facing body offsets; parked mug excluded from framing, tighter close-up permitted. Actual camera-to-packet cosine must be at least0.8 across the70 evaluated poses. Pure direction checks pass. This gate cannot prove visibility past hands or garment.
- Shape construction regression, Python compilation, film workspace verifier and git diff --check pass.

No Blender/bpy here. New runtime/render/author visual review pending. Same focused command and original source checkpoint;70 poses/140 images, no full-scene bake. No manuscript or checkpoint changes. Previous runtime pass retained as historical evidence only.
