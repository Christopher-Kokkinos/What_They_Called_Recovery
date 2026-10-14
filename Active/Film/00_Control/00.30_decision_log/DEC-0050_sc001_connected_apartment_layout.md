# DEC-0050 — Connected apartment layout test

Date: 2026-10-14
Status: Prepared; author review and Blender runtime pending

Root cause: the 10 × 7 m cutaway deliberately omitted partitions and reused hard-coded positions. Scaling that animation would enlarge people/props or preserve collisions. Prepare a separate room specification and static Blender test before migrating motion.

Judgments: use a 14 × 12 m gross footprint (2.4 times prior floor plate), four separated rooms, clear cross hall and reserved bedside working space. Human/prop scale remains unchanged. Room dimensions and furniture positions are provisional production decisions, not novel facts. Fireplace stays in bedroom per Chapter 1 mirror. Clock stays bedside under author direction, with style remodel deferred.

The author requested larger space and room contents in AR13–AR14. This implements a reviewable static proposal, not final resolution. Existing animation remains a checkpoint. Next: desktop layout review, shared anatomical bend/support correction, then contact targets and animation migration. Preserve accepted story beats and exit-camera direction; exact camera coordinates will need reconsideration for the new geometry.

Files: `Active/Film/03_Assets/Sets/EliasFlat/`, `sc001_layout.py`, `build_sc001_apartment_layout.py`, standalone run guide and `tools/verify_sc001_layout.py`. Evidence: `Reports/Film/2026-10-14_sc001_apartment_layout_preparation.md`.
