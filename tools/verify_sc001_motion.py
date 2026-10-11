"""Bounded pure checks; Blender evaluation and visuals are a separate desktop gate."""
import importlib.util
import json
import math
from pathlib import Path

root=Path(__file__).resolve().parents[1]
path=root/'Active/Film/04_Scenes/Automation/sc001_motion.py'
loader=importlib.util.spec_from_file_location('motion',path)
m=importlib.util.module_from_spec(loader);loader.loader.exec_module(m)
spec=json.loads((root/'Active/Film/04_Scenes/SC001/SC001_layout_test_spec_v0.1.json').read_text())
frames=m.preview_frames(spec)
assert len(frames)==460 and frames[0]==1 and frames[-1]==2755
assert len(frames)/4==115
assert {m.shot_at(spec,f)['shot_id'] for f in frames}=={s['shot_id'] for s in spec['shots']}
assert m.custody_at(661)['dose_taken'] is False
assert m.custody_at(870)['prescription']=='closed_drawer'
assert m.custody_at(1540)['mug']=='counter'
assert m.custody_at(2299)['letter_envelope']=='counter'
assert m.custody_at(2340)['letter_envelope']=='inner_pocket'
assert m.custody_at(2440)['keys']=='right_hand' and m.custody_at(2440)['mug']=='left_hand'
for frame in [2440,2510,2521,2640,2720,2760]:
 c=m.custody_at(frame)
 assert c['letter_envelope']=='inner_pocket' and c['keys']=='right_hand' and c['mug']=='left_hand' and c['dose_taken'] is False
for frame in range(1,2761):
 assert m.custody_at(frame)['dose_taken'] is False
 assert all(0<=x<=1 for x in m.pose_weights(frame))
assert m.pose_weights(1)==(1,0) and m.pose_weights(350)==(0,1) and m.pose_weights(889)==(0,0)
assert all(math.isclose(a,b,abs_tol=1e-12) for f in [2720,2760] for a,b in zip(m.root_at(f),(7.5,-.7,0)))
assert len(m.sample_frames(spec))==len(set(m.sample_frames(spec)))
assert all(a['frame']<b['frame'] for a,b in zip(m.EVENTS,m.EVENTS[1:]))
print('SC001 pure motion checks PASS; Blender runtime/visual gate separate')

# Bed geometry: head towards +Y pillow, sitting root beyond +X side, not foot (-Y).
assert m.root_at(1)==(2,5.15,.85)
assert m.root_rotation(1)[0]<0
assert 2.25<m.root_at(350)[0]<2.75 and 5<m.root_at(350)[1]<7
assert math.isclose(m.root_rotation(350)[2],math.pi/2)

# Reach audit across every frame of each active handling interval.
for frame in range(1,2761):
 pos=m.root_at(frame)
 if 1400<=frame<1540 or frame>=2420:
  goal=tuple(a+b for a,b in zip(m.coffee_target(frame),(.12,0,.11)))
  shoulder=tuple(a+b for a,b in zip(pos,(-.32,0,1.4)))
  assert math.dist(goal,shoulder)<=.70
 if frame>=2220:
  if frame>=2380:
   base=(7.05,4.42,1.035);target=m.carried_position(frame,(.35,-.28,1.05));t=min(1,(frame-2380)/30)
  else:
   base=(6.82,4.40,1.10);target=m.carried_position(frame,(.12,-.17,1.2));t=max(0,min(1,(frame-2300)/40))
  goal=tuple(a+(b-a)*t for a,b in zip(base,target));shoulder=tuple(a+b for a,b in zip(pos,(.32,0,1.4)))
  assert math.dist(goal,shoulder)<=.70
print('All-frame handling reach audit PASS (0.70 m maximum)')

assert m.camera_radial((0,0,0),0,2)==(0,2,2.0)
assert math.isclose(m.camera_radial((0,0,0),90,2)[0],2)
assert m.bedside_lean(810)==1 and m.bedside_lean(888)==0

# Seated hips within mattress; foot bottoms at floor; drawer-close reach bounded.
assert 1.25<m.root_at(350)[0]<2.75
assert math.isclose(m.root_at(350)[2]-.05-.05,0,abs_tol=1e-9)
print('Bed-edge/floor-contact plan PASS')

for f in range(750,889):
 assert math.isclose(math.dist(m.upper_point((0,0,1.1),f),m.upper_point((0,0,1.65),f)),.55,abs_tol=1e-10)
 assert m.upper_point((0,0,.75),f)==(0,0,.75)
print('Shared hip pivot and head/torso separation invariants PASS')

# Reusable opening articulation: constant limb lengths and planted seated ankles.
import sys
sys.path.insert(0,str(path.parent))
from elias_articulation import opening_joints,THIGH_LENGTH,CALF_LENGTH,SPINE_LENGTH
for f in range(1,889):
 j=opening_joints(f,m.root_at(f),m.BEDSIDE_LEAN_RADIANS*m.bedside_lean(f))
 for side in ['left','right']:
  a,b,c=j[side]
  assert math.isclose(math.dist(a,b),THIGH_LENGTH,abs_tol=1e-9)
  assert math.isclose(math.dist(b,c),CALF_LENGTH,abs_tol=1e-9)
  if f>=350:assert c==(3.05,5.8+(-.12 if side=='left' else .12),.1)
 assert math.isclose(math.dist(j['pelvis'],j['chest']),SPINE_LENGTH,abs_tol=1e-9)

from elias_articulation import dot,sub,mix,UPPER_ARM_LENGTH,FOREARM_LENGTH
for f in range(1,889):
 j=opening_joints(f,m.root_at(f),m.BEDSIDE_LEAN_RADIANS*m.bedside_lean(f))
 for side in ['left','right']:
  a,b,c=j[side+'_arm']
  assert math.isclose(math.dist(a,b),UPPER_ARM_LENGTH,abs_tol=1e-9)
  assert math.isclose(math.dist(b,c),FOREARM_LENGTH,abs_tol=1e-9)
  assert math.dist(a,c)<.70
 for axis in ['up','lateral','forward']:assert math.isclose(dot(j[axis],j[axis]),1,abs_tol=1e-9)
 assert abs(dot(j['up'],j['lateral']))<1e-9
 if 350<=f<=750:
  a,b,c=j['right_arm']
  for i in range(11):
   # Torso front half-depth .125; forearm half-width .055.
   assert dot(sub(mix(b,c,i/10),j['pelvis']),j['forward'])>=.18-1e-9
print('Shared chest axes, opening arm lengths/reach and rib-support forearm surface clearance PASS')

from sc001_standing import standing_joints
for f in range(889,2761):
 p=m.root_at(f);left=right=None
 if 1400<=f<1540 or f>=2420:left=tuple(a+b for a,b in zip(m.coffee_target(f),(.19,0,.11)))
 if f>=2220:
  if f>=2380:base=(7.05,4.42,1.035);target=m.carried_position(f,(.35,-.28,1.05));t=min(1,(f-2380)/30)
  else:base=(6.82,4.40,1.10);target=m.carried_position(f,(.12,-.17,1.2));t=max(0,min(1,(f-2300)/40))
  right=tuple(a+(b-a)*t for a,b in zip(base,target))
 elif 1190<=f<=1280:right=tuple(a+b for a,b in zip(p,(.25,-.25,1.55)))
 j=standing_joints(f,left,right)
 for side in ['left','right']:
  a,b,c=j[side+'_arm'];assert math.isclose(math.dist(a,b),.36,abs_tol=1e-9);assert math.isclose(math.dist(b,c),.34,abs_tol=1e-9)
  a,b,c=j[side];assert math.isclose(math.dist(a,b),.38,abs_tol=1e-9);assert math.isclose(math.dist(b,c),.40,abs_tol=1e-9)
  assert c[2]>=.1-1e-9
  if f>=2735:assert math.isclose(c[2],.1,abs_tol=1e-9)
  if 2641<=f<2720:
   offset=0 if side=='left' else 6
   phase=(f-2641+offset)%12
   if phase<5:
    nxt=standing_joints(f+1)[side][2]
    assert math.dist(c,nxt)<1e-9
print('Later arm/prop reach, leg lengths, stance planting and final grounded feet PASS')

# Regression: sampled transform curves must follow the same linear path as targets.
from bisect import bisect_left
from sc001_motion_blender import linearise_owned_actions
from types import SimpleNamespace as NS
for layered in [False,True]:
 curves=[NS(data_path=p,keyframe_points=[NS(interpolation='BEZIER')],update=lambda:None) for p in ['location','hide_render']]
 action=NS(is_action_layered=layered)
 if layered:action.layers=[NS(strips=[NS(channelbags=[NS(fcurves=curves)])])]
 else:action.fcurves=curves
 assert linearise_owned_actions([NS(name='test',animation_data=NS(action=action))])==2
 assert [c.keyframe_points[0].interpolation for c in curves]==['LINEAR','CONSTANT']
sampled=m.sample_frames(spec)
def linear_sample(f,fn):
 i=bisect_left(sampled,f)
 if sampled[i]==f:return fn(f)
 a,b=sampled[i-1:i+1];return mix(fn(a),fn(b),(f-a)/(b-a))
def sampled_right(f):
 base=(7.05,4.42,1.035) if f>=2380 else (6.82,4.40,1.10)
 offset=(.35,-.28,1.05) if f>=2380 else (.12,-.17,1.2)
 t=max(0,min(1,(f-(2380 if f>=2380 else 2300))/(30 if f>=2380 else 40)))
 return mix(base,m.carried_position(f,offset),t)
for f in range(889,2761):
 left=tuple(a+b for a,b in zip(linear_sample(f,m.coffee_target),(.19,0,.11))) if 1400<=f<1540 or f>=2420 else None
 right=linear_sample(f,sampled_right) if f>=2220 else tuple(a+b for a,b in zip(m.root_at(f),(.25,-.25,1.55))) if 1190<=f<=1280 else None
 standing_joints(f,left,right)
print('Explicit legacy/layered interpolation and sampled all-frame reach PASS')
