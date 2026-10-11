"""Local image-sequence viewer: no codecs, network, pip or add-ons required."""
import json


def write_viewer(path, entries):
    payload=json.dumps(entries).replace('<','\\u003c')
    path.write_text('''<!doctype html><meta charset="utf-8"><title>SC001 coarse motion review</title>
<style>body{background:#20252b;color:#eee;font:16px sans-serif;margin:20px}img{display:block;max-width:100%;width:960px}input{width:80%}button{padding:8px}#info{margin:12px 0}</style>
<h1>SC001 coarse motion review</h1><p>4 sampled frames/second • sampled sequence • silent diagnostic • timing provisional</p>
<img id="view" alt="SC001 sampled Blender frame"><div id="info"></div>
<button id="play">Play</button> <input id="scrub" type="range" min="0" value="0" step="1">
<p>Pause/scrub to inspect continuity. Use full-resolution stills for text readability. This preview samples the 24fps scene every six frames.</p>
<script>const frames='''+payload+''';let i=0,timer=null;const view=document.getElementById('view'),info=document.getElementById('info'),scrub=document.getElementById('scrub'),play=document.getElementById('play');scrub.max=frames.length-1;
function show(){const f=frames[i];view.src=f.image;info.textContent=f.shot+' | source frame '+f.frame+' | '+((f.frame-1)/24).toFixed(2)+' s | '+f.cue;scrub.value=i;}
function stop(){clearInterval(timer);timer=null;play.textContent='Play';}
play.onclick=()=>{if(timer){stop();return;}if(i===frames.length-1)i=0;play.textContent='Pause';timer=setInterval(()=>{show();if(i===frames.length-1){stop();}else{i++;}},250);};scrub.oninput=()=>{stop();i=Number(scrub.value);show();};show();
</script>''',encoding='utf-8')


def evaluated_render_state(bpy, scene):
    """Record evaluated camera/head state immediately before a review render."""
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    head=scene.objects['CHR_Elias_head'].evaluated_get(deps)
    cam=scene.camera.evaluated_get(deps)
    projected=[world_to_camera_view(scene,cam,head.matrix_world @ Vector(c)) for c in head.bound_box]
    return {'frame':scene.frame_current,'camera':scene.camera.name,
            'resolution':[scene.render.resolution_x,scene.render.resolution_y],
            'camera_matrix':[v for row in cam.matrix_world for v in row],
            'head_matrix':[v for row in head.matrix_world for v in row],
            'lens':cam.data.lens,
            'head_bounds_ndc':[min(p.x for p in projected),max(p.x for p in projected),
                               min(p.y for p in projected),max(p.y for p in projected)],
            'head_contained':all(0<=p.x<=1 and 0<=p.y<=1 and p.z>0 for p in projected)}
