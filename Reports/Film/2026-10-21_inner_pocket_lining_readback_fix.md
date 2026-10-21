# Inner-pocket lining readback correction

## Observed failure

Author Blender5.2.2 run at c29b322 failed in sc001_inner_pocket_blender.validate at semantic frame22: Evaluated lining bulge. The run reached the per-frame validation after rig/custody setup, but did not complete the70-frame gate or render review. No ZIP/visual inspection is claimed.

## Bounded correction

Explicit Basis-relative independent controls, with from_mix=False and every coordinate reset from the original grid before adding each deformation. This removes dependence on active/mixed shape creation. Suspected inherited deformation is not conclusively established by the old traceback, which omitted coordinates. Added full evaluated mismatch diagnostics and included the measured lining error in the returned maximum. No tolerance weakened; no movement or custody changes.

## Local evidence

- python tools/verify_inner_pocket_shape_keys.py: PASS for deliberately contaminated initial data/reference and16 independent opening/bulge combinations.
- python tools/verify_elias_inner_pocket.py: PASS,70 poses; maximum wrist angle59.3101degrees; maximum frame displacement41.975mm.
- py_compile, verify_film_workspace.py and git diff --check: PASS.

Construction regression uses a minimal stand-in for the shape-key API, not Blender evaluation. Blender/bpy unavailable locally; evaluated runtime and author visual review pending. Same source checkpoint and --inner-pocket-review invocation; no long full-scene bake needed. Manuscript and source checkpoint untouched.
