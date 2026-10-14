# DEC-0055 — Isolate hand diagnostics from shot camera bindings

2026-10-14. Author asks to proceed after independent review agrees fingers and hand views fail visual acceptance.

Evidence: all twelve SC001_hand images in rig_scene_20261014_154220_2ff584bb are pixel-identical to their corresponding SC001_rooms stills. The dedicated camera assignment did not control the render. Timeline camera bindings are the leading mechanism; previous implementation did not isolate them or inspect the camera at render start.

Repair: temporarily clear marker camera assignments for hand diagnostics, install a scoped render-pre camera assertion, record actual selected camera and bounded hand/prop projection, and restore bindings/camera/frame/render settings in finally. Fit full hand chains and prop context with an 8% image margin. Containment does not establish occlusion or contact.

Use the existing verified rig scene for a twelve-image read-only rerender instead of repeating the full 528-image preview. Current source hashes must match that scene's validation. Never resave the input blend. Output goes into a new hands_ folder.

Finger geometry retained for this isolated diagnostic pass. Visual finger failure remains open: segmented rod shapes, abrupt palm joins and inadequate prop-specific opposition. Correct close-ups precede further anatomy/contact changes. Accepted body movement/timing/prop sequence remains unchanged.
