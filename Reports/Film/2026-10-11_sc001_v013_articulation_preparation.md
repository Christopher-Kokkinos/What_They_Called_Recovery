# SC001 v0.13 opening articulation preparation

Author agreed to proceed from the full-sequence review toward a reusable articulated Elias proxy. This first bounded pass owns opening frames 1–888. It is a segmented diagnostic joint solver, not yet an armature, skinned character or approved performance.

## Implementation

Reusable pure elias_articulation.py supplies reachable two-segment solving and named pelvis/spine/chest/head and leg joints. The Blender adapter keys owned meshes at each source frame for the opening; it resumes the established standing pass at frame 889. Thighs remain 0.60 m and calves 0.64 m rather than changing scale between sleeping and seating. A 0.65 m split spine rises through a staged supine-to-seated transition. Seated ankle targets remain fixed in world space while the existing hips scoot, reducing the earlier foot-slide cause. The lower spine mesh is hidden after the kitchen cut. No new software, asset or add-on required.

Right-hand support now uses fixed two-segment arms at the left rib target for frames 350–750 and approaches the drawer continuously during 750–810, then follows the existing closure. A delayed quadratic hand approach keeps targets reachable while the torso leans. This replaces a horizontal support box and abrupt hand switch. Drawer geometry, medicine label, camera search, exact notice and final outgoing custody remain retained.

## Evidence and limitations

Pure checks PASS across all 888 opening frames for constant leg/spine lengths and fixed seated ankle targets; all support-to-drawer source frames satisfy the 0.70 m arm limit. Existing motion/custody/reach/pivot checks PASS. Automation syntax, film workspace and diff checks PASS. Six helpers are now included in desktop provenance hashes.

Agent has no Blender runtime; integration/rendered pose approval is pending. Dense keys verify source-frame planning, not subframe interpolation. The staged rise is not a physiologically convincing roll; opening arm alignment, knee bend, spine/head alignment, mattress intersections and foot surfaces require desktop inspection. No skinning, twist control, final rib contact, hand grip, clothing, walk cycle or audio is supplied. Existing kitchen-to-exit acting remains coarse. No final performance/pacing gate advanced.

Run full --render-shot-review --render-motion-preview: the focused bedside flag omits the waking transition. Review SH001 sit-up, SH002 planted seated feet/rib support and SH003 hand approach/closure, then check regression of outgoing custody. Generated runs are isolated and retained. No canonical/publication changes; unrelated existing binary modifications excluded.
