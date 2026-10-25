# FFrontierGate — round28 frontier and admission-conformance falsification

Seat: `KengakuR28.FFrontierGate` (author-side falsifier; not outside non-author closure).
Date: 2026-10-21. Axes: legacy novelty→canonical coverage/constructs7, calibration8 (held).
Candidate: frozen draft `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, SHA256
`77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (re-hashed; matches
`candidate-freeze.json`), writer KengakuR28. Canonical candidate path
`corpus/knowledge/webarena-task-spec-audit.md` is **absent** (not admitted). Tree read: lane working copy
`7d987564` (empty) over master `18b19226`; baseline `b9b24796`.

Scope is the frontier/admission boundary only. This is not a full Q10 source/number reread of the
candidate and gives it no source or number approval.

## Held: verified with no counterexample

1. **New six source rows: URL, date and a located quote of at most 25 words.** The lesson
   (`corpus/lessons/round-28.md:40–45`) records URL, `2026-10-21` and a located quote for S061–S066. Each
   quote was checked against retained bytes:
   - S061 `test.raw.json:18–21`: the eval object lines 19–21 contain the quote, with whitespace collapsed.
   - S062 `evaluators.py:351`: `score *= cur_score`.
   - S063 `helper_functions.py:169`: exact.
   - S064: `scratch/OpenS054/commonmark-0.31.2.html:2743`, wrapped across lines, with examples 124 and 125 present.
   - S065: `scratch/OpenS052/json-v3.15.1.rst:688–689`, under heading :684. Only reST markup differs.
   - S066: `scratch/OpenS038/wb20261004.pdf`. The quote sits in the right column under DISCUSSION, after
     page header 1677 and before CONCLUSION.

   The quotes run 4–18 words. Kind and recheck values are existing enum values. Tiers are A with
   narrowed scopes (S061 "not runtime task validity or paper-era scores"; S062 "not WebArena-Verified or
   actual browser outcomes"; S063 "not judge accuracy"). The `gpt-4-1106-preview` claim (S063:162/197) and
   the class and router line anchors (S062:71/173/244/336/356) match. Each new row's used-by matches its
   corpus literal citers exactly: S061–S063 are cited only by the lesson; S064/S065 by the lesson and
   `extraction-policy-comparison.md`; S066 by the lesson and `attribution-interval-calibration.md`.
2. **Old→new for existing cells.** A cell-level diff of `SOURCES.md` from b9b24796 to 18b19226 shows S038
   changing only status (queued→mined) and used-by (—→attribution-interval-calibration.md). S050 changes
   only used-by (adds extraction-policy-comparison.md). S038's opened `2026-10-20` and recheck `180d` are
   unchanged. This matches lesson:64–68 exactly. The S049 header correction from 25 to 27 is knowledge
   errata text, not a source-cell change.
3. **M65's red and green results come from the same unmodified checker, and the M65 change is the only
   difference between them.** I rebuilt the intermediate files in scratch: baseline `SOURCES.md` →
   b1a74eb5…; replacing only the S050 row → a06b7f65…; then replacing only the S038 row → 66e2235e….
   Each matches `registry-only-delta.json` byte-for-byte. The cells that differ are S038 [status, used-by]
   and S050 [used-by]. Next, I exported the baseline corpus into scratch and ran the delivered
   `registry_check.py` (sha 41561dfb…, which matches the freeze). Results:
   - baseline: exit 1, findings `cited_not_mined S038`, `missing_used_by S038`, `missing_used_by S050`;
   - with only the S050 change: exit 1, still failing on S038;
   - with both changes: exit 0.
   These are identical to the retained `registry-{baseline-red,s050-only-red,s038-only-delta-green}.stdout`.
   The final tree's `--summary` exits 0 with 13 rows, 35 paths and 12 links. Receipts:
   `scratch/FFrontierGate/replay-{base,s050,both}.json`.
4. **Knowledge stays pending until Q10 reports return.** The Gate row is `deferred`. README:302/323 assert
   no knowledge row and no frontier or coverage discharge. The Coverage map and Frontier are unchanged.
   SCORECARD does not claim capability in advance. Only six falsify reports exist at this time; none
   has been cited by a Gate cell.
5. **Outside spot-check stays roster-external.** Lesson §Outside spot-check, LOG and SCORECARD all keep
   lane-dispatched seats author-side. Nothing claims an outside verdict.
6. **QUALITY Q17 was added only after failure-capable evidence existed.** It cites the receipts replayed
   in item 3.

## Findings

### F1 (principal) — at admission, nothing would catch S061–S063 missing the new knowledge path in used-by, the same failure class as M65

- **Counterexample (scratch simulation):** I placed the exact frozen bytes (sha 77e19d5b…) at
  `corpus/knowledge/webarena-task-spec-audit.md` in a scratch copy of the current `corpus/`, leaving
  SOURCES unchanged. The candidate cites S061, S062 and S063, all `mined`, but their used-by holds only
  `corpus/lessons/round-28.md`. The delivered `registry_check.py --summary` still exits 0.
- **Why it passes:** this is by design. The frozen population excludes new rows and new files.
  `state_check.py` P4e covers only S043–S048. `round28_census.py` checks only README index-row
  bijection. No delivered command would fail on that admission tree. It would be exactly M65's
  cited-but-not-indexed failure, moved to rows outside C2's population.
- **What the plans say:** lesson:72–73 promises that "any later used-by change is separately recorded".
  Claims:31 and Q7 require the entry, README index row and coverage-map row to land together. Nothing
  makes either of these failure-capable at the admission commit.
- **Frontier gap:** README:258 names "Agentic benchmark task-spec audits" with next sources Terminal-Bench
  2.0, Toolathlon and SWE-bench Pro, a per-benchmark task-validity checklist, and separate contamination
  audits. Round28 replaces those leads with WebArena dce04686, and no claims or lesson text records why.
  The candidate (line 10) says only that it "Extends" the row. CritLowestAxis §4 asked that the closeout
  mark as covered only the static task-spec/scorer slice of the pinned snapshot; no pre-written discharge
  text exists.
- **Impacted axes:** coverage/constructs (frontier and coverage discharge could overreach) and
  calibration (an unchecked reference drift would recur in the very round that mined M65).
- **Smallest safe correction (for L1, in the admitting commit only):**
  - Add `corpus/knowledge/webarena-task-spec-audit.md` to the used-by of S061, S062 and S063, and record
    old→new in the lesson.
  - Add the README knowledge index row and a Coverage-map row (S061–S063, measured static depth).
  - Add a "Partly discharged round28" sub-bullet under README:258. Scope it to the WebArena dce04686
    static task-spec/scorer slice. State that Terminal-Bench 2.0, Toolathlon, SWE-bench Pro, contamination,
    live task validity and the per-benchmark validity checklist stay open, and record why WebArena was
    substituted.
  - Show a red/green result for the used-by change at the admitting commit, as a one-off literal census
    over S061–S066 and the new path. It must be kept separate from the frozen C2 population and must not
    count toward C2.
  - Confirm `round28_census.py` reports `unindexed: []` on that exact commit.

### F2 — the Gate rejection of "new scientific method or novelty score increase" has a reason that no evidence supports (Q9)

- **Counterexample:** lesson:27 gives as its reason "Reading task configs against scorer predicates is
  established evaluation practice", but cites no source and no prior-art evidence. F6 (claims:42) is
  conditioned on "after prior-art check". `build/ConnectScope.md:93` states "No prior-art or literature
  check was done". CritLowestAxis argues only that a novelty hold needs no search; it does not say the
  practice is established.
- **Rule broken:** Q9 says "A correct verdict with a wrong reason is a gate failure"; here the evidence
  for the reason is missing.
- **Matching evidence already in the corpus:** S005/S006 are self-audits of benchmark task validity, a
  property that matches the claim. `knowledge/benchmark-selection.md:18` also names WebArena-Verified as a
  re-audit lead. Neither is cited in the rejection.
- **Impacted axis:** novelty/coverage-constructs (the hold is right; the reason is unsupported).
- **Correction:** rewrite the reason to cite S005/S006, and state that F6's prior-art check was not
  performed, so F6 is informed-only and unresolved. The verdict and flip condition stay as they are.

### F3 (minor) — the S066 anchor omits where its own quote is located

- **Evidence:** the `SOURCES.md` S066 anchor reads "Introduction/Methods p.1675 and Conclusion p.1677".
  The row's load-bearing quote and its supersession teaching sit under **Discussion** p.1677, as the
  lesson:45 and knowledge errata say and the PDF layout confirms.
- **Impacted axis:** calibration (Q10 location precision).
- **Correction:** record an append-only location erratum in the lesson, or add Discussion p.1677 to the
  anchor before admission. The row's scope and teaching stay unchanged.

### F4 (observation, not blocking)

- **No `evidence/round28-sources/` directory.** Rounds 24–27 kept located opening quotes under
  `corpus/evidence/roundNN-sources/`; round28 keeps them only in lesson:40–45. The content requirement is
  met, but the established convention is not followed.
- **S064–S066 ownership is ambiguous.** Amendment 1 item 4 says C1 owns new source rows. Item 5 says new
  C1 links never edit baseline35 knowledge paths. S064–S066 are new rows whose used-by is baseline35
  knowledge files, and LOG labels them calibration errata. No checker reads these rows, so the
  separability results are unaffected, but the row partition should name their owner explicitly.

## Exercised operations

- Read the claims (including Amendment 1), the lesson, the frozen candidate, QUALITY, SOURCES, README,
  LOG/SCORECARD diffs, `CritLowestAxis.md` and `gate_timing_check.py` logic.
- `jj diff` and `file show` were read-only. Wrote only under
  `.ufo/waves/round-28/scratch/FFrontierGate/` (SOURCES variants, baseline export, replay JSON;
  admit-sim corpus copy removed).
- Ran `registry_check.py` three times on the scratch baseline export, once with `--summary` on the lane
  root, and once on the admit-sim copy, with `PYTHONDONTWRITEBYTECODE=1`. Used pdftotext and rg on the
  retained source receipts.
- No production edits, no upstream code execution, no network access, no benchmark contact, no
  installs or updates.

VERDICT: PARTIAL — the six new source rows, the old→new cell changes, the M65 red/red/green replay, the
pending-knowledge state and the outside-roster boundary all hold. However, admission conformance has
an unmet, failure-capable requirement (F1: used-by for S061–S063 plus the frontier, coverage and index
rows), and the novelty rejection's reason is not supported by cited evidence (F2). F3 and F4 are minor.
