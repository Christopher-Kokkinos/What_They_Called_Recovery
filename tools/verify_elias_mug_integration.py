"""All-frame pure target contract plus continuity checks around mug joins."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/04_Scenes/Automation'),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]
from elias_mug_integration import state,WINDOWS
from elias_mug_lifecycle import state as cycle
from elias_mug_contact import state as held
from sc001_room_performance import state as source
from elias_rig_math import bones
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
reference=bones(state(889,layout));max_steps={};previous=None
for frame in range(1,3169):
    s=state(frame,layout);old=source(frame,layout);target=bones(s)
    for field in ('root','mug','keys','letter','envelope'):assert s[field]==old[field],(frame,field)
    for name,b in target.items():assert abs(b['length']-reference[name]['length'])<1e-8,(frame,name)
    assert math.dist(target['forearm.L']['tail'],target['hand.L']['head'])<1e-9
    if 1387<=frame<=1560 or 2430<=frame<=2510:assert s==cycle(frame,layout),(frame,'Passed cycle changed')
    if frame>=2511:assert s==held(frame,layout),(frame,'Carry target changed')
    if previous:
        for name,a,b in WINDOWS:
            if a<frame<=b:
                wrist=math.dist(s['joints']['left_arm'][-1],previous['joints']['left_arm'][-1])
                elbow=math.dist(s['joints']['left_arm'][1],previous['joints']['left_arm'][1])
                chest=math.dist(s['joints']['chest'],previous['joints']['chest'])
                assert wrist<.065 and elbow<.08 and chest<.045,(frame,name,wrist,elbow,chest)
                max_steps[name]=max(max_steps.get(name,0),wrist)
    previous=s
print(json.dumps({'status':'pure_mug_integration_pass','source_frames':3168,'left_wrist':'connected','maximum_wrist_steps_metres':max_steps,'limitations':['All-frame pure targets only; Blender boundary clips/readback pending','Table/posture and exact skin contacts remain open']}))
