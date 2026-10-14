"""Shared Elias rig construction and exact FK sampling for Blender."""
import math
from mathutils import Matrix,Vector
from elias_rig_math import bones,skin


def create(bpy,scene,rest):
    definition=bones(rest);surface=skin(rest)
    asset=bpy.data.collections.new('CHR_Elias_rig_v0.3');scene.collection.children.link(asset);asset['asset_id']='CHR_Elias';asset['status']='deformation_mannequin_not_final_design'
    data=bpy.data.armatures.new('Elias_skeleton');rig=bpy.data.objects.new('CHR_Elias_RIG',data);asset.objects.link(rig);rig.show_in_front=True;rig['source']='verified SC001 joint targets'
    bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    for name,b in definition.items():
        bone=data.edit_bones.new(name);bone.head=b['head'];bone.tail=b['tail'];bone.align_roll(Vector(b['basis'][2]));bone.use_deform=name!='root'
        if b['parent']:bone.parent=data.edit_bones[b['parent']];bone.use_connect=False
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh=bpy.data.meshes.new('Elias_procedural_skin');mesh.from_pydata(surface['vertices'],[],surface['faces']);mesh.update()
    obj=bpy.data.objects.new('CHR_Elias_SKIN',mesh);asset.objects.link(obj)
    for name in definition:obj.vertex_groups.new(name=name)
    for index,w in enumerate(surface['weights']):
        for name,value in w.items():
            if value>0:obj.vertex_groups[name].add([index],value,'REPLACE')
    for name,color in [('neutral_wardrobe',(.25,.32,.36,1)),('neutral_mannequin',(.52,.52,.49,1)),('shoe_proxy',(.16,.19,.21,1))]:
        material=bpy.data.materials.new(name);material.diffuse_color=color;mesh.materials.append(material)
    obj['palm_vertex_indices_json']=__import__('json').dumps(surface['palm_vertex_indices'])
    for polygon,material in zip(mesh.polygons,surface['face_materials']):polygon.material_index=material;polygon.use_smooth=True
    modifier=obj.modifiers.new('Elias_armature_deform','ARMATURE');modifier.object=rig;modifier.use_deform_preserve_volume=True
    obj.parent=rig
    return rig,obj,definition


def pose_frame(bpy,rig,s,frame):
    rig.location=s['root'];rig.keyframe_insert(data_path='location',frame=frame)
    target=bones(s)
    for name,b in target.items():
        pose=rig.pose.bones[name];pose.rotation_mode='QUATERNION'
        matrix=Matrix(b['basis']).transposed().to_4x4();matrix.translation=Vector(b['head']);pose.matrix=matrix
        for field in ('location','rotation_quaternion','scale'):pose.keyframe_insert(data_path=field,frame=frame)
        bpy.context.view_layer.update()


def animate_and_validate(bpy,scene,layout,state,end):
    rig,obj,definition=create(bpy,scene,state(889,layout))
    for frame in range(1,end+1):
        scene.frame_set(frame);pose_frame(bpy,rig,state(frame,layout),frame)
    from sc001_motion_blender import linearise_owned_actions
    linearise_owned_actions([rig])
    palm_indices=__import__('json').loads(obj['palm_vertex_indices_json'])
    palm_error=0
    endpoint=scale=0;lowest=math.inf;checked=0
    # Read back the keyed action, including frames between rendered preview samples.
    for frame in range(1,end+1):
        scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        evaluated=rig.evaluated_get(deps);target=bones(state(frame,layout))
        for name,b in target.items():
            pose=evaluated.pose.bones[name]
            endpoint=max(endpoint,(pose.head-Vector(b['head'])).length,(pose.tail-Vector(b['tail'])).length)
            scale=max(scale,*[abs(v-1) for v in pose.matrix.to_scale()])
        skin_obj=obj.evaluated_get(deps);mesh=skin_obj.to_mesh()
        try:
            assert len(mesh.vertices)==len(obj.data.vertices),'Unexpected skin topology change'
            points=[skin_obj.matrix_world@v.co for v in mesh.vertices]
            assert all(math.isfinite(v) for p in points for v in p),'Non-finite skin vertex'
            from elias_hand_math import hands
            for side,hand in hands(state(frame,layout)).items():
                indices=palm_indices[hand['suffix']];assert indices,'Missing palm skin weights'
                center=sum((points[i] for i in indices),Vector((0,0,0)))/len(indices)
                palm_error=max(palm_error,(center-Vector(hand['palm']['center'])).length)
            lowest=min(lowest,min(p.z for p in points));checked+=len(points)
        finally:skin_obj.to_mesh_clear()
    assert endpoint<1e-4,f'Rig endpoint mismatch: {endpoint}'
    assert scale<1e-4,f'Rig bone scale mismatch: {scale}'
    assert palm_error<1e-4,f'Palm target mapping mismatch: {palm_error}'
    return {'maximum_palm_center_error':palm_error,'frames_checked':end,'mesh_vertex_checks':checked,'maximum_endpoint_error':endpoint,'maximum_bone_scale_error':scale,'minimum_skin_world_z':lowest,'skin_contact_status':'visual_review_required; proxy contact gates retained','limitations':['Skin volume differs from box contacts; not a skin collision pass','Articulated provisional fingers; exact grips/collisions require visual review','Integer-frame FK bake; fractional-frame interpolation not validated']}
