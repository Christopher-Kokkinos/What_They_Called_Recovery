# SC001 v0.25 departure camera preparation

Author authorised addressing parked-leaf occlusion and late scale widening after v0.24 verified physical passage/support.

## Root causes and change

The prior camera only checked projected subject bounds, so an intervening door could cover Elias. It independently refitted each frame; adding doorway bounds late caused a visible scale change. New helper configuration separates candidate viewing-angle selection and scale fitting from final key insertion.

For each candidate tracking offset, evaluate all source frames through arrival. Check projected full-body/prop containment and orthographic rays toward head/torso, forearms/palms and complete mug/key assemblies. Rays originate on the camera plane and travel parallel to camera direction; door/leaf/jamb/lintel ray casts account for object scale. Sample centres and eight bounding corners. First blocked frame/subject/structure recorded. Stop candidate on blockage; fail build if none clears. Front/right offsets tried first, higher angles available as diagnostic fallbacks.

Collect maximum required scale for each phase across all frames, then key that constant scale for every tracking frame. Pigeon phase has its own fixed scale and existing hard cut at 2841. Final pass rechecks containment and sampled structural visibility. Record trials, selected offset, phase scales, sampled-ray count and frame checks. Geometry, root motion, carried targets, 120-second duration and prop custody retained.

## Verification and limits

Pure candidate-pose/cut invariants and all existing geometry/reach/custody/support regressions PASS. Film workspace, AST syntax and diff checks PASS. No local Blender runtime; candidate selection, ray checks and real composition desktop-pending. Sampled bounds/centres do not certify every rendered pixel or body self-occlusion. A higher angle may clear geometry yet need artistic revision. Constant scale removes the identified automatic zoom, not all possible camera-performance issues.

Run full --render-shot-review --render-motion-preview; upload complete ZIP. Review approach around door, mug/key readability, actor size throughout tracking, arrival composition and pigeon cut. Check entry/support assertions remain passing. Last verified desktop v0.24; no final gate or publication prose changes.
