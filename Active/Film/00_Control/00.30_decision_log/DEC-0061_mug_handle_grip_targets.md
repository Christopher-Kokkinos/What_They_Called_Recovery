# DEC-0061 — Mug handle grip targets and framing

2026-10-15. Author calls connected-wrist mug experiment a massive improvement, requests refinement. Retain exact common wrist, neutral distal axis and source mug path.

Latest mug_20261015_132729_ad171f13 reports six poses, maximum wrist gap 1.519626234e-7 m and palm-centre error 2.198918670e-6 m. Twelve views inspected; finger/thumb wrap and wrist surface seam remain open. Drink close-ups at 1460/1500 widened because diagnostic prop selector fell through to Letter_ rather than Mug_. Use the mug experiment state marker to select mug geometry at every pose.

Replace inherited generic digit curls in the isolated experiment with handle-coordinate targets: fingers on one depth face of outer rail, thumb opposed on the other. Fit individual rail heights to knuckle height within ±50 mm. Solve all three phalanges at fixed length using bounded distal bend choices. Record target residuals; clamp unreachable transition targets without stretching, but require all six review poses reach all five targets exactly in pure verifier. Exact skin contact, finger-finger collisions and bend continuity remain visual/motion-review pending.

No wrist mesh/topology alteration in this pass: seam remains explicitly open rather than obscured with another connector. Paper/dial/key directions remain queued. Same six-pose builder; twelve renders, no full scene bake. Preserve input checkpoint and source body/mug route.
