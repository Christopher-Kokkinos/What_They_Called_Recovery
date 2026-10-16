# DEC-0078 — First mug lift torso clearance

Author accepted second table reach from table_reach_20261016_073841_cf6c2f68.zip. First reach remains open: mug collides with torso during lift. Inspection of lift samples confirms path runs too close to upright torso after stance moved forward220 mm.

Correction: first lift/return1400–1540 only, translate mug and entire left gripping hand forward by280 mm times existing smooth lift amount. Re-solve fixed-length arm. Resting table endpoints and mug dimensions unchanged; second reach unchanged. Grip geometry, timing and posture unchanged. Pure conservative separating-plane check projects original60 mm radius/90 mm half-height mug cylinder and full-depth125 mm torso half-box onto torso forward axis; require greater than10 mm separation at every integer frame. This is a proxy body-clearance proof, not evaluated full-skin/handle/head collision certification.

Optional --first-table-reach-only with --table-reach-review selects1369–1600:232 baked poses,78 images. Retain353-pose pure verification across both clips. Numerical checks pass; Blender and author visual confirmation pending.
