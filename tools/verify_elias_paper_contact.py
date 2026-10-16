"""Paper-edge geometry, fixed anatomy and rig topology regression."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_paper_contact import state,START,END
from elias_rig_math import bones,skin
from elias_articulation import dot,sub,unit,mul
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
rest=bones(state(889,layout));surface=skin(state(889,layout));maximum_step=0;previous=None
assert len(rest)==50
for weights in surface['weights']:assert abs(sum(weights.values())-1)<1e-8 and all(n in rest for n in weights)
for f in range(START,END+1):
    s=state(f,layout);definition=bones(s)
    for name,b in definition.items():assert abs(b['length']-rest[name]['length'])<1e-8,(f,name)
    for side in ('left','right'):
        c=s['_paper_contacts'][side];normal=c['normal'];p=c['contact']
        assert abs(dot(sub(c['index_tip'],p),normal)-(.009+c['opening']))<1e-8
        assert abs(dot(sub(c['thumb_tip'],p),normal)+(c['thumb_offset']+c['opening']))<1e-8
        _,elbow,wrist=s['joints'][side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
        angle=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(wrist,elbow)),axis)))))
        assert angle<(45 if side=='left' else 65),('Wrist-axis bend',f,side,angle)
        assert math.dist(s['_hand_origins'][side],s['joints'][side+'_arm'][-1])<1e-8
    # Contract independently follows the actual folding-half local edge.
    a=math.pi*s['fold'];left=s['_paper_contacts']['left']['surface_contact'];origin=s['letter']
    assert math.dist(left,(origin[0]-.105,origin[1]+.135*math.cos(a),origin[2]+.002+.135*math.sin(a)))<1e-8
    assert s['mug']==(11.24,8.98,1.06)
    if previous:
        maximum_step=max(maximum_step,*(math.dist(previous['joints'][side+'_arm'][-1],s['joints'][side+'_arm'][-1]) for side in ('left','right')))
    previous=s
assert maximum_step<.04,maximum_step
for f in range(2240,2261):
    s=state(f,layout)
    assert s['fold']==.5,('Fold moved during regrip',f)
    assert 'right' in s['_paper_support_hands']
    if 2240<f<2260:assert not s['_paper_contacts']['left']['active']
for f in range(START,END+1):
    s=state(f,layout)
    assert s['_paper_support_hands'],('Unsupported paper',f)
    # Palm frame stays stable: paper cannot dictate a180-degree wrist roll.
    if f>=2220:assert s['_hand_plan']['left']['palm']['basis']==state(2220,layout)['_hand_plan']['left']['palm']['basis']

assert state(START,layout)['fold']==0 and state(END,layout)['fold']==1
print(json.dumps({'status':'paper_contact_math_pass','frames':END-START+1,'bones':50,'maximum_wrist_step_m':maximum_step,'render_images':82,'limitations':['Contact centreline targets only; no complete skin collision proof','Starts with pinch formed; insertion/pocketing excluded','Blender and visual review pending']}))
