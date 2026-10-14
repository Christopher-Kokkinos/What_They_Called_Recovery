# Shower visibility failure and execution cost

Desktop rig_scene_20261014_192618_1ea9a213 stopped after three renders at frame 1213. Every candidate had <=1 visible probe. Several blockers are hidden body proxy meshes and hidden water diagnostic. Scene viewport rays incorrectly included non-rendering geometry. Other controls/skin blockers remain real candidates, so corrected visibility result is still pending.

Approximately 57:18 elapsed before first render; images then saved about 0.3 seconds apart. Cost is preparation/evaluation, not these twelve image renders. Existing FK implementation rebuilds depsgraph after each of 48 bone assignments across 3,168 frames. New exact parent/rest conversion updates once per pose. Snapshot diagnostic mode bakes/readbacks only twelve requested poses; no full motion-pass inference.

Validated scene and provenance now checkpoint before rendering. If corrected camera search fails, keep checkpoint and rerender after repair rather than repeat the build. Original failed run did not save its in-memory blend, so one new build is needed.

Compilation, pure 3,168-frame hand/rig contract and film workspace verifier PASS; diff check PASS. Blender optimisation, render-visible BVH, selected viewing angle and execution timing pending desktop. Original body/choreography and v0.4 hand geometry retained.
