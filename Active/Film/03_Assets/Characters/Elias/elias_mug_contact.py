"""Isolated connected-wrist mug experiment; no source choreography mutation."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,unit,dot,cross,two_segment
from elias_hand_math import hands
from sc001_room_performance import state as source_state,solve_arm
_CACHE={}
FRAMES=[1400,1411,1460,1500,2450,2510]


def state(frame,layout):
    # Shared constructor requests 889 as rest; choose a mug hold rest pose.
    frame=1460 if frame==889 else frame
    cache_key=(frame,json.dumps(layout,sort_keys=True))
    if cache_key in _CACHE:return deepcopy(_CACHE[cache_key])
    s=deepcopy(source_state(frame,layout));plan=hands(s);hand=plan['left'];palm=hand['palm'];old_center=palm['center'];center=old_center;palm={**palm,'center':center}
    shoulder,elbow,old_wrist=s['joints']['left_arm'];axis=unit(sub(center,elbow))
    for _ in range(120):
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
        delta=sub(point,old_center);return add(center,add(add(mul(x,dot(delta,old_basis[0])),mul(y,dot(delta,old_basis[1]))),mul(z,dot(delta,old_basis[2]))))
    hand['chains']={name:[transform(point) for point in points] for name,points in hand['chains'].items()}
    # Wrap around the existing boxout handle's outer rail. Frame targets
    # in mug coordinates, not world coordinates or generic finger curls.
    lateral=s['joints']['lateral'];forward=s['ground_forward'];mug=s['mug'];residuals={}
    for i,digit in enumerate(['index','middle','ring','little','thumb']):
        points=hand['chains'][digit];base=points[0];lengths=[math.dist(a,b) for a,b in zip(points,points[1:])]
        # Opposed thumb across the handle depth; fingers along rail height.
        height=max(-.05,min(.05,base[2]-mug[2]))
        target=add(add(mug,mul(lateral,-.105)),add(mul(forward,.024 if digit!='thumb' else -.018),(0,0,height)))
        if digit!='thumb':
            candidates=[]
            for degrees in range(0,360,10):
                theta=math.radians(degrees);u=add(mul(forward,math.cos(theta)),mul(lateral,math.sin(theta)));v=add(mul(forward,-math.sin(theta)),mul(lateral,math.cos(theta)))
                joints=[base]
                for direction,length in zip((u,v,mul(u,-1)),lengths):joints.append(add(joints[-1],mul(direction,length)))
                gaps=[]
                for start,end in zip(joints,joints[1:]):
                    for k in range(9):
                        point=add(start,mul(sub(end,start),k/8));relative=sub(point,mug)
                        local=(dot(relative,lateral)+.12,dot(relative,forward),relative[2]);half=(.0125,.015,.07)
                        outside=[abs(q)-h for q,h in zip(local,half)]
                        signed=math.sqrt(sum(max(0,q)**2 for q in outside))+min(0,max(outside))
                        gaps.append(signed-.008)
                gap=min(gaps);score=1000*max(0,-gap)+abs(gap)+.2*math.dist(joints[-1],target)
                candidates.append((score,joints,gap,degrees))
            _,joints,gap,degrees=min(candidates,key=lambda q:q[0]);hand['chains'][digit]=joints
            residuals[digit]={'target_distance_metres':math.dist(joints[-1],target),'sampled_rail_clearance_metres':gap,'bend_degrees':[90,90],'orientation_degrees':degrees}
            continue
        delta=sub(target,base);distance=math.sqrt(dot(delta,delta));hi=sum(lengths)-1e-5
        reached=add(base,mul(unit(delta),hi)) if distance>hi else target
        pole=add(base,add(mul(forward,.06 if digit!='thumb' else -.06),mul(axis,.025)))
        distance=math.dist(base,reached)
        equal_reach_angle=math.degrees(math.acos(max(-1,min(1,(lengths[0]**2-lengths[1]**2-lengths[2]**2)/(2*lengths[1]*lengths[2])))))
        for bend_degrees in (65,90,120,30,150,equal_reach_angle,0):
            distal=min(sum(lengths[1:])-2e-6,math.sqrt(lengths[1]**2+lengths[2]**2+2*lengths[1]*lengths[2]*math.cos(math.radians(bend_degrees))))
            if abs(lengths[0]-distal)+1e-7<distance<lengths[0]+distal-1e-7:break
        else:raise ValueError(('No fixed-length finger bend reaches handle',frame,digit,distance))
        joint=two_segment(base,reached,pole,lengths[0],distal)
        last=two_segment(joint,reached,pole,lengths[1],lengths[2])
        hand['chains'][digit]=[base,joint,last,reached];residuals[digit]=math.dist(reached,target)
    hand['palm']={**palm,'basis':basis};s['joints']['left_arm']=chain;s['_hand_plan']=plan;s['_hand_origins']={'left':wrist}
    s['_mug_contact_metrics']={'frame':frame,'wrist_axis_angle_degrees':angle,'palm_offset_metres':math.dist(wrist,center),'source_wrist_adjustment_metres':math.dist(wrist,old_wrist),'handle_target_residuals_metres':residuals}
    _CACHE[cache_key]=deepcopy(s)
    return s
