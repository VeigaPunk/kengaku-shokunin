# FBoundaryNoAxisHarm — integrated-claim boundary / no-axis-harm falsification (round28)

Seat: `KengakuR28.FBoundaryNoAxisHarm` (critic, leaf, author-side; not outside closure).
Scope: C1 new corpus ground + C2 error correction, scores held novelty7/calibration8, coverage cap
unresolved, no harm on unclaimed axes, no old knowledge left false/unmarked. Attacked the final wording.

Inputs read (exact):
- Frozen candidate `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, re-hashed
  SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (matches `candidate-freeze.json`).
  Canonical path `corpus/knowledge/webarena-task-spec-audit.md` is absent (not admitted), as stated.
- `plans/round-28-claims.md` including Amendment 1; `corpus/lessons/round-28.md`.
- `git diff b9b24796..18b19226` for `corpus/SOURCES.md`, `corpus/README.md`, both edited baseline knowledge
  files, `SCORECARD.md`, `LOG.md`, `SKILL.md`; acceptance receipts under `corpus/evidence/round28-calibration/`;
  `plans/fixtures/r28/acceptance.py`; pinned `evaluators.py`/`helper_functions.py`; build `OpenS038.md`,
  `OpenS051.md`, `CritClaimScope.md`, `OpenTasks.md`.
- Instrument digests re-hashed and equal to the freeze record: benchmark_spec_audit `f72a8569…`,
  registry_check `41561dfb…`, state_check `5db1eb78…`.

No builds/tests/checkers rerun. One read-only inline JSON census of `test.raw.json` (stdlib `json` only,
`python3 -B`, no upstream import/exec, no file writes). No tool installs or updates.

## Findings

### F1: S066's anchor cell leaves out the page where its supporting quote is (fixable calibration defect)

Counterexample: SOURCES row S066 (landed tree, line 88) gives its anchor as
"Introduction/Methods p.1675 and Conclusion p.1677". Its teaches clause rests on the caveat that the exact
construction "assume[s] that sensitivity and specificity are known exactly". That caveat is located elsewhere:
- `corpus/lessons/round-28.md:45` locates the S066 quote at **Discussion p.1677**.
- `corpus/knowledge/attribution-interval-calibration.md:196–197` also cites **Discussion p.1677**.
- `build/OpenS038.md:31,39` places the "known exactly" caveat in the **Discussion**. The Conclusion quote
  (`OpenS038.md:32`) is a different sentence, about adjusting CIs under known Se/Sp.

So the new row's anchor disagrees with its own lesson quote and with the knowledge erratum. The lane keeps
catching this kind of source-location drift (M66, S048). It sits outside the frozen13 IDs, so the C2 counters
are unaffected, and the candidate does not cite S066. It does mean a correction meant to fix an "old false"
row starts life slightly mislocated.

Impacted axis: calibration.

Smallest safe correction: S066 is a new round28 row, not an immutable baseline cell. Before admission, add
"Discussion p.1677" to its anchor cell, or record an explicit lesson disposition.

### F2: "applies exact_match before must_include" misdescribes an if/elif (advisory wording)

The candidate's Page content row (line 34) says the HTML evaluator "applies exact_match before must_include".
`S062:305–312` is `if "exact_match" in … elif "must_include" in …`, which is exclusive. When `exact_match` is
present, `must_include` is never evaluated.

My census found 0 targets with both keys (188 exact-only and 463 must_include-only, total 651). This matches
the candidate's "effective operators" counts, so no number changes and the pinned population takes no harm.
The risk is a reader applying this rule to a later snapshot that has both keys and assuming both predicates
are applied.

Impacted axis: calibration, wording only.

Smallest correction: "uses exact_match if present, otherwise must_include".

### F3: Amendment1 §4 assigns S064–S066 to C1 by its literal wording (advisory partition ambiguity)

§4 says "C1 owns new source rows/new knowledge". S064, S065 and S066 are new rows, but they are calibration
corrections. They are cited only by the calibration errata appended to baseline knowledge:
`extraction-policy-comparison.md:128–131` cites S064/S065, and `attribution-interval-calibration.md:194`
cites S066. The lesson already calls them "supplementary corrections … not 3 new publications".

The measured revert experiment is sound. In `acceptance.py:56–92` the baseline export lacks both the errata
and these rows, and neither counter counts them. However, an indiscriminate "revert C1 rows" on the final tree,
as §4 literally reads, would leave baseline knowledge citing absent rows.

Impacted axes: separability and provenance. No counter is impacted.

Smallest correction: one sentence in the lesson or SCORECARD placing S064–S066 in the calibration-errata
partition.

## Bounded no-objections (tested, no counterexample found)

1. **Amendment1 §5 (errata add no new edge to a frozen13 ID).** I compared the per-file ID sets at baseline
   and landed:
   - `attribution-interval-calibration.md`: the only new ID is S066 (S038 goes from 1 to 2 mentions).
   - `extraction-policy-comparison.md`: the only new IDs are S064 and S065. S049/S050/S051/S054/S058/S059
     only gain mentions, and each was already cited.

   `reference_links=12` holds in all five registry receipts (baseline-red, s050-only-red, s038-only-green,
   current, alternate).
2. **Old knowledge is marked, not silently left false.** Each known-false or overbroad baseline statement
   has a successor marker:

   | baseline statement | where it is marked |
   |---|---|
   | S049 `extraction.py:25` in the header | erratum at `extraction-policy-comparison.md:118` |
   | S038's unqualified fix clause | S066 supersedes it, plus the knowledge erratum |
   | S054's length shorthand | S064 supersedes it |
   | S051's exception breadth | knowledge erratum (row unchanged, per `OpenS051.md:92` advice) |
   | S053/S059 RFC-versus-lane comparison | erratum, plus S065 for the Python-side authority |
   | S050's corrective index reversal | explicit in the lesson and the erratum; S058 stays controlling |

   Round27 lesson M61 ("25, not 27") and lines 159/203 ("S050 lesson-only") are historical records left as
   written. They are explicitly reversed in round28 M66/M67 and the erratum, which follows the lane's
   append-only convention.
3. **Historical preservation.**
   - `build-preservation-corrected.json` gives 329/318/0/6/5, with out-of-population 28 = 26 old + 2 new.
   - `state_check.py` is byte-equal to the freeze digest.
   - The two-way revert asserts (`acceptance.py:83–92`) come before the failing line-97 assert, so they ran
     and passed in the red run. SCORECARD's "two-way revert counters agree" is therefore supported.
   - Nobody claims the whole initial harness passed.
4. **Scores and unclaimed axes.**
   - SCORECARD records 7→7 and 8→8, with depth9, coverage7 capped, operability8, freshness8 and adjacency8,
     the same as the round25/27 rows.
   - Candidate lines 140–141 deny coverage-cap relief and method novelty.
   - README states no frontier discharge.
   - Index parity holds: knowledge 35/35, lessons 31/31, evidence 21/21.
   - SKILL.md gains only two gate rows, each stating "NOT task validity" or "NOT source truth".
5. **Candidate source anchors match the pinned bytes.**
   - S062: 80–94, 98–111, 134, 142–149, 150–169, 159 (N/A assignment override), 187–239, 199–235 (pooled
     query values), 258–333, 271–301, 348–352, 361–374.
   - S063: 146–173, 161–173 (`gpt-4-1106-preview`), 176–208, assertions at 172 and 207.
6. **Independent census reproduces the selection.** 27 strata; the selected IDs equal
   `selected-task-ids.json` (389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399); all 36 N/A tasks
   use fuzzy_match only, which supports the claim at candidate line 47. The eval-type-set and site-set
   histograms each sum to 812.
7. **Pin date.** "committed 2025-11-26" has no support in `manifest.json`, but is supported by the GitHub API
   evidence in `CritClaimScope.md:49` and `OpenTasks.md:23`.

Admission advisory (not a current defect): if the candidate is admitted, any frontier marker must say
"partly discharged", limited to this WebArena snapshot. The frontier's named next sources (Terminal-Bench 2.0,
Toolathlon, SWE-bench Pro) and its contamination clause stay open.

## Verdict

The candidate bytes (`77e19d5b…`), planned for the canonical path `corpus/knowledge/webarena-task-spec-audit.md`,
gave me no counterexample that falsifies a C1 claim, C2 claim, score hold, cap statement or unclaimed axis.
The integrated round state is not fully clean:
- F1 is a real source-location defect in a new calibration row.
- F2 and F3 are fixable wording and partition advisories.

None of these changes a counter. Under the "complete support" rule this is not a PASS. It becomes a PASS
from this seat once F1 is corrected or explicitly dispositioned; F2 and F3 are recommended.

VERDICT: PARTIAL
