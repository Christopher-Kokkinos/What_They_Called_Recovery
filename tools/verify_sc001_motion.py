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
assert m.root_at(1)==(2,3.15,.85)
assert m.root_rotation(1)[0]<0
assert m.root_at(350)[0]>2.75 and 3<m.root_at(350)[1]<5
assert math.isclose(m.root_rotation(350)[2],math.pi/2)
