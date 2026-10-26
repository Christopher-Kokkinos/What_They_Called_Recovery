# DEC-0096 — Front support grip and torso-clearance gate

Author agreed to correction after the joined regrip showed the left arm behind the torso. Diagnosis:2026-10-26_pocket_handover_left_arm_diagnosis.md. This is a real target/solver issue, not a jacket visibility issue.

## Bounded change

Move left support from packet coordinates(-80,-30)mm to the forward edge(+110,-50)mm. Aim its finger axis across/up/slightly forward in body space and solve toward an outward/downward pole. During carry, interpolate from the supporting elbow to the accepted lapel elbow. Remove the previous large lateral pole detour for this bridge. Right regrip, all prop paths and custody timing remain unchanged; only left arm/hand in diagnostic17–156 changes.

Add analytic segment clearance against a body-local elliptical torso core, half-width170mm and half-depth90mm expanded35mm for limb envelope; test heights120–520mm above pelvis. Also require elbow width>=200mm on left and forward>=-20mm during the repair interval. The gate is bounded to the corrected support transition, not all accepted source clips. It excludes shoulder attachment/lower torso and is not final skin/garment collision certification. Minimum ellipse score must be>=1. Apply the same gate to planned poses and evaluated rig bones before rendering.

Local397-pose checks pass: score minimum1.311425, maximum wrist bend60degrees. Explicit recorded legacy posterior-arm fixture is rejected. Frame55 elbow moves from317mm behind shoulder plane to159mm in front, with wrist185mm in front. Source comparison confirms all397 prop paths/right hand and every pose outside17–156 are identical. Blender/readback/visual review of this correction pending. Same --pocket-handover-review;134 images. No acceptance of joined sequence until visual confirmation.
