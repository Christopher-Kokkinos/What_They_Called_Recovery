# SC001 connected-room performance v0.1

Status: implementation prepared; desktop build/render and visual acceptance pending. Uses the larger room layout accepted as a working foundation by the author. Original v0.26 animation remains available as a checkpoint.

Run from Git Bash:

```bash
cd /c/Projects/what_they_called_recovery
git pull --ff-only

"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_room_performance.py" \
  -- --render-shot-review --render-motion-preview
```

A fresh `Active/Film/_local/SC001/rooms_<timestamp>_<id>` folder contains the `.blend`, `validation.json`, full-resolution contact/action stills, 528 sampled motion PNGs, preview manifest and `motion_preview.html`. The command prints `SC001 ROOMS OUTPUT:` with the exact path. This is a new builder; rerunning `build_sc001_blockout.py` still produces the old apartment.

Open `motion_preview.html` locally to play or scrub the silent 4 fps sample. Source animation is 24 fps over 132 seconds. The extra 12 seconds provide the separated-room exit route; earlier beat frame ranges are retained. Review stills show the source frame in their filenames. ZIP the complete new `rooms_...` folder for readback.

## Review focus

- Sleeping feet within bed; side seat with thighs supported and feet on floor. Rise remains coarse, not a final physiological roll.
- Elbows below shoulders, with anatomically consistent left/right basis; arms are still segmented proxies.
- Left hand approaches real drawer handle, clear of cabinet and knee space; right arm provides earlier rib support. Small ten-cell strip remains inside drawer; no dose is taken.
- Right hand uses the rear-wall shower controls. Feet rest on the tray; cold cue follows three seconds of water. Label/water block are diagnostic cues, not final effects or audio.
- Left hand grips the mug on its actual handle side; mug returns to table before paper work.
- Both hands fold; left supports envelope, right inserts; flap closes as packet is pocketed; keys then mug are retrieved. Notice wording remains exact.
- Keys hang beside torso; mug elbow stays down, forearm raised ahead.
- Larger room positions, cupboard/tools, sofa clothes, post and imitation fireplace stay stable across shots. No floating jacket block is used.
- Exit pans indoors, cuts outdoors and ends on pigeons. Constant departure scale is retained across interior/exterior cuts. Door operation remains pending; apertures are open.

Diagnostic walls are 0.85 m high so contacts can be inspected. Full-height partition collision checks run in the pure verifier; final set occlusion/framing still requires Blender review. This output does not certify finished acting, skinning, finger contact, lighting, grain, audio or scene acceptance.

Optional preflight (if your Git Bash Python command is `python`):

```bash
python tools/verify_sc001_layout.py
python tools/verify_sc001_room_performance.py
```

## Frame 1213 targeted follow-up

The opaque water diagnostic intersected the right upper arm. It is now wireframe-only in the viewport and excluded from renders; cold cue remains. The joint plan does not change. For six contact/cue stills instead of the entire preview, use the same command with `-- --render-shower-review`. Frames: 1195, 1207, 1213, 1225, 1237, 1285. Full-scene checks and a fresh `.blend` still run. Upload the new `SC001_rooms_frame_1213.png` and `validation.json` to confirm whether this clears the observed artifact.
