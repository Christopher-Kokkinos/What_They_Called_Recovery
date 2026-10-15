# Mug join palm mapping failure and repair

Evidence: author Blender5.2.2 execution of318513b --join-review fails elias_rig_blender.py palm_error<1e-4 with0.05500507324159973 m before saving/rendering. Input rig checkpoint remains original. Earlier all-frame pure joint checks were insufficient: target-space correctness did not establish rigid skin mapping.

Diagnosis: integrated rest palm centroid coincides with wrist bone head; held target offset55 mm. Rigid hand-weighted skin cannot change its rest offset. DEC-0072 adds opt-in left palm control, skin/sleeve weights and digit parenting;49 bones integrated,48 legacy. Source hand/arm/palm/finger target positions and all story/prop paths unchanged. Actual Blender deformed palm gate100 microns retained, richer diagnostics added.

Verification: integration regression PASS3168 frames,49 bones, legacy error reproduced0.05499999999999961 m and maximum corrected predicted centroid error0 m. It independently predicts rest-skin centroid mapping over3168 frames, reproduces old55 mm fault, tests new mapping plus existing lengths/wrist/prop/retained-state/transition gates. Legacy verify_elias_rig.py PASS3168 frames,48 bones/2400 vertices/2640 faces. Python compilation, film workspace and diff checks PASS. Blender runtime not available here; corrected175-frame deformed-skin gate, output and visual join review remain pending. No claim of evaluated skin collision/physics or final hand anatomy.

Next: git pull and rerun identical --join-review on original rig_scene_20261014_204455_57a2b099 checkpoint. New mug_joins_ folder; review_index.html plus4 contact stills. Failed run folder can remain as evidence; no need to modify/delete source checkpoint.
