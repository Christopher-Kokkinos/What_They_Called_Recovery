#!/usr/bin/env python3
"""Extract deterministic paragraph text from a DOCX into chapter-oriented UTF-8 text.
Requires python-docx. This mirror is audit evidence, never manuscript authority.
"""
from pathlib import Path
import argparse
from docx import Document

def main():
    p=argparse.ArgumentParser(); p.add_argument('docx'); p.add_argument('--output', default='Reports/Manuscript_Text')
    a=p.parse_args(); out=Path(a.output); out.mkdir(parents=True, exist_ok=True)
    doc=Document(a.docx); chapter=None; buf=[]; index=0
    def flush():
        nonlocal buf, chapter, index
        if chapter is None: return
        (out/f'Chapter_{index:02d}.txt').write_text('\n\n'.join(buf).rstrip()+"\n", encoding='utf-8', newline='\n')
    for para in doc.paragraphs:
        text=para.text.replace('\r','').rstrip()
        if para.style and para.style.name.startswith('Heading 1') and text.upper().startswith('CHAPTER'):
            flush(); index+=1; chapter=text; buf=[text]
        elif chapter is not None:
            buf.append(text)
    flush(); print(f'chapters={index} output={out}')
if __name__=='__main__': main()
