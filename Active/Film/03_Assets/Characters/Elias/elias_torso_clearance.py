"""Analytic central-torso proxy gate; not a final skin collision solver.

Body-local elliptical core has half-width170mm and half-depth90mm, expanded
by35mm for a limb envelope. Only heights120–520mm above pelvis are tested;
shoulder attachments and lower-body contacts are outside this bounded gate.
"""
from elias_articulation import sub,dot
WIDTH,DEPTH,LOW,HIGH=.205,.125,.12,.52

def local(j,p):
    d=sub(p,j['pelvis']);return (-dot(d,j['lateral']),dot(d,j['up']),dot(d,j['forward']))

def segment_clearance(j,a,b):
    """Exact minimum ellipse score over the segment clipped to torso height."""
    a=local(j,a);b=local(j,b);d=tuple(y-x for x,y in zip(a,b));lo,hi=0.,1.
    if abs(d[1])<1e-12:
        if not LOW<=a[1]<=HIGH:return float('inf')
    else:
        t0,t1=sorted(((LOW-a[1])/d[1],(HIGH-a[1])/d[1]));lo=max(lo,t0);hi=min(hi,t1)
        if lo>hi:return float('inf')
    x,z=a[0]/WIDTH,a[2]/DEPTH;dx,dz=d[0]/WIDTH,d[2]/DEPTH
    t=max(lo,min(hi,-(x*dx+z*dz)/(dx*dx+dz*dz))) if dx*dx+dz*dz>1e-15 else lo
    return (x+dx*t)**2+(z+dz*t)**2

def left_arm_clearance(j,arm=None):
    sh,e,w=j['left_arm'] if arm is None else arm
    return min(segment_clearance(j,sh,e),segment_clearance(j,e,w))


def validate_left_support(j,arm=None):
    arm=j['left_arm'] if arm is None else arm
    score=left_arm_clearance(j,arm);elbow=local(j,arm[1])
    assert score>=1-1e-6,('Left arm intersects expanded torso core',score)
    assert elbow[0]>=.20 and elbow[2]>=-.02,('Left support elbow behind/across torso',elbow)
    return score
