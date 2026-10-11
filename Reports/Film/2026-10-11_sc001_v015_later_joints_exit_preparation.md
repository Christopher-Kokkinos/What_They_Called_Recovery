# SC001 v0.15 later joint targets and exit preparation

Author authorised extending shared joints to coffee, paper/pocket handling and a grounded exit, with unresolved issues to be reconciled against author notes before SC002. This pass extends the segmented diagnostic architecture; it does not complete SC001.

## Changes

sc001_standing.py separates pure later chest/limb targets from Blender application. The adapter owns body segments across source frames 1–2760. Later arms follow the same chest basis and analytic fixed-length solution; wrists target the mug handle reference, letter/pocket path and keys. Shower raised-arm/head cue retained. Original later motion pass still generates prop paths, but its body poses are overwritten by the adapter. A future cleanup can remove superseded body calculations after desktop regression passes.

Coffee target moves nearer the face: cup base at root offset (0,-0.19,1.38) during the held drink proxy; the wrist follows cup offset (0.19,0,0.11), matching the existing handle-side reference. Mug remains upright; no liquid/finger grip or final sip claim. Counter return and outgoing mug offset unchanged. Paper/envelope custody paths unchanged; pocket insertion remains symbolic rather than proved concealed clothing contact.

Exit body faces the path, using alternating six-frame world-space stance windows and lifted swing feet. Knees solve fixed later proxy legs; final feet settle by frame 2735. Source-frame planting removes continuous root-relative foot sliding during stance. It is contact-based step blocking, not a natural walk cycle. Current 8.17 m travel over 80 frames is about 2.45 m/s and too brisk for injured final acting; timing/distance must be resolved rather than calling this finished walking.

## Explicit limitations

Opening leg proxies are 0.60/0.64 m; later legs retain the old 0.38/0.40 m proportions. This cut-dependent anatomy, introduced when v0.13 replaced only the opening legs, is now logged centrally and must be unified with seat height/feet and prop reach before final character approval. Fingers, cloth/pocket concealment, roll/weight shifts, collisions, audio, final look and pacing remain open. No armature/skinning introduced. No story beats, exact notice, no-dose rule or outgoing custody changed.

## Checks and desktop gate

All-frame pure opening/later limb-length and prop-target reach checks PASS. Planned exit stance anchors are fixed; ankle targets stay above the floor and final feet settle. Automation syntax, workspace and diff checks PASS. Desktop script now checks arm endpoints against joints across all 2760 frames and later foot-bottom heights against stance/swing targets. Seven helpers are hashed. These Blender checks have not run in the agent environment; actual body/prop contact, framing and exit motion remain desktop-pending.

Run full --render-shot-review --render-motion-preview. Review SH006 cup/face/handle, SH008 folding/pocket/keys/mug, SH009 outgoing custody and SH010 feet/path/settling; check corrected opening and medicine label for regression. Preserve run archives. Before advancing beyond SC001, reconcile the central issue list with author's notes; author acceptance is not inferred from successful execution.
