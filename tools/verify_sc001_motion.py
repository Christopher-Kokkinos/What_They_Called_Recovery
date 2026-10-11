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
  base=(6.3,4.42,1.02) if frame>=2161 else (4.8,4.65,1.02)
  hand=m.carried_position(frame,(-.4,-.28,1.4 if frame<1540 else 1.05))
  if frame<=1470:t=(frame-1400)/70
  elif frame<1510:t=1
  elif frame<1540:t=1-(frame-1510)/30
  else:t=min(1,(frame-2420)/20)
  goal=tuple(a+(b-a)*t+c for a,b,c in zip(base,hand,(.12,0,.11)))
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
for f in range(810,871):
 local=m.upper_point((.32,0,1.4),f);shoulder=(2.5-local[1],5.8+local[0],.1+local[2]);goal=(3.22,5.80+(f-810)/60*.48,.72)
 assert math.dist(shoulder,goal)<=.70
print('Bed-edge/floor-contact plan and closure reach PASS')

for f in range(750,889):
 assert math.isclose(math.dist(m.upper_point((0,0,1.1),f),m.upper_point((0,0,1.65),f)),.55,abs_tol=1e-10)
 assert m.upper_point((0,0,.75),f)==(0,0,.75)
print('Shared hip pivot and head/torso separation invariants PASS')
