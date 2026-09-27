# Blender dual-execution SOP

## Purpose
Use Codex from VS Code to operate Blender through two complementary execution routes while keeping production changes inspectable, reproducible and recoverable.

## Route A — versioned `bpy` automation
Use Python scripts committed to the repository when an operation is repeatable, structural, batchable, safety-critical, or should be reproducible from a known starting state.

Typical uses:
- scene scaffolding
- collection/object naming
- imports and asset linking
- camera and lighting rig construction
- material/node setup
- Geometry Nodes construction
- render configuration
- validation and batch checks
- deterministic scene repair
- batch/headless rendering

Preferred pattern:

```text
shot/scene specification
        ↓
Codex writes/revises versioned Python
        ↓
Blender executes script
        ↓
scene/output validation
        ↓
script + result reviewed
```

Scripts must be stored under the film workspace or repository tooling, not left only in transient chat output.

## Route B — live Blender MCP
Use MCP when the task depends on inspecting or interactively adjusting the currently open Blender scene.

Typical uses:
- inspect scene state
- diagnose geometry/material/rig problems
- interactive camera framing
- artistic light adjustments
- object placement
- small corrective edits
- exploratory node/rig work
- read-back of scene properties before deciding the next action

Preferred pattern:

```text
human/Codex intent
        ↓
MCP scene inspection
        ↓
bounded live change
        ↓
inspect result
        ↓
accept, revise or revert
```

## Route selection rule
Use the **most reproducible route that is practical**.

Choose Route A when:
- the operation may need to be repeated;
- many objects/shots are affected;
- the result can be specified deterministically;
- the operation changes production structure;
- a reusable function/tool can eliminate future manual work.

Choose Route B when:
- the required decision depends on visual inspection;
- the change is exploratory or artistic;
- the active Blender state must be queried before acting;
- the operation is small and not worth formalising yet.

If a useful MCP operation is repeated, promote it into a versioned `bpy` tool.

## Hybrid use
A task may begin through MCP for diagnosis/prototyping and end as committed Python once the desired operation is understood.

## Safety and recovery
1. Canonical manuscript and KDP publication material are outside the Blender agent's write scope.
2. Do not let an AI agent operate on the only copy of a production scene.
3. Save/checkpoint before substantial live MCP changes.
4. Prefer branch/scene checkpoints before destructive or broad operations.
5. Generated Python must not access unrelated filesystem/network locations unless the task explicitly requires and authorises it.
6. Treat arbitrary Python execution through MCP as privileged execution.
7. Never accept a destructive batch operation without first identifying its target scope.

## Validation
After a significant operation, verify the intended state rather than assuming the command succeeded. Depending on the task, validate:
- expected objects/collections exist;
- naming conventions pass;
- asset links resolve;
- cameras/lights exist and have expected settings;
- frame range/FPS/resolution are correct;
- missing textures/dependencies are zero or documented;
- output paths are valid;
- scene saves successfully;
- the intended visual result is confirmed by preview/render when relevant.

## Production principle
Codex is an execution and automation agent. Blender remains the authoritative 3D scene environment. Versioned repository specifications, scripts and registers remain the authoritative record of why the scene was built that way.
