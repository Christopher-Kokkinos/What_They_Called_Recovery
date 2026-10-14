# SC001 hand diagnostics — failure evidence and repair preparation

Uploaded rig_scene_20261014_154220_2ff584bb inspected: twelve purported hand close-ups and corresponding scene stills. Each pair is pixel-identical (RGB comparison), proving close-up selection failed. Existing armature/palm evaluation passes all 3,168 frames: palm-centre error 8.598163696e-6 m; endpoint error 7.669394751e-7 m; scale error 5.960464478e-7; 5,968,512 finite skin vertex checks. Numerical execution does not prove finger grip correctness.

Visible segmented finger shapes and abrupt palm attachments fail character-hand quality; scene framing prevents reliable detailed assessment of thumb opposition/fingertip contact. Author and independent review agree physiological framework is useful but fingers/close-ups are not accepted.

Shared diagnostic renderer now isolates timeline bindings, asserts selected camera at render start, fits hand/prop bounds, records camera data and restores state in finally. Existing room builder uses this module; dedicated read-only renderer reuses prior blend and source validation hashes. Twelve stills only; no full animation rebuild, source blend overwrite or finger alteration.

Python compilation and film workspace verifier PASS; diff check PASS. Blender is unavailable in preparation environment. Actual camera selection/occlusion and resulting anatomy/grip detail remain desktop-pending. Historical exact runtime mechanism remains inferred from bindings and image duplication; new camera records will provide direct evidence.
