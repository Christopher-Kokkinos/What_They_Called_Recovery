"""Sampled full-scene preview from an all-frame validated integrated rig."""
import hashlib,json
from sc001_room_performance import SHOTS,END
from sc001_preview import write_viewer

SAMPLES=list(range(1,END+1,6))
if SAMPLES[-1]!=END:SAMPLES.append(END)


def camera_name(frame):
    if frame<2641:return 'CAM_'+next(name for a,b,name in SHOTS if a<=frame<=b)
    return 'CAM_'+('departure_inside' if frame<=3060 else 'departure_outside' if frame<=3120 else 'pigeons')


def render(bpy,scene,state,layout,out):
    bindings=[(m,m.camera) for m in scene.timeline_markers]
    old=(scene.camera,scene.frame_current,scene.render.filepath,scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage,scene.render.image_settings.file_format)
    folder=out/'motion_frames';folder.mkdir(exist_ok=False);entries=[];expected=[];hits=[]
    def guard(render_scene,*unused):
        if render_scene==scene:
            assert scene.camera.name==expected[-1],'Full-scene review camera mismatch'
            hits.append(scene.camera.name)
    try:
        for marker,_ in bindings:marker.camera=None
        bpy.app.handlers.render_pre.append(guard)
        scene.render.resolution_x=640;scene.render.resolution_y=360;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG'
        for index,frame in enumerate(SAMPLES):
            scene.frame_set(frame);name=camera_name(frame)
            camera=scene.objects.get(name);assert camera is not None and camera.type=='CAMERA',('Missing source camera',name)
            scene.camera=camera;expected.append(name);bpy.context.view_layer.update()
            path=folder/f'frame_{index:04d}.png';scene.render.filepath=str(path);before=len(hits);bpy.ops.render.render(write_still=True)
            assert len(hits)==before+1,'Full-scene render camera guard did not run'
            entries.append({'frame':frame,'image':path.relative_to(out).as_posix(),'shot':name,'cue':state(frame,layout)['phase'],'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            # Recoverable manifest/viewer even if a later render stops.
            report={'status':'partial_render' if index+1<len(SAMPLES) else 'rendered_visual_review_pending','source_fps':24,'fps':4,'duration_seconds':END/24,'expected_images':len(SAMPLES),'completed_images':len(entries),'entries':entries,'limitations':['Sampled640x360 review; all-frame rig readback recorded separately','Final sample has shorter source interval','Table/posture, contacts and scene visual acceptance remain open']}
            (out/'motion_preview_manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
            write_viewer(out/'motion_preview.html',entries)
            if (index+1)%24==0:print(f'FULL SCENE REVIEW: {index+1}/{len(SAMPLES)} images',flush=True)
        return report
    finally:
        if guard in bpy.app.handlers.render_pre:bpy.app.handlers.render_pre.remove(guard)
        for marker,camera in bindings:marker.camera=camera
        camera,frame,path,x,y,percentage,fmt=old
        scene.frame_set(frame);scene.camera=camera;scene.render.filepath=path;scene.render.resolution_x=x;scene.render.resolution_y=y;scene.render.resolution_percentage=percentage;scene.render.image_settings.file_format=fmt
