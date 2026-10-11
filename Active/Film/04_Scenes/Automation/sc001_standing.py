"""SC001 later joint targets and provisional planted-step exit. Pure math."""
import math
from elias_articulation import add,sub,mul,mix,unit,two_segment
from sc001_motion import root_at


def standing_joints(frame,left_target=None,right_target=None):
    root=root_at(frame)
    forward=unit((6.3,-5.2,0)) if frame>=2641 else (0,-1,0)
    lateral=(-forward[1],forward[0],0);up=(0,0,1)
    hip=add(root,(0,0,.75));chest=add(hip,(0,0,.65))
    j={'pelvis':hip,'spine':add(hip,(0,0,.325)),'chest':chest,
       'head':add(chest,(0,0,.25)),'up':up,'lateral':lateral,'forward':forward}
    for side,sign,target in [('left',-1,left_target),('right',1,right_target)]:
        shoulder=add(add(chest,(0,0,-.08)),mul(lateral,sign*.225))
        rest=add(add(add(shoulder,(0,0,-.60)),mul(forward,.13)),mul(lateral,sign*.04))
        wrist=target if target is not None else rest
        try:
            elbow=two_segment(shoulder,wrist,add(add(shoulder,mul(forward,.7)),mul(lateral,sign*.4)),.36,.34)
        except ValueError as error:
            raise ValueError(f'SC001 frame {frame}, {side} hand: shoulder={shoulder}, wrist={wrist}, reach={math.dist(shoulder,wrist):.9f} m, limit=0.700 m') from error
        j[side+'_arm']=(shoulder,elbow,wrist)
        ankle=add(add(root,mul(lateral,sign*.12)),mul(forward,.05));ankle=(ankle[0],ankle[1],.10)
        if frame>=2641:
            # Alternate six-frame stance windows. Anchors are world positions, not root offsets.
            offset=0 if side=='left' else 6
            cycle=math.floor((frame-2641+offset)/12);start=2641+cycle*12-offset
            phase=(frame-start)/12
            def anchor(f):
                p=root_at(max(2641,min(2720,f)))
                q=add(add(p,mul(lateral,sign*.12)),mul(forward,.05))
                return (q[0],q[1],.10)
            a=anchor(start+3);b=anchor(start+15)
            if phase<.5:ankle=a
            else:
                t=(phase-.5)*2;ankle=mix(a,b,t*t*(3-2*t))
                lift=.08*math.sin(math.pi*t) if math.dist(a,b)>.001 else 0
                ankle=add(ankle,(0,0,lift))
        leg_hip=add(hip,mul(lateral,sign*.12))
        knee=two_segment(leg_hip,ankle,add(hip,mul(forward,1)),.38,.40)
        j[side]=(leg_hip,knee,ankle)
    return j
