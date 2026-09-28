#!/usr/bin/env python3
"""Check navigation and critical reveal boundaries in the whole-film review draft."""

from collections import Counter
import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SCREENPLAY = ROOT / 'Active/Film/01_Adaptation/Screenplay/Whole_Film_Screenplay_v0.1.fountain'
REGISTER = ROOT / 'Active/Film/00_Control/adaptation_register.csv'
SOURCE_DIR = ROOT / 'Active/Film/01_Adaptation/Source_Decomposition'

screenplay = SCREENPLAY.read_text()
scene_ids = re.findall(r'^= (SC\d{3}) —', screenplay, re.M)
assert scene_ids == [f'SC{i:03}' for i in range(1, 58)], 'Scene IDs missing, duplicated or out of order'
sequences = re.findall(r'^# (SEQ-\d{2}) —', screenplay, re.M)
assert sequences == [f'SEQ-{i:02}' for i in range(1, 13)], 'Sequence headings out of order'

with REGISTER.open(newline='') as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 230
source_ids = {
    unit
    for path in SOURCE_DIR.glob('*.md')
    for unit in re.findall(r'(?<=\| )SRC-C\d{2}-\d{2}(?=:)', path.read_text())
}
assert {r['source_unit'] for r in rows} == source_ids, 'Source map coverage mismatch'
assert all(r['status'] == 'provisionally_accepted' for r in rows)
assert all(r['target_scene_ids'] and set(r['target_scene_ids'].split(';')) <= set(scene_ids) for r in rows)
counts = Counter(scene for row in rows for scene in row['target_scene_ids'].split(';'))
assert set(counts) == set(scene_ids), 'A scene has no mapped source unit'

by_source = {r['source_unit']: r for r in rows}
assert by_source['SRC-C41-02']['target_scene_ids'] == 'SC019;SC048'
assert by_source['SRC-C41-02']['disposition'] == 'SPLIT'
assert by_source['SRC-C18-01']['disposition'] == 'RELOCATE'
assert by_source['SRC-C46-06']['target_scene_ids'] == 'SC057'

positions = {scene: screenplay.index(f'= {scene} —') for scene in scene_ids}
assert positions['SC019'] < positions['SC047'] < positions['SC048']
assert 'first route' not in screenplay[positions['SC019']:positions['SC020']]
assert 'second' not in screenplay[positions['SC019']:positions['SC020']]
assert 'Mac obtains a duty safeguarding contact' in screenplay[positions['SC050']:positions['SC051']]
assert 'legal administrator refuses' in screenplay[positions['SC050']:positions['SC051']]
assert 'charges and inquiries, not convictions' in screenplay[positions['SC056']:positions['SC057']]
assert 'the ridge' in screenplay[positions['SC057']:]

for scene, path in [
    ('SC001', 'SC001_Elias_Apartment_draft.fountain'),
    ('SC002', 'SC002_Mrs_Doran_draft.fountain'),
    ('SC003', 'SC003_Clamp_draft.fountain'),
]:
    original = (SCREENPLAY.parent / path).read_text().split('\n\nINT.', 1)[1]
    block = screenplay[positions[scene]: positions[f'SC{int(scene[2:])+1:03}']]
    assert 'INT.' + original.rstrip() in block, f'{scene} differs from its reviewed standalone draft'

print(f'film screenplay draft: sequences={len(sequences)} scenes={len(scene_ids)} '
      f'source_units={len(rows)} split_links={sum(counts.values())-len(rows)} result=PASS')
