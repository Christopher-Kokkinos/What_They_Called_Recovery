# SC001 open production issues

Author will flag remaining concerns from personal notes before moving beyond SC001. Reconcile those notes with this list; do not close an issue solely because automation completes.

| Issue | Status / closure evidence needed |
| --- | --- |
| Shared anatomy, seat and floor support | v0.17 desktop verifies one 0.50/0.52 m leg pair and leg attachment across 2760 frames; standing pelvis 1.02 m. v0.18 evaluated thigh clearance passes (minimum 3.24 mm); soft support, weight transfer and final mattress contact remain open. |
| Standing head framing | v0.18 SH009 preview head clearance restored; matching still/preview states agree at all ten shot starts. Earlier crop cause not retrospectively proved; final composition remains reviewable. |
| Injured sit-up, pain and support acting | Coarse staging verified in v0.14; natural roll, weight transfer, restraint and expression pending. |
| Drawer/palm and body contact | Joint attachment verified for opening; rendered grip, intersections/subframes pending. |
| Coffee handle/sip contact | v0.16 sampled cup lift/return visible and evaluated wrist targeting passes; fingers, tilt and convincing sip/face contact pending. |
| Folding and jacket pocket | v0.19 desktop verifies packet bounds inside opaque torso across 541 frames; sampled concealment visible. Final jacket pocket, cloth, entry contact and grip remain open. |
| Exit contact and pace | v0.19 route speed 0.98 m/s and floor/stance checks pass. Elias leaves view early, creating roughly 6–7 seconds on room; v0.20 desktop verifies tracking containment across 240 frames; sampled arrival and pigeon cut readable. Natural injured gait and final camera performance remain open. |
| Entry opening and outside floor | v0.21 failed evaluated left-forearm clearance at frame 2787; v0.22 exit elbow-pole correction prepared with volume regression. v0.22 then stops at conservative parked-leaf AABB overlap frame 2791; v0.23 oriented-box classification prepared. v0.23 reaches mug clearance failure at 2794 (-249 mm). v0.24 body-relative carry/grip and complete prop-volume regression prepared; evaluated passage, parked leaf and sole support remain desktop-pending. Door handle/opening/closing performance remains open. |
| Full scene pacing | 120-second silent sample hypothesis (v0.19 adds five seconds to exit); timed playback/dialogue review pending; reaching two minutes does not pass the finished-slice gate. |
| Dialogue, sound, pigeons and final look | Production pending; no final lighting/grain/audio certification. |
| Author notes and scene acceptance | Reconcile before SC002; acceptance must be explicit. |

Reports and decision logs retain evidence and superseded failures. Last update: v0.26 split coverage preparation; no finished-slice gate passed.

## Author review received 2026-10-14

V0.26 rendered successfully but is visually unaccepted. The actionable register AR01–AR17 in [Reports/Film/2026-10-14_sc001_v026_author_review.md](../../../../Reports/Film/2026-10-14_sc001_v026_author_review.md) supersedes optimistic closure interpretations above. Anatomy, apartment layout, prop scale/contact and two-handed paper handling remain open; exit camera direction is liked, clock style deferred. See DEC-0049. No scene or finished-slice acceptance.

AR13–AR14: independent static room-layout proposal prepared under DEC-0050 (14 × 12 m, four rooms). Pure layout checks pass; desktop runtime/author review pending. Neither issue is closed; original animation and all anatomy/contact defects remain open.

AR01–AR16 correction pass implemented as connected-room performance preparation (DEC-0051); full-frame pure geometry regression and desktop evaluated-frame checks distinguish preparation from visual closure. See new report. Clock style stays deferred; initial envelope opening, natural acting, final skin/finger grips and door operation remain open. AR17 camera intent retained, reframed render review pending.

Author review of connected-room pass: major posture/support accepted conditionally, with frame 1213 right-arm graphical glitch outstanding. Letter hold length, furniture and minor posture/visual refinements explicitly deferred. Confirmed opaque-water/upper-arm intersection corrected in render setup; actual frame image and rerender review pending. This does not close the finished-slice gate.

Frame 1213 opaque-water overlay: CLEARED by targeted desktop review (Reports/Film/2026-10-14_sc001_shower_targeted_desktop_review.md); source hashes and runtime readback match. No full motion re-review inferred. Cold diagnostic label cleanup remains part of deferred visual polish. Author mechanical/posture pass is scoped; scene completion remains open.

## 2026-10-15 mug/table/posture correction — DEFERRED (DEC-0070)

Author passes bounded mug contact-cycle motion for this stage, flags telescopic mug and crouched reach. Restore original180 mm body (remove20 mm diagnostic extension), raise table and coordinate its letter/envelope/keys/chair contacts and both mug pickups. Reduce knee bend, use small forward lean from upright stance. Height/lean targets pending coordinated solve;20 mm initial support discrepancy alone does not determine desired working height. Keep this open through later layout/posture pass. Second-pickup review retains original checkpoint body/table and known support gap; no support acceptance. Final wrist seam/skin contact and keys pinch/immediate pocketing remain open.

2026-10-15 DEC-0071: Source1561 crouch-to-stand pop corrected in integrated target preparation, not yet Blender/visually passed. Review boundaries and consistent connected-left-wrist convention before full-scene bake. Table height, original mug/body support, upright working reach and skin/contact polish remain open.

2026-10-15 DEC-0072: Integrated boundary test FAILED55.005 mm rigid palm mapping; opt-in independent left palm control/weights prepared. Pure centroid mapping regression added, desktop evaluated skin rerun pending. Do not close from bone targets alone.

2026-10-15 DEC-0073:55 mm palm mapping defect CLEARED in175-frame integrated boundary readback (0.00996 mm maximum under0.1 mm gate). Whole-scene3168-frame runtime remains pending. Initial reach partly body-occluded, clearance not established. No final scene pass.

2026-10-16 DEC-0074: Overnight full-scene orientation FAILED1.4142; invalid parked basis in sleeping segment diagnosed. Stable table basis/preflight and earlier rig diagnostic save prepared. Pure basis checks pass; full evaluated Blender rerun pending. Rig function gates completed but no numerical report/checkpoint survived that run.

- DEC-0075 trial: raised table/original mug and upright reach prepared; two clips only. Paper/key contact, chair/table relationship and continuous scene promotion remain open.

- DEC-0076: resting-arm revision prepared; author visual confirmation pending. Cup arm retained exactly in contact intervals; keys pinch/pocket remains open.

- DEC-0077: author clarified elbow behind wrist. Forward-elbow requirement replaced; revised resting pose prepared, runtime/visual confirmation pending.

- DEC-0078: second table reach author accepted. First lift mug/torso collision correction prepared; first-only preview/runtime and visual confirmation pending.

- DEC-0079: first-only support check incorrectly visited unbaked second-clip frame2400; scope corrected and schedule regression passed. Same first-only rerun required.

- DEC-0080: both table reaches author provisionally accepted; hand/outer-thigh collision non-blocking and open. Paper pickup/fold contact diagnostic prepared (100 poses/68 images); runtime/visual review pending, insertion/pocketing next.

- DEC-0081: author anatomical guidance incorporated. Supported paper regrip prepared (120 poses/82 images); initial folded-hand roll remains pending runtime/visual correction confirmation. Envelope opening/insertion/pocketing follow; left stabilises/right manipulates.

- DEC-0082: envelope opening/insertion diagnostic prepared (160 poses/108 images). Fold remains working blockout; mechanical pause and crease press open. Envelope runtime/visual check, transition, pocketing and coordinated scene retiming pending.

- DEC-0083: wrong-side opening elbow correction prepared; 60-pose/42-image opening-only preview available. Later insertion targets unchanged; visual confirmation, withdrawal and occlusion remain open.

- DEC-0084: opening elbow author stage pass recorded. Insertion inspection/staged withdrawal prepared (110 poses/76 images, normal+labelled cutaway). Fingertip/withdrawal visual review, pocketing and integration remain open.

- DEC-0085: insertion ZIP runtime/hash checks and Codex blockout review passed; author acceptance pending. Closure/handover/pocket-approach diagnostic prepared (181 poses/122 images). Blender/visual review and clothing-pocket release pending; full sequence retiming remains open.

- DEC-0086: finish ZIP technical record and122 hashes passed; visual pass held for raised right elbow. Body-relative pole correction prepared; hand/packet targets unchanged across181 poses. Height/continuity gates pass; rerender/author visual review pending. Pocket fit/release and full skin collision clearance remain open.

- DEC-0087: author provisionally accepted corrected envelope finishing for blockout. Continuous paper diagnostic prepared (602 poses/204 images), including supported set-down/envelope pickup. Envelope restaged180mm nearer; release elbow continuity corrected without changing reused hand/prop paths. Runtime/visual review, pocket release and full-scene retiming pending.

- DEC-0088: joined paper ZIP runtime/hash checks passed; two author-authorised refinements prepared:10-frame regrip and direct32-frame transfer to flap.560 poses/190 images, local checks pass. Blender/visual review pending; pocket release, fine contact and full-scene retiming remain open.

- DEC-0089: author provisionally accepted refined paper blockout. Mug/paper handover diagnostic prepared:772 connected poses,172 images across two handover windows. Mug supported during paper; envelope remains held in right hand for second pickup. Local checks pass; Blender/visual review, pocket release and complete-scene retiming pending.

- DEC-0090: handover ZIP technical/hash checks passed; Codex provisional blockout recommendation. Pocket proxy insertion/release prepared (221 poses/150 images), with floor support and outward hand withdrawal. Local checks pass; Blender/visual review and full sequence integration pending. Temporary pocket is not final clothing.

- DEC-0091: author rejected rigid outer-pocket motion. New two-hand inner-jacket test prepared: lapel pull/lining bulge, bottom-first45-degree insertion, Child Of switch44, upward withdrawal and settling.70 semantic poses/140 images; local math passes, Blender/visual checks pending. Prior pocket not accepted; integration and envelope flex remain open.

- DEC-0092: frame22 evaluated lining mismatch blocks inner-pocket runtime pass. Independent shape construction prepared; exact evaluated gate retained, rerun required before rendering/visual acceptance.

- DEC-0092 desktop evidence:70-pose runtime and140 image hashes pass. Visual hold: packet edge-on in cutaway, off-hand elbow elevated; clearer contact framing and bounded posture refinement next. See Reports/Film/2026-10-21_inner_pocket_desktop_review.md.

- DEC-0093: lower off-hand elbow and packet-facing focused cameras prepared; all70 hand/packet/control targets unchanged. Local checks pass; rerender --inner-pocket-review for new runtime/visual confirmation.

- DEC-0094: new ZIP runtime/hash checks pass but foreground scenery blocks both views; visual hold. Labelled environment-isolated diagnostic views prepared with all-frame visibility preflight. Same focused rerun required.

- DEC-0094 isolated desktop ZIP:70-pose runtime/140 hashes pass; foreground obstruction resolved. Codex recommends provisional movement-scaffold pass, author acceptance pending. Detached jacket panels, low pocket staging, fine skin contact and integration remain open. See Reports/Film/2026-10-21_inner_pocket_isolated_desktop_review.md.

- DEC-0095: author accepted inner-pocket movement provisionally.397-pose paper→supported regrip→pocket→second mug joins prepared;134 sampled images, --pocket-handover-review. Local checks pass; Blender/visual review pending. Low pocket/garment/fine contact limitations remain open.

- DEC-0095 desktop ZIP:397 planned-pose checks and134 image hashes pass, but new left support/regrip runs behind torso (frame55 elbow317mm posterior). Author concern confirmed in cutaway. Joined visual pass held; restage grip/arm in front and add torso-clearance gate. Accepted standalone pocket remains provisional pass. See Reports/Film/2026-10-26_pocket_handover_left_arm_diagnosis.md.

- DEC-0096: supporting pinch moved to forward packet edge; left elbow/wrist now in front.397-pose local regression and analytic torso-proxy gate pass; legacy posterior fixture rejected. All prop/right-hand paths and poses outside17–156 unchanged. Same --pocket-handover-review runtime/visual rerun pending.

- DEC-0096 follow-up: desktop run failed because SUPPORT_EDGE was erroneously passed as ninth custody argument. Explicit scheduling options and actual-call signature regression pass locally; same focused runtime/visual rerun pending. See Reports/Film/2026-10-26_custody_argument_interface_fix.md.

- DEC-0096 desktop review:397-pose runtime/134 hashes and140-pose evaluated torso gate pass (minimum1.311426). Posterior supporting-arm route resolved visually; Codex recommends provisional blockout pass, author acceptance pending. Garment fit/low pocket/fine contact and whole-scene integration remain open. See Reports/Film/2026-10-26_front_support_join_desktop_review.md.
