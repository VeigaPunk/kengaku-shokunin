---
author: kengaku
round: 90
date: 2026-11-05
---

# Kengaku round 90 — an eighth executed Terminal-Bench 2.0 member (merge-diff-arc-agi-task), external counter pins, and the routed-findings freeze gate

DRAFT by ScribeR90 for the L1 (`KengakuR90`) to integrate into `corpus/lessons/round-90.md`. Placeholders are in angle brackets `<LIKE THIS>` and are filled only from measured output. Nothing here is a measured tip figure unless it is written out as a command output.

Round 90 (hyaku run 15, KengakuR90, wave `w1`), 2026-11-05. Lane `kengaku-shokunin`, branch `master`.
Base `dcdd494ef4b4a6c0ae349ecb597527124ee54f91`. Freeze A `45171d231f0444625106abf63cd4b0804d8812bd` (`plans/round-90-claims.md`, `plans/round90-cases.json`, before any instrument). Instruments B `664435cfcb9419c4e8ac7828a55aec11a1f36ec4` (`plans/round90_polydiff_probe.py`, `plans/round90_c1_replay.py`, `plans/round90_counter_pin.py`, `plans/round90_burndown.py`, `plans/counter-pins-r90.json`). Measured tip: `<TIP>`.

Three claims on separable surfaces:

- `R90-C1` coverage (lowest non-retired axis, held at its L0 cap 7): an eighth located offline replay, `merge-diff-arc-agi-task`, by `plans/round90_c1_replay.py` (eight legs, `TRUSTED_TOOL_SHA` pin on the probe).
- `R90-C2` calibration (held at ceiling 10): `plans/counter-pins-r90.json` + `plans/round90_counter_pin.py` pin the frozen instruments and the round-89 record table blob externally, closing the round-89 self-pin hole.
- `R90-C3` operability (held at ceiling 10) + capability: `plans/round90_burndown.py`, the routed-findings freeze gate, with triage of every pending row and seeds for rounds 83–89.

## Gate

### Source candidate S279 — `<S279 DECISION: admit | reject, from ScoutS279 gate-note.md>`

The scout (`ScoutS279`) fetched the pinned grader once and byte-compared it with the round-52 capture. The capture was re-hashed by the scribe in this round: `sha256sum corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py` = `2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149`, equal to the frozen subject SHA.

| id and decision | URL | access date | located quote (≤25 words) | reason / flip |
|---|---|---|---|---|
| S279 `<admit | reject>`, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py | 2026-11-05 | `<QUOTE>` at line `<LINE>` (`<WORDS>` words; fetch `<FETCH-HTTP>`, `<FETCH-BYTES>` B, `<FETCH-SHA256>`; `cmp` vs capture `<CMP-RESULT>`) | `<REASON from scout>`; the five test functions at :10, :16, :34, :40, :52 are the grader's graded state; `test_both_bundles_fetched` tests branch-name presence, so the row admits name-presence semantics only. Flip: `<FLIP from scout>` |

Reject row (the round's second, required by the round-89 defect `R89-D4` closure; the scout's reject candidate is the member's `tests/test.sh` in the same capture directory):

| id and decision | URL | access date | located quote (≤25 words) | reason / flip |
|---|---|---|---|---|
| `<SCOUT REJECT CANDIDATE id, e.g. S280 or "tests/test.sh">` reject | `<URL of tests/test.sh at 2fd12b88aafdd04a52c298e3940bcb189f9766d6, from ScoutS279 gate-note.md §4>` | 2026-11-05 | `<QUOTE or "none: decided from bytes">` | `<REASON from scout gate-note §4, decided from the bytes not the expectation>`. Flip: `<FLIP condition from scout>` |

Census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`):

- Before the round: exit 0, `kengaku ok`, 270 rows (measured 2026-11-05, `grep -c '^| S[0-9]' corpus/SOURCES.md` = 270).
- After S279 (if admitted): 271 rows; round-end exit `<CENSUS-END-RC>` measured by the L1.

### Freeze-gate candidate, not a source

`corpus/lessons/round-89-verifier-spotcheck.md` §4 item 4 and §7 item 4 (round-89 `## Gate` has no reject row) are closed here by the reject row above, not by editing round-89 text.

## Claims and their measurements

Figures below are from measured output only. Predictions from `plans/round-90-claims.md` are stated beside each measured figure; a mismatch is a mispredict, recorded, never repaired in the frozen text.

- **R90-C1 (coverage).** BASE `dcdd494e` (`.ufo/waves/round-90/L1/base-batteries.txt`): `TARGET executed_rows=33 member=merge-diff-arc-agi-task located=1 executed=0 cases=0 legs=0 mismatches=0 defects=10`, `PREDICATE R90-C1 fail`, rc 1. Defect lines: `L4-table` (case table absent), `L8-tool` (probe absent), `L1-receipt` (receipt absent), and seven `L7-ledger` lines (row unflipped, `executed=33 members=88 != frozen 34 of 88`, and five class cells `git-plumbing 1 of 3`, `serialization-schema 3 of 10`, `file-artifact 24 of 76`, `stdout-inspection 9 of 29`, `subprocess-exec 11 of 45` each != frozen after-value). **Mispredict:** the frozen Before predicted `defects=N` with N=5; measured N=10, because the ledger check emits one line per unflipped row and per class cell, not one line per failed artifact. Tip: `<C1 TIP LINE>`, `<C1 TIP PREDICATE>`.
- **R90-C2 (calibration).** BASE `dcdd494e`: `DEFECT SETUP unreadable plans/counter-pins-r90.json at dcdd494ef4b4`, `PREDICATE R90-C2 could-not-evaluate`, rc **2**. **Mispredict:** the frozen Before predicted rc 1 with `PIN-MISMATCH absent` per created path and `PIN-OK` for the pre-existing counters. The pin file is itself absent at BASE (the ledger lands at B), so the checker stops at SETUP. The fail-closed direction holds: no `PREDICATE ... pass`, no awk zero, and no `PINS checked=`. At B `664435cf`: `RECORD-TABLE blob=163f2843… matched`, `PINS checked=7 matched=7 mismatched=0`, `PREDICATE R90-C2 pass`, rc 0. Selftest at B: `SELFTEST cases=5 red-green-ok=5`, rc 0. Tip: `<C2 TIP LINE>`, `<C2 SELFTEST TIP LINE>`.
- **R90-C3 (operability).** BASE `dcdd494e`: `ROWS total=133 valid=132 invalid=1 superseded=0`, `DEFECT line 125: R82-F1: source must read <path>:<line>`, `DEFECT invalid-row-unresolved R82-F1`, `DEFECT check-failed R42-R2 rc=1`, `freeze=refused oldest_pending_round=39 pending=33 malformed_unresolved=1 seeds_83_89=0 resolutions=0 checks_run=98`, `PREDICATE R90-C3 fail`, rc 1. **Mispredict:** the frozen Before and Move (a) say 27 pending rows; measured 33 (open 32, blocked 1), opened in rounds 39, 40, 42, 45, 51 and 82 (oldest 39). The refusal still holds; the resolution count must cover 33 rows, not 27 (see Frozen-text observations). Selftest at BASE: `SELFTEST cases=7 red-green-ok=7`, rc 0. Tip: `<C3 TIP LINE>`, `<C3 SELFTEST TIP LINE>`.

## Mistakes

1. **Class `unwired-tripwire`.** Evidence: `plans/routed_open.py` (round 41) and `corpus/routed-findings.jsonl` existed, and a freeze step never invoked them. At BASE the burn-down reads `pending=33 oldest_pending_round=39` with no freeze step refusing, and `seeds_83_89=0`: no routed row exists for any finding from rounds 83–89. Captured-by: none (the round-39 Q30 lesson wired `order_check.py` into `round_close.py`, never `routed_open.py`). Fix: R90-C3, `plans/round90_burndown.py` refuses a round freeze while a pending row is opened before N−2, plus the freeze-citation rule: a freeze of any new coverage claim cites `freeze=admitted` at `--freeze-round <N>`. Tip: `<C3 TIP LINE>`.
2. **Class `schema-drift`.** Evidence: `corpus/routed-findings.jsonl` line 125 (`R82-F1`, status `open`) carries `source` = `corpus/lessons/round-82.md ## Corrections (R81-V2)`. It reads like a path to an eye, but the ledger's parser requires `<path>:<line>`: `python3 plans/routed_open.py --lane . --list` prints `DEFECT line=125 source must read <path>:<line>` and `ROWS total=133 invalid=1`. The row stayed in the pending count (33 includes it). Captured-by: `routed_open.py` validation (it caught the row; no gate read its output). Fix: supersede by a well-formed resolution row, appended, never edited in place; the C3 gate refuses (selftest `malformed-refuses`; battery `cases=7 red-green-ok=7`) while a malformed row is unresolved. Tip: `<C3 TIP LINE>`.
3. **Class `mispredict` (the C2 BASE prediction).** Evidence: the frozen C2 Before said rc 1 with per-path `PIN-MISMATCH absent` lines and `PIN-OK` for four pre-existing counters. Measured at BASE: rc 2, `DEFECT SETUP unreadable plans/counter-pins-r90.json`, `PREDICATE R90-C2 could-not-evaluate`, because the pin file is absent at BASE and the checker stops before it reads any path (`.ufo/waves/round-90/L1/base-batteries.txt`). Captured-by: Q66 (the do-nothing control is measured, not asserted; the prediction was wrong and the control recorded it). Fix: recorded here and in the report as a mispredict; frozen text not repaired; the BASE figure is rc 2 SETUP.

### Frozen-text observations (reported, not repaired)

These are elements of `plans/round-90-claims.md` that the measurements contradict. Per the freeze rule they are recorded, and the operator rules on them.

- C3 Move (a) and the Before line say 27 pending rows; measured 33 (`pending=33`). The predicate threshold (`no pending finding opened before round 88`) is unaffected; the resolution count is 33 or more, not 28.
- C2 Move says "the four pre-existing counters match"; the pin ledger lists three pre-existing paths (`plans/round88_claim_figures.py`, `plans/round89_c1_replay.py`, `plans/round89_claim_figures.py`). `plans/round89_polyglot_probe.py` is not a ledger path.
- Round shape says 12 seats (executor 3 … labrat 1, which sums to 11). The dispatched spec `.ufo/waves/round-90/w1-spec.json` has 12 seats: executor 5, scout 1, connector 1, scribe 1, reviewer 1, critic 1, mutation-tester 1, sentinel 1; no labrat. Attack seats are 4 of 12 (reviewer, critic, mutation-tester, sentinel), not 5.
- C3 Move (c) says every closed resolution row's `check` must exit 0. The existing closed row R42-R2 fails its check at BASE (`check-failed R42-R2 rc=1`). Its work is present (`plans/scratch_guard.py`, commit `ff14d76d`), and its check greps `^ROW R42-R2\.[12] status=closed` in `routed_open.py --list`, which prints no `ROW` lines. This is a stale check on a true close, not a fabricated close. Triage: a superseding resolution row, not an in-place edit.

### Honest limits (from the frozen claims; unchanged)

- The eight cases yield seven distinct predicted vectors (`PPPPF` occurs twice).
- The vector is a statement about the captured bytes plus this probe harness on this host's toolchain (git, python3), not about Terminal-Bench's own harness.
- `test_both_bundles_fetched` greps branch names; the cases prove name presence, not that a bundle was fetched. The graded state is lane-authored, as in every replay of this series.
- The C1 counter is pinnable by one commit that also rewrites the pin ledger; the C2 ledger is rewritable in one commit (the round-89 disclosure, narrowed, not eliminated).

## Wave findings

Filled by the L1 from the seat reports (`.ufo/waves/round-90/w1/<Seat>/`). One slot per seat-reported finding; the scribe does not invent findings.

1. `<slot 1: seat, class, evidence path, captured-by, fix or named blocker>`
2. `<slot 2>`
3. `<slot 3>`

## Frontier and assimilation

- `considerthese/2026-10-26.md` item 1 (routed-findings burn-down with a freeze refusal) is mined and implemented here via R90-C3.
- `merge/kengaku/` remains blocked by L0 `kengaku | round-54`; nothing is adopted from it.
- S279 status: `<S279 status: mined | rejected>`.

## Mistakes mined (not claims) — routed to the next round

Nothing routed beyond the three Mistakes above and the frozen-text observations. Tip-only defects, if any, are added by the L1 under their own numbers.
