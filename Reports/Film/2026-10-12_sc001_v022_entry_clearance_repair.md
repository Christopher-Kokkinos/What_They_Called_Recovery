# SC001 v0.21 failed entry check; v0.22 carry-pose repair

Author supplied Blender 5.2.2 LTS traceback from commit 940583f. Entry validation failed CHR_Elias_left_forearm at frame 2787, before saving/rendering. No successful v0.21 desktop run or visual acceptance is inferred.

## Root-cause reproduction

Route alignment and sole coverage are insufficient to bound carried-arm geometry. A pure segmented-box reconstruction using the fixed-length joint plan and Z/Y segment basis reproduces negative left-forearm clearance on the reported frame. Old planned margin approximately -0.052523 m: the forearm crosses the entry depth early while its extended forward elbow remains left of the opening. This reproduces the type/frame of failure; the exact evaluated Blender point was absent from the original error message, so the numerical margin is a pure reconstruction, not a measured desktop value.

Exit elbow pole now uses 0.1 m forward plus 0.4 m lateral bias and 0.5 m downward bias, replacing the old 0.7 m forward pole. Both carry elbows use this exit-only bend rule. Hand targets, arm lengths, opening, route, timing and camera retained. Earlier medicine/coffee/pocket poses are unchanged. This is a provisional carry-pose judgement requiring render inspection, not final injured acting.

## Checks

A new regression clips both upper-arm/forearm proxy box volumes to the entry slab across the final segment. It explicitly reproduces the old frame-2787 failure and passes revised poses, minimum planned margin 0.041686 m. Clipped-box logic is shared with the Blender entry validator. Actual Blender errors now include object, frame, point and margin. Evaluated clearance/support assertions remain strict.

All existing pure anatomy/reach/packet/stance/seat/camera/support-plan checks PASS. Film workspace, AST syntax and diff checks PASS. Blender execution, parked-door overlap and built support remain pending. Last successful desktop evidence stays v0.20. No publication prose or final gate changes.

Rerun full --render-shot-review --render-motion-preview. If it completes, provide complete ZIP; inspect forearm passage, carry silhouette, body contact, floor/landing and camera cut. If it stops, supply traceback with the new contextual point/margin. Prior failed run can remain; outputs use a fresh directory.
