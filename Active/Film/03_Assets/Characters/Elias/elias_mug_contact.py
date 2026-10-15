"""Isolated mug-local shared grip; source position/timing retained."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,unit,dot,cross,two_segment
from elias_hand_math import hands
from sc001_room_performance import state as source_state,solve_arm
FRAMES=[1400,1411,1460,1500,2450,2510]
_CACHE={}
# Shared by the pose checks and isolated Blender prop update (metres).
HANDLE=[('outer',(-.105,0,.0135),(.012,.018,.051),0),
        ('top',(-.081,0,.033),(.060,.018,.012),0),
        ('bottom',(-.081,0,-.0225),(math.hypot(.048,.021),.018,.012),math.atan2(.021,.048))]
FINGER_RADIUS=.008

def rail_gap(points,world_to_local):
    gap=1e9
    for a,b in zip(points,points[1:]):
        for k in range(65):
            local=world_to_local(add(a,mul(sub(b,a),k/64)))
            for _,center,size,angle in HANDLE:
                delta=sub(local,center)
                # Inverse of the same local Y rotation used by Blender.
                rotated=(math.cos(angle)*delta[0]-math.sin(angle)*delta[2],delta[1],math.sin(angle)*delta[0]+math.cos(angle)*delta[2])
                d=[abs(q)-h/2 for q,h in zip(rotated,size)]
                signed=math.sqrt(sum(max(0,q)**2 for q in d))+min(0,max(d))
                gap=min(gap,signed-FINGER_RADIUS)
    return gap


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
    # Palm faces the handle; contacts now have distinct roles rather than
    # making all four digits share a decorative polygon.
    center=world(-.153,-.018,-.017);axis=along
    wrist=sub(center,mul(axis,.055));shoulder,old_elbow,old_wrist=s['joints']['left_arm']
    chain=solve_arm(shoulder,wrist,s['joints']['up'],lat,-1,.35)
    wrist_angle=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(wrist,chain[1])),axis)))))
    assert wrist_angle<65,('Excessive experimental wrist angle',frame,wrist_angle)
    basis=(mul(up,-1),lat,mul(along,-1));chains={};metrics={}
    def local(point):
        delta=sub(point,mug);return (dot(delta,lat),dot(delta,along),dot(delta,up))
    for i,digit in enumerate(('index','middle','ring','little')):
        length=[.065,.072,.068,.055][i];lengths=[length*.42,length*.33,length*.25]
        inserted=i<2;height=[.016,-.003,-.048,-.067][i]
        first=world(-.105,.026,height)
        proximal=lat if inserted else unit(add(lat,mul(up,-.65)))
        base=sub(first,mul(proximal,lengths[0]))
        middle=unit(add(mul(lat,.88),mul(along,-.475)))
        crease=add(first,mul(middle,lengths[1]))
        tip=add(crease,mul(along,-lengths[2]))
        points=[base,first,crease,tip];chains[digit]=points
        gap=rail_gap(points,local)
        assert gap>=.0005,('Planned finger/rail overlap',frame,digit,gap)
        metrics[digit]={'role':'loop_insert' if inserted else 'under_handle_support',
            'sampled_handle_clearance_metres':gap,'crease_local':local(crease),
            'tip_local':local(tip),'proximal_end_local':local(first)}
    thumb_base=world(-.151,-.018,.025);thumb_tip=world(-.101,0,.048)
    pole=world(-.14,-.045,.075);lengths=[.025,.023,.020];distal=.038
    joint=two_segment(thumb_base,thumb_tip,pole,lengths[0],distal)
    last=two_segment(joint,thumb_tip,pole,lengths[1],lengths[2]);chains['thumb']=[thumb_base,joint,last,thumb_tip]
    thumb_gap=rail_gap(chains['thumb'],local)
    assert thumb_gap>=.0005,('Thumb/rail overlap',frame,thumb_gap)
    # Conservative palm/body bound: cylinder body radius60 mm; half palm width13 mm.
    palm_gap=-local(center)[0]-.013-.060
    assert palm_gap>.015,'Palm touches mug body'
    hand['chains']=chains;hand['palm']={'center':center,'size':(.075,.026,.075),'basis':basis}
    s['joints']['left_arm']=chain;s['_hand_plan']=plan;s['_hand_origins']={'left':wrist};s['_mug_basis']=(lat,along,up)
    s['_mug_contact_metrics']={'frame':frame,'wrist_axis_angle_degrees':wrist_angle,'palm_offset_metres':math.dist(wrist,center),'source_wrist_adjustment_metres':math.dist(wrist,old_wrist),'grip_model':'two_inside_two_under_thumb_on_top','palm_body_gap_metres':palm_gap,'thumb_handle_clearance_metres':thumb_gap,'mug_tilt_degrees':math.degrees(tilt),'finger_clearance':metrics,'thumb_contact_status':'top_anchor_nominal_clearance_checked_skin_pending'}
    _CACHE[key]=deepcopy(s)
    return s
