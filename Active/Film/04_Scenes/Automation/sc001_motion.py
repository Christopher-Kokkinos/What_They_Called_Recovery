"""Pure, testable SC001 coarse timing and prop-custody plan (DEC-0028).
Linear blocking, editorial elisions at shot boundaries, no final performance.
"""
import math
from elias_articulation import STANDING_HIP_HEIGHT, SEATED_HIP_HEIGHT

# Keep standing prop offsets relative to the shared pelvis height.
STANDING_HEIGHT_DELTA = STANDING_HIP_HEIGHT - .75
CARRIED_MUG_OFFSET = (-.4,-.28,1.05+STANDING_HEIGHT_DELTA)
CARRIED_KEYS_OFFSET = (.35,-.28,1.05+STANDING_HEIGHT_DELTA)
POCKET_OFFSET = (.08,-.075,1.2+STANDING_HEIGHT_DELTA)
DRINK_MUG_OFFSET = (0,-.19,1.38+STANDING_HEIGHT_DELTA)
SHOWER_HAND_OFFSET = (.25,-.25,1.55+STANDING_HEIGHT_DELTA)
JACKET_OFFSET = (0,.18,1.1+STANDING_HEIGHT_DELTA)

BEDSIDE_LEAN_RADIANS = .66
EXIT_START = 2641
EXIT_ARRIVAL = 2840
SCENE_END = 2880

ROOT_KEYS = [
    (1,(2,5.15,SEATED_HIP_HEIGHT)),(270,(2,5.15,SEATED_HIP_HEIGHT)),(350,(2.50,5.8,.10)),
    (888,(2.50,5.8,.10)),(889,(5,4.6,0)),(1128,(5,4.6,0)),
    (1129,(9,5,0)),(1368,(9,5,0)),(1369,(5.1,5,0)),
    (2160,(5.1,5,0)),(2161,(6.7,4.7,0)),(2440,(6.7,4.7,0)),
    (2520,(6.7,4.7,0)),(2521,(1.2,4.5,0)),(2640,(1.2,4.5,0)),(EXIT_ARRIVAL,(7.5,-.7,0)),
    (SCENE_END,(7.5,-.7,0)),
]
EVENTS = [
    {'frame':60,'event':'opening pigeon peck'},
    {'frame':270,'event':'wake/sit begins'},
    {'frame':350,'event':'seated; right arm supports left rib area'},
    {'frame':661,'event':'prescription insert; two empty cells, no tablet pickup'},
    {'frame':810,'event':'drawer closure begins'},
    {'frame':870,'event':'drawer closed; prescription hidden inside'},
    {'frame':1190,'event':'shower control reach'},
    {'frame':1260,'event':'cold-water reaction / Excellent cue'},
    {'frame':1400,'event':'coffee pickup begins'},
    {'frame':1470,'event':'mug held for coarse drink gesture'},
    {'frame':1540,'event':'mug returned to counter'},
    {'frame':1561,'event':'exact notice reading hold begins'},
    {'frame':2220,'event':'letter folding begins'},
    {'frame':2300,'event':'letter/envelope pocket transfer begins'},
    {'frame':2340,'event':'letter/envelope in inner pocket; hand pause'},
    {'frame':2380,'event':'keys pickup'},
    {'frame':2420,'event':'mug pickup for departure'},
    {'frame':2521,'event':'at window with carried props'},
    {'frame':2550,'event':"Flat's yours dialogue cue"},
    {'frame':2641,'event':'exit travel begins'},
    {'frame':EXIT_ARRIVAL,'event':'outside entry; letter/envelope/keys/mug retained'},
    {'frame':2860,'event':'final pigeon peck'},
]


def lerp_keys(keys, frame):
    if frame <= keys[0][0]:
        return tuple(keys[0][1])
    for (a,x),(b,y) in zip(keys,keys[1:]):
        if frame <= b:
            t=(frame-a)/(b-a)
            return tuple(u+(v-u)*t for u,v in zip(x,y))
    return tuple(keys[-1][1])


def root_at(frame):
    x,y,z = lerp_keys(ROOT_KEYS,frame)
    lean = bedside_lean(frame)
    return (x+.20*lean,y-.08*lean,z)


def pose_weights(frame):
    lying=max(0,min(1,(350-frame)/80)) if frame>=270 else 1
    seated=1-lying if frame<=888 else 0
    return lying,seated


def carried_position(frame, offset):
    return tuple(a+b for a,b in zip(root_at(frame),offset))


def custody_at(frame):
    return {
        'letter_envelope':'counter' if frame<2300 else ('transfer' if frame<2340 else 'inner_pocket'),
        'keys':'counter' if frame<2380 else ('transfer' if frame<2410 else 'right_hand'),
        'mug':('coffee_gesture' if 1400<=frame<1540 else ('counter' if frame<2420 else ('transfer' if frame<2440 else 'left_hand'))),
        'prescription':'drawer_visible' if frame<870 else 'closed_drawer',
        'dose_taken':False,
    }


def sample_frames(spec):
    frames={1,SCENE_END,*[f for f,_ in ROOT_KEYS],*[e['frame'] for e in EVENTS]}
    frames.update([60,75,120,750,780,810,840,870,888,1399,1400,1470,1510,1540,2219,2220,2260,2299,2300,2340,2379,2380,2410,2419,2420,2440,2850,2860,2870])
    for s in spec['shots']:
        frames.update([s['frame_start'],s['frame_end']])
    return sorted(frames)


def preview_frames(spec):
    return list(range(spec['frame_start'],spec['frame_end']+1,6))


def shot_at(spec,frame):
    return next(s for s in spec['shots'] if s['frame_start']<=frame<=s['frame_end'])

def root_rotation(frame):
    lying,seated=pose_weights(frame)
    return (-lying*math.pi/2,0,seated*math.pi/2)

def camera_radial(origin, bearing, radius, height=2.0):
    angle=math.radians(bearing)
    return (origin[0]+radius*math.sin(angle),origin[1]+radius*math.cos(angle),height)

def bedside_lean(frame):
    if frame<750 or frame>888:return 0
    if frame<810:return (frame-750)/60
    if frame<=870:return 1
    return (888-frame)/18

def upper_point(point,frame):
    """Rigid upper-body rotation around shared seated hip pivot."""
    x,y,z=point;angle=BEDSIDE_LEAN_RADIANS*bedside_lean(frame);c=math.cos(angle);s=math.sin(angle)
    return (x,y*c-(z-.75)*s,.75+y*s+(z-.75)*c)


def coffee_target(frame):
    counter=(6.3,4.42,1.02) if frame>=2161 else (4.8,4.65,1.02)
    if 1400<=frame<=1470:t=(frame-1400)/70
    elif 1470<frame<1510:t=1
    elif 1510<=frame<1540:t=1-(frame-1510)/30
    elif frame>=2420:t=min(1,(frame-2420)/20)
    else:t=0
    hand=carried_position(frame,DRINK_MUG_OFFSET) if frame<1540 else carry_position(frame,CARRIED_MUG_OFFSET)
    return tuple(a+(b-a)*t for a,b in zip(counter,hand))


def standing_yaw(frame):
    return math.atan2(6.3,5.2) if frame>=EXIT_START else 0.0


def pocket_position(frame):
    x,y,z=POCKET_OFFSET;angle=standing_yaw(frame)
    return carried_position(frame,(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),z))


def carry_vector(frame,offset):
    x,y,z=offset;angle=standing_yaw(frame)
    return (x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),z)


def carry_position(frame,offset):
    if frame>=EXIT_START and offset==CARRIED_MUG_OFFSET:
        offset=(-.30,offset[1],offset[2])
    if frame>=EXIT_START and offset==CARRIED_KEYS_OFFSET:
        offset=(.25,offset[1],offset[2])
    return carried_position(frame,carry_vector(frame,offset))


def mug_grip(frame,offset=(.19,0,.11)):
    from elias_articulation import add
    return add(coffee_target(frame),carry_vector(frame,offset))
