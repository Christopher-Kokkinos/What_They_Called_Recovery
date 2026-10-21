"""Bounded breast-pocket proxy: supported packet placement and hand release."""
from copy import deepcopy
import math
from elias_paper_refinement import state as paper_state
from elias_envelope_contact import blend_hand
from elias_table_reach import relaxed_arm
from elias_articulation import add,sub,mul,mix,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
from sc001_room_performance import progress
START,END=2720,2940
FLOOR,MOUTH=.29,.39

def rotate(v,t):
    a=math.pi/2*t;c,s=math.cos(a),math.sin(a);x,y,z=v;x,y=x*c-y*s,x*s+y*c
    a=.20*t;c,s=math.cos(a),math.sin(a)
    return (x*c+z*s,y,-x*s+z*c)

def local_point(j,width,front,height):
    return add(add(add(j['pelvis'],mul(j['lateral'],-width)),mul(j['forward'],front)),mul(j['up'],height))

def move_hand(h,w,origin,target,t,offset=(0,0,0)):
    h=deepcopy(h);point=lambda p:add(add(target,rotate(sub(p,origin),t)),offset)
    h['palm']['center']=point(h['palm']['center']);h['palm']['basis']=tuple(rotate(v,t) for v in h['palm']['basis'])
    h['chains']={d:[point(p) for p in chain] for d,chain in h['chains'].items()}
    return h,point(w)

def state(frame,layout):
    frame=START if frame==889 else frame
    assert START<=frame<=END
    base=paper_state(2720,layout);s=deepcopy(base);s['frame']=frame;j=s['joints'];origin=base['envelope']
    align=progress(frame,2720,2750);down=progress(frame,2774,2820)
    above=local_point(j,.08,.19,.55);seated=local_point(j,.08,.19,.375)
    center=mix(origin,above,align) if frame<=2750 else mix(above,seated,down)
    s['envelope']=center;s['letter']=add(center,rotate(sub(base['letter'],origin),align))
    s['_packet_basis_override']=tuple(rotate(v,align) for v in ((1,0,0),(0,0,1),(0,-1,0)))
    regrip=mul(j['up'],.03*progress(frame,2750,2774))
    h,w=move_hand(base['_hand_plan']['right'],base['_hand_origins']['right'],origin,center,align,regrip)
    phase='align_above_pocket' if frame<2750 else 'slide_grip_to_top' if frame<2774 else 'insert_to_pocket_floor' if frame<2820 else 'release_and_clear' if frame<2850 else 'lower_free_hand'
    active=frame<=2820
    if frame>2820:
        # First move forward/up clear of the lip; then lower the now-free hand.
        h0,w0=move_hand(base['_hand_plan']['right'],base['_hand_origins']['right'],origin,seated,1,mul(j['up'],.03))
        shift=add(mul(j['forward'],.10),mul(j['up'],.04))
        waypoint,ww=move_hand(h0,w0,(0,0,0),(0,0,0),0,shift)
        if frame<=2850:h,w=blend_hand(h0,w0,waypoint,ww,progress(frame,2820,2850))
        else:
            neutral=deepcopy(s);relaxed_arm(neutral,'right')
            nh=neutral['_hand_plan']['right'];nw=neutral['joints']['right_arm'][-1]
            outside=local_point(j,-.25,.35,.35)
            oh,ow=move_hand(nh,nw,(0,0,0),(0,0,0),0,sub(outside,nw))
            if frame<=2890:h,w=blend_hand(waypoint,ww,oh,ow,progress(frame,2850,2890))
            else:h,w=blend_hand(oh,ow,nh,nw,progress(frame,2890,2940))
    s['_hand_plan']['right']=h;s['_hand_origins']['right']=w
    shoulder=j['right_arm'][0];axis=mul(h['palm']['basis'][2],-1)
    low=add(add(add(shoulder,mul(j['up'],-.35)),mul(j['lateral'],.25)),mul(j['forward'],-.10))
    pole=mix(base['joints']['right_arm'][1],low,progress(frame,2720,2740))
    pole=mix(pole,sub(w,mul(axis,FOREARM_LENGTH)),progress(frame,2738,2750));e=two_segment(shoulder,w,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
    j['right_arm']=(shoulder,e,w)
    if frame==START:j['right_arm']=base['joints']['right_arm']
    free={'surface':'free_transfer','index_active':False,'thumb_active':False}
    s['_envelope_contacts']={'left':free,'right':{'surface':'envelope','index_active':active,'thumb_active':active}}
    s['_sequence_phase']=phase;s['_envelope_phase']=phase;s['_paper_support']='pocket_floor' if frame>=2820 else 'right_hand';s['_insertion']=1
    s['_notice_hidden']=True;s['_pocket_proxy']=True;s['_pocket_released']=frame>2820
    return s

def proxy_boxes(s):
    j=s['joints'];basis=(mul(j['lateral'],-1),mul(j['forward'],-1),j['up'])
    specs=[('front',.08,.245,.34,(.27,.01,.10)),('back',.08,.165,.34,(.27,.01,.10)),('bottom',.08,.205,.285,(.27,.09,.01)),('left',-.05,.205,.34,(.01,.09,.10)),('right',.21,.205,.34,(.01,.09,.10))]
    return [{'name':'REVIEW_Pocket_'+name,'center':local_point(j,x,y,z),'size':size,'basis':basis} for name,x,y,z,size in specs]
