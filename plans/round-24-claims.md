# Round 24 — declared claims (pre-registered before the L2 swarm)

Lane: kengaku. Steered round 24 (kaika steer table). Base `99cf615`, branch
`kaika/round`. Round 23 executed (30 stream trials, `ACCURACY: 30/30`) but its
target clause failed (`corpus/evidence/attrib-r23-stream.log:239`:
`STREAM TARGET opencode-go: on-target GT n=0 ... -> FAIL`) and was never
recorded; this round records it NOT-ADMITTED (claim C2) and does not re-run it.

Counting command for every number below: `sh plans/round24_census.sh` (lane
root). Before = output at `99cf615`.

Axis state at base (last numeric, `SCORECARD.md:162-168`): novelty 7,
calibration 8, depth 9, coverage 7, operability 8, freshness 8, adjacency 8.
Lowest non-retired: coverage 7 tied with novelty 7. Novelty +1 needs a new
probe construct with an in-repo instrument (`SCORECARD.md` §Scoring rubric);
no probe runs this round, so coverage is the lowest-axis claim. No stagnation
waiver is invoked (saturation line not yet declared; C2 declares it).

## C1 — coverage (lowest, 7): sourced expansion onto uncovered ground + the SOURCES capability

Move: create `corpus/SOURCES.md` per contract v1 (opened rows only, honest
tiers, ≥1 rejected row with reason+flip, `## Paths`, `## Search log`); admit
4–5 new `corpus/knowledge/` entries on ground the coverage map lacks
(contamination detection, judge calibration, benchmark saturation, agentic
time-horizon/task validity, paired uncertainty reporting), each opening with
the `source:`/`verified-at:`/`recheck:` triad and clearing
`corpus/QUALITY.md` §Admission bar; restore index parity both directions
(knowledge, lessons, root evidence logs, plans); add `## Frontier` to
`corpus/README.md`; append a Core/Frontier/Adjacent province map to
`PROVINCE.md` that re-verifies every surface today and keeps absent surfaces
enumerated under a historical heading (never deleted).

| census key | before (99cf615) | after target |
|---|---|---|
| C1.knowledge_files / rows / unindexed | 27 / 24 / 3 | 31–32 / = files / 0 |
| C1.lessons_files / rows / unindexed | 24 / 19 / 5 | 25 / 25 / 0 |
| C1.root_logs_indexed | 0/28 | 28/28 |
| C1.plans_indexed | 0/8 | all/all |
| C1.coverage_map_rows | 11 | ≥15 |
| C1.frontier_rows | 0 | ≥3 |
| C1.full_triad_knowledge | 0 | ≥4 (the new entries) |
| C1.sources_rows | absent | ≥15, census clean |
| C1.quality_admission_criteria | absent | 8 (Q1–Q8) |
| C1.province_core_sections | 0 | ≥3 |

Score rule (fixed now): coverage 7→8 only if every unindexed count is 0
**and** every PROVINCE Core row resolves with a dated `test -e` receipt
**and** absent surfaces stay enumerated. If the critic rules that SKILL.md's
remaining current-tense absent paths still trip the unresolvable-surface cap,
coverage is recorded `improved, held at 7 (cap)`.
Capability row `sources-registry` enters only if every contract census command
runs clean on the landed file.

## C2 — calibration (owned, 8): learn from the lane's own mistakes; record round 23 honestly

Move: `corpus/lessons/round-24.md` `## Mistakes` mines the lane's rejected,
harmed and honest-stop rounds (STATE dossier §4, M01–M18, each pointer
re-verified) as class · evidence pointer · captured-by criterion or `none` ·
fix; `corpus/QUALITY.md` gains `## Round-closure criteria` (R-rows, each
citing `corpus/lessons/round-24.md` and the source lesson) for every
uncaptured class; LOG.md and SCORECARD.md gain a Round 23 record
(NOT-ADMITTED, the `:239` FAIL quoted); SCORECARD declares the saturation line
and stagnation window, refreshes `planned`, appends errata for the stale
`149 checks` line, and enters demonstrated capabilities.

| census key | before (99cf615) | after target |
|---|---|---|
| C2.lesson_mistake_rows | absent | ≥18 |
| C2.quality_closure_criteria_citing_lesson | absent | ≥5 |
| C2.round23_sections (LOG SCORECARD) | 0 0 | 1 1 |
| C2.not_admitted_lines (LOG) | 0 | ≥1 |
| C2.saturation_declared | 0 | 1 |
| C2.capability_rows | 0 | ≥1 |

Score rule (fixed now): rubric clause (d) requires landing in the round the
probe ran; r23 lands late, so — exactly as round 14 ruled for r12 —
calibration is recorded `improved, held at 8 (late-landing breach)`; the
counts above are the falsifiable move. No score is bought by late landing.

## Separability

C1 is verifiable from `SOURCES.md`, the new knowledge entries, README and
PROVINCE alone, against `QUALITY.md` §Admission bar (created at round start,
before either claim's work). C2 is verifiable from the round lesson,
`QUALITY.md` §Round-closure criteria, LOG and SCORECARD alone. Neither claim's
counts change when the other's files are reverted.

## Harm checks (no axis may drop)

depth: SKILL.md grows by ≤3 lines (one SOURCES pointer); no knowledge deleted
(`git diff --diff-filter=D --name-only 99cf615 -- corpus/knowledge` → empty).
operability: `python3 grader.py` still exits 0. freshness: every new entry
carries `verified-at: 2026-10-19`. adjacency: connector routes sibling overlap.

## Amendment 1 — after the pre-registration review and critic (2026-10-19, before commit)

Inputs: PreregReviewer-3 (14 defects, census false-pass modes a–j), ClaimCritic-3
(binding coverage ruling), RoundPlanner-3 (separability breach). Applied:

1. **Census v2.** `plans/round24_census.sh` now matches backticked index rows
   only, checks the row→file direction (`dead_index_rows`, `dead_plans_rows`),
   tests the triad on the first three lines, scopes Round-23 checks to the
   `## Round 23 ` sections, counts R-criteria that cite round-24.md plus a
   mistake id, requires the stagnation window, and adds
   `C2.scorecard_state_defects_open`. Base output re-taken on a `git archive
   99cf615` tree: `corpus/evidence/round24-census/base-99cf615.txt`
   (identical base numbers to v1 for every shared key).
2. **No row quota.** `C1.sources_rows ≥15` is withdrawn (contract rule 4).
   C1's expansion key is `C1.expansion_entries_on_mined_rows` (0 → 5): entries
   with the triad whose `source:` cites a `mined` row that lists them.
3. **QUALITY §Admission bar is a prerequisite, not a C1 outcome.** It was
   written before any admission and is excluded from C1's measured moves. Its
   Q1/Q2/Q3/Q5 citations were tightened pre-commit (reviewer defects 6–8, 14):
   wording of support only, no criterion added or removed.
4. **Separability made explicit.** C1's lessons key excludes `round-24.md`
   (`lessons_unindexed_excl_round24`, 5 → 0); round-24.md and its index row
   belong to C2. C1's admit/reject gate lives in `## Gate` of round-24.md and
   in `corpus/evidence/round24-sources/gate.md`; that section is C1 content
   inside a C2 file — verifiable on its own, declared here as a shared file.
5. **Coverage score: hold at 7** (critic binding ruling — appending a
   Historical-absent province section does not clear the
   declared-but-unresolvable-surface cap; `round-13-coverage.md` §Gate). C1 is
   reported `coverage 7 → 7 (held by cap)` with its counts as the measured move.
6. **C2 restated.** The calibration move is measured as
   `C2.scorecard_state_defects_open` 6/6 → 0/6 (SCORECARD entries made to match
   repo state: D10–D14, D16) plus mistakes mined and closure criteria. Score
   `8 → 8 (held)`: rubric +1 needs an in-round scored probe (clauses a/b/d), and
   late recording buys nothing (r14 precedent). Critic and planner L2s judge
   this bookkeeping rather than an axis-move; that dissent is reported, not
   overruled — the operator rules.
7. **Capabilities.** Rows enter only for capabilities run in round 24:
   `offline-replay-gate` (`python3 grader.py`), `frozen-table-pin-check`
   (`plans/attrib_probe.py block-sha`), and `sources-registry` only if every
   contract census command runs clean on the landed file.
8. **Discernment** is not claimed: the non-author spot-check (≥1 admit, ≥1
   reject) is the orchestrator's, after landing.
