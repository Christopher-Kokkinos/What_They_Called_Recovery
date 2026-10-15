"""Isolated connected-wrist mug experiment; no source choreography mutation."""
from copy import deepcopy
import math
from elias_articulation import add,sub,mul,unit,dot,cross
from elias_hand_math import hands
from sc001_room_performance import state as source_state,solve_arm
FRAMES=[1400,1411,1460,1500,2450,2510]


def state(frame,layout):
    # Shared constructor requests 889 as rest; choose a mug hold rest pose.
    frame=1460 if frame==889 else frame
    s=deepcopy(source_state(frame,layout));plan=hands(s);hand=plan['left'];palm=hand['palm'];center=palm['center']
    shoulder,elbow,old_wrist=s['joints']['left_arm'];axis=unit(sub(center,elbow))
    for _ in range(40):
        wrist=sub(center,mul(axis,.055))
        chain=solve_arm(shoulder,wrist,s['joints']['up'],s['joints']['lateral'],-1)
        next_axis=unit(sub(wrist,chain[1]))
        if math.dist(axis,next_axis)<1e-10:axis=next_axis;break
        axis=next_axis
    wrist=sub(center,mul(axis,.055));chain=solve_arm(shoulder,wrist,s['joints']['up'],s['joints']['lateral'],-1)
    forearm_axis=unit(sub(wrist,chain[1]));angle=math.degrees(math.acos(max(-1,min(1,dot(axis,forearm_axis)))))
    assert angle<.1,('Wrist alignment did not converge',frame,angle)
    # Palm length points along the distal forearm; curl plane faces the mug.
    toward=sub(s['mug'],center);bend=sub(toward,mul(axis,dot(toward,axis)))
    if dot(bend,bend)<1e-10:bend=s['joints']['lateral']
    y=unit(bend);z=mul(axis,-1);x=unit(cross(y,z));basis=(x,y,z);old_basis=palm['basis']
    def transform(point):
        delta=sub(point,center);return add(center,add(add(mul(x,dot(delta,old_basis[0])),mul(y,dot(delta,old_basis[1]))),mul(z,dot(delta,old_basis[2]))))
    hand['chains']={name:[transform(point) for point in points] for name,points in hand['chains'].items()}
    hand['palm']={**palm,'basis':basis};s['joints']['left_arm']=chain;s['_hand_plan']=plan;s['_hand_origins']={'left':wrist}
    s['_mug_contact_metrics']={'frame':frame,'wrist_axis_angle_degrees':angle,'palm_offset_metres':math.dist(wrist,center),'source_wrist_adjustment_metres':math.dist(wrist,old_wrist)}
    return s
