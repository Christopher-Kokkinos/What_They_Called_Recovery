# SC001 first desktop blockout test

From Git Bash in the repository on `animated-movie`:

```bash
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_blockout.py" \
  -- --render-stills
```

No add-on or pip install is needed. This runs a separate Blender process and does not operate on your open scene. It refuses execution inside interactive Blender or with a loaded file. Every run creates a new folder beneath `Active/Film/_local/SC001/`; existing runs are retained. These generated files are ignored by Git.

On success the terminal prints `SC001 OUTPUT:` and the folder path. Open that folder in Explorer. It contains `SC001_blockout_v0.1.blend`, `validation.json` and three PNGs (frames 1, 889, 1561). Open the blend in Blender, select scene `SC001_BLOCKOUT_v0.1`, use camera view and inspect the ten timeline markers. The untouched factory scene may also be present.

Review room proportions, bird location outside the window, clock display, drawer prescription/two dark empty cells and readable MAC notice. The script uses cheap Workbench diagnostic shading; it does not demonstrate the approved final noir lighting or grain. Camera positions and lenses are provisional. No full sequence render is requested.

Elias is a box mannequin at discrete staging positions, not a rig or performance. Pain, waking, drawer closure, folding/pocketing, coffee carry and bird pecking are not animated. Letter/envelope/mug remain static diagnostic props: continuity is specified in the packet, not proven by this test. The 115-second range is a timing hypothesis, not measured screen performance.

If execution fails, retain the folder and terminal error; do not treat partial files as a passed test. Paste the terminal ending for diagnosis. The agent environment has no Blender/bpy, so runtime API compatibility and camera readability await this local test. Send the three stills for visual review before detailed modelling.
