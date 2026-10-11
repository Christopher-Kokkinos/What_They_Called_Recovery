"""Apply reusable diagnostic opening joints to owned SC001 proxy meshes only."""
from elias_articulation import opening_joints
from sc001_motion import root_at,bedside_lean,BEDSIDE_LEAN_RADIANS


def apply(bpy,scene,root,spec,box):
    from mathutils import Vector
    lower=box('CHR_Elias_lower_spine',(0,0,0),(.45,.25,.325),'CHARACTERS',(.27,.32,.36,1))
    lower.parent=root
    torso=scene.objects['CHR_Elias_torso']
    def segment(obj,a,b,width,depth,frame):
        inverse=root.matrix_world.inverted();a=inverse @ Vector(a);b=inverse @ Vector(b)
        obj.location=(a+b)/2;obj.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
        obj.scale=(width,depth,(b-a).length)
        for channel in ['location','rotation_euler','scale']:obj.keyframe_insert(data_path=channel,frame=frame)
    # Dense source-frame keys avoid segment-length changes caused by sparse transform interpolation.
    for frame in range(1,889):
        scene.frame_set(frame);bpy.context.view_layer.update()
        joints=opening_joints(frame,root_at(frame),BEDSIDE_LEAN_RADIANS*bedside_lean(frame))
        segment(lower,joints['pelvis'],joints['spine'],.45,.25,frame)
        segment(torso,joints['spine'],joints['chest'],.45,.25,frame)
        head=scene.objects['CHR_Elias_head'];head.location=root.matrix_world.inverted() @ Vector(joints['head'])
        head.keyframe_insert(data_path='location',frame=frame)
        for side in ['left','right']:
            hip,knee,ankle=joints[side]
            segment(scene.objects['CHR_Elias_'+side+'_thigh'],hip,knee,.18,.18,frame)
            segment(scene.objects['CHR_Elias_'+side+'_calf'],knee,ankle,.18,.18,frame)
            foot=scene.objects['CHR_Elias_'+side+'_foot']
            foot.location=root.matrix_world.inverted() @ Vector((ankle[0],ankle[1]-.05,ankle[2]-.05))
            foot.rotation_euler=root.rotation_euler.to_matrix().transposed().to_euler()
            foot.scale=(.18,.22,.10)
            for channel in ['location','rotation_euler','scale']:foot.keyframe_insert(data_path=channel,frame=frame)
        lower.hide_render=False;lower.hide_viewport=False
        for channel in ['hide_render','hide_viewport']:lower.keyframe_insert(data_path=channel,frame=frame)
    # Existing standing/action pass resumes at the kitchen cut. This module owns only 1–888.
    lower.hide_render=True;lower.hide_viewport=True
    for channel in ['hide_render','hide_viewport']:lower.keyframe_insert(data_path=channel,frame=889)
    checks=[]
    for frame in [350,661,750,810,870,888]:
        scene.frame_set(frame);bpy.context.view_layer.update()
        deps=bpy.context.evaluated_depsgraph_get()
        for side in ['left','right']:
            thigh=scene.objects['CHR_Elias_'+side+'_thigh'].evaluated_get(deps)
            calf=scene.objects['CHR_Elias_'+side+'_calf'].evaluated_get(deps)
            foot=scene.objects['CHR_Elias_'+side+'_foot'].evaluated_get(deps)
            bottom=min((foot.matrix_world @ Vector(c)).z for c in foot.bound_box)
            assert abs(thigh.matrix_world.to_scale().z-.60)<1e-5
            assert abs(calf.matrix_world.to_scale().z-.64)<1e-5
            assert abs(bottom)<1e-5, 'Foot off floor '+side+' '+str(frame)
            checks.append({'frame':frame,'side':side,'foot_bottom_z':bottom,'thigh':.60,'calf':.64})
    return {'evaluated_joint_checks':checks,'opening_articulation':'fixed_length_joint_proxy_desktop_pending','owned_frames':[1,888],
            'standing_and_handling':'existing_pass_retained','limitations':['Staged rise, not final roll','No skinning or armature yet','Drawer grip remains analytic proxy; final skinning/contact pending']}
