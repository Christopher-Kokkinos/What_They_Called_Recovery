# Overnight full-scene orientation failure

Author output: ea1f667, Blender5.2.2;3168-frame rig bake/readback progress reaches3120 then returns to caller, failing mug basis_error1.4142136466667896. Function control flow establishes rig gates completed; numerical rig report was only in process memory. Failure occurred before any checkpoint/render save. Original source .blend untouched, failed output directory may remain. No claim of recovered overnight bake.

Diagnosis independently reproduces invalid legacy parked basis at sourceframe1: body lateral and fixed ground_forward are parallel. These are not unit orthogonal right-handed rotation axes. Exact maximum-error Blender frame was absent from original message, now diagnostics add it. Fix stationary mug axes to kitchen table basis; preserve held orientation, paths, hand targets and timing.

DEC-0074 adds strict proper-basis and Euler round-trip preflight before expensive rig work, then a diagnostic .blend/status after rig checks but before prop readback. Normal validated save still requires rig and mug pass. Numerical gates remain unchanged; no collision/physics/scene pass inferred.

Validation: verify_elias_mug_integration.py PASS3168 frames,49 bones,0 predicted palm error; proper rotation gate at every frame and explicit rejection of legacyframe1; original55 mm palm regression still reproduced. verify_elias_mug_contact.py PASS246 frames. Compilation, workspace and diff checks PASS. Actual Blender conversion/evaluated orientation rerun pending. Repeat original --full-scene-review command after pull; script will fail early if basis/Euler preflight fails. Original input and canonical files unchanged.
