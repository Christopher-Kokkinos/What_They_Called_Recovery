"""Bounded radial sightline search, retaining author's 200-degree starting proposal."""
from sc001_motion import camera_radial


def configure(bpy,scene,cam):
    from mathutils import Vector
    def pose(frame,bearing):
        t=max(0,min(1,(frame-750)/60))
        cam.location=camera_radial((2.5,5.8,0),bearing,1.8+1.2*t,2.0)
        aim=Vector((3.5,6.05,.56)).lerp(Vector((2.5,5.8,1.05)),t)
        cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.lens=65-25*t
        return t,aim
    def rays(frame,bearing):
        scene.frame_set(frame);pose(frame,bearing);bpy.context.view_layer.update()
        deps=bpy.context.evaluated_depsgraph_get();records=[]
        for name in ['Prescription_cell_00','Prescription_cell_01','Prescription_label']:
            obj=scene.objects[name].evaluated_get(deps)
            corners=[obj.matrix_world @ Vector(c) for c in obj.bound_box]
            centre=sum(corners,Vector())/8
            # Centre plus inset samples towards four upper corners.
            targets=[centre]+[centre.lerp(corners[i],.6) for i in [1,3,5,7]]
            if name == 'Prescription_label':
                # Dense full-bounds grid catches initial glyph occlusion missed by inset rays.
                low=Vector(tuple(min(c[j] for c in obj.bound_box) for j in range(3)))
                high=Vector(tuple(max(c[j] for c in obj.bound_box) for j in range(3)))
                targets=[obj.matrix_world @ Vector((low.x+(high.x-low.x)*u/20,
                         low.y+(high.y-low.y)*v/4,(low.z+high.z)/2))
                         for u in range(21) for v in range(5)]
            for index,target in enumerate(targets):
                delta=target-cam.location
                hit,location,normal,face,blocker,matrix=scene.ray_cast(deps,cam.location,delta.normalized(),distance=delta.length+.001)
                clear=not hit or blocker.name==name
                records.append({'frame':frame,'target':name,'sample':index,'clear_ray':clear,'first_hit':blocker.name if hit else None})
        return records
    cam.animation_data_clear();cam.data.animation_data_clear();cam.data.type='PERSP'
    hold_frames=list(range(661,751,6))+[750]
    trials=[];chosen=200;selected=[]
    candidates=[200,195,205,190,210,185,215,180,220,175,225,170,230,110]
    for bearing in candidates:
        records=[]
        for frame in hold_frames:
            records.extend(rays(frame,bearing))
            if any(not r['clear_ray'] for r in records):break
        passed=all(r['clear_ray'] for r in records)
        trials.append({'radial':bearing,'passed':passed,'tested_rays':len(records)})
        if passed:chosen=bearing;selected=records;break
    if not selected:
        selected=[r for frame in hold_frames for r in rays(frame,200)]
    keys=[]
    for frame in [661,750,780,810,840,870,888]:
        scene.frame_set(frame);t,aim=pose(frame,chosen)
        cam.keyframe_insert(data_path='location',frame=frame);cam.keyframe_insert(data_path='rotation_euler',frame=frame);cam.data.keyframe_insert(data_path='lens',frame=frame)
        keys.append({'frame':frame,'radial':chosen,'radius':1.8+1.2*t,'height':2.0,'aim':list(aim)})
    return {'bedside_camera_keys':keys,'bedside_radial_trials':trials,'bedside_occlusion_samples':selected,
            'bedside_readability_status':'sampled_rays_clear_visual_review_pending' if all(r['clear_ray'] for r in selected) else 'occlusion_detected_visual_review_required'}
