# DEC-0058 — Render-visible rays and focused pose execution

2026-10-14. Author desktop failed at shower diagnostic after approximately 57 minutes of scene preparation and three sub-second renders. Failure log names CHR_Elias_right_palm/lower_spine and REVIEW_ShowerWater, all hidden from render. Viewport scene.ray_cast includes those meshes; the visibility assertion was testing a different scene from the rendered image. Genuine tap/skin blockers also appear; do not assume filtering alone certifies visibility.

Build an evaluated world-space triangle BVH using only non-hide_render mesh objects for the shower probes, recording excluded objects. Same six probes/four-visible threshold; actual controls/body remain blockers. No weakening of the visibility threshold or hiding actual scene geometry.

Save validated blend and source-provenance checkpoint before any renders, so camera failures are recoverable through the existing read-only rerender script. Prior failed run predates this safeguard; its three PNGs alone cannot recover the in-memory rig.

Reduce FK dependency-graph updates from one per bone to one per pose using exact rest/parent/target matrix conversion. All-frame evaluated assertions retained in normal mode; optimisation execution pending desktop.

Add --rig-sample-review for twelve hand frames only, allowed exclusively with --rig-test --render-hand-review and no scene/motion previews. Mark saved scene/report diagnostic snapshots only. It does not replace full 3,168-frame motion validation. Props retain existing source choreography; hands/skin unchanged. New desktop timing is unmeasured.
