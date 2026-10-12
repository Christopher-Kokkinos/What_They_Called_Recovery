"""Bounded pure checks; Blender evaluation and visuals are a separate desktop gate."""
import importlib.util
import json
import math
from pathlib import Path

root=Path(__file__).resolve().parents[1]
path=root/'Active/Film/04_Scenes/Automation/sc001_motion.py'
import sys
sys.path.insert(0,str(path.parent))
loader=importlib.util.spec_from_file_location('motion',path)
m=importlib.util.module_from_spec(loader);loader.loader.exec_module(m)
spec=json.loads((root/'Active/Film/04_Scenes/SC001/SC001_layout_test_spec_v0.1.json').read_text())
frames=m.preview_frames(spec)
assert len(frames)==480 and frames[0]==1 and frames[-1]==2875
assert len(frames)/4==120
assert {m.shot_at(spec,f)['shot_id'] for f in frames}=={s['shot_id'] for s in spec['shots']}
assert m.custody_at(661)['dose_taken'] is False
assert m.custody_at(870)['prescription']=='closed_drawer'
assert m.custody_at(1540)['mug']=='counter'
assert m.custody_at(2299)['letter_envelope']=='counter'
assert m.custody_at(2340)['letter_envelope']=='inner_pocket'
assert m.custody_at(2440)['keys']=='right_hand' and m.custody_at(2440)['mug']=='left_hand'
for frame in [2440,2510,2521,2640,m.EXIT_ARRIVAL,m.SCENE_END]:
 c=m.custody_at(frame)
 assert c['letter_envelope']=='inner_pocket' and c['keys']=='right_hand' and c['mug']=='left_hand' and c['dose_taken'] is False
for frame in range(1,m.SCENE_END+1):
 assert m.custody_at(frame)['dose_taken'] is False
 assert all(0<=x<=1 for x in m.pose_weights(frame))
assert m.pose_weights(1)==(1,0) and m.pose_weights(350)==(0,1) and m.pose_weights(889)==(0,0)
assert all(math.isclose(a,b,abs_tol=1e-12) for f in [m.EXIT_ARRIVAL,m.SCENE_END] for a,b in zip(m.root_at(f),(7.5,-.7,0)))
assert len(m.sample_frames(spec))==len(set(m.sample_frames(spec)))
assert all(a['frame']<b['frame'] for a,b in zip(m.EVENTS,m.EVENTS[1:]))
print('SC001 pure motion checks PASS; Blender runtime/visual gate separate')

# Bed geometry: head towards +Y pillow, sitting root beyond +X side, not foot (-Y).
assert m.root_at(1)==(2,5.15,.65)
assert m.root_rotation(1)[0]<0
assert 2.25<m.root_at(350)[0]<2.75 and 5<m.root_at(350)[1]<7
assert math.isclose(m.root_rotation(350)[2],math.pi/2)

# Reach audit across every frame of each active handling interval.
for frame in range(1,m.SCENE_END+1):
 pos=m.root_at(frame)
 if 1400<=frame<1540 or frame>=2420:
  goal=m.mug_grip(frame,(.12,0,.11))
  shoulder=tuple(a+b for a,b in zip(pos,(-.32,0,1.4)))
  assert math.dist(goal,shoulder)<=.70
 if frame>=2220:
  if frame>=2380:
   base=(7.05,4.42,1.035);target=m.carry_position(frame,m.CARRIED_KEYS_OFFSET);t=min(1,(frame-2380)/30)
  else:
   base=(6.82,4.40,1.10);target=m.pocket_position(frame);t=max(0,min(1,(frame-2300)/40))
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
for f in range(889,m.SCENE_END+1):
 p=m.root_at(f);left=right=None
 if 1400<=f<1540 or f>=2420:left=m.mug_grip(f)
 if f>=2220:
  if f>=2380:base=(7.05,4.42,1.035);target=m.carry_position(f,m.CARRIED_KEYS_OFFSET);t=min(1,(f-2380)/30)
  else:base=(6.82,4.40,1.10);target=m.pocket_position(f);t=max(0,min(1,(f-2300)/40))
  right=tuple(a+(b-a)*t for a,b in zip(base,target))
  if 2300<=f<2380:right=tuple(a+b for a,b in zip(right,(0,-.12,0)))
 elif 1190<=f<=1280:right=tuple(a+b for a,b in zip(p,m.SHOWER_HAND_OFFSET))
 j=standing_joints(f,left,right)
 for side in ['left','right']:
  a,b,c=j[side+'_arm'];assert math.isclose(math.dist(a,b),.36,abs_tol=1e-9);assert math.isclose(math.dist(b,c),.34,abs_tol=1e-9)
  a,b,c=j[side];assert math.isclose(math.dist(a,b),THIGH_LENGTH,abs_tol=1e-9);assert math.isclose(math.dist(b,c),CALF_LENGTH,abs_tol=1e-9)
  assert c[2]>=.1-1e-9
  if f>=m.EXIT_ARRIVAL+15:assert math.isclose(c[2],.1,abs_tol=1e-9)
  if 2641<=f<m.EXIT_ARRIVAL:
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
 offset=m.CARRIED_KEYS_OFFSET if f>=2380 else m.POCKET_OFFSET
 t=max(0,min(1,(f-(2380 if f>=2380 else 2300))/(30 if f>=2380 else 40)))
 return mix(base,m.carry_position(f,offset) if f>=2380 else m.pocket_position(f),t)
for f in range(889,m.SCENE_END+1):
 left=tuple(a+b for a,b in zip(linear_sample(f,m.coffee_target),m.carry_vector(f,(.19,0,.11)))) if 1400<=f<1540 or f>=2420 else None
 right=linear_sample(f,sampled_right) if f>=2220 else tuple(a+b for a,b in zip(m.root_at(f),m.SHOWER_HAND_OFFSET)) if 1190<=f<=1280 else None
 if 2300<=f<2380:right=tuple(a+b for a,b in zip(right,(0,-.12,0)))
 standing_joints(f,left,right)
print('Explicit legacy/layered interpolation and sampled all-frame reach PASS')

# One anatomy at every shot, including the seated-to-standing editorial cut.
for f in range(1,m.SCENE_END+1):
 j=opening_joints(f,m.root_at(f),m.BEDSIDE_LEAN_RADIANS*m.bedside_lean(f)) if f<=888 else standing_joints(f)
 assert math.isclose(math.dist(j['pelvis'],j['chest']),SPINE_LENGTH,abs_tol=1e-9)
 for side in ['left','right']:
  hip,knee,ankle=j[side]
  assert math.isclose(math.dist(hip,knee),THIGH_LENGTH,abs_tol=1e-9)
  assert math.isclose(math.dist(knee,ankle),CALF_LENGTH,abs_tol=1e-9)
  if f>=350:assert ankle[2]>=.1-1e-9
sleep=opening_joints(1,m.root_at(1),0)
assert all(5<=sleep[side][2][1]<=7 for side in ['left','right'])
seated=opening_joints(350,m.root_at(350),0)
assert 1.25<seated['pelvis'][0]<2.75
assert all(seated[side][1][0]>2.75 and seated[side][2][0]>2.75 for side in ['left','right'])
print('All scene frames share anatomy; supine feet on bed and seated knees beyond side PASS')

# Seated thigh proxy surfaces over the bed must clear its top, not just endpoints.
from elias_articulation import BED_TOP_HEIGHT,BED_SIDE_X,unit,mul,add
minimum_clearance=float('inf')
for f in range(350,889):
 j=opening_joints(f,m.root_at(f),m.BEDSIDE_LEAN_RADIANS*m.bedside_lean(f))
 for side in ['left','right']:
  a,b,c=j[side];direction=unit(sub(b,a));normal=(direction[2],0,-direction[0])
  for i in range(101):
   center=mix(a,b,i/100)
   for sign in [-1,1]:
    edge=add(center,mul(normal,sign*.09))
    if edge[0]<=BED_SIDE_X:
     minimum_clearance=min(minimum_clearance,edge[2]-BED_TOP_HEIGHT)
assert minimum_clearance>=0
print(f'Seated thigh cross-section clearance PASS, minimum {minimum_clearance:.6f} m; Blender surface validation separate')

# Packet is geometrically inside the upper torso proxy after insertion, not hidden/deleted.
from elias_articulation import STANDING_HIP_HEIGHT
for f in range(2340,m.SCENE_END+1):
 p=m.pocket_position(f);r=m.root_at(f);angle=m.standing_yaw(f)
 dx,dy=p[0]-r[0],p[1]-r[1]
 local=(dx*math.cos(angle)+dy*math.sin(angle),-dx*math.sin(angle)+dy*math.cos(angle),p[2]-(r[2]+STANDING_HIP_HEIGHT+SPINE_LENGTH*.75))
 assert abs(local[0])+.11<.225
 assert abs(local[1])+.005<.125
 assert abs(local[2])+.055<SPINE_LENGTH/4
speed=math.dist(m.root_at(2640),m.root_at(m.EXIT_ARRIVAL))/((m.EXIT_ARRIVAL-2640)/24)
assert .9<speed<1.1
assert m.SCENE_END-m.EXIT_ARRIVAL>=40
print(f'Packet volume and revised exit speed PASS ({speed:.3f} m/s); final pacing remains provisional')

from sc001_departure_camera import camera_pose,CLOSING_CUT
assert CLOSING_CUT==m.EXIT_ARRIVAL+1
for f in range(m.EXIT_START,m.EXIT_ARRIVAL+1):
 plan=camera_pose(f);p=m.root_at(f)
 assert plan['phase']=='departure'
 assert math.isclose(math.dist(plan['eye'],plan['aim']),math.sqrt(3**2+4**2+1.8**2),abs_tol=1e-9)
for f in range(CLOSING_CUT,m.SCENE_END+1):
 assert camera_pose(f)==camera_pose(CLOSING_CUT)
assert camera_pose(CLOSING_CUT)['phase']=='pigeons'
print('Departure tracking offset and explicit pigeon cut plan PASS')

from sc001_entry import supported_xy,ENTRY_Y,ENTRY_CENTER,ENTRY_HALF_WIDTH,ENTRY_HEIGHT
cross=1.2+6.3*(4.5-ENTRY_Y)/5.2
assert abs(cross-ENTRY_CENTER)<.02
for f in range(m.EXIT_START,m.SCENE_END+1):
 j=standing_joints(f)
 for side in ['left','right']:
  ankle=j[side][2]
  center=add(ankle,mul(j['forward'],.05))
  for a in [-1,1]:
   for b in [-1,1]:
    point=add(add(center,mul(j['lateral'],a*.09)),mul(j['forward'],b*.11))
    assert supported_xy(point[0],point[1])
assert ENTRY_HEIGHT>1.92+.14
print('Entry route alignment and full sole plan supported by floor/landing PASS; evaluated collision/support separate')

# Regression: entry checks need carried-arm volumes, not root/sole coverage alone.
from sc001_entry import clipped_box_points,opening_clearance
from elias_articulation import cross,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
cube=[(x,y,z) for x in [-.5,.5] for y in [-.5,.5] for z in [-.5,.5]]
def segment_box(a,b,width):
 z=unit(sub(b,a));x=unit(cross((0,1,0),z));y=cross(z,x);center=mix(a,b,.5);length=math.dist(a,b)
 return [add(add(add(center,mul(x,p[0]*width)),mul(y,p[1]*width)),mul(z,p[2]*length)) for p in cube]
minimum_arm_clearance=float('inf')
for f in range(m.EXIT_START,m.SCENE_END+1):
 left=m.mug_grip(f);right=m.carry_position(f,m.CARRIED_KEYS_OFFSET)
 j=standing_joints(f,left,right)
 for side in ['left','right']:
  a,b,c=j[side+'_arm']
  for points in [segment_box(a,b,.15),segment_box(b,c,.11)]:
   for p in clipped_box_points(points,cube):minimum_arm_clearance=min(minimum_arm_clearance,opening_clearance(p))
assert minimum_arm_clearance>=0
# Reproduce the superseded pole's failure on the reported source frame.
assert opening_clearance((5.7474765053,.13,1.6052405867))<0
print(f'Carried arm-volume regression PASS: revised all-frame minimum {minimum_arm_clearance:.6f} m; bpy evaluation separate')

# AABB overlap is only broad-phase evidence; test exact oriented-box separation.
from sc001_entry import boxes_overlap,box_axes
angle=math.pi/4
rotated=[(p[0]*2*math.cos(angle)-p[1]*.2*math.sin(angle),p[0]*2*math.sin(angle)+p[1]*.2*math.cos(angle),p[2]*2) for p in cube]
def small_box(center):return [tuple(a+b*.2 for a,b in zip(center,p)) for p in cube]
separate=small_box((.7,-.7,0));intersecting=small_box((.3,.3,0))
assert all(min(p[k] for p in rotated)<max(p[k] for p in separate) and max(p[k] for p in rotated)>min(p[k] for p in separate) for k in range(3))
assert not boxes_overlap(rotated,box_axes(rotated,cube),separate,box_axes(separate,cube))
assert boxes_overlap(rotated,box_axes(rotated,cube),intersecting,box_axes(intersecting,cube))
assert boxes_overlap(intersecting,box_axes(intersecting,cube),rotated,box_axes(rotated,cube))
leaf=[(5.72+p[0]*.045,-.75+p[1]*1.6,1.1+p[2]*2.2) for p in cube]
for f in range(m.EXIT_START,m.SCENE_END+1):
 j=standing_joints(f,m.mug_grip(f),m.carry_position(f,m.CARRIED_KEYS_OFFSET))
 for side in ['left','right']:
  a,b,c=j[side+'_arm']
  for cs in [segment_box(a,b,.15),segment_box(b,c,.11)]:
   assert not boxes_overlap(cs,box_axes(cs,cube),leaf,box_axes(leaf,cube))
print('Oriented-box broad/narrow collision regression and planned carried-arm leaf clearance PASS; actual Blender overlap classification pending')

# Whole carry assembly crossing: cup, three handle boxes, keys and jacket.
carry_parts=[('cup',(0,0,.11),(.2,.2,.22),'mug'),
 ('handle_top',(.14,0,.17),(.12,.035,.03),'mug'),
 ('handle_side',(.19,0,.11),(.035,.035,.13),'mug'),
 ('handle_bottom',(.14,0,.045),(.12,.035,.03),'mug'),
 ('key_ring',(0,0,0),(.06,.11,.015),'keys'),
 ('jacket',(0,0,0),(.5,.12,.8),'jacket')]
for i in range(2):
 carry_parts += [('key_shaft_'+str(i),(i*.06,-.12,0),(.025,.17,.015),'keys'),('key_tooth_'+str(i),(.025+i*.06,-.19,0),(.06,.025,.015),'keys')]
minimum_carry_clearance=float('inf');worst=None
for f in range(m.EXIT_START,m.SCENE_END+1):
 for name,offset,size,kind in carry_parts:
  base=m.coffee_target(f) if kind=='mug' else m.carry_position(f,m.CARRIED_KEYS_OFFSET if kind=='keys' else m.JACKET_OFFSET)
  cs=[add(base,m.carry_vector(f,add(offset,tuple(p[k]*size[k] for k in range(3))))) for p in cube]
  assert not boxes_overlap(cs,box_axes(cs,cube),leaf,box_axes(leaf,cube))
  for point in clipped_box_points(cs,cube):
   margin=opening_clearance(point)
   if margin<minimum_carry_clearance:minimum_carry_clearance=margin;worst=(name,f,point)
assert minimum_carry_clearance>=0,(minimum_carry_clearance,worst)
assert opening_clearance((5.5510001183,.1159996018,1.3199999332))<0
print(f'Complete carry assembly clearance PASS, minimum {minimum_carry_clearance:.6f} m; actual Blender gate separate')
