# SC001 v0.23 mug clearance failure; v0.24 carry repair

Blender 5.2.2 LTS traceback supplied by author: PRP_CoffeeMug frame 2794, point (5.5510001183,0.1159996018,1.3199999332), margin -0.249 m. Build fails before save/render. Earlier conservative parked-leaf stop is no longer the first failure; this does not establish passage/support success for the complete run.

## Diagnosis

Reported point agrees with old analytic world-offset mug path at that frame. Body facing changes on exit, but mug, keys and jacket offsets/assemblies remained world-aligned. The mug therefore leads into the opening left of the body. Arm-only and root/sole tests omitted prop extents and could not catch it. The opening assertion correctly stopped the invalid placement.

## Changes

Exit carry position/vector functions follow body yaw; outgoing mug, keys and jacket rotate consistently. Mug moves 0.10 m inward in local body X (-0.40 to -0.30), keys 0.10 m inward (+0.35 to +0.25). Mug/key parent groups rotate about their original prop references while translating to planned positions, preserving assembly dimensions. Evaluated mug grip follows its matrix instead of adding a fixed world offset. Exit elbow poles adapt to the revised wrists; arm lengths retained. Jacket follows facing, and packet concealment remains on its existing body-relative path. Earlier coffee/folding timing and pose targets before exit retained. Final custody readback uses shared carry positions.

## Expanded validation

Pure clipping now sweeps cup bounds, all three handle boxes, key ring/shafts/teeth and jacket across every final-segment frame, alongside arms. Expanded test caught a key-tooth margin failure before inward placement was finalised. Revised complete-prop minimum margin 0.066051 m and arm minimum 0.068913 m. Parked-leaf oriented-box tests pass for planned arm/prop assemblies. Runtime entry validator now includes all mug handles and individual key parts rather than only central objects.

Existing reach/anatomy/packet/seat/stance/camera/support-plan regressions PASS; film workspace, AST syntax and diff checks PASS. Blender evaluated geometry and images remain pending; no local runtime. Last successful desktop v0.20. No assertions removed, opening enlarged, route/timing changed or custody roles altered.

Run full review command. Inspect facing transition, hand-to-handle/key contact, body/prop clearance, landing support and pigeon cut. Carry transition is still diagnostic and may need smoothing/natural acting. If any assertion fails, send complete contextual traceback. If successful, send whole ZIP. No final gate or publication prose changes.
