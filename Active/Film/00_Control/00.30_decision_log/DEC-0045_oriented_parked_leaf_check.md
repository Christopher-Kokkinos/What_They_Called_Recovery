# DEC-0045 — Classify parked-leaf intersection before geometry changes

Date: 2026-10-12. Authority: supplied v0.22 desktop failure and ongoing repair.

V0.22 stops on possible AABB overlap, left forearm at 2791. AABB overlap is a candidate, not proof of intersection between rotated boxes. Pure model does not reproduce that runtime AABB exactly; do not label this specific case a false positive without evaluated evidence.

Add oriented-box separating-axis test using actual evaluated corners and edge axes (both box face axes and nine edge-cross axes). Confirmed intersection still stops with corners/object/frame; otherwise record broad-phase candidate count. Opening/support checks remain strict. Keep pose/geometry until classification. Pure synthetic AABB false-positive and true-intersection tests pass; Blender classification pending. See Reports/Film/2026-10-12_sc001_v023_parked_leaf_diagnosis.md. No gate advancement.
