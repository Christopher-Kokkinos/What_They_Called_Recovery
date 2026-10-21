"""Focused paper pickup/fold diagnostic from the original rig checkpoint."""
import sys,json,hashlib,uuid,math,argparse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]

def main():
    import bpy
    from mathutils import Vector,Matrix
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--envelope-review',action='store_true');parser.add_argument('--paper-sequence-review',action='store_true');parser.add_argument('--mug-paper-handover-review',action='store_true');parser.add_argument('--pocket-review',action='store_true');parser.add_argument('--inner-pocket-review',action='store_true');scope=parser.add_mutually_exclusive_group();scope.add_argument('--envelope-opening-only',action='store_true');scope.add_argument('--envelope-insertion-only',action='store_true');scope.add_argument('--envelope-finish-only',action='store_true')
    opts=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if opts.inner_pocket_review:
        if opts.pocket_review:parser.error('Choose one pocket mode')
        opts.pocket_review=True
    if opts.pocket_review:
        if opts.mug_paper_handover_review or opts.paper_sequence_review or opts.envelope_review or opts.envelope_opening_only or opts.envelope_insertion_only or opts.envelope_finish_only:parser.error('Pocket is a standalone mode')
        opts.envelope_review=True
    if opts.mug_paper_handover_review:
        if opts.paper_sequence_review or opts.envelope_review or opts.envelope_opening_only or opts.envelope_insertion_only or opts.envelope_finish_only:parser.error('Handover is a standalone mode')
        opts.envelope_review=True
    if opts.paper_sequence_review:
        if opts.envelope_review or opts.envelope_opening_only or opts.envelope_insertion_only or opts.envelope_finish_only:parser.error('Paper sequence is a standalone mode')
        opts.envelope_review=True
    if (opts.envelope_opening_only or opts.envelope_insertion_only or opts.envelope_finish_only) and not opts.envelope_review:parser.error('Envelope subset requires --envelope-review')
    if opts.envelope_review:
        from elias_envelope_contact import state,START,END
        from sc001_envelope_review_blender import key_geometry,validate as validate_envelope
        if opts.envelope_opening_only:END=2340
        if opts.envelope_insertion_only:START=2365
        if opts.envelope_finish_only:
            from elias_envelope_finish import state,START,END
    else:
        from elias_paper_contact import state,START,END
    if opts.paper_sequence_review:
        from elias_paper_refinement import state,START,END
    if opts.mug_paper_handover_review:
        from elias_table_handover import state,START,END,WINDOWS
    if opts.pocket_review:
        from elias_pocket import state,START,END
        from sc001_pocket_review_blender import create as create_pocket,validate as validate_pocket
    if opts.inner_pocket_review:
        from elias_inner_pocket import state,START,END
        from sc001_inner_pocket_blender import create as create_pocket,validate as validate_pocket,key_geometry as key_inner,custody
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
    out=local/(('inner_pocket_' if opts.inner_pocket_review else 'pocket_' if opts.pocket_review else 'table_handover_' if opts.mug_paper_handover_review else 'paper_sequence_' if opts.paper_sequence_review else 'envelope_finish_' if opts.envelope_finish_only else 'envelope_insert_' if opts.envelope_insertion_only else 'envelope_open_' if opts.envelope_opening_only else 'envelope_' if opts.envelope_review else 'paper_fold_')+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(exist_ok=False)
    for obj in list(scene.objects):
        obj.select_set(False)
        if obj.name.startswith('CHR_Elias'):obj.hide_render=True;obj.name='BASELINE_'+obj.name
    table=scene.objects['SET_table'];assert abs(table.location.z-.73)<1e-4,'Use original checkpoint table';table.location.z+=.20
    for name,position,size,angle in HANDLE:
        obj=scene.objects['Mug_handle_'+name];obj.rotation_euler=(0,0,0);obj.location=position;obj.dimensions=size;obj.rotation_euler=(0,angle,0)
    if opts.pocket_review:create_pocket(bpy,scene,state(START,layout))
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
            obj=scene.objects[name];obj.location=s[field];obj.rotation_euler=Matrix(s['_mug_basis']).transposed().to_euler() if field=='mug' else (math.pi/2,0,0) if field=='keys' else Matrix(s['_packet_basis_override']).transposed().to_euler() if '_packet_basis_override' in s else (s.get('_packet_rotation_x',0),0,0);obj.keyframe_insert(data_path='location',frame=f);obj.keyframe_insert(data_path='rotation_euler',frame=f)
        anchor=scene.objects['Envelope_text_anchor'];anchor.location=s['envelope'];anchor.rotation_euler=Matrix(s['_packet_basis_override']).transposed().to_euler() if '_packet_basis_override' in s else (s.get('_packet_rotation_x',0),0,0)
        anchor.keyframe_insert(data_path='location',frame=f);anchor.keyframe_insert(data_path='rotation_euler',frame=f)
        angle=math.pi*s['fold'];flap=scene.objects['Letter_fold'];flap.location=(0,.07425*math.cos(angle),.002+.07425*math.sin(angle));flap.rotation_euler=(angle,0,0)
        flap.keyframe_insert(data_path='location',frame=f);flap.keyframe_insert(data_path='rotation_euler',frame=f)
        text=scene.objects['Notice_exact_text'];text.hide_render=s.get('_notice_hidden',f>=2220);text.keyframe_insert(data_path='hide_render',frame=f)
        if opts.inner_pocket_review:key_inner(bpy,scene,s,f)
        if opts.envelope_review:key_geometry(scene,{**s,'_envelope_flap_angle':s.get('_envelope_flap_angle',0),'_envelope_mouth_angle':s.get('_envelope_mouth_angle',0)},f)
    linearise_owned_actions(owned)
    report={'status':'paper_fold_bake_pending','source_blend':str(source),'scene_accepted':False,
        'scope':'2161–2280: formed pinch, pickup, partial fold, release/regrip, closing fold',
        'limitations':['No reach-in/release or envelope insertion/pocketing yet','Not sheet or force simulation; full skin collisions require visual review','Approved mug clips unchanged; thigh contact remains non-blocking']}
    if opts.envelope_review:
        report.update(scope='2281–2474: left stabilises envelope; right opens flap, retrieves supported letter, inserts, releases',limitations=['Isolated stage; transitions from fold and pocketing not included','Proxy mouth/front deformation; not cloth or force simulation','No full skin collision certification'])
    if opts.envelope_opening_only:report['scope']='2281–2340: flap opening and transfer to parked letter only; insertion unchanged/excluded'
    if opts.envelope_insertion_only:report['scope']='2365–2474: insertion and slower withdrawal only; opening unchanged/excluded'
    if opts.envelope_finish_only:report.update(scope='2474–2654: closure, handover and provisional pocket approach/hold',limitations=['No cloth pocket or insertion/release certification; packet remains held at existing target','No adhesive simulation or full skin collision certification','Isolated diagnostic; full scene retiming pending'])
    if opts.paper_sequence_review:report.update(scope='2161–2720: continuous paper sequence with shorter regrip and direct flap transfer',limitations=['Starts with paper grip formed; clothing pocket insertion/release and full-scene timing pending','Parked envelope staged180mm closer for reachable pickup','No force simulation or full skin collision certification'])
    if opts.mug_paper_handover_review:report.update(scope='1500–2271: mug set-down, connected paper sequence and second pickup; only handover windows rendered',limitations=['Packet remains held in right hand; pocket insertion/release pending','Retimed diagnostic only; complete scene schedule not integrated','No full skin collision certification'])
    if opts.pocket_review:report.update(scope='2720–2940: align, insert to rigid pocket floor, release and withdraw',limitations=['Temporary open breast-pocket proxy; final garment/cloth absent','Standalone action, not integrated into mug/keys/departure timing','No complete skin collision certification'])
    if opts.inner_pocket_review:report.update(scope='Semantic frames1–70: off-hand lapel pull, bottom-first45-degree insertion, Child Of switch44, upward withdrawal and shape-key settling',limitations=['Standalone restaged two-hand blockout; previous mug/paper boundary not integrated','Controlled jacket patches and lining shape keys, not final clothing or cloth simulation','No complete skin/garment collision certification; envelope bend deferred'])
    report['rig']=animate_and_validate(bpy,scene,layout,state,END,list(range(START,END+1)))
    if opts.inner_pocket_review:report['custody']=custody(bpy,scene,state,layout)
    errors=[]
    for f in range(START,END+1):
        scene.frame_set(f);bpy.context.view_layer.update();s=state(f,layout);deps=bpy.context.evaluated_depsgraph_get()
        for field,name in names.items():
            obj=scene.objects[name].evaluated_get(deps);error=(obj.matrix_world.translation-Vector(s[field])).length
            assert error<1e-4,(f,name,error);errors.append(error)
        if opts.mug_paper_handover_review:
            actual=scene.objects['PRP_CoffeeMug'].evaluated_get(deps).matrix_world
            for axis,planned in enumerate(s['_mug_basis']):assert (actual.to_3x3().col[axis].normalized()-Vector(planned)).length<1e-4,(f,'Mug basis readback')
            if s['_mug_on_table']:
                def z_bounds(name):
                    obj=scene.objects[name].evaluated_get(deps);return [(obj.matrix_world@Vector(p)).z for p in obj.bound_box]
                assert abs(min(z_bounds('Mug_body'))-max(z_bounds('SET_table')))<1e-4,(f,'Mug/table support')
        assert abs(scene.objects['Letter_fold'].rotation_euler.x-math.pi*s['fold'])<1e-5
        if opts.pocket_review:errors.append(validate_pocket(bpy,scene,s,f))
        if opts.envelope_review and '_envelope_contacts' in s:
            errors.append(validate_envelope(bpy,scene,s,f));continue
        if '_paper_contacts' not in s:continue
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
        report['contact_phases']=[{'frame':f,'phase':state(f,layout).get('_sequence_phase',state(f,layout).get('_envelope_phase')),'paper_support':state(f,layout).get('_paper_support','hands'),'insertion_fraction':state(f,layout).get('_insertion',0)} for f in range(START,END+1)]
    if opts.paper_sequence_review:report['contact_surface_readback']='Fold/set-down pads checked against evaluated letter planes; active envelope/letter/flap grips checked against evaluated surfaces; free transfers excluded'
    if opts.mug_paper_handover_review:
        report['contact_surface_readback']='All772 rig/prop positions and mug orientations; table support while parked; paper/flap/envelope planes for declared active grips. Mug grip targets reused; no skin collision claim.'
        report['handover_phases']=[{'frame':f,'phase':state(f,layout)['_handover_phase'],'mug_on_table':state(f,layout)['_mug_on_table']} for f in range(START,END+1)]
        report['render_windows']=WINDOWS
    if opts.inner_pocket_review:
        report['contact_surface_readback']='Evaluated lapel point/pad gaps, lining bulge, finger targets, inner-pocket floor support and Child Of influence; free-hand phases excluded from contact claims'
        report['custody']['evaluated_readback']='all70 integer prop poses plus43/43.5/44/44.5 handoff checks passed'
    report['maximum_prop_or_pad_target_error_m']=max(errors)
    report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'Active/Film/03_Assets/Characters/Elias/elias_inner_pocket.py',Path(__file__).parent/'sc001_inner_pocket_blender.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_pocket.py',Path(__file__).parent/'sc001_pocket_review_blender.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_table_handover.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_paper_refinement.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_paper_sequence.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_envelope_finish.py',Path(__file__),ROOT/'Active/Film/03_Assets/Characters/Elias/elias_envelope_contact.py',Path(__file__).parent/'sc001_envelope_review_blender.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_paper_contact.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_table_reach.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_rig_math.py',Path(__file__).parent/'elias_rig_blender.py',Path(__file__).parent/'sc001_mug_motion_review.py']}
    scene.frame_start=START;scene.frame_end=END;scene.frame_set(START)
    report['status']='envelope_checkpoint_validated_render_pending' if opts.envelope_review else 'paper_fold_checkpoint_validated_render_pending'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/('SC001_inner_pocket_diagnostic.blend' if opts.inner_pocket_review else 'SC001_pocket_diagnostic.blend' if opts.pocket_review else 'SC001_table_handover_diagnostic.blend' if opts.mug_paper_handover_review else 'SC001_envelope_diagnostic.blend' if opts.envelope_review else 'SC001_paper_fold_diagnostic.blend')))
    def save():(out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    save();print('PAPER CHECKPOINT:',out,flush=True)
    report['previews']={}
    views=[('normal_context',False,()),('cutaway_contact',True,('Envelope_front','Envelope_flap','MAC_label'))] if opts.envelope_insertion_only else [('arm_context',False,()),('paper_contact',True,())]
    if opts.pocket_review:views=[('normal_context',False,()),('cutaway_contact',True,('REVIEW_Pocket_front',))]
    if opts.inner_pocket_review:views=[('normal_context',False,()),('cutaway_contact',True,('REVIEW_Jacket_lapel','REVIEW_InnerPocket_lining'))]
    default_window=('inner_pocket' if opts.inner_pocket_review else 'pocket_insert_release' if opts.pocket_review else 'paper_sequence' if opts.paper_sequence_review else 'envelope_finish_only' if opts.envelope_finish_only else 'envelope_insertion_only' if opts.envelope_insertion_only else 'envelope_opening_only' if opts.envelope_opening_only else 'envelope_open_insert' if opts.envelope_review else 'paper_pickup_fold',START,END)
    windows=WINDOWS if opts.mug_paper_handover_review else [default_window]
    for window in windows:
        for name,close,cutaway in views:
            name=window[0]+'_'+name if opts.mug_paper_handover_review else name
            folder=out/name;folder.mkdir(exist_ok=False)
            camera_options={}
            if opts.inner_pocket_review:
                from elias_inner_pocket import review_camera_offset
                camera_options=dict(camera_offset=review_camera_offset(state(35,layout),close),framing_prefixes=('Letter_','Envelope_','REVIEW_Jacket_','REVIEW_InnerPocket_'),minimum_packet_face_cosine=.8)
            report['previews'][name]=render(bpy,scene,state,layout,folder,window=window,paper_review=True,paper_closeup=close,cutaway_objects=cutaway,window_step=1 if opts.inner_pocket_review else 6 if opts.paper_sequence_review else 3,**camera_options)
            save()
    (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>SC001 paper pickup/fold</h1><p>Formed pinch through fold only. Insertion/pocketing pending.</p><ul><li><a href="arm_context/motion_preview.html">Arm context</a></li><li><a href="paper_contact/motion_preview.html">Paper contact</a></li></ul>',encoding='utf-8')
    if opts.envelope_review:
        index=out/'review_index.html';index.write_text(index.read_text().replace('SC001 paper pickup/fold','SC001 envelope opening/insertion').replace('Formed pinch through fold only. Insertion/pocketing pending.','Opening, pickup, insertion and release diagnostic. Pocketing and integrated timing pending.'))
    if opts.envelope_opening_only:
        index=out/'review_index.html';index.write_text(index.read_text().replace('SC001 envelope opening/insertion','SC001 envelope opening only').replace('Opening, pickup, insertion and release diagnostic. Pocketing and integrated timing pending.','Opening and transfer only. Insertion and pocketing excluded.'))
    if opts.envelope_insertion_only:
        (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>SC001 envelope insertion/withdrawal</h1><p>Normal view retains all geometry. Cutaway hides front, flap and label for inspection only. Pocketing/scene integration pending.</p><ul><li><a href="normal_context/motion_preview.html">Normal context</a></li><li><a href="cutaway_contact/motion_preview.html">Diagnostic cutaway contact</a></li></ul>',encoding='utf-8')
    if opts.envelope_finish_only:
        (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>Envelope closure and pocket approach</h1><p>Packet remains held at provisional pocket target. Clothing fit/release and full sequence pending.</p><a href="arm_context/motion_preview.html">Arm context</a> | <a href="paper_contact/motion_preview.html">Contact view</a>',encoding='utf-8')
    if opts.paper_sequence_review:
        (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>Continuous SC001 paper sequence</h1><p>Fold, table set-down, envelope pickup, insertion, closure and held pocket approach. Pocket release and full-scene timing pending.</p><a href="arm_context/motion_preview.html">Arm context</a> | <a href="paper_contact/motion_preview.html">Contact view</a>',encoding='utf-8')
    if opts.mug_paper_handover_review:
        links=''.join('<li><a href="'+name+'/motion_preview.html">'+name+'</a></li>' for name in report['previews'])
        (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>SC001 mug/paper handovers</h1><p>All772 poses validated; two handover windows rendered. Packet remains held, pocket release and complete scene timing pending.</p><ul>'+links+'</ul>',encoding='utf-8')
    if opts.pocket_review:
        (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>Pocket insertion and release</h1><p>Rigid proxy only. Normal view keeps all geometry; diagnostic cutaway hides pocket front only. Clothing and sequence integration pending.</p><a href="normal_context/motion_preview.html">Normal context</a> | <a href="cutaway_contact/motion_preview.html">Pocket cutaway</a>',encoding='utf-8')
    if opts.inner_pocket_review:
        (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><h1>Two-hand inner-pocket movement</h1><p>All70 semantic frames in both views. Child Of switches on44. Lapel and lining use controlled shape keys; cutaway hides those two patches only. Final clothing and integration pending.</p><a href="normal_context/motion_preview.html">Normal context</a> | <a href="cutaway_contact/motion_preview.html">Inner-pocket cutaway</a>',encoding='utf-8')
    report['status']='inner_pocket_validated_visual_review_pending' if opts.inner_pocket_review else 'pocket_validated_visual_review_pending' if opts.pocket_review else 'table_handover_validated_visual_review_pending' if opts.mug_paper_handover_review else 'paper_sequence_validated_visual_review_pending' if opts.paper_sequence_review else 'envelope_finish_validated_visual_review_pending' if opts.envelope_finish_only else 'envelope_insertion_validated_visual_review_pending' if opts.envelope_insertion_only else 'envelope_opening_validated_visual_review_pending' if opts.envelope_opening_only else 'envelope_validated_visual_review_pending' if opts.envelope_review else 'paper_fold_validated_visual_review_pending';save();print('SC001 PAPER OUTPUT:',out,flush=True)

if __name__=='__main__':main()
