# DEC-0072 — Independent palm control for integrated joins

2026-10-15. Desktop --join-review at318513b fails before save/render: palm target mapping mismatch0.05500507324159973 m. Source checkpoint retained. This is a rig/skin mapping defect, not a render issue or permission problem. No visual pass inferred.

Root cause: integrated rest889 has palm centre at wrist; mug poses require palm55 mm distal to wrist. Existing palm vertices are rigidly weighted to hand.L, whose head is the wrist. A single rigid bone preserves rest offset and cannot represent both target offsets. Earlier all-frame pure verifier checked bones/targets but omitted weighted palm mapping; Blender correctly rejected the mismatch. Do not weaken100-micron readback threshold.

Opt-in _palm_controls=('left',) on integrated state adds palm.L child of wrist hand.L. Palm control has fixed60 mm length and independently keyed target centre/orientation. Left palm skin and sleeve terminal weights follow palm.L; digit roots parent to it. Wrist hand.L remains at forearm endpoint. Existing48-bone legacy/snapshot rigs unchanged; integrated rig49 bones, same skin topology. This represents legacy varying palm targets; it does not certify final metacarpal anatomy or wrist surface topology.

Pure verifier now derives palm centroid from actual rest skin vertices/weights and transforms it using keyed bone targets. It reproduces legacy55 mm error and requires mapped palm centres match across3168 frames. Normalized weights/reference names checked. Existing target/bone/wrist/path/retained-interval gates remain. Blender exception now includes worst frame/side/actual/target and report bone count; thresholds unchanged.

Prepared pure integrated and legacy regressions, syntax/workspace/diff checks pass; desktop175-pose deformed-skin readback and four visual boundary clips still pending. Same original checkpoint/--join-review command. Retain failed output/evidence; original checkpoint never resaved. Table/posture/contacts remain open.
