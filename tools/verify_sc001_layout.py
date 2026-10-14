"""Check room partitioning, clear approaches and static furniture intersections."""
import copy
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Active/Film/04_Scenes/Automation'))
from sc001_layout import validate, svg
SPEC=ROOT/'Active/Film/03_Assets/Sets/EliasFlat/EliasFlat_layout_v0.1.json'

if __name__=='__main__':
    spec=json.loads(SPEC.read_text(encoding='utf-8'));result=validate(spec)
    for kind in ('room_overlap','furniture_collision','door_block','drawer_block'):
        bad=copy.deepcopy(spec)
        if kind=='room_overlap':bad['rooms'][0]['bounds'][1]=6
        elif kind=='furniture_collision':bad['furniture'][1]['position']=bad['furniture'][0]['position'][:]
        elif kind=='door_block':bad['furniture'][0]['position']=[4.5,7.7,.27]
        else:bad['furniture'][0]['position']=[3.5,10,.27]
        try:validate(bad)
        except AssertionError:pass
        else:raise AssertionError('Verifier failed to reject '+kind)
    expected=svg(spec); drawing=SPEC.with_suffix('.svg')
    if '--write-svg' in sys.argv:drawing.write_text(expected,encoding='utf-8')
    else:assert drawing.read_text(encoding='utf-8')==expected,'Floor plan drawing stale; regenerate with --write-svg'
    print(json.dumps({**result,'negative_cases':4,'drawing':'synchronized'}))
