"""Isolated flap opening, supported paper pickup, insertion and release."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,mix,unit,cross,dot,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
from elias_paper_contact import pinch
from elias_table_reach import state as table_state,relaxed_arm
from sc001_room_performance import progress
START,END=2281,2440
_CACHE={}

def digit_target(hand,digit,tip):
    points=hand['chains'][digit];lengths=[math.dist(a,b) for a,b in zip(points,points[1:])]
    base=points[0];pole=add(base,mul(hand['palm']['basis'][1],.08))
    middle=two_segment(base,tip,pole,lengths[0],sum(lengths[1:]))
    hand['chains'][digit]=[base,middle,mix(middle,tip,lengths[1]/sum(lengths[1:])),tip]
    hand['pinch'][digit+'_tip']=tip

def blend_hand(a,aw,b,bw,t):
    """Free transfer only: preserve phalanges while interpolating targets."""
    hand=deepcopy(a);x=unit(mix(a['palm']['basis'][0],b['palm']['basis'][0],t))
    y=mix(a['palm']['basis'][1],b['palm']['basis'][1],t);y=unit(sub(y,mul(x,dot(x,y))));z=unit(cross(x,y))
    hand['palm']={**a['palm'],'center':mix(a['palm']['center'],b['palm']['center'],t),'basis':(x,y,z)}
    for digit,ap in a['chains'].items():
        bp=b['chains'][digit];points=[mix(ap[0],bp[0],t)]
        for a0,a1,b0,b1 in zip(ap,ap[1:],bp,bp[1:]):
            direction=unit(mix(unit(sub(a1,a0)),unit(sub(b1,b0)),t))
            points.append(add(points[-1],mul(direction,math.dist(a0,a1))))
        hand['chains'][digit]=points
    return hand,mix(aw,bw,t)

def envelope_geometry(frame):
    flap=math.pi*progress(frame,2281,2305);mouth=.20*progress(frame,2281,2305)
    return flap,mouth

def folded_origin(frame):
    parked=(11.12,9.40,.971);aligned=(11.26,9.203,1.2135)
    if frame<=2340:return parked
    if frame<=2365:return mix(parked,aligned,progress(frame,2340,2365))
    return add(aligned,(0,.17125*progress(frame,2365,2420),0))

def letter_grip(frame):
    origin=folded_origin(frame);contact=add(origin,(.065,-.135,0))
    hand,wrist=pinch(contact,(0,0,1),(0,1,0),'right',thumb_offset=.011,index_offset=.011)
    insertion=progress(frame,2365,2420);release=progress(insertion,.60,.80)
    # Thumb clears the slot while the envelope takes over support.
    target=hand['pinch']['thumb_tip'];target=mix(target,(target[0],9.19,target[2]),release)
    digit_target(hand,'thumb',target)
    # Non-contact fingers curl above the mouth instead of reaching into it.
    for digit in ('middle','ring','little'):
        base=hand['chains'][digit][0]
        digit_target(hand,digit,add(base,(0,.018,.035)))
    return hand,wrist,{'surface':'letter','index_active':True,'thumb_active':release==0,'contact':contact,'normal':(0,0,1),'index_offset':.011,'thumb_offset':.011,'thumb_release':release}

def flap_grip(frame):
    flap,_=envelope_geometry(frame);env=(11.26,9.30,1.21)
    contact=add(env,(.10,-.085+.045*math.cos(flap),.010+.045*math.sin(flap)))
    normal=(0,-math.sin(flap),math.cos(flap))
    direction=unit((.65,.75,-.12));palm_normal=unit(sub((0,0,1),mul(direction,direction[2])))
    hand,wrist=pinch(contact,normal,direction,'right',palm_normal=palm_normal)
    return hand,wrist,{'surface':'flap','index_active':True,'thumb_active':True,'contact':contact,'normal':normal,'index_offset':.009,'thumb_offset':.011}

def state(frame,layout):
    frame=START if frame==889 else frame
    assert START<=frame<=END,frame
    key=(frame,json.dumps(layout,sort_keys=True))
    if key in _CACHE:return deepcopy(_CACHE[key])
    s=deepcopy(table_state(1400,layout));s['frame']=frame;s['phase']='envelope_contact_trial';s['paper_two_hands']=True
    s['envelope']=(11.26,9.30,1.21);s['letter']=folded_origin(frame);s['mug']=(11.24,8.98,1.06);s['keys']=(11.65,9.05,.978)
    s['fold']=1;s['packet_pocket']=False;s['pocket_rotation']=0;s['_palm_controls']=('left','right');s['_hand_origins']={}
    flap,mouth=envelope_geometry(frame);s['_envelope_flap_angle']=flap;s['_envelope_mouth_angle']=mouth
    # Grip close to the closed end. Front and back are separate surfaces.
    contact=add(s['envelope'],(-.11,.065,0));front_height=.008+.020*math.tan(mouth)
    left,lw=pinch(contact,(0,0,1),(.8,0,-.6),'left',palm_normal=(.6,0,.8),index_offset=front_height+.008/math.cos(mouth))
    contacts={'left':{'surface':'envelope','index_active':True,'thumb_active':True,'contact':contact,'normal':(0,0,1),'index_offset':front_height+.008/math.cos(mouth),'thumb_offset':.011}}
    if frame<=2305:
        right,rw,c=flap_grip(frame);phase='open_flap'
    elif frame<2340:
        a,aw,_=flap_grip(2305);b,bw,_=letter_grip(2340)
        right,rw=blend_hand(a,aw,b,bw,progress(frame,2305,2340));c={'surface':'free_transfer','index_active':False,'thumb_active':False};phase='transfer_to_parked_letter'
    elif frame<=2420:
        right,rw,c=letter_grip(frame);phase='lift_align' if frame<2365 else 'insert'
    else:
        a,aw,_=letter_grip(2420);neutral=deepcopy(s);relaxed_arm(neutral,'right');b=neutral['_hand_plan']['right'];bw=neutral['joints']['right_arm'][-1]
        right,rw=blend_hand(a,aw,b,bw,progress(frame,2420,2440));c={'surface':'free_release','index_active':False,'thumb_active':False};phase='withdraw_hand'
    contacts['right']=c;s['_hand_plan']={'left':left,'right':right};s['_hand_origins']={'left':lw,'right':rw}
    for side,wrist in [('left',lw),('right',rw)]:
        j=s['joints'];shoulder=j[side+'_arm'][0];direction=mul(s['_hand_plan'][side]['palm']['basis'][2],-1)
        pole=sub(wrist,mul(direction,FOREARM_LENGTH))
        if side=='right' and frame<2340:
            pole=add(add(add(shoulder,mul(j['up'],-.35)),mul(j['lateral'],.45)),mul(j['forward'],.15))
        elbow=two_segment(shoulder,wrist,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
        j[side+'_arm']=(shoulder,elbow,wrist)
    insertion=progress(frame,2365,2420)
    s['_envelope_contacts']=contacts;s['_envelope_phase']=phase;s['_insertion']=insertion
    s['_paper_support']='table' if frame<=2340 else 'right_hand' if frame<=2365 else 'right_hand_and_envelope' if frame<2420 else 'envelope'
    _CACHE[key]=deepcopy(s);return s
