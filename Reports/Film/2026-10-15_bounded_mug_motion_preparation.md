# SC001 bounded mug motion preparation

Input mug_20261015_160053_a546fe41.zip reviewed: all14 images and image hashes; six-pose wrist gap2.47556682e-7 m, endpoint1.19092817e-6 m,14400 vertex checks. Grip reads more unified, lower fingers closer and thumb less curled. Provisional blockout only, surface contact/seams open. Author agrees motion test.

DEC-0068 adds optional --motion-preview without altering pose/contact or source choreography.140 integer rig/mug readbacks,48 small renders, fixed camera and local HTML image player. Input checkpoint retained; new mug_motion_ output saved before render. Source interval1400–1539; formed grasp through near-table return, approach/release excluded. Exact final placement at1540 is outside interval.

Validation run: tools/verify_elias_mug_contact.py PASS246 frames including1400–1539; fixed lengths, wrist, nominal role contact bounds. Preview schedule checks PASS140 integer frames and48 ordered rendered samples/endpoints. Python compilation, tools/verify_film_workspace.py and git diff --check PASS. No Blender installed here: all-frame rig/mug readback and camera/skin/contact visuals pending desktop execution. Mathematical clearance is not evaluated mesh collision or force proof.

Review motion_preview.html for slipping, wrist popping, elbow direction, mug tilt and timing. Fixed camera may expose scene occlusion; do not equate containment with visibility. ZIP whole newest mug_motion_ folder including validation, manifest, .blend, HTML and motion_frames.
