# DEC-0057 — Wrist transition, pinches and shower visibility

2026-10-14. Author authorises a focused steady pass on wrist joins, pinches and shower diagnostics.

Last v0.3 run rig_scene_20261014_170733_de6d79a3 passes all 3,168 integer-frame rig checks (endpoint error 7.6694e-7 m, palm-centre error 6.9521e-6 m), but visual review rejects rounded wrist lumps, unconvincing paper/key grips and torso-blocked shower view. No body/choreography acceptance withdrawn.

Replace spherical wrist bridge with tapered forearm-to-palm sleeve weighted across both bones. This is overlapping closed topology, not a welded final hand. Mirror finger order so both index fingers sit on their thumb side. Add bounded opposed index/thumb tip targets for paper and keys, solved without changing phalange lengths. Pinch pad centre separation is 16 mm; exact skin/prop contact remains provisional. Solver limits unreachable transitions explicitly; completed planned grips are checked for target equality by pure verifier.

Shower diagnostics evaluate eight orthographic viewing directions by ray cast against evaluated scene geometry. Six probes (palm centre and five digit tips), accepting first hit within 25 mm of intended probe as local hand/contact surface. Require at least four visible probes; record all angles/blockers. This sampling does not guarantee whole-hand visibility; keep visual readback gate. Existing camera-selection isolation and projected containment retained.

Source wrists, body motion, story timing and prop custody unchanged. Fresh scene --rig-test --render-hand-review only; no full preview needed. Reusable hand collection now v0.4. All new geometry/contact/visibility remains desktop-pending.
