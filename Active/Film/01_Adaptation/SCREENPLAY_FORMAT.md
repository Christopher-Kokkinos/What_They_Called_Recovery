# Screenplay source format

The film adaptation master will use **Fountain-compatible plain text** as its canonical screenplay source format.

## Why
- readable directly in VS Code;
- clean Git diffs;
- straightforward for Codex to edit;
- no paid screenplay application required;
- separates screenplay source from formatted/exported deliverables.

## Authority
The Fountain screenplay is authoritative for the **film adaptation only**. It is not manuscript canon and must never replace or modify the publication master.

## Directory model

```text
01_Adaptation/
    SCREENPLAY_FORMAT.md
    Screenplay/
        WTCR_Screenplay.fountain
    Scene_Packets/
        SC001.md
        SC002.md
        ...
```

The master screenplay file should not be populated until the corresponding source material has passed through the adaptation register.

## Scene text principle
Write what can be seen or heard. Convert novelistic interiority deliberately rather than copying it into action description.

Internal prose must receive an explicit treatment:
- visual action;
- dialogue;
- voiceover;
- environmental storytelling;
- deliberate omission.

## Production separation
Do not place camera directions, lens choices, rig instructions or Blender implementation detail into the screenplay unless they are essential to understanding the storytelling. Those belong in scene packets and shot specifications.
