"""Open rigid pocket proxy and evaluated support gate for focused blockout."""
def create(bpy,scene,s):
    from mathutils import Matrix
    from elias_pocket import proxy_boxes
    for box in proxy_boxes(s):
        assert box['name'] not in scene.objects
        bpy.ops.mesh.primitive_cube_add(size=1,location=box['center'])
        obj=bpy.context.object;obj.name=box['name'];obj.dimensions=box['size'];obj.rotation_euler=Matrix(box['basis']).transposed().to_euler()
        obj['status']='temporary_open_pocket_proxy_not_final_clothing'

def validate(bpy,scene,s,frame):
    if frame<2820:return 0
    from mathutils import Vector
    j=s['joints'];deps=bpy.context.evaluated_depsgraph_get();up=Vector(j['up']);origin=Vector(j['pelvis'])
    def heights(name):
        obj=scene.objects[name].evaluated_get(deps)
        return [((obj.matrix_world@Vector(p))-origin).dot(up) for p in obj.bound_box]
    gap=min(heights('Envelope_back'))-max(heights('REVIEW_Pocket_bottom'))
    assert abs(gap)<1e-4,(frame,'Pocket floor support',gap)
    return abs(gap)
