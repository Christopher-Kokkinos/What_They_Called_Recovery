"""Isolated mug-local shared grip; source position/timing retained."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,unit,dot,cross,two_segment
from elias_hand_math import hands
from sc001_room_performance import state as source_state,solve_arm
FRAMES=[1400,1411,1460,1500,2450,2510]
_CACHE={}


def state(frame,layout):
    frame=1460 if frame==889 else frame
    key=(frame,json.dumps(layout,sort_keys=True))
    if key in _CACHE:return deepcopy(_CACHE[key])
    s=deepcopy(source_state(frame,layout));plan=hands(s);hand=plan['left'];mug=s['mug'];lat=s['joints']['lateral'];forward=s['ground_forward']
    # Tilt the mug and its grip together during the first drink, avoiding an
    # upright handle demanding an approximately right-angle wrist extension.
    lift=max(0,min(1,(frame-1400)/60))*(1-max(0,min(1,(frame-1500)/40))) if frame<1540 else 0
    tilt=math.radians(45)*lift
    along=add(mul(forward,math.cos(tilt)),(0,0,math.sin(tilt)))
    up=add(mul(forward,-math.sin(tilt)),(0,0,math.cos(tilt)))
    def world(x,y,z):return add(mug,add(add(mul(lat,x),mul(along,y)),mul(up,z)))
    diagonal=math.radians(-30);stand_off=.0345
    grip_lat=add(mul(lat,math.cos(diagonal)),mul(along,math.sin(diagonal)))
    grip_along=add(mul(lat,-math.sin(diagonal)),mul(along,math.cos(diagonal)))
    def grip_world(x,y,z):
        dx=x+.12
        return world(-.12+dx*math.cos(diagonal)-y*math.sin(diagonal)-stand_off,dx*math.sin(diagonal)+y*math.cos(diagonal),z)
    center=grip_world(-.150,-.015,.005);axis=grip_along;wrist=sub(center,mul(axis,.055));shoulder,old_elbow,old_wrist=s['joints']['left_arm']
    chain=solve_arm(shoulder,wrist,s['joints']['up'],lat,-1,.35)
    wrist_angle=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(wrist,chain[1])),axis)))))
    assert wrist_angle<65,('Excessive experimental wrist angle',frame,wrist_angle)
    basis=(mul(up,-1),grip_lat,mul(grip_along,-1));chains={};metrics={}
    for i,digit in enumerate(('index','middle','ring','little')):
        length=[.065,.072,.068,.055][i];lengths=[length*.42,length*.33,length*.25]
        height=.005-(i-1.5)*.019
        # Common grip plane and direction: around outer/front rail corner.
        # Pads stop 1 mm outside nominal handle faces after 8 mm skin radius.
        base=grip_world(-.1415,.024+lengths[2]-lengths[0],height);points=[base]
        for direction,segment_length in zip((grip_along,grip_lat,mul(grip_along,-1)),lengths):points.append(add(points[-1],mul(direction,segment_length)))
        chains[digit]=points;gap=1e9
        for a,b in zip(points,points[1:]):
            for k in range(33):
                point=add(a,mul(sub(b,a),k/32));delta=sub(point,mug);local=(dot(delta,lat),dot(delta,along),dot(delta,up))
                for rail_center,half in [((-.12,0,0),(.0125,.015,.07)),((-.09,0,.065),(.04,.015,.0125)),((-.09,0,-.065),(.04,.015,.0125))]:
                    d=[abs(q-c)-h for q,c,h in zip(local,rail_center,half)]
                    signed=math.sqrt(sum(max(0,q)**2 for q in d))+min(0,max(d));gap=min(gap,signed-.008)
        assert gap>=.0009,('Planned finger/rail overlap',frame,digit,gap)
        metrics[digit]={'bend_degrees':[90,90],'sampled_handle_clearance_metres':gap,'grip_height_metres':height}
    thumb_base=grip_world(-.150,-.015,.036);thumb_tip=world(-.1425,-.026,.040);pole=grip_world(-.18,-.065,.06)
    lengths=[.025,.023,.020];distal=.030
    joint=two_segment(thumb_base,thumb_tip,pole,lengths[0],distal)
    last=two_segment(joint,thumb_tip,pole,lengths[1],lengths[2]);chains['thumb']=[thumb_base,joint,last,thumb_tip]
    hand['chains']=chains;hand['palm']={'center':center,'size':(.075,.026,.075),'basis':basis}
    s['joints']['left_arm']=chain;s['_hand_plan']=plan;s['_hand_origins']={'left':wrist};s['_mug_basis']=(lat,along,up)
    s['_mug_contact_metrics']={'frame':frame,'wrist_axis_angle_degrees':wrist_angle,'palm_offset_metres':math.dist(wrist,center),'source_wrist_adjustment_metres':math.dist(wrist,old_wrist),'grip_diagonal_degrees':-30,'grip_outward_shift_metres':stand_off,'mug_tilt_degrees':math.degrees(tilt),'finger_clearance':metrics,'thumb_contact_status':'opposed_target_only_skin_clearance_pending'}
    _CACHE[key]=deepcopy(s)
    return s
