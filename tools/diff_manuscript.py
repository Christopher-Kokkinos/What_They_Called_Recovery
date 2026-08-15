#!/usr/bin/env python3
"""Create a unified UTF-8 text diff between two files."""
from pathlib import Path
import argparse, difflib

def main():
    p=argparse.ArgumentParser(); p.add_argument('base'); p.add_argument('current'); p.add_argument('--output', required=True); a=p.parse_args()
    b=Path(a.base).read_text(encoding='utf-8').splitlines(True); c=Path(a.current).read_text(encoding='utf-8').splitlines(True)
    diff=''.join(difflib.unified_diff(b,c,fromfile=a.base,tofile=a.current))
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(diff,encoding='utf-8',newline='\n')
    print(f'diff_lines={len(diff.splitlines())} output={a.output}')
if __name__=='__main__': main()
