# DEC-0083 — Envelope opening elbow on correct side

Author confirms manipulating elbow is on wrong side of torso and authorises correction. Uploaded envelope_20261016_084920_c3f6281c.zip passes160 poses and108 image hashes (maximum palm error0.00000674455 m, prop/pad error0.00000158598 m), but opening elbow visibly crosses upper chest. Contact validation did not certify anatomical side.

Root cause: nearest hand-axis elbow solution unconstrained by torso side; original opening elbow lateral coordinate about -100 mm relative to torso, instead of right-side positive. Correct flap hand direction to include right/left lateral reach appropriate to task, independent of flap normal. Constrain opening/transfer elbow pole down and towards anatomical right. From2340 onward retain exact old targets; no insertion alignment change.

Checks: opening elbow centre stays >150 mm on right of midline and >150 mm below shoulder;70 mm elbow-radius proxy separated from450×250 mm torso via outboard/front plane with >10 mm clearance. Actual minimum measured18.276 mm. Wrist-axis bend remains <65 degrees; maximum opening elbow step15.566 mm.160-pose regression passes,101 later poses2340–2440 exactly unchanged in one-off comparison to prior provider. Full skin contacts still require visual review.

Add --envelope-opening-only with --envelope-review:60 poses,42 images, opening/transfer only. Existing full envelope mode retained. Abrupt final withdrawal and fingertip occlusion remain open; not silently fixed or accepted. No story/manuscript change.
