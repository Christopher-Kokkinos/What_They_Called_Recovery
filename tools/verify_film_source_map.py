#!/usr/bin/env python3
"""Check film source-map coverage, unit order and chapter titles."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
maps = root / "Active/Film/01_Adaptation/Source_Decomposition"
chapters = root / "Reports/Manuscript_Text"
files = sorted(maps.glob("Chapter*.md"))
errors = []
total = 0

for chapter in range(1, 47):
    source = chapters / f"Chapter_{chapter:02}.txt"
    if not source.exists():
        errors.append(f"missing source mirror: {source.name}")
        continue
    source_title = source.read_text(encoding="utf-8").splitlines()[0]
    expected_title = source_title.replace("CHAPTER", "Chapter", 1)
    matches = []
    units = []
    for path in files:
        data = path.read_text(encoding="utf-8")
        if re.search(r"^#{1,2} (?:Source map: )?" + re.escape(expected_title) + r"$", data, re.M):
            matches.append(path.name)
        for line in data.splitlines():
            match = re.match(r"^\| SRC-C(\d{2})-(\d{2}):", line)
            if match and int(match[1]) == chapter:
                units.append((path.name, int(match[2])))
    if len(matches) != 1:
        errors.append(f"chapter {chapter}: title in {matches}, expected exactly one")
    sequence = [number for _, number in units]
    if sequence != list(range(1, len(sequence) + 1)) or not sequence:
        errors.append(f"chapter {chapter}: unit sequence {units}")
    total += len(units)

print(f"film source map: chapters=46 units={total} errors={len(errors)} result={'FAIL' if errors else 'PASS'}")
for error in errors:
    print(error)
sys.exit(bool(errors))
