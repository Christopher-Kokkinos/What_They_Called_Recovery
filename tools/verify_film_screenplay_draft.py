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
    ('SC004', 'SC004_Mac_Call_draft.fountain'),
    ('SC005', 'SC005_Arrivals_Processing_draft.fountain'),
    ('SC006', 'SC006_First_Terms_draft.fountain'),
    ('SC007', 'SC007_Car_Test_draft.fountain'),
    ('SC008', 'SC008_Public_Stop_draft.fountain'),
    ('SC009', 'SC009_Cain_Threat_draft.fountain'),
    ('SC010', 'SC010_Three_Minutes_draft.fountain'),
    ('SC011', 'SC011_Seven_Days_draft.fountain'),
    ('SC012', 'SC012_Ordinary_Errand_draft.fountain'),
    ('SC013', 'SC013_House_Rules_draft.fountain'),
    ('SC014', 'SC014_Showing_Escape_draft.fountain'),
    ('SC015', 'SC015_Home_Changed_draft.fountain'),
    ('SC016', 'SC016_Jackie_Decoy_draft.fountain'),
    ('SC017', 'SC017_The_Flight_draft.fountain'),
    ('SC018', 'SC018_No_Grandmother_draft.fountain'),
    ('SC019', 'SC019_Jackie_Cutaway_draft.fountain'),
    ('SC020', 'SC020_The_Contract_draft.fountain'),
    ('SC021', 'SC021_First_lesson_draft.fountain'),
    ('SC022', 'SC022_Eastbound_ghost_draft.fountain'),
    ('SC023', 'SC023_Different_methods_draft.fountain'),
    ('SC024', 'SC024_Market_observation_draft.fountain'),
    ('SC025', 'SC025_A_fallback_and_a_bait_room_draft.fountain'),
    ('SC026', 'SC026_Reyes_enters_draft.fountain'),
    ('SC027', 'SC027_Sam_draft.fountain'),
    ('SC028', 'SC028_Contact_draft.fountain'),
    ('SC029', 'SC029_Public_terms_draft.fountain'),
    ('SC030', 'SC030_The_delivery_van_draft.fountain'),
    ('SC031', 'SC031_The_index_draft.fountain'),
    ('SC032', 'SC032_Routes_and_exceptions_draft.fountain'),
    ('SC033', 'SC033_Recipients_draft.fountain'),
    ('SC034', 'SC034_The_limited_query_draft.fountain'),
    ('SC035', 'SC035_Circular_answers_draft.fountain'),
    ('SC036', 'SC036_Two_orders_draft.fountain'),
    ('SC037', 'SC037_A_profile_is_not_a_person_draft.fountain'),
    ('SC038', 'SC038_Reaction_draft.fountain'),
    ('SC039', 'SC039_Helen_and_Brian_s_file_draft.fountain'),
    ('SC040', 'SC040_The_real_organisation_draft.fountain'),
    ('SC041', 'SC041_North_Vale_answers_draft.fountain'),
    ('SC042', 'SC042_The_yellow_coat_draft.fountain'),
    ('SC043', 'SC043_A_record_beyond_the_drive_draft.fountain'),
    ('SC044', 'SC044_Cost_of_containment_draft.fountain'),
    ('SC045', 'SC045_The_match_draft.fountain'),
    ('SC046', 'SC046_Through_glass_draft.fountain'),
    ('SC047', 'SC047_Three_messages_draft.fountain'),
    ('SC048', 'SC048_Jackie_answers_draft.fountain'),
    ('SC049', 'SC049_Partial_plans_draft.fountain'),
    ('SC050', 'SC050_The_safeguarding_call_draft.fountain'),
    ('SC051', 'SC051_Inside_and_outside_draft.fountain'),
    ('SC052', 'SC052_Owned_conduct_draft.fountain'),
    ('SC053', 'SC053_Irreversible_draft.fountain'),
    ('SC054', 'SC054_Custody_draft.fountain'),
    ('SC055', 'SC055_Jackie_and_Zoe_draft.fountain'),
    ('SC056', 'SC056_A_life_still_being_decided_draft.fountain'),
    ('SC057', 'SC057_The_ridge_draft.fountain'),
]:
    original = (SCREENPLAY.parent / path).read_text().split('\n\n', 1)[1]
    block = screenplay[positions[scene]: positions.get(f'SC{int(scene[2:])+1:03}', len(screenplay))]
    assert original.rstrip() in block, f'{scene} differs from its reviewed standalone draft'

print(f'film screenplay draft: sequences={len(sequences)} scenes={len(scene_ids)} '
      f'source_units={len(rows)} split_links={sum(counts.values())-len(rows)} result=PASS')
