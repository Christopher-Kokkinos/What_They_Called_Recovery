"""Anatomy, cadence and unchanged-source regression for paper refinements."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_paper_refinement import state,START,END,source_frame,TRANSFER_START,TRANSFER_END
from elias_paper_sequence import state as baseline
from elias_rig_math import bones
from elias_articulation import dot,unit,sub,mul
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
rest=bones(state(889,layout));steps={k:0 for k in ['left_wrist','right_wrist','left_elbow','right_elbow','letter','envelope']};last=None;max_bend=0
for f in range(START,END+1):
 s=state(f,layout);b=bones(s)
 for n in b:assert abs(b[n]['length']-rest[n]['length'])<1e-8,(f,n)
 source=source_frame(f)
 if source is not None:
  a=baseline(source,layout)
  for k in ['joints','_hand_plan','_hand_origins','letter','envelope','fold']:assert s[k]==a[k],(f,k)
 for side in ('left','right'):
  sh,e,w=s['joints'][side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
  bend=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(w,e)),axis)))));max_bend=max(max_bend,bend)
  assert bend<65,(f,side,bend)
  assert math.dist(w,s['_hand_origins'][side])<1e-9
 if last:
  for side in ('left','right'):
   for part,index in [('wrist',2),('elbow',1)]:
    k=side+'_'+part;steps[k]=max(steps[k],math.dist(s['joints'][side+'_arm'][index],last['joints'][side+'_arm'][index]))
  for k in ('letter','envelope'):steps[k]=max(steps[k],math.dist(s[k],last[k]))
 if TRANSFER_START<=f<=TRANSFER_END:
  assert s['_paper_support']=='envelope'
  assert s['_envelope_contacts']['left']['index_active'] and s['_envelope_contacts']['left']['thumb_active']
  assert s['letter']==baseline(2542,layout)['letter'] and s['envelope']==baseline(2542,layout)['envelope']
  assert s['_hand_origins']['right'][2]>1.23,('Unnecessary hand drop',f)
  if f<TRANSFER_END:
   for digit,chain in s['_hand_plan']['right']['chains'].items():
    radius=.010 if digit=='thumb' else .008
    assert max(p[1] for p in chain)+radius<s['envelope'][1]-.085,('Hand crosses envelope mouth',f,digit)
 last=s
for k,v in steps.items():assert v<(.065 if 'elbow' in k else .045),(k,v)
assert state(2240,layout)['fold']==state(2250,layout)['fold']==.5
assert source_frame(2250)==2260 and source_frame(END)==2762
renders=list(range(START,END+1,6));renders+=[] if renders[-1]==END else [END]
print(json.dumps({'status':'paper_refinement_math_pass','poses':END-START+1,'images':len(renders)*2,'max_wrist_bend_degrees':max_bend,'maximum_steps_m':steps,'limitations':['Blender/visual review pending','No complete skin collision/pocket release certification']}))
