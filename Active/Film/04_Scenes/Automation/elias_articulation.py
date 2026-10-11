"""Reusable fixed-length diagnostic joints. No Blender dependency or final acting claim."""
import math

THIGH_LENGTH = .50
CALF_LENGTH = .52
SPINE_LENGTH = .65
UPPER_ARM_LENGTH = .36
FOREARM_LENGTH = .34
STANDING_HIP_HEIGHT = 1.02
SEATED_HIP_HEIGHT = .85
ANKLE_HEIGHT = .10


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mix(a,b,t):return add(mul(a,1-t),mul(b,t))
def unit(a):
    n=math.sqrt(dot(a,a))
    if n<1e-10: raise ValueError('Degenerate joint direction')
    return mul(a,1/n)


def two_segment(start,end,pole,first,second):
    """Analytic knee/elbow solve with explicit reachable-target failure."""
    delta=sub(end,start);distance=math.sqrt(dot(delta,delta))
    if not abs(first-second)+1e-8<distance<first+second-1e-8:
        raise ValueError('Unreachable joint target: '+str(distance))
    direction=unit(delta);hint=sub(pole,start)
    normal=unit(sub(hint,mul(direction,dot(hint,direction))))
    along=(first*first-second*second+distance*distance)/(2*distance)
    return add(add(start,mul(direction,along)),mul(normal,math.sqrt(max(0,first*first-along*along))))


def opening_joints(frame,root_position,lean):
    """World-space opening joints; fixed seated ankle targets survive the hip scoot.

    Supine-to-seated is a diagnostic staged rise, not a physiological roll.
    Foot descent finishes at frame 350; late seated feet stay planted.
    """
    t=max(0,min(1,(frame-270)/80));smooth=t*t*(3-2*t)
    hip=(2+.5*smooth,5.9-.1*smooth,SEATED_HIP_HEIGHT)
    if frame>=350:hip=(root_position[0],root_position[1],root_position[2]+.75)
    rise=math.pi/2*smooth
    direction=unit((math.sin(lean),math.cos(rise)*math.cos(lean),math.sin(rise)*math.cos(lean)))
    # Split spine supplies a joint for later chest/neck acting without stretching.
    middle=add(hip,mul(direction,SPINE_LENGTH/2))
    chest=add(hip,mul(direction,SPINE_LENGTH))
    head=add(chest,mul(direction,.25))
    yaw=math.pi/2*smooth;lateral=(math.cos(yaw),math.sin(yaw),0)
    lateral=unit(sub(lateral,mul(direction,dot(lateral,direction))))
    forward=unit(cross(lateral,direction))
    joints={'pelvis':hip,'spine':middle,'chest':chest,'head':head,
            'up':direction,'lateral':lateral,'forward':forward}
    # Every opening arm uses the same chest basis as the spine and head.
    for side,sign in [('left',-1),('right',1)]:
        shoulder=add(add(chest,mul(direction,-.08)),mul(lateral,sign*.225))
        rest=add(add(add(shoulder,mul(direction,-.60)),mul(forward,.13)),mul(lateral,sign*.04))
        wrist=rest
        if side=='right':
            rib=add(add(add(hip,mul(direction,.40)),mul(lateral,-.16)),mul(forward,.19))
            support=max(0,min(1,(frame-300)/50))
            wrist=mix(rest,rib,support)
            if 750<=frame<=810:
                wrist=mix(rib,(3.22,5.80,.72),((frame-750)/60)**2)
            elif 810<frame<=870:
                wrist=(3.22,5.80+(frame-810)/60*.48,.72)
            elif frame>870:
                wrist=mix((3.22,6.28,.72),rest,(frame-870)/18)
            joints['rib_target']=rib
        pole=add(add(shoulder,mul(forward,.7)),mul(lateral,sign*.4))
        elbow=two_segment(shoulder,wrist,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH)
        joints[side+'_arm']=(shoulder,elbow,wrist)
    for side,sign in [('left',-1),('right',1)]:
        start=add(hip,mul(lateral,sign*.12))
        sleep=(2+sign*.12,5.00,SEATED_HIP_HEIGHT)
        seated=(3.05,5.80+sign*.12,ANKLE_HEIGHT)
        ankle=add(mul(sleep,1-smooth),mul(seated,smooth))
        pole=add(hip,(1.5,-1,1))
        knee=two_segment(start,ankle,pole,THIGH_LENGTH,CALF_LENGTH)
        joints[side]=(start,knee,ankle)
    return joints
