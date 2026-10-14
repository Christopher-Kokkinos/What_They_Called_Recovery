# SC001 weighted-rig movement and interaction test

Run in Git Bash from the repository root:

```bash
cd /c/Projects/what_they_called_recovery
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_room_performance.py" \
  -- --rig-test --render-shot-review --render-motion-preview
```

The all-frame armature/skin checks run before rendering and can take longer than earlier box builds. If any assertion fails, send the traceback; do not treat the partial folder as a completed run.

ZIP the entire newest `rig_scene_...` folder under `C:\Projects\what_they_called_recovery\Active\Film\_local\SC001`. It contains `SC001_rig_performance_v0.1.blend`, `validation.json`, 46 review stills, 528 motion samples, manifest and HTML viewer. The output line retains `SC001 ROOMS OUTPUT:`.

Review all movements with particular attention to shoulder/hip seams, elbow/knee deformation, bed and sole support, drawer palm contact, shower control reach, mug grip, both-handed folding/insertion, pocketing, keys and departure. Box contact tests remain useful but do not prove the new skin clears furniture. Skin is a neutral mannequin, without final fingers, face, clothes, materials or continuous fractional-frame validation.

To reproduce the accepted box performance, omit `--rig-test`; earlier outputs are never overwritten.

## Hand revision v0.2

Add `--render-hand-review` to the rig-test command for twelve dedicated hand/prop close-ups. With the full flags, outputs include 46 scene stills, twelve hand stills and 528 motion frames. All-frame Blender checks now include evaluated palm mesh centroid vs the accepted action-specific target. This is a mapping test, not a fingertip collision/grip certificate. Fingers remain provisional articulated closed components. The scene filename remains SC001_rig_performance_v0.1.blend (scene scaffold version); its reusable character collection is v0.2.
