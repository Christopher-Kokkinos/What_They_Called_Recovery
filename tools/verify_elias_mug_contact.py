"""Connected-wrist regression for the isolated mug experiment."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/04_Scenes/Automation'),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]
from elias_mug_contact import state,FRAMES
from sc001_room_performance import state as baseline
from elias_rig_math import bones
from sc001_mug_motion_review import START,END,BAKE_FRAMES,RENDER_FRAMES
assert BAKE_FRAMES==list(range(1400,1540))
assert RENDER_FRAMES[0]==START and RENDER_FRAMES[-1]==END and len(RENDER_FRAMES)==48
assert set(RENDER_FRAMES)<=set(BAKE_FRAMES)
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
    pose=state(frame,layout);m=pose['_mug_contact_metrics']
    assert m['palm_body_gap_metres']>.015
    assert .0005<=m['thumb_handle_clearance_metres']<.0011
    for digit,q in m['finger_clearance'].items():
        assert q['sampled_handle_clearance_metres']>=.0005
        if digit in ('index','middle'):
            assert q['role']=='loop_insert'
            assert q['sampled_handle_clearance_metres']<.0011,'Inserted fingers not seated near rail'
            for p in (q['crease_local'],q['tip_local']):
                assert -.099<p[0]<-.060 and abs(p[2])<.027,'Distal segments outside loop'
            assert q['proximal_end_local'][1]>.017,'Proximal segment enters handle'
        else:
            assert q['role']=='under_handle_support'
            assert q['crease_local'][2]<-.033,'Support finger not below sloping return'
    assert m['finger_clearance']['ring']['sampled_handle_clearance_metres']<.002,'Ring finger too far from support'
    upper=m['finger_clearance']['middle']['proximal_end_local'][2]
    lower=m['finger_clearance']['ring']['proximal_end_local'][2]
    assert upper-lower<.025,'Excessive upper/lower finger separation'
print(json.dumps({'status':'pure_connected_mug_pass','source_frames':len(frames),'maximum_wrist_axis_angle_degrees':maximum,'limitations':['Role-based contact contract; no force simulation','Blender skin/contact and motion visuals pending']}))
