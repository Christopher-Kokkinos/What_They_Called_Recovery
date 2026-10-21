"""Foreground blockers must be removed from labelled diagnostic views only."""
import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Active/Film/04_Scenes/Automation'))
from sc001_mug_motion_review import diagnostic_environment_names
prefixes=('CHR_Elias','Letter_','Envelope_','MAC_label','REVIEW_Jacket_','REVIEW_InnerPocket_')
names=['SET_fridge','SET_partition','PRP_other','BASELINE_CHR_Elias_SKIN','CHR_Elias_SKIN','Envelope_back','Letter_fixed','MAC_label','REVIEW_Jacket_lapel','REVIEW_InnerPocket_lining']
objects=[SimpleNamespace(name=n,type='MESH') for n in names]+[SimpleNamespace(name='KeyLight',type='LIGHT'),SimpleNamespace(name='Camera',type='CAMERA')]
assert diagnostic_environment_names(objects,prefixes)==tuple(names[:4])
assert all(obj.type!='MESH' or obj.name.startswith(prefixes) or obj.name in diagnostic_environment_names(objects,prefixes) for obj in objects)
print('DIAGNOSTIC_ISOLATION_SELECTION_PASS; Blender visibility/visual review pending')
