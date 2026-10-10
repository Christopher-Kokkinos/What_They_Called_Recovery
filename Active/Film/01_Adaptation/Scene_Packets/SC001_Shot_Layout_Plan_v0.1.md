# SC001 — provisional shot and layout plan v0.1

Status: first blockout specification under DEC-0022. It implements the accepted screenplay and packet; camera order and timing are editable film judgements. No Blender scene or moving preview exists yet.

Authoritative machine-readable specification: `../../04_Scenes/SC001/SC001_layout_test_spec_v0.1.json`.

## Timing and framing

24 fps, frames 1–2760, 115 seconds. Proposed preview size 1280×720; final delivery settings and rendering engine unselected. These defaults limit the initial review workload; they are not a measured performance claim. Grain and finished surfaces are deferred until timing/legibility can be inspected.

| Shot | Beat | Frames | Seconds | Framing / action | Review check |
|---|---|---|---|---|---|
| SC001_SH001 | B01 | 1–360 | 15 | Window-to-room establishing view: Pigeons outside, clock at eight, Elias wakes | Two pigeons; ordinary morning; alarm off |
| SC001_SH002 | B02 | 361–660 | 12.5 | Medium three-quarter bed view: Elias sits with rib/shoulder pain | Support arm and hesitation legible; no hero pose |
| SC001_SH003 | B02 | 661–888 | 9.5 | Drawer insert: Prescribed strip, two empty cells; drawer closes | No dose taken; distinguish prescription from moral judgement |
| SC001_SH004 | B03 | 889–1128 | 10 | Kitchen and entry medium-wide: Clean surfaces/ordered tools contrasted with post/clothes | Few clear objects; avoid readable invented bills |
| SC001_SH005 | B04 | 1129–1368 | 10 | Bathroom threshold view: Water loses heat; Excellent | Offscreen water and restrained response; no fluid simulation |
| SC001_SH006 | B04 | 1369–1560 | 8 | Kitchen medium: Dressed Elias makes/takes coffee | Transition only; departure jacket and mug consistent |
| SC001_SH007 | B05 | 1561–2160 | 25 | Notice insert with hand context: MAC envelope and exact notice read | Readable at playback; no zoom needed; not yet delivered |
| SC001_SH008 | B06 | 2161–2520 | 15 | Medium at kitchen/entry: Letter folded, inner pocket pause, keys taken | Letter/envelope travel together; mug carried into SC002 |
| SC001_SH009 | B07 | 2521–2640 | 5 | Elias-to-window medium: Flat's yours dialogue | Pigeons remain outside; dry delivery |
| SC001_SH010 | B07 | 2641–2760 | 5 | Window and departing-room hold: Exit and final peck | Clear departure; no new plot reveal |

## Apartment layout proposal

Coordinates are provisional film design, not source canon: metres; X east, Y north, Z up. Overall footprint 10×7 m, height 2.6 m. Bedroom western 4 m; kitchen/entry middle 4 m; bathroom implied to east. Window on west wall; exterior ledge for pigeons; door on south side of kitchen/entry. Keep the fake fireplace/clock beside the bed, a drawer within reach, clean kitchen, ordered tools and contrasting sparse clutter. Initial set uses boxes with removable camera walls. No detailed city exterior, plumbing or neighbour rooms needed.

Map every major object to its registered ID; draw set components from SET_EliasFlat, not duplicate assets. One pigeon geometry reused as two independently movable instances. Elias first represented with simple articulated shapes for weight and hand tasks. The proxy silhouette is not approval of his face, age, clothing details or body design.

Continuity: letter folds into inside jacket pocket, notice remains undelivered, keys and coffee mug leave with Elias. Clock reads eight, two tablets absent, no tablet taken; pigeons remain outside. Shower is mostly implied by sound and performance. SC002 begins outside the flat with his mug.

## Camera principles

Establish geography before inserts; keep action screen direction consistent once blocked. Choose exact positions/lenses by rendered tests, not arbitrary novel claims. Letter insert may fill most of the frame with hand context; maintain source wording and test reading time. Drawer insert communicates prescribed strip/absence without inventing patient data. Medium movement views prioritise body support and hand actions; shadows cannot conceal essential gesture.

Initial preview can use readable proxy labels where necessary. Labels support diagnosis and are removed/replaced in final assets. Final noir contrast/grain are a later look test; do not confuse flat proxy shading or render noise with the approved aesthetic.

## Proposed build and validation

The next automation should create a NEW owned SC001 test scene with named collections, set proxies, character/prop proxies, ten cameras and cut markers. It must not delete objects from an unrelated open scene or overwrite an existing output. Prefer a fresh background Blender process and an output under ignored Active/Film/_local/SC001/. Repository contains the specification and script; generated previews remain local.

Read back frame/FPS/resolution, shot cuts, required objects, camera assignment and saved output. Render selected stills before a full timing preview. Check all seven beats, real-time letter reading, physical pain, mug/letter continuity, two birds and window/exit geography. Benchmark locally before promising full playback speed. The finished-slice gate remains unpassed; measured natural duration may be below two minutes.

## Judgements and revisions

Ten shots split seven performance beats: pain/drawer, shower/transition and final line/peck each separate for legibility. 115 seconds retained from packet. Exact geography invented only as changeable film layout. Every timing or camera change should retain beat links and contiguous coverage in the JSON. Changes affecting a connected scene need a decision-log entry.
