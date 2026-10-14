# Elias reusable rig/skin prototype v0.1

Status: neutral deformation mannequin prepared; Blender runtime and visual review pending. This is an asset test, not Elias's approved appearance and not a replacement for SC001's accepted mechanical blocking.

## What is built

- An 18-bone armature, named left/right arm and leg chains, pelvis/spine/neck/head and foot/hand deformation helpers.
- One procedural mesh: 1,104 vertices, 1,224 faces, twelve closed surface components. Limbs blend weights near elbows/knees; body/head/hands/shoes use simple diagnostic forms.
- No paid or imported asset dependencies. Neutral materials are provisional. Facial features, hair, outfit design and final skin/hand topology are unchosen.
- Shared fixed dimensions from `Elias_proxy_anatomy_v0.1.md`; source positions from the verified room choreography. Nonconnected helper bones allow direct source-pose mapping without stretching bones.

`elias_rig_math.py` defines bones and skin without Blender. The versioned builder at `Active/Film/04_Scenes/Automation/build_elias_rig.py` creates the actual armature/modifier/weighted mesh and keys a separate pose gallery. Mesh surfaces are not yet welded into one production skin; seams and bend quality require visual review. No IK/facial/finger controls or cloth rig are claimed.

## Desktop command

```bash
cd /c/Projects/what_they_called_recovery
git pull --ff-only

"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_elias_rig.py" \
  -- --render-review
```

Output: a new `Active/Film/_local/Characters/Elias/rig_<timestamp>_<id>` folder. The command prints `ELIAS RIG OUTPUT:`. It includes:

- `CHR_Elias_rig_v0.1.blend`: neutral rest asset, rig and skin in collection `CHR_Elias_rig_v0.1`; ready for later append tests.
- `Elias_rig_pose_gallery_v0.1.blend`: separate held-pose gallery, frames 1–10.
- Ten named pose PNGs and `rig_validation.json`.

The gallery samples source frames 61, 360, 780, 1225, 1460, 2227, 2300, 2510, 2629 and 2810. Scene travel is removed by recentering at the actor origin. Rooms, bed, tray and props are not present; this gallery tests deformation, not room contact or continuous motion. Camera scale is held at the maximum required to fit the gallery.

Inspect elbow/knee volume, shoulder/hip joins, wrist orientation and head/neck attachment. The first rig keeps bone wrist targets; the different grip offsets of proxy palms still need retargeting to real fingers/skin before scene integration. ZIP the output folder for readback.

Pure preflight: `python tools/verify_elias_rig.py`. Next gate: Blender evaluated endpoints/scale and finite deformation checks, then visual review. Only after that integrate with SC001 and rerun mesh contact/collision checks.
