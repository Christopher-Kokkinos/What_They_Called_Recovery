"""Provisional reusable five-digit hands driven by existing SC001 palm targets."""
import math
from elias_articulation import add,sub,mul,unit,dot,cross,mix,two_segment
from sc001_room_performance import joint_boxes


def hands(s):
    if '_hand_plan' in s:return s['_hand_plan']
    boxes=joint_boxes(s);out={};f=s['frame']
    def ramp(a,b):return max(0,min(1,(f-a)/(b-a)))
    for side,suffix in [('left','L'),('right','R')]:
        palm=boxes[side+'_palm'];x,y,z=palm['basis'];center=palm['center'];mode='relaxed';curl=.18
        if side=='left' and 580<=f<=888:mode='drawer';curl=.60*ramp(590,600)*(1-ramp(850,870))
        elif side=='right' and 1180<=f<=1260:mode='shower';curl=.55*ramp(1180,1210)*(1-ramp(1230,1260))
        elif side=='left' and (1375<=f<=1540 or f>=2430):mode='mug';curl=.85*(ramp(1375,1400)*(1-ramp(1500,1540)) if f<2430 else ramp(2430,2450))
        elif 2161<=f<2360:mode='paper';curl=.25
        elif side=='right' and f>=2380:mode='keys';curl=.95*ramp(2380,2395)
        # Flatten palm and align paper hands to the packet plane instead of
        # letting the spherical placeholder intersect the page at insertion.
        original=palm
        if mode=='mug':
            x=mul(s['ground_forward'],-1);y=s['joints']['lateral'];z=(0,0,1)
        elif mode=='shower':x=mul(x,-1);y=mul(y,-1)
        if mode=='paper':
            t=s['pocket_rotation'] if f>=2320 else 0
            normal=unit(mix((0,0,1),s['packet_basis'][2],t))
            x=unit(sub((1,0,0),mul(normal,normal[0]))) if abs(normal[0])<.99 else s['joints']['lateral']
            z=unit(cross(x,normal));y=normal
            surface=s['envelope'] if f>=2275 else s['letter']
            if not(side=='left' and f<2260):center=add(sub(center,mul(normal,dot(sub(center,surface),normal))),mul(normal,.032))
            curl=.15
        palm={'center':center,'size':(.075,.026,.075),'basis':(x,y,z)}
        # Palm positions/bases come from the verified contact boxes. Fingers
        # are provisional articulation, not certified contact/force geometry.
        direction=mul(z,-1);bend=y
        chains={}
        for i,name in enumerate(['index','middle','ring','little']):
            length=[.065,.072,.068,.055][i];base=add(center,add(mul(x,(i-1.5)*.019*(-1 if side=='right' else 1)),mul(direction,palm['size'][2]*.36)))
            points=[base]
            for k,fraction in enumerate([.42,.33,.25]):
                angle=curl*(k+1)*.75;
                if mode=='paper':angle=-curl*(k+1)*.55
                step=add(mul(direction,math.cos(angle)),mul(bend,math.sin(angle)))
                points.append(add(points[-1],mul(step,length*fraction)))
            chains[name]=points
        sign=-1 if side=='left' else 1
        base=add(center,mul(x,sign*.031));points=[base]
        for k,length in enumerate([.025,.023,.020]):
            step=unit(add(add(mul(x,sign*(1-curl*.85)),mul(direction,.85)),mul(y,curl*(k+1)*.25)))
            points.append(add(points[-1],mul(step,length)))
        chains['thumb']=points
        pinch=None
        if mode in ('paper','keys'):
            # Opposed index/thumb pads, with a 16 mm centre separation.
            # Targets are provisional surface contacts, not force constraints.
            index_target=add(add(center,mul(direction,.052)),add(mul(x,sign*.0285),mul(y,-.024))) if mode=='paper' else add(s['keys'],(0,0,.008))
            thumb_target=add(index_target,mul(y,-.016)) if mode=='paper' else add(s['keys'],(0,0,-.008))
            amount=ramp(2161,2215)*(1-ramp(2340,2360)) if mode=='paper' else ramp(2380,2395)
            for digit,target,lengths in [('index',index_target,[.065*.42,.065*.33,.065*.25]),('thumb',thumb_target,[.025,.023,.020])]:
                original_chain=chains[digit];base=original_chain[0];target=mix(original_chain[-1],target,amount)
                # Preserve every phalange length while changing the contact.
                distal=lengths[1]+lengths[2];delta=sub(target,base);distance=math.sqrt(dot(delta,delta))
                maximum=sum(lengths)-1e-6;minimum=abs(lengths[0]-distal)+1e-6
                if not minimum<=distance<=maximum:target=add(base,mul(unit(delta),max(minimum,min(maximum,distance))))
                middle=two_segment(base,target,add(base,mul(y,.08)),lengths[0],distal)
                last_joint=mix(middle,target,lengths[1]/distal)
                chains[digit]=[base,middle,last_joint,target]
            pinch={'index_target':index_target,'thumb_target':thumb_target,'amount':amount,'index_tip':chains['index'][-1],'thumb_tip':chains['thumb'][-1]}

        out[side]={'palm':palm,'chains':chains,'mode':mode,'curl':curl,'suffix':suffix,'legacy_palm':original,'pinch':pinch}
    return out
