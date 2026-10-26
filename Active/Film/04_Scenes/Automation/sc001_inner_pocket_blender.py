"""Lapel/lining shape controls and evaluated Child Of custody handoff."""
import math

def body_matrix(s):
    from mathutils import Matrix,Vector
    j=s['joints'];m=Matrix((tuple(-v for v in j['lateral']),j['up'],j['forward'])).transposed().to_4x4();m.translation=Vector(j['pelvis']);return m

def independent_key(obj,name,basis,coordinates):
    """Never inherit an active/mixed key when building additive jacket controls."""
    key=obj.shape_key_add(name=name,from_mix=False)
    key.relative_key=basis
    for item,co in zip(key.data,coordinates):item.co=co
    return key

def create(bpy,scene,s):
    for name,lo,hi,front in [('REVIEW_Jacket_lapel',(-.02,.20),(.32,.58),.17),('REVIEW_InnerPocket_lining',(-.08,.20),(.28,.48),.22)]:
        verts=[(lo[0]+(hi[0]-lo[0])*x/4,lo[1]+(hi[1]-lo[1])*y/4,front) for y in range(5) for x in range(5)]
        faces=[(y*5+x,y*5+x+1,(y+1)*5+x+1,(y+1)*5+x) for y in range(4) for x in range(4)]
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new(name,mesh);scene.collection.objects.link(obj);obj.matrix_world=body_matrix(s)
        basis=obj.shape_key_add(name='Basis',from_mix=False);obj.data.shape_keys.use_relative=True
        pull=independent_key(obj,'PullOpen',basis,verts);pull.slider_min=-.15;pull.slider_max=1.15
        for i,v in enumerate(verts):
            x=(v[0]-lo[0])/(hi[0]-lo[0]);pull.data[i].co.x+=.09*(1-x) if 'lapel' in name else 0;pull.data[i].co.z+=.23*(1-x) if 'lapel' in name else .11
        if 'lining' in name:
            bulge=independent_key(obj,'HandBulge',basis,verts)
            for i,v in enumerate(verts):
                x=(v[0]-lo[0])/(hi[0]-lo[0]);y=(v[1]-lo[1])/(hi[1]-lo[1]);bulge.data[i].co.z+=.025*math.sin(math.pi*x)*math.sin(math.pi*y)
        obj['status']='controlled_jacket_patch_not_final_wardrobe_or_cloth_simulation'
    bpy.ops.mesh.primitive_cube_add(size=1);obj=bpy.context.object;obj.name='REVIEW_InnerPocket_bottom';obj.dimensions=(.36,.01,.22)
    key_geometry(bpy,scene,s,1)

def key_geometry(bpy,scene,s,frame):
    from mathutils import Matrix,Vector
    base=body_matrix(s)
    for name in ('REVIEW_Jacket_lapel','REVIEW_InnerPocket_lining'):
        obj=scene.objects[name];obj.matrix_world=base
        for field in ('location','rotation_euler','scale'):obj.keyframe_insert(data_path=field,frame=frame)
        keys=obj.data.shape_keys.key_blocks;keys['PullOpen'].value=s['_inner_pocket']['opening'];keys['PullOpen'].keyframe_insert(data_path='value',frame=frame)
        if 'HandBulge' in keys:keys['HandBulge'].value=s['_inner_pocket']['bulge'];keys['HandBulge'].keyframe_insert(data_path='value',frame=frame)
    obj=scene.objects['REVIEW_InnerPocket_bottom'];obj.location=base@Vector((.10,.195,.24));obj.rotation_euler=base.to_euler()
    for field in ('location','rotation_euler'):obj.keyframe_insert(data_path=field,frame=frame)

def custody(bpy,scene,state,layout,start=1,end=70,attach=1,release=44):
    from mathutils import Matrix,Vector
    from sc001_motion_blender import linearise_owned_actions
    rig=scene.objects['CHR_Elias_RIG'];names=[('PRP_MACEnvelope','envelope'),('PRP_ResignationLetter','letter'),('Envelope_text_anchor','envelope')]
    def goal(s,field):
        m=Matrix(s['_packet_basis_override']).transposed().to_4x4();m.translation=Vector(s[field]);return m
    scene.frame_set(attach);bpy.context.view_layer.update();driver=rig.matrix_world@rig.pose.bones['palm.R'].matrix
    binds={name:driver.inverted()@goal(state(attach,layout),field) for name,field in names}
    constraints={}
    for name,_ in names:
        obj=scene.objects[name];c=obj.constraints.new('CHILD_OF');c.name='Pocket_hand_custody';c.target=rig;c.subtarget='palm.R';c.inverse_matrix=Matrix.Identity(4);constraints[name]=c
    for frame in range(start,end+1):
        scene.frame_set(frame);s=state(frame,layout)
        for name,field in names:
            obj=scene.objects[name];c=constraints[name];c.influence=s['_inner_pocket']['hand_influence'];obj.matrix_basis=binds[name] if attach<=frame<release else goal(s,field)
            for path in ('location','rotation_euler','scale'):obj.keyframe_insert(data_path=path,frame=frame)
            c.keyframe_insert(data_path='influence',frame=frame)
    objects=[scene.objects[n] for n,_ in names]+[scene.objects[n] for n in ('REVIEW_Jacket_lapel','REVIEW_InnerPocket_lining','REVIEW_InnerPocket_bottom')]
    linearise_owned_actions(objects+[scene.objects[n].data.shape_keys for n in ('REVIEW_Jacket_lapel','REVIEW_InnerPocket_lining')])
    # Constraint influence is a custody switch, never a fractional crossfade.
    for name,_ in names:
        action=scene.objects[name].animation_data.action;curves=[]
        if getattr(action,'is_action_layered',False):
            for layer in action.layers:
                for strip in layer.strips:
                    for bag in getattr(strip,'channelbags',()):curves.extend(bag.fcurves)
        else:curves=list(action.fcurves)
        for curve in curves:
            if 'Pocket_hand_custody' in curve.data_path:
                for key in curve.keyframe_points:key.interpolation='CONSTANT'
            elif curve.data_path in ('location','rotation_euler','scale'):
                for key in curve.keyframe_points:
                    if any(abs(key.co.x-boundary)<1e-6 for boundary in (attach-1,release-1)):key.interpolation='CONSTANT'
    # Reject handoff pops at the half-frame immediately before release.
    samples=[release-1,release-.5,release,release+.5]+([attach-1,attach-.5,attach] if attach>start else [])
    for f in sorted(set(x for x in samples if start<=x<=end)):
        scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        for name,field in names:
            actual=scene.objects[name].evaluated_get(deps).matrix_world
            expected=goal(state(int(f),layout),field)
            assert max(abs(actual[i][k]-expected[i][k]) for i in range(4) for k in range(4))<1e-4,(name,f,'Custody handoff discontinuity')
    return {'release_frame':release,'attach_frame':attach,'target':'CHR_Elias_RIG:palm.R','objects':[n for n,_ in names],'mode':'Child Of holding, pocket-relative keyed placement after release; evaluated gate pending'}

def validate(bpy,scene,s,frame):
    from mathutils import Vector
    deps=bpy.context.evaluated_depsgraph_get();rig=scene.objects['CHR_Elias_RIG'].evaluated_get(deps);meta=s['_inner_pocket'];maximum=0
    for side,suffix in [('left','L'),('right','R')]:
        for digit in ('index','middle','thumb'):
            actual=rig.matrix_world@rig.pose.bones[digit+'_3.'+suffix].tail;target=Vector(s['_hand_plan'][side]['chains'][digit][-1]);error=(actual-target).length;maximum=max(maximum,error);assert error<1e-4,(frame,side,digit,'Finger target',error)
    for name in ('REVIEW_Jacket_lapel','REVIEW_InnerPocket_lining'):
        keys=scene.objects[name].data.shape_keys.key_blocks
        assert abs(keys['PullOpen'].value-meta['opening'])<1e-5
        if 'HandBulge' in keys:assert abs(keys['HandBulge'].value-meta['bulge'])<1e-5
    if meta['left_active']:
        # Inner edge is linear in height; verify the evaluated cloth point, not only targets.
        obj=scene.objects['REVIEW_Jacket_lapel'].evaluated_get(deps);mesh=obj.to_mesh()
        try:
            # Grid edge nodes at heights .485 and .58 bracket .53.
            a=obj.matrix_world@mesh.vertices[15].co;b=obj.matrix_world@mesh.vertices[20].co;actual=a.lerp(b,(.53-.485)/.095)
            assert (actual-Vector(meta['left_contact'])).length<1e-4,(frame,'Lapel contact mapping')
        finally:obj.to_mesh_clear()
        for digit,expected in [('index',.009),('thumb',-.011)]:
            tip=rig.matrix_world@rig.pose.bones[digit+'_3.L'].tail
            assert abs((tip-Vector(meta['left_contact'])).dot(Vector(meta['left_normal']))-expected)<1e-4,(frame,'Lapel pad gap',digit)
    lining=scene.objects['REVIEW_InnerPocket_lining'].evaluated_get(deps);mesh=lining.to_mesh()
    try:
        expected=body_matrix(s)@Vector((.10,.34,.22+.11*meta['opening']+.025*meta['bulge']))
        actual=lining.matrix_world@mesh.vertices[12].co;error=(actual-expected).length;maximum=max(maximum,error)
        assert error<1e-4,(frame,'Evaluated lining bulge',{'actual':tuple(actual),'expected':tuple(expected),'error_m':error,'opening':meta['opening'],'bulge':meta['bulge']})
    finally:lining.to_mesh_clear()
    c=scene.objects['PRP_MACEnvelope'].constraints['Pocket_hand_custody'];assert c.influence==meta['hand_influence']
    if meta.get('support_active',frame>=40):
        up=Vector(s['joints']['up']);origin=Vector(s['joints']['pelvis'])
        def heights(name):
            obj=scene.objects[name].evaluated_get(deps);return [((obj.matrix_world@Vector(p))-origin).dot(up) for p in obj.bound_box]
        gap=min(heights('Envelope_back'))-max(heights('REVIEW_InnerPocket_bottom'));assert abs(gap)<1e-4,(frame,'Inner pocket support',gap);maximum=max(maximum,abs(gap))
    return maximum
