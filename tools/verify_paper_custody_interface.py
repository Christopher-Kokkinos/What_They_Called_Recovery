"""Bind the actual builder call to custody's signature without importing bpy."""
import ast,inspect,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUTO=ROOT/'Active/Film/04_Scenes/Automation'
sys.path.insert(0,str(AUTO))
from sc001_inner_pocket_blender import custody
signature=inspect.signature(custody)
tree=ast.parse((AUTO/'build_sc001_paper_contact_review.py').read_text())
assignment=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='custody_options' for t in n.targets))
# Evaluate only the actual options expression with inert constants in both modes.
for enabled in (False,True):
 from types import SimpleNamespace
 options=eval(compile(ast.Expression(assignment.value),'<custody options>','eval'),{'__builtins__':{},'dict':dict,'opts':SimpleNamespace(pocket_handover_review=enabled),'START':1,'END':397,'ATTACH':157,'RELEASE':200})
 for call in [n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='custody']:
  assert all(k.arg is None and isinstance(k.value,ast.Name) and k.value.id=='custody_options' for k in call.keywords)
  signature.bind(*[object() for _ in call.args],**options)
 assert options==({'start':1,'end':397,'attach':157,'release':200} if enabled else {})
try:signature.bind(*[object() for _ in range(9)])
except TypeError:pass
else:raise AssertionError('Legacy extra SUPPORT_EDGE argument was accepted')
print('PAPER_CUSTODY_INTERFACE_PASS; both modes bind, legacy ninth argument rejected')
