# SC001 desktop test — v0.8

Run from Git Bash on `animated-movie`:

```bash
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_blockout.py" \
  -- --render-shot-review --render-motion-preview
```

No add-ons/codecs/pip needed. Runs in an isolated background process; refuses loaded files or interactive execution. Each run creates a new ignored folder under `Active/Film/_local/SC001/`, retaining previous runs.

Successful output: `SC001_blockout_v0.8.blend`, `validation.json`, ten 1280×720 shot-start PNGs, `motion_preview.html`, a manifest and 460 640×360 preview PNGs. Open HTML beside its image folder in a browser, click Play and pause/scrub. Send the entire run ZIP and terminal ending. Missing/partial output after an error is not a passed run.

Review low bedside drawers against the pillow-end wall, clock on top, medicine inside drawer, corrected bed head direction/side seating, portrait notice, hinged thirds, unchanged-size envelope and reach/grip. Verify SH002 foreground clearance and SH008 handling readability. Workbench is diagnostic: no final lighting/grain/audio or rigs. 115 seconds remains a hypothesis. Preview samples 24fps source at 4fps; runtime not benchmarked.

v0.7 desktop execution was verified, but arm stretching and cabinet obstruction failed visual review. v0.8 uses fixed handling segment lengths with reach assertions and reachable surfaces. Python/pure checks pass; desktop execution and visual approval pending. Paper folding, drawer movement and pocket entry remain coarse proxies. No finished-slice gate passed. DEC-0030 records author corrections and film layout judgements.

Render flags are optional: no flags builds animated blend; `--render-motion-preview` adds player frames; still precedence is `--render-shot-review`, `--render-targeted-review` (SH005/SH008), then `--render-stills` (three original frames).
