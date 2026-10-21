"""Regression: jacket controls must start from Basis despite contaminated active keys.

This exercises coordinate construction without bpy; evaluated Blender readback remains required.
"""
import sys, math
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Active/Film/04_Scenes/Automation'))
from sc001_inner_pocket_blender import independent_key
class Object:
    def shape_key_add(self,*,name,from_mix):
        assert from_mix is False
        # Deliberately dirty coordinates and relative reference: helper must replace both.
        return SimpleNamespace(data=[SimpleNamespace(co=(9,9,9)) for _ in range(25)],relative_key=object())
verts=[(-.08+.36*x/4,.20+.28*y/4,.22) for y in range(5) for x in range(5)]
basis=object();obj=Object()
pull=independent_key(obj,'PullOpen',basis,verts)
bulge=independent_key(obj,'HandBulge',basis,verts)
assert pull.relative_key is basis and bulge.relative_key is basis
assert [v.co for v in pull.data]==verts and [v.co for v in bulge.data]==verts
for i,(x,y,z) in enumerate(verts):
    pull.data[i].co=(x,y,z+.11)
    bulge.data[i].co=(x,y,z+.025*math.sin(math.pi*((x+.08)/.36))*math.sin(math.pi*((y-.20)/.28)))
for opening in (-.06,0,.5,1):
    for amount in (0,.01,.65,.8):
        actual=tuple(verts[12][k]+opening*(pull.data[12].co[k]-verts[12][k])+amount*(bulge.data[12].co[k]-verts[12][k]) for k in range(3))
        assert math.dist(actual,(.10,.34,.22+.11*opening+.025*amount))<1e-12
print('INDEPENDENT_SHAPE_CONSTRUCTION_PASS; evaluated Blender readback pending')
