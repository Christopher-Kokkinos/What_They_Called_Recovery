# Elias reusable rig preparation — 2026-10-14

## Prepared result

Reusable armature/weighted mesh builder, pure rig definitions, neutral asset output and ten-pose gallery. Source: accepted SC001 blocking targets; no manuscript or screenplay changes. Existing character dossier is explicitly pending, so neutral materials/forms are production test choices, not approved Elias appearance.

Pure definition: 18 bones, 1,104 vertices, 1,224 faces, twelve closed components. Arm/leg tubes blend two bone weights near bends; torso/head/hands/shoes are simple forms. The final character mesh is not yet welded, furnished with face/hair/cloth, or integrated into SC001.

## Validation

`python tools/verify_elias_rig.py`: PASS. Bone lengths are constant across all 3,168 source frames; ten gallery poses selected. Vertex values finite, weight sums normalized, referenced bones valid, component edges each shared by two faces and signed volumes positive (outward winding). Initial tube winding was inward and corrected before publication.

Python compilation of new rig definitions, builder and verifier: PASS. Film-workspace verifier and `git diff --check`: PASS. These are preparation checks; no Blender executable is available here.

## Runtime checks prepared

Builder checks evaluated armature head/tail error and bone scale for all ten gallery poses, topology count and finite deformed vertices. Pose-gallery curves hold discrete frames; no continuous animation inferred. It fits a constant review camera across all sampled deformed shapes. A separate neutral asset is saved after clearing the gallery action from the rig; gallery remains in its own `.blend`. Source/helper hashes are recorded.

Bone endpoint checks do not certify skin volume or final contact. Hand deformation helpers retain wrist targets; proxy grip offsets need mapping onto actual skin/finger geometry before room integration. Visual review must inspect joint pinching, shoulder/hip joins, wrist/foot orientation and head/neck attachment.

## Next gate

Desktop run using `Active/Film/03_Assets/Characters/Elias/README.md`, then upload the new `rig_...` folder. Review deformation before replacing scene proxies. No final character appearance or finished-slice acceptance claimed.
