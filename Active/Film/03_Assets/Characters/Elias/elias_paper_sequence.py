"""Continuous paper diagnostic with supported set-down and envelope pickup."""
from copy import deepcopy
from elias_paper_contact import state as fold_state,pinch
from elias_envelope_contact import state as envelope_state,blend_hand
from elias_envelope_finish import state as finish_state,translated
from elias_articulation import add,sub,mul,mix,unit,dot,cross,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
from sc001_room_performance import progress
START,END=2161,2762
PARKED_ENVELOPE=(11.42,9.35,.971)
ENVELOPE_START=2389

def envelope_frame(frame):return 2281+frame-ENVELOPE_START

def state(frame,layout):
    frame=START if frame==889 else frame
    assert START<=frame<=END
    if frame<=2280:
        s=fold_state(frame,layout);s['envelope']=PARKED_ENVELOPE;s['_sequence_phase']='fold';return s
    if frame>=ENVELOPE_START:
        source=envelope_frame(frame)
        s=envelope_state(source,layout) if source<=2474 else finish_state(source,layout)
        s['_sequence_source_frame']=source;s['frame']=frame;s['_sequence_phase']=s['_envelope_phase']
        # Keep free-release elbows independent of the rotating palm basis.
        side=start=None
        if 2434<source<=2474:side,start='right',2434
        if source>=2474:side,start='left',2474
        if side:
            j=s['joints'];shoulder,_,wrist=j[side+'_arm'];sign=1 if side=='right' else -1
            origin=envelope_state(start,layout) if start<=2474 else finish_state(start,layout)
            if side=='left':
                low=add(add(add(shoulder,mul(j['up'],-.35)),mul(j['lateral'],-.25)),mul(j['forward'],-.10))
                pole=mix(origin['joints'][side+'_arm'][1],low,progress(source,start,2530))
            else:
                end_state=envelope_state(2474,layout)
                axis=unit(sub(wrist,shoulder))
                def radial(point):
                    v=sub(point,shoulder);return unit(sub(v,mul(axis,dot(v,axis))))
                first=radial(origin['joints'][side+'_arm'][1]);last=radial(end_state['joints'][side+'_arm'][1])
                import math
                angle=math.atan2(dot(axis,cross(first,last)),dot(first,last))*progress(source,start,2474)
                direction=add(mul(first,math.cos(angle)),mul(cross(axis,first),math.sin(angle)))
                pole=add(shoulder,direction)
            e=two_segment(shoulder,wrist,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
            j[side+'_arm']=(shoulder,e,wrist)
        return s
    s=fold_state(2280,layout);s['frame']=frame;s['envelope']=PARKED_ENVELOPE
    begin=s['letter'];parked=envelope_state(2340,layout)['letter'];pos=mix(begin,parked,progress(frame,2280,2316));s['letter']=pos
    # Both hands accompany the folded letter to the table; no unsupported transfer.
    for side in ('left','right'):
        s['_hand_plan'][side],s['_hand_origins'][side]=translated(s['_hand_plan'][side],s['_hand_origins'][side],begin,pos)
        c=s['_paper_contacts'][side]
        for key in ('contact','surface_contact','index_tip','thumb_tip'):c[key]=add(c[key],sub(pos,begin))
    # Share the lowering reach with the forearm instead of leaving the wrist bent.
    import math
    pitch=math.radians(20-56.87*progress(frame,2280,2316))
    c=s['_paper_contacts']['left'];direction=(math.cos(pitch),0,math.sin(pitch));normal=(-math.sin(pitch),0,math.cos(pitch))
    hand,wrist=pinch(c['contact'],(0,0,1),direction,'left',palm_normal=normal,thumb_offset=.013)
    s['_hand_plan']['left']=hand;s['_hand_origins']['left']=wrist
    c.update(index_tip=hand['chains']['index'][-1],thumb_tip=hand['chains']['thumb'][-1])
    if frame<=2316:
        s['_sequence_phase']='set_down_folded_letter'
    else:
        # Table now supports letter while left reaches the envelope.
        target=envelope_state(2281,layout);held=target['envelope']
        target_left,target_lw=translated(target['_hand_plan']['left'],target['_hand_origins']['left'],held,PARKED_ENVELOPE)
        old_left=s['_hand_plan']['left'];old_lw=s['_hand_origins']['left']
        free={'surface':'free_transfer','index_active':False,'thumb_active':False}
        rc={'surface':'letter','index_active':True,'thumb_active':True,'contact':add(pos,(.065,-.135,0)),'index_offset':.009,'thumb_offset':.011}
        if frame<=2348:
            left,lw=blend_hand(old_left,old_lw,target_left,target_lw,progress(frame,2316,2348));lc=free
            phase='reach_parked_envelope'
        else:
            origin=mix(PARKED_ENVELOPE,held,progress(frame,2348,2388));s['envelope']=origin
            left,lw=translated(target_left,target_lw,PARKED_ENVELOPE,origin)
            lc={'surface':'envelope','index_active':True,'thumb_active':True}
            right,rw=blend_hand(s['_hand_plan']['right'],s['_hand_origins']['right'],target['_hand_plan']['right'],target['_hand_origins']['right'],progress(frame,2348,2388))
            s['_hand_plan']['right']=right;s['_hand_origins']['right']=rw;rc=free
            phase='lift_envelope_transfer_right'
        s['_hand_plan']['left']=left;s['_hand_origins']['left']=lw
        s.pop('_paper_contacts');s['_envelope_contacts']={'left':lc,'right':rc}
        s['_envelope_flap_angle']=0;s['_envelope_mouth_angle']=0;s['_envelope_phase']=phase;s['_paper_support']='table';s['_insertion']=0
        s['_sequence_phase']=phase
    for side in ('left','right'):
        j=s['joints'];w=s['_hand_origins'][side];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
        pole=sub(w,mul(axis,FOREARM_LENGTH))
        # Envelope pickup ends at the approved opening elbow solution.
        if frame>2348 and side=='right':
            target=envelope_state(2281,layout)
            pole=mix(pole,target['joints']['right_arm'][1],progress(frame,2348,2388))
        e=two_segment(j[side+'_arm'][0],w,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
        j[side+'_arm']=(j[side+'_arm'][0],e,w)
    return s
