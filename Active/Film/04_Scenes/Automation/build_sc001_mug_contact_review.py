"""Rebuild isolated mug snapshots or a bounded first-drink motion test."""
import argparse,hashlib,json,sys,uuid
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'Active/Film/03_Assets/Characters/Elias')]


def main():
    import bpy
    parser=argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--full-scene-review',action='store_true',help='Bake/validate all3168 frames and render sampled full-scene preview')
    modes.add_argument('--join-review',action='store_true',help='Four short boundary clips around integrated mug actions')
    modes.add_argument('--second-pickup',action='store_true',help='Second mug approach and pickup after letter pocketing')
    modes.add_argument('--contact-cycle',action='store_true',help='Approach, formed grip, table placement and release trial')
    modes.add_argument('--motion-preview',action='store_true',help='Bake first drink integer frames and render48 small motion images')
    opts=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    from elias_mug_contact import state,FRAMES,HANDLE,validate_mug_basis
    from elias_rig_blender import animate_and_validate
    from sc001_hand_review_blender import render
    from sc001_mug_motion_review import BAKE_FRAMES,START,END
    moving=opts.motion_preview or opts.contact_cycle or opts.second_pickup or opts.join_review or opts.full_scene_review
    if opts.contact_cycle:
        from elias_mug_lifecycle import state,START,END,BODY_DEPTH,BODY_CENTER_Z
        from sc001_mug_motion_review import cycle_schedule
        BAKE_FRAMES,_=cycle_schedule()
    if opts.second_pickup:
        from elias_mug_lifecycle import state
        from sc001_mug_motion_review import second_schedule
        BAKE_FRAMES,_=second_schedule();START,END=2430,2510
    if opts.join_review:
        from elias_mug_integration import state,WINDOWS
        BAKE_FRAMES=sorted({f for _,a,b in WINDOWS for f in range(a,b+1)});START,END=BAKE_FRAMES[0],BAKE_FRAMES[-1]
    if opts.full_scene_review:
        from elias_mug_integration import state
        BAKE_FRAMES=list(range(1,3169));START,END=1,3168
    frames=BAKE_FRAMES if moving else FRAMES
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
    out=local/(('sc001_integrated_' if opts.full_scene_review else 'mug_joins_' if opts.join_review else 'mug_second_' if opts.second_pickup else 'mug_cycle_' if opts.contact_cycle else 'mug_motion_' if moving else 'mug_')+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(exist_ok=False)
    report={'status':'mug_test_build_pending','source_blend':str(source),'scene_accepted':False,'limitations':['Six snapshots only; no continuous motion pass','Paper/dials/keys revisions queued separately','Role-based grip and articulated wrist; skin/contact pending visual review']}
    if moving:report['limitations'][0]='First-drink integer-frame bake only; approach/release and later carry excluded'
    # Resize only the copied diagnostic prop, using the same contract as pose checks.
    for name,position,size,angle in HANDLE:
        obj=scene.objects['Mug_handle_'+name];obj.rotation_euler=(0,0,0);obj.location=position;obj.dimensions=size;obj.rotation_euler=(0,angle,0)
    report['handle_geometry_metres']=HANDLE
    if opts.contact_cycle:
        body=scene.objects['Mug_body'];body.dimensions.z=BODY_DEPTH;body.location.z=BODY_CENTER_Z
        report['limitations'][0]='Bounded contact cycle; scene-boundary integration pending'
        report['mug_body_support_correction']={'depth_metres':BODY_DEPTH,'local_center_z':BODY_CENTER_Z}
    if opts.second_pickup:
        report['limitations'][0]='Second pickup only; table height/posture correction deferred; original mug body retained'
        report['deferred_layout_issue']='Original180 mm body/table retained;20 mm initial support gap not corrected or passed in this mode. Raise table and coordinate supported props/posture later.'
    if opts.join_review:report['limitations'][0]='Four disjoint boundary clips; no continuous full-scene Blender pass'
    if opts.full_scene_review:report['limitations'][0]='All integer-frame rig/mug readback; sampled renders only, no full-resolution final animation'
    from mathutils import Matrix,Vector
    # Reject singular/reflected target bases and Euler conversion errors before rig bake.
    conversion_error=0
    for frame in frames:
        basis=state(frame,layout)['_mug_basis'];validate_mug_basis(basis,frame)
        converted=Matrix(basis).transposed().to_euler().to_matrix()
        for axis in range(3):
            conversion_error=max(conversion_error,(converted.col[axis]-Vector(basis[axis])).length)
    assert conversion_error<1e-4,('Mug Euler preflight mismatch',conversion_error)
    report['mug_orientation_preflight']={'frames_checked':len(frames),'maximum_euler_basis_error':conversion_error}
    for frame in frames:
        scene.frame_set(frame);mug=scene.objects['PRP_CoffeeMug'];mug.rotation_euler=Matrix(state(frame,layout)['_mug_basis']).transposed().to_euler();mug.keyframe_insert(data_path='rotation_euler',frame=frame)
    report['rig']=animate_and_validate(bpy,scene,layout,state,3168,frames)
    # Preserve completed rig work even if a later prop readback fails.
    if opts.full_scene_review:
        scene.frame_start=START;scene.frame_end=END;scene.frame_set(1)
        report['rig']['coverage']='all_integer_frames'
        report['status']='rig_readback_passed_mug_readback_pending'
        bpy.ops.wm.save_as_mainfile(filepath=str(out/'SC001_integrated_rig_diagnostic.blend'))
        (out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print('SC001 RIG DIAGNOSTIC CHECKPOINT:',out,flush=True)
    if moving:
        report['rig']['coverage']='bounded_integer_frames';scene.frame_start=START;scene.frame_end=END;scene.render.fps=24
        from mathutils import Vector
        position_error=basis_error=0;basis_worst=None
        for frame in frames:
            scene.frame_set(frame);bpy.context.view_layer.update();target=state(frame,layout)
            actual=scene.objects['PRP_CoffeeMug'].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world
            position_error=max(position_error,(actual.translation-Vector(target['mug'])).length)
            for axis,planned in enumerate(target['_mug_basis']):
                error=(actual.to_3x3().col[axis].normalized()-Vector(planned)).length
                if error>basis_error:
                    basis_error=error;basis_worst={'frame':frame,'axis':axis,'actual':list(actual.to_3x3().col[axis].normalized()),'planned':list(planned)}
        assert position_error<1e-4,('Mug motion position mismatch',position_error)
        assert basis_error<1e-4,('Mug motion orientation mismatch',basis_error,basis_worst)
        report['mug_motion_readback']={'frames_checked':len(frames),'maximum_position_error_metres':position_error,'maximum_basis_vector_error':basis_error,'worst_orientation_sample':basis_worst}
        if opts.contact_cycle:
            support=[]
            for frame in (1375,1400,1540,1550,1560):
                scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
                def corners(name):
                    obj=scene.objects[name].evaluated_get(deps)
                    return [obj.matrix_world@Vector(p) for p in obj.bound_box]
                body=corners('Mug_body');table=corners('SET_table')
                gap=min(p.z for p in body)-max(p.z for p in table)
                assert abs(gap)<1e-4,('Mug/table support gap',frame,gap)
                support.append({'frame':frame,'vertical_gap_metres':gap})
            report['table_support_readback']=support
    if opts.contact_cycle or opts.second_pickup:report['contact_cycle']=[{'frame':f,**state(f,layout).get('_mug_lifecycle',{'phase':'held'})} for f in frames]
    if opts.full_scene_review:report['rig']['coverage']='all_integer_frames'
    if opts.join_review:
        report['rig']['coverage']='four_disjoint_boundary_windows';report['boundary_windows']=WINDOWS
        scene.frame_start=WINDOWS[0][1];scene.frame_end=WINDOWS[0][2]
    report['planned_contacts']=[state(f,layout)['_mug_contact_metrics'] for f in ([1400,1460,1539,1561,2450,2511,3168] if opts.full_scene_review else [1369,1375,1560,1561,1600,2429,2430,2510,2511] if opts.join_review else [2430,2440,2450,2480,2510] if opts.second_pickup else [1400,1411,1460,1500,1539] if moving else FRAMES)]
    report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'Active/Film/03_Assets/Characters/Elias/elias_mug_contact.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_hand_math.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_rig_math.py',Path(__file__).parent/'elias_rig_blender.py',Path(__file__).parent/'sc001_hand_review_blender.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_mug_integration.py',Path(__file__).parent/'sc001_full_scene_review.py',Path(__file__).parent/'sc001_preview.py',Path(__file__).parent/'sc001_mug_motion_review.py',ROOT/'Active/Film/03_Assets/Characters/Elias/elias_mug_lifecycle.py']}
    scene['rig_coverage']='ALL3168 INTEGER FRAMES; sampled full-scene review pending' if opts.full_scene_review else 'FOUR DISJOINT BOUNDARY CLIPS; no whole-scene validation' if opts.join_review else 'SECOND MUG PICKUP; whole-scene integration pending' if opts.second_pickup else 'BOUNDED CONTACT CYCLE; scene integration pending' if opts.contact_cycle else 'FIRST DRINK INTEGER FRAMES; approach/release excluded' if moving else 'SIX MUG SNAPSHOTS; not continuous animation';scene.frame_set(frames[0]);report['status']='mug_checkpoint_validated_render_pending'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/('SC001_integrated_rig_v0.1.blend' if opts.full_scene_review else 'SC001_mug_contact_test_v0.1.blend')));(out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('MUG CHECKPOINT:',out,flush=True)
    if moving:
        from sc001_mug_motion_review import render as render_motion
        if opts.full_scene_review:
            from sc001_full_scene_review import render as render_full
            report['full_scene_preview']=render_full(bpy,scene,state,layout,out)
        elif opts.join_review:
            report['boundary_previews']=[]
            for window in WINDOWS:
                folder=out/window[0];folder.mkdir(exist_ok=False)
                report['boundary_previews'].append({'folder':window[0],'preview':render_motion(bpy,scene,state,layout,folder,window=window)})
            report['contact_closeups']=render(bpy,scene,state,layout,out,[(f,'left') for f in (1374,1561,2429,2511)])
            links=''.join(f'<li><a href="{name}/motion_preview.html">{name}: source frames {a}–{b}</a></li>' for name,a,b in WINDOWS)
            (out/'review_index.html').write_text('<!doctype html><meta charset="utf-8"><title>SC001 mug joins</title><h1>SC001 mug joins</h1><p>Four separate boundary clips; full-scene Blender validation and table/posture correction remain pending.</p><ul>'+links+'</ul>',encoding='utf-8')
        else:report['motion_preview']=render_motion(bpy,scene,state,layout,out,contact_cycle=opts.contact_cycle,second_pickup=opts.second_pickup)
        if opts.second_pickup:report['contact_closeups']=render(bpy,scene,state,layout,out,[(f,'left') for f in (2430,2440,2450,2510)])
        if opts.contact_cycle:report['contact_closeups']=render(bpy,scene,state,layout,out,[(f,'left') for f in (1387,1399,1544,1550)])
        report['status']='sc001_integrated_all_frames_validated_visual_review_pending' if opts.full_scene_review else 'mug_join_review_validated_visual_review_pending' if opts.join_review else 'mug_second_pickup_validated_visual_review_pending' if opts.second_pickup else 'mug_contact_cycle_validated_visual_review_pending' if opts.contact_cycle else 'mug_bounded_motion_validated_visual_review_pending'
    else:
        samples=[(f,'left') for f in FRAMES];report['closeups']=render(bpy,scene,state,layout,out,samples);report['arm_views']=render(bpy,scene,state,layout,out,samples,arm_context=True)
        report['top_views']=render(bpy,scene,state,layout,out,[(1460,'left'),(2510,'left')],top_down=True)
        report['status']='mug_snapshot_rig_validated_visual_review_pending'
    (out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SC001 MUG OUTPUT:',out)

if __name__=='__main__':main()
