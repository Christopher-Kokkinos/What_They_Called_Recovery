"""Apply reusable diagnostic opening joints to owned SC001 proxy meshes only."""
from elias_articulation import opening_joints, THIGH_LENGTH, CALF_LENGTH, SPINE_LENGTH, STANDING_HIP_HEIGHT, BED_TOP_HEIGHT, BED_SIDE_X
from sc001_standing import standing_joints
from sc001_motion_blender import linearise_owned_actions
from sc001_motion import root_at,bedside_lean,BEDSIDE_LEAN_RADIANS,SHOWER_HAND_OFFSET


def apply(bpy,scene,root,spec,box):
    from mathutils import Vector, Matrix
    lower=box('CHR_Elias_lower_spine',(0,0,0),(.45,.25,SPINE_LENGTH/2),'CHARACTERS',(.27,.32,.36,1))
    lower.parent=root
    torso=scene.objects['CHR_Elias_torso']
    neck=box('CHR_Elias_neck',(0,0,0),(.12,.12,.10),'CHARACTERS',(.27,.32,.36,1));neck.parent=root
    def segment(obj,a,b,width,depth,frame,basis=None):
        inverse=root.matrix_world.inverted();a=inverse @ Vector(a);b=inverse @ Vector(b)
        obj.location=(a+b)/2
        obj.rotation_euler=basis.to_euler() if basis is not None else (b-a).to_track_quat('Z','Y').to_euler()
        obj.scale=(width,depth,(b-a).length)
        for channel in ['location','rotation_euler','scale']:obj.keyframe_insert(data_path=channel,frame=frame)
    def joints_at(frame):
        if frame<=888:
            return opening_joints(frame,root_at(frame),BEDSIDE_LEAN_RADIANS*bedside_lean(frame))
        else:
            deps=bpy.context.evaluated_depsgraph_get()
            left_target=right_target=None
            if 1400<=frame<1540 or frame>=2420:
                p=scene.objects['PRP_CoffeeMug'].evaluated_get(deps).matrix_world.translation
                left_target=tuple(p+Vector((.19,0,.11)))
            if frame>=2220:
                name='PRP_Keys' if frame>=2380 else 'PRP_ResignationLetter'
                right_target=tuple(scene.objects[name].evaluated_get(deps).matrix_world.translation)
            elif 1190<=frame<=1280:
                right_target=tuple(Vector(root_at(frame))+Vector(SHOWER_HAND_OFFSET))
            return standing_joints(frame,left_target,right_target)

    # Dense source-frame keys avoid segment-length changes caused by sparse transform interpolation.
    for frame in range(1,2761):
        scene.frame_set(frame);bpy.context.view_layer.update()
        joints=joints_at(frame)
        world_basis=Matrix((joints['lateral'],tuple(-x for x in joints['forward']),joints['up'])).transposed()
        local_basis=root.matrix_world.inverted().to_3x3() @ world_basis
        segment(lower,joints['pelvis'],joints['spine'],.45,.25,frame,local_basis)
        segment(torso,joints['spine'],joints['chest'],.45,.25,frame,local_basis)
        neck_end=Vector(joints['chest'])+Vector(joints['up'])*.10
        segment(neck,joints['chest'],neck_end,.12,.12,frame,local_basis)
        head=scene.objects['CHR_Elias_head'];head.location=root.matrix_world.inverted() @ Vector(joints['head'])
        head.rotation_euler=(local_basis @ Matrix.Rotation(.08,3,'X')).to_euler() if 1260<=frame<=1300 else local_basis.to_euler()
        for channel in ['location','rotation_euler']:head.keyframe_insert(data_path=channel,frame=frame)
        for side in ['left','right']:
            shoulder,elbow,wrist=joints[side+'_arm']
            segment(scene.objects['CHR_Elias_'+side+'_arm'],shoulder,elbow,.15,.15,frame)
            forearm=scene.objects['CHR_Elias_'+side+'_forearm']
            segment(forearm,elbow,wrist,.11,.11,frame)
            palm=scene.objects['CHR_Elias_'+side+'_palm']
            palm.location=root.matrix_world.inverted() @ Vector(wrist)
            palm.rotation_euler=local_basis.to_euler()
            for channel in ['location','rotation_euler']:palm.keyframe_insert(data_path=channel,frame=frame)
            for obj in [forearm,palm,neck]:
                obj.hide_render=False;obj.hide_viewport=False
                for channel in ['hide_render','hide_viewport']:obj.keyframe_insert(data_path=channel,frame=frame)
        for side in ['left','right']:
            hip,knee,ankle=joints[side]
            segment(scene.objects['CHR_Elias_'+side+'_thigh'],hip,knee,.18,.18,frame)
            segment(scene.objects['CHR_Elias_'+side+'_calf'],knee,ankle,.18,.18,frame)
            foot=scene.objects['CHR_Elias_'+side+'_foot']
            centre=Vector((ankle[0],ankle[1]-.05,ankle[2]-.05)) if frame<=888 else Vector(ankle)+Vector(joints['forward'])*.05-Vector((0,0,.05))
            foot.location=root.matrix_world.inverted() @ centre
            foot.rotation_euler=root.rotation_euler.to_matrix().transposed().to_euler() if frame<=888 else local_basis.to_euler()
            foot.scale=(.18,.22,.10)
            for channel in ['location','rotation_euler','scale']:foot.keyframe_insert(data_path=channel,frame=frame)
        lower.hide_render=False;lower.hide_viewport=False
        for channel in ['hide_render','hide_viewport']:lower.keyframe_insert(data_path=channel,frame=frame)
    linearise_owned_actions(root.children)
    max_attachment_error=0.0
    max_foot_height_error=0.0
    max_leg_endpoint_error=0.0
    max_leg_length_error=0.0
    minimum_seated_thigh_clearance=float('inf')
    for frame in range(1,2761):
        scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        joints=joints_at(frame)
        for side in ['left','right']:
            arm=scene.objects['CHR_Elias_'+side+'_arm'].evaluated_get(deps)
            forearm=scene.objects['CHR_Elias_'+side+'_forearm'].evaluated_get(deps)
            shoulder,elbow,wrist=map(Vector,joints[side+'_arm'])
            errors=[(arm.matrix_world @ Vector((0,0,-.5))-shoulder).length,
                    (arm.matrix_world @ Vector((0,0,.5))-elbow).length,
                    (forearm.matrix_world @ Vector((0,0,-.5))-elbow).length,
                    (forearm.matrix_world @ Vector((0,0,.5))-wrist).length]
            max_attachment_error=max(max_attachment_error,*errors)
            hip,knee,ankle=map(Vector,joints[side])
            thigh=scene.objects['CHR_Elias_'+side+'_thigh'].evaluated_get(deps)
            calf=scene.objects['CHR_Elias_'+side+'_calf'].evaluated_get(deps)
            leg_errors=[(thigh.matrix_world @ Vector((0,0,-.5))-hip).length,
                        (thigh.matrix_world @ Vector((0,0,.5))-knee).length,
                        (calf.matrix_world @ Vector((0,0,-.5))-knee).length,
                        (calf.matrix_world @ Vector((0,0,.5))-ankle).length]
            max_leg_endpoint_error=max(max_leg_endpoint_error,*leg_errors)
            max_leg_length_error=max(max_leg_length_error,
                abs(thigh.matrix_world.to_scale().z-THIGH_LENGTH),
                abs(calf.matrix_world.to_scale().z-CALF_LENGTH))
            if 350<=frame<=888:
                local=list(thigh.bound_box)
                corners=[thigh.matrix_world @ Vector(c) for c in local]
                over_bed=[c for c in corners if c.x<=BED_SIDE_X]
                for i,a in enumerate(corners):
                    for k,b in enumerate(corners[i+1:],i+1):
                        if sum(abs(local[i][axis]-local[k][axis])>1e-8 for axis in range(3))!=1:
                            continue
                        if (a.x-BED_SIDE_X)*(b.x-BED_SIDE_X)<0:
                            over_bed.append(a.lerp(b,(BED_SIDE_X-a.x)/(b.x-a.x)))
                if over_bed:
                    minimum_seated_thigh_clearance=min(minimum_seated_thigh_clearance,min(c.z for c in over_bed)-BED_TOP_HEIGHT)
            if frame>=889:
                foot=scene.objects['CHR_Elias_'+side+'_foot'].evaluated_get(deps)
                bottom=min((foot.matrix_world @ Vector(c)).z for c in foot.bound_box)
                expected=joints[side][2][2]-.10
                max_foot_height_error=max(max_foot_height_error,abs(bottom-expected))
                assert bottom>=-1e-5,'Later foot below floor'

    assert minimum_seated_thigh_clearance>=-1e-5,'Seated thigh intersects bed top'
    assert max_leg_endpoint_error<1e-5,'Leg attachment mismatch'
    assert max_leg_length_error<1e-5,'Shared anatomy length mismatch'
    assert max_attachment_error<1e-5,'Arm attachment mismatch'
    assert max_foot_height_error<1e-5,'Later foot height target mismatch'

    checks=[]
    for frame in [350,661,750,810,870,888]:
        scene.frame_set(frame);bpy.context.view_layer.update()
        deps=bpy.context.evaluated_depsgraph_get()
        for side in ['left','right']:
            thigh=scene.objects['CHR_Elias_'+side+'_thigh'].evaluated_get(deps)
            calf=scene.objects['CHR_Elias_'+side+'_calf'].evaluated_get(deps)
            foot=scene.objects['CHR_Elias_'+side+'_foot'].evaluated_get(deps)
            bottom=min((foot.matrix_world @ Vector(c)).z for c in foot.bound_box)
            assert abs(thigh.matrix_world.to_scale().z-THIGH_LENGTH)<1e-5
            assert abs(calf.matrix_world.to_scale().z-CALF_LENGTH)<1e-5
            assert abs(bottom)<1e-5, 'Foot off floor '+side+' '+str(frame)
            checks.append({'frame':frame,'side':side,'foot_bottom_z':bottom,'thigh':THIGH_LENGTH,'calf':CALF_LENGTH})
    return {'minimum_seated_thigh_clearance':minimum_seated_thigh_clearance,'bed_top_height':BED_TOP_HEIGHT,'anatomy':{'thigh':THIGH_LENGTH,'calf':CALF_LENGTH,'spine':SPINE_LENGTH,'standing_hip_height':STANDING_HIP_HEIGHT},'maximum_leg_endpoint_error':max_leg_endpoint_error,'maximum_leg_length_error':max_leg_length_error,'anatomy_checked_frames':2760,'maximum_later_foot_height_error':max_foot_height_error,'attachment_checked_frames':2760,'maximum_arm_endpoint_error':max_attachment_error,'evaluated_joint_checks':checks,'opening_articulation':'fixed_length_joint_proxy_desktop_pending','owned_frames':[1,2760],
            'standing_and_handling':'shared_chest_prop_targets_provisional_exit_steps','limitations':['Staged rise, not final roll','No skinning or armature yet','Drawer grip remains analytic proxy; final skinning/contact pending']}
