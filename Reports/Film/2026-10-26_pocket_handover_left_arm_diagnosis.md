# Joined pocket handover: left-arm visual failure

Author observed an apparent wrong-way arm bend and asked whether jacket concealment explains it.

## Evidence

ZIP pocket_handover_20261026_091059_1db57a8a.zip, SHA256e09c4382167dd8404bd66482750d055b469b3a5425c532c7cbfaa206b2d65780. Runtime report passes397 planned poses, constraint boundary samples and support/shape gates. All134 PNG hashes match. Reviewed all134 poses in chronological contact sheets and full-resolution cutaway source43/109/121.

The cutaway hides the jacket panels, yet the left arm remains hidden behind the torso during the new support/regrip/carry transition. This is not merely jacket concealment. Planned left elbow body-forward coordinates: frame31=-.224m,43=-.299m,55=-.317m,97=-.317m,115=-.309m; frame55 wrist=-.081m. Coordinates are relative to pelvis in the torso frame; shoulder lies at forward0. These are reproduced from the source provider, not fresh Blender measurements. Uploaded rig readback reports matching those planned endpoints to micrometre tolerance.

## Diagnosis and disposition

Visual FAIL/HOLD for the new joins. This does not revoke the separately accepted70-pose pocket action; the faulty support/regrip precedes it. The support wrist target is behind the torso plane and the hand-axis-biased elbow solve selects a posterior elbow. Later the elbow swings outward to the pocket pose. Fixed bone lengths, wrist angle and small frame steps do not establish an anatomically valid or collision-free arm route. The technical pass was accurate for target readback but incomplete as a posture gate.

Required correction: restage the supporting grip and its approach in front of the torso, then choose an outward/downward elbow path. Check arm-segment clearance from the torso as well as elbow branch/continuity; moving the camera or hiding more geometry would not solve this. Preserve packet support through regrip and accepted pocket/mug endpoints. New poses must be locally checked and rendered before any join pass. No production code changed in this diagnostic review; no new render requested yet.
