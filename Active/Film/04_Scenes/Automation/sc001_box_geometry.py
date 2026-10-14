"""Oriented-box intersection, with touching surfaces treated as contact."""
from elias_articulation import cross,dot,unit


def bounds(points):return tuple((min(p[k] for p in points),max(p[k] for p in points)) for k in range(3))


def intersects(a,axes_a,b,axes_b,tolerance=1e-5):
    ba,bb=bounds(a),bounds(b)
    if any(min(ba[k][1],bb[k][1])-max(ba[k][0],bb[k][0])<=tolerance for k in range(3)):return False
    axes=list(axes_a)+list(axes_b)+[cross(x,y) for x in axes_a for y in axes_b]
    for axis in axes:
        if dot(axis,axis)<1e-12:continue
        axis=unit(axis);pa=[dot(p,axis) for p in a];pb=[dot(p,axis) for p in b]
        if min(max(pa),max(pb))-max(min(pa),min(pb))<=tolerance:return False
    return True
