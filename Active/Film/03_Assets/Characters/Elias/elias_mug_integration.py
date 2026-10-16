"""Join tested mug actions to surrounding table motion; room cuts retained."""
from copy import deepcopy
import math,json
from elias_articulation import add,sub,mul,dot,cross,unit,mix
from elias_hand_math import hands
from elias_mug_lifecycle import state as cycle_state,ramp
from elias_mug_contact import state as held_state
from sc001_room_performance import state as source_state,solve_arm
_CACHE={}
WINDOWS=[('first_approach',1369,1400),('release_to_rest',1540,1600),('second_approach',2400,2450),('carry_join',2490,2520)]

def baseline(frame,layout):
    s=deepcopy(source_state(frame,layout))
    # One left-wrist origin convention throughout the integrated rig avoids a
    # forearm roll convention changing at a patch boundary.
    s['_mug_basis']=((0,-1,0),(1,0,0),(0,0,1))
    s['_mug_contact_metrics']={'frame':frame,'phase':'surrounding_motion_no_grasp_claim'}
    s['_hand_plan']=hands(s);s['_hand_origins']={'left':s['joints']['left_arm'][-1]}
    return s


def blend_hand(s,target,amount):
    a=s['_hand_plan']['left'];b=target['_hand_plan']['left']
    x=unit(mix(a['palm']['basis'][0],b['palm']['basis'][0],amount))
    y=mix(a['palm']['basis'][1],b['palm']['basis'][1],amount);y=unit(sub(y,mul(x,dot(x,y))));z=unit(cross(x,y))
    chains={}
    for digit,ap in a['chains'].items():
        bp=b['chains'][digit];points=[mix(ap[0],bp[0],amount)]
        for a0,a1,b0,b1 in zip(ap,ap[1:],bp,bp[1:]):
            direction=unit(mix(unit(sub(a1,a0)),unit(sub(b1,b0)),amount))
            points.append(add(points[-1],mul(direction,math.dist(a0,a1))))
        chains[digit]=points
    palm={'center':mix(a['palm']['center'],b['palm']['center'],amount),'size':a['palm']['size'],'basis':(x,y,z)}
    a['chains']=chains;a['palm']=palm
    wrist=mix(s['_hand_origins']['left'],target['_hand_origins']['left'],amount)
    j=s['joints'];j['left_arm']=solve_arm(j['left_arm'][0],wrist,j['up'],j['lateral'],-1,.16+.19*amount)
    s['_hand_origins']['left']=wrist
    return s


def state(frame,layout):
    key=(frame,json.dumps(layout,sort_keys=True))
    if key in _CACHE:return deepcopy(_CACHE[key])
    if 1387<=frame<=1560 or 2430<=frame<=2510:s=cycle_state(frame,layout)
    elif 2511<=frame<=3168:s=held_state(frame,layout)
    else:
        s=baseline(frame,layout)
        if 1369<=frame<1387:
            s['_hand_plan']['left']=deepcopy(baseline(1369,layout)['_hand_plan']['left'])
            s=blend_hand(s,cycle_state(1387,layout),ramp(frame,1369,1387))
        elif 1560<frame<1600:
            t=ramp(frame,1560,1600)
            # Replay the existing smooth table rise as kinematics only. Props
            # retain actual source time; this removes the source1561 stand pop.
            body=source_state(1410+50*t,layout)
            s['joints']=deepcopy(body['joints'])
            j=s['joints'];shoulder=j['left_arm'][0]
            rest=add(add(add(shoulder,mul(j['up'],-.60)),mul(s['ground_forward'],.10)),mul(j['lateral'],-.045))
            j['left_arm']=solve_arm(shoulder,rest,j['up'],j['lateral'],-1,.16)
            s.pop('_hand_plan',None)
            s['_mug_basis']=((0,-1,0),(1,0,0),(0,0,1))
            s['_mug_contact_metrics']={'frame':frame,'phase':'surrounding_motion_no_grasp_claim'}
            s['_hand_plan']=hands(s);s['_hand_origins']={'left':s['joints']['left_arm'][-1]}
            s=blend_hand(s,cycle_state(1560,layout),1-t)
        elif 2400<=frame<2430:
            s=blend_hand(s,cycle_state(2430,layout),ramp(frame,2400,2430))
    s['_palm_controls']=('left',)
    _CACHE[key]=deepcopy(s)
    return s
