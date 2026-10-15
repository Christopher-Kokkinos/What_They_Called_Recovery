"""Contact-cycle regression: unchanged passed interval and bounded transitions."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/04_Scenes/Automation'),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]
from elias_mug_lifecycle import state,START,END,BODY_DEPTH,BODY_CENTER_Z
from elias_mug_contact import state as passed
from elias_rig_math import bones
from sc001_mug_motion_review import cycle_schedule,second_schedule
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
bake,renders=cycle_schedule();assert bake==list(range(1375,1561)) and len(renders)==48
assert renders[0]==START and renders[-1]==END
reference=bones(state(889,layout));previous=None;max_wrist_step=max_elbow_step=0
for frame in bake:
    s=state(frame,layout);target=bones(s);old=passed(frame,layout)
    assert s['mug']==old['mug'] and s['root']==old['root'] and s['_mug_basis']==old['_mug_basis']
    if 1400<=frame<=1539:assert s==old,'Passed interval changed'
    for n,b in target.items():assert abs(b['length']-reference[n]['length'])<1e-8,(frame,n)
    assert math.dist(target['forearm.L']['tail'],target['hand.L']['head'])<1e-9
    if previous:
        max_wrist_step=max(max_wrist_step,math.dist(s['_hand_origins']['left'],previous['_hand_origins']['left']))
        max_elbow_step=max(max_elbow_step,math.dist(s['joints']['left_arm'][1],previous['joints']['left_arm'][1]))
    previous=s
    if frame<=1400 or frame>=1540:
        table=next(o for o in layout['furniture'] if o['id']=='table')
        assert abs(s['mug'][2]+BODY_CENTER_Z-BODY_DEPTH/2-(table['position'][2]+table['size'][2]/2))<1e-9
        for axis in (0,1):assert abs(s['mug'][axis]-table['position'][axis])+.06<=table['size'][axis]/2,'Cup footprint leaves table'
for a,b in [(1375,1400),(1540,1560)]:
    assert state(a,layout)['_mug_lifecycle']['grip_amount']==(0 if a==1375 else 1)
    if b==1400:assert '_mug_lifecycle' not in state(b,layout)
    else:assert state(b,layout)['_mug_lifecycle']['grip_amount']==0
assert max_wrist_step<.04 and max_elbow_step<.07,'Transition jump'
second,second_images=second_schedule()
assert second==list(range(2430,2511)) and len(second_images)==41
previous=None
for frame in second:
    s=state(frame,layout);old=passed(frame,layout)
    if frame>=2450:assert s==old,'Second carry poses changed'
    assert s['mug']==old['mug'] and s['keys']==old['keys'] and s['root']==old['root']
    assert s['joints']['right_arm']==old['joints']['right_arm']
    assert s['_hand_plan']['right']==old['_hand_plan']['right'],'Right key hand changed'
    target=bones(s)
    for n,b in target.items():assert abs(b['length']-reference[n]['length'])<1e-8,(frame,n)
    assert math.dist(target['forearm.L']['tail'],target['hand.L']['head'])<1e-9
    if previous:
        assert math.dist(s['_hand_origins']['left'],previous['_hand_origins']['left'])<.04
        assert math.dist(s['joints']['left_arm'][1],previous['joints']['left_arm'][1])<.07
    previous=s
assert state(2430,layout)['_mug_lifecycle']['grip_amount']==0
print(json.dumps({'status':'pure_mug_lifecycle_pass','first_cycle_frames':len(bake),'second_pickup_frames':len(second),'second_preview_images':len(second_images),'maximum_first_wrist_step_metres':max_wrist_step,'maximum_first_elbow_step_metres':max_elbow_step,'passed_intervals_unchanged':True,'limitations':['Nominal rail clearance only; evaluated skin and motion visuals pending','Second pickup retains original body/table pending coordinated posture pass']}))
