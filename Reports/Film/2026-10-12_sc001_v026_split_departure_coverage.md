# SC001 v0.25 visibility failure; v0.26 split coverage

Blender 5.2.2 LTS traceback supplied by author: all eight camera offsets rejected before saving. First blocks at frames 2712–2756, mostly mug/lintel and one forearm/lintel. Last verified desktop remains v0.24. This is failed camera coverage, not failure of the prior verified physical passage.

## Diagnosis and coverage decision

Tested fixed-offset views move across the doorway while looking toward actor/props; their rays intersect lintel during part of the approach. No blocker is hidden or removed. Instead use an interior approach view and exterior arrival view. This is a camera coverage decision, not proof that every possible single continuous camera is impossible.

Interior eye fixed at (8,3,2.3), aimed at actor root height 1.0, frames 2641–2812. Hard cut at 2813 to candidate exterior tracking eye. Existing pigeon cut at 2841 retained. New cut keys use CONSTANT interpolation at 2812 so there is no subframe sweep. One fitted maximum departure scale spans both interior/exterior views; pigeon scale remains separate. Route, timing, body/carry targets, doorway and floor retained. Three camera compositions remain recorded within existing SH010 diagnostic segment; final shot list may later split these explicitly.

## Independent regression

Add analytic orthographic segment/AABB structural ray checks using geometry dimensions captured from the entry builder. Sweep complete mug/handle/key assemblies, head, torso and forearms across all departure frames. Earlier cut timing retained exterior obstructions; later timing retained an interior key/right-jamb obstruction. At cut 2813 the planned regression passes for four exterior candidates. This is planned geometry evidence, not evaluated Blender visibility certification.

All existing geometry/reach/anatomy/support-plan/custody tests PASS. Workspace, AST syntax and diff checks PASS. Blender retains strict evaluated ray gate and selects a passing candidate; actual results and renders remain pending. No local Blender runtime.

## Desktop review

Full run provides 480 preview images, ten standard stills and five phase stills at 2812/2813/2840/2841/2860. Review interior/exterior cut continuity, actor/props at doorway, constant departure size, arrival and pigeon closing beat. Sampled rays do not prove every pixel or body self-occlusion. Audio, final camera language, door use and natural acting remain open. No publication prose or final gate changes.
