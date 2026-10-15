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

## Shared grip frame (DEC-0063)

Same original checkpoint and builder command. Mug position path retained; experiment now keys up to45-degree mug/grip tilt during the first drink. All four finger planes share one frame rather than individual searches. Pure sampled clearance against all three bars passes for four fingers; thumb and evaluated skin contact still need review. Six poses, twelve images, fresh mug_ folder. Wrist joint remains connected but now articulates; previous neutral-wrist assertion is superseded for this isolated test.

## Diagonal wrap (DEC-0064)

Same command and original source checkpoint. Preserves U bends while moving/rotating whole hand and solving connected arm. Six poses, now fourteen images: six close-ups, six arm views, two extra `_top` images at1460/2510 along mug axis. Check diagonal grip and wrist-side movement in top views; thumb/skin contact and seam remain pending. ZIP entire newest mug_ folder.

## Role-based contacts (DEC-0065; supersedes polygon grip)

Same command and original checkpoint. Builder modifies only the copied diagnostic handle to a78 mm outer height and rebuilds six rig poses: index/middle distal segments inside, thumb above, ring/little below. Source position/timing retained. Fourteen images, fresh mug_ folder. Review crease seating, thumb top contact, support placement, palm gap and wrist continuity. Pure geometry gates pass; rendered skin and continuous movement remain pending. ZIP the entire newest mug_ folder.

## Tapered handle trial (DEC-0066)

Same original checkpoint/command;14 images in fresh mug_ folder. Hand/arm poses unchanged. Shorter outer rail and diagonal lower return replace rectangular bottom; source scene retained. Inspect lower finger clearance and overall handle shape first. Ring/little spacing and exact thumb/crease contacts remain pending subsequent refinement.
