# Elias diagnostic anatomy contract v0.1

Status: shared fixed-length proxy prepared; not a final armature, skin or accepted character model. Dimensions inherit v0.26 and are production hypotheses, not novel measurements.

| Element | Length / size |
| --- | --- |
| Upper arm / forearm | 0.36 / 0.34 m |
| Thigh / calf | 0.50 / 0.52 m |
| Spine | 0.65 m, two equal mesh sections |
| Upright hip / ankle height | 1.02 / 0.10 m above support |
| Neck | 0.10 m proxy |
| Head | 0.28 × 0.25 × 0.30 m |
| Elbow flexion ceiling | 160° provisional diagnostic limit |

Source dimensions: `elias_articulation.py`. New shared bend solver and world transforms: `sc001_room_performance.py`. The elbow pole favours the hip and modest outward bias; reach, bend direction, flexion and basis handedness are checked separately. Bones do not stretch. Lower pelvis during a lean is a bent-knee stance, not shorter legs. Palm boxes represent different grip orientations; they are not a finished hand model.

The body right vector is `(forward_y, -forward_x, 0)` for horizontal forward. Torso up follows lean, and body forward is rebuilt perpendicular to right and up. Ground direction stays separate for props, foot support and route. Orthonormal box transforms are shared by Python checks and Blender meshes, avoiding reflected bases or independent pose reconstruction.

Sleeping shoes remain fully within the bed footprint with their lowest point on the mattress. Side-seat knees/feet extend beyond the mattress; pelvis and supported thighs remain over the bed. Rise is a coarse staged movement, not a finished physiological roll or soft-body contact simulation.

Run `python tools/verify_sc001_room_performance.py` for full source-frame checks. Blender evaluated-mesh checks and author review remain required.
