# DEC-0062 — Open U finger bends

2026-10-15. Author rejects folded fingers and specifies three sides of a square with space around handle. Retain connected wrist and fixed phalange lengths.

Previous endpoint-driven solver reached targets but allowed tightly folded middle joints. Replace four-finger endpoint solve with three fixed-length segments following orthogonal directions u, v, -u: open U with two 90-degree changes. Select orientation in mug forward/lateral plane using sampled rail clearance and tip proximity; thumb retains opposed fixed-length solve. Finger bases and palm position retained. Cache solved poses keyed by source frame/layout to avoid repeated search in diagnostics.

Pure checks verify fixed lengths, wrist continuity/roll, orthogonal bends and noncollapsed grip opening at six review frames; normal 246-frame invariant regression retained. Sample segment centreline distance to rail, subtract 8 mm nominal finger radius, and record signed gap. This is a diagnostic metric, not an evaluated skin collision certificate. Some planned poses still show slight rail overlap; do not declare contact PASS. U bend shape and rail fit are distinct review questions. Finger-finger/top-bottom handle/mug-body collisions and transition continuity remain open.

Same isolated six-pose mug build and twelve images. No extra wrist/arm/prop timing changes, no rail shrink or finger stretching to conceal fit limitations. Author review required before accepting grip.
