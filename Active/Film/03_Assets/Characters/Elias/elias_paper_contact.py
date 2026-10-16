"""Bounded paper pickup/fold contract; provisional contact, not sheet simulation."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,mix,unit,cross,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH
from elias_table_reach import state as table_state
from sc001_room_performance import progress,solve_arm
START,END=2161,2280
_CACHE={}

def pinch(contact,normal,direction,side,palm_normal=None,opening=0,thumb_offset=.011,index_offset=.009):
    """Opposed pads at a paper edge; fixed phalange lengths and connected wrist."""
    palm_normal=palm_normal or normal
    z=mul(direction,-1);x=unit(cross(palm_normal,z));basis=(x,palm_normal,z)
    center=add(sub(contact,mul(direction,.065)),mul(palm_normal,.025))
    chains={};tips={}
    for i,digit in enumerate(('index','middle','ring','little')):
        length=(.065,.072,.068,.055)[i];lengths=(length*.42,length*.33,length*.25)
        base=add(add(center,mul(direction,.027)),mul(x,(i-1.5)*.019))
        if digit=='index':tip=add(contact,mul(normal,index_offset+opening))
        else:tip=add(add(base,mul(direction,length*.68)),mul(normal,.012))
        middle=two_segment(base,tip,add(base,mul(normal,.07)),lengths[0],sum(lengths[1:]))
        chains[digit]=[base,middle,mix(middle,tip,lengths[1]/sum(lengths[1:])),tip]
        tips[digit]=tip
    base=add(add(center,mul(direction,.025)),mul(x,.02))
    tip=add(contact,mul(normal,-thumb_offset-opening));lengths=(.025,.023,.020)
    middle=two_segment(base,tip,add(base,mul(x,.06)),lengths[0],sum(lengths[1:]))
    chains['thumb']=[base,middle,mix(middle,tip,lengths[1]/sum(lengths[1:])),tip];tips['thumb']=tip
    wrist=sub(center,mul(direction,.045))
    return {'palm':{'center':center,'size':(.075,.026,.075),'basis':basis},'chains':chains,'mode':'paper_edge_pinch','suffix':'L' if side=='left' else 'R','pinch':{'contact':contact,'normal':normal,'index_tip':tips['index'],'thumb_tip':tip}},wrist

def state(frame,layout):
    frame=START if frame==889 else frame
    assert START<=frame<=END,frame
    key=(frame,json.dumps(layout,sort_keys=True))
    if key in _CACHE:return deepcopy(_CACHE[key])
    s=deepcopy(table_state(1400,layout));s['frame']=frame;s['phase']='paper_contact_trial';s['paper_two_hands']=True
    lift=progress(frame,2175,2215);fold=.5*progress(frame,2220,2240)+.5*progress(frame,2260,2280);angle=math.pi*fold
    s['letter']=(11.12+.14*progress(frame,2205,2220),9.30,.971+.25*lift);s['envelope']=(11.60,9.35,.971);s['mug']=(11.24,8.98,1.06);s['keys']=(11.65,9.05,.978)
    s['fold']=fold;s['packet_pocket']=False;s['pocket_rotation']=0;s['_palm_controls']=('left','right')
    s['_hand_origins']={};contacts={}
    for side in ('left','right'):
        if side=='left':
            edge=add(s['letter'],(-.105,.135*math.cos(angle),.002+.135*math.sin(angle)))
            regrip=progress(frame,2240,2260);withdraw=math.sin(math.pi*regrip)
            if 2240<frame<2260:normal=(0,-math.cos(math.pi*regrip),math.sin(math.pi*regrip))
            else:normal=mul((0,-math.sin(angle),math.cos(angle)),1 if frame<=2240 else -1)
            contact=add(edge,(-.08*withdraw,0,.02*withdraw))
            pitch=math.radians(-36.87+56.87*lift)
            direction=(math.cos(pitch),0,math.sin(pitch))
            palm_normal=(-math.sin(pitch),0,math.cos(pitch));opening=.006*withdraw
            active=not 2240<frame<2260

        else:
            contact=add(s['letter'],(.065,-.135,0));normal=(0,0,1);direction=(0,1,0)
            palm_normal=normal;opening=0;active=True;edge=contact
        thumb_offset=.011+(.002*progress(frame,2260,2280) if side=='left' else 0)
        hand,wrist=pinch(contact,normal,direction,side,palm_normal,opening,thumb_offset)
        s['_hand_plan'][side]=hand;s['_hand_origins'][side]=wrist
        j=s['joints'];shoulder=j[side+'_arm'][0]
        # Choose the elbow circle point nearest a forearm aligned with the hand.
        # This shares the reach between shoulder and elbow instead of bending the wrist to compensate.
        pole=sub(wrist,mul(direction,FOREARM_LENGTH))
        elbow=two_segment(shoulder,wrist,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
        j[side+'_arm']=(shoulder,elbow,wrist)
        contacts[side]={**hand['pinch'],'active':active,'surface_contact':edge,'surface_sign':1 if side=='right' or frame<=2240 else -1,'opening':opening,'thumb_offset':thumb_offset}
    s['_paper_phase']='regrip' if 2240<frame<2260 else 'finish_fold' if frame>=2260 else 'partial_fold' if frame>=2220 else 'pickup'
    s['_paper_support_hands']=['right'] if 2240<frame<2260 else ['left','right']
    s['_paper_contacts']=contacts
    _CACHE[key]=deepcopy(s)
    return s
