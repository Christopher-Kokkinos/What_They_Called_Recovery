"""Reusable fixed-length diagnostic joints. No Blender dependency or final acting claim."""
import math

THIGH_LENGTH = .60
CALF_LENGTH = .64
SPINE_LENGTH = .65


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
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
    hip=(2+.5*smooth,5.9-.1*smooth,.85)
    if frame>=350:hip=(root_position[0],root_position[1],root_position[2]+.75)
    rise=math.pi/2*smooth
    direction=unit((math.sin(lean),math.cos(rise)*math.cos(lean),math.sin(rise)*math.cos(lean)))
    # Split spine supplies a joint for later chest/neck acting without stretching.
    middle=add(hip,mul(direction,SPINE_LENGTH/2))
    chest=add(hip,mul(direction,SPINE_LENGTH))
    head=add(chest,mul(direction,.25))
    yaw=math.pi/2*smooth;lateral=(math.cos(yaw),math.sin(yaw),0)
    joints={'pelvis':hip,'spine':middle,'chest':chest,'head':head}
    for side,sign in [('left',-1),('right',1)]:
        start=add(hip,mul(lateral,sign*.12))
        sleep=(2+sign*.12,4.70,.85)
        seated=(3.05,5.80+sign*.12,.10)
        ankle=add(mul(sleep,1-smooth),mul(seated,smooth))
        pole=add(hip,(1.5,-1,1))
        knee=two_segment(start,ankle,pole,THIGH_LENGTH,CALF_LENGTH)
        joints[side]=(start,knee,ankle)
    return joints
