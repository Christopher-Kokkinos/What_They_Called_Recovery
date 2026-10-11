# SC001 v0.18 seat support and framing investigation

Author authorised proceeding on seated support and SH009 still/preview discrepancy.

## Seat diagnosis and implementation

Shared 0.52 m calves are incompatible with nearly horizontal thighs at the old elevated seated pelvis (0.85 m) and floor ankles (0.10 m); knees cannot remain at hip level and reach those ankles. Solving reach alone angled thighs down into the old 0.70 m bed top. Bed top now 0.54 m and seated pelvis 0.65 m; sleeping pelvis/root and pillow lower with the bed. Knee pole points toward the bed side without the previous diagonal lateral bias. Shared thigh/calf/arm/spine lengths and standing pelvis remain unchanged. Seated ankles stay planted and the drawer target stays fixed; opening arm reach rechecked across every frame.

Pure cross-section sampling across seated frames 350–888 passes, minimum thigh-surface clearance approximately 0.00354 m. This improves clearance but is not final soft contact or mattress deformation. Blender now clips evaluated thigh cube vertices/edges at the bed-side plane and checks minimum surface clearance throughout seated frames. Feet and shared anatomy assertions retained. Sleeping/pillow placement and actual support must be visually reviewed.

## Framing diagnosis and instrumentation

V0.17 SH009 full-resolution still has head clearance but matching preview crops head top. The source selects the same camera and frame, with matching 16:9 aspect ratios; an intentional alternate composition was not found. No Blender runtime is available here to reproduce evaluated render state, so a precise root cause cannot honestly be asserted.

V0.18 explicitly updates the view layer after frame/camera selection, before both render routes. It records evaluated camera/head matrices, lens and normalised projected head bounds at each still and preview shot start. Matching source frames report maximum state difference and whether states match. All window preview samples record containment. This provides evidence for a state mismatch versus an image-render discrepancy; it does not claim the crop fixed. No camera move made solely on the prior mismatched outputs.

## Validation and desktop gate

All-frame pure anatomy/reach/custody, sampled linear prop interpolation, stance/floor targets and sampled thigh clearance checks PASS. Film workspace, Python syntax and diff checks PASS. Blender evaluated thigh clearance and render state instrumentation remain desktop-pending. Use --render-shot-review --render-motion-preview, retain full ZIP. Inspect opening feet/pillow, thigh support, drawer reach and window framing; include validation.json so the state comparison can be audited.

Pocket concealment, brisk exit and injured acting remain open. Timing, exact notice and canonical publication prose retained. No scene acceptance or finished-slice gate advances.
