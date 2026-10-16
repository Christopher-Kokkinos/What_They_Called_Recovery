"""Supported mug/paper handovers; isolated table sequence, packet remains held."""
from copy import deepcopy
import math
from elias_table_reach import state as mug_state
from elias_paper_refinement import state as paper_state
from elias_envelope_contact import blend_hand
from elias_articulation import add,sub,mul,mix,dot,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
from sc001_room_performance import progress
START,END=1500,2271
WINDOWS=[('mug_release_to_paper',1500,1620),('paper_to_second_mug_pickup',2140,2271)]

def body_map(point,a,b,vector=False):
    v=point if vector else sub(point,a['pelvis'])
    out=(0,0,0)
    for name in ('lateral','forward','up'):out=add(out,mul(b[name],dot(v,a[name])))
    return out if vector else add(b['pelvis'],out)

def overlay_packet(s,held):
    """Right hand and packet follow torso rigidly while left picks up the mug."""
    a=held['joints'];b=s['joints'];point=lambda p:body_map(p,a,b);vector=lambda p:body_map(p,a,b,True)
    h=deepcopy(held['_hand_plan']['right']);h['palm']['center']=point(h['palm']['center']);h['palm']['basis']=tuple(vector(v) for v in h['palm']['basis'])
    h['chains']={d:[point(p) for p in chain] for d,chain in h['chains'].items()}
    s['_hand_plan']['right']=h;s['_hand_origins']['right']=point(held['_hand_origins']['right'])
    s['joints']['right_arm']=tuple(point(p) for p in a['right_arm'])
    for k in ('letter','envelope'):s[k]=point(held[k])
    s['fold']=1;s['_envelope_flap_angle']=0;s['_envelope_mouth_angle']=0
    # Closed packet starts vertical; retain that orientation relative to torso.
    s['_packet_basis_override']=tuple(vector(v) for v in ((1,0,0),(0,0,1),(0,-1,0)))
    s['_envelope_contacts']={'left':{'surface':'free_transfer','index_active':False,'thumb_active':False},'right':{'surface':'envelope','index_active':True,'thumb_active':True}}
    s['_paper_support']='right_hand';s['_insertion']=1;s['_envelope_phase']='hold_packet_second_mug_pickup'
    return s

def state(frame,layout):
    frame=START if frame==889 else frame
    assert START<=frame<=END
    if frame<=1560:
        s=mug_state(frame,layout);s['letter']=paper_state(2161,layout)['letter'];s['envelope']=paper_state(2161,layout)['envelope'];s['keys']=(11.65,9.05,.978)
        s['fold']=0;s['_handover_phase']='mug_place_and_release'
    elif frame<=1600:
        a=state(1560,layout);b=paper_state(2161,layout);s=deepcopy(b);t=progress(frame,1560,1600)
        s['_paper_contacts']={side:{**c,'active':False} for side,c in s['_paper_contacts'].items()}
        for side in ('left','right'):
            h,w=blend_hand(a['_hand_plan'][side],a['joints'][side+'_arm'][-1],b['_hand_plan'][side],b['_hand_origins'][side],t)
            s['_hand_plan'][side]=h;s['_hand_origins'][side]=w
            s['_paper_contacts'][side].update(index_tip=h['chains']['index'][-1],thumb_tip=h['chains']['thumb'][-1])
            j=s['joints'];shoulder=j[side+'_arm'][0]
            pole=mix(a['joints'][side+'_arm'][1],b['joints'][side+'_arm'][1],t)
            j[side+'_arm']=(shoulder,two_segment(shoulder,w,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH),w)
        s['_handover_phase']='free_hands_to_parked_paper'
    elif frame<=2160:
        s=paper_state(frame+560,layout);s['_handover_phase']='paper_sequence'
    else:
        source=frame+239;s=mug_state(source,layout);s['_handover_phase']='second_mug_pickup_with_packet_held'
        held=paper_state(2720,layout);s=overlay_packet(s,held);s['keys']=(11.65,9.05,.978)
        j=s['joints'];sh,_,w=j['left_arm']
        axis=mul(s['_hand_plan']['left']['palm']['basis'][2],-1)
        aligned=sub(w,mul(axis,FOREARM_LENGTH))
        pole=mix(held['joints']['left_arm'][1],aligned,progress(frame,2161,2171))
        j['left_arm']=(sh,two_segment(sh,w,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH),w)
    s['_palm_controls']=('left','right')
    for side in ('left','right'):s.setdefault('_hand_origins',{})[side]=s['joints'][side+'_arm'][-1]
    s['_mug_on_table']=1540<=frame<=2211
    s['_notice_hidden']=frame>=1660
    s['frame']=frame
    return s
