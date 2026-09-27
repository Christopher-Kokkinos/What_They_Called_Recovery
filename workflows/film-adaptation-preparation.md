# Film adaptation preparation workflow

## Purpose
Convert the canonical novel into an explicit screen-adaptation source layer before shot production. The novel remains authoritative source material; the adaptation is a controlled derivative.

## Core rule
Do not translate prose directly into Blender shots.

Use this chain:

```text
canonical manuscript
        ↓
source beats / scene candidates
        ↓
adaptation decisions
        ↓
screenplay
        ↓
production scene packets
        ↓
shot specifications
        ↓
Blender
```

## Stage 1 — source decomposition
Work through the manuscript in canonical order and identify:
- dramatic beats;
- physical locations;
- participating characters;
- visible actions;
- dialogue;
- internal thought/narration;
- exposition;
- transitions;
- information that must reach the audience;
- continuity dependencies.

Do not rewrite the canonical manuscript.

## Stage 2 — adaptation disposition
Register every meaningful source unit in `Active/Film/00_Control/adaptation_register.csv`.

Allowed dispositions:
- `KEEP` — retain substantially as a screen scene/beat.
- `COMPRESS` — retain function/information with reduced duration or dialogue.
- `MERGE` — combine with another source unit/scene.
- `OMIT` — intentionally remove from the film.
- `RELOCATE` — retain but move to a different screen scene/order.
- `VISUALISE` — convert prose, exposition or internal material into visible action/image.
- `VOICEOVER` — retain selected internal/narrative material as spoken narration.
- `SPLIT` — divide one source unit into multiple screen scenes/beats.

Every non-`KEEP` decision requires a concise reason.

## Stage 3 — information preservation check
Before approving an omission/compression/merge, identify what narrative work the source unit performs:
- plot causality;
- character development;
- motivation;
- clue/reveal;
- world information;
- relationship development;
- tension/pacing;
- setup/payoff;
- thematic function.

If the function is still required, record where it is transferred.

## Stage 4 — screenplay
Create the screen-adaptation master as plain-text Fountain screenplay material under `Active/Film/01_Adaptation/Screenplay/`.

Fountain is preferred because it is:
- plain text;
- Git-diffable;
- easy for Codex to read/edit;
- convertible later into formatted screenplay output;
- independent of paid screenplay software.

The screenplay is a film document, not a rewritten novel. It should contain only what the audience can see/hear, except for concise production-relevant description.

## Stage 5 — production scene packets
After screenplay scenes are approved, create one production packet per `SC###` containing:
- source chapter/beat references;
- screenplay scene text/reference;
- purpose of scene;
- characters;
- set/location;
- required props;
- wardrobe/continuity;
- emotional state entering/leaving;
- required information/reveal;
- approximate duration;
- animation/performance requirements;
- audio requirements;
- special production risks.

## Stage 6 — shot specification
Only after the scene packet is approved should the scene be decomposed into `SC###_SH###` shots for Blender.

## Adaptation audit principles
- No source omission is silent.
- No new plot fact is introduced without being marked as an adaptation invention.
- No film decision changes manuscript canon by implication.
- Compression may change presentation, not silently change causality.
- Where several source scenes are merged, preserve chronology/continuity explicitly.
- Internal narration must be deliberately classified as visualised, voiced, transferred to dialogue, or omitted.
- Repeated information may be removed, but the retained carrier must be identified.

## Vertical-slice relationship
The vertical slice should be selected from the adaptation map after enough of the story has been decomposed to understand the scene's dependencies. It should not be chosen solely because an isolated chapter looks visually interesting.
