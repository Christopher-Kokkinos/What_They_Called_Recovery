"""SC001 diagnostic blockout v0.23. Run only in a fresh background Blender.
No performance animation or final assets. Outputs are isolated and never reused.
"""
import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[4]
SPEC = ROOT / 'Active/Film/04_Scenes/SC001/SC001_layout_test_spec_v0.1.json'


def validate_spec(spec):
    assert spec['scene_id'] == 'SC001'
    assert spec['fps'] == 24 and spec['preview_resolution'] == [1280, 720]
    expected = spec['frame_start']
    ids = set()
    for shot in spec['shots']:
        assert shot['shot_id'] not in ids
        ids.add(shot['shot_id'])
        assert shot['frame_start'] == expected
        assert shot['frame_end'] >= expected
        expected = shot['frame_end'] + 1
    assert len(ids) == 10 and expected == spec['frame_end'] + 1
    assert (expected - spec['frame_start']) / spec['fps'] == spec['duration_seconds']
    source = ROOT / 'Active/Film/01_Adaptation/Screenplay/SC001_Elias_Apartment_draft.fountain'
    # Git on Windows can check text out with CRLF; authority hash uses LF.
    content = source.read_bytes().replace(b'\r\n', b'\n')
    assert hashlib.sha256(content).hexdigest() == spec['screenplay_sha256'], 'Screenplay changed; review specification first'


def select_review_shots(spec, render_stills=False, render_shot_review=False, render_targeted_review=False):
    if render_shot_review:
        return spec['shots']
    if render_targeted_review:
        return [s for s in spec['shots'] if s['shot_id'] in {'SC001_SH003','SC001_SH007'}]
    if render_stills:
        return [s for s in spec['shots'] if s['frame_start'] in {1, 889, 1561}]
    return []


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--render-stills', action='store_true')
    args.add_argument('--render-shot-review', action='store_true',
                      help='Render one labelled still per shot; supersedes --render-stills')
    args.add_argument('--render-bedside-preview',action='store_true',help='Sample SH002/SH003 only for bedside action review')
    args.add_argument('--render-motion-preview', action='store_true',
                      help='Render sampled 640x360 PNGs and local HTML player')
    args.add_argument('--render-targeted-review', action='store_true',
                      help='Render SH003 and SH007 only; all-ten mode takes precedence')
    options = args.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    spec = json.loads(SPEC.read_text(encoding='utf-8'))
    validate_spec(spec)
    import bpy
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from sc001_motion import sample_frames, preview_frames, shot_at, EVENTS, camera_radial
    from sc001_motion_blender import apply_motion
    from sc001_preview import write_viewer, evaluated_render_state
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    if not bpy.app.background or bpy.data.filepath:
        raise RuntimeError('Use --background --factory-startup; loaded production files are refused')
    out = ROOT / 'Active/Film/_local/SC001' / (datetime.now(timezone.utc).strftime('run_%Y%m%d_%H%M%S_') + uuid.uuid4().hex[:8])
    out.mkdir(parents=True, exist_ok=False)
    scene = bpy.data.scenes.new('SC001_BLOCKOUT_v0.23')
    bpy.context.window.scene = scene
    scene.unit_settings.system = 'METRIC'
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x, scene.render.resolution_y = spec['preview_resolution']
    scene.render.resolution_percentage = 100
    scene.render.fps = spec['fps']
    scene.frame_start, scene.frame_end = spec['frame_start'], spec['frame_end']
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.film_transparent = False
    scene.display.shading.background_type = 'VIEWPORT'
    scene.display.shading.background_color = (.12, .14, .16)
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'OBJECT'
    # Diagnostic text must not cast an offset duplicate onto the paper.
    # Final lighting/shadow direction remains governed by DEC-0021.
    scene.display.shading.show_shadows = False
    collections = {}
    for name in ['SET', 'CHARACTERS', 'PROPS', 'CAMERAS', 'LABELS']:
        col = bpy.data.collections.new('SC001_' + name)
        scene.collection.children.link(col)
        collections[name] = col

    def box(name, pos, size, group='PROPS', color=(.35, .32, .29, 1)):
        verts = [(x/2, y/2, z/2) for x, y, z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
        mesh = bpy.data.meshes.new(name + '_mesh')
        mesh.from_pydata(verts, [], [(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
        obj = bpy.data.objects.new(name, mesh)
        collections[group].objects.link(obj)
        obj.location = pos
        obj.scale = size
        obj.color = color
        return obj

    def label(name, body, pos, size=.12, flat=False):
        curve = bpy.data.curves.new(name, 'FONT')
        curve.body, curve.size = body, size
        obj = bpy.data.objects.new(name, curve)
        collections['LABELS'].objects.link(obj)
        obj.location = pos
        if not flat:
            obj.rotation_euler.x = math.pi / 2
        obj.color = (.08,.08,.08,1)
        return obj

    box('SET_EliasFlat_floor', (5,3.5,-.1), (10,7,.2), 'SET')
    # Cutaway layout: ceiling/front/partitions omitted for unobstructed diagnostic cameras.
    box('SET_EliasFlat_north_wall', (5,7.05,1.3), (10,.1,2.6), 'SET', (.55,.55,.52,1))
    from elias_articulation import BED_TOP_HEIGHT
    box('SET_EliasFlat_bed', (2,6,BED_TOP_HEIGHT/2), (1.5,2,BED_TOP_HEIGHT), 'SET')
    box('SET_EliasFlat_pillow',(2,6.75,BED_TOP_HEIGHT+.05),(.85,.35,.10),'SET')
    # Hollow low bedside carcass: back flush with north wall, aligned with pillow.
    for suffix,pos,size in [('left',(2.91,6.6,.375),(.04,.8,.75)),('right',(3.59,6.6,.375),(.04,.8,.75)),('back',(3.25,6.98,.375),(.7,.04,.75)),('top',(3.25,6.6,.73),(.7,.8,.04)),('bottom',(3.25,6.6,.02),(.7,.8,.04)),('lower_front',(3.25,6.20,.18),(.62,.04,.28))]:
        box('SET_EliasFlat_bedside_'+suffix,pos,size,'SET')
    box('SET_EliasFlat_fake_fireplace', (4.4,6.7,.5), (1.2,.4,1), 'SET')
    # Hollow frame: the v0.1 solid slab hid the outside pigeon proxies.
    for side, pos, size in [
        ('lower', (0,4.5,.75), (.08,1.8,.08)),
        ('upper', (0,4.5,2.05), (.08,1.8,.08)),
        ('left', (0,3.6,1.4), (.08,.08,1.3)),
        ('right', (0,5.4,1.4), (.08,.08,1.3)),
    ]:
        box('SET_EliasFlat_window_frame_' + side, pos, size, 'SET')
    box('SET_EliasFlat_outside_ledge', (-.35,4.5,.9), (.7,1.8,.12), 'SET')
    from sc001_entry import build as build_entry
    entry_parts=build_entry(box)
    box('SET_EliasFlat_kitchen_counter', (6,5.8,.5), (2.8,.8,1), 'SET')
    box('PRP_AlarmClock', (3.25,6.6,.90), (.5,.12,.28))
    label('Clock_display', '08:00  ALARM OFF', (3.01,6.52,.90), .055)
    box('PRP_PrescriptionStrip', (3.25,6.05,.54), (.52,.35,.02), color=(.75,.75,.72,1))
    label('Prescription_label', 'OXYCODONE', (3.09,6.13,.56), .042, True)
    for i in range(8):
        box('Prescription_cell_%02d' % i, (3.04+(i%4)*.13,5.94+(i//4)*.09,.57), (.08,.06,.015), color=((.12,.12,.12,1) if i < 2 else (.85,.82,.7,1)))
    box('PRP_TorchTools', (6.8,5.8,1.035), (.65,.3,.03))
    box('PRP_Torch_body', (6.65,5.8,1.09), (.28,.08,.08), color=(.18,.2,.22,1))
    box('PRP_Torch_head', (6.47,5.8,1.09), (.1,.13,.13), color=(.3,.32,.33,1))
    for n in range(2):
        box('PRP_Tool_%d' % n, (6.9,5.73+n*.14,1.07), (.2,.045,.035))
    box('PRP_ClothesPost', (4.2,4.8,.08), (.65,.5,.16), color=(.38,.3,.24,1))
    for n in range(3):
        obj = box('PRP_Clothes_layer_%d' % n, (4.2+n*.06,4.8,.19+n*.05), (.55,.32,.07), color=(.35,.31+n*.03,.32,1))
        obj.rotation_euler.z = (n-1)*.3
    for n in range(2):
        obj = box('PRP_Post_sheet_%d' % n, (4.1+n*.22,4.5,.015+n*.012), (.25,.18,.01), color=(.8,.78,.7,1))
        obj.rotation_euler.z = n*.35
    box('SET_EliasFlat_bathroom_floor', (9,5,.015), (1.9,3.8,.03), 'SET', (.43,.47,.48,1))
    box('SET_EliasFlat_bathroom_threshold', (9,3.1,.06), (1.9,.12,.12), 'SET')
    box('SET_EliasFlat_bathroom_jamb', (8,3.1,1.25), (.1,.12,2.5), 'SET')
    box('PRP_ShowerFixture', (9,6,1.85), (.25,.25,.12))
    box('PRP_Shower_pipe', (9,6.05,1.3), (.035,.035,1))
    box('PRP_Shower_control', (9,5.99,1.1), (.2,.05,.1))
    # Hollow procedural cup with rim, bottom and a simple box handle.
    count, radius, height = 24, .1, .22
    verts = [(r*math.cos(2*math.pi*i/count), r*math.sin(2*math.pi*i/count), z)
             for r,z in [(radius,0),(radius,height),(radius*.78,height),(radius*.78,.025)]
             for i in range(count)]
    faces = []
    for a,b in [(0,1),(1,2),(2,3)]:
        for i in range(count):
            j=(i+1)%count
            faces.append((a*count+i,a*count+j,b*count+j,b*count+i))
    faces.append(tuple(range(3*count,4*count)))
    mesh=bpy.data.meshes.new('PRP_CoffeeMug_mesh'); mesh.from_pydata(verts,[],faces)
    mug=bpy.data.objects.new('PRP_CoffeeMug',mesh); collections['PROPS'].objects.link(mug)
    mug.location=(4.8,4.65,1.02); mug.color=(.65,.64,.59,1)
    for suffix,pos,size in [('top',(4.94,4.65,1.19),(.12,.035,.03)),('side',(4.99,4.65,1.13),(.035,.035,.13)),('bottom',(4.94,4.65,1.065),(.12,.035,.03))]:
        box('PRP_Mug_handle_'+suffix,pos,size,color=(.65,.64,.59,1))
    box('PRP_Keys', (6.9,5.6,1.035), (.06,.11,.015), color=(.7,.68,.55,1))
    for i in range(2):
        box('PRP_Key_shaft_%d' % i, (6.9+i*.06,5.48,1.035), (.025,.17,.015), color=(.7,.68,.55,1))
        box('PRP_Key_tooth_%d' % i, (6.925+i*.06,5.41,1.035), (.06,.025,.015), color=(.7,.68,.55,1))
    for obj in collections['PROPS'].objects:
        if obj.name=='PRP_Keys' or obj.name.startswith('PRP_Key_'):
            obj.location += Vector((.15,-1.18,0))
    box('SET_EliasFlat_coffee_surface',(5.1,4.7,.99),(.9,.55,.04),'SET')
    box('SET_EliasFlat_handling_surface',(6.7,4.40,.99),(1.15,.55,.04),'SET')
    box('PRP_EliasJacket', (7.6,5.4,1.1), (.5,.12,.8))
    box('PRP_MACEnvelope', (6.2,5.5,1.015), (.22,.11,.004), color=(.9,.9,.86,1))
    label('Envelope_label', 'MAC', (6.13,5.5,1.02), .018, True)
    box('PRP_ResignationLetter', (5.9,5.3,1.03), (.210,.297,.002), color=(.92,.9,.85,1))
    label('Notice_exact_text', 'I will complete work\nalready accepted.\nI will not take further\nassignments after Friday.\nPlease arrange final\npayment.', (5.805,5.41,1.033), .015, True)
    pigeon = box('CHR_Pigeon_A', (-.35,4.2,1.05), (.2,.35,.22), 'CHARACTERS')
    second = bpy.data.objects.new('CHR_Pigeon_B', pigeon.data)
    collections['CHARACTERS'].objects.link(second)
    second.location, second.scale = (-.35,4.8,1.05), pigeon.scale.copy()
    second.color = pigeon.color
    root = bpy.data.objects.new('CHR_Elias_proxy_root', None)
    collections['CHARACTERS'].objects.link(root)
    for name, pos, size in [('torso',(0,0,1.1),(.45,.25,.7)),('head',(0,0,1.65),(.25,.25,.3)),('left_thigh',(-.12,0,.59),(.18,.22,.38)),('right_thigh',(.12,0,.59),(.18,.22,.38)),('left_calf',(-.12,0,.2),(.18,.22,.4)),('right_calf',(.12,0,.2),(.18,.22,.4)),('right_arm',(.32,0,1.1),(.15,.18,.65)),('left_arm',(-.32,0,1.1),(.15,.18,.65))]:
        obj = box('CHR_Elias_' + name, pos, size, 'CHARACTERS', (.27,.32,.36,1))
        obj.parent = root
    for side,x in [('left',-.12),('right',.12)]:
        obj=box('CHR_Elias_'+side+'_foot',(x,-.05,.05),(.18,.22,.10),'CHARACTERS',(.27,.32,.36,1));obj.parent=root
    # Discrete staging only. No claim to sleeping/pain/letter/mug performance.
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'CONSTANT'
    placements = [(2,4.85,.85),(2,2.87,0),(2,2.87,0),(5,4.6,0),(9,5,0),(5.1,5,0),(5.1,5,0),(6.7,4.7,0),(1.2,4.5,0),(7.5,-1,0)]
    cameras = [((3,1,2.3),(0.9,4.6,1.2),28),((4.8,4.4,1.9),(2.8,5.8,1.1),45),((3.25,3.3,2.1),(3.25,6.05,.54),55),((6,1.3,2.2),(6,5.5,1),32),((8,3.6,1.9),(9,6,1.3),40),((7.8,3.4,2.1),(5.5,5.6,1.1),40),((6,5.3,2.4),(6,5.3,1.03),48),((6.3,2.3,3.8),(6.4,4.5,1.2),35),((2.8,3,1.8),(.1,4.5,1.2),35),((3,1,2.3),(0.9,4.6,1.2),28)]
    defaults = {obj.name:(obj.location.copy(),obj.scale.copy()) for obj in root.children}
    pose_checks = []
    def stage_pose(index, frame):
        root.location = placements[index]
        root.rotation_euler = (math.pi/2,0,0) if index == 0 else (0,0,0)
        for obj in root.children:
            obj.location, obj.scale = defaults[obj.name]
            if index in (1,2):
                if 'thigh' in obj.name:
                    obj.location.y, obj.location.z = -.25, .69
                    obj.scale = (.18,.6,.18)
                elif 'calf' in obj.name:
                    obj.location.y, obj.location.z = -.5,.32
                    obj.scale = (.18,.18,.64)
                elif obj.name.endswith('right_arm'):
                    obj.location = (-.04,-.22,1.0)
                    obj.scale = (.43,.15,.16)
            obj.keyframe_insert(data_path='location',frame=frame)
            obj.keyframe_insert(data_path='scale',frame=frame)
        root.keyframe_insert(data_path='location',frame=frame)
        root.keyframe_insert(data_path='rotation_euler',frame=frame)

    for index, (shot, pos, (eye, target, lens)) in enumerate(zip(spec['shots'], placements, cameras)):
        stage_pose(index,shot['frame_start'])
        pose_checks.append({'shot':shot['shot_id'], 'pose':'lying' if index==0 else ('seated_support_proxy' if index in (1,2) else 'standing'), 'position':list(pos)})
        data = bpy.data.cameras.new(shot['shot_id'])
        data.lens, data.clip_start, data.clip_end = lens, .05, 100
        cam = bpy.data.objects.new(shot['shot_id'], data)
        collections['CAMERAS'].objects.link(cam)
        cam.location = eye
        cam.rotation_euler = (Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        marker = scene.timeline_markers.new(shot['shot_id'], frame=shot['frame_start'])
        marker.camera = cam
    # Blender layered actions vary by version: insert duplicate holds before next cut
    # so interpolation cannot move the mannequin through a shot.
    for i, shot in enumerate(spec['shots']):
        stage_pose(i,shot['frame_end'])
    for obj in scene.objects:
        if obj.name.startswith(('SET_EliasFlat_bedside_','Prescription_cell_')) or obj.name in {'PRP_AlarmClock','Clock_display','PRP_PrescriptionStrip','Prescription_label'}:
            obj.location.x += .25
    motion = apply_motion(bpy,scene,root,defaults,spec,box)
    from sc001_articulation_blender import apply as apply_articulation
    motion['articulation'] = apply_articulation(bpy,scene,root,spec,box)
    from sc001_entry import validate as validate_entry
    motion['entry_geometry']=validate_entry(bpy,scene)
    pose_checks = []
    for shot in spec["shots"]:
        scene.frame_set(shot["frame_start"])
        bpy.context.view_layer.update()
        pose_checks.append({"shot":shot["shot_id"], "frame":shot["frame_start"], "position":list(root.matrix_world.translation), "rotation":list(root.rotation_euler), "status":"evaluated_coarse_pose"})
    # Fit diagnostic subjects from their actual bounds, including evaluated text.
    # This tests containment, not occlusion or legibility; still review is mandatory.
    framing_checks = []
    upper = ['CHR_Elias_head','CHR_Elias_torso','CHR_Elias_left_arm','CHR_Elias_right_arm','CHR_Elias_left_forearm','CHR_Elias_right_forearm','CHR_Elias_left_palm','CHR_Elias_right_palm']
    subjects = {
        0: ['SET_EliasFlat_bed', 'CHR_Pigeon_A', 'CHR_Pigeon_B', 'Clock_display'] + [o.name for o in root.children],
        1: upper,
        2: ['PRP_PrescriptionStrip','Prescription_label'] + ['Prescription_cell_%02d' % i for i in range(8)],
        3: ['SET_EliasFlat_kitchen_counter', 'PRP_TorchTools', 'PRP_ClothesPost'] + [o.name for o in collections['PROPS'].objects if o.name.startswith(('PRP_Clothes_','PRP_Post_','PRP_Torch_','PRP_Tool_'))] + [o.name for o in root.children],
        4: upper + ['PRP_ShowerFixture','PRP_Shower_control'],
        5: upper + ['PRP_CoffeeMug'] + [o.name for o in collections['PROPS'].objects if o.name.startswith('PRP_Mug_handle_')],
        6: ['PRP_LetterFold_-1','PRP_LetterFold_1','PRP_ResignationLetter', 'Notice_exact_text'],
        7: upper + ['PRP_LetterFold_-1','PRP_LetterFold_1','PRP_Keys','PRP_CoffeeMug','PRP_ResignationLetter','PRP_MACEnvelope'] + [o.name for o in collections['PROPS'].objects if o.name.startswith('PRP_Key_')],
        8: upper + ['CHR_Pigeon_A','CHR_Pigeon_B'],
        9: ['SET_EliasFlat_bed', 'CHR_Pigeon_A', 'CHR_Pigeon_B', 'Clock_display'],
    }
    for index, names in subjects.items():
        shot=spec['shots'][index]
        check_frames=sorted({shot['frame_start'],shot['frame_end'],
                             *[f for f in sample_frames(spec) if shot['frame_start']<=f<=shot['frame_end']]})
        points=[]
        for check_frame in check_frames:
            scene.frame_set(check_frame)
            bpy.context.view_layer.update()
            deps=bpy.context.evaluated_depsgraph_get()
            for name in names:
                original=scene.objects[name]
                if original.hide_render:
                    continue
                obj=original.evaluated_get(deps)
                points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
        center = sum(points, Vector()) / len(points)
        cam = scene.objects[spec['shots'][index]['shot_id']]
        if index == 2:
            # Approach from the free (+X) bedside side, above drawer height.
            cam.location = center + Vector((.85,.55,1.6))
            cam.data.type = 'ORTHO'
            cam.data.ortho_scale = .75
        elif index == 6:
            # Top-down insert remains a diagnostic view, not final hand performance.
            cam.data.type = 'ORTHO'
            cam.data.ortho_scale = .34
            cam.location = center + Vector((0,0,2))
        else:
            direction = (cam.location - center).normalized()
            cam.location = center + direction * max((cam.location-center).length, 2)
        cam.rotation_euler = (center-cam.location).to_track_quat('-Z','Y').to_euler()
        for attempt in range(80):
            bpy.context.view_layer.update()
            projected = [world_to_camera_view(scene, cam, point) for point in points]
            if all(.06 <= p.x <= .94 and .06 <= p.y <= .94 and p.z > 0 for p in projected):
                break
            if cam.data.type == 'ORTHO':
                cam.data.ortho_scale *= 1.08
            else:
                cam.location = center + (cam.location-center) * 1.08
        else:
            raise RuntimeError('Could not safely frame ' + cam.name)
        framing_checks.append({'shot':cam.name, 'subjects':names, 'margin':.06,
                               'containment_passed':True, 'camera_type':cam.data.type,
                               'sample_frames':check_frames, 'position':list(cam.location), 'ortho_scale':cam.data.ortho_scale})
    from sc001_bedside_camera import configure
    motion.update(configure(bpy,scene,scene.objects['SC001_SH003']))
    framing_checks[2]['containment_passed']=None
    framing_checks[2]['status']='radial_motion_camera_sampled_occlusion_checks_visual_review_pending'
    from sc001_departure_camera import configure as configure_departure
    motion['departure_camera']=configure_departure(bpy,scene,scene.objects['SC001_SH010'])
    framing_checks[9]={'shot':'SC001_SH010','status':'tracking_and_pigeon_cutaway','containment_passed':True,'checked_frames':motion['departure_camera']['checked_frames']}
    scene.camera = scene.objects['SC001_SH001']
    scene.frame_set(1)
    assert len(framing_checks) == len(spec['shots'])
    assert len(pose_checks) == len(spec['shots'])
    assert scene.render.fps == spec['fps']
    assert (scene.frame_start, scene.frame_end) == (spec['frame_start'], spec['frame_end'])
    assert [scene.render.resolution_x, scene.render.resolution_y] == spec['preview_resolution']
    required = ['PRP_AlarmClock', 'PRP_PrescriptionStrip', 'PRP_TorchTools', 'PRP_ClothesPost', 'PRP_ShowerFixture', 'PRP_CoffeeMug', 'PRP_Keys', 'PRP_EliasJacket', 'PRP_MACEnvelope', 'PRP_ResignationLetter', 'CHR_Elias_proxy_root']
    assert all(name in scene.objects for name in required)
    assert len(collections['CAMERAS'].objects) == 10
    assert len(scene.timeline_markers) == 10
    assert all(m.camera and m.frame == s['frame_start'] for m,s in zip(scene.timeline_markers, spec['shots']))
    assert len([o for o in collections['CHARACTERS'].objects if o.name.startswith('CHR_Pigeon_')]) == 2
    # Actual evaluated read-back of final custody positions (not hand-contact QA).
    scene.frame_set(spec['frame_end']);bpy.context.view_layer.update()
    final_root=root.matrix_world.translation
    from sc001_motion import POCKET_OFFSET, CARRIED_KEYS_OFFSET, CARRIED_MUG_OFFSET, pocket_position
    for name,offset in [('PRP_ResignationLetter',POCKET_OFFSET),('PRP_MACEnvelope',POCKET_OFFSET),('PRP_Keys',CARRIED_KEYS_OFFSET),('PRP_CoffeeMug',CARRIED_MUG_OFFSET)]:
        actual=scene.objects[name].matrix_world.translation
        expected=Vector(pocket_position(spec['frame_end'])) if name in {'PRP_ResignationLetter','PRP_MACEnvelope'} else final_root+Vector(offset)
        assert (actual-expected).length<.001, 'Final custody mismatch: '+name
    assert scene.objects['PRP_PrescriptionStrip'].hide_render
    motion['final_custody_readback']='PASS'
    scene.frame_set(1);scene.camera=scene.objects['SC001_SH001']
    blend = out / 'SC001_blockout_v0.23.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend), check_existing=True)
    assert blend.is_file() and blend.stat().st_size > 0
    report = {'status':'structure_validated_visual_review_pending', 'blender_version':bpy.app.version_string, 'spec_sha256':hashlib.sha256(SPEC.read_bytes()).hexdigest(), 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'blend':str(blend), 'engine':scene.render.engine, 'motion':motion, 'pose_checks':pose_checks, 'framing_checks':framing_checks, 'cameras':len(collections['CAMERAS'].objects), 'objects':len(scene.objects), 'fps':scene.render.fps, 'frames':[scene.frame_start,scene.frame_end], 'resolution':[scene.render.resolution_x,scene.render.resolution_y], 'stills':[], 'limitations':['Coarse linear box motion, no final performance','Hinged paper and drawer motion remain coarse proxies','No final lighting, grain, audio, materials or rigs','Camera readability and wall geometry require visual review']}
    review_shots = select_review_shots(spec, options.render_stills, options.render_shot_review, options.render_targeted_review)
    report['review_mode'] = 'all_ten_shots' if options.render_shot_review else ('targeted_sh003_sh007' if options.render_targeted_review else ('three_stills' if options.render_stills else 'build_only'))
    report['builder_version'] = '0.23'
    report['diagnostic_shadows'] = scene.display.shading.show_shadows
    report['shot_review'] = []
    report['render_evaluation'] = {'stills':[], 'preview_shot_starts':[], 'window_preview':[], 'departure_preview':[]}
    still_states={}
    if review_shots:
        for shot in review_shots:
            frame = shot['frame_start']
            scene.frame_set(frame)
            scene.camera = scene.objects[shot['shot_id']]
            state=evaluated_render_state(bpy,scene)
            still_states[frame]=state
            report['render_evaluation']['stills'].append(state)
            filename = (shot['shot_id'] + '_frame_%04d.png' % frame) if (options.render_shot_review or options.render_targeted_review) else ('frame_%04d.png' % frame)
            scene.render.filepath = str(out / filename)
            bpy.ops.render.render(write_still=True, scene=scene.name)
            assert Path(scene.render.filepath).is_file()
            report['stills'].append(scene.render.filepath)
            report['shot_review'].append({'shot_id':shot['shot_id'], 'beat_id':shot['beat_id'],
                                         'frame':frame, 'camera':scene.camera.name,
                                         'review_check':shot['review_check'], 'image':scene.render.filepath})
        assert len(report['stills']) == len(review_shots)
    if options.render_shot_review:
        report['departure_phase_review']=[]
        for frame in [2840,2841,2860]:
            scene.frame_set(frame);scene.camera=scene.objects['SC001_SH010']
            state=evaluated_render_state(bpy,scene)
            filename='SC001_SH010_phase_frame_%04d.png'%frame
            scene.render.filepath=str(out/filename)
            bpy.ops.render.render(write_still=True,scene=scene.name)
            assert (out/filename).is_file()
            report['departure_phase_review'].append({'frame':frame,'image':str(out/filename),'state':state})
    report['module_sha256']={name:hashlib.sha256((Path(__file__).resolve().parent/name).read_bytes()).hexdigest() for name in ['sc001_motion.py','sc001_motion_blender.py','sc001_preview.py','sc001_bedside_camera.py','elias_articulation.py','sc001_articulation_blender.py','sc001_standing.py','sc001_departure_camera.py','sc001_entry.py']}
    if options.render_motion_preview or options.render_bedside_preview:
        preview_dir=out/'motion_frames';preview_dir.mkdir(exist_ok=False)
        entries=[]
        try:
            scene.render.resolution_x,scene.render.resolution_y=640,360
            selected_frames=preview_frames(spec) if options.render_motion_preview else [f for f in preview_frames(spec) if 361<=f<=888]
            for number,frame in enumerate(selected_frames):
                shot=shot_at(spec,frame);scene.frame_set(frame);scene.camera=scene.objects[shot['shot_id']]
                state=evaluated_render_state(bpy,scene)
                if frame==shot['frame_start']:
                    report['render_evaluation']['preview_shot_starts'].append(state)
                    if frame in still_states:
                        reference=still_states[frame]
                        difference=max(abs(a-b) for field in ['camera_matrix','head_matrix','head_bounds_ndc'] for a,b in zip(reference[field],state[field]))
                        state['still_difference']=difference
                        state['still_state_matches']=difference<1e-5 and reference['lens']==state['lens'] and reference['camera']==state['camera']
                if shot['shot_id']=='SC001_SH009':
                    report['render_evaluation']['window_preview'].append(state)
                if shot['shot_id']=='SC001_SH010':
                    state['phase']='departure' if frame<motion['departure_camera']['closing_cut'] else 'pigeons'
                    report['render_evaluation']['departure_preview'].append(state)
                filename='motion_frames/frame_%04d.png'%number
                scene.render.filepath=str(out/filename)
                bpy.ops.render.render(write_still=True,scene=scene.name)
                assert (out/filename).is_file()
                cues=[e['event'] for e in EVENTS if e['frame']<=frame]
                entries.append({'frame':frame,'shot':shot['shot_id'],'image':filename,'cue':cues[-1] if cues else 'morning hold'})
                if number%40==0:print('SC001 MOTION PREVIEW',number,'/',len(selected_frames),flush=True)
        finally:
            scene.render.resolution_x,scene.render.resolution_y=spec['preview_resolution']
        assert len(entries)==len(selected_frames)
        write_viewer(out/'motion_preview.html',entries)
        (out/'motion_preview_manifest.json').write_text(json.dumps({'fps':4,'source_fps':24,'duration_seconds':len(entries)/4,'resolution':[640,360],'entries':entries},indent=2),encoding='utf-8')
        report['motion_preview']={'player':str(out/'motion_preview.html'),'manifest':str(out/'motion_preview_manifest.json'),'frames':len(entries),'fps':4,'resolution':[640,360]}
    (out / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('SC001 OUTPUT:', out)
    print('STRUCTURE VALIDATED; VISUAL REVIEW PENDING')


if __name__ == '__main__':
    main()
