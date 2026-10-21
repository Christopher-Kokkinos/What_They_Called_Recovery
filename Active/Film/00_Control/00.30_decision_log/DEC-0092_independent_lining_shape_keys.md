# DEC-0092 — Independent lining deformation controls

Author runtime: c29b322 stopped at semantic frame22, Evaluated lining bulge. No render or visual pass resulted.

Judgement: isolate jacket controls from active/mixed shape-key creation state. Both PullOpen and HandBulge now explicitly use Basis-relative coordinates seeded from the original grid, with from_mix=False. This addresses possible inherited opening displacement in the bulge key; the old assertion did not log coordinates, so that diagnosis remains provisional until Blender readback confirms it. Movement, custody switch44 and strict 0.1mm evaluated tolerance remain unchanged.

Add deterministic construction regression using contaminated initial coordinates/reference, and log actual/expected positions and error for any lining mismatch. Local construction,70-pose anatomy, compilation and film workspace checks pass. Blender unavailable here; rerun the same --inner-pocket-review command. Runtime and visual acceptance remain pending.
