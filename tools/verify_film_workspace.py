#!/usr/bin/env python3
"""Verify the permanent WTCR film-production workspace skeleton."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
film = root / 'Active' / 'Film'

required_dirs = [
    '00_Control',
    '01_Adaptation',
    '02_Design',
    '03_Assets',
    '04_Scenes',
    '05_Capture',
    '06_Audio',
    '07_Post',
    '08_Deliverables',
]
required_files = [
    'README.md',
    '00_Control/production_manifest.json',
    '00_Control/scene_register.csv',
    '00_Control/asset_register.csv',
    '00_Control/licence_register.csv',
]

missing_dirs = [p for p in required_dirs if not (film / p).is_dir()]
missing_files = [p for p in required_files if not (film / p).is_file()]
report_dir_ok = (root / 'Reports' / 'Film').is_dir()
film_rule_ok = (root / 'docs' / 'rules' / 'film.md').is_file()
workflow_ok = (root / 'workflows' / 'film-vertical-slice.md').is_file()

ok = not missing_dirs and not missing_files and report_dir_ok and film_rule_ok and workflow_ok
print(
    f'missing_dirs={missing_dirs} missing_files={missing_files} '
    f'reports_film={report_dir_ok} film_rule={film_rule_ok} '
    f'vertical_slice_workflow={workflow_ok} result={"PASS" if ok else "FAIL"}'
)
sys.exit(0 if ok else 1)
