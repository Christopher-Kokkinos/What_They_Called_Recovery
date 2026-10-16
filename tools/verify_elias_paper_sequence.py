"""Continuous paper joins: fixed anatomy, support and preserved accepted clips."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_paper_sequence import state,START,END,ENVELOPE_START,envelope_frame
from elias_envelope_contact import state as env
from elias_envelope_finish import state as finish
from elias_rig_math import bones
from elias_articulation import dot,unit,sub,mul
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
rest=bones(state(889,layout));steps={k:0 for k in ['left_wrist','right_wrist','left_elbow','right_elbow','letter','envelope']};previous=None
for f in range(START,END+1):
 s=state(f,layout);b=bones(s)
 for side in ('left','right'):
  sh,e,w=s['joints'][side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
  bend=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(w,e)),axis)))))
  assert bend<65,('Wrist bend',f,side,bend)
  assert math.dist(w,s['_hand_origins'][side])<1e-9
 if 2280<f<=2316:
  c=s['_paper_contacts']['left'];h=s['_hand_plan']['left']
  assert abs(h['chains']['index'][-1][2]-c['surface_contact'][2]-.009)<1e-9
  assert abs(h['chains']['thumb'][-1][2]-c['surface_contact'][2]+.013)<1e-9
 for n in b:assert abs(b[n]['length']-rest[n]['length'])<1e-8,(f,n)
 if previous:
  for side in ('left','right'):
   for part,index in [('wrist',2),('elbow',1)]:
    k=side+'_'+part;steps[k]=max(steps[k],math.dist(s['joints'][side+'_arm'][index],previous['joints'][side+'_arm'][index]))
  for k in ('letter','envelope'):steps[k]=max(steps[k],math.dist(s[k],previous[k]))
 if 2316<=f<ENVELOPE_START:assert abs(s['letter'][2]-.971)<1e-9,('No table support',f)
 if f>=ENVELOPE_START:
  source=envelope_frame(f);a=env(source,layout) if source<=2474 else finish(source,layout)
  for k in ['_hand_plan','_hand_origins','letter','envelope']:assert s[k]==a[k],(f,k)
 previous=s
for k,v in steps.items():assert v<(.065 if 'elbow' in k else .045),(k,v)
renders=list(range(START,END+1,6));renders+=[] if renders[-1]==END else [END]
assert len(renders)*2==204
print(json.dumps({'status':'paper_sequence_math_pass','frames':END-START+1,'maximum_steps_m':steps,'limitations':['Blender and visual review pending','Pocket remains held; no full skin collision certification']}))
