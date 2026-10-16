# DEC-0079 — Restrict support checks to baked frames

Desktop first-only run at5c95a19 failed at frame2400 with -0.180000067 m gap. Root cause: fixed support sample list included second clip despite only first clip receiving revised prop keys. Frame2400 evaluated original checkpoint animation against raised table; it was outside requested coverage.

Fix: intersect support sample candidates with actual baked frames. First-only retains all five first-clip resting checks; combined mode retains eight. No pose, geometry, tolerance or collision requirement changed. Pure regression verifies first-only, combined and historical contact-cycle schedules. Runtime rerun required.
