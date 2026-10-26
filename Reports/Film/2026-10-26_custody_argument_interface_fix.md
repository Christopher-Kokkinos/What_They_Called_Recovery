# Custody call argument fix

Author Blender5.2.2 run at f13580d stopped before rendering: custody accepts4–8 positional arguments but builder supplied9. Root cause: SUPPORT_EDGE was inadvertently included in the custody call while adding it to the movement-provider import for the regrip surface check. It is not a custody parameter.

Replace positional scheduling arguments with an explicit options dictionary containing only start/end/attach/release. Keep SUPPORT_EDGE for the grip-plane gate. No pose, grip, clearance, custody timing or tolerance changes.

Added verify_paper_custody_interface.py: parse the actual builder call/options, bind both standalone and joined modes against the actual function signature without bpy, and verify the legacy9-argument pattern raises TypeError. PASS. Python compilation, verify_film_workspace.py and git diff --check pass.

Blender unavailable locally. Runtime/visual review still pending; same --pocket-handover-review rerun required. The failed run did not validate the new custody/clearance gates or produce review renders. This is an implementation error, not a device/setup fault.
