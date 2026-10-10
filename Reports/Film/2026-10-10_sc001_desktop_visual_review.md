# SC001 first desktop execution and image review

Evidence supplied by author on 2026-10-10: terminal log from commit 883a20c; Blender 5.2.2 LTS build d13f752e3b9c; successful save, three render saves and structural validation; four screen photographs (27835.jpg kitchen, 27836.jpg notice, 27834.jpg opening, 27837.jpg open Blender scene). Generated run identifier: run_20261010_211727_a07b1185. Raw screenshots/system paths are not committed.

Observed:
- Background execution, .blend generation and three PNG renders succeeded. Opened Blender scene shows rough set and camera objects.
- Notice image crops beginnings of all three lines on the left. Exact complete text cannot be reviewed in that render.
- Opening shows a solid dark window slab; pigeon proxies are not identifiable in this photograph. Code inspection confirms a slab between interior camera and outside birds.
- Kitchen view cuts off lower mannequin and gives little clear clean/disordered contrast.
- Opening shows checkerboard transparency outside cutaway geometry. This is diagnostic background behaviour, not the intended final look.

Do not infer final grain, render quality or fine readability from photographed screens: camera/screen artefacts are present. No full timing/performance review or finished-slice acceptance occurred.

Root-cause correction: v0.1 fixed camera parameters had no subject-containment checks; window opening used solid box geometry; opaque preview output/background was unspecified. DEC-0024 and builder v0.2 address these with evaluated bounds fitting, hollow bars and explicit RGB/background settings. Letter uses orthographic diagnostic insert; no final cinematography claim.

Agent verification: Python compilation, unchanged screenplay-hash/spec checks, film workspace verifier, film screenplay verifier and git diff --check pass. Code review confirms unique outputs retained; no scene deletion or protected-file write introduced. v0.2 cannot be executed in agent environment (no Blender/bpy), so new API execution, framing, occlusion and readability remain pending desktop evidence. Framing assertions run on the desktop before saving.
