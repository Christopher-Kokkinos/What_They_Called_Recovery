"""Joined custody, anatomical continuity and unchanged source-clip regression."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_pocket_handover import state,END,ATTACH,RELEASE,POCKET_END,PICKUP_START,PAPER_BASIS
from elias_inner_pocket import state as pocket
from elias_table_reach import state as mug
from elias_rig_math import bones
from elias_articulation import sub,dot,mul,unit,cross
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
rest=bones(state(889,layout));previous=None;maximum={};worst=0
assert len(rest)==50
for f in range(1,END+1):
 s=state(f,layout);j=s['joints'];B=s['_packet_basis_override']
 for name,b in bones(s).items():assert abs(b['length']-rest[name]['length'])<1e-8,(f,name)
 for i in range(3):
  for k in range(3):assert abs(dot(B[i],B[k])-(i==k))<1e-8
 assert dot(cross(B[0],B[1]),B[2])>.999999
 for side in ('left','right'):
  sh,e,w=j[side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1);angle=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(w,e)),axis)))));worst=max(worst,angle);assert angle<65,(f,side,angle)
 if 56<=f<=96:
  contact=tuple(s['envelope'][i]-.08*B[0][i]-.03*B[1][i] for i in range(3))
  for digit,gap in [('index',.016),('thumb',-.011)]:assert abs(dot(sub(s['_hand_plan']['left']['chains'][digit][-1],contact),B[2])-gap)<1e-8,(f,'Supported regrip',digit)
 if 97<=f<RELEASE:
  h=s['_hand_plan']['right'];relative=sub(s['envelope'],h['palm']['center']);signature=tuple(dot(relative,axis) for axis in h['palm']['basis'])
  if f==97:bind=signature
  assert math.dist(signature,bind)<1e-8,(f,'Held packet slip')
 if ATTACH<=f<=POCKET_END:
  source=pocket(f-ATTACH+1,layout)
  for key in ('joints','_hand_plan','envelope','letter','_packet_basis_override'):assert s[key]==source[key],(f,key)
 if f>=PICKUP_START:
  source=mug(2400+f-PICKUP_START,layout)
  assert s['mug']==source['mug'] and s['_mug_basis']==source['_mug_basis']
  if f>=PICKUP_START+30:assert s['_hand_plan']['left']==source['_hand_plan']['left']
 assert s['_inner_pocket']['hand_influence']==(1 if ATTACH<=f<RELEASE else 0)
 if s['_mug_on_table']:assert abs(s['mug'][2]-.09-.97)<1e-8
 if previous:
  for side in ('left','right'):
   for name,i in [('elbow',1),('wrist',2)]:
    key=side+'_'+name;maximum[key]=max(maximum.get(key,0),math.dist(j[side+'_arm'][i],previous['joints'][side+'_arm'][i]))
   for digit in ('index','thumb'):
    key=side+'_'+digit;maximum[key]=max(maximum.get(key,0),math.dist(s['_hand_plan'][side]['chains'][digit][-1],previous['_hand_plan'][side]['chains'][digit][-1]))
  for key in ('envelope','letter','mug'):maximum[key]=max(maximum.get(key,0),math.dist(s[key],previous[key]))
 previous=s
assert max(maximum.values())<.065,maximum
print(json.dumps({'poses':END,'maximum_step_m':maximum,'maximum_wrist_bend_deg':worst,'status':'pocket_handover_math_pass','runtime_visual':'pending'}))
