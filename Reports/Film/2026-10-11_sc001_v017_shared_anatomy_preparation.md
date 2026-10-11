# SC001 v0.17 shared anatomy preparation

Author authorised unifying Elias's anatomy. The v0.16 desktop review identified different opening/later thigh/calf lengths. This pass removes the duplicated limb dimensions and adjusts dependent placement together.

## Changes and judgement calls

The shared pure articulation module supplies 0.50 m thighs, 0.52 m calves, 0.65 m spine and existing 0.36/0.34 m arms. Opening and standing solvers now use the same lengths. The leg pair is a provisional diagnostic choice: it accommodates the existing seated floor targets and a plausible taller standing placement without retaining the oversized opening lengths. It does not assert canonical height or final anatomy approval.

Standing pelvis rises from 0.75 to 1.02 m; head centre becomes 1.92 m. Seated pelvis remains 0.85 m and existing planted ankles remain outside the +X bed side. Sleeping ankles move from Y=4.70 to 5.00 to remain reachable with the shorter legs. Opening hip scoot, medicine target and no-dose action retained. Knee centres remain outside the bed side after seating; this centre-based check does not certify the full thigh mesh against the mattress.

Body-relative drinking mug, carried mug/keys, pocket, jacket and shower wrist targets rise by the same 0.27 m. New standing offsets are centralised in sc001_motion.py and used by prop animation, pure checks and outgoing readback. Counter surfaces/prop resting heights remain unchanged. A first reach check caught the old outgoing key height exceeding arm reach after the pelvis change; target adjustment resolves it without stretching arms or clamping targets.

The desktop adapter now checks evaluated thigh/calf lengths and hip/knee/ankle endpoints across every source frame, alongside existing arm attachment and floor checks. Validation records shared dimensions, checked frame count and maximum errors. Builder v0.17 retains isolated output directories and explicit action interpolation.

## Verification and limits

python tools/verify_sc001_motion.py PASS: all 2760 frames share leg/spine dimensions; pure arm reach including sampled linear prop curves, planted seated ankles, exit stance/floor targets and outgoing custody pass. Sleeping ankles lie on the bed plan and seated knee/ankle centres lie beyond its side. python tools/verify_film_workspace.py, automation AST syntax and git diff --check PASS.

No Blender runtime exists in the agent environment. Evaluated mesh assertions, visual mattress support, proportions, hand contact and camera framing await Blender 5.2.2. Last successful desktop evidence remains v0.16. Full preview is required because standing height affects every later shot. Pocket concealment, brisk exit and natural injured acting remain open, not solved by anatomy unification. Exact notice, story beats, shot duration and canonical publication prose are unchanged. No finished-slice gate advances.

Run --render-shot-review --render-motion-preview and supply the complete run archive. Prioritise waking feet, seated thigh/mattress support, head framing in later shots, coffee height, paper/key reach and exit leg attachment. Record author notes before SC002.
