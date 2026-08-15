#!/usr/bin/env python3
"""Verify the permanent WTCR repository root structure."""
from pathlib import Path
import sys
required={'Active','Reference','Reports','Archive','docs','workflows','tools'}
root=Path(__file__).resolve().parents[1]
missing=sorted(x for x in required if not (root/x).exists())
forbidden=[p.name for p in root.iterdir() if p.is_file() and (p.suffix.lower() in {'.docx','.pdf','.zip','.kpf','.kcb'})]
ok=not missing and not forbidden
print(f'missing={missing} root_binary_clutter={forbidden} result={"PASS" if ok else "FAIL"}')
sys.exit(0 if ok else 1)
