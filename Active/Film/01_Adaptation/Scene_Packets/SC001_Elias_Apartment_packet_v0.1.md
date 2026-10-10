# SC001 — Elias's apartment: production scene packet v0.1

Status: **packet drafted for the first layout test**. Screenplay direction accepted under DEC-0012; production preparation authorised by the author's “okay lets do it” on 2026-10-10. DEC-0021 subsequently accepts the overall visual direction; specific designs, shot specifications, animation and finished vertical slice remain open. DEC-0020 records the scope and judgements.

## Authority and boundary

- Sequence: SEQ-01. Source: Chapter 1, SRC-C01-01 / ADP0001 and SRC-C01-02 / ADP0002; dispositions remain provisionally accepted.
- Film source: [SC001 screenplay](../Screenplay/SC001_Elias_Apartment_draft.fountain) and [accepted scene review](../Screenplay/SC001_Elias_Apartment_review.md).
- Screenplay SHA-256 at packet preparation: `95b545cc0605d0590c7e6267352599a3415132e3c365faba5b5e1408c936cadd`. A screenplay revision requires this packet's dependency check, not silent reuse.
- Entry: Elias wakes late, in pain, intending to stop working for Mac. Exit: he has pocketed notice, taken his keys and left the flat; Mac has not redirected him yet.
- Scope ends at flat departure. Mrs Doran, mailboxes, clamp and airport call belong to SC002–SC004. No Zoe, Mac appearance or invented past-operation flashback.

## Dramatic job

Establish an ordinary, capable, worn man before the assignment. He maintains equipment and a clean kitchen while his clothes and post are neglected. Pain interrupts his morning; prescribed medication is present without a diagnosis being inferred from a drawer. His decision to resign is tangible but not completed. Humour is habitual and brief.

The viewer should leave knowing: this man hurts; he is late; he intends to stop working for Mac; he has practical habits and a dry voice. The viewer need not yet know Sam, previous dependence or the nature of Mac's operation.

## Required beats and provisional timing

These are performance blocks, **not camera shots**. First timing experiment totals 115 seconds; this is an editorial hypothesis, not a measured duration. Retest roughly 90–140 seconds through blocking. Do not add empty holds to meet the project's 2–5 minute finished-slice target. If SC001 naturally stays shorter, record it as a pipeline/layout test and select a suitable wider sample separately.

| Beat | Action and information | First timing hypothesis | Required check |
|---|---|---|---|
| B01 | Two pigeons stamp/peck; eight o'clock, alarm off; Elias wakes in yesterday's clothes. | 15 s | Morning, late awakening and bird count clear without explanatory narration. |
| B02 | Sitting up hurts left ribs; right arm supports him, shoulder objects; prescribed strip with two tablets absent; drawer closed. | 22 s | Weight shift reads; medication shot does not imply taking a dose or inherently wrongful treatment. |
| B03 | Clean kitchen and ordered tools contrast with clothes/post. | 10 s | A few readable contrasts; avoid excessive set dressing. |
| B04 | Shower runs cold after seconds; “Excellent.” Dressing transition remains discreet. | 18 s | Loss of hot water understood through performance/audio; no expensive water simulation required. |
| B05 | Coffee, MAC envelope, exact three-sentence notice; deliberate reread. | 25 s | Letter readable at review size; enough time to understand withdrawal. |
| B06 | Letter folded into inside jacket pocket, hand pause, keys taken. | 15 s | Prop continuity and unresolved choice visible. |
| B07 | “Flat's yours.” Departure; pigeon pecks again. | 10 s | Dry tone, physical exit, ordinary life continuing. |

Keep required dialogue and letter wording from the linked screenplay. Proposed duration, furniture layout and performance blocking are film judgements, not added novel facts. No voiceover or music is needed for the first test.

## Performance and relationship foundations

Elias is stiff, economical and competent, not helpless or theatrically intoxicated. Use clear pauses and physical support before facial detail. Humour is directed at circumstances and birds, not an audience. Never turn shutting the drawer into medical advice or proof of his whole treatment history. SC004's clinic call and SC056's medical help carry later recovery information.

Resignation is a present intention, not already delivered or approved. The pause at his pocket must remain available for SC004, where the assignment interrupts it. Ordinary care and restraint continue in SC002 and SC003; do not force those later traits into a new speech here.

## Space and continuity

One reusable flat set with bedroom, kitchen, window ledge, shower/bathroom implication and entry door. Their precise adjacency, dimensions and architecture are not established by this packet; propose a readable compact arrangement in layout and log it as design. Shower may remain mostly offscreen. Remove walls for camera access only in the production set, not as a story change.

| Item/state | Entry / local action | Handoff or limit |
|---|---|---|
| Pigeons | Two outside on narrow ledge; one pecks twice. | Reuse one pigeon asset with two instances; both remain outside. |
| Clock | Beside fake fireplace; reads 08:00, alarm off. | Readable clock design undecided; not a new digital-device plot. |
| Prescription strip | Drawer slightly open, two tablets absent. | Drawer closes; no dose taken on screen; label/absence readable without private patient data. |
| Notice | White MAC envelope and three-sentence letter. | Fold into inner jacket pocket; still undelivered through SC002–SC003, redirected in SC004. |
| Coffee | Made and taken into morning departure. | Keep reusable mug for SC002 stairwell/door action; exact colour undecided. |
| Clothing/jacket | Previous clothes on waking; dressing transition. | Choose one consistent departure outfit, not yet an approved design. |
| Keys/tools | Keys taken; tools precisely arranged. | Tools show practical habits; do not introduce clamp grinder into this scene as a new action. |

## Minimum asset inventory

The authoritative inventory is [asset_register.csv](../../00_Control/asset_register.csv). These IDs are planned dependencies, not existing assets or proof of licences. Leave canonical paths unassigned until a reusable source is built or selected. Do not duplicate set components as separately built props unless reuse warrants it.

| ID | Minimum use | First-test representation / later requirement |
|---|---|---|
| CHR_Elias | Rise, support body, shut drawer, dress transition, coffee/letter, exit. | Articulated proxy first; hands and upper-body motion matter before face polish. Reusable character rig later. |
| CHR_Pigeon | Two instances, stamping and two pecks. | Simple body/head shapes; linked geometry, independent movement later. |
| SET_EliasFlat | Bed, bedside drawer, fake fireplace, kitchen, ledge, entry, implied bathroom. | Box geometry; drawer as set component, movable front. No full exterior needed. |
| PRP_AlarmClock | Time and off alarm. | Readable placeholder text/state. |
| PRP_PrescriptionStrip | Prescription, two absent tablets. | Flat proxy with missing cells; no drug-brand artwork dependency. |
| PRP_TorchTools | Ordered practical equipment. | Group of simple shapes, no functional mechanism. |
| PRP_ResignationLetter | MAC envelope and exact notice. | Two simple surfaces with readable text; later fold/hand interaction. |
| PRP_EliasJacket | Inner-pocket letter custody. | Proxy costume/pocket indication; integrate with rig later. |
| PRP_Keys | Taken before leaving. | Simple bundle, later hand attachment. |
| PRP_CoffeeMug | Kitchen then stairwell. | One reusable silhouette and scale. |
| PRP_ClothesPost | Selective clutter contrast. | Small reusable dressing group, no invented readable debt notice. |
| PRP_ShowerFixture | Hot-water failure. | Implied fixture; sound/performance before fluid effects. |

## Audio and first-test output

Temporary self-recorded lines or timing markers: “Excellent” and “Flat's yours.” Scratch audio is replaceable, not casting. Foley: bird feet/pecks, drawer, kettle/cup, water stopping/changing, paper, keys, door. Quiet morning ambience. Use original temporary audio or silence; record source/licence before any final external sound. Community voice-group concept remains shelved.

First result should be a rough continuous timing review, not finished rendering: simple geometry, legible key information, provisional lighting, no textures or detailed facial animation. Camera list and frame ranges follow a separate shot specification after packet/design review. No Blender script or scene has been created by this preparation.

## Open design and environment decisions

1. Overall direction accepted under DEC-0021: stylised realism, muted full colour, strong shadow contrast and subtle grain. Exact grade, lighting and grain strength need moving-image review.
2. Elias's appearance, wardrobe and pigeon style; source-backed details separate from design inventions.
3. Desktop evidence now confirms Blender 5.2.2 LTS running, AMD FX-6300 (6 cores/6 threads), 24 GB DDR3 and Radeon RX 5500 XT with about 4 GB GDDR6. VS Code/Codex installation is author-reported. Blender system report detects HIP GPU. Render performance and local execution remain untested; this environment cannot directly inspect Chris's Windows PC.
4. Initial technical settings and execution route. Versioned bpy is the default reproducible route once specifications exist; MCP is optional, not a prerequisite.

## Review criteria

- Story: all seven beats, accepted wording, letter handoff and two-source-unit functions survive.
- Readability: clock, strip and letter understood without zooming into stills; test real-time playback.
- Performance: pain and decision pause legible; no medication moral judgement or unearned menace.
- Pace: measure natural duration; record where letter/physical tasks need more time. Do not certify the whole feature's running time from this sample.
- Reuse/cost: character, mug, jacket and tools remain reusable; no paid dependency; external resources have licence evidence before final use.
- Gate: packet drafted only. Overall visual direction and hardware inventory are now established; next verify local execution, develop shot specifications and rough blockout; completed slice must still cover final assets, animation, lighting, audio and edit.
