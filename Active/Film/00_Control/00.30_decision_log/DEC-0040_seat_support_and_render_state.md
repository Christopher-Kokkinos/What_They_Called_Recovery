# DEC-0040 — Seat support and render-state diagnosis

Date: 2026-10-11. Authority: author authorised next refinement after v0.17 desktop review.

Decision: adapt bed/seat placement to shared limbs rather than stretching calves. Bed top becomes 0.54 m, seated pelvis 0.65 m; sleeping root/pelvis follows this height and pillow follows bed. Knee pole aligns toward bed side. Keep existing seated ankle positions and standing anatomy/prop targets. Add pure sampled thigh-surface and Blender evaluated clipped-cube clearance checks. These are diagnostic support choices, not final mattress deformation or natural acting approval.

The same nominal SH009 frame crops the head in preview but not the full-resolution still. Code inspection found no intended alternate preview camera/aspect ratio. Exact cause unproven without evaluated state evidence. Add explicit scene update before each render and camera/head/projected-bounds readbacks at matching still/preview frames; record comparison and window containment. Do not silently reframe a camera to conceal an unexplained discrepancy.

Evidence: Reports/Film/2026-10-11_sc001_v018_seat_framing_preparation.md. Desktop and visuals pending; story, notice, no-dose rule, custody and gates retained.
