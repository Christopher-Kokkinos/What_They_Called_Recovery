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
    assert math.dist(b['forearm.L']['basis'][0],b['hand.L']['basis'][0])<1e-7,'Forearm/hand roll mismatch'
    maximum=max(maximum,s['_mug_contact_metrics']['wrist_axis_angle_degrees'])
for frame in FRAMES:
    residuals=state(frame,layout)['_mug_contact_metrics']['handle_target_residuals_metres']
    for digit in ('index','middle','ring','little'):
        assert residuals[digit]['bend_degrees']==[90,90]
        assert math.isfinite(residuals[digit]['sampled_rail_clearance_metres'])
        points=state(frame,layout)['_hand_plan']['left']['chains'][digit]
        vectors=[tuple(b-a for a,b in zip(p,q)) for p,q in zip(points,points[1:])]
        for u,v in zip(vectors,vectors[1:]):assert abs(sum(a*b for a,b in zip(u,v)))<1e-9,'Finger folded instead of orthogonal U bend'
        assert math.dist(points[0],points[-1])>.018,'Grip opening collapsed'
print(json.dumps({'status':'pure_connected_mug_pass','source_frames':len(frames),'maximum_wrist_axis_angle_degrees':maximum,'limitations':['Neutral aligned wrist test, not final acting','Blender skin/contact and motion visuals pending']}))
