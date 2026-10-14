# SC001 connected-room performance preparation — 2026-10-14

## Result and authority

New versioned choreography and Blender builder implement the requested correction pass in the 14 × 12 m apartment working layout. Author feedback approves that layout as a working foundation. No new layout ZIP or console result was supplied for independent runtime verification. Existing v0.26 builder, source screenplay and canonical manuscript remain unchanged.

New source-frame span: 1–3168 at 24 fps (132 seconds). Earlier shot ranges remain; departure extends by 12 seconds to walk the connected route rather than cross the old open set. New performance specification binds the screenplay hash, layout hash, shot ranges and decision authority.

## Author corrections covered by prepared code

| Register IDs | Prepared change | Remaining evidence |
| --- | --- | --- |
| AR01–AR02 | Bed-contained sleeping shoes, supported side seat, consistent right/left basis, lower elbow poles and flexion limit | Evaluated Blender meshes and visual acting review |
| AR03–AR04, AR07, AR12–AR14 | New rooms, checked furniture/wall clearance, hollow drawer, stable clutter and wardrobe placement | Full desktop review; final furnished assets still proxies |
| AR05 | 0.14 × 0.055 m blister insert with ten cells, two empty | Render readability; no dose action |
| AR06 | Clock proxy retained | Style remodel deferred by author |
| AR08 | A4 letter and envelope supported within table bounds; exact wording | Full-resolution text/shape review |
| AR09 | Right-hand target at actual rear controls; feet supported by tray | Rendered tap grip and cold response |
| AR10, AR15 | Handle-side left grip; first drink rises upright; low elbow on carry | Mug/hand mesh and rendered contact review |
| AR11 | Set mug down, two-hand fold, left supports envelope, right inserts/pockets; keys then second mug pickup | Timing, finger contact, packet and flap readback |
| AR16 | Table keys lie flat; lowered side carry after pickup | Rendered grip review |
| AR17 | Indoor pan/exterior cut/pigeon ending; fixed departure scale | Reframed cameras remain visually unapproved |

None of these visual issues is marked finally closed by code preparation.

## Diagnoses caught during verification

The initial route crossed the bed; it now goes around it. Feet initially intersected the shower tray; support is now its actual 0.16 m surface. Drawer approach initially clipped side/handle geometry and the open drawer crossed knee space; a forward approach waypoint, wrist/palm contact offset and more footward seat correct those intersections. A nearly folded-flat elbow during first mug lift was exposed by a new flexion check; rising for the drink removes that geometry. Lowering papers onto actual table support required explicit wrist-to-palm offsets instead of floating props.

## Validation

`python tools/verify_sc001_room_performance.py`: PASS over all 3,168 frames and 3,120,558 tested body/obstacle pairs. Maximum limb error 1.89e-15 m; minimum body-axis elbow drop 0.13224 m; maximum elbow flexion 151.711° (ceiling 160°); carried mug elbow maximum Z 1.24014 m. Support coverage, packet envelope bounds and negative intersection/invalid-target cases pass. It checks fixed joint lengths, lowered elbows, provisional flexion ceiling, basis handedness, body/furniture/full-height-wall intersections, moving drawer clearance, foot support/coverage, bed containment, paper custody, actual tap/handle targets and packet bounds. Intended palm contact with drawer components and soft pillow contact are explicitly excluded from collision rejection; they require rendered review. Actor self-contact/final skin deformation is not certified.

Blender is unavailable in this environment. The builder is syntax-checked but unexecuted here; it keys exact shared transforms and reads evaluated Blender corners back at contact frames, including sleeping support, floor/tray soles and packet containment. No Blender runtime or visual PASS is claimed.

## Next desktop gate

Run `SC001_Room_Performance_Run_Guide.md`. Upload the complete new `rooms_...` output folder, including validation JSON, stills, 528 preview PNGs, manifest, viewer and `.blend`. Review injury acting, elbow direction, drawer sweep, tap use, mug handle, both-hand fold/insertion, relaxed carry, clutter continuity and departure. No scene acceptance or finished-slice gate.

Additional checks: static layout verifier PASS; film workspace verifier PASS; Python compilation of new modules/builder/verifier PASS; `git diff --check` PASS. No source manuscript, screenplay, Reference or Archive files changed.
