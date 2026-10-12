# SC001 v0.22 parked-leaf stop; v0.23 evaluated classification

Author supplied Blender 5.2.2 LTS traceback: possible parked-door collision, CHR_Elias_left_forearm, frame 2791. Build stops before save/render. Last successful desktop remains v0.20.

The existing validator asserts on world-axis bounding-box overlap. For rotated forearm geometry this may include empty space, so overlap alone cannot prove mesh intersection. The pure segment reconstruction does not reproduce this runtime AABB exactly; roll/evaluated geometry differences remain possible. No local Blender runtime exists to inspect those actual corners. This particular failure is neither declared a confirmed collision nor a proven false alarm.

V0.23 keeps geometry and pose while adding an oriented-box separating-axis test on actual evaluated box corners and three edge axes per box. All six box-face axes and nine edge-cross axes are checked; degenerate cross axes skipped. An AABB candidate reaches this narrow test. A confirmed intersection still fails, now reporting actual corners. A successful run records candidate count and zero confirmed intersections. This is exact for the diagnostic box bounding volumes (conservative for a non-box prop), not final skin/cloth collision simulation. Opening clipping and built-support checks remain unchanged.

Tests cover rotated boxes whose AABBs overlap while boxes separate, a true intersection and operand symmetry. Planned carried arms remain clear of leaf under pure reconstruction, but this is not a Blender runtime result. Existing pure regressions, film workspace, AST syntax and diff checks PASS. Actual classification remains desktop-pending. No gate/prose changes.

Rerun full command. If another confirmed intersection occurs, supplied evaluated corners will support a concrete pose/leaf correction rather than guessing from broad-phase bounds. If successful, inspect full ZIP for passage, support and carry acting. Prior failed run retained; fresh output directory used.
