# SC001 standalone apartment layout test

Run in Git Bash from `C:/Projects/what_they_called_recovery` on branch `animated-movie`:

```bash
git pull --ff-only

"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_apartment_layout.py" \
  -- --render
```

This command produces a separate `.blend`, `top.png`, `overview.png` and `layout_validation.json` in a unique `Active/Film/_local/SC001/layout_<timestamp>_<id>` directory, printed at completion. It does not generate motion frames or modify an existing run. Default wall height is 0.85 m for diagnostic visibility; add `--full-walls` for a separate 2.6 m wall test. Furniture and fixtures are placement proxies.

Review connected rooms, bed/drawer alignment, furniture spacing and room proportions. Upload that output directory as a ZIP for Blender readback and visual review. No actor or anatomy fixes are present yet. Existing animation can still be generated with `build_sc001_blockout.py`; it remains v0.26 and retains the old apartment.
