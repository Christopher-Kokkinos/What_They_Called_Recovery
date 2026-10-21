"""Two-hand inner-jacket pocket diagnostic; semantic frames1–70."""
import math
from copy import deepcopy
from elias_paper_contact import pinch
from elias_envelope_contact import blend_hand,digit_target
from elias_table_reach import state as table_state
from elias_articulation import add,sub,mul,mix,unit,cross,two_segment,UPPER_ARM_LENGTH,FOREARM_LENGTH,SPINE_LENGTH
from sc001_room_performance import progress
START,END,RELEASE=1,70,44
FLOOR=.20

def point(j,w,u,f):return add(add(add(j['pelvis'],mul(j['lateral'],-w)),mul(j['up'],u)),mul(j['forward'],f))
def vector(j,w,u,f):return sub(point(j,w,u,f),j['pelvis'])
def local(j,p):
    from elias_articulation import dot
    d=sub(p,j['pelvis']);return (-dot(d,j['lateral']),dot(d,j['up']),dot(d,j['forward']))

def opening(f):
    if f<=55:return progress(f,7,20)
    if f<=63:return 1-progress(f,55,63)
    t=f-63;return .06*math.exp(-.4*t)*math.sin(t*math.pi/3.5)

def grip(j,center,basis):
    width,height,normal=basis;contact=add(add(center,mul(width,-.06)),mul(height,.08))
    direction=add(mul(height,.8),mul(normal,-.6));pn=add(mul(height,.6),mul(normal,.8))
    h,w=pinch(contact,normal,direction,'right',palm_normal=pn,index_offset=.016)
    digit_target(h,'middle',add(add(contact,mul(width,.012)),mul(normal,.016)))
    return h,w

def state(frame,layout):
    f=START if frame==889 else frame;assert START<=f<=END
    s=deepcopy(table_state(1400,layout));j=s['joints']
    lean=.20+.035*progress(f,20,40)*(1-progress(f,55,70));j['up']=(math.sin(lean),0,math.cos(lean));j['forward']=unit(cross(j['up'],j['lateral']))
    j['spine']=add(j['pelvis'],mul(j['up'],SPINE_LENGTH/2));j['chest']=add(j['pelvis'],mul(j['up'],SPINE_LENGTH));j['head']=add(j['chest'],mul(j['up'],.25))
    for side,sign in [('left',-1),('right',1)]:
        shoulder=add(add(j['chest'],mul(j['up'],-.08)),mul(j['lateral'],sign*.225));j[side+'_arm']=(shoulder,shoulder,shoulder)
    o=opening(f);theta=math.pi/4*progress(f,1,20);W=mul(j['lateral'],-1);U=j['up'];N=j['forward']
    B=(add(mul(W,math.cos(theta)),mul(U,-math.sin(theta))),add(mul(W,math.sin(theta)),mul(U,math.cos(theta))),N)
    insert=progress(f,20,40);height=.625-(.625-(FLOOR+(.11+.085)/math.sqrt(2)))*insert
    center=point(j,-.12+.22*progress(f,1,20)-.025*math.sin(math.pi*insert),height,.30-.095*insert)
    s['envelope']=center;s['letter']=add(add(center,mul(B[1],.07425)),mul(N,.0035));s['_packet_basis_override']=B
    h,rw=grip(j,center,B)
    if f>=41:
        digit_target(h,'thumb',add(h['chains']['thumb'][-1],mul(N,-.003*progress(f,40,44))))
        # Two-frame pad drag at the top edge while packet custody changes.
        drag=.003*progress(f,43,45)
        digit_target(h,'index',add(h['chains']['index'][-1],mul(B[1],drag)))
    if f>=46:
        shift=add(mul(U,.19*progress(f,45,55)),mul(N,.07*progress(f,52,60)))
        h['palm']['center']=add(h['palm']['center'],shift);h['chains']={d:[add(p,shift) for p in ch] for d,ch in h['chains'].items()};rw=add(rw,shift)
    grab=point(j,-.02+.09*o,.53,.17+.23*o)
    normal=unit(vector(j,.23*o/(.34-.09*o),0,1));direction=unit(vector(j,-.8,-.2,-.3));pn=unit(sub(normal,mul(direction,sum(a*b for a,b in zip(normal,direction)))))
    lh,lw=pinch(grab,normal,direction,'left',palm_normal=pn,opening=.008*(1-progress(f,1,7)))
    if f<7:
        shift=vector(j,.12,-.12,.04);shift=mul(shift,1-progress(f,1,7));lh['palm']['center']=add(lh['palm']['center'],shift);lh['chains']={d:[add(p,shift) for p in ch] for d,ch in lh['chains'].items()};lw=add(lw,shift)
    if f>55:
        shift=vector(j,.16,-.16,.10);lh['palm']['center']=add(lh['palm']['center'],mul(shift,progress(f,55,70)));lh['chains']={d:[add(p,mul(shift,progress(f,55,70))) for p in ch] for d,ch in lh['chains'].items()};lw=add(lw,mul(shift,progress(f,55,70)))
    s['_hand_plan']={'left':lh,'right':h};s['_hand_origins']={'left':lw,'right':rw};s['_palm_controls']=('left','right')
    for side,w in [('left',lw),('right',rw)]:
        sh=j[side+'_arm'][0];axis=mul(s['_hand_plan'][side]['palm']['basis'][2],-1);pole=sub(w,mul(axis,FOREARM_LENGTH))
        if side=='left':pole=mix(pole,point(j,-.30,.12,.20),.20)
        e=two_segment(sh,w,pole,UPPER_ARM_LENGTH,FOREARM_LENGTH);j[side+'_arm']=(sh,e,w)
    s.update(frame=f,fold=1,mug=(11.24,8.98,1.06),keys=(11.65,9.05,.978),_envelope_flap_angle=0,_envelope_mouth_angle=0,_notice_hidden=True)
    s['_inner_pocket']={'opening':o,'bulge':.65*progress(f,21,35)*(1-progress(f,48,60))+.15*progress(f,35,44),'hand_influence':1 if f<RELEASE else 0,'left_contact':grab,'left_normal':normal,'left_active':7<=f<=55,'right_index_active':f<=45,'right_thumb_active':f<=40}
    s['_sequence_phase']='lapel_pull' if f<=20 else 'bottom_first_insert' if f<=40 else 'release_with_pad_drag' if f<=50 else 'upward_withdrawal_and_lapel_settle'
    s['_paper_support']='right_hand' if f<RELEASE else 'inner_pocket';s['_insertion']=insert
    return s


def review_camera_offset(s,closeup=False):
    """Face the packet normal; keep a modest side/elevation cue for depth."""
    return vector(s['joints'],.35 if closeup else .8,.25 if closeup else .6,2.0)
