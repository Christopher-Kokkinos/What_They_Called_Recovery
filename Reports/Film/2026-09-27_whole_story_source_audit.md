# Whole-story source-map audit — 27 September 2026

## Scope and result

**Structural/source-dependency audit completed with corrections.** The map has 46 chapter headings and 230 unique, consecutive chapter-local `SRC-C##-##` IDs. The corrected units are `SRC-C18-04`, `SRC-C40-05`, `SRC-C42-03`, `SRC-C42-04` and `SRC-C46-01`. No treatment, scene, character dossier, adaptation disposition or vertical-slice choice was approved.

This is a whole-map continuity and evidence-chain audit, with targeted passage verification at the identified turns. It is not a claim that every sentence of the novel and every one of the 230 summaries received a line-by-line literary review. User review and treatment judgment remain separate.

## Method and source authority

1. Checked chapter headings against all 46 `Reports/Manuscript_Text/Chapter_##.txt` titles and checked every source-unit ID for completeness/order with `python tools/verify_film_source_map.py`.
2. Re-extracted `Active/Production/What_They_Called_Recovery_KDP_Publication_Phase4.docx` using `tools/extract_manuscript.py` into a temporary directory. All 46 chapter files matched the committed text mirrors **byte for byte**. The mirrors are navigation evidence; the DOCX is the current publication master.
3. Extracted all 46 locked Phase 7 chapter PDFs with `pdftotext -layout`. Removed only each page's ordinal footer, normalized whitespace and the scene-break representation for lexical comparison. Twenty-seven chapters matched the current master on that basis. Nineteen had bounded wording, capitalization or punctuation variants.
4. Followed major setups, reversals, custody paths, source-of-authority changes and final payoffs across the map and checked the disputed causal passages against the chapter text. Working chronology and dependency tables are under `Active/Film/20_Story_System/`.
5. After author review, checked `Active/Editorial/WTCR_KDP_Phase2_Style_Sheet.docx` and `Reports/Phase2/WTCR_KDP_Phase2_Copyedit_Log.csv` against the lexical differences. The relevant changes are recorded Phase 2 copy edits or source-production repairs. This establishes their editorial provenance; it does not attribute them to Amazon's automatic formatting.

### Locked PDF variants

| Chapters | Difference from current publication master | Film impact |
|---|---|---|
| 4–6 | Phase 7 PDFs use “server”; the current master uses “waitress” in Chapters 4–5 and “member of staff” for an unidentified Chapter 6 employee. | The locked style sheet specifies UK restaurant narration and protection of Zoe's American voice; the copy-edit log records 25 terminology changes. This is a documented correction, not evidence of a different worker. |
| 34 | Current master adds “she” after Zoe's note. | Log records restoration of the omitted subject in a malformed sentence and separation of notebook text from narration. No plot or identity change found. |
| 10, 19, 21, 22, 31, 37, 38, 40, 41 | Spacing, nested quotation, dash, ellipsis or compound punctuation. | Log and style sheet specify closed prose em dashes, no stray nested-quote spaces, three-period ellipses and `adult-child`. These are documented copy-edit fixes. |
| 24, 28, 29, 33, 36, 45 | Capitalization and spelling/compound variants, including “Requestor/Requester” and “multistorey/multi-storey.” | Log records sentence-initial capitalization in notebook/message/prose, preferred `requester`, and UK/style-sheet `multi-storey`. Preserve exact displayed-record typography from the current master. |

The 19 PDF variants are **documented Phase 2 copy-edit/source-production changes** to an earlier baseline, not a manuscript regression introduced by this audit. The current publication master is the repository's publication authority. The locked PDFs remain an earlier story baseline; if a later film task depends on exact wording, cite which version supplied it. The reviewed differences include genuine earlier spelling, capitalization and punctuation defects corrected in the current master. This comparison found no unresolved current-master error among them; it cannot certify that the entire manuscript is free of errors. No source prose was edited.

## Corrections made to the map

| Unit | Prior problem | Corrected source sequence |
|---|---|---|
| `SRC-C18-04` | Collapsed cottage and tracker searches into a generic hunters' inspection. | Reyes watches without entering; Vale inspects the cottage; Voss follows and recovers the trailer-mounted tracker; all regroup Monday. |
| `SRC-C40-05` | Deferred the content of the image to Chapter 41. | Chapter 40 itself reveals the three likely Jackie messages; Chapter 41 tests the sender through a private challenge response. |
| `SRC-C42-03`–`04` | Incorrectly credited the legal administrator with initiating the safeguarding disclosure. | Mac gives his name and reports Jackie's disputed movement to the duty contact; an independent team is dispatched, then the administrator refuses further transfer and Jackie verifies Sarah and Leanne. |
| `SRC-C46-01` | Conflated Ruth's envelope with custody of the drive. | Ruth takes a separate envelope; an evidence officer records and seals the original drive at a secure office. |
| Chapter 19 heading | ASCII apostrophe differed from source title. | Heading now matches the source's typographic apostrophe. |

## Dependency findings

- **Retrospective versus current time:** Chapters 8–14 are Zoe's seven-day account during the journey; Chapters 15–18 resume and overlap the live pursuit. Chapter 18 looks back across Tuesday–Monday. Chapters 20–23 span the lock-up death and Monday response; later archive chapters proceed by weekdays. See `20.10_timeline/Source_Chronology.md`.
- **Knowledge versus fact:** Zoe's Jackie betrayal inference is explicitly overturned in stages. Mac's guardian/grandmother and contractor papers are claims. `AC019`, `BRG` and recipient scores are analytic leads until independent corroboration. The court/source discrepancy, North Vale inquiry and signed contractor accounts narrow the proof without validating the entire archive.
- **Custody and agency:** Zoe's folder, original drive, working copies, separate envelope, controlled disclosures and final evidence bag have different custody. Her boundaries at the airport, cottage, café, investigation and ending form a continuous character line, not a single rescue event.
- **Mixed institution:** Westmere performs lawful work alongside restricted misuse; the ending confirms some restricted cases legitimate. The film cannot turn every worker, recipient or record into knowing wrongdoing without contradicting the source.
- **Consequences:** Reyes's death, Voss/Vale's testimony, Mac's disclosure, Cain's charges and Helen/Brian's admissions each retain accountability. Charges are not convictions, and a cooperative act does not erase earlier conduct.

## Remaining gates and limits

1. The author is reviewing the map. Record any corrections against specific source units before treatment locks a narrative spine.
2. A treatment must decide presentation order, viewpoint, evidence legibility and what source functions fit the running time. Register every KEEP/COMPRESS/MERGE/OMIT/RELOCATE/VISUALISE/VOICEOVER/SPLIT choice afterward; none is assigned here.
3. Exact calendar dates, detailed institutional legal realism and final custody arrangements beyond the narrated ending are not inferred from this audit.
4. This audit did not render or visually compare the PDF pages and did not re-run KDP publication checks; it used extracted text solely for story-version reconciliation.

Validation at completion: `python tools/verify_film_source_map.py`, `python tools/verify_film_workspace.py`, `python tools/verify_workspace.py`, JSON parse of the manifest, and `git diff --check`. No `Active/Production/`, `Reference/` or `Archive/` files changed.
