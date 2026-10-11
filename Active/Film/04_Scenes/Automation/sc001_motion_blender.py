"""Apply scoped coarse animation to owned SC001 objects; no external scene writes."""
import math
from sc001_motion import root_at, pose_weights, carried_position, sample_frames, custody_at, EVENTS


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
    tray=box('PRP_DrawerTray',(3.25,3.9,1.30),(.65,.7,.025))
    front=box('PRP_DrawerFront',(3.25,3.53,1.14),(.65,.045,.32))
    drawer=group('SC001_DrawerMotion',[o.name for o in scene.objects if o.name in {'PRP_PrescriptionStrip','Prescription_label','PRP_DrawerTray','PRP_DrawerFront'} or o.name.startswith('Prescription_cell_')])
    moving=[mug,keys,drawer,scene.objects['PRP_ResignationLetter'],scene.objects['PRP_MACEnvelope'],scene.objects['PRP_EliasJacket']]
    initial={o.name:(o.location.copy(),o.scale.copy()) for o in moving}
    right=scene.objects['CHR_Elias_right_arm'];left=scene.objects['CHR_Elias_left_arm']
    bird=scene.objects['CHR_Pigeon_A'];bird_start=bird.location.copy()
    frames=sample_frames(spec)
    for frame in frames:
        pos=root_at(frame);lying,seated=pose_weights(frame)
        root.location=pos;root.rotation_euler=(lying*math.pi/2,0,0)
        for obj in body:
            location,scale=defaults[obj.name]
            obj.location=location.copy();obj.scale=scale.copy()
            if 'thigh' in obj.name:
                obj.location.y=-.25*seated;obj.location.z=.59+.1*seated
                obj.scale=(.18,.22+.38*seated,.38-.2*seated)
            elif 'calf' in obj.name:
                obj.location.y=-.5*seated;obj.location.z=.2+.12*seated
                obj.scale=(.18,.22-.04*seated,.4+.24*seated)
            elif obj==right and seated:
                obj.location=(-.04,-.22,1.0);obj.scale=(.43,.15,.16)
        if 1190<=frame<=1280:
            right.location=(.25,-.25,1.4);right.scale=(.16,.2,.4)
        if 1400<=frame<1540 or frame>=2420:
            left.location=(-.35,-.18,1.15);left.scale=(.16,.22,.4)
        if 2220<=frame<2380:
            right.location=(.02,-.24,1.15);right.scale=(.43,.16,.16)
        elif frame>=2380:
            right.location=(.35,-.18,1.1);right.scale=(.16,.22,.4)
        # Head tilt is symbolic response, not facial expression or lip sync.
        head=scene.objects['CHR_Elias_head']
        head.rotation_euler=(.08 if 1260<=frame<=1300 else 0,0,0)
        for obj in [root]+body:
            for channel in ['location','rotation_euler','scale']:
                obj.keyframe_insert(data_path=channel,frame=frame)

        # Drawer never transfers tablets to a hand. At closure hide internal strip.
        t=max(0,min(1,(frame-810)/60))
        drawer.location=(0,t*.65,-t*.35)
        drawer.keyframe_insert(data_path='location',frame=frame)
        for obj in drawer.children:
            if obj.name not in {'PRP_DrawerFront'}:
                obj.hide_render=frame>=870;obj.hide_viewport=frame>=870
                obj.keyframe_insert(data_path='hide_render',frame=frame)
                obj.keyframe_insert(data_path='hide_viewport',frame=frame)

        coffee=(5.55,5.85,1.02)
        if 1400<=frame<=1470:
            t=(frame-1400)/70;hand=carried_position(frame,(-.4,-.28,1.4))
            target=tuple(a+(b-a)*t for a,b in zip(coffee,hand))
        elif 1470<frame<1510:target=carried_position(frame,(-.4,-.28,1.4))
        elif 1510<=frame<1540:
            t=(frame-1510)/30;hand=carried_position(frame,(-.4,-.28,1.4))
            target=tuple(a+(b-a)*t for a,b in zip(hand,coffee))
        elif frame>=2420:
            t=min(1,(frame-2420)/20);hand=carried_position(frame,(-.4,-.28,1.05))
            target=tuple(a+(b-a)*t for a,b in zip(coffee,hand))
        else:target=coffee
        mug.location=tuple(a-b for a,b in zip(target,coffee));mug.keyframe_insert(data_path='location',frame=frame)
        keybase=(6.9,5.6,1.035);t=max(0,min(1,(frame-2380)/30));hand=carried_position(frame,(.35,-.28,1.05))
        keys.location=tuple((b-a)*t for a,b in zip(keybase,hand));keys.keyframe_insert(data_path='location',frame=frame)
        for name in ['PRP_ResignationLetter','PRP_MACEnvelope']:
            obj=scene.objects[name];base,scale=initial[name]
            t=max(0,min(1,(frame-2300)/40));pocket=carried_position(frame,(.12,-.17,1.2))
            obj.location=tuple(a+(b-a)*t for a,b in zip(base,pocket))
            fold=max(0,min(1,(frame-2220)/40)) if name=='PRP_ResignationLetter' else t
            # One scaled slab is only a symbolic folded packet, not paper simulation.
            obj.scale=tuple(v*(1-.7*fold) for v in scale)
            obj.rotation_euler=(t*math.pi/2,0,0)
            for channel in ['location','scale','rotation_euler']:obj.keyframe_insert(data_path=channel,frame=frame)
        for name,limit in [('Notice_exact_text',2220),('Envelope_label',2300)]:
            obj=scene.objects[name];obj.hide_render=frame>=limit;obj.hide_viewport=frame>=limit
            obj.keyframe_insert(data_path='hide_render',frame=frame);obj.keyframe_insert(data_path='hide_viewport',frame=frame)
        jacket=scene.objects['PRP_EliasJacket']
        jacket.location=carried_position(frame,(0,.18,1.1)) if frame>=1369 else initial[jacket.name][0]
        jacket.keyframe_insert(data_path='location',frame=frame)
        # Opening and final peck are box translations, not bird anatomy.
        peck=.05 if frame in (60,2740) else 0
        bird.location=bird_start.copy();bird.location.x+=peck
        bird.keyframe_insert(data_path='location',frame=frame)
    return {'events':EVENTS,'sampled_custody':[{'frame':f,**custody_at(f)} for f in [661,870,1470,1540,2340,2410,2440,2510,2720,2760]],
            'keyframes':frames,'status':'coarse_motion_visual_review_pending',
            'limitations':['linear box posing, no gait/rig/facial performance','drawer closure uses slide/hide approximation','paper fold uses scale, pocket packet remains a symbolic slab','editorial spatial elisions at SH004/SH005/SH006/SH008/SH009 starts','no audio; dialogue and temperature changes are review cues']}
