author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 87 — non-author verifier spot-check

Subject: lane round 87 (hyaku run 15, attempt 1), lane HEAD `6b7e83aa2aabdc26089830986e8ee2e04a2ba00d`
(`master`, remote `refs/heads/master` identical). Base `b9be687774e6b559470f5b0d9b936315b51ff311`.
Report: `.ufo/reports/round-87/kengaku.md`, committed in the fleet repo as `bc4c38c9` by
`kengaku-shokunin <kengaku@shokunin.local>`. Written by a closure session that did not author any
round-87 bytes. Nothing in the lane's own files was edited by this pass.

Method disclosure: plain measurements (`git show`, `grep`, `awk`, `sha256sum`, `curl`, `python3` over
committed bytes) were run by this integrator. The lane's counters (`plans/round87_c1_replay.py`,
`plans/round87_c2_wording.py`) were **not** executed; their committed transcripts were verified as
evidence. The captured grader was replayed by this integrator in a plain Python harness (path rewritten
to a temp file, `AssertionError`/`FileNotFoundError` = F, other exceptions = E, pass = P) over the frozen
case table. That run is independent of the lane's bubblewrap probe, which was only verified by its receipt.

## 1. Conformance (protocol step 1)

| check | observed | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-87/kengaku.md` → `kengaku-shokunin bc4c38c9…` | pass |
| report is a real report, not a marker | named commits, work items, evidence pointers, Landed-changes table, before→after table, Sources & frontier, Trend verdicts, `SHONEN` heading with four lines | status `ok` |
| cited commits exist and are ancestors of `master` | `merge-base --is-ancestor` for `b9be6877`, `b0f07651`, `21da383b`, `10de494d`, `6b7e83aa` all pass against `master` | pass |
| lane pushed, no round leftovers | `jj-lane.sh state …kengaku-shokunin` → `branch=master local=6b7e83aa… remote=6b7e83aa… ahead=0 behind=0 untracked=0`; `git status --porcelain` empty | pass |
| remote tip | `git ls-remote origin refs/heads/master` → `6b7e83aa…` | pass |
| driver lines (digest, `.ufo/watchdog.log`) | `2026-11-05T00:44:04-03:00 launch kengaku round=87 pgid=1767021 driver=hyaku-inline attempt=1`; `2026-11-05T01:56:38-03:00 complete kengaku round=87; hyaku-inline attempt=1`; no `lane-dead-no-report kengaku round=87` line | matches the dispatch digest |
| prompt template contract | `.ufo/prompts/kengaku-round-87.md` carries §1 mission binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract with the `SHONEN` heading, §5 push scope and L0 channel. Commit-before-report ordering and lane write scope appear only in §5 prose, not as named items | minor template defect, routed to the operator (not the lane) |
| L2 floor (≥8 L2 subagents in one batch, MISSION §L2) | zero seats dispatched: `w1.ready` present, `w1.ready.dispatched` absent, report says `Round total seats run: 0` | **conformance defect**, status-neutral; does not bar admission (protocol: undispatched wave) |
| stale-lane clause | report names no open mission as progressing or silent; it calls the round wave "unsettled" | minor conformance defect |
| L2 route map vs MISSION bucket | prompt §6 quotes alias-level routes; MISSION §L2 names buckets; the alias→bucket table is not in the repo, so no contradiction is checkable | not checkable, noted |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `ok … corpus/SOURCES.md`, exit `0`. W04 lines are duplicate-URL advisories across scopes; I did not diff them against base | exit 0, pass |
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`: base 266, head 268 | matches report |
| tiers | awk tier histogram base `A=236 B=24 C=6`, head `A=238 B=24 C=6` | matches report |
| status histogram (head) | `mined=243 queued=8 rejected=17` | matches report (`mined 242→243`, `rejected 16→17`, `queued 8`) |
| frontier step present | S275 admitted (`mined`), S276 rejected with flip; lesson `## Mistakes` present with three rows; sourced claim C1 cites S275 | pass |
| L0 side channel | `.ufo/l0-questions.md:312` `kengaku | round-87 | Wave w1 …` | present |

## 2. Claims — re-derived against `6b7e83aa`

Frozen claim file `plans/round-87-claims.md` and case table `plans/round87-cases.json` are byte-identical
from freeze `b0f07651` to HEAD (`git diff --stat b0f07651 HEAD -- <those files>` is empty). The instruments
(`plans/round87_*.py`) first appear at `21da383b`, after the freeze. `SCORECARD.md` changed by 23 insertions
and 0 deletions (`git diff --numstat b9be6877 6b7e83aa -- SCORECARD.md`), so no existing axis score row moved.

### R87-C1 — coverage: fifth located replay (`mteb-retrieve`)

Re-measured by this integrator (plain counts over committed bytes):

- Ledger executed rows, `plans/grader-population-ledger.json`, via
  `python3` `json.load` over `git show <rev>:…`:
  base `b9be6877` → `executed 30 total 88`; head `6b7e83aa` → `executed 31 total 88`. **30 → 31 confirmed.**
- `file-artifact` membership (`'file-artifact' in classes`): base `76` members, `22` executed; head `76` members,
  `23` executed. **22 of 76 → 23 of 76 confirmed.**
- `mteb-retrieve` ledger row at head: `status: executed`, `round: 87`, `receipt: corpus/evidence/round87/mteb-retrieve-probe.txt`.
- Subject bytes: `sha256sum corpus/evidence/round52/graders/mteb-retrieve/tests/test_outputs.py` →
  `e4e6b21fed6662adb4a42aba23d35609450392839a2282f3ba77c70c8d907c0b`, equal to the receipt's `SUBJECT_SHA`.
  Live fetch `curl -sS -o … https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-retrieve/tests/test_outputs.py`
  → `200 559`, sha `e4e6b21f…c0b`, `cmp` silent against the round-52 capture.
- Case table: `sha256sum plans/round87-cases.json` → `848eac38…be86b`, equal to the receipt's `CASE_TABLE_SHA`.
- Independent replay of the captured grader over the eight frozen cases (this integrator's harness):
  `exact P/P=P/P`, `absent-file F/F=F/F`, `two-lines P/F=P/F`, `sibling-value P/F=P/F`, `trailing-space P/P=P/P`,
  `empty-file P/F=P/F`, `result-is-directory P/E=P/E`, `non-utf8-bytes P/E=P/E`. `all predicted==observed: True`,
  8 cases, 16 legs.

Evidence-verified (committed transcripts, not re-executed):

- `.ufo/waves/round-87/L1/base-runs.txt`: `TARGET executed_rows=30 member=mteb-retrieve located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`, `PREDICATE R87-C1 fail`, rc 1. Defects `L4-table`, `L1-receipt`, `L7-ledger`.
- `.ufo/waves/round-87/L1/tip-runs.txt`: `TARGET executed_rows=31 member=mteb-retrieve located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`, `PREDICATE R87-C1 pass`, rc 0 (measured revision `10de494d`).
- `corpus/evidence/round87/mteb-retrieve-probe.txt`: `LANE_TIP 21da383b…`, `WORKTREE clean`, eight `CASE` lines whose observed vectors equal their predicted vectors, `cases=8 legs=16 mismatches=0`, `PREDICATE R87-PROBE pass`. `LANE_TIP` is an ancestor of `master` (checked).
- `.ufo/waves/round-87/L1/controls.txt`: ledger-only → `DEFECT L1-receipt`, rc 1; forged `LANE_TIP` → `DEFECT L3-tip`, rc 1.

Frozen-element discrepancies (reported, not repaired; see routed defects V1–V2):

- The frozen text (`plans/round-87-claims.md`) says BASE `defects=7`. The committed BASE transcript says `defects=3`. The `7` is the round-86 C1 BASE figure (`plans/round-86-claims.md:29`), carried over. The predicate (`defects=0` at tip, `fail` at BASE) is unaffected, and the do-nothing BASE still fails with rc 1.
- The frozen C2 control expected `mismatches>=1` for the "five schema-drift" fixture. The committed control reports `DEFECT CANON … mismatches=0 defects=1`, rc 1. The fixture is still rejected, by a different leg.

Verdict: **R87-C1 verified** on its predicate. Before→after is measured (fail → pass; executed 30 → 31). The frozen BASE figure is a mispredicted number, not a failed predicate. This integrator does not treat it as a claim failure. Operator may rule otherwise.

### R87-C2 — calibration: live case-set wording

Re-measured by this integrator:

- `git show <rev>:corpus/README.md | grep -n 'eight frozen schema-drift'`: base line 941 has the stale wording; head has none.
- Head row, `corpus/README.md:941`: `lessons/round-86.md … eight case shapes, six schema-drift and two controls …`.
- Derived split from the frozen round-86 table (`git show b9be6877:plans/round86-cases.json`, python `'schema drift' in why`): `total 8, schema 6, control 2`. Matches the row.
- Scope files `PROVINCE.md` and `SKILL.md` at head: no `schema-drift` count phrase. Repo-wide grep at head found no other live statement; the remaining hits are frozen claims, the lane's own SCORECARD record, the instrument, and `plans/round-86-claims.md`, all append-only or record text.

Evidence-verified: `.ufo/waves/round-87/L1/base-runs.txt` (`TARGET mismatches=1 defects=2 total=8 schema=6 control=2`, `PREDICATE R87-C2 fail`, rc 1); `tip-runs.txt` (`TARGET mismatches=0 defects=0 total=8 schema=6 control=2`, `PREDICATE R87-C2 pass`, rc 0).

Verdict: **R87-C2 verified** on its predicate. Before→after: mismatch 1 → 0 (re-measured). Calibration score held at ceiling 10.

## 3. Per-axis verdicts (`SCORECARD.md`, axes table)

| axis | score (round 87) | verdict | evidence |
|---|---|---|---|
| novelty | 8 | unchanged | SCORECARD diff additive only; no row moved |
| depth | 10 | unchanged | same |
| coverage | 7 (held at L0 cap) | **improved** | counted observable moved: located+executed members 0 → 1, executed 30 → 31 of 88, file-artifact 22 → 23 of 76; score held because of the cap, not because the measure is flat |
| operability | 10 | unchanged | pointer checker committed and red on the round-86 report (`paths-red.txt`), but not claimed in the round; no score move |
| freshness | 10 | unchanged | S275 bytes re-fetched and byte-identical; no score move |
| calibration | 10 (ceiling) | **improved** | live mismatch 1 → 0, re-measured; score held at ceiling |
| adjacency | 9 | unchanged | none |

No axis is **harmed**. No claim is exploratory, so no `unprovable-but-better` judgment is needed.

## 4. Discernment spot-check (LEARNING.md) — `corpus/lessons/round-87.md` `## Gate`

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| S275 `mteb-retrieve` grader | admit (tier A, member replay only) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-retrieve/tests/test_outputs.py` — live `200 559 B`, sha `e4e6b21f…c0b`, `cmp` silent vs round-52 capture | **agree** | pinned grader source code is tier A for the member-replay scope; the located quote is verbatim at line 15 and is 8 whitespace words, under the 25-word limit; the scope is stated and is narrow |
| S276 `mteb-leaderboard` grader | reject (flip: a sibling grader that adds an edge class) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-leaderboard/tests/test_outputs.py` — live `200 537 B`, sha `b28f8fc8…892cf` | **agree** | lines 6–15 match S275's shape; only `expected` differs (`GritLM/GritLM-7B`). That string is already the frozen `sibling-value` case in `plans/round87-cases.json` (predicted P/F, observed P/F), so a replay adds no vector the lane's table lacks. The rejection is grounded in the lane's own table. The flip is stated in the right kind of term |
| S275 newly written row, quote ≤25 words | row check | same as S275 | **agree** | `assert lines[0].strip() == expected, "result.txt contains unexpected value"` — 8 words, verbatim, line 15 |

Spot-check result: agree on the admit and on the reject. Sample size is two; this is the minimum the rule requires. Discernment trend: `improved` (LEARNING table: "the spot-check agrees with the gate on admits *and* rejects").

## 5. Trend verdicts

- **expansion — unchanged.** No admitted `knowledge/` entry on uncovered ground; S275 is a registry row only; the member's kind (`code`, file-artifact class) is already held. Evidence: `corpus/SOURCES.md` S275 row; no new `corpus/knowledge/*` file in the round diff. Agrees with the lane.
- **quality — improved.** A live statement that was false against the derived split (README:941, "eight frozen schema-drift cases") is repaired by derivation and verified at head. The reference-drift in the round-86 report is recorded as an erratum and the pointer checker fails closed. No admitted entry was found failing a re-check in this pass. Agrees with the lane.
- **discernment — improved.** Spot-check agrees on one admit and one reject (section 4). The lane's own Mistake 2 (carried BASE figure) was not caught by a gate; it is recorded and routed (V2), and it is not a gate-decision disagreement.

## 6. Routed defects for the lane (next round)

- **V1 (conformance, wave).** Zero L2 seats were dispatched in round 87. MISSION §L2 requires at least 8 in one batch. The `w1.ready` handoff was never marked; L0 question at `.ufo/l0-questions.md:312` is open. Not admission-barring per protocol. The next round must dispatch, or record the non-dispatch under its own line in the report.
- **V2 (freeze accuracy).** A frozen BASE figure (`defects=7`) was copied from round 86 without measurement. The frozen C2 control expectation (`mismatches>=1`) does not match the committed fixture result (`mismatches=0 defects=1`). Do not repair the frozen text. File the Q66 counter-side check as a round-88 instrument: before freeze, measure every before-figure with its counter and copy it from that output. Errata go in an appended LOG entry.
- **V3 (lesson structure).** `corpus/lessons/round-87.md` `## Gate` has no spot-check result line. LEARNING.md requires one. Add a dated pointer to this file (`corpus/lessons/round-87-verifier-spotcheck.md`) as an append in the round-88 lesson, not an edit of round-87's text.
- **V4 (mistake fix, not yet able to fail).** Mistake 2's fix (Q66) has no executable half. Per protocol a fix counts only once shown able to fail. Mistakes 1 and 3 do count (red/green shown). Round 88 must show Q66 able to fail or keep it marked as not counted.
- **V5 (report wording).** The report's coverage verdict reads as "held" and its expansion line says the observable "did not move". The coverage axis moved on its counted observable (executed 30 → 31). State the axis verdict explicitly in the SCORECARD round section, next to the held score.
- **V6 (report stale-lane clause).** Name the open round-87 mission as progressing or silent per the protocol's stale-lane clause.

## 7. Admission basis

Every claim (R87-C1, R87-C2) verifies on its frozen predicate, measured or evidence-verified as above. No axis is harmed. The conformance defects (V1, V5, V6, and the template items) are status-neutral. The frozen-figure mispredictions (V2) are recorded and do not change the predicate outcome. Admission: **admitted**.

Not written in this pass: any `[x]` in `SHONEN.md`, any promotion or mint. Box assessments are operator-owned. This integrator did not assess the four SHONEN boxes beyond the round's own surfaces.
