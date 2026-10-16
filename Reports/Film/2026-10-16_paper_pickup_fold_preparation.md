# Paper pickup/fold preparation

Diagnosis: generic paper palms and detached pad targets did not share evaluated sheet-edge transforms. New pure paper contact module constructs opposed pad targets in sheet-half coordinates, follows the actual fold angle, resolves fixed-length arms and digits, and uses connected wrists plus independent palm controls.

verify_elias_paper_contact.py PASS:100 poses,50 bones, fixed bone lengths, normalized skin weights, contact-plane targets, fold-edge trajectories, parked mug, maximum consecutive wrist movement0.02897235 m. verify_elias_table_reach.py PASS353 existing poses. Python compilation, film workspace and whitespace checks PASS. No local Blender runtime; no runtime or skin-collision pass claimed.

Builder opens original rig checkpoint, verifies layout/source hashes, hides original actor and rebuilds diagnostic rig, keys paper/flap/parked props. Reads every prop transform, finger endpoints and evaluated fixed/folding-half contact planes. Saves checkpoint before rendering. Outputs paper_fold_* with review_index.html, arm_context and paper_contact players;68 images total. Source scene untouched. Starts with pinch formed; hand approach/release, envelope insertion and pocketing are next stages. Full surface collisions require visual review.
