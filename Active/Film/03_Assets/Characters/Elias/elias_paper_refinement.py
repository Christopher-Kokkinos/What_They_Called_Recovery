"""Bounded timing and free-hand refinement over the reviewed paper sequence."""
from copy import deepcopy
from elias_paper_sequence import state as baseline
from elias_envelope_contact import blend_hand
from elias_articulation import mix,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
from sc001_room_performance import progress
START,END=2161,2720
TRANSFER_START,TRANSFER_END=2532,2564

def source_frame(frame):
    """Old sequence coordinates; transfer interior has no legacy source pose."""
    if frame<=2240:return frame
    if frame<=2250:return 2240+2*(frame-2240)
    if frame<=TRANSFER_START:return frame+10
    if frame<TRANSFER_END:return None
    return frame+42

def state(frame,layout):
    frame=START if frame==889 else frame
    assert START<=frame<=END
    source=source_frame(frame)
    if source is not None:
        s=baseline(source,layout);s['_refinement_source_frame']=source;s['frame']=frame
        return s
    a=baseline(2542,layout);b=baseline(2606,layout);s=deepcopy(a)
    t=progress(frame,TRANSFER_START,TRANSFER_END)
    hand,wrist=blend_hand(a['_hand_plan']['right'],a['_hand_origins']['right'],b['_hand_plan']['right'],b['_hand_origins']['right'],t)
    s['_hand_plan']['right']=hand;s['_hand_origins']['right']=wrist
    for side in ('left','right'):
        shoulder=s['joints'][side+'_arm'][0];w=s['_hand_origins'][side]
        pole=mix(a['joints'][side+'_arm'][1],b['joints'][side+'_arm'][1],t)
        e=two_segment(shoulder,w,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
        s['joints'][side+'_arm']=(shoulder,e,w)
    s['_envelope_contacts']['right']={'surface':'free_transfer','index_active':False,'thumb_active':False}
    s['frame']=frame;s['_refinement_source_frame']=None;s['_sequence_phase']='direct_transfer_to_flap';s['_envelope_phase']='direct_transfer_to_flap'
    s['_paper_support']='envelope'
    return s
