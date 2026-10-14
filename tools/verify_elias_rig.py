"""Source-pose rig contract and procedural skin integrity checks."""
import json,math,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/04_Scenes/Automation'),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]
from sc001_room_performance import state,END
from elias_rig_math import bones,skin,POSE_FRAMES
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text(encoding='utf-8'))
if __name__=='__main__':
    rest=state(889,layout);reference=bones(rest);mesh=skin(rest);edges=collections.Counter()
    for frame in range(1,END+1):
        actual=bones(state(frame,layout));assert set(actual)==set(reference)
        for name,b in actual.items():assert abs(b['length']-reference[name]['length'])<1e-9,(frame,name)
    for p,w in zip(mesh['vertices'],mesh['weights']):
        assert all(math.isfinite(v) for v in p);assert abs(sum(w.values())-1)<1e-9;assert set(w)<=set(reference)
    for f in mesh['faces']:
        assert len(f)==len(set(f))
        for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted((a,b)))]+=1
    assert set(edges.values())=={2},'Open or nonmanifold component'
    from elias_articulation import dot,cross
    adjacency=collections.defaultdict(set)
    for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
    remaining=set(range(len(mesh['vertices'])));components=[]
    while remaining:
        first=next(iter(remaining));component={first};queue=[first];remaining.remove(first)
        while queue:
            for v in adjacency[queue.pop()]:
                if v in remaining:remaining.remove(v);component.add(v);queue.append(v)
        components.append(component)
    for component in components:
        volume=0
        for face in mesh['faces']:
            if face[0] not in component:continue
            a=mesh['vertices'][face[0]]
            for i in range(1,len(face)-1):volume+=dot(a,cross(mesh['vertices'][face[i]],mesh['vertices'][face[i+1]]))/6
        assert volume>1e-8,'Inverted component winding'
    print(json.dumps({'bones':len(reference),'vertices':len(mesh['vertices']),'faces':len(mesh['faces']),'pose_samples':len(POSE_FRAMES),'source_frames_checked':END,'weights':'normalized','closed_components':len(components),'status':'pure_contract_pass','limitations':['Disconnected closed skin components, not final welded topology','Blender deformation and contact readback pending']}))
