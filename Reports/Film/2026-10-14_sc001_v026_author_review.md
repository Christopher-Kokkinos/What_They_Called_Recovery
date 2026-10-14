# SC001 v0.26 author review — 2026-10-14

## Evidence and scope

Recovered and inspected `run_20261012_104556_ababe7b1.zip`, including validation JSON, preview manifest and the ten cited source frames (61, 271, 505, 1003, 1225, 1411, 2227, 2317, 2587, 2629), plus exit samples 2815/2839. These are source frames at 24 fps, not preview-file ordinals. The preview contains 480 samples at 4 fps over 120 seconds.

Run builder, nine helper modules and layout-spec hashes match commit `dc2c26a88fd27dc7eb8104229c826a5d4e9081cc` when repository LF text is encoded as Windows CRLF. Raw LF hashes differ; no substantive source mismatch is inferred. Blender was not rerun here.

The run records structure validation, not visual approval. Departure records 240 checked frames, 27,000 structural visibility rays, exterior offset (5, -3, 2.8), shared departure scale 7.65047 and pigeon scale 2.4. These are recovered runtime results, not newly executed tests. They do not validate anatomy, prop realism or complete apartment collisions.

## Author correction register

All observations below are author requirements. Inspection supports the broad posing, prop-scale and layout concerns; exact intersecting-object identities remain to be diagnosed in Blender.

| ID | Source frame | Author observation | Required result / disposition |
| --- | --- | --- | --- |
| AR01 | 61 | Feet overhang the bed while sleeping. | Match bed length and sleeping placement to anatomy; reserve side overhang for the seated pose. |
| AR02 | Whole scene; 1003, 1225 | Elbows bend the wrong way. | Establish anatomical bend planes and limits for both arms in every pose; limb-length checks alone are insufficient. |
| AR03 | 271 | Bedside table collides with another object. | Resolve furniture bounds and drawer sweep in the bedroom layout. |
| AR04 | 271 | Books/papers appear on the floor. | Identify and place each clutter asset consistently; distinguish intentional source-backed clutter from misplaced geometry. |
| AR05 | 505 | Oxycodone strip fills the drawer. | Use plausible human-scale blister packaging, much smaller than the drawer; keep medicine inside, clock on top. No dose invention. |
| AR06 | Whole scene | Alarm clock style wrong; author permits it to remain. | DEFERRED: retain current clock for blocking; remodel later. |
| AR07 | 1003 | Elias intersects another object. | Identify blocker and remove body/set intersection through the full action, including transitions. |
| AR08 | 1003 | MAC notice protrudes over table edge. | Keep paper properly supported on the tabletop; preserve approved wording and distinguish MAC notice from resignation letter. |
| AR09 | 1225 | Shower reach uses hidden pretend taps on a pillar. | Animate hand contact with visible rear-wall controls; remove duplicate action targets and make water response readable. |
| AR10 | 1411 | Mug handle on wrong side; grip awkward. | Orient handle for the actual hand and preserve palm/handle alignment during lift, sip, set-down and carry. |
| AR11 | 2227 onward | Paper/envelope action one-handed; mug should be set down. | Explicit sequence: set mug down; both hands fold letter and insert into envelope; one hand pockets packet; pick mug up again. Show each custody transfer. |
| AR12 | 2317 | Unexpected object behind/beside Elias. | Identify object, establish its presence before this shot and keep placement/custody consistent; do not guess its identity from the render. |
| AR13 | Whole apartment | Apartment feels too small; author requests double to triple size. | Develop a larger connected floor plan at unchanged human/prop scale. Provisional interpretation is 2–3 times usable floor area, not 2–3 times every dimension; exact dimensions remain a layout judgment. |
| AR14 | Whole apartment | Missing fireplace, sofa, television and separate rooms. | Provide readable living room, bedroom, kitchen and bathroom. Kitchen: white goods, sink, table/chairs. Bathroom: toilet, wall vent, towel rail, laundry basket. Make fireplace recognisable; existing proxy does not satisfy the visual requirement. |
| AR15 | 2587 | Mug elbow raised to shoulder height. | Keep upper arm and elbow beside torso; raise forearm ahead to carry mug naturally. |
| AR16 | 2629 | Keys held awkwardly. | Carry keys in a relaxed lowered hand at the side; reserve a deliberate reach for door use. |
| AR17 | Exit | Author likes new exit camera panning. | RETAIN camera direction and split interior/exterior coverage intent; revalidate visibility after layout changes. This is not whole-scene acceptance. |

## Inspection distinctions

At source 2227 the mug is visibly on the table, although the nearby hand and coarse staging make custody unclear. The current motion plan also puts it down before letter handling and retrieves it later. This does not resolve AR11: folding and envelope insertion need both hands and clearly shown transfers. Do not discard the author requirement because an event register describes custody correctly.

A `SET_EliasFlat_fake_fireplace` proxy exists in the builder, but the current apartment does not read as the requested furnished, separated rooms. The unidentified object behind Elias may be a coarse wearable/set proxy; its identity is not established by image inspection.

## Revision order and acceptance

1. Define connected room layout and furniture clearances, alongside fixed human proportions. Interpret size by usable floor area provisionally; record chosen dimensions and source-backed set details before rebuilding.
2. Correct shared elbow bend direction, sleeping support and natural carry poses. Verify bends as well as segment lengths and reach.
3. Place and scale furniture, papers, medicine and actual bathroom controls; test body/set and drawer collisions through each action.
4. Rebuild two-handed paper/envelope choreography, mug handle/grip and relaxed key carry, preserving story information and custody.
5. Review transitions, clutter continuity, real contacts and all shots in playback. Preserve accepted exit camera intent and revalidate it against the revised set.

Clock style is deferred by the author. No visual corrections are claimed implemented by this documentation update; no new render is requested yet. Scene acceptance and finished-slice gate remain open.

## Repository validation

`python tools/verify_film_workspace.py`: PASS (no missing files/directories). `git diff --check`: PASS for this control-only update. Historical run evidence remains intact.
