# SC001 v0.3 ten-camera desktop review

Evidence: author-supplied run_20261010_213539_047f09f1.zip containing the v0.3 blend, ten PNGs and validation.json. Every PNG was opened and visually inspected at native 1280x720 resolution. Archive provenance SHA256: 7cb6467f77dacf63c1418e7ae7ad941180c84d14daedd8166a954ce8c0f6f0cb. Raw archive/images and private desktop paths are not committed.

## Deterministic evidence

PASS: ten decodable 1280x720 PNGs; ten distinct shot/camera/frame/check mappings match the committed spec; Blender report identifies 5.2.2 LTS, builder 0.3, Workbench, 24fps, frames 1–2760, ten cameras, 52 objects and diagnostic shadows disabled. Recorded script/spec hashes match the committed files with CRLF checkout line endings. The archive contains a nonempty blend; its internal state was not independently loaded in the agent environment. Reported structural checks are desktop script evidence, not a separate blend inspection.

## Visual findings

| Shot | Camera/geometry finding | Outstanding story/performance requirement |
|---|---|---|
| SH001 | Both outside bird boxes and opening visible; bedroom spatial view usable provisionally. Clock display small in wide view. | Sleeping/waking pose absent; standing proxy legs intersect bed. Final clock readability and ordinary morning performance pending. |
| SH002 | Unintended head crop at upper edge; torso fills view. Revise framing before performance blocking. | Rib/shoulder pain and right support arm not staged. |
| SH003 | OXYCODONE label and eight cells contained; two dark cells distinguishable. Insert usable provisionally. | Dark raised boxes are symbols, not convincing empty blister cells. Drawer/prescription context and no-dose action remain unbuilt. |
| SH004 | Kitchen framing tighter and mannequin contained. Clothes/post proxy partly concealed by body and not recognisable as clutter. | Improve simple clutter/tool proxy silhouettes before judging ordered/disordered contrast. |
| SH005 | Head and shower-fixture box visible; lower/right body crop and no bathroom threshold geometry. Cannot establish bathroom setting yet. | Shower response and offscreen water/audio absent; no fluid simulation needed. |
| SH006 | Head cropped; mannequin blocks view of coffee area. Camera requires reframing/line-of-sight review. | Mug/jacket continuity and coffee action remain unbuilt. |
| SH007 | Exact three sentences and MAC readable at native resolution without duplicate shadows. Diagnostic insert passes text containment/readability. | Hand context, reading pace, folding and custody still unbuilt. Orthographic view remains diagnostic. |
| SH008 | Head cropped; isolated torso near entry does not include counter props. Camera requires revised action-zone coverage. | Pocket pause, letter/envelope/keys/mug custody and transition to SC002 remain unbuilt. |
| SH009 | Both bird proxies and Elias head/torso visible. Medium spatial relationship usable provisionally. | Facing/eyeline, dry dialogue and bird appearance/performance pending. |
| SH010 | Both birds and empty bed area visible. End-state framing usable provisionally. | Absence of mannequin does not prove a clear exit; motion path, carried props and final peck pending. |

Root cause: v0.2/v0.3 subject-containment logic covers only SH001/SH004/SH007/SH010. The other six cameras retain initial lens/position guesses. Technical render success and four framing passes cannot be promoted to ten-camera visual approval. Subject bounds alone also cannot detect actor occlusion or establish readable proxy identity.

## Next bounded work

1. Define shot-specific framing subjects for SH002/SH005/SH006/SH008, with deliberate medium framing that retains head/arms and the relevant action area. Re-check line of sight to mug and counter props; do not indiscriminately fit the whole apartment.
2. Improve elementary bed/sitting pose, bathroom threshold, mug, tools and clutter representations enough to judge the planned action spatially. Keep detailed character design, rigs, final lighting and material work deferred.
3. Render replacement diagnostic views and only then start coarse performance/custody blocking. The 115-second timing remains a hypothesis; ten start-frame stills are not a timed animatic.

No complete camera-layout, scene, performance or finished-slice gate passed. Final visual direction and story authority unchanged. This report records review; it does not claim an implemented successor builder.

Repository checks: film workspace verifier PASS; film screenplay verifier PASS; git diff --check PASS. Existing protected KDP/archive binary modifications untouched and excluded.
