# First-only support validation scope failure

Desktop log: --table-reach-review --first-table-reach-only, commit5c95a19. Completed rig and mug readback before support assertion selected unbaked frame2400. Gap -0.180000067 m matches original mug height against raised tabletop. This did not diagnose first-lift geometry.

Replaced unconditional support list with candidates intersected with baked frames. Regression confirms first-only samples1375,1400,1540,1550,1560 and combined samples additionally2400,2430,2450. All353 pose checks PASS; film workspace, Python compile and whitespace PASS. No numerical tolerance relaxed. No Blender available locally; desktop rerun and visual review pending.
