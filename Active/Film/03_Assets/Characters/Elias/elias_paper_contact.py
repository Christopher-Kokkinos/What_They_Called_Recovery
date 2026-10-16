"""Bounded paper pickup/fold contract; provisional contact, not sheet simulation."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,mix,unit,cross,two_segment
from elias_table_reach import state as table_state
from sc001_room_performance import progress,solve_arm
START,END=2161,2260
_CACHE={}

def pinch(contact,normal,direction,side):
    """Opposed pads at a paper edge; fixed phalange lengths and connected wrist."""
    z=mul(direction,-1);x=unit(cross(normal,z));basis=(x,normal,z)
    center=add(sub(contact,mul(direction,.065)),mul(normal,.025))
    chains={};tips={}
    for i,digit in enumerate(('index','middle','ring','little')):
        length=(.065,.072,.068,.055)[i];lengths=(length*.42,length*.33,length*.25)
        base=add(add(center,mul(direction,.027)),mul(x,(i-1.5)*.019))
        if digit=='index':tip=add(contact,mul(normal,.009))
        else:tip=add(add(base,mul(direction,length*.68)),mul(normal,.012))
        middle=two_segment(base,tip,add(base,mul(normal,.07)),lengths[0],sum(lengths[1:]))
        chains[digit]=[base,middle,mix(middle,tip,lengths[1]/sum(lengths[1:])),tip]
        tips[digit]=tip
    base=add(add(center,mul(direction,.025)),mul(x,.02))
    tip=add(contact,mul(normal,-.011));lengths=(.025,.023,.020)
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
    lift=progress(frame,2175,2215);fold=progress(frame,2220,2260);angle=math.pi*fold
    s['letter']=(11.12,9.30,.971+.25*lift);s['envelope']=(11.60,9.35,.971);s['mug']=(11.24,8.98,1.06);s['keys']=(11.65,9.05,.978)
    s['fold']=fold;s['packet_pocket']=False;s['pocket_rotation']=0;s['_palm_controls']=('left','right')
    s['_hand_origins']={};contacts={}
    for side in ('left','right'):
        if side=='left':
            contact=add(s['letter'],(-.065,.135*math.cos(angle),.002+.135*math.sin(angle)))
            normal=(0,-math.sin(angle),math.cos(angle));direction=(0,-math.cos(angle),-math.sin(angle))
        else:
            contact=add(s['letter'],(.065,-.135,0));normal=(0,0,1);direction=(0,1,0)
        hand,wrist=pinch(contact,normal,direction,side)
        s['_hand_plan'][side]=hand;s['_hand_origins'][side]=wrist
        j=s['joints'];j[side+'_arm']=solve_arm(j[side+'_arm'][0],wrist,j['up'],j['lateral'],-1 if side=='left' else 1,.16)
        contacts[side]=hand['pinch']
    s['_paper_contacts']=contacts
    _CACHE[key]=deepcopy(s)
    return s
