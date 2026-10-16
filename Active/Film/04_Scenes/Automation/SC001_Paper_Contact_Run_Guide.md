# SC001 paper pickup/fold diagnostic

From repository root, open the original rig checkpoint in background using build_sc001_paper_contact_review.py. No extra flags. Same Blender executable and rig_scene_20261014_204455_57a2b099/SC001_rig_performance_v0.1.blend checkpoint as the mug tests.

Output: Active/Film/_local/SC001/paper_fold_<timestamp>_<id>/. Open review_index.html. Review arm_context and paper_contact players;100 integer poses,34 small images per view (68 total). Zip the whole paper_fold folder, including validation.json and both view subfolders.

Check opposed finger/thumb contact, wrist continuity, left hand following fold, right hand stabilising sheet, and visible hand/paper collisions. Diagnostic starts with formed pinch. No reach-in/release, insertion/pocketing or full-scene acceptance. Original exact notice retained; source checkpoint never resaved.
