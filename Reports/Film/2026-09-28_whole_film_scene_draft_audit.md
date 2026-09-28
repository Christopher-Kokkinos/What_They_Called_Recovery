# Whole-film scene draft v0.1 audit — 2026-09-28

## Scope and status

The author requested the remaining scenes as a combined review pass to assess chronology and consistency. `Active/Film/01_Adaptation/Screenplay/Whole_Film_Screenplay_v0.1.fountain` now contains SC001–SC057 in twelve sequences. SC001 reproduces the previously accepted direction; SC002 and SC003–SC057 remain draft. The scene index gives a compact route through the film. Each of the 230 provisional register rows now points to one intended draft scene, except `SRC-C41-02`, which points to the approved early/later split (SC019 and SC048). `SRC-C18-01` is provisionally classified RELOCATE because the contractor split is presented after the pair's trailer/farmhouse move; no source chronology is asserted to change.

**This is a compact scene pass of approximately 7,800 words, not a feature-length shooting screenplay.** Some scene IDs group more than one location and may need separate production sluglines. Dialogue, performance, duration and the degree of dramatization require development after the combined review. A register target is a planned carrier, not evidence that every detail of a KEEP unit has already appeared on screen. Source-by-source scene acceptance remains the next gate.

## Whole-film dependencies checked

| Dependency | Present screen carrier / boundary |
|---|---|
| Elias before Zoe | SC001–SC004 keep pain, pills, notice, Mrs Doran, evidence-first clamp, clinic call, convoy and Mac's airport diversion. |
| Zoe's account | SC011 hands the story to Zoe; SC012–SC017 run Tuesday through Monday as bounded memory; SC018 returns to the missed grandmother exit. Folder contents are not known when taken in SC014. |
| Earned trust | Negotiated doors/calls (SC006–SC008), the timed fallback (SC009–SC010), cottage revision (SC021–SC022), Zoe's market observations (SC024), her challenge after Reyes (SC026–SC027), refusal of transfer (SC029), evidence leadership (SC031 onward), independent wishes (SC051–SC057). |
| Hunters | Distinct Voss, Vale and Reyes assessments; Reyes's unilateral lock-up breach and death; Voss/Vale's old-job reconstruction, bounded statements and later interviews. Kindness is not absolution. |
| Jackie knowledge | SC019 shows only survival and coercion to the audience. SC047 carries the three likely messages and first/second-route distinction to Zoe; SC048 authenticates by private response and gives fuller sibling leverage. |
| Evidence | Offline original/copies, hypothesis AC019, specific changed order versus independent court copy, North Vale's challenge, Westmere preservation, contractor/carer accounts, limited disclosure and recorded original-drive handover. |
| Ending | SC056 treats charges as charges and historic cases as open. SC057 preserves Elias's stated wish, Zoe's participation and the novel's ridge choice. |

## Known development questions, not silent approvals

- The scripted scenes are deliberately concise. Pacing cannot be derived reliably from word count; a read-through and animatic should determine whether this structure supports a feature duration and where dramatic beats need room.
- Some research turns are compressed into screen actions or document comparisons. During scene review, test whether a first-time audience can distinguish hypotheses, supplied-channel confirmations and independent proof without explanatory overload.
- SC001's previous-dependence and Mac-work history need later explicit carriers if the audience must know their detail. The visible drawer and notice do not prove the full backstory.
- SC019's early captivity staging must be checked so it reveals Jackie's survival without revealing which route she withheld. SC047 must precede SC048.
- Grouped `INT./EXT.` scenes and rapid location transitions are planning conveniences. Split into precise screenplay/production scenes before scene packets, location assets, timing or shots are approved.
- The 167 provisional KEEP decisions were source-planning choices. The compact draft cannot be treated as implementation approval for all of them merely because each has a linked scene ID. Any lost function requires a revised disposition and traceable transfer.

## Mechanical validation

`python tools/verify_film_screenplay_draft.py` checks the 57 ordered scene IDs, twelve sequence headings, 230 source links, the single split link, key reveal/order boundaries and unchanged SC001/SC002 standalone scene text in the compilation. Run it with the existing source-map, film workspace and workspace verifiers, JSON parse and `git diff --check` before publishing. Canonical manuscript, publication master and locked references remain untouched.
