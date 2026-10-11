# SC001 v0.7 bed and handling preparation

Root cause: +90-degree lying X rotation sends the mannequin's local head toward -Y; the old seated root Y 2.87 is beyond the bed foot. Reverse X rotation, begin at Y 3.15 and sit at X 2.8/Y 3.8 beyond the bed's +X side, with outward seated yaw. Add a pillow at +Y to make direction inspectable. Author reported the defect; DEC-0029 records the correction and provisional side choice.

Also address reviewed motion readability: revised support-shot eye position, elevated handling camera, near-side symbolic paper/envelope positions at SH008 cut, and coarse palm/reach segments following prop targets. Arm targets transform through the planned root orientation; final custody readback remains mandatory. No source text changes.

Validation: pure motion checks include bed head-direction/sign, side-seat bounds and yaw; Python compilation and film workspace checks pass. Source/spec validation remains required by builder. No Blender runtime here: v0.7 execution, contact readability and occlusion must be assessed on desktop. Prior v0.6 runtime success does not certify this revision. Full preview/stills command is unchanged. No final performance or timing gate advanced.
