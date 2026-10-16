"""Check bounded raised-table variant independently of Blender."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'Active/Film/03_Assets/Characters/Elias'),str(ROOT/'Active/Film/04_Scenes/Automation')]
from elias_table_reach import state,WINDOWS,TABLE_TOP
from elias_mug_integration import state as baseline
from elias_articulation import UPPER_ARM_LENGTH,FOREARM_LENGTH,THIGH_LENGTH,CALF_LENGTH
layout=json.loads((ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json').read_text())
maximum_step=0
for name,a,b in WINDOWS:
    previous=None
    for f in range(a,b+1):
        s=state(f,layout);old=baseline(f,layout);j=s['joints']
        for side in ('left','right'):
            for chain,lengths in [(j[side+'_arm'],(UPPER_ARM_LENGTH,FOREARM_LENGTH)),(j[side],(THIGH_LENGTH,CALF_LENGTH))]:
                for p,q,length in zip(chain,chain[1:],lengths):assert abs(math.dist(p,q)-length)<1e-8,(f,side)
            for digit,points in s['_hand_plan'][side]['chains'].items():
                original=old['_hand_plan'][side]['chains'][digit]
                for p,q,x,y in zip(points,points[1:],original,original[1:]):assert abs(math.dist(p,q)-math.dist(x,y))<1e-8
        assert abs(j['pelvis'][2]-1.02)<1e-8
        assert abs(math.atan2(j['up'][0],j['up'][2]))<=.200001
        if previous:maximum_step=max(maximum_step,math.dist(previous,j['left_arm'][-1]))
        previous=j['left_arm'][-1]
        for prop in ('letter','envelope'):assert abs(s[prop][2]-old[prop][2]-.2)<1e-8 or f>=2161
for f in (1375,1400,1540,1550,1560,2400,2430,2450):assert abs(state(f,layout)['mug'][2]-.09-TABLE_TOP)<1e-8
assert maximum_step<.09,maximum_step
print(json.dumps({'status':'bounded_math_pass','frames':sum(b-a+1 for _,a,b in WINDOWS),'maximum_left_wrist_step_m':maximum_step,'table_top_m':TABLE_TOP,'limitations':['Blender readback and visual review pending','Paper/key interaction and chair redesign not passed']}))
