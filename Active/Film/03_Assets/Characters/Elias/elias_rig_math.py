"""Reusable armature and procedural skin definitions; no Blender dependency."""
import math
from elias_articulation import add,sub,mul,mix,unit,dot,cross
from sc001_room_performance import joint_boxes
from elias_hand_math import hands
POSE_FRAMES=[61,360,780,1225,1460,2227,2300,2510,2629,2810]


def bones(s):
    j=s['joints'];origin=s['root'];out={}
    def bone(name,a,b,parent,preferred=None):
        y=unit(sub(b,a));ref=preferred or j['lateral'];x=sub(ref,mul(y,dot(ref,y)))
        if dot(x,x)<1e-8:x=sub((0,0,1),mul(y,y[2]))
        x=unit(x);z=unit(cross(x,y))
        out[name]={'head':sub(a,origin),'tail':sub(b,origin),'basis':(x,y,z),'parent':parent,'length':math.dist(a,b)}
    bone('root',origin,add(origin,(0,0,.20)),None,(1,0,0))
    bone('pelvis',add(j['pelvis'],mul(j['up'],-.09)),add(j['pelvis'],mul(j['up'],.09)),'root')
    bone('spine_01',j['pelvis'],j['spine'],'pelvis');bone('spine_02',j['spine'],j['chest'],'spine_01')
    bone('neck',j['chest'],add(j['chest'],mul(j['up'],.10)),'spine_02')
    bone('head',add(j['head'],mul(j['up'],-.15)),add(j['head'],mul(j['up'],.15)),'neck')
    boxes=joint_boxes(s);hand_plan=hands(s)
    for side,suffix in [('left','L'),('right','R')]:
        a,e,w=j[side+'_arm'];h,k,ankle=j[side]
        bone('upper_arm.'+suffix,a,e,'spine_02');bone('forearm.'+suffix,e,w,'upper_arm.'+suffix)
        palm=hand_plan[side]['palm'];center=palm['center'];axis=mul(palm['basis'][2],-1)
        bone('hand.'+suffix,center,add(center,mul(axis,.10)),'forearm.'+suffix,palm['basis'][0])
        for digit,points in hand_plan[side]['chains'].items():
            for digit_index,(a,b) in enumerate(zip(points,points[1:])):
                name=f'{digit}_{digit_index+1}.{suffix}';parent='hand.'+suffix if digit_index==0 else f'{digit}_{digit_index}.{suffix}'
                bone(name,a,b,parent,palm['basis'][0])
        bone('thigh.'+suffix,h,k,'pelvis');bone('calf.'+suffix,k,ankle,'thigh.'+suffix)
        foot=boxes[side+'_foot'];axis=foot['basis'][1]
        bone('foot.'+suffix,add(foot['center'],mul(axis,-.11)),add(foot['center'],mul(axis,.11)),'calf.'+suffix,foot['basis'][0])
    return out


def skin(rest):
    """Closed components in one mesh; blended elbow/knee tube weights."""
    verts=[];faces=[];weights=[];materials=[];j=rest['joints'];root=rest['root'];boxes=joint_boxes(rest)
    def vertex(p,w):verts.append(sub(p,root));weights.append(w);return len(verts)-1
    def face(ids,material):faces.append(tuple(ids));materials.append(material)
    def tube(centers,radii,axes,groups,material):
        rings=[];steps=12
        for center,radius,axis,w in zip(centers,radii,axes,groups):
            x=sub(j['lateral'],mul(axis,dot(j['lateral'],axis)))
            if dot(x,x)<1e-8:x=sub((0,0,1),mul(axis,axis[2]))
            x=unit(x);z=unit(cross(x,axis))
            ring=[vertex(add(center,add(mul(x,radius*math.cos(t*2*math.pi/steps)),mul(z,radius*math.sin(t*2*math.pi/steps)))),w) for t in range(steps)];rings.append(ring)
        for a,b in zip(rings,rings[1:]):
            for i in range(steps):face([a[i],b[i],b[(i+1)%steps],a[(i+1)%steps]],material)
        start=vertex(centers[0],groups[0]);end=vertex(centers[-1],groups[-1])
        for i in range(steps):face([start,rings[0][i],rings[0][(i+1)%steps]],material);face([end,rings[-1][(i+1)%steps],rings[-1][i]],material)
    def ellipsoid(center,size,basis,name,material):
        count=12;levels=8;ring_ids=[]
        def point(x,y,z):return add(center,add(add(mul(basis[0],x*size[0]/2),mul(basis[1],y*size[1]/2)),mul(basis[2],z*size[2]/2)))
        bottom=vertex(point(0,0,-1),{name:1})
        for i in range(1,levels):
            phi=-math.pi/2+i*math.pi/levels
            ring_ids.append([vertex(point(math.cos(phi)*math.cos(t*2*math.pi/count),math.cos(phi)*math.sin(t*2*math.pi/count),math.sin(phi)),{name:1}) for t in range(count)])
        top=vertex(point(0,0,1),{name:1})
        for i in range(count):face([bottom,ring_ids[0][(i+1)%count],ring_ids[0][i]],material);face([top,ring_ids[-1][i],ring_ids[-1][(i+1)%count]],material)
        for a,b in zip(ring_ids,ring_ids[1:]):
            for i in range(count):face([a[i],a[(i+1)%count],b[(i+1)%count],b[i]],material)
    # Trunk profile keeps shoulder width instead of tapering to a sphere's point.
    ts=[0,.15,.50,.84,1];rs=[.17,.20,.225,.225,.06]
    centers=[add(j['pelvis'],mul(j['up'],.65*t)) for t in ts]
    groups=[{'spine_01':1-t,'spine_02':t} for t in ts]
    # Tube trunk is deliberately within the earlier 0.45 m width; depth comes
    # from compressing the cross-section before skinning.
    begin=len(verts);tube(centers,rs,[j['up']]*len(ts),groups,0)
    for i in range(begin,len(verts)):
        relative=sub(add(verts[i],root),j['pelvis']);depth=dot(relative,j['forward'])
        verts[i]=sub(verts[i],mul(j['forward'],depth*.45))
    for name,bone_name,material in [('pelvis','pelvis',0),('neck','neck',1),('head','head',1)]:
        b=boxes[name];ellipsoid(b['center'],b['size'],b['basis'],bone_name,material)
    for side,suffix in [('left','L'),('right','R')]:
        for chain,first,second,r0,r1,r2 in [(j[side+'_arm'],'upper_arm.'+suffix,'forearm.'+suffix,.07,.055,.045),(j[side],'thigh.'+suffix,'calf.'+suffix,.09,.085,.075)]:
            a,b,c=chain;u=unit(sub(b,a));v=unit(sub(c,b));ss=[0,.25,.65,.85,1,1.15,1.35,1.75,2];centers=[];radii=[];axes=[];groups=[]
            for t in ss:
                centers.append(mix(a,b,t) if t<=1 else mix(b,c,t-1));radii.append(r0+(r1-r0)*t if t<=1 else r1+(r2-r1)*(t-1));axes.append(unit(mix(u,v,max(0,min(1,(t-.85)/.30)))))
                w=max(0,min(1,(t-.85)/.30));groups.append({first:1-w,second:w})
            tube(centers,radii,axes,groups,0)
        for name,bone_name,material in [(side+'_palm','hand.'+suffix,1),(side+'_foot','foot.'+suffix,2)]:
            b=boxes[name];ellipsoid(b['center'],b['size'],b['basis'],bone_name,material)
    for side,hand in hands(rest).items():
        for digit,points in hand['chains'].items():
            for digit_index,(a,b) in enumerate(zip(points,points[1:])):
                axis=unit(sub(b,a));name=f'{digit}_{digit_index+1}.{hand["suffix"]}'
                tube([a,b],[.008 if digit!='thumb' else .010]*2,[axis,axis],[{name:1},{name:1}],1)
    return {'vertices':verts,'faces':faces,'weights':weights,'face_materials':materials}
