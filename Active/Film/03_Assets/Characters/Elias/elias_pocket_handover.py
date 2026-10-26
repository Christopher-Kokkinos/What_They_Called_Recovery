"""Focused closed-paper → supported regrip → inner pocket → second mug pickup.

Diagnostic time only. Established source clips remain unmodified.
"""
from copy import deepcopy
import math
from elias_paper_refinement import state as paper
from elias_inner_pocket import state as pocket,point,vector
from elias_table_reach import state as mug
from elias_table_handover import body_map
from elias_envelope_contact import blend_hand
from elias_paper_contact import pinch
from elias_articulation import add,sub,mul,mix,dot,cross,unit,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
from sc001_room_performance import progress
START,END=1,397
ATTACH,RELEASE=157,200
POCKET_END=226
PICKUP_START=287
PAPER_BASIS=((1,0,0),(0,0,1),(0,-1,0))
SUPPORT_EDGE=(.11,-.05)

def basis_blend(a,b,t):
    x=unit(mix(a[0],b[0],t));y=mix(a[1],b[1],t);y=unit(sub(y,mul(x,dot(x,y))));return x,y,unit(cross(x,y))

def packet_hand(h,w,a,ab,b,bb):
    def v(p):return tuple(sum(bb[k][i]*dot(p,ab[k]) for k in range(3)) for i in range(3))
    def p(p):return add(b,v(sub(p,a)))
    h=deepcopy(h);h['palm']['center']=p(h['palm']['center']);h['palm']['basis']=tuple(v(x) for x in h['palm']['basis']);h['chains']={d:[p(x) for x in ch] for d,ch in h['chains'].items()}
    return h,p(w)

def solve(s,side,h,w,pole):
    j=s['joints'];sh=j[side+'_arm'][0];s['_hand_plan'][side]=h;s['_hand_origins'][side]=w;j[side+'_arm']=(sh,two_segment(sh,w,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH),w)

def limit_free_wrist(s,side):
    """Rotate only a free hand about its wrist, preserving every digit length."""
    sh,e,w=s['joints'][side+'_arm'];h=s['_hand_plan'][side]
    a=mul(h['palm']['basis'][2],-1);b=unit(sub(w,e));angle=math.acos(max(-1,min(1,dot(a,b))))
    turn=max(0,angle-math.radians(60))
    if turn==0:return
    axis=unit(cross(a,b))
    def v(p):return add(add(mul(p,math.cos(turn)),mul(cross(axis,p),math.sin(turn))),mul(axis,dot(axis,p)*(1-math.cos(turn))))
    def p(x):return add(w,v(sub(x,w)))
    h['palm']['center']=p(h['palm']['center']);h['palm']['basis']=tuple(v(x) for x in h['palm']['basis']);h['chains']={d:[p(x) for x in ch] for d,ch in h['chains'].items()}

def state(frame,layout):
    f=START if frame==889 else frame;assert START<=f<=END
    a=paper(2720,layout);a['_packet_basis_override']=PAPER_BASIS
    p=pocket(1,layout);last=pocket(70,layout)
    # Left hand supports a separate packet edge while right hand changes grip.
    contact=add(add(a['envelope'],mul(PAPER_BASIS[0],SUPPORT_EDGE[0])),mul(PAPER_BASIS[1],SUPPORT_EDGE[1]))
    direction=unit(vector(a['joints'],-.8,.3,.3))
    pn=unit(sub(a['joints']['forward'],mul(direction,dot(a['joints']['forward'],direction))))
    lh,lw=pinch(contact,PAPER_BASIS[2],direction,'left',palm_normal=pn,index_offset=.016)
    support_pole=point(a['joints'],.40,.20,.20)
    support_elbow=two_segment(a['joints']['left_arm'][0],lw,support_pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
    rh,rw=packet_hand(p['_hand_plan']['right'],p['_hand_origins']['right'],p['envelope'],p['_packet_basis_override'],a['envelope'],PAPER_BASIS)
    if f<=16:
        s=paper(2704+f,layout);s['_packet_basis_override']=PAPER_BASIS;phase='accepted_closed_packet_tail';support='right_hand'
    elif f<=56:
        s=deepcopy(a);t=progress(f,16,56);h,w=blend_hand(a['_hand_plan']['left'],a['_hand_origins']['left'],lh,lw,t)
        solve(s,'left',h,w,mix(a['joints']['left_arm'][1],support_elbow,t));phase='left_reaches_packet_support';support='right_hand'
    elif f<=96:
        s=deepcopy(a);t=progress(f,56,96);h,w=blend_hand(a['_hand_plan']['right'],a['_hand_origins']['right'],rh,rw,t)
        solve(s,'left',lh,lw,support_elbow)
        solve(s,'right',h,w,mix(a['joints']['right_arm'][1],sub(rw,mul(rh['palm']['basis'][2],-FOREARM_LENGTH)),t));phase='right_regrip_left_supports';support='left_hand'
    elif f<ATTACH:
        s=deepcopy(a);t=progress(f,96,156);B=basis_blend(PAPER_BASIS,p['_packet_basis_override'],t);center=mix(a['envelope'],p['envelope'],t)
        s['envelope']=center;s['_packet_basis_override']=B
        # Letter remains rigidly nested in the closed envelope.
        s['letter']=add(add(center,mul(B[1],.07425)),mul(B[2],.0035))
        h,w=packet_hand(rh,rw,a['envelope'],PAPER_BASIS,center,B)
        aligned=sub(w,mul(h['palm']['basis'][2],-FOREARM_LENGTH));solve(s,'right',h,w,mix(aligned,p['joints']['right_arm'][1],t))
        h,w=blend_hand(lh,lw,p['_hand_plan']['left'],p['_hand_origins']['left'],t)
        start_pole=support_elbow
        solve(s,'left',h,w,mix(start_pole,p['joints']['left_arm'][1],t))
        limit_free_wrist(s,'left');phase='packet_carry_and_lapel_approach';support='right_hand'
    elif f<=POCKET_END:
        s=pocket(f-ATTACH+1,layout);phase='inner_pocket_'+s['_sequence_phase'];support=s['_paper_support'];s['_inner_pocket']['support_active']=f>=ATTACH+39
    elif f<PICKUP_START:
        s=deepcopy(last);target=mug(2400,layout);t=progress(f,POCKET_END,286)
        for side in ('left','right'):
            h,w=blend_hand(last['_hand_plan'][side],last['_hand_origins'][side],target['_hand_plan'][side],target['joints'][side+'_arm'][-1],t)
            solve(s,side,h,w,mix(last['joints'][side+'_arm'][1],target['joints'][side+'_arm'][1],t))
        phase='hands_clear_pocket_to_mug_start';support='inner_pocket'
    else:
        s=mug(2400+f-PICKUP_START,layout)
        h=s['_hand_plan']['left'];w=s['joints']['left_arm'][-1];aligned=sub(w,mul(h['palm']['basis'][2],-FOREARM_LENGTH));t=progress(f,PICKUP_START,PICKUP_START+30)
        solve(s,'left',h,w,add(mix(mug(2400,layout)['joints']['left_arm'][1],aligned,t),mul(s['joints']['lateral'],-.4*math.sin(math.pi*t))))
        if f<PICKUP_START+30:limit_free_wrist(s,'left')
        for key in ('envelope','letter'):s[key]=body_map(last[key],last['joints'],s['joints'])
        s['_packet_basis_override']=tuple(body_map(v,last['joints'],s['joints'],True) for v in last['_packet_basis_override'])
        phase='accepted_second_mug_pickup_packet_pocketed';support='inner_pocket'
    s.pop('_envelope_contacts',None);s.pop('_paper_contacts',None)
    s.setdefault('_packet_basis_override',PAPER_BASIS)
    if f<ATTACH:
        s['_inner_pocket']={**p['_inner_pocket'],'opening':0,'bulge':0,'left_active':False,'right_index_active':False,'right_thumb_active':False,'support_active':False}
    elif f>POCKET_END:
        s['_inner_pocket']={**last['_inner_pocket'],'left_active':False,'right_index_active':False,'right_thumb_active':False,'support_active':True}
    s['_inner_pocket']['hand_influence']=1 if ATTACH<=f<RELEASE else 0
    if f<PICKUP_START:s['mug']=a['mug'];s['_mug_basis']=mug(2400,layout)['_mug_basis']
    s['_mug_on_table']=f<=PICKUP_START+50
    s['keys']=(11.65,9.05,.978);s['fold']=1;s['_envelope_flap_angle']=0;s['_envelope_mouth_angle']=0;s['_notice_hidden']=True
    s['_sequence_phase']=phase;s['_paper_support']=support;s['_palm_controls']=('left','right');s['frame']=f
    for side in ('left','right'):s.setdefault('_hand_origins',{})[side]=s['joints'][side+'_arm'][-1]
    return s
