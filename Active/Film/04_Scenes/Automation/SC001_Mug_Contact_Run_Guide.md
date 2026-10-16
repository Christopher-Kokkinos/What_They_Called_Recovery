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

## Contact seating (DEC-0067)

Same command and original checkpoint;14 images. Tapered handle retained. Index/middle crease seating and thumb extension refined; lower pair raised closer to upper pair/return. Review thumb top contact, ring support, little-finger spacing, distal crease contact and skin intersections. New quantitative nominal contact bounds pass, rendered surface contact pending. ZIP newest mug_ folder.

## Bounded motion test (DEC-0068)

From repository root, reuse the original rig checkpoint:

```bash
cd /c/Projects/what_they_called_recovery
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background "Active/Film/_local/SC001/rig_scene_20261014_204455_57a2b099/SC001_rig_performance_v0.1.blend" \
  --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_mug_contact_review.py" \
  -- --motion-preview
```

New **mug_motion_...** folder under Active/Film/_local/SC001. Bake/check140 integer frames1400–1539; render48 PNGs640x360. Open **motion_preview.html** in a browser from its folder, click Play or scrub. Keep motion_frames beside HTML. Original timing24 fps, preview samples8 fps with exact source timestamps. This starts with grip formed and returns towards table; approach/release, exact placement at1540 and later carry excluded. Review wrist/arm continuity, handle slipping, mug tilt and occlusion. This is a bounded motion test, not full-scene/contact acceptance. ZIP the entire newest mug_motion_ folder. Default command without flag still produces14 stills.

## Contact cycle (DEC-0069)

Use the original checkpoint and add **-- --contact-cycle** (instead of --motion-preview). New **mug_cycle_...** folder.186 integer frames1375–1560,48 motion PNGs640x360 and4 contact close-ups1387/1399/1544/1550. Open motion_preview.html, then review contact stills. Passed1400–1539 poses retained; source cup top/handle/motion retained with copied body extended20 mm downward for table support. Evaluate grip formation, supported release and withdrawal. This is a bounded contact-cycle prototype; transitions into surrounding scene/later carry remain pending. ZIP entire newest mug_cycle_ folder.

## Second pickup (DEC-0070)

Same original checkpoint and builder, use **-- --second-pickup**. Fresh **mug_second_...** folder:81 integer frames2430–2510,41 motion images640x360 plus4 contact closeups2430/2440/2450/2510. Open motion_preview.html and review stills, then ZIP entire folder. Passed carry poses2450–2510 retained; right arm/key geometry/targets retained, not accepted as final key action. Original checkpoint mug body used; table/posture and20 mm support gap explicitly deferred. Historical --contact-cycle retains extended trial body for reproducibility. Whole-scene integration pending.

## Boundary joins (DEC-0071)

Same original checkpoint and builder, use **-- --join-review**. New **mug_joins_...** folder: four subfolders first_approach/release_to_rest/second_approach/carry_join,62 motion images total plus4 root contact closeups. Open **review_index.html** and each linked player, then inspect closeups1374/1561/2429/2511. ZIP entire newest mug_joins_ folder.175 disjoint integer poses are baked/read back; saved .blend defaults to first clip, gaps between clips are NOT whole-scene animation validation. Original body/table and known support gap retained. Initial approach lengthened; source1561 pop smoothed; scene room cuts preserved. Blender boundary/skin/roll review pending before full-scene bake.

## Palm mapping repair (DEC-0072)

If --join-review fails at palm target mapping~0.055 m, pull update and rerun the identical command against the original checkpoint. Integrated rig now uses49 bones with independent left palm control; all earlier diagnostic modes keep48 bones.100-micron evaluated palm gate remains unchanged. New output folder only after a successful build; failed folder can remain. Same four clips/62 motion images+4 closeups; inspect review_index.html after successful execution.

## Continuous scene bake / overnight review (DEC-0073)

Same original checkpoint/builder, use **-- --full-scene-review**. New **sc001_integrated_...** folder.3168 rig and mug integer-frame readbacks, then save **SC001_integrated_rig_v0.1.blend** and validation before rendering529 PNGs640x360. Existing source cameras/shot cuts retained. Progress prints RIG BAKE, RIG READBACK and FULL SCENE REVIEW; runtime hardware-dependent. Open **motion_preview.html** after completion; partial player/manifest retained if render stops. ZIP entire newest sc001_integrated_ folder. Computer must remain awake; screen may turn off. This is sampled4fps review of24fps bake, not final frames/scene acceptance. Deferred table/posture/skin/contact corrections remain open.

## Full-scene parked orientation repair (DEC-0074)

After overnight mug orientation mismatch1.4142, pull and rerun identical --full-scene-review against original checkpoint. Stable parked table axes replace invalid sleeping body/ground combination. All basis/Euler preflight runs before rig bake. After rig gates, **SC001_integrated_rig_diagnostic.blend** saves with pending-mug status; this diagnostic is not a validated scene. Normal **SC001_integrated_rig_v0.1.blend** still requires mug readback pass before renders. Previous failed process exited before saving, so another bake is necessary. Same529-image output/player; original input remains unchanged.
