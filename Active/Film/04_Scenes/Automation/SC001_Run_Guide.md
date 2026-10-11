# SC001 desktop test — v0.13

Run from Git Bash on `animated-movie`:

```bash
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_blockout.py" \
  -- --render-shot-review --render-bedside-preview
```

No add-ons/codecs/pip needed. Runs in an isolated background process; refuses loaded files or interactive execution. Each run creates a new ignored folder under `Active/Film/_local/SC001/`, retaining previous runs.

Full-review output (use `--render-shot-review --render-motion-preview`): `SC001_blockout_v0.13.blend`, `validation.json`, ten 1280×720 shot-start PNGs, `motion_preview.html`, a manifest and 460 640×360 preview PNGs. Open HTML beside its image folder in a browser, click Play and pause/scrub. Send the entire run ZIP and terminal ending. Missing/partial output after an error is not a passed run.

Review low bedside drawers against the pillow-end wall, clock on top, medicine inside drawer, corrected bed head direction/side seating, portrait notice, hinged thirds, unchanged-size envelope and reach/grip. Verify SH002 foreground clearance and SH008 handling readability. Workbench is diagnostic: no final lighting/grain/audio or rigs. 115 seconds remains a hypothesis. Preview samples 24fps source at 4fps; runtime not benchmarked.

v0.7 desktop execution was verified, but arm stretching and cabinet obstruction failed visual review. v0.13 uses fixed handling segment lengths with reach assertions and reachable surfaces. Python/pure checks pass; desktop execution and visual approval pending. Paper folding, drawer movement and pocket entry remain coarse proxies. No finished-slice gate passed. DEC-0030 records author corrections and film layout judgements.

Render flags are optional: no flags builds animated blend; `--render-motion-preview` adds player frames; still precedence is `--render-shot-review`, `--render-targeted-review` (SH003/SH007), then `--render-stills` (three original frames).

Current focused command produces SH003/SH007 stills plus blend and validation, without the 460-frame sequence. Review medicine label/two empty cells and notice text. v0.8 desktop execution verified the geometry but those insert views failed; v0.13 framing/text changes remain desktop-pending.

Current command renders ten stills and only SH002/SH003 motion: 88 samples, 22 seconds, 4fps. Open motion_preview.html; review hips/feet, drawer clearance, lean/closure and 200° camera sightline. Validation includes bedside_occlusion_samples/readability_status: blockers are failures to resolve, not approval. Full sequence remains available via --render-motion-preview.

v0.13 connected hip rotation replaces separate torso/head translations. Read bedside_radial_trials and selected camera keys: 200 is tried first, bounded alternate radials may be selected if sampled rays are blocked. Check both empty cells and label visually regardless of ray result. Connected lean/reach remains provisional and requires desktop review.

v0.13 shifts the medicine label 8 cm right within the strip and reduces its font to 0.042 m. Label occlusion now samples a 21×5 grid over full local text bounds. Lean reduces from 0.85 to 0.66 rad (49° to 38°), paired with a 20 cm sideways/8 cm forward seated scoot. This is a smaller coarse lean, not final subtle acting; review foot sliding and mattress support as well as label/empty cells. New outputs never overwrite old runs.

v0.13 adds reusable fixed-length opening leg/spine joints and planted seated ankle targets, plus right rib-support-to-drawer analytic hand reach. This is a segmented diagnostic proxy, not a skinned armature or final roll/walk. The focused 361–888 preview omits waking: for this pass use --render-shot-review --render-motion-preview to include the sit-up. Review knees/feet, mattress support, chest/head alignment and rib-hand placement; supply the whole run ZIP.
