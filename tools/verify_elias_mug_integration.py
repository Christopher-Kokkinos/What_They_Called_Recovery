"""All-frame pure target contract plus continuity checks around mug joins."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/04_Scenes/Automation'),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]
from elias_mug_integration import state,WINDOWS
from elias_mug_lifecycle import state as cycle
from elias_mug_contact import state as held
from sc001_room_performance import state as source
from elias_rig_math import bones,skin
from elias_articulation import add,sub,mul,dot
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
rest=state(889,layout);reference=bones(rest);surface=skin(rest);max_steps={};previous=None;maximum_palm_error=0
# Predict centroid deformation from actual saved skin weights/rest transforms,
# independently of the requested palm centre (no Blender dependency).
centroids={}
for side,suffix in [('left','L'),('right','R')]:
    indices=surface['palm_vertex_indices'][suffix]
    names={name for i in indices for name,value in surface['weights'][i].items() if value>0}
    assert len(names)==1
    name=next(iter(names));assert all(surface['weights'][i]=={name:1} for i in indices)
    centroid=tuple(sum(surface['vertices'][i][axis] for i in indices)/len(indices) for axis in range(3))
    centroids[side]=(name,centroid)
assert centroids['left'][0]=='palm.L' and len(reference)==49
for weights in surface['weights']:
    assert set(weights)<=set(reference) and abs(sum(weights.values())-1)<1e-9
# Reproduce the old rigid wrist-weighted palm error before testing the fix.
legacy_rest={k:v for k,v in rest.items() if k!='_palm_controls'}
legacy_bones=bones(legacy_rest);legacy_surface=skin(legacy_rest)
ids=legacy_surface['palm_vertex_indices']['L'];name='hand.L'
assert all(legacy_surface['weights'][i]=={name:1} for i in ids)
center=tuple(sum(legacy_surface['vertices'][i][axis] for i in ids)/len(ids) for axis in range(3))
sip=held(1460,layout);sip_bone=bones(sip)[name];delta=sub(center,legacy_bones[name]['head']);mapped=sip_bone['head']
for axis in range(3):mapped=add(mapped,mul(sip_bone['basis'][axis],dot(delta,legacy_bones[name]['basis'][axis])))
legacy_error=math.dist(add(mapped,sip['root']),sip['_hand_plan']['left']['palm']['center'])
assert abs(legacy_error-.055)<1e-8,'Failed to reproduce reported mapping fault'
for frame in range(1,3169):
    s=state(frame,layout);old=source(frame,layout);target=bones(s)
    for side,(name,centroid) in centroids.items():
        delta=sub(centroid,reference[name]['head']);mapped=target[name]['head']
        for axis in range(3):mapped=add(mapped,mul(target[name]['basis'][axis],dot(delta,reference[name]['basis'][axis])))
        error=math.dist(add(mapped,s['root']),s['_hand_plan'][side]['palm']['center'])
        maximum_palm_error=max(maximum_palm_error,error);assert error<1e-8,(frame,side,error)
    without_control={k:v for k,v in s.items() if k!='_palm_controls'}
    for field in ('root','mug','keys','letter','envelope'):assert s[field]==old[field],(frame,field)
    for name,b in target.items():assert abs(b['length']-reference[name]['length'])<1e-8,(frame,name)
    assert math.dist(target['forearm.L']['tail'],target['hand.L']['head'])<1e-9
    if 1387<=frame<=1560 or 2430<=frame<=2510:assert without_control==cycle(frame,layout),(frame,'Passed cycle changed')
    if frame>=2511:assert without_control==held(frame,layout),(frame,'Carry target changed')
    if previous:
        for name,a,b in WINDOWS:
            if a<frame<=b:
                wrist=math.dist(s['joints']['left_arm'][-1],previous['joints']['left_arm'][-1])
                elbow=math.dist(s['joints']['left_arm'][1],previous['joints']['left_arm'][1])
                chest=math.dist(s['joints']['chest'],previous['joints']['chest'])
                assert wrist<.065 and elbow<.08 and chest<.045,(frame,name,wrist,elbow,chest)
                max_steps[name]=max(max_steps.get(name,0),wrist)
    previous=s
print(json.dumps({'status':'pure_mug_integration_pass','source_frames':3168,'left_wrist':'connected','bones':len(reference),'legacy_reproduced_error_metres':legacy_error,'maximum_predicted_palm_centroid_error_metres':maximum_palm_error,'maximum_wrist_steps_metres':max_steps,'limitations':['All-frame pure targets only; Blender boundary clips/readback pending','Table/posture and exact skin contacts remain open']}))
