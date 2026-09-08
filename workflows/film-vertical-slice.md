# Film vertical-slice workflow

1. Select one representative scene targeting approximately 2–5 finished minutes.
2. Assign a `SC###` ID and register it in `Active/Film/00_Control/scene_register.csv`.
3. Adapt the scene for screen in `Active/Film/01_Adaptation/` without modifying canonical manuscript prose.
4. Define the visual target in `02_Design/`.
5. Identify the minimum reusable asset set; register assets and licences before final use.
6. Build a rough layout/animatic before detailed production.
7. Produce required Blender assets/scenes and performance capture.
8. Complete animation, lighting and render passes.
9. Complete dialogue, Foley, ambience, SFX and music.
10. Edit, composite, grade and master the scene.
11. Review the finished scene as a film, not merely as an animation test.
12. Record time bottlenecks, reusable systems and quality limits in `Reports/Film/`.
13. Run `python tools/verify_film_workspace.py` and confirm the zero-cash/licensing controls remain satisfied.
14. Only then decide whether the pipeline is ready to scale beyond the vertical slice.
