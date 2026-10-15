"""Bounded mug-motion diagnostics; no full-scene bake or extra dependency."""
import hashlib,json
from pathlib import Path

START=1400
END=1539
SOURCE_FPS=24
STEP=3
BAKE_FRAMES=list(range(START,END+1))
RENDER_FRAMES=list(range(START,END+1,STEP))
if RENDER_FRAMES[-1]!=END:RENDER_FRAMES.append(END)


def cycle_schedule():
    from elias_mug_lifecycle import START,END
    bake=list(range(START,END+1));renders=list(range(START,END+1,4))
    if renders[-1]!=END:renders.append(END)
    return bake,renders


def render(bpy,scene,state,layout,out,contact_cycle=False):
    """One fixed camera/scale for the full path, avoiding auto-frame pumping."""
    bake_frames,render_frames=cycle_schedule() if contact_cycle else (BAKE_FRAMES,RENDER_FRAMES)
    start,end=bake_frames[0],bake_frames[-1];step=4 if contact_cycle else STEP
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    from elias_hand_math import hands
    bindings=[(m,m.camera) for m in scene.timeline_markers]
    old=(scene.camera,scene.frame_current,scene.render.filepath,scene.render.resolution_x,
         scene.render.resolution_y,scene.render.resolution_percentage,scene.render.image_settings.file_format)
    data=bpy.data.cameras.new('CAM_mug_motion_review')
    cam=bpy.data.objects.new('CAM_mug_motion_review',data);scene.collection.objects.link(cam)
    data.type='ORTHO';data.clip_start=.01;data.clip_end=100
    active=[]
    def guard(render_scene,*unused):
        if render_scene==scene:
            assert render_scene.camera==cam,'Timeline overrode motion review camera'
            active.append(cam.name)
    try:
        for marker,_ in bindings:marker.camera=None
        bpy.app.handlers.render_pre.append(guard)
        scene.render.resolution_x=640;scene.render.resolution_y=360;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG'
        points=[]
        # Include all integer poses and evaluated prop bounds in the fixed framing.
        for frame in bake_frames:
            scene.frame_set(frame);bpy.context.view_layer.update();s=state(frame,layout)
            points.extend(Vector(p) for chain in hands(s)['left']['chains'].values() for p in chain)
            points.extend(Vector(p) for p in s['joints']['left_arm'])
            points.extend(Vector(s['joints'][name]) for name in ('head','pelvis'))
            deps=bpy.context.evaluated_depsgraph_get()
            for obj in scene.objects:
                if obj.type=='MESH' and obj.name.startswith('Mug_') and not obj.hide_render:
                    evaluated=obj.evaluated_get(deps)
                    points.extend(evaluated.matrix_world@Vector(v) for v in evaluated.bound_box)
        low=Vector(tuple(min(p[i] for p in points) for i in range(3)))
        high=Vector(tuple(max(p[i] for p in points) for i in range(3)))
        target=(low+high)/2;cam.location=target+Vector((1.8,-2.2,1.5))
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
        data.ortho_scale=1.5;bpy.context.view_layer.update()
        for _ in range(40):
            projected=[world_to_camera_view(scene,cam,p) for p in points]
            if all(.08<=p.x<=.92 and .08<=p.y<=.92 and p.z>0 for p in projected):break
            data.ortho_scale*=1.08
        else:raise RuntimeError('Fixed mug motion framing failed')
        folder=out/'motion_frames';folder.mkdir(exist_ok=False);entries=[]
        for index,frame in enumerate(render_frames):
            scene.frame_set(frame);bpy.context.view_layer.update()
            path=folder/f'frame_{index:04d}.png';scene.render.filepath=str(path);before=len(active)
            bpy.ops.render.render(write_still=True)
            assert len(active)==before+1,'Motion review camera guard did not run'
            entries.append({'image':path.relative_to(out).as_posix(),'source_frame':frame,
                'time_seconds':(frame-start)/SOURCE_FPS,'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        manifest={'status':'rendered_visual_review_pending','source_fps':SOURCE_FPS,'preview_fps':SOURCE_FPS/step,
            'source_start':start,'source_end':end,'duration_seconds':(end-start+1)/SOURCE_FPS,
            'entries':entries,'camera':{'name':cam.name,'location':list(cam.location),'target':list(target),'ortho_scale':data.ortho_scale,
            'fixed_for_entire_clip':True,'containment_pass':True,'occlusion_status':'visual_review_pending'},
            'limitations':['Bounded contact cycle; integration with previous/following scene motion pending' if contact_cycle else 'Starts with grip formed; approach/release excluded','48 low-resolution samples; every integer pose validated separately','Final sample may have shorter interval; use timestamps for exact timing','No force simulation or evaluated skin collision pass']}
        (out/'motion_preview_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
        # Local image-sequence player: no video encoder or new software required.
        player="""<!doctype html><meta charset="utf-8"><title>SC001 mug motion review</title>
<style>body{background:#222;color:#eee;font:16px sans-serif;max-width:900px;margin:2rem auto}img{width:100%;image-rendering:auto}input{width:65%}button{padding:.5rem}p{line-height:1.5}</style>
<h1>SC001 first mug lift and return</h1><p>Blockout review. Grip already formed; approach and release excluded. Skin contact and natural motion require visual review.</p>
<img id="view" alt="Mug motion frame"><p><button id="play">Play</button> <input id="seek" type="range" min="0" step="1"> <span id="label"></span></p>
<script>
const manifest=__MANIFEST__,frames=manifest.entries,view=document.getElementById('view'),seek=document.getElementById('seek'),label=document.getElementById('label'),play=document.getElementById('play');
let running=false,start=0,current=0;seek.max=frames.length-1;
function show(i){current=i;view.src=frames[i].image;seek.value=i;label.textContent='Source frame '+frames[i].source_frame;}
play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play';start=performance.now()-frames[current].time_seconds*1000;};
seek.oninput=()=>{show(Number(seek.value));start=performance.now()-frames[current].time_seconds*1000;};
function tick(now){if(running){let time=((now-start)/1000)%manifest.duration_seconds;let i=0;while(i+1<frames.length&&frames[i+1].time_seconds<=time)i++;if(i!==current)show(i);}requestAnimationFrame(tick);}
show(0);requestAnimationFrame(tick);
</script>"""
        if contact_cycle:player=player.replace('Grip already formed; approach and release excluded.','Contact-cycle trial includes approach, grip formation, placement and release. Scene integration remains pending.')
        (out/'motion_preview.html').write_text(player.replace('__MANIFEST__',json.dumps(manifest)),encoding='utf-8')
        return manifest
    finally:
        if guard in bpy.app.handlers.render_pre:bpy.app.handlers.render_pre.remove(guard)
        for marker,camera in bindings:marker.camera=camera
        camera,frame,path,x,y,percentage,fmt=old
        scene.frame_set(frame);scene.camera=camera;scene.render.filepath=path
        scene.render.resolution_x=x;scene.render.resolution_y=y;scene.render.resolution_percentage=percentage;scene.render.image_settings.file_format=fmt
        bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(data)
