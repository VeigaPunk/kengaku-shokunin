author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 96 — non-author verifier spot-check

Reviewed lane tip: `f6033dadc7ae8694c0b2156a020d671284dff6b2` (BASE `45740a616028015b5dfcf9900753e3bb5e6fe689`; P0 `ff6765a6`; P1 `cea469bd`; P1b `e8a80c0e`; P2 `a3b57321`; freeze F `be3ff962c3558ece7843119c1df26fa2cdbd313a`; measured tip T = C `09717e49ff46fad5b255619d671aaaae52dfc180`; receipts `7b7a17d3`, `599c1fa1`; revert `3f300cbd`; integration `0fb7d589`; end receipts `f6033dad`). Report: `.ufo/reports/round-96/kengaku.md` (fleet commit `9b437fdce9461a3048cfa9968057ec7610cc174e`, author `kengaku-shokunin <kengaku@shokunin.local>`, 2026-11-06 00:54:56 -0300). Prompt: `.ufo/prompts/kengaku-round-96.md` (fleet `fc20a85b` attempt 1, `c3015fa9` attempt 2, 904 lines).

Driver digest (`.ufo/watchdog.log`, copied 2026-11-06):
- `2026-11-05T22:27:10-03:00 launch kengaku round=96 pgid=4001070 driver=hyaku-inline attempt=1`
- `2026-11-05T23:31:12-03:00 lane-dead-no-report kengaku round=96; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-96/kengaku.md)`
- `2026-11-05T23:31:14-03:00 launch kengaku round=96 pgid=2172327 driver=hyaku-inline attempt=2`
- `2026-11-06T00:55:41-03:00 complete kengaku round=96; hyaku-inline attempt=2`

Method. Plain measurements over committed bytes (`git show <rev>:<path> | sha256`, `git log -- <path>`, `git merge-base --is-ancestor`, a Python `json` read of `plans/grader-population-ledger.json` at BASE and the tip), the census CLI, and live re-fetches of four upstream files (Python `urllib`, sha256, line/quote check). The lane's counters (`round96_c1_replay.py`, `round96_standing_battery.py`, `round94_freeze_integrity.py`, `round95_c2_counter.py`) and the merger probe were **not executed** by this integrator (PROTOCOL §Gate standard, "Closure consequence"); their committed receipts under `.ufo/waves/round-96/` were read and graded evidence-verified.

## 1. Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-96/kengaku.md` → `kengaku-shokunin 9b437fdc…` | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` with 4 `[~]` lines; `grep -c '^- \[' SHONEN.md` → 4 | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t` + `git merge-base --is-ancestor <h> master` for all 11 round commits + BASE → all `commit`, all ancestors; all 11 round commits authored `kengaku-shokunin` | pass |
| lane pushed, clean | `jj-lane.sh state` → `branch=master local=remote=f6033dad… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` → empty; `ls-remote origin refs/heads/master` → `f6033dad…` | pass |
| report filed after its commits | lane tip committed 00:52:54 -03, report 00:54:56, completion line 00:55:41 | pass |
| prompt carries template contract | prompt headings §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit scope = all six `templates/round-prompt.md` headings, plus §6 hyaku addendum, §7 scratch, run-15 notes; attempt-2 diff is the one-word attempt counter | pass |
| marker? | real report, 11 lane commits with checkable work | not a marker → status `ok` |

Round-95 routed defects: dispositions tabled in `corpus/lessons/round-96.md` §"Round-95 spot-check routed defects — disposition" (7 rows: #1, #2 claimed as R96-C2 and reverted; #5, #6 done; #3, #4, #7 carried).

Conformance defects (status-neutral, routed in §6):
- (a) Attempt 1 died without a report (`lane-dead-no-report`); attempt 2 reused its bytes. 7 of 13 w1 seats were lost; residual r1 (4 seats) re-ran the critic, C2 reviewer, C1 mutation-tester, connector. ExecC2Rerun, MutTesterC2, ScribeLesson were not re-run.
- (b) The C commit landed bytes outside the frozen `candidate-bytes` table (the `mteb-retrieve` ledger `subject` cell; lesson M5), which already trips R96-C2's kill rule.
- (c) Both new registry rows (`SKILL.md:701-702`, `round96-c1-replay`, `round96-standing-battery`) record self-test `none` and are typed `gate`. The PROTOCOL §Gate standard self-test clause is unmet. The battery is declared non-deterministic in its own row (M2), so a single run of it is not a gate verdict.
- (d) A fleet-root `.pytest_cache` was written by a seat (misroot); the L1 relocated it under `L1a2/misroot/` (lesson M7).

## 2. Claims — re-derivation

### R96-C1 — coverage (lowest non-retired axis, L0 cap 7)

- Re-measured (Python `json` over `git show <rev>:plans/grader-population-ledger.json`, `status == "executed"`, class tally over `classes`):
  - BASE `45740a61`: 88 members, executed **39**, `file-artifact` executed 30/76, `serialization-schema` 6/10; `multi-source-data-merger` `status unexecuted`, `reason unattempted`.
  - tip `f6033dad`: 88 members, executed **40**, `file-artifact` 31/76, `serialization-schema` 7/10; the member row carries `status executed`, `round 96`, `receipt corpus/evidence/round96/merger-probe.txt`, `subject tb2-header`, `verdict cases`.
  - Matches the reported 39 → 40, 30 → 31, 6 → 7 exactly.
- Freeze integrity re-measured: all 11 `frozen-instruments` rows of `plans/round-96-claims.md` hash equal at the tip (11/11). `git log be3ff962..f6033dad -- <round96 instruments + capture dir>` returns 0 commits.
- Receipt `corpus/evidence/round96/merger-probe.txt` @ tip: `TOOL_SHA 78ce14ce…` = frozen probe sha; `ENV_SIDE … 3.11.17 2.2.3 17.0.0`; `mismatches 0`; the last case is `C17 … ok=True`.
- Live upstream (pin `2fd12b88`) `tests/test_outputs.py`: HTTP 200, 1889 B, sha256 = row/frozen. The mechanism holds on re-read:
  - line 53 `if email_conflicts:` guards the only value check of the conflict report (C04);
  - lines 22–35 content-check only users 101 and 104 (C06);
  - line 23 compares `user_id` by set equality only, so a float64 `101.0` passes (C07).
- Counter evidence-verified:
  - `L1/c1-tip.txt` @ T: `LEGS L1..L9=pass`, `TARGET executed_rows=40 member=multi-source-data-merger cells=file-artifact:31,serialization-schema:7 … cases=17 legs=68 mismatches=0 defects=0`, `PREDICATE R96-C1 pass`, rc=0.
  - The same result at `3f300cbd` (`L1a2/c1-landing.txt`) and at `0fb7d589` (`L1a2/end-receipts.txt`).
- Critic dissent ruled: **verifies, narrowed**. The 17-case finding set is incomplete: CriticClaimsR's over-report, wrong-name-winner and partial-`values` states all pass `P,P,P,1` and are not in the case table. The report and SCORECARD say so. Axis: **improved**.

### R96-C2 — calibration (ceiling 10)

- Evidence-verified at BASE `ff6765a6` (`L1/dryrun/battery-base.txt`): 6 GATE lines `verdict=red` (r79 `SUBJECT-MISMATCH mteb-retrieve`; r90–r94 absolute L7 pins), `PREDICATE R96-C2 fail`.
- Evidence-verified at T (`L1/c2-tip.txt`): `STANDING total=14 green=14 red=0`, `BITES checked=12 bitten=12`, `GROWS checked=6 tolerant=5`, `PREDICATE R96-C2 fail`, rc=1. **The frozen predicate fails at T, so the claim is not met.** Two non-author runs at T (`r1/CriticClaims/battery-t.txt`, `r1/ReviewerC2/battery-T-at-T.txt`) disagree with the official run. That makes the instrument non-deterministic (M2); it does not re-score the frozen official receipt. Kill-rule byte scope is also tripped (defect b).
- Harm re-measured by plain `git log --format='%h %s' -- <path>`. The C commit `09717e49` and the revert `3f300cbd` both touch:
  - `plans/round87_c1_replay.py` (frozen at `21da383b`);
  - `plans/round93_c1_replay.py` (frozen at `17cb9337`);
  - `plans/round94_c1_replay.py` (frozen at `997a6fe5`);
  - `plans/round95_c1_replay.py` (frozen at `16dcfed7`).
  `git diff --stat 45740a61 f6033dad -- plans/round8*_c1_replay.py plans/round9[0-5]_c1_replay.py` is empty, so the bytes are restored, but the history touch is permanent.
- Freeze-integrity evidence-verified (`L1a2/freeze-landing.txt`): `INSTRUMENT plans/round93_c1_replay.py … touched=2 verdict=broken:touched-after-freeze=2`, `FREEZE-INTEGRITY instruments=9 intact=8 broken=1`, `PREDICATE freeze-integrity fail`, rc=1 (×3 rounds). At BASE these gates pass (`w1/ExecHarm.md` §3, `freeze-r{93,94,95}-base.txt`). The gate's contract counts any `rev-list --full-history freeze..rev` touch, so this harm cannot be undone by a byte revert.
- Standing counters at the landing tip (`L1a2/battery-landing.txt`): `STANDING total=14 green=7 red=7`. These are BASE's six reds plus r95 (absolute L7 pin 39, red once C1 lands; growth drift, the `c1-only` control state).
- Axis: **harmed**. I agree with the lane's self-grade. Three freeze-integrity verdicts of closed rounds went PASS → FAIL permanently, and the claimed 6 → 0 red repair is reverted.

### Owned axes not claimed

`git diff 45740a61 f6033dad -- SCORECARD.md`: only the appended round-96 section; no axis score line was edited. The section states novelty 8, depth 10, operability 10, freshness 10, adjacency 9 held. Harm check, evidence-verified in `L1a2/end-receipts.txt` at `0fb7d589`:
- `VERDICT: PASS` (grader.py);
- `PREDICATE R68-A3 pass`;
- `ANCHORLINE … live=0 cells=0`;
- `PREDICATE R91-F1 pass`.

The round-79 gate is `DEFECTS n=1` at the landing tip (`L1a2/r79-landing.txt`), the BASE state.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | re-measured 39 → 40 of 88 (file-artifact 30 → 31, serialization-schema 6 → 7); 11/11 frozen hashes equal; receipt mismatches 0 |
| calibration | harmed | R96-C2 frozen predicate fails at T. r93/r94/r95 freeze-integrity gates went PASS → FAIL through a permanent history touch (re-measured via `git log`). Standing reds 6 → 7 at the tip |
| novelty | unchanged | no claim; score held |
| depth | unchanged | no claim; score held |
| operability | unchanged | no claim; score held |
| freshness | unchanged | no claim; score held |
| adjacency | unchanged | no claim; score held; ConnectorOverlapR CO-1: PROVINCE holds |

## 3. Discernment spot-check (`corpus/lessons/round-96.md` `## Gate`)

Re-opened live 2026-11-06 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/multi-source-data-merger/<path>`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S310 `tests/test_outputs.py` | admit (A) | HTTP 200, 1889 B, sha256 = row; line 53 = `if email_conflicts:` (2 words) | agree | It is the exact grader the replay scores. The guarded email check, the 101/104-only content checks and the set-only `user_id` compare are all on the page, so the grading-gap reasons are true |
| S314 `instruction.md` | admit (A) | HTTP 200, 1912 B, sha256 = row; line 61 = `- Data types are correct (user_id as integer)` (8 words) | agree | Primary task contract. Next to S310 it shows the stated contract is stricter than the graded one |
| S316 `README.md` | reject (B) | HTTP 200, 2567 B, sha256 = row; line 20 = `- **Pre-installed tools**: pandas (2.2.3), pyarrow (17.0.0), tmux, asciinema` (9 words) | agree | Derivative of the Dockerfile pins (S312) and the instruction. Neither the grader nor the replay reads any of its bytes |
| S315 `task.toml` | reject (A) | HTTP 200, 1107 B, sha256 = row; line 30 = `docker_image = "alexgshaw/multi-source-data-merger:20251031"` (3 words) | agree | The replay never consumes the prebuilt image. The flip was exercised by a non-author seat (ExecImage) with byte-identical outputs, so the image is confirmation, not an input |

SOURCES row re-check: rows S310, S314, S315, S316 at `corpus/SOURCES.md:326,330,331,332`. Each quote is ≤25 words, sits on the cited line, and its word count equals the row's. Each sha256 equals the live bytes.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok …/kengaku-shokunin/corpus/SOURCES.md` (only W04 cross-scope duplicate-URL warnings, as at round start).

Spot-check result: 4/4 agree.

## 4. Trend verdicts

- **expansion: improved.** Re-measured: the ledger frontier moved 39 → 40 of 88. Five tier-A rows (S310–S314) were added on a member the corpus did not hold. SOURCES went 301 → 308 rows (the census is ok).
- **quality: unchanged.** No admitted `knowledge/` entry was superseded or re-verified this round (`git diff --stat 45740a61 f6033dad -- corpus/knowledge` is empty).
- **discernment: improved.** Spot-check 4/4 agree, with both rejections carrying exercised or stated flips. Q79 (closed-round frozen instruments are never byte-replaced) and Q80 (a non-deterministic frozen predicate is not a gate) are grounded in M1/M2 at `corpus/QUALITY.md`. The harmful repair was reverted under Q78 rather than kept.

## 5. Closure

Status `ok` (real report, checkable work). **Not admitted**: R96-C2 is not met and calibration is harmed. Verdict `rejected-harmed`. C1 verifies narrowed and its bytes stand in the lane.

## 6. Routed defects (lane must address in round 97)

1. Calibration harm: the r93/r94/r95 freeze-integrity gates read `broken:touched-after-freeze` permanently. Either land successor counters as new files with new freeze tables (Q79), or record a named correction entry: an explicit, dated waiver that freeze-integrity consumers honour. Never byte-edit the closed tables.
2. Standing reds stay at 7 at the tip: r79 `SUBJECT-MISMATCH mteb-retrieve`, and r90–r95 absolute L7 pins (r95 newly red from C1 growth). Address this with successor counters, not edits to frozen files.
3. `round96-standing-battery` is non-deterministic (M2/Q80). Make it deterministic, or keep failing-run output and require two agreeing runs before freeze. Until then, register it as a `probe`, not a `gate`.
4. Both round-96 registry rows record self-test `none`. Add a self-invocation mode over isolated fixtures with committed expected exit code and finding-id (PROTOCOL §Gate standard, Self-test).
5. R96-C1 finding set: add the three missing wrong-pass states (over-report, wrong name winner, partial `values`), and narrow L6 to the pinned triples (unpinned numpy; W-2).
6. The C commit landed bytes outside the frozen candidate-bytes table (M5). Add a pre-push byte-scope check against the F table.
7. Wave losses: MutTesterC2 and ScribeLesson were never re-run. If C2 is re-claimed, run a C2 mutation seat.
8. Carried items: R95-C1 at reward scope, R95-C2 held-out false gates, round-92 items, W-4.

Operator note: all four SHONEN boxes in the report are `[~]` with pointers. Promotion is operator-owned, and none is promoted here.
