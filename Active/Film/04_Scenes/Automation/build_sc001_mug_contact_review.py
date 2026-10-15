"""Read existing scene, rebuild only experimental Elias rig for six mug poses."""
import hashlib,json,sys,uuid
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]


def main():
    import bpy
    from elias_mug_contact import state,FRAMES
    from elias_rig_blender import animate_and_validate
    from sc001_hand_review_blender import render
    if not bpy.app.background or not bpy.data.filepath:raise RuntimeError('Open existing SC001 checkpoint in background')
    source=Path(bpy.data.filepath);local=ROOT/'Active/Film/_local/SC001'
    assert source.resolve().is_relative_to(local.resolve()),'Use a local diagnostic SC001 checkpoint'
    baseline=json.loads((source.parent/'validation.json').read_text(encoding='utf-8'))
    def match(path,digest):
        b=path.read_bytes().replace(b'\r\n',b'\n');return digest in [hashlib.sha256(b).hexdigest(),hashlib.sha256(b.replace(b'\n',b'\r\n')).hexdigest()]
    layout_path=ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json'
    assert match(layout_path,baseline['spec_sha256']),'Layout changed'
    assert match(Path(__file__).parent/'sc001_room_performance.py',baseline['module_sha256']['sc001_room_performance.py']),'Source choreography changed'
    layout=json.loads(layout_path.read_text(encoding='utf-8'));scene=bpy.context.scene
    for obj in list(scene.objects):
        obj.select_set(False)
        if obj.name.startswith('CHR_Elias'):
            obj.hide_render=True;obj.name='BASELINE_'+obj.name
    out=local/('mug_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(exist_ok=False)
    report={'status':'mug_test_build_pending','source_blend':str(source),'scene_accepted':False,'limitations':['Six snapshots only; no continuous motion pass','Paper/dials/keys revisions queued separately','Fixed neutral wrist is a test hypothesis; grip skin/contact pending visual review']}
    from mathutils import Matrix
    for frame in FRAMES:
        scene.frame_set(frame);mug=scene.objects['PRP_CoffeeMug'];mug.rotation_euler=Matrix(state(frame,layout)['_mug_basis']).transposed().to_euler();mug.keyframe_insert(data_path='rotation_euler',frame=frame)
    report['rig']=animate_and_validate(bpy,scene,layout,state,3168,FRAMES)
    report['planned_contacts']=[state(f,layout)['_mug_contact_metrics'] for f in FRAMES]
    report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'Active/Film/03_Assets/Characters/Elias/elias_mug_contact.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_hand_math.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_rig_math.py',Path(__file__).parent/'elias_rig_blender.py',Path(__file__).parent/'sc001_hand_review_blender.py']}
    scene['rig_coverage']='SIX MUG SNAPSHOTS; not continuous animation';scene.frame_set(FRAMES[0]);report['status']='mug_checkpoint_validated_render_pending'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'SC001_mug_contact_test_v0.1.blend'));(out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('MUG CHECKPOINT:',out,flush=True)
    samples=[(f,'left') for f in FRAMES];report['closeups']=render(bpy,scene,state,layout,out,samples);report['arm_views']=render(bpy,scene,state,layout,out,samples,arm_context=True)
    report['status']='mug_snapshot_rig_validated_visual_review_pending';(out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SC001 MUG OUTPUT:',out)

if __name__=='__main__':main()
