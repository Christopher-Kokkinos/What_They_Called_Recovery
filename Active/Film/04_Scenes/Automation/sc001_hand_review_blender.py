"""Dedicated hand diagnostics, isolated from timeline camera bindings."""
import hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from elias_hand_math import hands

SAMPLES=[(600,'left'),(640,'left'),(850,'left'),(1213,'right'),(1411,'left'),(2227,'left'),(2260,'right'),(2300,'left'),(2320,'right'),(2395,'right'),(2510,'left'),(2629,'right')]


def render(bpy,scene,state,layout,out):
    bindings=[(m,m.camera) for m in scene.timeline_markers];old_camera=scene.camera;old_frame=scene.frame_current
    old_path=scene.render.filepath;old_percentage=scene.render.resolution_percentage
    data=bpy.data.cameras.new('CAM_hand_review_verified');cam=bpy.data.objects.new('CAM_hand_review_verified',data);scene.collection.objects.link(cam);data.type='ORTHO'
    records=[];active=[]
    def guard(render_scene,*unused):
        if render_scene==scene:
            assert render_scene.camera==cam,'Timeline overrode hand review camera'
            active.append(render_scene.camera.name)
    try:
        for marker,_ in bindings:marker.camera=None
        bpy.app.handlers.render_pre.append(guard)
        scene.render.resolution_percentage=100
        for frame,side in SAMPLES:
            scene.frame_set(frame);bpy.context.view_layer.update();hand=hands(state(frame,layout))[side];center=Vector(hand['palm']['center'])
            # Frame the entire palm/digits and relevant prop, not just the wrist.
            points=[Vector(v) for chain in hand['chains'].values() for v in chain]
            palm=hand['palm']
            for x in (-1,1):
                for y in (-1,1):
                    for z in (-1,1):points.append(center+sum((Vector(palm['basis'][i])*palm['size'][i]*v/2 for i,v in enumerate((x,y,z))),Vector()))
            prefix='Drawer_front' if frame in (600,640,850) else 'SET_rear_wall_taps' if frame==1213 else 'Mug_' if frame in (1411,2510) else 'Key_' if frame in (2395,2629) else 'Envelope_' if frame in (2300,2320) else 'Letter_'
            deps=bpy.context.evaluated_depsgraph_get()
            for obj in scene.objects:
                if (obj.name.startswith(prefix) or (prefix=='Drawer_front' and obj.name=='Drawer_handle')) and obj.type=='MESH' and not obj.hide_render:
                    evaluated=obj.evaluated_get(deps);points.extend(evaluated.matrix_world@Vector(v) for v in evaluated.bound_box)
            target=sum(points,Vector())/len(points);visibility_trials=[]
            offset=Vector(state(frame,layout)['joints']['lateral'])*.65+Vector((0,0,.35)) if frame==2629 else Vector((.45,-.55,.40))
            if frame==1213:
                from mathutils.bvhtree import BVHTree
                vertices=[];triangles=[];owners=[]
                # Viewport scene.ray_cast includes hide_render objects. Build
                # explicit world-space render-visible geometry instead.
                excluded=[]
                for source_obj in scene.objects:
                    if source_obj.type!='MESH':continue
                    if source_obj.hide_render:excluded.append(source_obj.name);continue
                    evaluated=source_obj.evaluated_get(deps);mesh=evaluated.to_mesh()
                    try:
                        base=len(vertices);vertices.extend(evaluated.matrix_world@v.co for v in mesh.vertices);mesh.calc_loop_triangles()
                        for tri in mesh.loop_triangles:triangles.append(tuple(base+i for i in tri.vertices));owners.append(source_obj.name)
                    finally:evaluated.to_mesh_clear()
                bvh=BVHTree.FromPolygons(vertices,triangles,all_triangles=True)
                probes=[center]+[Vector(chain[-1]) for chain in hand['chains'].values()]
                for candidate in [(.8,0,.35),(-.8,0,.35),(.65,.65,.35),(.65,-.65,.35),(-.65,.65,.35),(-.65,-.65,.35),(0,.8,.5),(0,-.8,.5)]:
                    delta=Vector(candidate);visible=0;blockers=[]
                    for point in probes:
                        where,normal,index,distance=bvh.ray_cast(point+delta,-delta.normalized(),delta.length)
                        hit=where is not None
                        if not hit or (where-point).length<=.025:visible+=1
                        else:blockers.append({'object':owners[index],'distance_to_contact':(where-point).length})
                    visibility_trials.append({'offset':candidate,'visible_probes':visible,'total':len(probes),'blockers':blockers,'excluded_render_hidden':excluded})
                chosen=max(visibility_trials,key=lambda q:q['visible_probes'])
                assert chosen['visible_probes']>=4,'No shower diagnostic angle clears sufficient contact probes: '+str(visibility_trials)
                offset=Vector(chosen['offset'])
            cam.location=target+offset;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();data.ortho_scale=.48;scene.camera=cam
            bpy.context.view_layer.update()
            for _ in range(40):
                projected=[world_to_camera_view(scene,cam,p) for p in points]
                if all(.08<=p.x<=.92 and .08<=p.y<=.92 and p.z>0 for p in projected):break
                data.ortho_scale*=1.08
            else:raise RuntimeError(f'Hand/prop framing failed at {frame}')
            path=f'SC001_hand_{side}_{frame:04d}.png';scene.render.filepath=str(out/path);before=len(active);bpy.ops.render.render(write_still=True)
            assert len(active)==before+1,'Render camera guard did not run'
            assert scene.camera==cam,'Hand camera changed during render'
            records.append({'frame':frame,'side':side,'image':path,'render_camera':active[-1],'camera_location':list(cam.location),'target':list(target),'ortho_scale':data.ortho_scale,'containment_points':len(points),'containment_pass':True,'image_sha256':hashlib.sha256((out/path).read_bytes()).hexdigest(),'visibility_trials':visibility_trials,'occlusion_status':'sampled_shower_rays_checked_visual_review_pending' if visibility_trials else 'visual_review_pending'})
    finally:
        if guard in bpy.app.handlers.render_pre:bpy.app.handlers.render_pre.remove(guard)
        for marker,camera in bindings:marker.camera=camera
        scene.frame_set(old_frame);scene.camera=old_camera;scene.render.filepath=old_path;scene.render.resolution_percentage=old_percentage
        bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(data)
    return records
