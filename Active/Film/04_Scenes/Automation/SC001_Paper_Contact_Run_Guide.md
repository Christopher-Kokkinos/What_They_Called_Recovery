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
