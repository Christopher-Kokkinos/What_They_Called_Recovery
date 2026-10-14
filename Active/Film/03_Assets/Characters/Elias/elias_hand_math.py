"""Provisional reusable five-digit hands driven by existing SC001 palm targets."""
import math
from elias_articulation import add,sub,mul,unit,dot,cross,mix
from sc001_room_performance import joint_boxes


def hands(s):
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
            length=[.065,.072,.068,.055][i];base=add(center,add(mul(x,(i-1.5)*.019),mul(direction,palm['size'][2]*.36)))
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
        out[side]={'palm':palm,'chains':chains,'mode':mode,'curl':curl,'suffix':suffix,'legacy_palm':original}
    return out
