"""Independent reusable Elias armature/skin gallery. No scene proxy replacement."""
import argparse,hashlib,json,sys,uuid,math
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]


def main():
    sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]
    from sc001_room_performance import state
    from elias_rig_math import bones,skin,POSE_FRAMES
    import bpy
    from mathutils import Matrix,Vector
    from bpy_extras.object_utils import world_to_camera_view
    p=argparse.ArgumentParser();p.add_argument('--render-review',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if not bpy.app.background or bpy.data.filepath:raise RuntimeError('Use fresh --background --factory-startup')
    layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text(encoding='utf-8'))
    rest=state(889,layout);definition=bones(rest);surface=skin(rest)
    out=ROOT/'Active/Film/_local/Characters/Elias'/('rig_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(parents=True,exist_ok=False)
    scene=bpy.data.scenes.new('ELIAS_RIG_GALLERY_v0.1');bpy.context.window.scene=scene;scene.unit_settings.system='METRIC';scene.render.engine='BLENDER_WORKBENCH';scene.render.fps=1;scene.frame_start=1;scene.frame_end=len(POSE_FRAMES)
    scene.render.resolution_x=1280;scene.render.resolution_y=960;scene.render.resolution_percentage=100;scene.display.shading.color_type='MATERIAL';scene.display.shading.light='STUDIO';scene.render.film_transparent=False
    from elias_rig_blender import create
    rig,obj,definition=create(bpy,scene,rest)
    mesh=obj.data
    camera_data=bpy.data.cameras.new('Rig_review_camera');camera=bpy.data.objects.new('Rig_review_camera',camera_data);scene.collection.objects.link(camera);camera.location=(3.5,4.5,2.8);camera.rotation_euler=(Vector((0,0,1))-camera.location).to_track_quat('-Z','Y').to_euler();camera_data.type='ORTHO';camera_data.ortho_scale=4.0;scene.camera=camera
    report={'status':'rig_gallery_runtime_checks_pending','pose_sources':POSE_FRAMES,'bones':len(definition),'vertices':len(mesh.vertices),'faces':len(mesh.polygons),'poses':[],'limitations':['Neutral mannequin, not approved Elias appearance','Closed disconnected skin components; topology and skin weights provisional','Provisional articulated fingers; no IK, face, cloth or final grips','Gallery snapshots are not a continuous action'],'scene_accepted':False}
    max_error=0;max_scale_error=0
    def matrix(b):
        m=Matrix(b['basis']).transposed().to_4x4();m.translation=Vector(b['head']);return m
    for gallery_frame,source_frame in enumerate(POSE_FRAMES,1):
        scene.frame_set(gallery_frame);target=bones(state(source_frame,layout))
        for name,b in target.items():
            assert abs(b['length']-definition[name]['length'])<1e-8,'Bone length changed'
            pose=rig.pose.bones[name];pose.rotation_mode='QUATERNION';pose.matrix=matrix(b)
            for field in ['location','rotation_quaternion','scale']:pose.keyframe_insert(data_path=field,frame=gallery_frame)
            bpy.context.view_layer.update()
        bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();evaluated=rig.evaluated_get(deps)
        for name,b in target.items():
            pose=evaluated.pose.bones[name];max_error=max(max_error,(pose.head-Vector(b['head'])).length,(pose.tail-Vector(b['tail'])).length);max_scale_error=max(max_scale_error,*[abs(v-1) for v in pose.matrix.to_scale()])
        deformed=obj.evaluated_get(deps).to_mesh()
        assert len(deformed.vertices)==len(mesh.vertices),'Deformation changed topology unexpectedly'
        points=[obj.matrix_world@v.co for v in deformed.vertices];assert all(math.isfinite(v) for point in points for v in point)
        # Bounded constant camera fit; retain maximum scale across all gallery poses.
        for _ in range(20):
            projected=[world_to_camera_view(scene,camera,p) for p in points]
            if all(.06<=p.x<=.94 and .06<=p.y<=.94 and p.z>0 for p in projected):break
            camera_data.ortho_scale*=1.08
        else:raise RuntimeError('Rig gallery camera cannot contain deformed mesh')
        obj.evaluated_get(deps).to_mesh_clear()
        report['poses'].append({'gallery_frame':gallery_frame,'source_frame':source_frame,'bone_endpoints_checked':len(target),'mesh_vertices_finite':True})
    assert max_error<1e-4,f'Rig endpoint mismatch: {max_error}'
    assert max_scale_error<1e-4,f'Bone scale changed: {max_scale_error}'
    # Snapshot gallery deliberately holds poses instead of synthesising motion between them.
    action=rig.animation_data.action;curves=[]
    if getattr(action,'is_action_layered',False):
        for layer in action.layers:
            for strip in layer.strips:
                for bag in getattr(strip,'channelbags',()):curves.extend(bag.fcurves)
    else:curves.extend(action.fcurves)
    assert curves,'No rig animation curves found'
    for curve in curves:
        for point in curve.keyframe_points:point.interpolation='CONSTANT'
    if args.render_review:
        for gallery_frame,source_frame in enumerate(POSE_FRAMES,1):
            scene.frame_set(gallery_frame);scene.render.filepath=str(out/f'Elias_pose_{gallery_frame:02d}_source_{source_frame:04d}.png');bpy.ops.render.render(write_still=True)
    scene.frame_set(1);action.name='Elias_SC001_pose_gallery_v0.1';action.use_fake_user=True
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'Elias_rig_pose_gallery_v0.4.blend'))
    # Reusable asset starts neutral; gallery action is retained as a separate file.
    rig.animation_data.action=None
    for pose in rig.pose.bones:pose.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'CHR_Elias_rig_v0.4.blend'))
    report.update(status='evaluated_rig_gallery_validated_visual_review_pending',blender_version=bpy.app.version_string,maximum_endpoint_error=max_error,maximum_bone_scale_error=max_scale_error,camera_scale=camera_data.ortho_scale,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rig_math_sha256=hashlib.sha256((ROOT/'Active/Film/03_Assets/Characters/Elias/elias_rig_math.py').read_bytes()).hexdigest(),module_sha256={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in ['sc001_room_performance.py','elias_articulation.py']},layout_sha256=hashlib.sha256((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_bytes()).hexdigest())
    (out/'rig_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('ELIAS RIG OUTPUT:',out);print('RIG GALLERY VALIDATED; DEFORMATION VISUAL REVIEW PENDING')

if __name__=='__main__':main()
