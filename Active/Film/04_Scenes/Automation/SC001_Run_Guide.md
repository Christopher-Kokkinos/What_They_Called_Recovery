# SC001 desktop test — v0.15

Run from Git Bash on `animated-movie`:

```bash
git pull --ff-only
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --background --factory-startup --python-exit-code 1 \
  --python "Active/Film/04_Scenes/Automation/build_sc001_blockout.py" \
  -- --render-shot-review --render-bedside-preview
```

No add-ons/codecs/pip needed. Runs in an isolated background process; refuses loaded files or interactive execution. Each run creates a new ignored folder under `Active/Film/_local/SC001/`, retaining previous runs.

Full-review output (use `--render-shot-review --render-motion-preview`): `SC001_blockout_v0.22.blend`, `validation.json`, ten 1280×720 shot-start PNGs, `motion_preview.html`, a manifest and 480 640×360 preview PNGs. Open HTML beside its image folder in a browser, click Play and pause/scrub. Send the entire run ZIP and terminal ending. Missing/partial output after an error is not a passed run.

Review low bedside drawers against the pillow-end wall, clock on top, medicine inside drawer, corrected bed head direction/side seating, portrait notice, hinged thirds, unchanged-size envelope and reach/grip. Verify SH002 foreground clearance and SH008 handling readability. Workbench is diagnostic: no final lighting/grain/audio or rigs. 120 seconds remains a hypothesis (v0.19 extends only the final exit shot). Preview samples 24fps source at 4fps; runtime not benchmarked.

v0.7 desktop execution was verified, but arm stretching and cabinet obstruction failed visual review. v0.15 uses fixed handling segment lengths with reach assertions and reachable surfaces. Python/pure checks pass; desktop execution and visual approval pending. Paper folding, drawer movement and pocket entry remain coarse proxies. No finished-slice gate passed. DEC-0030 records author corrections and film layout judgements.

Render flags are optional: no flags builds animated blend; `--render-motion-preview` adds player frames; still precedence is `--render-shot-review`, `--render-targeted-review` (SH003/SH007), then `--render-stills` (three original frames).

Current focused command produces SH003/SH007 stills plus blend and validation, without the 460-frame sequence. Review medicine label/two empty cells and notice text. v0.8 desktop execution verified the geometry but those insert views failed; v0.15 framing/text changes remain desktop-pending.

Current command renders ten stills and only SH002/SH003 motion: 88 samples, 22 seconds, 4fps. Open motion_preview.html; review hips/feet, drawer clearance, lean/closure and 200° camera sightline. Validation includes bedside_occlusion_samples/readability_status: blockers are failures to resolve, not approval. Full sequence remains available via --render-motion-preview.

v0.15 connected hip rotation replaces separate torso/head translations. Read bedside_radial_trials and selected camera keys: 200 is tried first, bounded alternate radials may be selected if sampled rays are blocked. Check both empty cells and label visually regardless of ray result. Connected lean/reach remains provisional and requires desktop review.

v0.15 shifts the medicine label 8 cm right within the strip and reduces its font to 0.042 m. Label occlusion now samples a 21×5 grid over full local text bounds. Lean reduces from 0.85 to 0.66 rad (49° to 38°), paired with a 20 cm sideways/8 cm forward seated scoot. This is a smaller coarse lean, not final subtle acting; review foot sliding and mattress support as well as label/empty cells. New outputs never overwrite old runs.

v0.15 adds reusable fixed-length opening leg/spine joints and planted seated ankle targets, plus right rib-support-to-drawer analytic hand reach. This is a segmented diagnostic proxy, not a skinned armature or final roll/walk. The focused 361–888 preview omits waking: for this pass use --render-shot-review --render-motion-preview to include the sit-up. Review knees/feet, mattress support, chest/head alignment and rib-hand placement; supply the whole run ZIP.

v0.15 unifies opening shoulders/elbows/wrists and head orientation with the chest basis, adds a neck bridge, and removes competing opening-arm ownership from the old motion pass. Evaluated arm endpoint checks span 888 source frames. Pure rib-support forearm clearance is checked against the torso front plane. Review actual sit-up attachment, neck/head, protective hand position and drawer release; numerical endpoints do not certify collision-free acting.

v0.15 extends joint ownership across all 2760 frames. Later wrists target mug handle/paper/keys; coffee lifts nearer the face, while final custody offsets stay retained. Exit alternates world-space stance anchors and lifted swing feet; current travel speed is provisional and too brisk for final injured acting. Standing leg lengths retain earlier 0.38/0.40 m proxies, unlike opening 0.60/0.64 m: unify anatomy before final character approval. Seven helpers are hashed. Use full preview and check coffee/paper/exit and the opening regression. See SC001 open issues in project state.

V0.16 repairs the explicit animation interpolation contract after the v0.15 build failed before saving. Run the full command above. An empty failed run folder is expected; each retry creates a new folder. If it fails again, supply the traceback, which now identifies frame and hand. Successful execution still requires visual review.

v0.17 uses shared 0.50/0.52 m leg lengths throughout, with a taller standing pelvis and adjusted body-relative prop targets. Run --render-shot-review --render-motion-preview. Review supine feet/pillow, seated thighs against mattress, floor contact, standing height/head framing, coffee near face, paper/keys reach, jacket position and exit feet. Validation now reports anatomy and all-frame leg length/endpoint errors. Supply the whole run ZIP; pocket concealment and brisk exit are still open.

v0.18 lowers bed/seated placement to match shared legs and adds evaluated seated-thigh clearance checks. Full preview required. Review thigh support, feet, sleeping/pillow placement, drawer reach and window head framing. validation.json now records render_evaluation with matching still/preview camera/head states and window head containment. The preview crop cause remains under investigation; keep the complete run ZIP.

v0.19: full run now has 2880 source frames/120 seconds and 480 preview images. Inspect paper/envelope insertion through frame 2340, exterior hand pause, concealment through window/exit, outgoing mug/keys, slower exit steps and final bird peck. validation.json includes pocket bounds/checked frames and all-frame anatomy/attachment. Packet stays in the scene inside an opaque torso proxy; final jacket pocket and cloth are still pending.

v0.20 tracks Elias through departure, cuts at 2841 to outside pigeons, and retains final peck at 2860. Full review adds three SC001_SH010_phase_frame PNGs (2840/2841/2860) beside the ten shot-start stills. Eight helpers are hashed. Review entire exit for actor/mug/keys visibility, doorway relationship, cut readability and bird/window occlusion. Containment alone does not prove an unobstructed composition.

v0.21 replaces the entry marker with clear opening/flush threshold and outside landing, with a parked-open leaf. Nine helpers hashed. Full preview required: review diagonal passage, feet on threshold/landing, mug/key clearance, parked leaf, arrival framing and pigeon cut. validation.json motion.entry_geometry reports crossing frames, opening margin and stance support error. Door-use performance is not implemented.

v0.22 corrects exit elbow bend after v0.21 failed left-forearm doorway clearance at 2787. Wrists, limb lengths, opening and timing retained. Pure carried-arm volume regression added; runtime errors now print exact point/margin. Use full review command. Empty v0.21 run is failed evidence, not a render result; retain it and rerun in a new directory.
