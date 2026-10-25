# R30FxDeadSeats — wave accounting: seats, roles, dead seats, yield

Seat: `R30FxDeadSeats` (falsify wave, role `scout`, axis calibration). Leaf; no subagent, no background
job, no model passed, no `agent://all`. No tool installed or upgraded during this audit (nothing was
needed; `python3` 3.14.8 and `awk`/`git` were already present), so this report records no transaction.
Lane writes: this file only. Scratch: `/tmp/r30fx-deadseats/` (measurement scripts). Nothing in the lane
was modified; `yield.tsv` was read, never written, by this seat — an external append landed during the
audit and is reported as an observation, timestamped.

Domain: the wave-accounting sentence of `corpus/lessons/round-30.md:119-124`, plus the registries,
dispatches, dispatcher assignments, the live agent roster and the yield ledger. The frozen claims
`plans/round-30-claims.md` carry no seat-count predicate; the numbers under attack are those the round
publishes about itself.

`VERDICT:` line is deliberately **not** emitted. My item is neither a source re-read nor the
complete-set review, and a PASS/FAIL verdict on `corpus/knowledge/contamination-transparency-card.md`
from a seat that only counted seats would be an unrun check asserted as a result. This report therefore
must not be cited as a Gate second-seat return: `plans/gate_timing_check.py` requires a `VERDICT:` line
in cited reports and would (correctly) invalidate it. It says nothing about the entry.

## Snapshots

All times `-0300`, 2026-10-25. Everything below is measured at the stated instant, not reconstructed.

| # | instant | fact |
|---|---|---|
| T0 | 04:35:32 | falsify wave dispatched (`falsify-dispatch.json`, `falsify/swarm-registry.json`, both same mtime) |
| T1 | 04:36–04:38 | first inventory: `yield.tsv` = 40 data rows, all round 29; build = 34 `.md`, falsify = 0 `.md` |
| T2 | 04:38:42 | `corpus/lessons/round-30.md` written (mtime) |
| T3 | 04:39:08 | `yield.tsv` rewritten by another seat: 36 round-30 rows appended (`sha256 9ba9046b…49fadd`, 7772 B) |
| T4 | 04:39:53 | final inventory (the numbers in §1–§5 unless marked T1): build = 35 `.md`, falsify = 0 `.md` |
| T5 | 04:40:37 | falsify returns begin: `R30FxDeadSeats.md` (04:40:33) and `R30FxSrcS082.md` (04:40:38); build still 35, `R30DraftEntry` still absent, ledger still 36 round-30 rows with 1 unresolving path |
| T6 | 04:40:59 | + `R30FxSrcS081.md`; 1 of the 8 Gate-cited falsify reports now exists, 7 do not; build and ledger unchanged |

## 1. Wave 1 (build) — 36 spawned seats

Source: `.ufo/waves/round-30/build/swarm-registry.json` (36 members) — identical in name set **and
order** to `build-dispatch.json`'s `registry.members` and to `build-assignments.json`'s 36 keys
(`counts.spawn = 36`, `counts.resume = 0`). Report column measured at T4 relative to repo root.

| seat | role | report | bytes |
|---|---|---|---|
| R30SrcS081 | scout | present | 14468 |
| R30SrcS082 | scout | present | 8897 |
| R30SrcS083 | scout | present | 11970 |
| R30SrcS084 | scout | present | 11024 |
| R30SrcS085 | scout | present | 18757 |
| R30SrcS086 | scout | present | 16738 |
| R30RowSchema | scout | present | 26148 |
| R30Overlap | scout | present | 16256 |
| R30DefectState | scout | present | 15351 |
| R30Considerthese | scout | present | 17325 |
| R30DraftEntry | scribe | **absent** | — |
| R30DraftIndex | scribe | present | 11798 |
| R30DraftGate | scribe | present | 12700 |
| R30DraftScore | scribe | present | 6965 |
| R30GateQuote | executor | present | 16255 |
| R30DefectFix | executor | present | 15634 |
| R30BuildAppend | executor | present | 16689 |
| R30Yield | executor | present | 8995 |
| R30Census | executor | present | 39169 |
| R30Q13Check | executor | present | 20543 |
| R30RevEntryQ1Q6 | reviewer | present | 22400 |
| R30RevEntryQ7Q9 | reviewer | present | 20672 |
| R30RevRows | reviewer | present | 10144 |
| R30RevGate | reviewer | present | 23124 |
| R30RevCounter | reviewer | present | 19422 |
| R30RevDefects | reviewer | present | 18588 |
| R30RevLesson | reviewer | present | 26352 |
| R30CritC1 | critic | present | 18701 |
| R30CritC2 | critic | present | 16355 |
| R30CritC3 | critic | present | 11728 |
| R30ConnSibling | connector | present | 13669 |
| R30ConnCorpus | connector | present | 53852 |
| R30MutGate | mutation-tester | present | 13829 |
| R30MutCounter | mutation-tester | present | 10195 |
| R30RevFlip | revenger | present | 20774 |
| R30SimplGate | simplifier | present | 14821 |

Role mix: scout 10, reviewer 7, executor 6, scribe 4, critic 3, connector 2, mutation-tester 2,
revenger 1, simplifier 1 = 36. Every present report is non-trivial and names its own seat (checked:
`len < 500 B` or seat name missing → 0 hits). No file on disk is outside the registry.

Movement inside the audit window, stated because it changes what "missing" means: at T1, 34 reports
existed; `R30SimplGate.md` landed 04:39:10 and `R30RevCounter.md` was last rewritten 04:39:02. At the
lesson's write instant (T2) only 33 reports existed; `R30DraftEntry`, `R30RevCounter` and
`R30SimplGate` were all absent then.

## 2. Wave 2 (falsify) — 33 spawned seats

Source: `.ufo/waves/round-30/falsify/swarm-registry.json` (33 members) — same set as
`falsify-spec.json`'s 33 items, `falsify-assignments.json`'s 33 keys and `falsify-dispatch.json`'s
`counts.spawn = 33 / total = 33`. At T4 the directory held only `swarm-registry.json`, so every row is
absent at that instant — the wave was ~4 minutes old and all 33 agents were live (`running`) in the
roster. The table's report column is T4 plus the T5 movement noted in the row it affects; later returns
(which are expected) do not retroactively make the T4 reading wrong, and this seat cannot see the wave
close.

| seat | role | report |
|---|---|---|
| R30FxSrcS081 | scout | **present at T6** |
| R30FxSrcS082 | scout | **present at T5** (13 300 B, 04:40:38) |
| R30FxSrcS083 | scout | **absent** |
| R30FxSrcS084 | scout | **absent** |
| R30FxSrcS085 | scout | **absent** |
| R30FxSrcS086 | scout | **absent** |
| R30FxEntryCompleteSet | reviewer | **absent** |
| R30FxEntryQ1Q3 | reviewer | **absent** |
| R30FxEntryQ4Q6 | reviewer | **absent** |
| R30FxEntryQ7Q9 | reviewer | **absent** |
| R30FxQuotes | scout | **absent** |
| R30FxRowsCensus | scout | **absent** |
| R30FxC1Counter | critic | **absent** |
| R30FxC1Predicate | critic | **absent** |
| R30FxC2Counter | critic | **absent** |
| R30FxC2Recheck | reviewer | **absent** |
| R30FxC3Gate | reviewer | **absent** |
| R30FxC3CLI | executor | **absent** |
| R30FxGateRegression | executor | **absent** |
| R30FxCounterSelfGuard | mutation-tester | **absent** |
| R30FxNoHarm | reviewer | **absent** |
| R30FxR13Revert | executor | **absent** |
| R30FxQuarantine | scout | **absent** |
| R30FxConsiderthese | reviewer | **absent** |
| R30FxC1ControlJunk | executor | **absent** |
| R30FxEvidence | scout | **absent** |
| R30FxFlipRev | revenger | **absent** |
| R30FxCoverageAxis | critic | **absent** |
| R30FxPriorArt | critic | **absent** |
| R30FxSibling | connector | **absent** |
| R30FxQ13Fixture | executor | **absent** |
| R30FxStagedContrast | scout | **absent** |
| R30FxDeadSeats (this seat) | scout | present (this file) |

Role mix: scout 12, reviewer 8, critic 5, executor 5, mutation-tester 1, revenger 1, connector 1 = 33.

## 3. Dead seats

Criterion used (the fleet's own, e.g. round-64: a seat that "died on the provider's cyber-policy filter
at spawn"): a **dead** seat is a dispatched seat whose agent is gone or cancelled *and* whose report never
landed. A seat that is still live without a report is **unlanded**, not dead; counting it as dead would
inflate the death count the lesson reports.

**Dead-seat list: empty.** Evidence — the live roster at T4 holds exactly 69 `L1Kengaku30.*` children,
36 for build (`R30SrcS081` … `R30SimplGate`) and 33 for falsify (`R30Fx*‑3`); set-difference against
both registries in both directions is empty; no build seat is cancelled, and all 33 falsify seats read
`running`.

Missing reports (not deaths):

| wave | dispatched | reports at T4 | missing |
|---|---|---|---|
| build | 36 | 35 | `R30DraftEntry` (scribe) — agent live/`running`, `/tmp/r30-DraftEntry/entry.md` 26 317 B written 04:35, report never written |
| falsify | 33 | 0 (+ this file) | all 33; wave 4 min old at snapshot, every agent live |

Second-order fact: at T2, when the lesson asserted "No seat died before wave 2", that sentence was true
on deaths but the wave-1 return count was 33/36, and its continuation — "dead-seat detail is in the round
report" — points at `.ufo/reports/round-30`, which does not exist (the newest entry under `.ufo/reports/`
is `round-17`). The pointer does not resolve.

## 4. Yield ledger

`.ufo/waves/yield.tsv`, header `round seat role_family report caused_change commit`.

| measurement | T1 | T4 |
|---|---|---|
| file mtime | 03:57:34 (pre-dates the round's first byte) | 04:39:08 |
| `sha256` | `e505d5a2…3b964fb` | `9ba9046b…49fadd` |
| data rows | 40 | 76 |
| rows with `round = 29` | 40 | 40 |
| rows with `round = 30` | **0** | **36** |

Round-30 rows at T4 (36 = build wave only):

- seat names **equal the build registry exactly, in registry order** (compared as an ordered list →
  `True`); no falsify seat has a row; no unknown seat has a row.
- `role_family` matches the registry role for all 36 (0 mismatches).
- `report` paths: **35 of 36 resolve**; `R30DraftEntry` → `.ufo/waves/round-30/build/R30DraftEntry.md`
  does not exist. This is the same defect class `R30Yield` flagged for round 29 (2 unresolving paths).
- `commit` column: `pending` in all 36 rows. Nothing of round 30 is committed — `HEAD` is `363a4eb`
  ("round-29 verifier spot-check"), `.ufo/waves/round-30/` is untracked, `corpus/lessons/round-30.md` is
  untracked, and `yield.tsv` itself is dirty against its own landing commit `5fd54a4`. Q19 asks for "the
  commit that carries it"; `pending` is an honest placeholder but not the column the criterion requires,
  and `caused_change = yes` (31 rows; 5 `no`) is asserted with no commit binding.
- format: all 76 data rows have exactly 6 fields; no duplicate `(round, seat)` pair.
- per role family (round 30, build wave): scout 10 seats/9 changed, reviewer 7/7, executor 6/5,
  scribe 4/3, critic 3/3, connector 2/1, mutation-tester 2/2, revenger 1/1, simplifier 1/0. No family is
  at zero yield for two consecutive rounds on this evidence; `simplifier` is at zero this round.
- Q19 coverage: one row per **dispatched** seat would be 69; present are 36 (all wave 1). Falsify rows:
  **0 of 33**.
- Standing-ness: there is no landed generator (`plans/mkyield.py` absent; no `yield*.py` in `plans/`), so
  the round's ledger depends on an unlanded scratch tool — `R30Yield` says so itself ("the generator is
  not standing yet").

## 5. Round total

**69 seats** = 36 (build) + 33 (falsify). Round-30 yield rows required by Q19: 69; present at T4: 36.
The lesson's own arithmetic (36 + "34") would give 70; the second addend is wrong by one.

## 6. Claims tested

| # | claim | verdict | evidence |
|---|---|---|---|
| A1 | lesson `:121-122` — wave 1 = 36 seats, 10/7/6/4/3/2/2/1/1 | **holds** | registry = dispatch = assignments = spec, role counts recomputed |
| A2 | lesson `:122` — "Wave 2 (falsify) 34 seats" | **FALSIFIED** | spec items 33; assignments keys 33; dispatch `spawn 33 / total 33`; registry 33; roster 33 `R30Fx*‑3` children — five independent artifacts say 33 |
| A3 | lesson `:122` — "≥25% attack roles" | holds, convention-dependent | reviewer+critic+mutation-tester+sentinel = 14/33 = 42.4 % (the fleet convention used in rounds 26/65); under the narrower critic+mutation-tester+revenger reading it is 7/33 = 21.2 %. Recorded, not smoothed |
| A4 | lesson `:123` — "Seat-level yield: `.ufo/waves/yield.tsv` round-30 rows" | **FALSIFIED at T2**, half-true at T4 | at the instant the lesson was written the ledger held 0 round-30 rows and its mtime (03:57:34) pre-dated the round; at T4 it holds 36 of 69, all `commit=pending`, one unresolving report path |
| A5 | lesson `:123` — "No seat died before wave 2" | holds | 36/36 build agents registered and uncancelled; roster set-difference empty |
| A6 | lesson `:124` — "dead-seat detail is in the round report" | **FALSIFIED** | `.ufo/reports/round-30` does not exist |
| A7 | lesson `:17,31-35` — 8 falsify report paths cited as the Q10 second-seat re-reads (`R30FxEntryCompleteSet`, `R30FxEntryQ1Q3`, `R30FxEntryQ4Q6`, `R30FxEntryQ7Q9`, `R30FxQuotes`, `R30FxSrcS081`, `R30FxSrcS086`, `R30FxRowsCensus`) | **FALSIFIED at the lesson's write instant**; unresolved at T6 | at T2 the falsify directory held no report at all; at T6 (04:40:59) 1 of 8 exists (`R30FxSrcS081.md`, landed 04:40:5x) and 7 do not. Independently, nothing of round 30 is committed, so `plans/gate_timing_check.py` reports "absent from commit tree" for each of the eight — file presence alone does not discharge the citation |

## 7. Remaining unknowns

- Whether `R30DraftEntry` lands at all: its agent was live at snapshot with scratch output but no report;
  a later append cannot be distinguished here from a post-freeze repair.
- Who appended the 36 round-30 rows at 04:39:08, and with which tool: the append is not reproducible from
  any file in `plans/`, and `R30Yield` explicitly declined to write. The row set is nevertheless correct
  against the build registry, so this is a provenance gap, not a data defect.
- `caused_change` truth for the 31 `yes` rows: it cannot be bound without a commit, and binding it is
  outside this seat's item.

## Files

- written: `.ufo/waves/round-30/falsify/R30FxDeadSeats.md` (this report)
- read-only in the lane: the two registries, two dispatch files, two assignments files, `falsify-spec.json`,
  `build-spec.json`, `build/*.md` (35), `falsify/`, `.ufo/waves/yield.tsv`, `corpus/lessons/round-30.md`,
  `corpus/QUALITY.md` Q19, `plans/gate_timing_check.py`, `plans/round-30-claims.md`, `claims/*.txt`, roster
- git (read-only): `HEAD = 363a4eb`, `git status` on the accounting paths, `git log` for `yield.tsv`
- scratch: `/tmp/r30fx-deadseats/` (throwaway measurement scripts; deletable)
