"""Bounded approach/grasp/release around the passed mug-motion interval."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,dot,cross,unit
from elias_mug_contact import state as held_state,rail_gap
from sc001_room_performance import solve_arm

START=1375
END=1560
BODY_DEPTH=.20
BODY_CENTER_Z=-.01
_CACHE={}

def ramp(frame,a,b):
    t=max(0,min(1,(frame-a)/(b-a)))
    return t*t*(3-2*t)


def state(frame,layout):
    key=(frame,json.dumps(layout,sort_keys=True))
    if key in _CACHE:return deepcopy(_CACHE[key])
    s=deepcopy(held_state(frame,layout))
    if frame==889 or 1400<=frame<=1539 or 2450<=frame<=2510:return s
    if not (1375<=frame<=1560 or 2430<=frame<2450):return s
    lat,along,up=s['_mug_basis'];hand=s['_hand_plan']['left']
    second=2430<=frame<2450
    approach=frame<1400 or second
    if second:
        grip=ramp(frame,2438,2450);away=1-ramp(frame,2430,2440)
    else:
        grip=ramp(frame,1387,1400) if approach else 1-ramp(frame,1540,1550)
        away=(1-ramp(frame,1375,1390)) if approach else ramp(frame,1550,1560)
    offset=add(mul(lat,-.09*away),mul(along,-.025*away))
    # Rotate digit fans out of the loop, preserving every segment length.
    # Opposite thumb sweep opens the opposed anchor rather than crossing it.
    angle=math.radians(70)*(1-grip)
    chains={}
    for digit,points in hand['chains'].items():
        theta=-angle*.45 if digit=='thumb' else angle
        axis=up;origin=points[0]
        def transform(point):
            v=sub(point,origin)
            rotated=add(add(mul(v,math.cos(theta)),mul(cross(axis,v),math.sin(theta))),mul(axis,dot(axis,v)*(1-math.cos(theta))))
            pitch=.55*math.sin(angle) if digit in ('ring','little') else 0
            rotated=add(add(mul(rotated,math.cos(pitch)),mul(cross(along,rotated),math.sin(pitch))),mul(along,dot(along,rotated)*(1-math.cos(pitch))))
            return add(add(origin,rotated),offset)
        chains[digit]=[transform(p) for p in points]
    hand['chains']=chains;hand['palm']['center']=add(hand['palm']['center'],offset)
    wrist=add(s['_hand_origins']['left'],offset);shoulder=s['joints']['left_arm'][0]
    s['joints']['left_arm']=solve_arm(shoulder,wrist,s['joints']['up'],lat,-1,.35)
    s['_hand_origins']['left']=wrist
    def local(point):
        delta=sub(point,s['mug']);return (dot(delta,lat),dot(delta,along),dot(delta,up))
    gaps={digit:rail_gap(points,local) for digit,points in chains.items()}
    assert min(gaps.values())>=.0005,('Lifecycle handle overlap',frame,gaps)
    angle_wrist=math.degrees(math.acos(max(-1,min(1,dot(unit(sub(wrist,s['joints']['left_arm'][1])),along)))))
    assert angle_wrist<65,('Lifecycle wrist bend',frame,angle_wrist)
    s['_mug_contact_metrics'].update(wrist_axis_angle_degrees=angle_wrist)
    s['_mug_lifecycle']={'phase':'second_approach_and_form_grip' if second else 'approach_and_form_grip' if approach else 'place_open_withdraw',
        'grip_amount':grip,'withdrawal_fraction':away,'sampled_digit_rail_gaps_metres':gaps}
    _CACHE[key]=deepcopy(s)
    return s
