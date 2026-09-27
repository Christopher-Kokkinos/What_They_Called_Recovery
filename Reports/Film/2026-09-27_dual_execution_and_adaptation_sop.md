# WTCR Film SOP Decision — 2026-09-27

## Locked decisions

### 1. Blender dual-execution SOP
Codex/VS Code will use two Blender execution routes:
- **Route A:** versioned `bpy` Python for repeatable, structural, batch and reproducible work.
- **Route B:** live Blender MCP for active-scene inspection, diagnosis and bounded interactive/artistic changes.

Repeated or production-critical MCP operations should be promoted into versioned Python.

Binding workflow:
- `workflows/blender-dual-execution-sop.md`

### 2. Adaptation must precede Blender scene production
Raw novel prose will not be translated directly into Blender shots.

Locked chain:

```text
canonical manuscript
        ↓
source decomposition
        ↓
film treatment / narrative spine
        ↓
sequence outline
        ↓
adaptation decisions
        ↓
Fountain screenplay
        ↓
production scene packets
        ↓
shot specifications
        ↓
Blender production
```

Binding workflow:
- `workflows/film-adaptation-preparation.md`

### 3. Adaptation decisions are explicit
Source units may be classified as:
- KEEP
- COMPRESS
- MERGE
- OMIT
- RELOCATE
- VISUALISE
- VOICEOVER
- SPLIT

All non-KEEP decisions require a reason. Narrative information removed from one source location must be traced to its new carrier when still required.

### 4. Canon separation
The novel/publication master remains canonical source material. Film screenplay and production documents are derivative and must not silently alter manuscript canon.

### 5. Screenplay source format
The canonical film screenplay source will use Fountain-compatible plain text for VS Code/Codex/Git compatibility.

## Current phase
`adaptation_preparation`

The vertical-slice selection remains blocked until enough of the story has been decomposed and outlined to understand candidate scenes' dependencies.

## Manuscript impact
None. This decision changes film-production governance and derivative-work structure only.
