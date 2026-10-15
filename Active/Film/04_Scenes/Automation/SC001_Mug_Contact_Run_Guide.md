# Connected mug wrist — six-pose experiment

Git Bash, repository root:

```bash
cd /c/Projects/what_they_called_recovery
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background "Active/Film/_local/SC001/rig_scene_20261014_204455_57a2b099/SC001_rig_performance_v0.1.blend" \
  --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_mug_contact_review.py"
```

Reuses apartment/props, rebuilds only experimental Elias rig at six mug poses. Saves a new mug_ folder under Active/Film/_local/SC001 before rendering six close-ups and six wider arm views. ZIP that entire newest mug_ folder. Input blend retained. No full animation rebuild.

Review wrist attachment, forearm rotation, elbow position and actual mug grip. Neutral aligned wrist is a hypothesis; anatomy/handle clearance still need visual assessment. Intermediate animation, paper/dial/keys revisions and final scene acceptance remain pending. See DEC-0060.

## Handle-target refinement (DEC-0061)

Run the same command against the original rig_scene_20261014_204455_57a2b099 checkpoint. New code rebuilds only six experimental mug poses with handle-coordinate finger/thumb targets and corrected Mug_ framing at every pose. Output remains a fresh mug_ folder with twelve images. Wrist surface seam remains open. Validation records any finger target residuals; six planned review grips are required reachable by pure tests. Skin contact and motion still require review.

## Open U bend shape (DEC-0062)

Same command/six poses/twelve images. Four fingers now use two open orthogonal bends rather than endpoint folding. Validation planned_contacts records signed sampled rail clearance for each finger; negative gap means remaining overlap, not a contact pass. Review U shape, middle segment spacing and thumb opposition; retain connected wrist. Search is cached per pose/layout. Finger/handle fit and wrist surface seam remain open.
