"""Bounded envelope phase/support, geometry and fixed-anatomy checks."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_envelope_contact import state,START,END
from elias_rig_math import bones,skin
from elias_articulation import dot,sub,unit,mul
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
rest=bones(state(889,layout));surface=skin(state(889,layout));step=0;previous=None;max_bend=0
assert len(rest)==50
for w in surface['weights']:assert abs(sum(w.values())-1)<1e-8 and all(n in rest for n in w)
for f in range(START,END+1):
    s=state(f,layout);j=s['joints'];definition=bones(s)
    for n,b in definition.items():assert abs(b['length']-rest[n]['length'])<1e-8,(f,n)
    assert s['_paper_support']
    assert s['_envelope_contacts']['left']['index_active'] and s['_envelope_contacts']['left']['thumb_active']
    if f<2340:assert s['letter'][2]==.971 and s['_paper_support']=='table'
    for side in ('left','right'):
        _,elbow,wrist=j[side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
        bend=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(wrist,elbow)),axis)))));max_bend=max(max_bend,bend)
        assert bend<65,(f,side,bend)
        assert math.dist(wrist,s['_hand_origins'][side])<1e-8
        if previous:step=max(step,math.dist(wrist,previous['joints'][side+'_arm'][-1]))
    if s['_insertion']>.80:
        tip=s['_hand_plan']['right']['chains']['thumb'][-1]
        if f<=2420:assert tip[1]+.010<s['envelope'][1]-.085,('Thumb enters slot',f)
        assert not s['_envelope_contacts']['right']['thumb_active']
    if f>=2365:
        env=s['envelope'];origin=s['letter'];mouth=s['_envelope_mouth_angle'];normal=(0,math.sin(mouth),math.cos(mouth))
        front=(env[0],env[1]+.085-.085*math.cos(mouth),env[2]+.008+.085*math.sin(mouth))
        for x in (-.105,.105):
            for y in (-.1485,0):
                for z in (-.001,.003):
                    p=(origin[0]+x,origin[1]+y,origin[2]+z)
                    assert abs(p[0]-env[0])<.109
                    if p[1]>=env[1]-.085:
                        assert p[1]<env[1]+.084
                        assert p[2]>env[2]+.001
                        assert dot(sub(p,front),normal)<-.001,('Paper/front penetration',f)
    previous=s
assert step<.055,step
end=state(END,layout);env=end['envelope'];paper=end['letter']
assert end['_paper_support']=='envelope' and end['_insertion']==1
assert env[1]-.085<paper[1]-.1485 and paper[1]<env[1]+.084
assert state(START,layout)['_envelope_flap_angle']==0
assert abs(end['_envelope_flap_angle']-math.pi)<1e-8
print(json.dumps({'status':'envelope_math_pass','frames':END-START+1,'bones':50,'maximum_wrist_step_m':step,'maximum_wrist_axis_bend_degrees':max_bend,'images':108,'limitations':['Blender/evaluated skin collision review pending','Isolated opening/insertion stage; fold transfer and pocketing excluded']}))
