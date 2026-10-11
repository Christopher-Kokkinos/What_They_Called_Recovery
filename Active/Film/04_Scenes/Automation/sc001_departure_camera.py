"""SC001 departure tracking and pigeon cutaway; pure plan plus bpy adapter."""
from sc001_motion import root_at,EXIT_START,EXIT_ARRIVAL,SCENE_END

CLOSING_CUT=EXIT_ARRIVAL+1


def camera_pose(frame):
    if frame<CLOSING_CUT:
        x,y,z=root_at(frame)
        return {'phase':'departure','eye':(x+3,y-4,z+2.8),
                'aim':(x,y,z+1.0),'scale':4.8}
    return {'phase':'pigeons','eye':(1.9,2.7,2.1),
            'aim':(-.35,4.5,1.15),'scale':2.4}


def configure(bpy,scene,cam):
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    from sc001_motion_blender import linearise_owned_actions
    cam.animation_data_clear();cam.data.animation_data_clear()
    cam.data.type='ORTHO'
    checks=[]
    body=[o.name for o in scene.objects['CHR_Elias_proxy_root'].children]
    for frame in range(EXIT_START,SCENE_END+1):
        scene.frame_set(frame);bpy.context.view_layer.update()
        plan=camera_pose(frame);cam.location=plan['eye'];cam.data.ortho_scale=plan['scale']
        cam.rotation_euler=(Vector(plan['aim'])-cam.location).to_track_quat('-Z','Y').to_euler()
        names=body+['PRP_CoffeeMug','PRP_Keys','PRP_EliasJacket'] if frame<CLOSING_CUT else ['CHR_Pigeon_A','CHR_Pigeon_B']
        if EXIT_ARRIVAL-20<=frame<CLOSING_CUT:names+=['SET_EliasFlat_entry_marker']
        bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        points=[]
        for name in names:
            obj=scene.objects[name].evaluated_get(deps)
            points.extend(obj.matrix_world @ Vector(c) for c in obj.bound_box)
        for attempt in range(30):
            bpy.context.view_layer.update()
            projected=[world_to_camera_view(scene,cam,p) for p in points]
            if all(.04<=p.x<=.96 and .04<=p.y<=.96 and p.z>0 for p in projected):break
            cam.data.ortho_scale*=1.06
        else:raise RuntimeError('Departure framing failed at frame '+str(frame))
        for channel in ['location','rotation_euler']:cam.keyframe_insert(data_path=channel,frame=frame)
        cam.data.keyframe_insert(data_path='ortho_scale',frame=frame)
        checks.append({'frame':frame,'phase':plan['phase'],'subjects_contained':True,'scale':cam.data.ortho_scale})
    linearise_owned_actions([cam,cam.data])
    # Explicit hard cut: no subframe camera sweep between the two compositions.
    for owner in [cam,cam.data]:
        action=owner.animation_data.action
        curves=[c for layer in action.layers for strip in layer.strips for bag in strip.channelbags for c in bag.fcurves] if getattr(action,'is_action_layered',False) else list(action.fcurves)
        for curve in curves:
            for key in curve.keyframe_points:
                if key.co.x>=EXIT_ARRIVAL:key.interpolation='CONSTANT'
            curve.update()
    return {'closing_cut':CLOSING_CUT,'tracking_frames':[EXIT_START,EXIT_ARRIVAL],
            'closing_frames':[CLOSING_CUT,SCENE_END],'checked_frames':len(checks),
            'containment_checks':checks,'limitations':['Containment is not occlusion or natural camera performance','Birds remain diagnostic boxes']}
