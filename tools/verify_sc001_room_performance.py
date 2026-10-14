"""Full source-frame math regression for the connected-room choreography."""
import json,math,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Active/Film/04_Scenes/Automation'))
from sc001_room_performance import state,END,joint_boxes,box_corners,bedside_geometry,drawer_geometry
from elias_articulation import dot,sub,cross,add
from sc001_box_geometry import intersects
from sc001_layout import walls
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text(encoding='utf-8'))
if __name__=='__main__':
    plan=json.loads((ROOT/'Active/Film/04_Scenes/SC001/SC001_room_performance_spec_v0.1.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT/plan['layout']).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==plan['layout_sha256_lf']
    assert hashlib.sha256((ROOT/plan['screenplay']).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==plan['screenplay_sha256']
    I=((1,0,0),(0,1,0),(0,0,1))
    items=[(o['id'],o['position'],o['size']) for o in layout['furniture'] if o['id'] not in ('bedside_drawers','pillow')] + list(walls(layout)) + [('bedside_'+n,p,d) for n,p,d in bedside_geometry(layout)]
    obstacles=[(n,box_corners({'center':p,'size':d,'basis':I})) for n,p,d in items]
    worst=0;min_drop=1;max_carry_elbow=-1;collision_pairs=0;max_flexion=0
    for f in range(1,END+1):
        s=state(f,layout);j=s['joints'];boxes=joint_boxes(s)
        drawers=[('drawer_'+n,box_corners({'center':add((3.5,11.48-s['drawer_slide'],0),p),'size':d,'basis':I})) for n,p,d in drawer_geometry()]
        for name,b in boxes.items():
            assert abs(dot(cross(b['basis'][0],b['basis'][1]),b['basis'][2])-1)<1e-8,'Reflected or non-orthonormal body basis'
            corners=box_corners(b)
            for obstacle,other in obstacles+drawers:
                if 'palm' in name and obstacle.startswith('drawer_') and 580<=f<=888:continue
                collision_pairs+=1
                assert not intersects(corners,b['basis'],other,I),f'{name} intersects {obstacle} at frame {f}'
            if 'foot' in name:
                support=.16 if 1129<=f<=1368 else .54 if f<=270 else 0
                bottom=min(p[2] for p in corners)
                assert bottom>=support-1e-8,(f,name,bottom,support)
                if f<=270 or 360<=f<2641 or f>=3120:assert abs(bottom-support)<1e-8
                if f<=270:assert all(1.4<=p[0]<=3 and 9.65<=p[1]<=11.85 for p in corners)
                if f>=360:
                    for p in corners:
                        if 1129<=f<=1368:assert 12.2<=p[0]<=13.6 and .4<=p[1]<=1.8
                        else:assert (0<=p[0]<=14 and 0<=p[1]<=12) or (14<=p[0]<=15.8 and 5<=p[1]<=7)
        for side in ['left','right']:
            for chain,lengths in [(j[side+'_arm'],(.36,.34)),(j[side],(.50,.52))]:
                for a,b,length in zip(chain,chain[1:],lengths):worst=max(worst,abs(math.dist(a,b)-length))
            shoulder,elbow,wrist=j[side+'_arm'];distance=math.dist(shoulder,wrist);flexion=180-math.degrees(math.acos(max(-1,min(1,(.36**2+.34**2-distance**2)/(.36*.34*2)))));max_flexion=max(max_flexion,flexion);assert flexion<=160
            min_drop=min(min_drop,-dot(sub(elbow,shoulder),j['up']))
        if 2161<=f<2320:assert not s['mug_held'] and s['paper_two_hands']
        if f>=2510:
            shoulder,elbow,wrist=j['left_arm'];max_carry_elbow=max(max_carry_elbow,elbow[2]);assert elbow[2]<wrist[2] and elbow[2]<shoulder[2]-.15
        if 360<=f<=888 or f>=889:
            for side in ['left','right']:assert j[side][2][2]>=.10-1e-8
        if f<=270:
            for side in ['left','right']:
                ankle=j[side][2];assert 1.4<=ankle[0]-.09 and ankle[0]+.09<=3 and 9.65<=ankle[1]-.10 and ankle[1]+.10<=11.85
    a=box_corners({'center':(0,0,0),'size':(1,1,1),'basis':I});b=box_corners({'center':(.25,0,0),'size':(1,1,1),'basis':I});c=box_corners({'center':(1,0,0),'size':(1,1,1),'basis':I})
    assert intersects(a,I,b,I) and not intersects(a,I,c,I),'Intersection/contact classification failed'
    from sc001_room_performance import solve_arm
    for wrist in [(0,0,1.025),(0,0,1.8)]:
        try:solve_arm((0,0,1),wrist,(0,0,1),(1,0,0),1)
        except (ValueError,AssertionError):pass
        else:raise AssertionError('Invalid elbow target accepted')
    for f in range(2360,END+1):
        s=state(f,layout);j=s['joints'];packet={'center':s['envelope'],'size':(.22,.17,.024),'basis':s['packet_basis']}
        for point in box_corners(packet):
            d=sub(point,j['pelvis']);assert abs(dot(d,j['lateral']))<.225 and 0<dot(d,j['up'])<.65 and abs(dot(d,j['forward']))<.125
    assert worst<1e-9
    assert math.dist(state(1225,layout)['joints']['right_arm'][2],state(1225,layout)['shower_contact'])<1e-9
    assert math.dist(state(780,layout)['joints']['left_arm'][2],state(780,layout)['drawer_contact'])<1e-9
    assert state(2360,layout)['packet_pocket'] and not state(2359,layout)['packet_pocket']
    print(json.dumps({'frames':END,'body_obstacle_pairs':collision_pairs,'full_height_wall_checks':True,'limb_error':worst,'minimum_elbow_drop':min_drop,'maximum_carry_elbow_z':max_carry_elbow,'maximum_elbow_flexion_degrees':max_flexion,'status':'pure_math_pass','limitations':['Blender mesh intersections, support and rendered contacts still require runtime review']}))
