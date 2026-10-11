"""Pure, testable SC001 coarse timing and prop-custody plan (DEC-0028).
Linear blocking, editorial elisions at shot boundaries, no final performance.
"""
import math

ROOT_KEYS = [
    (1,(2,5.15,.85)),(270,(2,5.15,.85)),(350,(2.80,5.8,.10)),
    (888,(2.80,5.8,.10)),(889,(5,4.6,0)),(1128,(5,4.6,0)),
    (1129,(9,5,0)),(1368,(9,5,0)),(1369,(5.1,5,0)),
    (2160,(5.1,5,0)),(2161,(6.7,4.7,0)),(2440,(6.7,4.7,0)),
    (2520,(6.7,4.7,0)),(2521,(1.2,4.5,0)),(2640,(1.2,4.5,0)),(2720,(7.5,-.7,0)),
    (2760,(7.5,-.7,0)),
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
    {'frame':2720,'event':'outside entry; letter/envelope/keys/mug retained'},
    {'frame':2740,'event':'final pigeon peck'},
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
    return lerp_keys(ROOT_KEYS,frame)


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
    frames={1,2760,*[f for f,_ in ROOT_KEYS],*[e['frame'] for e in EVENTS]}
    frames.update([60,75,120,810,870,1399,1400,1470,1510,1540,2219,2220,2260,2299,2300,2340,2379,2380,2410,2419,2420,2440,2730,2740,2750])
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
