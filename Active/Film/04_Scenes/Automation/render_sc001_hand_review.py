"""Render corrected hand diagnostics from an existing rig .blend; never resave it."""
import hashlib,json,sys,uuid
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]


def main():
    import bpy
    from sc001_room_performance import state
    from sc001_hand_review_blender import render
    source=Path(bpy.data.filepath)
    if not bpy.app.background or not bpy.data.filepath:raise RuntimeError('Load the existing rig .blend in background mode')
    allowed=(ROOT/'Active/Film/_local/SC001').resolve()
    if not source.resolve().is_relative_to(allowed):raise RuntimeError('Source must be an SC001 local diagnostic build')
    scene=bpy.context.scene
    assert scene.objects.get('CHR_Elias_RIG') and scene.objects.get('CHR_Elias_SKIN'),'Weighted rig missing'
    baseline=json.loads((source.parent/'validation.json').read_text(encoding='utf-8'))
    def matches(path,digest):
        data=path.read_bytes().replace(b'\r\n',b'\n')
        return digest in [hashlib.sha256(data).hexdigest(),hashlib.sha256(data.replace(b'\n',b'\r\n')).hexdigest()]
    for path,digest in [(ROOT/'Active/Film/03_Assets/Characters/Elias/elias_hand_math.py',baseline['hand_math_sha256']),(ROOT/'Active/Film/03_Assets/Characters/Elias/elias_rig_math.py',baseline['rig_math_sha256']),(Path(__file__).parent/'sc001_room_performance.py',baseline['module_sha256']['sc001_room_performance.py'])]:
        assert matches(path,digest),'Loaded rig targets differ from current source: '+path.name
    layout_path=ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json'
    assert matches(layout_path,baseline['spec_sha256']),'Loaded layout differs'
    layout=json.loads(layout_path.read_text(encoding='utf-8'))
    out=allowed/('hands_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(exist_ok=False)
    records=render(bpy,scene,state,layout,out)
    report={'status':'camera_selection_and_containment_checked_visual_review_pending','source_blend':str(source),'source_validation_sha256':hashlib.sha256((source.parent/'validation.json').read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'hand_camera_records':records,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'camera_module_sha256':hashlib.sha256((Path(__file__).parent/'sc001_hand_review_blender.py').read_bytes()).hexdigest(),'source_resaved':False,'limitations':['Finger geometry unchanged to isolate camera failure','Containment does not prove visibility or contact','No scene acceptance']}
    (out/'hand_review_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SC001 HAND REVIEW OUTPUT:',out)

if __name__=='__main__':main()
