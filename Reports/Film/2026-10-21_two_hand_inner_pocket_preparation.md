# SC001 inner-pocket replacement preparation

Diagnosis from author: prior rigid pocket insertion lacked the off-hand opening the jacket and did not look right. No new ZIP was supplied with this correction; do not claim a visual inspection of an unseen failed render. Prior test is not accepted.

Implemented separate pure movement provider and Blender jacket/custody module.70 semantic poses,140 images, normal context plus labelled lapel/lining cutaway. Left lapel grip, right thumb/index/middle grip,45-degree lower-edge entry, slight forward lean, release44, index drag, upward hand clearance and controlled settling. Lapel and lining are deformable grid patches, not complete garments. Original envelope meshes remain rigid; bending is deferred until contact is verified.

Local deterministic checks pass: fixed50-bone lengths, connected anatomical geometry, max wrist angle59.32 degrees; max per-frame left wrist41.98mm/elbow37.85mm, right wrist28.12mm/elbow16.78mm. Left actively holds opening during21–40; envelope seated against pocket floor from40; custody changes on44; hand-relative packet transform constant before switch. Settling includes a damped overshoot. py_compile, verify_film_workspace.py and git diff --check pass.

Blender is unavailable locally. Runtime gates check all finger targets, evaluated lapel attachment/pad gaps, actual lining bulge, pocket support, all prop transforms/influence and handoff half-frames. These gates have not run here. No full skin/clothing collision, final timing or boundary integration pass claimed. Source checkpoint and manuscript unchanged.
