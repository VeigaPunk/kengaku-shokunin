# R45RevDispatch — wave bookkeeping for the round-shape paragraph

Seat: R45RevDispatch (reviewer, axis operability). Wave: kengaku-r45-a3w1. Lane tip measured:
`fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C …/kengaku-shokunin rev-parse master HEAD`, both print that hash).
Sources read: `w1/swarm-registry.json`, `w1-results.json`, `w1-dispatch.json`, `w2/swarm-registry.json`,
`w2-dispatch.json`, `w2-results.json`, `a3w1-dispatch.json`, `w2-spec.json`, `a3w1-spec.json`,
`make_wave1_spec.py` / `make_wave2_spec.py` / `make_a3w1_spec.py`, and the `w1/`, `w2/`, `a3w1/` report dirs.
Full census dump: `.ufo/waves/round-45/a3w1/R45RevDispatch/census.txt` (verbatim script output).

## Paste-ready table (round-shape paragraph)

| wave | spawned | settled (usable outcome) | report file | results-only | dead (no output, no report) | last error text of dead seats |
|---|---|---|---|---|---|---|
| w1 (build) | 39 | 39 (all outputs delivered) | 39 | 0 | 0 | — none; every result has `note: null`, no `error` key |
| w2 (falsify, killed) | 39 | 5 (3 output+report, 2 report-only) | 5 | 0 | 34 | `spawned as job <name>; still running at the session exit and killed - no output delivered` (×34, uniform; 12 seats show job suffix `-2` = one respawn each) |
| a3w1 (re-dispatch) | 34 | in flight — 9 report files on disk at read time | 9 so far | — | — | — |

`settled` = left a usable outcome (recovered `output` in `w2-results.json` and/or a `<Seat>.md` report file).
a3w1 spawned set is exactly `w2 dead ∪ w2 report-only` = w2's 39 minus the 5 settled reports
(verified: `a3w1 set == w2 − {R45CritAssimilation, R45ExecCensusPost, R45ExecNoHarm, R45LabratRefetch, R45RevC1Receipt}` → True).

## Measured numbers and their commands

All counts produced by `python3` JSON census (script + output in `census.txt`, sha at end of this file):

- **Spawned**: `w1-dispatch.json` `counts={spawn:39,resume:0,total:39}`; `w2-dispatch.json` `counts={spawn:39,resume:0,total:39}`;
  `a3w1-dispatch.json` `counts={spawn:34,resume:0,total:34}`. Registry `members` = 39 (w1), 39 (w2); all `kind:spawn`, `agentId:null`.
- **Settled w1**: `w1-results.json` `seats:39`, `results` length 39, every entry has non-empty `output`, `error` key absent,
  `note:null` (Counter: `{None: 39}`). Registry ∩ results = ∅ both directions (39/39 names match).
- **Report files w1**: `find .ufo/waves/round-45/w1 -maxdepth 1 -name '*.md'` → 39 files, 0 zero-byte
  (`find … -size 0 | wc -l` → 0; smallest `R45MutV11States.md` = 763 B). 34 seat dirs exist; 5 reports
  (R45ConnSibling, R45MutParser, R45MutV11States, R45RevC1Instrument, R45ScoutTB2) have no subdir — still counted as report-file seats.
- **Settled w2**: `w2-results.json`: `seats:39, spawned:39, outputs_recovered:3`,
  `settled_by:"orchestrator session exit (no seat live)"`. Recovered outputs: R45RevC1Receipt, R45LabratRefetch,
  R45CritAssimilation — each `note:"output recovered from the orchestrator session transcript (job …, status completed, delivered 2026-10-27T02:5x)"`.
  `report_file` set on exactly 5 rows: the 3 recovered + R45ExecCensusPost.md + R45ExecNoHarm.md (report-only, `output:null`).
  `ls w2/*.md` confirms all 5 exist on disk (7006–16738 B). **Results-only: 0.**
- **Dead w2**: 34 rows with `output:null` and `report_file:null`. Their uniform last-error text
  (`w2-results.json`, per-row `note`, 34 occurrences): "spawned as job <name>; still running at the session exit and
  killed - no output delivered". Root cause (`w2-results.json` `note`, ≤25w): "The orchestrator omp session exited at
  2026-10-26T23:57:36-03:00 (SIGHUP during an operator-requested `omp update`); every L1 and seat running in it was killed."
  12 dead/settled rows name a `-2` job suffix (R45MutLandedFence, R45RevC1Receipt, R45CritV11Bypass, R45MutC2Checks,
  R45RevEntryQuotes, R45RevRowCells, R45LabratRefetch, R45SentC2Grader, R45CritC1Overclaim, R45CritAssimilation,
  R45MutHostileFixtures, R45ExecTipRerun) — these were respawns; the first spawn's error text is **not preserved anywhere**
  in registry/results (`agentId:null` throughout, no `error` field). 20 dead seats left partial dirs under `w2/` (unverified
  leads), 14 left nothing.
- **a3w1**: dispatch spawn=34; role mix from `taskCall.tasks[].agent`: mutation-tester 10, critic 10, reviewer 8,
  sentinel 2, executor 2, connector 1, simplifier 1. At read time 9 `*.md` reports on disk (seats still landing;
  this seat's own report excluded from that count by timing).

## Role mix vs the routing note — PASS on all waves

Routing note located in `make_wave1_spec.py:6` and enforced at `:442-444` / `make_wave2_spec.py:384-385` /
`make_a3w1_spec.py:50`:
- Wave-1 docstring (≤25w): "m_flash-routed roles must carry >= half, attack roles >= a quarter."
- Sets (`make_wave1_spec.py:427-428`, identical `make_wave2_spec.py:369-370`):
  `FLASH={executor,labrat,scribe,sonic,simplifier,revenger,sentinel}`, `ATTACK={reviewer,critic,mutation-tester,labrat}`.
- w2/a3w1 enforce `attack*4>=n` only (falsify wave); w1 enforces both.

| wave | n | mix (dispatch `agent`) | ATTACK | FLASH | verdict |
|---|---|---|---|---|---|
| w1 | 39 | exec 11, reviewer 7, scribe 5, scout 5, critic 3, mut-tester 2, sentinel 2, connector 2, revenger 1, simplifier 1 | 12 ≥ 10 ✓ | 22 ≥ 20 ✓ | pass |
| w2 | 39 | mut-tester 10, critic 11, reviewer 9, exec 5, sentinel 2, simplifier 1, connector 1 | 30 ≥ 10 ✓ | 9 (not required) | pass |
| a3w1 | 34 | mut-tester 10, critic 10, reviewer 8, exec 2, sentinel 2, simplifier 1, connector 1 | 28 ≥ 9 ✓ | 6 (not required) | pass |

All waves inside the `32–64` band (`assert 32 <= len(items) <= 64`). Roles are consistent across spec
(`items[].role`), registry (`members[].role`), dispatch (`tasks[].agent`) and results (`results[].agent`): zero
mismatches in all three waves (cross-check in `census.txt`). Naming quirk, not a defect: seats named `R45Labrat*`
carry `executor`/`reviewer` spec roles, so role `labrat` appears in neither mix.

## `model` overrides — none

- Dispatch tasks carry exactly `{name, agent, task}` in w1, w2 and a3w1 — **no `model` key on any of the 112 task objects**.
- No `model` key anywhere in `w1/swarm-registry.json` members, `w2/swarm-registry.json` members, `w1-spec.json` items,
  `w2-spec.json` items, `a3w1-spec.json` items, `w1-results.json` or `w2-results.json` rows (recursive key walk).
- `grep -o '"model"[^,}]*'` over all five dispatch/results/registry files → no matches.
- The only literal `model` string in any task text is inside R45RevDispatch's own prompt ("no seat ran `model` overrides").

## Findings (for the L1)

1. **No defect in the bookkeeping itself.** w1: 39 spawned → 39 settled, 39 reports, zero results-only, zero dead. The
   r43 D3 failure mode (output-in-results-only) did not recur.
2. **w2 lost 34/39 seats to one infrastructure event** (SIGHUP on `omp update`, 2026-10-26 23:57:36 -03), not to seat
   errors. `w2-results.json` is honest about it: `settled_by:"orchestrator session exit (no seat live)"`, per-row notes,
   `outputs_recovered:3`. Report-only settlements R45ExecCensusPost/R45ExecNoHarm show the write-report-first rule paying off.
3. **Information loss worth one LOG line**: the 12 `-2`-suffixed respawns prove first-attempt failures existed, but no
   first-attempt error text survived (registry `agentId:null`, no `error` field in results). Table records that honestly.
4. a3w1 re-dispatch coverage is exact: 34 = w2 dead+report-only set, verified set-equal, `a3 - w2 = ∅`.

Residual risk: a3w1 is mid-flight; its settled/dead columns will change — the L1 should re-run the census at wave close
(the script in `census.txt` is rerunnable verbatim). Verification gap: first-attempt errors of respawned w2 jobs are
unrecoverable from repo artifacts (would need the dead session's transcript).

Receipt: `.ufo/waves/round-45/a3w1/R45RevDispatch/census.txt` — full JSON census output (18 lines, <1 MiB).
No fixture/counter/probe was run; no envelope needed (read-only JSON + report writes only). No tools installed.

VERDICT: wave-table-ready-seats-112
