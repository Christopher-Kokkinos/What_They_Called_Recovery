"""SC001 diagnostic blockout v0.3. Run only in a fresh background Blender.
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


def select_review_shots(spec, render_stills=False, render_shot_review=False):
    if render_shot_review:
        return spec['shots']
    if render_stills:
        return [s for s in spec['shots'] if s['frame_start'] in {1, 889, 1561}]
    return []


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--render-stills', action='store_true')
    args.add_argument('--render-shot-review', action='store_true',
                      help='Render one labelled still per shot; supersedes --render-stills')
    options = args.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    spec = json.loads(SPEC.read_text(encoding='utf-8'))
    validate_spec(spec)
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    if not bpy.app.background or bpy.data.filepath:
        raise RuntimeError('Use --background --factory-startup; loaded production files are refused')
    out = ROOT / 'Active/Film/_local/SC001' / (datetime.now(timezone.utc).strftime('run_%Y%m%d_%H%M%S_') + uuid.uuid4().hex[:8])
    out.mkdir(parents=True, exist_ok=False)
    scene = bpy.data.scenes.new('SC001_BLOCKOUT_v0.3')
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
    box('SET_EliasFlat_north_wall', (5,7,1.3), (10,.1,2.6), 'SET', (.55,.55,.52,1))
    box('SET_EliasFlat_bed', (2,4,.35), (1.5,2,.7), 'SET')
    box('SET_EliasFlat_drawer', (3.25,4,.65), (.7,.8,1.3), 'SET')
    box('SET_EliasFlat_fake_fireplace', (2,6.6,.5), (1.5,.4,1), 'SET')
    # Hollow frame: the v0.1 solid slab hid the outside pigeon proxies.
    for side, pos, size in [
        ('lower', (0,4.5,.75), (.08,1.8,.08)),
        ('upper', (0,4.5,2.05), (.08,1.8,.08)),
        ('left', (0,3.6,1.4), (.08,.08,1.3)),
        ('right', (0,5.4,1.4), (.08,.08,1.3)),
    ]:
        box('SET_EliasFlat_window_frame_' + side, pos, size, 'SET')
    box('SET_EliasFlat_outside_ledge', (-.35,4.5,.9), (.7,1.8,.12), 'SET')
    box('SET_EliasFlat_entry_marker', (7.5,.05,1), (1,.1,2), 'SET')
    box('SET_EliasFlat_kitchen_counter', (6,5.8,.5), (2.8,.8,1), 'SET')
    box('PRP_AlarmClock', (2,6.35,1.15), (.5,.12,.28))
    label('Clock_display', '08:00  ALARM OFF', (1.76,6.27,1.15), .055)
    box('PRP_PrescriptionStrip', (3.25,3.9,1.32), (.52,.35,.02), color=(.75,.75,.72,1))
    label('Prescription_label', 'OXYCODONE', (3.01,3.98,1.34), .05, True)
    for i in range(8):
        box('Prescription_cell_%02d' % i, (3.04+(i%4)*.13,3.79+(i//4)*.09,1.35), (.08,.06,.015), color=((.12,.12,.12,1) if i < 2 else (.85,.82,.7,1)))
    box('PRP_TorchTools', (6.8,5.8,1.07), (.55,.22,.12))
    box('PRP_ClothesPost', (4.5,4.9,.18), (.6,.4,.35))
    box('PRP_ShowerFixture', (9,6,1.7), (.25,.25,.15))
    box('PRP_CoffeeMug', (5.2,5.6,1.16), (.18,.18,.3))
    box('PRP_Keys', (6.6,5.6,1.04), (.18,.1,.02))
    box('PRP_EliasJacket', (7,2,1.1), (.5,.12,.8))
    box('PRP_MACEnvelope', (6,5.65,1.015), (.65,.3,.02), color=(.9,.9,.86,1))
    label('Envelope_label', 'MAC', (5.76,5.65,1.03), .1, True)
    box('PRP_ResignationLetter', (6,5.25,1.03), (1.4,.6,.015), color=(.92,.9,.85,1))
    label('Notice_exact_text', 'I will complete work already accepted.\nI will not take further assignments after Friday.\nPlease arrange final payment.', (5.33,5.43,1.045), .052, True)
    pigeon = box('CHR_Pigeon_A', (-.35,4.2,1.05), (.2,.35,.22), 'CHARACTERS')
    second = bpy.data.objects.new('CHR_Pigeon_B', pigeon.data)
    collections['CHARACTERS'].objects.link(second)
    second.location, second.scale = (-.35,4.8,1.05), pigeon.scale.copy()
    second.color = pigeon.color
    root = bpy.data.objects.new('CHR_Elias_proxy_root', None)
    collections['CHARACTERS'].objects.link(root)
    for name, pos, size in [('torso',(0,0,1.1),(.45,.25,.7)),('head',(0,0,1.65),(.25,.25,.3)),('legs',(0,0,.4),(.4,.22,.8)),('right_arm',(.32,0,1.1),(.15,.18,.65)),('left_arm',(-.32,0,1.1),(.15,.18,.65))]:
        obj = box('CHR_Elias_' + name, pos, size, 'CHARACTERS', (.27,.32,.36,1))
        obj.parent = root
    # Discrete staging only. No claim to sleeping/pain/letter/mug performance.
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'CONSTANT'
    placements = [(2.1,3.5,0),(2.1,3.5,0),(2.1,3.5,0),(5,4.6,0),(9,5,0),(5.1,5,0),(5.1,5,0),(7,1.5,0),(1.2,4.5,0),(7.5,-1,0)]
    cameras = [((3,1,2.3),(0.9,4.6,1.2),28),((3.8,2.3,1.7),(2.1,3.5,1),45),((3.25,3.3,2.1),(3.25,3.9,1.32),55),((6,1.3,2.2),(6,5.5,1),32),((8,3.6,1.9),(9,6,1.3),40),((5,3.4,1.9),(5.6,5.6,1.1),40),((6,5.3,2.4),(6,5.3,1.03),48),((5.5,.4,1.8),(7,2,1.1),35),((2.8,3,1.8),(.1,4.5,1.2),35),((3,1,2.3),(0.9,4.6,1.2),28)]
    for shot, pos, (eye, target, lens) in zip(spec['shots'], placements, cameras):
        root.location = pos
        root.keyframe_insert(data_path='location', frame=shot['frame_start'])
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
        root.location = placements[i]
        root.keyframe_insert(data_path='location', frame=shot['frame_end'])
    # Fit diagnostic subjects from their actual bounds, including evaluated text.
    # This tests containment, not occlusion or legibility; still review is mandatory.
    framing_checks = []
    subjects = {
        0: ['SET_EliasFlat_bed', 'CHR_Pigeon_A', 'CHR_Pigeon_B', 'Clock_display'] + [o.name for o in root.children],
        3: ['SET_EliasFlat_kitchen_counter', 'PRP_TorchTools', 'PRP_ClothesPost'] + [o.name for o in root.children],
        6: ['PRP_ResignationLetter', 'Notice_exact_text', 'PRP_MACEnvelope', 'Envelope_label'],
        9: ['SET_EliasFlat_bed', 'CHR_Pigeon_A', 'CHR_Pigeon_B', 'Clock_display'],
    }
    for index, names in subjects.items():
        scene.frame_set(spec['shots'][index]['frame_start'])
        bpy.context.view_layer.update()
        deps = bpy.context.evaluated_depsgraph_get()
        points = []
        for name in names:
            obj = scene.objects[name].evaluated_get(deps)
            points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
        center = sum(points, Vector()) / len(points)
        cam = scene.objects[spec['shots'][index]['shot_id']]
        if index == 6:
            # Top-down insert remains a diagnostic view, not final hand performance.
            cam.data.type = 'ORTHO'
            cam.data.ortho_scale = 1.8
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
                               'position':list(cam.location), 'ortho_scale':cam.data.ortho_scale})
    scene.camera = scene.objects['SC001_SH001']
    scene.frame_set(1)
    assert scene.render.fps == spec['fps']
    assert (scene.frame_start, scene.frame_end) == (spec['frame_start'], spec['frame_end'])
    assert [scene.render.resolution_x, scene.render.resolution_y] == spec['preview_resolution']
    required = ['PRP_AlarmClock', 'PRP_PrescriptionStrip', 'PRP_TorchTools', 'PRP_ClothesPost', 'PRP_ShowerFixture', 'PRP_CoffeeMug', 'PRP_Keys', 'PRP_EliasJacket', 'PRP_MACEnvelope', 'PRP_ResignationLetter', 'CHR_Elias_proxy_root']
    assert all(name in scene.objects for name in required)
    assert len(collections['CAMERAS'].objects) == 10
    assert len(scene.timeline_markers) == 10
    assert all(m.camera and m.frame == s['frame_start'] for m,s in zip(scene.timeline_markers, spec['shots']))
    assert len([o for o in collections['CHARACTERS'].objects if o.name.startswith('CHR_Pigeon_')]) == 2
    blend = out / 'SC001_blockout_v0.3.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend), check_existing=True)
    assert blend.is_file() and blend.stat().st_size > 0
    report = {'status':'structure_validated_visual_review_pending', 'blender_version':bpy.app.version_string, 'spec_sha256':hashlib.sha256(SPEC.read_bytes()).hexdigest(), 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'blend':str(blend), 'engine':scene.render.engine, 'framing_checks':framing_checks, 'cameras':len(collections['CAMERAS'].objects), 'objects':len(scene.objects), 'fps':scene.render.fps, 'frames':[scene.frame_start,scene.frame_end], 'resolution':[scene.render.resolution_x,scene.render.resolution_y], 'stills':[], 'limitations':['Diagnostic boxes and discrete staging, not performance animation','Letter, mug and keys custody not animated','No final lighting, grain, audio, materials or rigs','Camera readability and wall geometry require visual review']}
    review_shots = select_review_shots(spec, options.render_stills, options.render_shot_review)
    report['review_mode'] = 'all_ten_shots' if options.render_shot_review else ('three_stills' if options.render_stills else 'build_only')
    report['builder_version'] = '0.3'
    report['diagnostic_shadows'] = scene.display.shading.show_shadows
    report['shot_review'] = []
    if review_shots:
        for shot in review_shots:
            frame = shot['frame_start']
            scene.frame_set(frame)
            scene.camera = scene.objects[shot['shot_id']]
            filename = (shot['shot_id'] + '_frame_%04d.png' % frame) if options.render_shot_review else ('frame_%04d.png' % frame)
            scene.render.filepath = str(out / filename)
            bpy.ops.render.render(write_still=True, scene=scene.name)
            assert Path(scene.render.filepath).is_file()
            report['stills'].append(scene.render.filepath)
            report['shot_review'].append({'shot_id':shot['shot_id'], 'beat_id':shot['beat_id'],
                                         'frame':frame, 'camera':scene.camera.name,
                                         'review_check':shot['review_check'], 'image':scene.render.filepath})
        assert len(report['stills']) == len(review_shots)
    (out / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('SC001 OUTPUT:', out)
    print('STRUCTURE VALIDATED; VISUAL REVIEW PENDING')


if __name__ == '__main__':
    main()
