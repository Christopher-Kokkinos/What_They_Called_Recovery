"""Pocket proxy support, rig and release checks; not cloth certification."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_pocket import state,START,END,FLOOR,MOUTH,proxy_boxes
from elias_rig_math import bones
from elias_articulation import sub,dot,unit,mul
l=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text());rest=bones(state(889,l));last=None;steps={};bends=[]
for f in range(START,END+1):
 s=state(f,l);b=bones(s);j=s['joints']
 for n in b:assert abs(b[n]['length']-rest[n]['length'])<1e-8,(f,n)
 for side in ('left','right'):
  sh,e,w=j[side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1);bend=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(w,e)),axis)))));bends.append((bend,f,side))
  assert math.dist(w,s['_hand_origins'][side])<1e-8
 if f>=2820:
  local=sub(s['envelope'],j['pelvis']);assert abs(dot(local,j['up'])-.085-FLOOR)<1e-8
  assert s['_paper_support']=='pocket_floor'
  assert s['envelope']==state(2820,l)['envelope']
 if f>=2820:
  for box in proxy_boxes(s):
   for digit,chain in s['_hand_plan']['right']['chains'].items():
    for a,b in zip(chain,chain[1:]):
     for sample in range(9):
      t=sample/8;p=tuple(x*(1-t)+y*t for x,y in zip(a,b));v=sub(p,box['center'])
      distance=math.sqrt(sum(max(abs(dot(v,axis))-size/2,0)**2 for axis,size in zip(box['basis'],box['size'])))
      assert distance>=(.010 if digit=='thumb' else .008),(f,'Digit/proxy clearance',box['name'],digit)
 if f>2820:assert not s['_envelope_contacts']['right']['index_active'] and s['_pocket_released']
 if last:
  for k,p in [('wrist',j['right_arm'][2]),('elbow',j['right_arm'][1]),('packet',s['envelope'])]:
   old=last['joints']['right_arm'][2 if k=='wrist' else 1] if k!='packet' else last['envelope'];steps[k]=max(steps.get(k,0),math.dist(p,old))
 last=s
assert state(END,l)['_pocket_released']
assert len(range(START,END+1,3))*2+2==150
assert max(bends)[0]<65
assert steps['elbow']<.065 and steps['wrist']<.025 and steps['packet']<.02
print(json.dumps({'status':'pocket_math_pass','poses':221,'images':150,'limitations':['Blender/visual review pending','Rigid open pocket proxy; no cloth or full skin collision proof']}))
