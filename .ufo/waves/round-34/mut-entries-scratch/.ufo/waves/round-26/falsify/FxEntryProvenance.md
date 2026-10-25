# FxEntryProvenance — source provenance review

Candidate reviewed: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/drafts/grader-perturbation-audit.md`; intended destination: `corpus/knowledge/grader-perturbation-audit.md`.

## Triad, writer, and source rows

- Draft lines 1–3 have the required `source:`, `verified-at:`, `recheck:` order. `verified-at: 2026-10-21` matches the source-opening date recorded for S044–S048 in `corpus/SOURCES.md:66-70` and `corpus/evidence/round26-sources/gate.md:1,32-40`. Recheck cadence and actions are explicit.
- `writer: KengakuR26-2` at draft line 4 matches the round-26 plan's named L1 author (`plans/round-26-claims.md`, opening header); no identity discrepancy observed.
- S048, S044, S045, S046 are all `mined` and have nonempty `used-by` entries in `corpus/SOURCES.md:66-70`; each currently points to `corpus/lessons/round-26.md`, consistent with the entry still being unadmitted. Add the knowledge-entry path to `used-by` if/when admitted. S047 is not cited in this draft.
- S048: tier A is scoped to CheckList's original model-input INV/DIR method, not grader validation (`SOURCES.md:70`). The exact quoted definition is at §2.2, PDF p.3 / proceedings p.4904; direct PDF read confirmed the quote there. The initial S043 p.2/p.4903 location is explicitly superseded by S048 in `corpus/evidence/round26-sources/gate.md:32-40` and `corpus/lessons/round-26.md:57-66`; the draft correctly cites S048.
- S044: tier A is scoped to xFinder's own extraction motivation/method, not general extractor accuracy (`SOURCES.md:66`). Its v3 date (2025-02-25), Abstract, PDF p.1 and 2026-10-21 opening date are consistent with `build/SrcXFinder.md:5-10` and registry row S044. Direct abstract read confirms the cited RegEx-extraction motivation. The draft calls it adjacent, not grader validation.
- S045: tier B correctly marks community-tooling documentation as evidence of shipped mechanism, not correctness (`SOURCES.md:67`). The 0.1.0 README section and release date 2026-08-10 are located in `build/SrcToolingPyPI.md:10-16`; direct PyPI page read confirms the equivalent-change/brittle-spot description. The draft uses it as direct tooling prior art and holds novelty at 7; it does not present evalmut as independent validation.
- S046: tier A is correctly scoped to official Python regex semantics, not method prior art (`SOURCES.md:68`). Python 3.15.0 and the `\s` CR quote are located in `build/SrcPythonJsonRe.md:9-15`; the direct docs read identifies Python 3.15.0. **Actionable Q1 defect:** draft line 1 gives only “Regular expression syntax,” while the exact cited anchor in `SOURCES.md:68` and `round26-sources/gate.md:8` is “Regular expression syntax → special sequence backslash-s.” Amend the source-line anchor before admission; Q1 requires the exact anchor (`corpus/QUALITY.md:15-18`).

## Independence and execution record

No external source is represented as independent validation of itself. The draft explicitly limits CheckList to model prediction invariance, xFinder to adjacent extraction research, evalmut to published tooling mechanism, and Python docs to regex behavior (draft lines 17–21, 49–50); its observed corpus rates are attributed to its pinned local instrument/oracle, not to those sources. S045's self-reporting limitation is explicit in `SOURCES.md:67` and the source receipt (`round26-sources/gate.md:11-13`).

Read-only source and repository reads only; no shell commands, package installs, or production edits. Command exit status: not applicable. External source opens: ACL PDF, arXiv abstract, PyPI project page, Python docs; see exact paths/URLs above.

Residual admission note: round-26 Gate currently defers this candidate pending second-seat Q10/Q13 requirements (`corpus/lessons/round-26.md:29-41`). This report checks provenance only, not the other admission criteria.

VERDICT: PARTIAL — citations, tiers, writer, dates, and self-validation boundaries are supported, but S046 lacks its exact `\s` source anchor in the required Q1 triad.

## Scoped Q1 re-read (2026-10-21)

L1 reports the unadmitted draft's S046 triad citation was corrected to `https://docs.python.org/3/library/re.html#regular-expression-syntax`, specifically the `\s` special sequence (Unicode whitespace including CR). Treating that reported change as ground truth, the exact-anchor Q1 finding above is closed for this criterion; I did not re-open or edit the draft. The original PARTIAL verdict is retained as the initial snapshot. This is not a complete Q10/Q13 admission review.

VERDICT: PARTIAL — initial provenance review was PARTIAL; the S046 anchor criterion is reported corrected, but this scoped re-read does not clear the other admission requirements.