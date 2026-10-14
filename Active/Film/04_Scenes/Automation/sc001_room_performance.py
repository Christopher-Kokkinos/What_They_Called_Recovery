"""Pure fixed-length room choreography. Provisional blocking, not final acting."""
import math
from elias_articulation import add, sub, mul, mix, unit, dot, cross, two_segment
from elias_articulation import THIGH_LENGTH, CALF_LENGTH, SPINE_LENGTH, UPPER_ARM_LENGTH, FOREARM_LENGTH

END=3168
NOTICE='I will complete work already accepted. I will not take further assignments after Friday. Please arrange final payment.'
SHOTS=[(1,360,'SH001'),(361,660,'SH002'),(661,888,'SH003'),(889,1128,'SH004'),(1129,1368,'SH005'),(1369,1560,'SH006'),(1561,2160,'SH007'),(2161,2520,'SH008'),(2521,2640,'SH009'),(2641,END,'SH010')]
ROUTE=[(2641,(.9,10.4,0)),(2690,(.9,8.8,0)),(2760,(4.5,8.1,0)),(2810,(4.5,6,0)),(3060,(13.3,6,0)),(3120,(14.8,6,0))]


def progress(frame,start,end):
    t=max(0,min(1,(frame-start)/(end-start)));return t*t*(3-2*t)


def travel(frame):
    for (a,p),(b,q) in zip(ROUTE,ROUTE[1:]):
        if frame<=b:return mix(p,q,max(0,(frame-a)/(b-a))),unit(sub(q,p))
    return ROUTE[-1][1],(1,0,0)


def world(root,forward,lateral,f,s,z):return add(add(add(root,mul(forward,f)),mul(lateral,s)),(0,0,z))


def solve_arm(shoulder,wrist,up,lateral,sign,side_bias=.16):
    # Pole goes towards the hip, not forward towards the hand. Side bias avoids
    # degeneracy for a vertical resting arm and keeps elbows outside the torso.
    pole=add(add(shoulder,mul(up,-.65)),mul(lateral,sign*side_bias))
    distance=math.dist(shoulder,wrist)
    cosine=(UPPER_ARM_LENGTH**2+FOREARM_LENGTH**2-distance**2)/(2*UPPER_ARM_LENGTH*FOREARM_LENGTH)
    flexion=180-math.degrees(math.acos(max(-1,min(1,cosine))))
    if flexion>160:raise ValueError('Excessive elbow flexion: '+str(flexion))
    elbow=two_segment(shoulder,wrist,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
    assert dot(sub(elbow,shoulder),up)<.02, 'Elbow rises above shoulder'
    return shoulder,elbow,wrist


def state(frame,layout):
    furniture={o['id']:o for o in layout['furniture']}
    drawer_y=furniture['bedside_drawers']['position'][1]-.4
    drawer_slide=.025+.195*progress(frame,600,660)
    drawer_slide*=1-progress(frame,780,850)
    drawer_hand=(3.5,drawer_y-drawer_slide-.08,.75)
    targets={};phase='bedroom'
    if frame<=888:
        t=progress(frame,270,360)
        root=mix((2.2,10.70,0),(2.85,10.4,0),t)
        up=unit(mix((0,1,0),(0,0,1),t))
        lateral=unit(mix((-1,0,0),(0,-1,0),t));lateral=unit(sub(lateral,mul(up,dot(lateral,up))))
        forward=unit(cross(up,lateral));hip=add(root,(0,0,.665-.015*t+.09*math.sin(math.pi*t)))
        lean=.52*progress(frame,540,580)*(1-progress(frame,850,888))
        if frame>=360:up=unit((math.sin(lean),0,math.cos(lean)));forward=unit(cross(up,lateral))
    elif frame<=1128:
        root=(9.4,9.1,0);forward=(0,1,0);up=(0,0,1);lateral=(1,0,0);hip=add(root,(0,0,1.02));phase='kitchen_overview'
    elif frame<=1368:
        root=(13.325,.75,.16);forward=(0,-1,0);up=unit((0,-.5,1));lateral=(-1,0,0);hip=add(root,(0,0,.94));phase='shower'
    elif frame<=2520:
        root=(10.55,9.2,0);forward=(1,0,0);lateral=(0,-1,0)
        # Lean over the near table edge for grasping, then return upright for carry.
        stand=progress(frame,1410,1460)*(1-progress(frame,1500,1540)) if frame<=1560 else 1 if frame<=2160 else progress(frame,2450,2510)
        lean=.80*(1-stand);up=unit((math.sin(lean),0,math.cos(lean)));hip=add(root,(0,0,.94+.08*stand));phase='table'
    elif frame<=2640:
        root=(.9,10.4,0);forward=(-1,0,0);lateral=(0,1,0);up=(0,0,1);hip=add(root,(0,0,1.02));phase='window'
    else:
        root,forward=travel(frame);lateral=(forward[1],-forward[0],0);up=(0,0,1);hip=add(root,(0,0,1.02));phase='departure'
    chest=add(hip,mul(up,SPINE_LENGTH));head=add(add(chest,mul(up,.25)),mul(forward,.125 if frame<=270 else 0))
    joints={'pelvis':hip,'spine':add(hip,mul(up,SPINE_LENGTH/2)),'chest':chest,'head':head,'up':up,'forward':unit(cross(up,lateral)),'lateral':lateral}
    shoulders={side:add(add(add(chest,mul(up,-.08)),mul(lateral,sign*.225)),mul(forward,.06*(1-progress(frame,270,360)) if frame<=360 else 0)) for side,sign in [('left',-1),('right',1)]}
    rests={side:add(add(add(p,mul(up,-.60)),mul(forward,.10)),mul(lateral,sign*.045)) for (side,p),sign in zip(shoulders.items(),[-1,1])}
    if 540<=frame<=888:
        for hand in ['left','right']:rests[hand]=add(rests[hand],(0,0,.08))
    if 360<=frame<580:
        targets['right']=world(hip,forward,lateral,.19,-.12,.36)
    if 580<=frame<=888:
        waypoint=(3.03,10.93,.77)
        if frame<590:targets['left']=mix(rests['left'],waypoint,progress(frame,580,590))
        elif frame<600:targets['left']=mix(waypoint,drawer_hand,progress(frame,590,600))
        elif frame<850:targets['left']=drawer_hand
        elif frame<870:targets['left']=mix(drawer_hand,waypoint,progress(frame,850,870))
        else:targets['left']=mix(waypoint,rests['left'],progress(frame,870,888))
    shower_contact=add(furniture['rear_wall_taps']['position'],(0,.14,0))
    if 1180<=frame<=1260:targets['right']=mix(rests['right'],shower_contact,progress(frame,1180,1210)*(1-progress(frame,1230,1260)))
    mug_table=(11.24,8.98,.88);envelope_table=(11.20,9.13,.772);letter_table=(11.18,9.42,.772);keys_table=(11.05,9.00,.778)
    mug=mug_table;keys=keys_table;letter=letter_table;envelope=envelope_table
    mug_held=False;keys_held=False;packet_pocket=False
    carry=world(root,forward,lateral,.31,-.28,1.30)
    handle_side=mul(lateral,-.12)
    if 1375<=frame<1400:targets['left']=mix(rests['left'],add(mug_table,add(handle_side,(0,0,.035))),progress(frame,1375,1400))
    if 1400<=frame<1540:
        # One initial lift and an explicit return leave both hands free for paper.
        hold=world(root,forward,lateral,.20,-.28,1.70)
        lift=progress(frame,1400,1460)*(1-progress(frame,1500,1540));mug=mix(mug_table,hold,lift)
        targets['left']=add(mug,add(handle_side,(0,0,.035)));mug_held=True
    if 2161<=frame<2260:
        letter=mix(letter_table,world(root,forward,lateral,.60,0,1.16),progress(frame,2161,2215))
        angle=math.pi*progress(frame,2220,2260)
        targets['left']=add(letter,(-.06,.085*math.cos(angle),.06+.085*math.sin(angle)))
        targets['right']=add(letter,(.06,-.085,.06))
    elif 2260<=frame<2320:
        envelope=mix(envelope_table,world(root,forward,lateral,.60,-.06,1.16),progress(frame,2275,2300))
        insertion_start=world(root,forward,lateral,.60,.04,1.163)
        held=world(root,forward,lateral,.60,0,1.16)
        letter=mix(held,insertion_start,progress(frame,2260,2300)) if frame<2300 else mix(insertion_start,add(envelope,(0,.07425,.003)),progress(frame,2300,2320))
        pickup=add(add(envelope,mul(lateral,-.07)),(0,0,.06))
        held=add(world(root,forward,lateral,.60,.085,1.16),(-.06,0,.06))
        targets['left']=mix(held,pickup,progress(frame,2260,2275)) if frame<2275 else pickup
        targets['right']=add(letter,(.06,-.07425,.06))
    body_forward=unit(cross(up,lateral))
    pocket=add(add(hip,mul(up,.40)),add(mul(body_forward,.08),mul(lateral,.08)))
    if frame>=2320:
        envelope=mix(world(root,forward,lateral,.60,-.06,1.16),pocket,progress(frame,2320,2360))
        letter=add(envelope,(0,0,.003*(1-progress(frame,2320,2360))))
        if frame<2380:targets['right']=add(envelope,mul(forward,.04))
        if frame<2340:targets['left']=mix(add(world(root,forward,lateral,.60,-.13,1.16),(0,0,.06)),rests['left'],progress(frame,2320,2340))
        packet_pocket=frame>=2360
    if frame>=2380:
        keys=mix(keys_table,world(root,forward,lateral,.04,.31,.98),progress(frame,2395,2430));keys_held=frame>=2395
        grip=add(keys,(0,0,.045));start_hand=add(pocket,mul(forward,.04))
        targets['right']=mix(start_hand,grip,progress(frame,2380,2395)) if frame<2395 else grip
    if frame>=2430:
        mug=mix(mug_table,carry,progress(frame,2450,2510));mug_held=frame>=2450
        grip=add(mug,add(handle_side,(0,0,.035)))
        targets['left']=mix(rests['left'],grip,progress(frame,2430,2450)) if frame<2450 else grip
    for side,sign in [('left',-1),('right',1)]:
        wrist=targets.get(side,rests[side])
        try:joints[side+'_arm']=solve_arm(shoulders[side],wrist,up,lateral,sign,.03 if side=='left' and 580<=frame<=888 else .16)
        except ValueError as e:raise ValueError(f'frame {frame} {side}: shoulder={shoulders[side]} wrist={wrist}') from e
        start=add(hip,mul(lateral,sign*.12))
        if frame<=888:
            t=progress(frame,270,360);sleep=(2.2-sign*.12,9.78,.64);seated=(3.38,10.4-sign*.12,.10);ankle=mix(sleep,seated,t)
            if 270<frame<360:ankle=(ankle[0],ankle[1],.64+.18*math.sin(math.pi*t) if t<.8 else .64-.54*progress(t,.8,1))
            pole=add(start,(1,0,.4)) if frame>270 else add(start,(0,-.5,.3))
        else:
            ankle=world(root,forward,lateral,.04,sign*.12,.10)
            if frame>=2641 and frame<3120:
                offset=0 if side=='left' else 10;cycle=math.floor((frame-2641+offset)/20);a=2641+cycle*20-offset;t=(frame-a)/20
                def anchor(f):
                    p,d=travel(max(2641,min(3120,f)));lat=(d[1],-d[0],0);return world(p,d,lat,.04,sign*.12,.10)
                first,last=anchor(a+5),anchor(a+25)
                ankle=first if t<.5 else add(mix(first,last,progress(t,.5,1)),(0,0,.05*math.sin(math.pi*max(0,(t-.5)*2))))
            pole=add(start,mul(forward,1))
        joints[side]=(start,two_segment(start,ankle,pole,THIGH_LENGTH,CALF_LENGTH),ankle)
    return {'frame':frame,'phase':phase,'root':root,'ground_forward':(1,0,0) if frame<=888 else forward,'joints':joints,'drawer_slide':drawer_slide,'shower_on':frame>=1210 and frame<=1320,'shower_cold':frame>=1282,'mug':mug,'handle_side':handle_side,'keys':keys,'letter':letter,'envelope':envelope,'fold':progress(frame,2220,2260),'mug_held':mug_held,'keys_held':keys_held,'packet_pocket':packet_pocket,'packet_basis':(lateral,up,mul(body_forward,-1)),'pocket_rotation':progress(frame,2320,2360),'paper_two_hands':2161<=frame<2320,'shower_contact':shower_contact,'drawer_contact':drawer_hand}


def joint_boxes(s):
    """Exact orthonormal box transforms shared by mesh builder and math checks."""
    j=s['joints'];basis=(j['lateral'],j['forward'],j['up']);out={}
    def segment(name,a,b,width,depth,preferred=None):
        z=unit(sub(b,a));ref=preferred or j['lateral'];x=sub(ref,mul(z,dot(ref,z)))
        if dot(x,x)<1e-8:x=sub((0,0,1),mul(z,z[2]))
        x=unit(x);y=unit(cross(z,x));out[name]={'center':mix(a,b,.5),'size':(width,depth,math.dist(a,b)),'basis':(x,y,z)}
    pelvis_basis=basis if s['frame']<360 else (j['lateral'],s['ground_forward'],(0,0,1))
    out['pelvis']={'center':j['pelvis'],'size':(.36,.22,.18),'basis':pelvis_basis}
    for name,a,b in [('lower_spine',j['pelvis'],j['spine']),('torso',j['spine'],j['chest'])]:out[name]={'center':mix(a,b,.5),'size':(.45,.25,math.dist(a,b)),'basis':basis}
    out['neck']={'center':add(j['chest'],mul(j['up'],.05)),'size':(.12,.12,.10),'basis':basis}
    out['head']={'center':j['head'],'size':(.28,.25,.30),'basis':basis}
    for side in ['left','right']:
        shoulder,elbow,wrist=j[side+'_arm'];hip,knee,ankle=j[side]
        segment(side+'_upper_arm',shoulder,elbow,.14,.14);segment(side+'_forearm',elbow,wrist,.10,.10)
        palm={'center':wrist,'size':(.09,.08,.10),'basis':basis}
        if s['paper_two_hands']:palm={'center':add(wrist,(0,0,-.03)),'size':(.09,.08,.06),'basis':((1,0,0),(0,1,0),(0,0,1))}
        if 580<=s['frame']<=888 and side=='left':
            grip=progress(s['frame'],580,600)*(1-progress(s['frame'],850,888))
            palm={'center':add(wrist,(0,.0075*grip,-.06*grip)),'size':(.09,.08,.10+.02*grip),'basis':((1,0,0),(0,1,0),(0,0,1))}
        if s['phase']=='shower' and side=='right':palm={'center':add(wrist,(0,-.04,0)),'size':(.09,.08,.10),'basis':((1,0,0),(0,1,0),(0,0,1))}
        if side=='right' and s['frame']>=2380:palm={'center':wrist,'size':(.09,.08,.10),'basis':(j['lateral'],s['ground_forward'],(0,0,1))}
        out[side+'_palm']=palm
        segment(side+'_thigh',hip,knee,.18,.18);segment(side+'_calf',knee,ankle,.16,.16)
        if s['frame']<=270:
            foot_basis=((1,0,0),(0,0,-1),(0,1,0));center=add(ankle,(0,-.05,.01))
        elif s['frame']<350:
            t=progress(s['frame'],270,350);up=unit(mix((0,1,0),(0,0,1),t));lat=unit(mix((-1,0,0),(0,-1,0),t));lat=unit(sub(lat,mul(up,dot(lat,up))));forward=unit(cross(up,lat));foot_basis=(lat,forward,up);center=add(add(ankle,mul(forward,.01+.04*t)),mul(up,-.05))
        else:
            f=s['ground_forward'];lat=(f[1],-f[0],0)
            if s['frame']<=888:f=(1,0,0);lat=(0,-1,0)
            foot_basis=(lat,f,(0,0,1));center=add(add(ankle,mul(f,.05)),(0,0,-.05))
        out[side+'_foot']={'center':center,'size':(.18,.22,.10),'basis':foot_basis}
    return out


def box_corners(box):
    corners=[]
    for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]:
        p=box['center']
        for sign,size,axis in zip((x,y,z),box['size'],box['basis']):p=add(p,mul(axis,sign*size/2))
        corners.append(p)
    return corners


def bedside_geometry(layout):
    item=next(o for o in layout['furniture'] if o['id']=='bedside_drawers');x,y,_=item['position'];w,d,h=item['size']
    return [('left',(x-w/2+.02,y,h/2),(.04,d,h)),('right',(x+w/2-.02,y,h/2),(.04,d,h)),('back',(x,y+d/2-.02,h/2),(w-.04,.04,h)),('top',(x,y,h-.02),(w,d,.04)),('base',(x,y,.02),(w-.04,d,.04)),('lower_front',(x,y-d/2+.02,.18),(w-.08,.04,.28))]


def drawer_geometry():
    return [('base',(0,0,.50),(.60,.62,.035)),('front',(0,-.32,.61),(.62,.035,.20)),('handle',(0,-.355,.66),(.18,.035,.035)),('left',(-.285,0,.61),(.03,.62,.20)),('right',(.285,0,.61),(.03,.62,.20))]
