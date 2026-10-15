# DEC-0069 — Mug approach, grip formation and release

2026-10-15. Author explicitly passes DEC-0068 motion at this stage and requests next work. Acceptance limited to first lift/drink/return interval1400–1539, not final surface contact/scene.

Input mug_motion_20261015_170307_3152dd5d.zip:48 image hashes match, all48 frames inspected in ordered galleries.140 Blender rig/mug frames pass; wrist gap3.69837095e-7 m, endpoint1.52345700e-6 m, mug position error0, basis error1.37451841e-7. No obvious gross detachment/flip in wide sequence; fine hand contacts unresolved.

Add separate elias_mug_lifecycle wrapper and --contact-cycle mode, retaining passed state exactly1400–1539. Bound1375–1560 (186 frames). Approach translates palm from90 mm outward/25 mm back, smoothsteps to contact1390; finger fan closes1387–1400. After placement1540, fingers open through1550; hand withdraws1550–1560. Thumb opposes fan; lower pair rotates down at fixed bases to clear sloping return. Fixed phalange lengths and connected wrist retained. This is a bounded prototype, not a splice into surrounding scene animation.

Placement diagnosis: source cup centre880 mm, original body half-depth90 mm => bottom790 mm; table top770 mm. Copy-only body becomes200 mm deep centred z=-10 mm locally, preserving top+90 mm, handle and passed rig/mug transforms while lowering bottom20 mm. Source checkpoint/builder unmodified. Adds evaluated vertical support checks at1375/1400/1540/1550/1560 and mathematical footprint bound. Revised silhouette remains provisional.

Render48 images640x360 at six samples/sec plus four1280x720 contact stills1387/1399/1544/1550. Same fixed-camera HTML player; mug_cycle_ output saved before render. Existing14-still and first-drink modes retained. Runtime records lifecycle opening/clearance and source hashes.

Pure186-frame lifecycle contract PASS: passed interval equality, lengths, wrist, source mug/root/basis, table support/footprint, rail clearance and transition bounds. Max wrist step39.107 mm (includes passed lift), elbow30.558 mm. Pure246-frame mug regression/workspace/compilation/diff PASS. Blender evaluated186-frame readback, support, skin/contact and visual naturalness pending. Wrist seams, whole-scene integration, later carry and other prop tasks remain open.
