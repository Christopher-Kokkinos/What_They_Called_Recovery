#!/usr/bin/env python3
"""Verify the permanent WTCR film-production workspace skeleton."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
film = root / 'Active' / 'Film'

required_dirs = [
    '00_Control',
    '00_Control/00.10_governance',
    '00_Control/00.20_canon_register',
    '00_Control/00.30_decision_log',
    '00_Control/00.40_project_state',
    '00_Control/00.50_schemas',
    '01_Adaptation',
    '01_Adaptation/Treatment',
    '01_Adaptation/Sequences',
    '01_Adaptation/Screenplay',
    '01_Adaptation/Scene_Packets',
    '02_Design',
    '03_Assets',
    '04_Scenes',
    '05_Capture',
    '06_Audio',
    '07_Post',
    '08_Deliverables',
    '10_Characters',
    '10_Characters/10.10_Elias',
    '10_Characters/10.20_Zoe',
    '10_Characters/10.30_Jackie',
    '10_Characters/10.40_Mac',
    '10_Characters/10.50_Cain',
    '10_Characters/10.60_Voss',
    '10_Characters/10.70_Vale',
    '10_Characters/10.80_Reyes',
    '10_Characters/10.90_Helen',
    '10_Characters/10.91_Brian',
    '10_Characters/10.92_Sam',
    '20_Story_System',
    '20_Story_System/20.10_timeline',
    '20_Story_System/20.20_relationships',
    '20_Story_System/20.30_reveals',
    '20_Story_System/20.40_continuity',
    '04_Scenes/Automation',
]
required_files = [
    'README.md',
    'AGENTS.md',
    '00_Control/production_manifest.json',
    '00_Control/scene_register.csv',
    '00_Control/asset_register.csv',
    '00_Control/licence_register.csv',
    '00_Control/adaptation_register.csv',
    '01_Adaptation/SCREENPLAY_FORMAT.md',
    '00_Control/00.20_canon_register/canon_register.csv',
    '00_Control/00.30_decision_log/_TEMPLATE.md',
    '10_Characters/_TEMPLATE.md',
]

missing_dirs = [p for p in required_dirs if not (film / p).is_dir()]
missing_files = [p for p in required_files if not (film / p).is_file()]
report_dir_ok = (root / 'Reports' / 'Film').is_dir()
film_rule_ok = (root / 'docs' / 'rules' / 'film.md').is_file()
vertical_slice_workflow_ok = (root / 'workflows' / 'film-vertical-slice.md').is_file()
adaptation_workflow_ok = (root / 'workflows' / 'film-adaptation-preparation.md').is_file()
dual_execution_sop_ok = (root / 'workflows' / 'blender-dual-execution-sop.md').is_file()

ok = (
    not missing_dirs
    and not missing_files
    and report_dir_ok
    and film_rule_ok
    and vertical_slice_workflow_ok
    and adaptation_workflow_ok
    and dual_execution_sop_ok
)
print(
    f'missing_dirs={missing_dirs} missing_files={missing_files} '
    f'reports_film={report_dir_ok} film_rule={film_rule_ok} '
    f'vertical_slice_workflow={vertical_slice_workflow_ok} '
    f'adaptation_workflow={adaptation_workflow_ok} '
    f'dual_execution_sop={dual_execution_sop_ok} '
    f'result={"PASS" if ok else "FAIL"}'
)
sys.exit(0 if ok else 1)
