# Elias hand mapping preparation

The reviewed SC001 rig run establishes reproducible integer-frame bone/mesh evaluation. The old palm skin was tied to a wrist-origin hand bone while accepted contact boxes use offsets and task-specific orientation. That prevented exact transfer of drawer/shower/paper palm targets.

New pure elias_hand_math module exposes the accepted palm boxes and five-digit fixed-length chains with bounded task curls. Hand rig heads map to palm centres; forearms stay on the original wrist targets. Adds 30 phalange bones and closed finger skin tubes. Shared constructor remains used by gallery and scene. Blender scene tester reads the weighted palm centroid at all 3,168 source frames; twelve dedicated close-ups prepared. No source timing, camera sequence, prop custody or character relationships change.

Validation: pure rig contract PASS across 3,168 frames: 48 bones, 1,884 vertices, 2,304 faces, 42 closed components; normalized weights, outward winding, fixed lengths and exact planned palm origins. Python compilation PASS; film workspace verifier PASS. No Blender execution locally; evaluated palm-centre readback, finger collisions, grip visuals and continuous playback pending. Curls are provisional author-review choices, not proof of grasp. Remaining wrist/shoulder/hip topology seams explicitly retained for later refinement.
