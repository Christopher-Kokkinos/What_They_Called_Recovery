"""Provisional raised-table variant; existing integrated take remains reproducible."""
from copy import deepcopy
import math
from elias_articulation import add,sub,mul,unit,cross,two_segment,SPINE_LENGTH,THIGH_LENGTH,CALF_LENGTH
from elias_mug_integration import state as integrated
from sc001_room_performance import solve_arm,progress
TABLE_TOP=.97
TABLE_RISE=.20
MUG_RISE=.18  # original180 mm body: .88 + .18 - .09 == .97
WINDOWS=[('first_table_reach',1369,1600),('second_table_reach',2400,2520)]

def offsets(frame):
    lift=progress(frame,1400,1460)*(1-progress(frame,1500,1540)) if frame<1540 else progress(frame,2450,2510) if frame>=2430 else 0
    return {'mug':MUG_RISE*(1-lift),'letter':TABLE_RISE*(1-progress(frame,2161,2215)),
            'envelope':TABLE_RISE*(1-progress(frame,2275,2300)), 'keys':TABLE_RISE*(1-progress(frame,2395,2430))}

def state(frame,layout):
    s=deepcopy(integrated(frame,layout));delta=offsets(frame)
    for name,dz in delta.items():s[name]=add(s[name],(0,0,dz))
    if not any(a<=frame<=b for _,a,b in WINDOWS):return s
    j=s['joints'];old=deepcopy(j);lat=j['lateral'];forward=s['ground_forward']
    # Keep the accepted drink/carry endpoints; reduce table lean from .80 to .20rad.
    lean=math.atan2(old['up'][0],old['up'][2])*.25
    up=unit((math.sin(lean),0,math.cos(lean)))
    s['root']=add(s['root'],(.22,0,0))
    j['up']=up;j['forward']=unit(cross(up,lat));j['pelvis']=add(s['root'],(0,0,1.02))
    j['spine']=add(j['pelvis'],mul(up,SPINE_LENGTH/2));j['chest']=add(j['pelvis'],mul(up,SPINE_LENGTH));j['head']=add(j['chest'],mul(up,.25))
    for side,sign in [('left',-1),('right',1)]:
        shoulder=add(add(j['chest'],mul(up,-.08)),mul(lat,sign*.225))
        old_shoulder,_,old_wrist=old[side+'_arm'];shift=sub(shoulder,old_shoulder)
        if side=='left' and (1369<=frame<=1600 or 2400<=frame<=2520):
            weight=progress(frame,1369,1400) if frame<1400 else 1-progress(frame,1560,1600) if frame>1560 and frame<=1600 else progress(frame,2400,2430) if frame>=2400 and frame<2430 else 1
            shift=add(mul(shift,1-weight),(0,0,delta['mug']*weight))
        elif s['paper_two_hands']:
            dz=delta['letter'] if side=='right' or frame<2260 else delta['envelope'];shift=(0,0,dz)
        elif side=='right' and frame>=2380:shift=(0,0,delta['keys'])
        wrist=add(old_wrist,shift)
        j[side+'_arm']=solve_arm(shoulder,wrist,up,lat,sign,.35 if side=='left' else .16)
        hand=s['_hand_plan'][side]
        hand['palm']['center']=add(hand['palm']['center'],shift)
        hand['chains']={digit:[add(p,shift) for p in points] for digit,points in hand['chains'].items()}
        if side in s['_hand_origins']:s['_hand_origins'][side]=add(s['_hand_origins'][side],shift)
        hip=add(j['pelvis'],mul(lat,sign*.12));ankle=add(old[side][-1],(.22,0,0))
        j[side]=(hip,two_segment(hip,ankle,add(hip,forward),THIGH_LENGTH,CALF_LENGTH),ankle)
    s['_table_reach_trial']={'table_top':TABLE_TOP,'lean_radians':lean,'offsets':delta}
    return s
