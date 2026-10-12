# DEC-0046 — Body-relative exit carry and complete assembly checks

Date: 2026-10-12. Authority: supplied v0.23 failure and ongoing authorised repair.

Runtime mug at frame 2794 violates left opening by 0.249 m; point matches the pure old carry path. Body turns but mug/keys/jacket retained world-axis offsets, so the carried silhouette crosses obliquely without following facing. Previous arm/sole regressions did not cover complete props.

During exit, rotate carry positions and whole mug/key assemblies with body yaw; rotate evaluated mug grip reference too. Bring mug and keys 0.10 m inward in body coordinates (mug X=-0.30, keys X=+0.25). Revise exit elbow poles for new wrists; dimensions fixed. Jacket follows yaw; packet already did. Earlier coffee/paper staging retained. Final readback uses the same carry function. Keep route, opening, duration and custody roles.

Add complete cup/handle/key/jacket volume regression and include all handle/key subparts in runtime entry checks. Regression caught a key-tooth failure and guided inward keys placement before publish. Planned prop margin 0.0661 m; planned arm margin 0.0689 m. Blender execution/visuals remain pending. No gate/prose change. Evidence: Reports/Film/2026-10-12_sc001_v024_body_relative_carry_repair.md.
