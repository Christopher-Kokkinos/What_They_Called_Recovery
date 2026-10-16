"""Focused paper pickup/fold diagnostic from the original rig checkpoint."""
import sys,json,hashlib,uuid,math,argparse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]

def main():
    import bpy
    from mathutils import Vector,Matrix
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--envelope-review',action='store_true')
    opts=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if opts.envelope_review:
        from elias_envelope_contact import state,START,END
        from sc001_envelope_review_blender import key_geometry,validate as validate_envelope
    else:
        from elias_paper_contact import state,START,END
    from elias_mug_contact import HANDLE
    from elias_rig_blender import animate_and_validate
    from sc001_mug_motion_review import render
    from sc001_motion_blender import linearise_owned_actions
    assert bpy.app.background and bpy.data.filepath,'Open original rig checkpoint in background'
    source=Path(bpy.data.filepath);local=ROOT/'Active/Film/_local/SC001'
    assert source.resolve().is_relative_to(local.resolve())
    old=json.loads((source.parent/'validation.json').read_text(encoding='utf-8'))
    spec=ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json'
    def matches(path,digest):
        data=path.read_bytes().replace(b'\r\n',b'\n')
        return digest in (hashlib.sha256(data).hexdigest(),hashlib.sha256(data.replace(b'\n',b'\r\n')).hexdigest())
    assert matches(spec,old['spec_sha256']),'Layout checkpoint mismatch'
    assert matches(Path(__file__).parent/'sc001_room_performance.py',old['module_sha256']['sc001_room_performance.py']),'Source choreography checkpoint mismatch'
    layout=json.loads(spec.read_text());scene=bpy.context.scene
    out=local/(('envelope_' if opts.envelope_review else 'paper_fold_')+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(exist_ok=False)
    for obj in list(scene.objects):
        obj.select_set(False)
        if obj.name.startswith('CHR_Elias'):obj.hide_render=True;obj.name='BASELINE_'+obj.name
    table=scene.objects['SET_table'];assert abs(table.location.z-.73)<1e-4,'Use original checkpoint table';table.location.z+=.20
    for name,position,size,angle in HANDLE:
        obj=scene.objects['Mug_handle_'+name];obj.rotation_euler=(0,0,0);obj.location=position;obj.dimensions=size;obj.rotation_euler=(0,angle,0)
    names={'letter':'PRP_ResignationLetter','envelope':'PRP_MACEnvelope','mug':'PRP_CoffeeMug','keys':'PRP_Keys'}
    owned=[scene.objects[n] for n in names.values()]+[scene.objects[n] for n in ('Letter_fold','Envelope_text_anchor','Notice_exact_text')]
    if opts.envelope_review:
        owned.extend(obj for obj in scene.objects if obj.name.startswith(('Letter_','Envelope_')) or obj.name=='MAC_label')
    for f in range(START,END+1):
        scene.frame_set(f);s=state(f,layout)
        if opts.envelope_review:
            for obj in owned:
                obj.hide_render=False;obj.keyframe_insert(data_path='hide_render',frame=f)
        for field,name in names.items():
            obj=scene.objects[name];obj.location=s[field];obj.rotation_euler=Matrix(s['_mug_basis']).transposed().to_euler() if field=='mug' else (math.pi/2,0,0) if field=='keys' else (0,0,0);obj.keyframe_insert(data_path='location',frame=f);obj.keyframe_insert(data_path='rotation_euler',frame=f)
        anchor=scene.objects['Envelope_text_anchor'];anchor.location=s['envelope'];anchor.rotation_euler=(0,0,0)
        anchor.keyframe_insert(data_path='location',frame=f);anchor.keyframe_insert(data_path='rotation_euler',frame=f)
        angle=math.pi*s['fold'];flap=scene.objects['Letter_fold'];flap.location=(0,.07425*math.cos(angle),.002+.07425*math.sin(angle));flap.rotation_euler=(angle,0,0)
        flap.keyframe_insert(data_path='location',frame=f);flap.keyframe_insert(data_path='rotation_euler',frame=f)
        text=scene.objects['Notice_exact_text'];text.hide_render=f>=2220;text.keyframe_insert(data_path='hide_render',frame=f)
        if opts.envelope_review:key_geometry(scene,s,f)
    linearise_owned_actions(owned)
    report={'status':'paper_fold_bake_pending','source_blend':str(source),'scene_accepted':False,
        'scope':'2161–2280: formed pinch, pickup, partial fold, release/regrip, closing fold',
        'limitations':['No reach-in/release or envelope insertion/pocketing yet','Not sheet or force simulation; full skin collisions require visual review','Approved mug clips unchanged; thigh contact remains non-blocking']}
    if opts.envelope_review:
        report.update(scope='2281–2440: left stabilises envelope; right opens flap, retrieves supported letter, inserts, releases',limitations=['Isolated stage; transitions from fold and pocketing not included','Proxy mouth/front deformation; not cloth or force simulation','No full skin collision certification'])
    report['rig']=animate_and_validate(bpy,scene,layout,state,END,list(range(START,END+1)))
    errors=[]
    for f in range(START,END+1):
        scene.frame_set(f);bpy.context.view_layer.update();s=state(f,layout);deps=bpy.context.evaluated_depsgraph_get()
        for field,name in names.items():
            obj=scene.objects[name].evaluated_get(deps);error=(obj.matrix_world.translation-Vector(s[field])).length
            assert error<1e-4,(f,name,error);errors.append(error)
        assert abs(scene.objects['Letter_fold'].rotation_euler.x-math.pi*s['fold'])<1e-5
        if opts.envelope_review:
            errors.append(validate_envelope(bpy,scene,s,f));continue
        for side,suffix in [('left','L'),('right','R')]:
            contact=s['_paper_contacts'][side]
            surface=scene.objects['Letter_fold' if side=='left' else 'Letter_fixed'].evaluated_get(deps)
            local=Vector((-.105/.21,(.135-.07425)/.1485,0)) if side=='left' else Vector((.065/.21,(-.135+.07425)/.1485,0))
            plane=surface.matrix_world@local;normal=surface.matrix_world.to_3x3().col[2].normalized()
            assert (plane-Vector(contact['surface_contact'])).length<1e-4,(f,side,'Paper edge mapping')
            for digit in ('index','thumb'):
                actual=scene.objects['CHR_Elias_RIG'].matrix_world@scene.objects['CHR_Elias_RIG'].pose.bones[digit+'_3.'+suffix].tail
                error=(actual-Vector(contact[digit+'_tip'])).length
                assert error<1e-4,(f,side,digit,error);errors.append(error)
                if contact['active']:
                    signed=(actual-plane).dot(normal)*contact['surface_sign'];expected=.009 if digit=='index' else -contact['thumb_offset']
                    assert abs(signed-expected)<1e-4,(f,side,digit,'Paper pad clearance',signed)
    report['rig']['coverage']=f'all_integer_frames_in_{START}_{END}_only'
    report['contact_surface_readback']='Pad targets checked at all120 frames; sheet-plane clearance checked only for declared active grips. Right hand continuously supports sheet; fold pauses during left regrip'
    report['contact_phases']=[] if opts.envelope_review else [{'frame':f,'phase':state(f,layout)['_paper_phase'],'support_hands':state(f,layout)['_paper_support_hands'],'left_grip_active':state(f,layout)['_paper_contacts']['left']['active']} for f in range(START,END+1)]
    if opts.envelope_review:
        report['contact_surface_readback']='Active digit targets checked against evaluated flap/front/back/letter planes; free transfers excluded from contact claims'
        report['contact_phases']=[{'frame':f,'phase':state(f,layout)['_envelope_phase'],'paper_support':state(f,layout)['_paper_support'],'insertion_fraction':state(f,layout)['_insertion']} for f in range(START,END+1)]
    report['maximum_prop_or_pad_target_error_m']=max(errors)
    report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'Active/Film/03_Assets/Characters/Elias/elias_envelope_contact.py',Path(__file__).parent/'sc001_envelope_review_blender.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_paper_contact.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_table_reach.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_rig_math.py',Path(__file__).parent/'elias_rig_blender.py',Path(__file__).parent/'sc001_mug_motion_review.py']}
    scene.frame_start=START;scene.frame_end=END;scene.frame_set(START)
    report['status']='envelope_checkpoint_validated_render_pending' if opts.envelope_review else 'paper_fold_checkpoint_validated_render_pending'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/('SC001_envelope_diagnostic.blend' if opts.envelope_review else 'SC001_paper_fold_diagnostic.blend')))
    def save():(out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    save();print('PAPER CHECKPOINT:',out,flush=True)
    report['previews']={}
    for name,close in [('arm_context',False),('paper_contact',True)]:
        folder=out/name;folder.mkdir(exist_ok=False)
        report['previews'][name]=render(bpy,scene,state,layout,folder,window=('envelope_open_insert' if opts.envelope_review else 'paper_pickup_fold',START,END),paper_review=True,paper_closeup=close)
        save()
    (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>SC001 paper pickup/fold</h1><p>Formed pinch through fold only. Insertion/pocketing pending.</p><ul><li><a href="arm_context/motion_preview.html">Arm context</a></li><li><a href="paper_contact/motion_preview.html">Paper contact</a></li></ul>',encoding='utf-8')
    if opts.envelope_review:
        index=out/'review_index.html';index.write_text(index.read_text().replace('SC001 paper pickup/fold','SC001 envelope opening/insertion').replace('Formed pinch through fold only. Insertion/pocketing pending.','Opening, pickup, insertion and release diagnostic. Pocketing and integrated timing pending.'))
    report['status']='envelope_validated_visual_review_pending' if opts.envelope_review else 'paper_fold_validated_visual_review_pending';save();print('SC001 PAPER OUTPUT:',out,flush=True)

if __name__=='__main__':main()
