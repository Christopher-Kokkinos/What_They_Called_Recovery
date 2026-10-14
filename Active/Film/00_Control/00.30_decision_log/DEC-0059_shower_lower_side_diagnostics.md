# DEC-0059 — Lower side shower diagnostic coverage

2026-10-14. Checkpoint rig_scene_20261014_204455_57a2b099.zip contains blend, validation and three drawer stills. Twelve-pose readback passes: endpoint error 1.169385180e-6 m, palm error 6.676784499e-6 m. Four stored source hashes match current geometry/targets with CRLF accounted for. It is diagnostic snapshot coverage, not complete motion validation.

Filtered rays still fail shower with maximum two of six visible probes. All original eight candidate cameras had positive vertical offsets. Pure source fingertip targets at 1213 include index/middle/ring below the tap block bottom Z=1.04 m; above-to-contact rays meet actual controls first. This is a diagnostic view-space gap, not proof that the control mesh or finger skin is correct. Palm-centre self-occlusion is also possible.

Add four lower side candidate offsets, retaining render-visible evaluated BVH, existing above-angle candidates, four-of-six threshold, camera guard and containment. No rig/contact geometry change or blocker removal. Rerender existing checkpoint; no fresh build. Visual grip/wrist seams remain open.
