# SC001 desktop coarse motion test — v0.6

From Git Bash in the repository on `animated-movie`:

```bash
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_blockout.py" \
  -- --render-shot-review --render-motion-preview
```

No add-on, pip install or codec is needed. This uses an isolated background process and refuses loaded files or interactive execution. Each run creates a new ignored folder under `Active/Film/_local/SC001/`, preserving earlier runs.

On success, open the printed `SC001 OUTPUT:` folder. It contains `SC001_blockout_v0.6.blend`, `validation.json`, ten full-resolution shot-start PNGs, `motion_preview.html`, `motion_preview_manifest.json` and 460 smaller PNGs under `motion_frames/`. Open the HTML file in your desktop browser and click Play; pause/scrub to inspect action and carry. Keep the image folder beside the player. Archive the entire run folder for review. Rendering 470 images takes longer than the previous two-shot test; runtime is not benchmarked.

The blend scene `SC001_BLOCKOUT_v0.6` contains 24fps coarse animation and camera markers. The player samples at 4fps, 640×360 for the provisional 115 seconds; use the full-resolution stills for notice readability. Workbench shading is diagnostic and does not demonstrate final noir lighting or grain.

Review waking/support, drawer closure without taking medicine, shower response, coffee return, readable unchanged notice, symbolic fold/pocket, keys/mug collection, birds and exit. Letter/envelope, keys and mug should finish with Elias. Camera assertions check sampled containment and final evaluated prop positions; occlusion, contact and continuous readability still need visual review. Exact shot durations remain hypotheses.

Linear box posing, sliding exit, scale-based folding and drawer hide/slide are approximations. Dressing and changes between room zones use editorial elisions. No facial performance, gait, audio or water simulation is included. No finished-slice gate has passed. See DEC-0028 for judgement calls.

`--render-motion-preview` can be used alone. Still-mode precedence is all-ten, targeted SH005/SH008, then original three-still mode. Omit render flags to build the animated blend without images. If execution fails, retain the run folder and paste the terminal error; partial files are not a passed run. v0.5 desktop execution and focused visual corrections were reviewed. v0.6 has only agent-side Python/timeline checks until this desktop test succeeds.
