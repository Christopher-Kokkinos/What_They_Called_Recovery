# SC001 paper pickup/fold diagnostic

From repository root, open the original rig checkpoint in background using build_sc001_paper_contact_review.py. No extra flags. Same Blender executable and rig_scene_20261014_204455_57a2b099/SC001_rig_performance_v0.1.blend checkpoint as the mug tests.

Output: Active/Film/_local/SC001/paper_fold_<timestamp>_<id>/. Open review_index.html. Review arm_context and paper_contact players;120 integer poses,41 small images per view (82 total). Zip the whole paper_fold folder, including validation.json and both view subfolders.

Check opposed finger/thumb contact, wrist continuity, left hand following fold, right hand stabilising sheet, and visible hand/paper collisions. Diagnostic starts with formed pinch. Supported halfway regrip is included. No initial reach-in/final release, insertion/pocketing or full-scene acceptance. Original exact notice retained; source checkpoint never resaved.

DEC-0081: watch the partial fold, supported pause/regrip, and closing fold. The folding palm should no longer roll180 degrees with the sheet. This isolated clip extends to2280; later envelope timing remains to be coordinated.

## Envelope diagnostic — DEC-0082

Use the same original checkpoint and builder, adding `-- --envelope-review` after the Python path. Output `Active/Film/_local/SC001/envelope_<timestamp>_<id>/`. Open review_index.html and zip entire envelope folder.160 baked poses,54 samples in each of arm_context and paper_contact (108 total). Check flap opening, left support, right transfer/pickup, insertion and thumb withdrawal. Starts with grips formed. Pocketing/closing and fold-to-envelope transition excluded. Isolated review timings overlap older pickup and must not be promoted without retiming.

DEC-0083: add `--envelope-opening-only` alongside `--envelope-review` to check opening/transfer only (60 poses/42 images). Output `envelope_open_<timestamp>_<id>/`; review and zip entire folder. Right elbow should remain on anatomical right and below shoulder. Insertion/withdrawal poses are unchanged and excluded from this smaller preview.

## Insertion and withdrawal — DEC-0084

Use `-- --envelope-review --envelope-insertion-only` with the same builder/original checkpoint. Mutually exclusive with opening-only. Output `envelope_insert_<timestamp>_<id>/`; open review_index.html and zip entire folder.110 baked/readback poses,76 images across normal_context and cutaway_contact. The cutaway hides front/flap/MAC label only for inspection after full-geometry validation; it is not a final camera or collision pass. Check guiding index/thumb, extraction through mouth, then lowering after fingers clear. Opening/pickup/insertion targets unchanged; pocketing and integrated timing pending. Full envelope mode now spans2281–2474 (194 poses); focused review avoids repeating it.

## Closure / handover / pocket approach (DEC-0085)

Use the same original rig checkpoint and builder with `--envelope-review --envelope-finish-only`. Output: `Active/Film/_local/SC001/envelope_finish_<timestamp>_<id>/`. Open `review_index.html`; ZIP the whole output folder.181 poses/122 images, two normal-geometry views. Packet remains held at the provisional pocket target; clothing fit and release are pending. Earlier insertion motion is unchanged. Full-scene timing is not yet integrated.

DEC-0086: same finish-only command now uses a body-relative right-elbow guide; hand and packet targets unchanged. New output required to review the correction. Prior runtime passed but prior visual pass was held.

## Continuous paper sequence (DEC-0087)

Use original checkpoint and `build_sc001_paper_contact_review.py -- --paper-sequence-review` (standalone flag; do not combine envelope subset flags). Output `Active/Film/_local/SC001/paper_sequence_<timestamp>_<id>/`. Open `review_index.html`; ZIP the whole folder.602 poses/204 images: fold, supported table set-down, envelope pickup, insertion, closure and held pocket approach. Initial paper grip already formed; pocket clothing release and whole-scene mug timing pending. New staging brings parked envelope180mm nearer. Both views retain all geometry.

### DEC-0088 refinement — current sequence command

Same `--paper-sequence-review` command and original checkpoint. Now560 poses/190 images (2161–2720): shorter regrip, direct hand transfer from cleared mouth to flap. Output remains `paper_sequence_<timestamp>_<id>/`; open `review_index.html`, ZIP the whole new output folder. The602-pose sequence is retained as the reviewed baseline in code. New timing still requires full-scene integration; pocket remains held.

## Mug/paper handovers (DEC-0089)

Use original rig checkpoint with `build_sc001_paper_contact_review.py -- --mug-paper-handover-review` (standalone flag). Output `Active/Film/_local/SC001/table_handover_<timestamp>_<id>/`.772 poses validated;172 images render only the two handovers, in context/contact views. Open `review_index.html` for four links; ZIP entire new output folder. Connected bake is `SC001_table_handover_diagnostic.blend`. Right hand retains packet during left second pickup; pocket release and full-scene/key/departure timing pending. Source checkpoint read-only.

## Pocket proxy insertion/release (DEC-0090)

Use the original rig checkpoint and `build_sc001_paper_contact_review.py -- --pocket-review` (standalone flag). Output `Active/Film/_local/SC001/pocket_<timestamp>_<id>/`.221 poses/150 images; normal context plus labelled cutaway hiding only REVIEW_Pocket_front. Full geometry retained for validation/saved blend. Open `review_index.html`, then ZIP the whole new folder. Temporary shallow rigid pocket; no cloth/final wardrobe claim. Prior handover remains unchanged; later integrate before keys.

## Two-hand inner pocket (DEC-0091 — replaces rejected pocket movement)

Use original rig checkpoint and `build_sc001_paper_contact_review.py -- --inner-pocket-review` alone. Output `Active/Film/_local/SC001/inner_pocket_<timestamp>_<id>/`;70 semantic poses/140 images. Open `review_index.html`, ZIP whole folder. Normal context and diagnostic cutaway (lapel/lining hidden only). Shape-key jacket patches and Child Of custody switch44; evaluated gates precede rendering. Restaged isolated test, no automatic join to old scene. Final clothing/skin collision checks and envelope bending remain pending. Previous `--pocket-review` retained only for failure reproduction.

DEC-0093: same `--inner-pocket-review` invocation now lowers the off-hand elbow and uses fixed packet-facing cameras. Cutaway close-up excludes the parked mug from framing.70 poses/140 images; camera face-orientation gate does not replace visual occlusion/contact review.
