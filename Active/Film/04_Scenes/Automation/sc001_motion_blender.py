"""Apply scoped coarse animation to owned SC001 objects; no external scene writes."""
import math
from sc001_motion import root_at, pose_weights, carried_position, sample_frames, custody_at, EVENTS, root_rotation, bedside_lean, upper_point, BEDSIDE_LEAN_RADIANS, coffee_target, CARRIED_KEYS_OFFSET, POCKET_OFFSET, JACKET_OFFSET, pocket_position, standing_yaw, EXIT_ARRIVAL, SCENE_END


def linearise_owned_actions(objects):
    """Set actual curves, including Blender layered action channel bags.

    Python key insertion must not rely on a UI preference. Visibility keys
    remain constant; transform keys use the pure planner's linear contract.
    """
    count=0
    for obj in objects:
        animation=obj.animation_data
        if animation is None or animation.action is None:
            continue
        action=animation.action
        curves=[]
        if getattr(action,'is_action_layered',False):
            for layer in action.layers:
                for strip in layer.strips:
                    for bag in getattr(strip,'channelbags',()):
                        curves.extend(bag.fcurves)
        else:
            curves.extend(action.fcurves)
        if not curves:
            raise RuntimeError('No animation curves found for '+obj.name)
        for curve in curves:
            interpolation='CONSTANT' if curve.data_path.startswith('hide_') else 'LINEAR'
            for key in curve.keyframe_points:
                key.interpolation=interpolation
                count+=1
            curve.update()
    return count


def apply_motion(bpy, scene, root, defaults, spec, box):
    bpy.context.preferences.edit.keyframe_new_interpolation_type='LINEAR'
    body=list(root.children)
    for obj in [root]+body:
        obj.animation_data_clear()

    def group(name,names):
        obj=bpy.data.objects.new(name,None)
        scene.collection.objects.link(obj)
        for n in names:
            scene.objects[n].parent=obj
        return obj

    mug=group('SC001_MugMotion',[o.name for o in scene.objects if o.name=='PRP_CoffeeMug' or o.name.startswith('PRP_Mug_handle_')])
    keys=group('SC001_KeysMotion',[o.name for o in scene.objects if o.name=='PRP_Keys' or o.name.startswith('PRP_Key_')])
    # Set a shallow tray under the unchanged strip; closing slides it beneath cabinet.
    tray=box('PRP_DrawerTray',(3.50,6.05,.52),(.61,.65,.025))
    front=box('PRP_DrawerFront',(3.50,5.72,.48),(.62,.045,.42))
    drawer=group('SC001_DrawerMotion',[o.name for o in scene.objects if o.name in {'PRP_PrescriptionStrip','Prescription_label','PRP_DrawerTray','PRP_DrawerFront'} or o.name.startswith('Prescription_cell_')])
    moving=[mug,keys,drawer,scene.objects['PRP_ResignationLetter'],scene.objects['PRP_MACEnvelope'],scene.objects['PRP_EliasJacket']]
    initial={o.name:(o.location.copy(),o.scale.copy()) for o in moving}
    right=scene.objects['CHR_Elias_right_arm'];left=scene.objects['CHR_Elias_left_arm']
    bird=scene.objects['CHR_Pigeon_A'];bird_start=bird.location.copy()
    palms={}
    for side in ['left','right']:
        palm=box('CHR_Elias_'+side+'_palm',(0,0,0),(.10,.08,.10),'CHARACTERS',(.27,.32,.36,1))
        palm.parent=root;palms[side]=palm
    forearms={}
    for side in ['left','right']:
        obj=box('CHR_Elias_'+side+'_forearm',(0,0,0),(.11,.11,.34),'CHARACTERS',(.27,.32,.36,1));obj.parent=root;forearms[side]=obj
    flaps=[box('PRP_LetterFold_'+str(i),(0,0,0),(.21,.099,.002),color=(.92,.9,.85,1)) for i in [-1,1]]
    reach_checks=[]
    frames=sample_frames(spec)
    for frame in frames:
        pos=root_at(frame);lying,seated=pose_weights(frame)
        root.location=pos;root.rotation_euler=root_rotation(frame)
        for obj in body:
            location,scale=defaults[obj.name]
            obj.location=location.copy();obj.scale=scale.copy();obj.rotation_euler=(0,0,0)
            if 'thigh' in obj.name:
                obj.location.y=-.25*seated;obj.location.z=.59+.1*seated
                obj.scale=(.18,.22+.38*seated,.38-.2*seated)
            elif 'calf' in obj.name:
                obj.location.y=-.5*seated;obj.location.z=.2+.12*seated
                obj.scale=(.18,.22-.04*seated,.4+.24*seated)
            elif 'foot' in obj.name:
                obj.location.y=-.55*seated-.05*(1-seated);obj.location.z=.05-.10*seated
            elif obj==right and seated:
                obj.location=(-.02,-.23,1.05);obj.scale=(.48,.15,.16)
        if 1190<=frame<=1280:
            right.location=(.25,-.25,1.4);right.scale=(.16,.2,.4)
        if 1400<=frame<1540 or frame>=2420:
            left.location=(-.35,-.18,1.15);left.scale=(.16,.22,.4)
        if 2220<=frame<2380:
            right.location=(.02,-.24,1.15);right.scale=(.43,.16,.16)
        elif frame>=2380:
            right.location=(.35,-.18,1.1);right.scale=(.16,.22,.4)
        lean=bedside_lean(frame)
        for obj in body:
            if obj.name in {'CHR_Elias_torso','CHR_Elias_head','CHR_Elias_left_arm','CHR_Elias_right_arm'}:
                obj.location=upper_point(tuple(obj.location),frame)
                obj.rotation_euler.x=BEDSIDE_LEAN_RADIANS*lean
        head=scene.objects['CHR_Elias_head']
        head.rotation_euler.x+=.08 if 1260<=frame<=1300 else 0
        for obj in [root]+body:
            for channel in ['location','rotation_euler','scale']:
                obj.keyframe_insert(data_path=channel,frame=frame)

        # Drawer never transfers tablets to a hand. At closure hide internal strip.
        t=max(0,min(1,(frame-810)/60))
        drawer.location=(0,t*.48,0)
        drawer.keyframe_insert(data_path='location',frame=frame)
        for obj in drawer.children:
            if obj.name not in {'PRP_DrawerFront'}:
                obj.hide_render=frame>=870;obj.hide_viewport=frame>=870
                obj.keyframe_insert(data_path='hide_render',frame=frame)
                obj.keyframe_insert(data_path='hide_viewport',frame=frame)

        target=coffee_target(frame)
        mug.location=tuple(a-b for a,b in zip(target,(4.8,4.65,1.02)));mug.keyframe_insert(data_path='location',frame=frame)
        keybase=(7.05,4.42,1.035);t=max(0,min(1,(frame-2380)/30));hand=carried_position(frame,CARRIED_KEYS_OFFSET)
        keys.location=tuple((b-a)*t for a,b in zip(keybase,hand));keys.keyframe_insert(data_path='location',frame=frame)
        for name in ['PRP_ResignationLetter','PRP_MACEnvelope']:
            obj=scene.objects[name];base,scale=initial[name]
            t=max(0,min(1,(frame-2300)/40));pocket=pocket_position(frame)
            if frame>=2161:
                base=(6.82,4.40,1.10) if name=='PRP_ResignationLetter' else (6.50,4.40,1.015)
            obj.location=tuple(a+(b-a)*t for a,b in zip(base,pocket))
            fold=max(0,min(1,(frame-2220)/40)) if name=='PRP_ResignationLetter' else t
            # Preserve paper width and envelope dimensions; fold hinged thirds.
            obj.scale=(.21,.099,.002) if name=='PRP_ResignationLetter' else scale
            if name=='PRP_ResignationLetter':
                from mathutils import Vector, Euler
                packet_rotation=t*math.pi/2
                for sign,flap in zip([-1,1],flaps):
                    angle=sign*math.pi*fold
                    offset=Vector((0,sign*.0495+sign*.0495*math.cos(angle),.0495*math.sin(math.pi*fold)+abs(sign)*.002*fold))
                    flap.location=Vector(obj.location)+Euler((packet_rotation,0,standing_yaw(frame))).to_matrix() @ offset
                    flap.rotation_euler=(packet_rotation+angle,0,standing_yaw(frame))
                    for channel in ['location','rotation_euler']:
                        flap.keyframe_insert(data_path=channel,frame=frame)
            obj.rotation_euler=(t*math.pi/2,0,standing_yaw(frame))
            for channel in ['location','scale','rotation_euler']:obj.keyframe_insert(data_path=channel,frame=frame)
        for name,limit in [('Notice_exact_text',2161),('Envelope_label',2161)]:
            obj=scene.objects[name];obj.hide_render=frame>=limit;obj.hide_viewport=frame>=limit
            obj.keyframe_insert(data_path='hide_render',frame=frame);obj.keyframe_insert(data_path='hide_viewport',frame=frame)
        from mathutils import Vector, Euler
        for side in ['left','right']:
            active=(1400<=frame<1540 or frame>=2420) if side=='left' else (2220<=frame)
            palm=palms[side];palm.hide_render=not active;palm.hide_viewport=not active
            if side=='left':
                goal=Vector(target)+Vector((.12,0,.11))
            elif frame>=2380:
                goal=Vector(keybase)+keys.location
            else:
                goal=scene.objects['PRP_ResignationLetter'].location.copy()
            if active:
                endpoint=Euler(root_rotation(frame)).to_matrix().transposed() @ (goal-Vector(pos))
                shoulder=Vector(upper_point((-.32 if side=='left' else .32,0,1.4),frame))
                arm=left if side=='left' else right
                delta=endpoint-shoulder;distance=delta.length
                assert .02<distance<=.70, 'Unreachable '+side+' target at frame '+str(frame)
                direction=delta.normalized();normal=direction.cross(Vector((0,0,1)))
                if normal.length<.001:normal=direction.cross(Vector((0,1,0)))
                normal.normalize()
                along=(.36**2-.34**2+distance**2)/(2*distance)
                elbow=shoulder+direction*along+normal*math.sqrt(max(0,.36**2-along**2))
                for segment,a,b,length in [(arm,shoulder,elbow,.36),(forearms[side],elbow,endpoint,.34)]:
                    segment.location=(a+b)/2;segment.scale=(.11,.11,length)
                    segment.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
                    for channel in ['location','rotation_euler','scale']:
                        segment.keyframe_insert(data_path=channel,frame=frame)
                palm.location=endpoint;palm.keyframe_insert(data_path='location',frame=frame)
                reach_checks.append({'frame':frame,'side':side,'distance':distance,'limit':.70})
            forearms[side].hide_render=not active;forearms[side].hide_viewport=not active
            for channel in ['hide_render','hide_viewport']:
                forearms[side].keyframe_insert(data_path=channel,frame=frame)
            for channel in ['hide_render','hide_viewport']:
                palm.keyframe_insert(data_path=channel,frame=frame)
        jacket=scene.objects['PRP_EliasJacket']
        jacket.location=carried_position(frame,JACKET_OFFSET) if frame>=1369 else initial[jacket.name][0]
        jacket.keyframe_insert(data_path='location',frame=frame)
        # Opening and final peck are box translations, not bird anatomy.
        peck=.05 if frame in (60,2860) else 0
        bird.location=bird_start.copy();bird.location.x+=peck
        bird.keyframe_insert(data_path='location',frame=frame)
    interpolation_keys=linearise_owned_actions(scene.objects)
    return {'explicit_interpolation_keys':interpolation_keys,'reach_checks':reach_checks,'events':EVENTS,'sampled_custody':[{'frame':f,**custody_at(f)} for f in [661,870,1470,1540,2340,2410,2440,2510,EXIT_ARRIVAL,SCENE_END]],
            'keyframes':frames,'status':'coarse_motion_visual_review_pending',
            'limitations':['linear box posing, no gait/rig/facial performance','drawer slides into hollow carcass; contents hide at closure','hinged paper thirds; pocket entry remains proxy choreography','editorial spatial elisions at SH004/SH005/SH006/SH008/SH009 starts','no audio; dialogue and temperature changes are review cues']}
