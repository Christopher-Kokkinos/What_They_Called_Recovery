# First lift collision correction

Author: second reach correct; first mug lift intersects torso. Inspected first-lift samples1399,1429,1444,1459,1474,1498. Root cause: original mug trajectory retained after forward stance change. Forward offset tied to existing smooth lift, with hand translated identically, corrects first lift/return only.

verify_elias_table_reach.py PASS353 poses including conservative mug-cylinder/torso-box separation >10 mm throughout1400–1540, fixed limb/finger lengths, resting elbow direction, table support and wrist continuity. Python compilation, film workspace and whitespace checks PASS. No local Blender runtime. Author second reach accepted; first visual review pending. First-only render option78 images,232 baked/readback poses. No whole-scene pass.
