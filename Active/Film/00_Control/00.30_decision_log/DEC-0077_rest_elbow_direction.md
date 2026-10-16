# DEC-0077 — Correct resting elbow direction

Author explicitly corrected the forward-pointing elbow interpretation. Resting upper arm should hang near torso, elbow behind wrist, forearm gently forward. DEC-0076 improved the render but did not resolve it; its forward-elbow test was an incorrect requirement.

Replace resting wrist offset with685 mm down,60 mm forward,20 mm outboard; elbow pole340 mm down,150 mm back,20 mm outboard. Preserve fixed anatomy and established cup-arm targets. Replace the incorrect forward-elbow assertion with wrist ahead of elbow, upper arm less than15 degrees from downward torso axis, and resting elbow flexion between5 and30 degrees. Check right resting arm throughout353 poses and both initial left poses. Keep existing bounded continuity and cup-arm preservation checks.

Status: numerical preparation passed; Blender/visual review pending. Same119-image two-clip review; no whole-scene acceptance. Keys proxy follows resting hand; detailed pinch/pocket remains open.
