# SC001 connected apartment layout preparation — 2026-10-14

## Diagnosis and evidence

Author corrections AR13–AR14 require separated furnished rooms and more space. Current builder has a 10 × 7 m floor, one north wall, omitted partitions and fixed per-shot actor placements. Chapter 1 text mirror was read for set requirements: bedroom imitation fireplace; sofa/clothes; clean kitchen sink and worktops; hall tools; separate bathroom. Source dimensions are not specified. This update does not alter manuscript text or screenplay.

## Prepared result

A separate static 14 × 12 m proposal has four rooms and cross-hall circulation, a 2.2 m bed, low drawers flush to the bedroom north-wall interior, recognisable fireplace component placement, sofa/television, kitchen worktop/sink/appliances/table/chairs and bathroom tray/rear controls/toilet/basin/vent/towel rail/laundry basket. Exact dimensions are production judgments. Current clock proxy retained. A JSON specification drives SVG floor plan and independent Blender builder through shared pure geometry checks.

The original v0.26 animation is retained; no poses, paper interaction, mug grip, key carry or elbow corrections are claimed. The new builder refuses a loaded file or non-background operation and saves isolated outputs. Default low walls are diagnostic; lintels and detailed door/window geometry remain open. Medicine and small narrative props are not included in this static room test.

## Verification

- `python tools/verify_sc001_layout.py`: PASS; gross area 168 m², ratio 2.4, four rooms; partition coverage, non-overlap, bounds, open approaches, bedside reservation and static 3D furniture intersections checked. Four intentionally invalid cases rejected (room overlap, furniture collision, door blocking and bedside obstruction). Drawing matches specification.
- First placement check found fridge/cooker intersection; fridge moved to separate side position, then checks passed.
- Python compilation for two new modules and verifier: PASS.
- `python tools/verify_film_workspace.py`: PASS.
- `git diff --check`: PASS.
- Floor-plan geometry/labels inspected in a scratch raster preview. No Blender executable or bpy is available here; no Blender build/render claim. Desktop saved-object readback and visual review pending.

## Next gate

Run standalone layout on the desktop using `SC001_Apartment_Layout_Run_Guide.md`; inspect scale, furniture and circulation. Then correct shared anatomy bend/support, place real contact objects, and migrate motion explicitly. AR01–AR17 stay open except explicitly deferred clock work and retained exit direction. No finished-slice gate or whole-scene acceptance.
