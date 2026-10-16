# SC001 joined paper review and two refinements

Reviewed paper_sequence_20261016_165206_a629dda8.zip: clean CRC,204/204 SHA256 image hashes verified; all204 images inspected across both labelled views.602-pose runtime passed, max palm error6.76e-6m, prop/pad target error1.66e-6m. Codex recommended provisional sequence-structure pass, with mechanical regrip pause and unnecessary right arm lower/return noted. Author authorised those refinements; no new explicit whole-scene acceptance recorded.

New wrapper preserves baseline module. Regrip reduced20→10 frames;64-frame lowered-arm detour replaced by32-frame direct transfer. Total602→560 poses,25.08→23.33 seconds at24fps.190 images across normal arm/contact views.

Checks pass every integer pose:50 fixed-length bones; connected wrists; wrist bend<65 degrees (max63.26); wrist step max36.65mm left/20.54mm right; elbow step max31.64mm left/17.15mm right. During direct transfer, left grip active and paper supported by envelope, props stationary, right wrist above1.23m and all right digit chain points plus nominal radii remain outside mouth until contact arrival. Outside this transfer, source joint/hand/letter/envelope/fold state preserved exactly under remapping.

Passed verify_elias_paper_refinement.py, verify_elias_paper_sequence.py, verify_film_workspace.py, py_compile and git diff --check. No local bpy; Blender/evaluated validation and visual review pending. No force/cloth/full skin collision certification. Pocket remains held, crease pressing and full scene retiming/integration pending. Canonical publication files unchanged.
