"""Diagnostic entry opening, flush threshold and supported landing. No bpy at import."""
from sc001_motion import EXIT_START,SCENE_END

ENTRY_CENTER=6.6
ENTRY_Y=.05
ENTRY_HALF_WIDTH=.8
ENTRY_HEIGHT=2.3
WALL_HALF_DEPTH=.08
LANDING_BOUNDS=(5.4,9.2,-2.0,0.0)


def supported_xy(x,y):
    return (0<=x<=10 and 0<=y<=7) or (LANDING_BOUNDS[0]<=x<=LANDING_BOUNDS[1] and LANDING_BOUNDS[2]<=y<=LANDING_BOUNDS[3])


def build(box):
    parts=[]
    def part(name,pos,size):
        parts.append(box(name,pos,size,'SET'))
    left=ENTRY_CENTER-ENTRY_HALF_WIDTH;right=ENTRY_CENTER+ENTRY_HALF_WIDTH
    part('SET_EliasFlat_entry_left_jamb',(left-.05,ENTRY_Y,ENTRY_HEIGHT/2),(.1,.16,ENTRY_HEIGHT))
    part('SET_EliasFlat_entry_right_jamb',(right+.05,ENTRY_Y,ENTRY_HEIGHT/2),(.1,.16,ENTRY_HEIGHT))
    part('SET_EliasFlat_entry_lintel',(ENTRY_CENTER,ENTRY_Y,ENTRY_HEIGHT+.05),(1.8,.16,.1))
    # Parked open leaf is outside clear passage; no door-use performance implied.
    part('SET_EliasFlat_entry_open_leaf',(left-.08,-.75,1.1),(.045,1.6,2.2))
    part('SET_EliasFlat_entry_threshold',(ENTRY_CENTER,ENTRY_Y,-.05),(1.6,.2,.1))
    x0,x1,y0,y1=LANDING_BOUNDS
    part('SET_EliasFlat_landing',((x0+x1)/2,(y0+y1)/2,-.1),(x1-x0,y1-y0,.2))
    return [o.name for o in parts]


def validate(bpy,scene):
    from mathutils import Vector
    support_names=['SET_EliasFlat_floor','SET_EliasFlat_landing','SET_EliasFlat_entry_threshold']
    subjects=[o.name for o in scene.objects['CHR_Elias_proxy_root'].children]+['PRP_CoffeeMug','PRP_Keys','PRP_EliasJacket']
    checked=0;crossing=[];minimum_clearance=float('inf');maximum_support_gap=0.0
    for frame in range(EXIT_START,SCENE_END+1):
        scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        for name in subjects:
            obj=scene.objects[name].evaluated_get(deps)
            local=list(obj.bound_box);corners=[obj.matrix_world @ Vector(c) for c in local]
            leaf=scene.objects['SET_EliasFlat_entry_open_leaf'].evaluated_get(deps)
            leaf_corners=[leaf.matrix_world @ Vector(c) for c in leaf.bound_box]
            overlap=all(min(c[axis] for c in corners)<max(c[axis] for c in leaf_corners)-1e-5 and max(c[axis] for c in corners)>min(c[axis] for c in leaf_corners)+1e-5 for axis in range(3))
            assert not overlap,'Possible parked-door collision: '+name+' frame '+str(frame)
            if min(c.y for c in corners)>ENTRY_Y+WALL_HALF_DEPTH or max(c.y for c in corners)<ENTRY_Y-WALL_HALF_DEPTH:continue
            points=[c for c in corners if abs(c.y-ENTRY_Y)<=WALL_HALF_DEPTH]
            for i,a in enumerate(corners):
                for k,b in enumerate(corners[i+1:],i+1):
                    if sum(abs(local[i][axis]-local[k][axis])>1e-8 for axis in range(3))!=1:continue
                    for plane in [ENTRY_Y-WALL_HALF_DEPTH,ENTRY_Y+WALL_HALF_DEPTH]:
                        if (a.y-plane)*(b.y-plane)<0:points.append(a.lerp(b,(plane-a.y)/(b.y-a.y)))
            for p in points:
                clearance=min(p.x-(ENTRY_CENTER-ENTRY_HALF_WIDTH),(ENTRY_CENTER+ENTRY_HALF_WIDTH)-p.x,ENTRY_HEIGHT-p.z)
                minimum_clearance=min(minimum_clearance,clearance)
                assert clearance>=-1e-5,'Entry clearance failed: '+name+' frame '+str(frame)
            if points:crossing.append(frame)
        for side in ['left','right']:
            foot=scene.objects['CHR_Elias_'+side+'_foot'].evaluated_get(deps)
            corners=[foot.matrix_world @ Vector(c) for c in foot.bound_box];bottom=min(c.z for c in corners)
            soles=[c for c in corners if c.z<=bottom+1e-5]
            for point in soles:
                hits=[]
                for name in support_names:
                    surface=scene.objects[name].evaluated_get(deps);inverse=surface.matrix_world.inverted()
                    origin=point+Vector((0,0,.01))
                    direction=inverse.to_3x3() @ Vector((0,0,-1))
                    ok,hit,normal,index=surface.ray_cast(inverse @ origin,direction,distance=.25*direction.length)
                    if ok:hits.append(surface.matrix_world @ hit)
                assert hits,'No built floor beneath '+side+' foot at frame '+str(frame)
                hit=max(hits,key=lambda p:p.z);gap=point.z-hit.z
                assert gap>=-1e-5,'Foot penetrates support surface'
                if bottom<1e-5:
                    maximum_support_gap=max(maximum_support_gap,abs(gap))
                    assert abs(gap)<1e-5,'Stance sole not on built floor'
        checked+=1
    assert crossing,'Route never crosses entry opening'
    return {'checked_frames':checked,'crossing_frames':[min(crossing),max(crossing)],
            'minimum_opening_clearance':minimum_clearance,'maximum_stance_support_gap':maximum_support_gap,
            'status':'evaluated_opening_and_built_support_verified','door_leaf':'parked_open_interaction_pending'}
