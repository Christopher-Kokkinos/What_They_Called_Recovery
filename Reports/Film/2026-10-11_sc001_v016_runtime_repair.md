# SC001 v0.15 failed desktop build; v0.16 repair preparation

The author supplied a Blender 5.2.2 LTS traceback from commit e81a706. Later standing articulation requested a wrist 0.738464338 m from its shoulder, exceeding the fixed 0.70 m reach. Execution stopped before saving/rendering; the empty run folder is consistent with that failure. This is a failed desktop build, not a visual-review result. The traceback lacks frame/side, so the exact target remains unconfirmed.

The analytic paths and their sparse linear interpolation pass all-frame reach checks. The implementation relied on the UI preference for Python-inserted key interpolation, without explicitly setting actual action curves. V0.16 now assigns LINEAR to owned transform keys and CONSTANT to visibility keys, supporting legacy actions and layered channel bags. It normalises curves before evaluated prop targeting and after dense body insertion. This repairs an unverified interpolation contract; the desktop failure's exact cause is not claimed proven. No arm lengths are increased, target is not clamped, and story/custody paths remain unchanged.

Reach failures now identify source frame, hand, shoulder, wrist, distance and limit. If the runtime discrepancy persists, the next traceback will isolate the target directly. Empty prior runs can remain; the next run uses a separate output directory.

Validation: pure all-frame motion/reach, sampled-linear reach regression, legacy/layered curve assignment regression, Python syntax, film workspace and diff checks PASS. No Blender executable/bpy runtime is available here; Blender 5.2.2 execution and visual checks remain pending. Last verified desktop evidence remains v0.14. No finished-slice gate advances.

Rerun the committed builder with --render-shot-review --render-motion-preview and retain the complete output folder. Review coffee, folding/pocket/keys and exit, with opening regression. Author notes and central open issues remain required before SC002.
