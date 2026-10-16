# DEC-0074 — Parked mug orientation preflight and earlier recovery

2026-10-16. Overnight ea1f667 --full-scene-review completes rig bake/readback loops and returns from rig checks, then fails mug orientation basis error1.4142136466667896 before checkpoint save. No numerical rig summary or .blend saved by that run; source checkpoint untouched. Another bake required; no recovery claim for unsaved process after Blender quit.

Root cause: integrated baseline used body lateral plus ground_forward/world up to orient stationary kitchen mug. In sleeping poses body lateral and fixed ground_forward become parallel (legacy pure basis fails already at frame1); axes are not a proper rotation and Euler conversion cannot preserve them. Trace did not record exact worst Blender frame. Original source also used this invalid combination, but new full-scene readback exposes it. Prior pure target tests omitted rotation-basis validity.

Parked mug now uses stable right-handed table axes((0,-1,0),(1,0,0),(0,0,1)); held mug tilt/body-relative carry unchanged. Source mug/root/prop positions and hand/arm targets retained. Add pure shape/unit/orthogonality/determinant validation and Blender Euler matrix round-trip preflight for every selected frame BEFORE rig bake. Thresholds unchanged. Report orientation worst frame/axis/actual/planned on evaluated mismatch.

Save SC001_integrated_rig_diagnostic.blend and status rig_readback_passed_mug_readback_pending immediately after full rig gate, before mug evaluated readback. Diagnostic checkpoint is not a fully passed scene; normal validated checkpoint remains separate after mug checks. This preserves future completed rig work if a later prop gate fails. Raw checkpoint is for diagnosis, not automatic resume guarantee.

Pure3168-frame integration/palm/basis contract PASS; legacy singular frame1 rejected, old55 mm palm fault regression retained. Existing246-frame mug contract, syntax/workspace/diff checks PASS. Blender Euler preflight and full evaluated rerun still pending. Original input remains safe. No final visual, table/posture or contact acceptance.
