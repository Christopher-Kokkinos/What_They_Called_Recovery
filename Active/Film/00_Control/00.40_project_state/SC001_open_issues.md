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
