# Elias flat — static room layout v0.1

Status: provisional layout prepared; Blender execution and visual review pending. This is a separate test scene, not v0.27 of the animation.

- Authority: author review AR13–AR14 and DEC-0050. Chapter 1 mirror (`Reports/Manuscript_Text/Chapter_01.txt`) supports separate bedroom/kitchen/bathroom, bedroom imitation fireplace, sofa, clean kitchen and neglected clothes/post.
- Author additions: television, kitchen white goods/table/chairs, bathroom toilet/vent/towel rail/laundry basket. Exact placement, room dimensions and appliances are production judgments.
- Footprint: 14 × 12 m (168 m² gross), 2.4 times the earlier 70 m² floor plate. Bedroom/living room each 35 m²; kitchen/bathroom each 28 m²; circulation 42 m² before wall deduction. This deliberately spacious proposal is not a canonical measurement or certified net usable area.
- Fixed scale: 1 metre = 1 Blender metre. Bed 1.6 × 2.2 m, top 0.54 m. Drawers 0.7 × 0.8 m, top 0.75 m; back flush to inner face of north wall. Clock retains existing blockout style. Fireplace stays in bedroom; clock stays bedside following later author direction.
- Four 1.1 m door apertures open into a 2 m cross hall; north/south spine 1.4 m wide. Entrance at east end. Low diagnostic walls omit lintels and window sill/header; detailed door/window construction is pending.
- Furniture is a static box placement guide. Medicine, paper, mugs, keys, cupboard/tools, clothes, pigeons, ledge/fire escape and actors require subsequent detailed placement and animation. Do not infer their removal from this test.

The JSON is the shared geometry specification; the SVG is generated from it. `sc001_layout.py` supplies static checks to both the verifier and standalone Blender builder. The current v0.26 builder is retained. Its fixed coordinates cannot be reused in this apartment without a deliberate scene migration.

Run `python tools/verify_sc001_layout.py` for partition, door-approach, drawer-space and static-box collision checks. These checks do not certify anatomy, motion, actual grips, door swings, final composition or a finished scene.
