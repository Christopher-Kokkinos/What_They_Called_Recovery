# SC001 first desktop blockout test

From Git Bash in the repository on `animated-movie`:

```bash
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_blockout.py" \
  -- --render-shot-review
```

No add-on or pip install is needed. This runs a separate Blender process and does not operate on your open scene. It refuses execution inside interactive Blender or with a loaded file. Every run creates a new folder beneath `Active/Film/_local/SC001/`; existing runs are retained. These generated files are ignored by Git.

On success the terminal prints `SC001 OUTPUT:` and the folder path. Open that folder in Explorer. It contains `SC001_blockout_v0.3.blend`, `validation.json` and ten PNGs named by shot ID and start frame. Open the blend in Blender, select scene `SC001_BLOCKOUT_v0.3`, use camera view and inspect the ten timeline markers. The untouched factory scene may also be present.

Review room proportions, bird location outside the window, clock display, drawer prescription/two dark empty cells and readable MAC notice. The script uses cheap Workbench diagnostic shading; it does not demonstrate the approved final noir lighting or grain. Camera positions and lenses are provisional. The builder fits opening/kitchen/letter/departure key subjects within a 6% frame margin using evaluated object bounds. The letter uses a top-down orthographic diagnostic camera. Containment does not test occlusion or text legibility. No full sequence render is requested.

Elias is a box mannequin at discrete staging positions, not a rig or performance. Pain, waking, drawer closure, folding/pocketing, coffee carry and bird pecking are not animated. Letter/envelope/mug remain static diagnostic props: continuity is specified in the packet, not proven by this test. The 115-second range is a timing hypothesis, not measured screen performance.

If execution fails, retain the folder and terminal error; do not treat partial files as a passed test. Paste the terminal ending for diagnosis. v0.1 desktop execution succeeded in Blender 5.2.2 and v0.2 replacement images demonstrated corrected cropping. v0.3 shadow/kitchen changes and the ten-shot review still require local execution. The agent environment has no Blender/bpy. Send the ten PNGs for visual review before detailed modelling; include validation.json if available. Each file corresponds to one shot, and the report pairs it with the packet review obligation.

The diagnostic preview disables cast shadows to remove duplicate-looking notice text. Final noir shadows remain a production requirement. Clothes/post staging is moved beside the kitchen to let the contrast and full mannequin fit a tighter view; that placement is provisional film design. `--render-stills` retains the original three-image mode, and omitting both flags builds without rendering. `--render-shot-review` takes precedence if both flags are supplied. Ten start-frame stills do not prove shot motion or timing.
