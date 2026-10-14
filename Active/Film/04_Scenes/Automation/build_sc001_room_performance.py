"""SC001 connected-room performance v0.1. Fresh background Blender only."""
import argparse
from datetime import datetime,timezone
import hashlib,json,math,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
SPEC=ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json'


def main():
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from sc001_layout import validate,walls
    from sc001_room_performance import state,joint_boxes,box_corners,END,SHOTS,NOTICE,bedside_geometry,drawer_geometry
    import bpy
    from mathutils import Matrix,Vector
    p=argparse.ArgumentParser();p.add_argument('--rig-test',action='store_true',help='Separate weighted Elias rig integration test; proxy contact checks retained');p.add_argument('--render-shot-review',action='store_true');p.add_argument('--render-motion-preview',action='store_true');p.add_argument('--render-shower-review',action='store_true',help='Six shower contact/cue stills only; full-scene flag takes precedence')
    opts=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if not bpy.app.background or bpy.data.filepath:raise RuntimeError('Use --background --factory-startup; loaded production files refused')
    plan_path=ROOT/'Active/Film/04_Scenes/SC001/SC001_room_performance_spec_v0.1.json'
    plan=json.loads(plan_path.read_text(encoding='utf-8'))
    source=(ROOT/plan['screenplay']).read_bytes().replace(b'\r\n',b'\n')
    assert hashlib.sha256(source).hexdigest()==plan['screenplay_sha256'],'Screenplay changed; review choreography first'
    assert NOTICE.encode() in source,'Exact notice missing from source'
    assert hashlib.sha256(SPEC.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==plan['layout_sha256_lf'],'Room layout changed; review contacts first'
    assert [(q['frame_start'],q['frame_end'],q['shot_id']) for q in plan['shots']]==[(a,b,'SC001_'+n) for a,b,n in SHOTS]
    layout=json.loads(SPEC.read_text(encoding='utf-8'));static=validate(layout)
    out=ROOT/'Active/Film/_local/SC001'/(('rig_scene_' if opts.rig_test else 'rooms_')+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(parents=True,exist_ok=False)
    scene=bpy.data.scenes.new('SC001_ROOM_PERFORMANCE_v0.1');bpy.context.window.scene=scene
    scene.unit_settings.system='METRIC';scene.render.engine='BLENDER_WORKBENCH';scene.render.fps=24;scene.frame_start=1;scene.frame_end=END
    scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
    scene.display.shading.color_type='OBJECT';scene.display.shading.light='STUDIO';scene.display.shading.show_shadows=True;scene.render.film_transparent=False
    def box(name,pos,size,color=(.53,.54,.52,1),parent=None):
        mesh=bpy.data.meshes.new(name+'_mesh');mesh.from_pydata([(x/2,y/2,z/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]],[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
        obj=bpy.data.objects.new(name,mesh);scene.collection.objects.link(obj);obj.location=pos;obj.scale=size;obj.color=color;obj.parent=parent;return obj
    def empty(name):
        obj=bpy.data.objects.new(name,None);scene.collection.objects.link(obj);return obj
    def label(name,text,pos,size,parent=None):
        curve=bpy.data.curves.new(name,'FONT');curve.body=text;curve.size=size
        obj=bpy.data.objects.new(name,curve);scene.collection.objects.link(obj);obj.location=pos;obj.color=(.06,.07,.07,1);obj.parent=parent;return obj
    def key(obj,frame,fields=('location','rotation_euler','scale')):
        for field in fields:obj.keyframe_insert(data_path=field,frame=frame)
    def orientation(basis):return Matrix(basis).transposed().to_euler()
    box('SET_EliasFlat_floor',(7,6,-.1),(14,12,.2))
    box('SET_EliasFlat_landing',(14.9,6,-.1),(1.8,2,.2))
    for name,pos,size in walls(layout):
        pos[2]=.425;size[2]=.85;box('SET_'+name,pos,size,(.70,.71,.68,1))
    for item in layout['furniture']:
        if item['id']=='bedside_drawers':continue
        box('SET_'+item['id'],item['position'],item['size'])
    # Hollow bedside shell and a single moving drawer; no concealed control pillar.
    for name,pos,size in bedside_geometry(layout):box('SET_bedside_'+name,pos,size)
    drawer=empty('PRP_BedsideDrawer')
    for n,pos,size in drawer_geometry():box('Drawer_'+n,pos,size,parent=drawer)
    # True blister-scale insert: ten cells, two empty, no dose action.
    box('PRP_PrescriptionStrip',(0,-.10,.535),(.14,.055,.012),(.77,.78,.74,1),drawer)
    for i in range(10):box('Prescription_cell_'+str(i),(-.0576+i*.0128,-.10,.548),(.008,.013,.008),(.15,.15,.14,1) if i<2 else (.85,.83,.7,1),drawer)
    label('Prescription_label','OXYCODONE',(-.064,-.125,.556),.010,drawer)
    label('Alarm_display','08:00  OFF',(3.30,11.465,.90),.035).rotation_euler=(math.pi/2,0,0)
    box('Fireplace_coals',(5.9,11.375,.55),(.8,.03,.30),(.48,.24,.12,1))
    # Narrative clutter stays in living area and on ledges, not unexplained floor stacks.
    box('SET_post_table',(4.1,1.1,.35),(.9,.6,.7))
    for i in range(3):box('Post_'+str(i),(4.1,1.1,.71+i*.018),(.24,.17,.015),(.75,.74,.69,1))
    for i in range(3):box('Folded_clothes_'+str(i),(2,1.1,.94+i*.045),(.4,.3,.04),(.3,.35,.4,1))
    box('SET_hall_tool_cupboard',(13.0,6.8,.6),(.8,.25,1.2));box('PRP_Torch',(13.0,6.8,1.25),(.25,.07,.07),(.15,.18,.20,1))
    for i in range(3):box('Tool_'+str(i),(12.7+i*.12,6.8,1.24),(.07,.13,.04),(.2,.24,.26,1))
    box('SET_WindowLedge',(-.35,10.4,1.10),(.7,1.8,.1))
    for n,pos,size in [('sill',(0,10.4,1.13),(.08,1.8,.08)),('top',(0,10.4,2.3),(.08,1.8,.08)),('a',(0,9.5,1.7),(.08,.08,1.2)),('b',(0,11.3,1.7),(.08,.08,1.2))]:box('Window_'+n,pos,size)
    for i,y in enumerate([10.05,10.70]):
        box('Pigeon_'+str(i),(-.3,y,1.25),(.20,.14,.20),(.27,.3,.31,1))
        box('Pigeon_head_'+str(i),(-.22,y,1.36),(.10,.10,.10),(.3,.32,.33,1))
    actor={name:box('CHR_Elias_'+name,b['center'],b['size'],(.28,.35,.40,1)) for name,b in joint_boxes(state(1,layout)).items()}
    mug=empty('PRP_CoffeeMug');bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.06,depth=.18)
    body=bpy.context.object
    for col in list(body.users_collection):col.objects.unlink(body)
    scene.collection.objects.link(body);body.name='Mug_body';body.parent=mug;body.location=(0,0,0);body.color=(.77,.76,.7,1)
    for name,pos,size in [('outer',(-.12,0,0),(.025,.03,.14)),('top',(-.09,0,.065),(.08,.03,.025)),('bottom',(-.09,0,-.065),(.08,.03,.025))]:box('Mug_handle_'+name,pos,size,(.77,.76,.7,1),mug)
    keys=empty('PRP_Keys');box('Key_ring',(0,0,0),(.06,.015,.06),(.62,.64,.66,1),keys)
    for i in range(2):box('Key_'+str(i),(.015*i,0,-.045),(.014,.012,.065),(.62,.64,.66,1),keys)
    letter=empty('PRP_ResignationLetter');left=box('Letter_fixed',(0,-.07425,0),(.21,.1485,.002),(.90,.89,.84,1),letter)
    flap=box('Letter_fold',(0,.07425,.002),(.21,.1485,.002),(.90,.89,.84,1),letter)
    text=label('Notice_exact_text',NOTICE.replace('. ','.\n'),(-.099,.060,.005),.0065,letter)
    envelope=empty('PRP_MACEnvelope');envelope_surfaces=[]
    for name,pos,size in [('back',(0,0,0),(.22,.17,.002)),('front',(0,0,.008),(.22,.17,.002)),('left',(-.1095,0,.004),(.001,.17,.010)),('right',(.1095,0,.004),(.001,.17,.010)),('closed_edge',(0,.0845,.004),(.22,.001,.010))]:envelope_surfaces.append(box('Envelope_'+name,pos,size,(.91,.90,.85,1),envelope))
    envelope_flap=box('Envelope_flap',(0,-.11,.001),(.22,.05,.002),(.91,.90,.85,1),envelope);envelope_surfaces.append(envelope_flap)
    mac=label('MAC_label','MAC',(-.04,0,.010),.025,envelope)
    # Parent scale cancels here so the label remains in metres, not envelope units.
    mac.parent=None;mac_parent=empty('Envelope_text_anchor');mac.parent=mac_parent
    water=box('REVIEW_ShowerWater',(12.9,.65,1.5),(.4,.04,1.0),(.48,.62,.67,1))
    water.display_type='WIRE';water.hide_render=True
    cold=label('REVIEW_ShowerCue','COLD / Excellent',(12.1,1.7,2),.10);cold.rotation_euler=(math.pi/2,0,0)
    cameras={}
    for name,eye,target,scale in [('SH001',(7.0,6.5,4.6),(2.5,10.7,.9),7),('SH002',(6,9.0,2.4),(3,10.9,1),4),('SH003',(3.5,10.7,1.4),(3.5,11.1,.54),.55),('SH004',(16,6,5),(10.5,9.5,1),10),('SH005',(10.5,3.6,2.6),(12.9,.7,1.1),4),('SH006',(8.5,6.8,2.7),(11.0,9.2,1.0),4),('SH007',(11.18,9.42,1.80),(11.18,9.42,.772),.60),('SH008',(8.5,6.8,2.7),(11.0,9.2,1.0),4),('SH009',(3.8,7.8,2.6),(.9,10.4,1.1),4),('departure_inside',(8,4.4,4.5),(4.5,8,1),14),('departure_outside',(18,3,2.8),(14.8,6,1),14),('pigeons',(2.5,9.0,2),(-.3,10.4,1.3),2.4)]:
        data=bpy.data.cameras.new('CAM_'+name);obj=bpy.data.objects.new('CAM_'+name,data);scene.collection.objects.link(obj);obj.location=eye;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=scale;cameras[name]=obj
    for start,end,name in SHOTS[:-1]:m=scene.timeline_markers.new(name,frame=start);m.camera=cameras[name]
    for name,f in [('departure_inside',2641),('departure_outside',3061),('pigeons',3121)]:m=scene.timeline_markers.new(name,frame=f);m.camera=cameras[name]
    expected={};maximum_floor_error=0
    for f in range(1,END+1):
        s=state(f,layout);boxes=joint_boxes(s)
        for name,b in boxes.items():
            obj=actor[name];obj.location=b['center'];obj.scale=b['size'];obj.rotation_euler=orientation(b['basis']);key(obj,f)
            if name in ('torso','lower_spine'):obj.color=(.18,.23,.27,1) if f>=1369 else (.28,.35,.40,1);key(obj,f,('color',))
        drawer.location=(3.5,11.48-s['drawer_slide'],0);key(drawer,f,('location',))
        mug.location=s['mug'];mug.rotation_euler=orientation((s['joints']['lateral'],s['ground_forward'],(0,0,1)));key(mug,f,('location','rotation_euler'))
        keys.location=s['keys'];keys.rotation_euler=(math.pi/2*(1-max(0,min(1,(f-2395)/35))),0,0);key(keys,f,('location','rotation_euler'))
        packet_rotation=Matrix.Identity(3).to_quaternion().slerp(Matrix(s['packet_basis']).transposed().to_quaternion(),s['pocket_rotation']).to_euler()
        letter.rotation_euler=packet_rotation;envelope.rotation_euler=packet_rotation;mac_parent.rotation_euler=packet_rotation
        letter.location=Vector(s['envelope'])+packet_rotation.to_matrix()@Vector((0,.07425,.003)) if f>=2320 else s['letter'];letter.hide_render=s['packet_pocket'];key(letter,f,('location','rotation_euler','hide_render'))
        # Object hiding does not propagate to children, so key every visible surface.
        for obj in [left,flap,text]:obj.hide_render=s['packet_pocket'] or (obj==text and f>=2220);key(obj,f,('hide_render',))
        angle=math.pi*s['fold'];flap.rotation_euler=(angle,0,0);flap.location=(0,.07425*math.cos(angle),.002+.07425*math.sin(angle));key(flap,f,('location','rotation_euler'))
        envelope.location=s['envelope'];envelope.hide_render=s['packet_pocket'];key(envelope,f,('location','rotation_euler','hide_render'));mac_parent.location=s['envelope'];key(mac_parent,f,('location','rotation_euler'));mac.hide_render=s['packet_pocket'];key(mac,f,('hide_render',))
        close=max(0,min(1,(f-2320)/20));angle=math.pi*close;envelope_flap.location=(0,-.085-.025*math.cos(angle),.001+.025*math.sin(angle)+.009*close);envelope_flap.rotation_euler=(-angle,0,0);key(envelope_flap,f,('location','rotation_euler'))
        for obj in envelope_surfaces:obj.hide_render=s['packet_pocket'];key(obj,f,('hide_render',))
        water.hide_render=True;water.hide_viewport=not s['shower_on'];cold.hide_render=not(s['shower_on'] and s['shower_cold']);key(water,f,('hide_render','hide_viewport'));key(cold,f,('hide_render',))
        peck=max(0,1-abs(f-60)/15) if f<100 else max(0,1-abs(f-3148)/10)
        bird=scene.objects['Pigeon_head_0'];bird.location=(-.22+.18*peck,10.05,1.36-.05*peck);key(bird,f,('location',))
        if f>=2641:
            cam=cameras['departure_inside' if f<=3060 else 'departure_outside'];target=Vector(s['root'])+Vector((0,0,1));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();key(cam,f,('rotation_euler',))
        if f in [61,271,360,505,580,590,600,640,661,780,850,870,888,1003,1195,1207,1210,1213,1225,1237,1282,1285,1411,1540,1561,2161,2215,2227,2260,2275,2300,2320,2340,2360,2395,2430,2450,2510,2587,2629,2810,3060,3061,3120,3121,3148]:expected[f]=boxes
    from sc001_motion_blender import linearise_owned_actions
    linearise_owned_actions(list(scene.objects))
    rig_report=None
    if opts.rig_test:
        sys.path.insert(0,str(ROOT/'Active/Film/03_Assets/Characters/Elias'))
        from elias_rig_blender import animate_and_validate
        rig_report=animate_and_validate(bpy,scene,layout,state,END)
        for proxy in actor.values():proxy.hide_render=True
    # Read evaluated Blender transforms back at review frames, not only authored keys.
    max_error=0;packet_points=0
    for f,boxes in expected.items():
        scene.frame_set(f);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        for name,b in boxes.items():
            obj=actor[name].evaluated_get(deps);actual=[obj.matrix_world@Vector(c) for c in obj.bound_box];planned=box_corners(b)
            # Local vertex order of Blender bound_box is not assumed.
            max_error=max(max_error,max(min((v-Vector(p)).length for p in planned) for v in actual))
        if f>=2360:
            s=state(f,layout);j=s['joints']
            for part in [left,flap]+envelope_surfaces:
                obj=part.evaluated_get(deps)
                for corner in obj.bound_box:
                    delta=obj.matrix_world@Vector(corner)-Vector(j['pelvis']);x=delta.dot(Vector(j['lateral']));z=delta.dot(Vector(j['up']));depth=delta.dot(Vector(j['forward']))
                    assert abs(x)<.225+1e-5 and 0<z<.65 and abs(depth)<.125+1e-5,'Packet protrudes outside torso: '+part.name
                    packet_points+=1
        for side in ['left','right']:
            foot=actor[side+'_foot'].evaluated_get(deps);points=[foot.matrix_world@Vector(c) for c in foot.bound_box]
            if f<=270:
                assert all(1.4-1e-5<=p.x<=3+1e-5 and 9.65-1e-5<=p.y<=11.85+1e-5 for p in points),'Sleeping feet overhang'
                assert abs(min(p.z for p in points)-.54)<1e-5,'Sleeping shoe support'
            elif f>=360:
                support=.16 if 1129<=f<=1368 else 0;gap=min(p.z for p in points)-support
                assert gap>=-1e-5,'Foot penetrates support'
                if f<2641:maximum_floor_error=max(maximum_floor_error,abs(gap));assert abs(gap)<1e-5,'Stationary sole floats'
    assert max_error<1e-4,'Evaluated mesh differs from exact transform plan'
    manifest=[]
    review_frames=sorted(expected) if opts.render_shot_review else [1195,1207,1213,1225,1237,1285] if opts.render_shower_review else []
    if opts.render_motion_preview:(out/'motion_frames').mkdir()
    def select_camera(f):
        name=next(n for a,b,n in SHOTS if a<=f<=b) if f<2641 else ('departure_inside' if f<=3060 else 'departure_outside' if f<=3120 else 'pigeons')
        scene.camera=cameras[name]
    for f in review_frames:
        scene.frame_set(f);select_camera(f);scene.render.resolution_percentage=100;scene.render.filepath=str(out/f'SC001_rooms_frame_{f:04d}.png');bpy.ops.render.render(write_still=True)
    if opts.render_motion_preview:
        scene.render.resolution_percentage=50
        for i,f in enumerate(range(1,END+1,6)):
            scene.frame_set(f);select_camera(f);path=f'motion_frames/frame_{i:04d}.png';scene.render.filepath=str(out/path);bpy.ops.render.render(write_still=True);manifest.append({'frame':f,'image':path,'shot':scene.camera.name,'cue':state(f,layout)['phase']})
        (out/'motion_preview_manifest.json').write_text(json.dumps({'fps':4,'source_fps':24,'duration_seconds':END/24,'entries':manifest},indent=2),encoding='utf-8')
    if manifest:
        from sc001_preview import write_viewer
        write_viewer(out/'motion_preview.html',manifest)
    scene.render.resolution_percentage=100;scene.frame_set(1);scene.camera=cameras['SH001'];blend=out/('SC001_rig_performance_v0.1.blend' if opts.rig_test else 'SC001_room_performance_v0.1.blend');bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    report={'status':'evaluated_review_frames_validated_visual_review_pending','blender_version':bpy.app.version_string,'spec_sha256':hashlib.sha256(SPEC.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'module_sha256':{n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in ['sc001_room_performance.py','sc001_layout.py','elias_articulation.py','sc001_motion_blender.py','sc001_motion.py','sc001_preview.py']},'static_layout':static,'frame_end':END,'duration_seconds':END/24,'evaluated_review_frames':sorted(expected),'maximum_transform_error':max_error,'maximum_stationary_support_gap':maximum_floor_error,'performance_spec_sha256':hashlib.sha256(plan_path.read_bytes()).hexdigest(),'motion_samples':len(manifest),'packet_evaluated_corner_checks':packet_points,'stills':[f'SC001_rooms_frame_{f:04d}.png' for f in review_frames],'blend':str(blend),'letter_sequence':'mug on table; both hands fold; envelope supported left; right inserts and pockets; keys then mug retrieved','limitations':['Diagnostic low walls; door-use and final occlusion review pending','Box anatomy without final skinning or performance','No final water/lighting/grain/audio','No whole-scene acceptance'],'scene_accepted':False}
    if opts.rig_test:
        report['rig']=rig_report;report['module_sha256']['elias_rig_blender.py']=hashlib.sha256((Path(__file__).parent/'elias_rig_blender.py').read_bytes()).hexdigest()
        report['rig_math_sha256']=hashlib.sha256((ROOT/'Active/Film/03_Assets/Characters/Elias/elias_rig_math.py').read_bytes()).hexdigest()
        report['limitations']=[x for x in report['limitations'] if x!='Box anatomy without final skinning or performance']+rig_report['limitations']
    (out/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SC001 ROOMS OUTPUT:',out);print('EVALUATED REVIEW FRAMES VALIDATED; VISUAL REVIEW PENDING')

if __name__=='__main__':main()
