"""Validate isolated closure/support and rigid packet approach, without bpy."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_envelope_finish import state,START,END,rotate
from elias_envelope_contact import state as prior
from elias_rig_math import bones
from elias_articulation import sub,dot,unit,mul
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
rest=bones(state(889,layout));maximum=0;previous=None;maxbend=0
assert len(rest)==50
for f in range(START,END+1):
 s=state(f,layout);b=bones(s)
 for n in b:assert abs(b[n]['length']-rest[n]['length'])<1e-8,(f,n)
 assert s['_paper_support']=='envelope'
 assert s['_envelope_contacts']['left']['index_active'] or s['_envelope_contacts']['right']['index_active'],('Unsupported packet',f)
 for side in ('left','right'):
  shoulder,elbow,wrist=s['joints'][side+'_arm']
  assert math.dist(wrist,s['_hand_origins'][side])<1e-9
  axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
  bend=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(wrist,elbow)),axis)))));maxbend=max(maxbend,bend)
  if previous:maximum=max(maximum,math.dist(wrist,previous['_hand_origins'][side]))
 if f>=2594:
  expected=rotate(sub(prior(2474,layout)['letter'],prior(2474,layout)['envelope']),s.get('_packet_rotation_x',0))
  assert math.dist(sub(s['letter'],s['envelope']),expected)<1e-9
 previous=s
for side in ('left','right'):
 assert math.dist(state(START,layout)['_hand_origins'][side],prior(START,layout)['_hand_origins'][side])<1e-9
assert maximum<.045,maximum
assert maxbend<65,maxbend
assert state(2550,layout)['_envelope_flap_angle']==0
assert state(END,layout)['_envelope_phase']=='pocket_hold'
assert state(END,layout)['_envelope_contacts']['right']['index_active']
print(json.dumps({'status':'finish_math_pass','frames':END-START+1,'images':122,'max_wrist_step_m':maximum,'max_wrist_bend_degrees':maxbend,'limitations':['No Blender runtime or skin/pocket collision pass','Packet remains held; clothing pocket release pending']}))
