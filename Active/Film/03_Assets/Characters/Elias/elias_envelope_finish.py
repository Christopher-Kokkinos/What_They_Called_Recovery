"""Isolated envelope closure, supported handover and provisional pocket approach."""
from copy import deepcopy
import math
from elias_envelope_contact import state as prior,blend_hand
from elias_paper_contact import pinch
from elias_table_reach import relaxed_arm
from elias_articulation import add,sub,mul,mix,two_segment,FOREARM_LENGTH,UPPER_ARM_LENGTH
from sc001_room_performance import progress
START,END=2474,2654

def rotate(p,a):
    x,y,z=p;return (x,y*math.cos(a)-z*math.sin(a),y*math.sin(a)+z*math.cos(a))

def translated(hand,wrist,origin,target,angle=0):
    hand=deepcopy(hand)
    point=lambda p:add(target,rotate(sub(p,origin),angle))
    hand['palm']['center']=point(hand['palm']['center'])
    hand['palm']['basis']=tuple(rotate(v,angle) for v in hand['palm']['basis'])
    hand['chains']={d:[point(p) for p in chain] for d,chain in hand['chains'].items()}
    return hand,point(wrist)

def state(frame,layout):
    frame=START if frame==889 else frame
    assert START<=frame<=END
    s=prior(START,layout);s['frame']=frame
    env=s['envelope'];left=s['_hand_plan']['left'];lw=s['_hand_origins']['left']
    neutral=deepcopy(s);relaxed_arm(neutral,'left');rest_left=neutral['_hand_plan']['left'];rest_lw=neutral['joints']['left_arm'][-1]
    # Close the mouth before folding the flap; retain clearance for the paper stack.
    mouth=.20*(1-progress(frame,2498,2518));flap=math.pi*(1-progress(frame,2518,2550))
    s['_envelope_mouth_angle']=mouth;s['_envelope_flap_angle']=flap
    contact=add(env,(-.11,.065,0))
    left,lw=pinch(contact,(0,0,1),(.8,0,-.6),'left',palm_normal=(.6,0,.8),index_offset=.008+.020*math.tan(mouth)+.008/math.cos(mouth))
    lc={'surface':'envelope','index_active':True,'thumb_active':True}
    def flap_hand(angle):
        contact=add(env,(.10,-.085+.045*math.cos(angle),.010+.045*math.sin(angle)))
        # Index presses from above; thumb remains below the thin flap proxy.
        from elias_articulation import unit,dot
        direction=unit((.65,.75,-.12));normal=(0,-math.sin(angle),math.cos(angle))
        pn=unit(sub((0,0,1),mul(direction,direction[2])))
        h,w=pinch(contact,normal,direction,'right',palm_normal=pn)
        return h,w,{'surface':'flap','index_active':True,'thumb_active':True,'contact':contact,'index_offset':.009,'thumb_offset':.011}
    fh,fw,fc=flap_hand(flap)
    grip,gw=pinch(add(env,(.11,.05,0)),(0,0,1),(.8,0,-.6),'right',palm_normal=(.6,0,.8),index_offset=.016,thumb_offset=.011)
    free={'surface':'free_transfer','index_active':False,'thumb_active':False}
    if frame<2498:
        right,rw=blend_hand(s['_hand_plan']['right'],s['_hand_origins']['right'],fh,fw,progress(frame,2474,2498));rc=free;phase='reach_flap'
    elif frame<=2550:right,rw,rc=fh,fw,fc;phase='close_mouth' if frame<2518 else 'fold_flap'
    elif frame<2574:
        a,aw,_=flap_hand(0);right,rw=blend_hand(a,aw,grip,gw,progress(frame,2550,2574));rc=free;phase='transfer_to_packet_edge'
    else:
        right,rw=grip,gw;rc={'surface':'envelope','index_active':True,'thumb_active':True};phase='release_left_support'
        if frame<=2594:left,lw=blend_hand(left,lw,rest_left,rest_lw,progress(frame,2574,2594))
        else:left,lw=rest_left,rest_lw
        lc=free if frame>2574 else lc
        if frame>2594:
            t=progress(frame,2594,2634);j=s['joints']
            target=add(add(j['pelvis'],mul(j['up'],.40)),add(mul(j['forward'],.08),mul(j['lateral'],.08)))
            position=mix(env,target,t);angle=math.pi/2*t
            right,rw=translated(grip,gw,env,position,angle)
            s['letter']=add(position,rotate(sub(s['letter'],env),angle));s['envelope']=position;s['_packet_rotation_x']=angle
            phase='pocket_approach' if frame<2634 else 'pocket_hold'
    s['_hand_plan']={'left':left,'right':right};s['_hand_origins']={'left':lw,'right':rw}
    for side,w in [('left',lw),('right',rw)]:
        j=s['joints'];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
        elbow=two_segment(j[side+'_arm'][0],w,sub(w,mul(axis,FOREARM_LENGTH)),UPPER_ARM_LENGTH,FOREARM_LENGTH)
        j[side+'_arm']=(j[side+'_arm'][0],elbow,w)
    s['_envelope_contacts']={'left':lc,'right':rc};s['_envelope_phase']=phase;s['_paper_support']='envelope';s['_insertion']=1
    return s
