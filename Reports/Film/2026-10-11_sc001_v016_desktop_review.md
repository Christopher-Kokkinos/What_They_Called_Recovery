# SC001 v0.16 desktop review

Evidence: author-uploaded run_20261011_160746_f22251a1.zip and successful Blender console output. Blender 5.2.2 LTS; builder v0.16, published commit 6675e80. Archive inspected without modifying its contents. Unrelated KDP attachments were not part of this film review.

## Verified execution and provenance

Builder and all seven helper hashes match repository source when Windows CRLF conversion is accounted for. The archive contains the saved blend, validation JSON, player/manifest, ten 1280×720 shot stills and all 460 valid 640×360 preview PNGs. Preview manifest spans 115 seconds at 4 fps, sampling the 24 fps source.

Reported evaluated arm endpoint checks cover all 2760 source frames; maximum error is 0.000001092571 m (approximately 0.0011 mm). Later foot-height maximum error is 0.000000013113 m. Final prop-position custody readback is PASS. These are geometric assertions from the desktop script, not certification of natural acting, grip, collision avoidance or concealed pocket contents.

V0.15 failed before saving; v0.16 completes with explicit curve interpolation. This supports the repair's effectiveness. The earlier traceback contained no frame/hand or curve evidence, so the precise earlier failing target and interpolation mode cannot be retrospectively proven.

## Sampled visual findings

Thirty ordered preview samples cover waking/seating, medicine hold/closure, kitchen/shower, coffee pickup/hold/return, notice, folding/pocket/keys/mug, window and exit. This is sampled visual inspection, not a continuous playback pacing review. The full-resolution notice still is readable and retains the exact accepted wording.

The opening protective pose and medicine staging remain recognisable. Coffee approaches the face and returns to the counter; fingers, mug tilt and sip contact remain coarse. Paper folding and outgoing mug/keys are visible. After the nominal pocket path, the packet remains visibly attached outside the chest: position custody does not prove concealment. Standing legs remain shorter than seated legs. Exit shows alternating step poses and departure from view, but the short fast path remains unsuitable for final injured acting. No visual acceptance is inferred from the successful build.

## Next work and unchanged gates

Prioritise one consistent reusable anatomy across opening and standing shots, jointly resolving mattress support, foot positions and prop reach. Then refine pocket concealment and grip, followed by exit distance/timing and weight transfer. This avoids polishing contact around proportions already known to change. Retain the central open-issues list and reconcile the author's notes before SC002. SC001 remains diagnostic; no finished-slice gate advances and no publication manuscript changes were made.

Repository checks: python tools/verify_film_workspace.py PASS; git diff --check PASS. No code changes in this evidence-recording pass.
