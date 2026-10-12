"""SC001 departure coverage: stable phase scales and structural sight checks."""
from sc001_motion import root_at,EXIT_START,EXIT_ARRIVAL,SCENE_END

CLOSING_CUT=EXIT_ARRIVAL+1
TRACK_OFFSETS=[(5,-3,2.8),(6,-3,2.8),(5,-2,2.8),(6,-2,3.2),(5,-4,3.2),(6,-4,3.6),(5,-3,5.0),(6,-4,6.0)]


def camera_pose(frame,offset=None):
    if frame<CLOSING_CUT:
        x,y,z=root_at(frame);dx,dy,dz=offset or TRACK_OFFSETS[0]
        return {'phase':'departure','eye':(x+dx,y+dy,z+dz),
                'aim':(x,y,z+1.0),'scale':4.8}
    return {'phase':'pigeons','eye':(1.9,2.7,2.1),
            'aim':(-.35,4.5,1.15),'scale':2.4}


def configure(bpy,scene,cam):
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    from sc001_motion_blender import linearise_owned_actions
    cam.animation_data_clear();cam.data.animation_data_clear();cam.data.type='ORTHO'
    body=[o.name for o in scene.objects['CHR_Elias_proxy_root'].children]
    structure=['SET_EliasFlat_entry_open_leaf','SET_EliasFlat_entry_left_jamb','SET_EliasFlat_entry_right_jamb','SET_EliasFlat_entry_lintel']
    visible=['CHR_Elias_head','CHR_Elias_torso','CHR_Elias_left_forearm','CHR_Elias_right_forearm','CHR_Elias_left_palm','CHR_Elias_right_palm','PRP_CoffeeMug','PRP_Keys']+[o.name for o in scene.objects if o.name.startswith(('PRP_Mug_handle_','PRP_Key_'))]
    def place(frame,offset,scale=None):
        scene.frame_set(frame);plan=camera_pose(frame,offset)
        cam.location=plan['eye'];cam.data.ortho_scale=plan['scale'] if scale is None else scale
        cam.rotation_euler=(Vector(plan['aim'])-cam.location).to_track_quat('-Z','Y').to_euler()
        bpy.context.view_layer.update()
        return plan
    def subject_points(frame,deps):
        names=body+['PRP_CoffeeMug','PRP_Keys','PRP_EliasJacket'] if frame<CLOSING_CUT else ['CHR_Pigeon_A','CHR_Pigeon_B']
        if EXIT_ARRIVAL-20<=frame<CLOSING_CUT:names+=structure[1:]
        return [obj.matrix_world @ Vector(c) for name in names for obj in [scene.objects[name].evaluated_get(deps)] for c in obj.bound_box]
    def contained(points):
        projected=[world_to_camera_view(scene,cam,p) for p in points]
        return all(.04<=p.x<=.96 and .04<=p.y<=.96 and p.z>0 for p in projected)
    def sight(deps):
        # Orthographic rays originate at the camera plane, not the camera centre.
        direction=cam.matrix_world.to_quaternion() @ Vector((0,0,-1))
        samples=0
        for name in visible:
            target=scene.objects[name].evaluated_get(deps)
            points=[target.matrix_world.translation]+[target.matrix_world @ Vector(c) for c in target.bound_box]
            for point in points:
                depth=(point-cam.matrix_world.translation).dot(direction)
                if depth<=0:return samples,{'subject':name,'reason':'behind_camera'}
                origin=point-direction*depth;samples+=1
                for blocker_name in structure:
                    blocker=scene.objects[blocker_name].evaluated_get(deps);inverse=blocker.matrix_world.inverted()
                    local_direction=inverse.to_3x3() @ direction
                    hit,location,normal,index=blocker.ray_cast(inverse @ origin,local_direction,distance=max(0,depth-1e-4)*local_direction.length)
                    if hit:return samples,{'subject':name,'blocker':blocker_name}
        return samples,None
    trials=[];selected=None;phase_scales={};total_samples=0
    for offset in TRACK_OFFSETS:
        scales={'departure':4.8,'pigeons':2.4};samples=0;failure=None
        for frame in range(EXIT_START,SCENE_END+1):
            plan=place(frame,offset);deps=bpy.context.evaluated_depsgraph_get();points=subject_points(frame,deps)
            for attempt in range(40):
                if contained(points):break
                cam.data.ortho_scale*=1.06;bpy.context.view_layer.update()
            else:raise RuntimeError('Departure fit failed '+str(frame))
            scales[plan['phase']]=max(scales[plan['phase']],cam.data.ortho_scale)
            if frame<CLOSING_CUT:
                count,blocked=sight(deps);samples+=count
                if blocked:failure={'frame':frame,**blocked};break
        trials.append({'offset':offset,'passed':failure is None,'sampled_rays':samples,'first_blocked':failure})
        if failure is None:selected=offset;phase_scales=scales;total_samples=samples;break
    if selected is None:raise RuntimeError('No departure viewing angle clears structure: '+str(trials))
    checks=[]
    for frame in range(EXIT_START,SCENE_END+1):
        phase=camera_pose(frame,selected)['phase'];plan=place(frame,selected,phase_scales[phase]);deps=bpy.context.evaluated_depsgraph_get()
        assert contained(subject_points(frame,deps)),'Stable-scale departure framing failed '+str(frame)
        if phase=='departure':
            count,blocked=sight(deps)
            assert blocked is None,'Departure structure occlusion '+str(frame)+' '+str(blocked)
        for channel in ['location','rotation_euler']:cam.keyframe_insert(data_path=channel,frame=frame)
        cam.data.keyframe_insert(data_path='ortho_scale',frame=frame)
        checks.append({'frame':frame,'phase':phase,'subjects_contained':True,'scale':phase_scales[phase]})
    linearise_owned_actions([cam,cam.data])
    for owner in [cam,cam.data]:
        action=owner.animation_data.action
        curves=[c for layer in action.layers for strip in layer.strips for bag in strip.channelbags for c in bag.fcurves] if getattr(action,'is_action_layered',False) else list(action.fcurves)
        for curve in curves:
            for key in curve.keyframe_points:
                if key.co.x>=EXIT_ARRIVAL:key.interpolation='CONSTANT'
            curve.update()
    return {'closing_cut':CLOSING_CUT,'tracking_frames':[EXIT_START,EXIT_ARRIVAL],
            'closing_frames':[CLOSING_CUT,SCENE_END],'checked_frames':len(checks),
            'selected_offset':selected,'phase_scales':phase_scales,'view_trials':trials,
            'structure_visibility_samples':total_samples,'containment_checks':checks,
            'limitations':['Sampled structural rays do not certify all pixels or body self-occlusion','No final camera-performance approval','Birds remain diagnostic boxes']}
