"""Envelope proxy geometry and evaluated contact checks for the bounded trial."""
import math

def key_geometry(scene,s,frame):
    flap=s['_envelope_flap_angle'];mouth=s['_envelope_mouth_angle']
    obj=scene.objects['Envelope_flap'];obj.location=(0,-.085+.025*math.cos(flap),.010+.025*math.sin(flap));obj.rotation_euler=(flap,0,0)
    front=scene.objects['Envelope_front'];front.location=(0,.085-.085*math.cos(mouth),.008+.085*math.sin(mouth));front.rotation_euler=(-mouth,0,0)
    for item in (obj,front):
        item.keyframe_insert(data_path='location',frame=frame);item.keyframe_insert(data_path='rotation_euler',frame=frame)

def validate(bpy,scene,s,frame):
    from mathutils import Vector
    deps=bpy.context.evaluated_depsgraph_get();rig=scene.objects['CHR_Elias_RIG'].evaluated_get(deps);maximum=0
    def surface(name,point):
        obj=scene.objects[name].evaluated_get(deps)
        return obj.matrix_world@Vector(point),obj.matrix_world.to_3x3().col[2].normalized()
    for side,suffix in [('left','L'),('right','R')]:
        c=s['_envelope_contacts'][side]
        for digit in ('index','thumb'):
            actual=rig.matrix_world@rig.pose.bones[digit+'_3.'+suffix].tail
            target=s['_hand_plan'][side]['chains'][digit][-1]
            error=(actual-Vector(target)).length;maximum=max(maximum,error)
            assert error<1e-4,(frame,side,digit,'Pad target',error)
            if not c[digit+'_active']:continue
            if c['surface']=='envelope':
                if digit=='index':
                    plane,normal=surface('Envelope_front',(0,0,0));expected=.008
                else:plane,normal=surface('Envelope_back',(-.5,.065/.17,0));expected=-.011
            elif c['surface']=='flap':
                plane,normal=surface('Envelope_flap',(.10/.22,.020/.05,0));expected=c[digit+'_offset'] if digit=='index' else -c['thumb_offset']
                assert (plane-Vector(c['contact'])).length<1e-4,(frame,'Flap edge mapping')
            else:
                plane,normal=surface('Letter_fixed',(.065/.21,(-.135+.07425)/.1485,0));expected=c['index_offset'] if digit=='index' else -c['thumb_offset']
                assert (plane-Vector(c['contact'])).length<1e-4,(frame,'Letter edge mapping')
            gap=(actual-plane).dot(normal)
            assert abs(gap-expected)<1e-4,(frame,side,digit,'Surface gap',gap,expected)
    return maximum
