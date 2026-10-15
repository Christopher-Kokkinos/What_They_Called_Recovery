"""Connected-wrist regression for the isolated mug experiment."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/04_Scenes/Automation'),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]
from elias_mug_contact import state,FRAMES
from sc001_room_performance import state as baseline
from elias_rig_math import bones
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text(encoding='utf-8'))
reference=bones(state(889,layout));maximum=0;frames=list(range(1375,1540))+list(range(2430,2511))
for frame in frames:
    s=state(frame,layout);b=bones(s);old=baseline(frame,layout)
    assert s['mug']==old['mug'] and s['root']==old['root'],'Mug/body route changed'
    for n,q in b.items():assert abs(q['length']-reference[n]['length'])<1e-8,(frame,n)
    assert math.dist(b['forearm.L']['tail'],b['hand.L']['head'])<1e-9,'Detached wrist'
    assert s['_mug_contact_metrics']['wrist_axis_angle_degrees']<65,'Excessive wrist bend'
    maximum=max(maximum,s['_mug_contact_metrics']['wrist_axis_angle_degrees'])
for frame in FRAMES:
    pose=state(frame,layout)
    for digit,q in pose['_mug_contact_metrics']['finger_clearance'].items():
        assert q['bend_degrees']==[90,90]
        assert q['sampled_handle_clearance_metres']>=.0009
        points=pose['_hand_plan']['left']['chains'][digit]
        for point in points:assert abs(sum((point[i]-pose['mug'][i])*pose['_mug_basis'][2][i] for i in range(3))-q['grip_height_metres'])<1e-8,'Finger left common grip plane'
print(json.dumps({'status':'pure_connected_mug_pass','source_frames':len(frames),'maximum_wrist_axis_angle_degrees':maximum,'limitations':['Shared mug-local grip and articulated wrist; not final acting','Blender skin/contact and motion visuals pending']}))
