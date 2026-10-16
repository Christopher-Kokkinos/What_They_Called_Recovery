"""Table handover support, custody, fixed anatomy and transition regression."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_table_handover import state,START,END,WINDOWS
from elias_paper_refinement import state as paper
from elias_table_reach import state as mug
from elias_rig_math import bones
from elias_articulation import dot,unit,sub,mul,cross
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text());rest=bones(state(889,layout));maximum={};previous=None
assert len(rest)==50
for f in range(START,END+1):
 s=state(f,layout);b=bones(s)
 for n in b:assert abs(b[n]['length']-rest[n]['length'])<1e-8,(f,n,b[n]['length'],rest[n]['length'])
 if 1601<=f<=2160:
  a=paper(f+560,layout)
  for k in ('joints','_hand_plan','letter','envelope','mug'):assert s[k]==a[k],(f,k)
 if f>2160:
  a=mug(f+239,layout)
  for k in ('mug','_mug_basis'):assert s[k]==a[k]
  assert s['_hand_plan']['left']==a['_hand_plan']['left']
  basis=s['_packet_basis_override']
  for i in range(3):
   for k in range(3):assert abs(dot(basis[i],basis[k])-(1 if i==k else 0))<1e-8
  assert dot(cross(basis[0],basis[1]),basis[2])>.999999
  assert s['_envelope_contacts']['right']['index_active'] and not s['_envelope_contacts']['left']['index_active']
 if s['_mug_on_table']:assert abs(s['mug'][2]-.09-.97)<1e-9,(f,'Mug support')
 for side in ('left','right'):
  sh,e,w=s['joints'][side+'_arm'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
  bend=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(w,e)),axis)))))
  assert bend<65,(f,side,bend)
 for side in ('left','right'):assert math.dist(s['_hand_origins'][side],s['joints'][side+'_arm'][-1])<1e-9
 if previous:
  for side in ('left','right'):
   for name,index in [('wrist',2),('elbow',1)]:
    k=side+'_'+name;maximum[k]=max(maximum.get(k,0),math.dist(s['joints'][side+'_arm'][index],previous['joints'][side+'_arm'][index]))
  for k in ('mug','letter','envelope'):maximum[k]=max(maximum.get(k,0),math.dist(s[k],previous[k]))
 previous=s
for k,v in maximum.items():assert v<.065,(k,v)
images=sum((len(range(a,b+1,3))+(0 if (b-a)%3==0 else 1))*2 for _,a,b in WINDOWS)
print(json.dumps({'status':'table_handover_math_pass','poses':END-START+1,'images':images,'maximum_steps_m':maximum,'limitations':['No Blender or full skin collision pass','Packet stays held; pocket release and complete scene retiming pending']}))
