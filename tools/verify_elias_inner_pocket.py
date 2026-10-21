"""Two-hand inner-pocket anatomy and custody checks."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_inner_pocket import state,START,END,RELEASE,FLOOR,local
from elias_rig_math import bones
from elias_articulation import dot,unit,sub,mul
l=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text());rest=bones(state(889,l));worst=[];steps={};previous=None
for f in range(START,END+1):
 s=state(f,l);b=bones(s);j=s['joints'];p=s['_inner_pocket']
 for n in b:assert abs(b[n]['length']-rest[n]['length'])<1e-8,(f,n)
 for side in ('left','right'):
  sh,e,w=j[side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1);worst.append((math.degrees(math.acos(max(-1,min(1,dot(unit(sub(w,e)),axis))))),f,side))
  if previous:
   for key,k in [('wrist',2),('elbow',1)]:
    name=side+'_'+key;steps[name]=max(steps.get(name,0),math.dist(j[side+'_arm'][k],previous['joints'][side+'_arm'][k]))
 if 21<=f<=40:assert p['opening']>.99 and p['left_active']
 if f<=43:
  # A fixed hand-relative packet transform is required for Child Of custody.
  h=s['_hand_plan']['right'];relative=sub(s['envelope'],h['palm']['center'])
  signature=tuple(dot(relative,axis) for axis in h['palm']['basis'])
  if f==1:bind=signature
  assert math.dist(signature,bind)<1e-8,(f,'Hand-relative packet slip')
 if f>=40:
  w,u,d=local(j,s['envelope']);assert abs(u-(.11+.085)/math.sqrt(2)-FLOOR)<1e-8
  assert abs(w-.10)<1e-8 and abs(d-.205)<1e-8
 assert p['hand_influence']==(1 if f<RELEASE else 0)
 if 7<=f<=55:assert p['left_active']
 previous=s
print('bend',max(worst),'steps',steps)
assert max(worst)[0]<65
assert max(steps.values())<.065
assert any(state(f,l)['_inner_pocket']['opening']<0 for f in range(64,70))
print('INNER_POCKET_MATH_PASS; Blender constraint/shape readback and visual review pending')
