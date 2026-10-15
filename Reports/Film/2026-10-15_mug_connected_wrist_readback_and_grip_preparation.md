# Mug wrist readback and grip refinement

mug_20261015_132729_ad171f13 ZIP inspected: six closeups and six arm-context images; evaluated six-pose wrist gap <=1.519626234e-7 m, palm error <=2.198918670e-6 m, endpoint error <=1.190928173e-6 m. Author reports massive improvement. Visuals support connected arm/wrist baseline; finger/thumb wrap and surface seam unfinished. No continuous motion acceptance.

Prop selection incorrectly framed distant letter for 1460/1500; corrected using mug experiment marker. New target solver works in mug lateral/forward coordinates, opposed finger/thumb rail sides, reachable heights. Three fixed phalanges with non-collinear distal bend replace generic curls. Residuals recorded; six review frames reach five targets to pure tolerance <1e-8. Transition clamps remain explicit and are not a contact pass. Wrist sleeve unchanged; seam remains open.

Validation: 246-frame pure connected-chain/length/root/mug-path regression PASS; six review-pose target assertions PASS; Python compilation and film workspace verifier PASS; diff check PASS. Blender skin/grip/occlusion and continuous motion pending. Preserve prior body improvement; no paper/dial/key changes yet.
