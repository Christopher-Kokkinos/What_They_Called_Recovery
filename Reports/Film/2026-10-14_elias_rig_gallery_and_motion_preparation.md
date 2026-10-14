# Elias gallery readback and SC001 motion-test preparation

## Evidence
Uploaded rig_20261014_134651_06eb40af.zip includes two Blender files, ten pose PNGs and rig_validation.json. Blender 5.2.2 LTS reports 18 bones, 1,104 vertices, 1,224 faces; all ten pose endpoint checks and finite geometry checks complete. Maximum endpoint error 6.174099736e-7 m; maximum bone-scale error 2.384185791e-7. Source file hashes match Windows CRLF encodings of the published source. All ten images inspected; no obvious catastrophic deformation. Shoulder/hip seams and placeholder hands remain provisional. Author explicitly passes gallery poses.

## Implementation and judgement
Extract the existing rig constructor unchanged into shared elias_rig_blender.py. Both gallery and opt-in room test use this constructor. The scene test keys exact source targets, including world travel, for all 3,168 frames, then reads evaluated keyed action and skin. Retain hidden-in-render box proxies for established contact gates. Output is separate from accepted room blockout. No timing, relationships, source text or choreography changes.

## Validation
Python compilation and tools/verify_elias_rig.py PASS (3,168 pure source frames, normalized weights, closed topology); tools/verify_film_workspace.py PASS. Blender execution is unavailable in the preparation environment. Runtime readback, skin contact and motion visual review remain pending. Pure contract does not prove skin clears props/furniture. No final scene or final character appearance acceptance.
