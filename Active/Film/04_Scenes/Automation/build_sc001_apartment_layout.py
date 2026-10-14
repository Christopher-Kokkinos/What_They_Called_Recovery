"""Standalone static apartment review; does not load or modify v0.26 animation."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import uuid
ROOT=Path(__file__).resolve().parents[4]
SPEC=ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json'

def main():
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from sc001_layout import validate, walls
    args=argparse.ArgumentParser();args.add_argument('--full-walls',action='store_true');args.add_argument('--render',action='store_true')
    opts=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    import bpy
    from mathutils import Vector
    if not bpy.app.background or bpy.data.filepath:raise RuntimeError('Use fresh background Blender with --factory-startup')
    spec=json.loads(SPEC.read_text(encoding='utf-8'));result=validate(spec)
    out=ROOT/'Active/Film/_local/SC001'/('layout_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8]);out.mkdir(parents=True,exist_ok=False)
    scene=bpy.data.scenes.new('SC001_APARTMENT_LAYOUT_v0.1');bpy.context.window.scene=scene
    scene.unit_settings.system='METRIC';scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=1280;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
    scene.display.shading.color_type='OBJECT';scene.display.shading.light='STUDIO';scene.display.shading.show_shadows=True;scene.render.film_transparent=False
    def box(name,pos,size,color):
        mesh=bpy.data.meshes.new(name+'_mesh');mesh.from_pydata([(x/2,y/2,z/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]],[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
        obj=bpy.data.objects.new(name,mesh);scene.collection.objects.link(obj);obj.location=pos;obj.scale=size;obj.color=color;return obj
    box('SET_EliasFlat_floor',[7,6,-.1],[14,12,.2],(.55,.55,.52,1))
    for name,pos,size in walls(spec):
        if not opts.full_walls:size[2]=.85;pos[2]=.425
        box('SET_EliasFlat_'+name,pos,size,(.7,.7,.67,1))
    for item in spec['furniture']:
        obj=box('LAYOUT_'+item['id'],item['position'],item['size'],(.35,.46,.53,1));obj['room']=item['room'];obj['status']='static_placement_proxy'
    for reserve in spec['reservations']:
        x0,y0,x1,y1=reserve['bounds'];box('REVIEW_'+reserve['id'],[(x0+x1)/2,(y0+y1)/2,.008],[x1-x0,y1-y0,.016],(.55,.35,.12,1))
    for name,eye,target in [('top',[7,6,23],[7,6,0]),('overview',[22,-13,19],[7,6,0])]:
        data=bpy.data.cameras.new('LAYOUT_'+name);cam=bpy.data.objects.new('LAYOUT_'+name,data);scene.collection.objects.link(cam);cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=22;scene.camera=cam
        if opts.render:scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    blend=out/'SC001_apartment_layout_v0.1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    assert blend.exists()
    (out/'layout_validation.json').write_text(json.dumps({**result,'blender_version':bpy.app.version_string,'spec_sha256':hashlib.sha256(SPEC.read_bytes()).hexdigest(),'wall_mode':'full' if opts.full_walls else 'cutaway_0.85m','blend':str(blend),'scene_acceptance':False},indent=2)+'\n')
    print('SC001 LAYOUT OUTPUT:',out);print('STATIC LAYOUT VALIDATED; BLENDER VISUAL REVIEW PENDING')

if __name__=='__main__':main()
