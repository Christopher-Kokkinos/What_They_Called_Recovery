"""Pure room-layout validation and drawing shared by review tools and Blender."""
import html


def overlap(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) + 1e-8 and min(a[3], b[3]) > max(a[1], b[1]) + 1e-8


def footprint(item):
    x, y, _ = item['position']; w, d, _ = item['size']
    return [x-w/2, y-d/2, x+w/2, y+d/2]


def validate(spec):
    floor = spec['floor_bounds']; rooms = {r['id']: r for r in spec['rooms']}
    regions = spec['rooms'] + spec['circulation']
    area = lambda b: (b[2]-b[0])*(b[3]-b[1])
    assert all(area(r['bounds']) > 0 for r in regions)
    assert abs(sum(area(r['bounds']) for r in regions)-area(floor)) < 1e-8
    for i, region in enumerate(regions):
        b = region['bounds']
        assert floor[0] <= b[0] < b[2] <= floor[2] and floor[1] <= b[1] < b[3] <= floor[3]
        for other in regions[i+1:]:
            assert not overlap(b, other['bounds']), (region['id'], other['id'])
    ids = set()
    for item in spec['furniture']:
        assert item['id'] not in ids; ids.add(item['id'])
        b = footprint(item); r = rooms[item['room']]['bounds']
        assert all(s > 0 for s in item['size'])
        assert r[0]+.06-1e-8 <= b[0] and b[2] <= r[2]-.06+1e-8 and r[1]+.06-1e-8 <= b[1] and b[3] <= r[3]-.06+1e-8, item['id']
    for room in rooms.values():
        d = room['door']; b = room['bounds']; lo, hi = d['center']-d['width']/2, d['center']+d['width']/2
        assert d['width'] >= 1 and b[0]+.12 < lo < hi < b[2]-.12
        sweep = [lo,b[1],hi,b[1]+1.1] if d['edge']=='south' else [lo,b[3]-1.1,hi,b[3]]
        assert any(overlap([lo,b[1]-.1,hi,b[1]+.1] if d['edge']=='south' else [lo,b[3]-.1,hi,b[3]+.1], c['bounds']) for c in spec['circulation']), room['id']
        for item in spec['furniture']:
            if item['room']==room['id']: assert not overlap(sweep, footprint(item)), ('door approach',item['id'])
    for reserve in spec['reservations']:
        for item in spec['furniture']:
            if item['room']==reserve['room']: assert not overlap(reserve['bounds'],footprint(item)), ('reservation',item['id'])
    # Static 3D box collisions; vertically supported objects may touch but not intersect.
    for i, a in enumerate(spec['furniture']):
        for b in spec['furniture'][i+1:]:
            za, zb = a['position'][2], b['position'][2]
            intersects_z = min(za+a['size'][2]/2,zb+b['size'][2]/2)>max(za-a['size'][2]/2,zb-b['size'][2]/2)+1e-8
            assert not (intersects_z and overlap(footprint(a),footprint(b))), ('static collision',a['id'],b['id'])
    return {'status':'static_layout_pass','gross_floor_area_m2':area(floor),'old_area_ratio':area(floor)/spec['previous_floor_area_m2'],'room_count':len(rooms),'limitations':['No actor/contact/motion validation','Proxy geometry only; final door swing and net usable area not certified']}


def walls(spec):
    """Room partitions with door apertures; low-wall diagnostic is chosen by builder."""
    t=spec['wall_thickness']; h=spec['wall_height']
    for r in spec['rooms']:
        x0,y0,x1,y1=r['bounds']; d=r['door']
        for edge,y in [('south',y0),('north',y1)]:
            segments=[(x0,x1)]
            if d['edge']==edge:segments=[(x0,d['center']-d['width']/2),(d['center']+d['width']/2,x1)]
            for i,(lo,hi) in enumerate(segments):yield f"{r['id']}_{edge}_{i}",[(lo+hi)/2,y,h/2],[hi-lo,t,h]
        for edge,x in [('west',x0),('east',x1)]:
            segments=[(y0,y1)]
            if r['id']=='bedroom' and edge=='west':
                w=spec['bedroom_window'];segments=[(y0,w['center']-w['width']/2),(w['center']+w['width']/2,y1)]
            for i,(lo,hi) in enumerate(segments):yield f"{r['id']}_{edge}_{i}",[x,(lo+hi)/2,h/2],[t,hi-lo,h]
    yield 'hall_west', [0,6,h/2], [t,2,h]
    # The east end of the hall contains the apartment entrance.
    d=spec['entry'];x=spec['floor_bounds'][2]
    for i,(lo,hi) in enumerate([(5,d['center']-d['width']/2),(d['center']+d['width']/2,7)]):yield f'entry_{i}',[x,(lo+hi)/2,h/2],[t,hi-lo,h]


def svg(spec):
    scale=65; margin=60; W=1030; H=920
    def rect(b,fill,stroke='#536575',dash=''):
        return f'<rect x="{margin+b[0]*scale}" y="{margin+(12-b[3])*scale}" width="{(b[2]-b[0])*scale}" height="{(b[3]-b[1])*scale}" fill="{fill}" stroke="{stroke}" {dash}/>'
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#fafafa"/>','<text x="60" y="28" font-size="18">SC001 apartment layout v0.1 — 14 × 12 m; static proposal</text>']
    for r in spec['rooms']:
        out.append(rect(r['bounds'],'#edf1f4'))
        b=r['bounds'];out.append(f'<text x="{margin+(b[0]+.2)*scale}" y="{margin+(12-b[3]+.35)*scale}" font-size="15">{r["id"].upper()}</text>')
    for item in spec['furniture']:
        out.append(rect(footprint(item),'#bdcfde'))
        x,y,_=item['position'];out.append(f'<text x="{margin+x*scale}" y="{margin+(12-y)*scale}" text-anchor="middle" font-size="8">{html.escape(item["id"].replace("_"," "))}</text>')
    for r in spec['rooms']:
        d=r['door'];y=r['bounds'][1] if d['edge']=='south' else r['bounds'][3]
        out.append(f'<path d="M {margin+(d["center"]-d["width"]/2)*scale} {margin+(12-y)*scale} h {d["width"]*scale}" stroke="#fafafa" stroke-width="6"/>')
    for res in spec['reservations']:out.append(rect(res['bounds'],'none','#b87424','stroke-dasharray="5 4"'))
    out += ['<text x="540" y="445" font-size="13">HALL → ENTRY</text>','<text x="60" y="867" font-size="13">Dashed: bedside seat/drawer working space. Furniture: placement proxies, not final models.</text>','<text x="60" y="890" font-size="13">Human scale unchanged. Fireplace in bedroom. Clock style deferred. No animation migrated.</text>','</svg>']
    return '\n'.join(out)+'\n'
