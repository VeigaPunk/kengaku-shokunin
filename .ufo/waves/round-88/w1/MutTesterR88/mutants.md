# MutTesterR88 — mutation battery on both round-88 counters (wave 1, seat MutTesterR88)

Read-only on production. No production file, commit, index or stash was touched. Every mutant is a scratch copy; each differs from its base by one single-line, in-place edit (`evidence/mutant-diffs/*.diff`). Kill rule: a mutant is **killed** on a fixture when its exit code differs from the unmutated counter's exit code on that same fixture. Survivors are classed as **necessary** (the removed check is the only catcher on some fixture), **redundant** (another leg catches the same fixture; named), or **output-only** (rc unchanged; only a printed figure moves).

Tools installed: none.

## 0. Frozen inputs and tip baseline

- Instrument bytes unchanged between 1f267d4b and 7fcc680b (verified by sha256 against `git show 1f267d4b:<path>` and `git diff --stat 1f267d4b 7fcc680b -- <paths>` empty): `plans/round88_c1_replay.py` (0c47f5ec…), `plans/round88_claim_figures.py` (229a0edd…), `plans/round88_fixgit_probe.py` (50ae36d6…), `plans/round88-cases.json` (72f8ea0c…), and the fix-git capture (sha a8a6f51e…). The ledger changes at the tip (expected, not an instrument).
- Scratch tip checkout at 7fcc680b (detached, from a `git clone --no-hardlinks` of the lane). Counters run from that tree with `--rev HEAD`.
- **Unmutated C1 at tip:** rc 0. `TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`, `PREDICATE R88-C1 pass`. Re-run byte-identical.
- **Unmutated Q66 at tip:** rc 0. `MISMATCH KNOWN R87-C1 kv:defects claimed==7 defects claimed =7 measured 3`, `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, `DEFECTS n=0`, `TARGET … defects=0`, `PREDICATE R88-C2 pass`. Selftest rc 0 (`SELFTEST T1–T4 pass`, `PREDICATE R88-C2-SELFTEST pass`).
- Tip extraction by claim: 15 claims carry records (56 total). `R82-C3` is prose-mode. `R83-C2` carries zero records (see O4).

Fixtures: `evidence/fixtures.txt` (commit SHAs, what each changes, which leg it targets).

## 1. C1 counter — `plans/round88_c1_replay.py` (13 mutants, 12 fixtures + tip = 168 cells)

Full rc matrix: `evidence/rc-matrices.txt`; all cells: `evidence/out/c1__*.txt`.

| # | Mutant (guard disabled) | Fixture | Unmutated rc and DEFECT | Mutant rc and output | Verdict |
|---|---|---|---|---|---|
| m01 | L1 receipt-exists defect removed | c1-L1 (receipt deleted) | 1: `DEFECT L1-receipt corpus/evidence/round88/fix-git-probe.txt absent` | 0: `TARGET … located=1 executed=1 cases=0 legs=0 defects=0` (reports executed with zero cases) | **killed**; necessary (only catcher) |
| m02 | L2 required-field check removed | c1-L2m (COMMAND line removed) | 1: `DEFECT L2-stamp missing COMMAND` | 0 | **killed**; necessary |
| m03 | L3 ancestor check removed (resolve kept) | c1-L3o (LANE_TIP = orphan commit 368cfa7a) | 1: `DEFECT L3-tip LANE_TIP 368cfa7a7f81 is not an ancestor of c430c2c374d3` | 0 | **killed**; necessary |
| m04 | L3 entirely (any LANE_TIP accepted) | c1-L3a (LANE_TIP absent); also c1-L3o | 1: `DEFECT L3-tip LANE_TIP 'absent' does not resolve to a commit` | 0 on both | **killed**; necessary (m03 keeps the resolve check and still catches absent) |
| m05 | L4 table compared against measured tree, not FREEZE_REV | c1-L4 (table comment key; CASE_TABLE_SHA updated) | 1: `DEFECT L4-table table sha=52ea3b2a… != frozen 72f8ea0c…` | 0 | **killed**; necessary (L2 passes because the stamp was updated, probe ignores the key) |
| m06 | L5 entirely | c1-L5 (receipt `CASE exact observed=F/P`) | 1: `DEFECT L5-vectors exact observed=F/P predicted=P/P` + `DEFECT L6-reproduce re-run observation block differs` | 1: only `DEFECT L6-reproduce …` | **survived**; redundant with **L6** (catches the same change; defects 2→1) |
| m07 | L6 compares only the `cases=` summary line | c1-L6x (non-CASE line in observation block) | 1: `DEFECT L6-reproduce re-run observation block differs` | 0 | **killed**; necessary for non-summary tampering |
| m08 | L6 entirely (both branches) | c1-L6x | 1 (same) | 0 | **killed**; necessary |
| m09 | L7 entirely | c1-L7s (ledger status "planned") | 1: `DEFECT L7-ledger row {…"status": "planned"…}` | 0 (`TARGET executed_rows=31 … executed=1`) | **killed**; necessary (also killed on c1-L7r) |
| m10 | L7 receipt field dropped from tuple | c1-L7r (ledger receipt → other-probe.txt) | 1: `DEFECT L7-ledger row {…"receipt": "corpus/evidence/round88/other-probe.txt"…}` | 0 | **killed**; necessary (c1-L7s still caught by the status field, so only c1-L7r isolates it) |
| m11 | L8 subject-SHA defect removed | c1-L8 (grader comment; receipt SUBJECT_SHA updated) | 1: `DEFECT L8-subject sha=18cff308… != frozen` + `DEFECT L6-reproduce probe re-run rc=2 produced no observation block` | 1: only the L6 line | **survived**; redundant with **L6** (the probe's own SUBJECT_SHA gate raises SetupDefect, rc 2) |
| m12 | `executed_rows` counted as the constant 32 | c1-rows (one extra executed ledger row) | 0: `TARGET executed_rows=33` | 0: `TARGET executed_rows=32` | **survived (rc)**; output-only. No predicate leg reads executed_rows (O6) |
| m13 | L5 observed-vs-predicted comparison removed | c1-L5 | 1 (2 defects) | 1: only `DEFECT L6-reproduce …` | **survived**; redundant with **L6** |

Tally C1: 9 killed (m01, m02, m03, m04, m05, m07, m08, m09, m10), 4 survived (m06, m11, m13 redundant with L6; m12 output-only). No mutant of the L1–L8 legs escapes the rc on every fixture it targets; every mutant that removes a leg whose change is also visible to L6 survives only because L6 fires on the same fixture.

## 2. Q66 counter — `plans/round88_claim_figures.py` (10 mutants, 6 fixtures + tip = 66 cells, plus 11 selftests)

Full rc matrix: `evidence/rc-matrices.txt`; cells: `evidence/out/cf__*.txt`, `evidence/out/cfst__*.txt`.

Prediction column = my prediction of the tip run before running it. Actual = observed.

| # | Mutant | Predicted tip | Actual tip rc | Fixture kill evidence (unmutated rc → mutant rc) | Verdict |
|---|---|---|---|---|---|
| m01 | KNOWN check dropped (`known_pairs = set()`) | FAIL, mispredict becomes UNEXPECTED | **1**: `MISMATCH UNEXPECTED R87-C1 kv:defects claimed==7 … measured 3`, `DEFECT F5-unexpected R87-C1 kv:defects` | tip 0→1 (mutant fails, expected); c2-missing 1→0 | **killed**; necessary (set compare is the only catcher of the known mispredict; without KNOWN a vanished mispredict passes) |
| m02 | KNOWN emptied (`KNOWN = {}`) | FAIL | **1**: same DEFECT lines | c2-missing 1→0; rc identical to m01 on all six fixtures | **killed**; behaviourally equivalent to m01 (not an independent catch) |
| m03 | MISMATCH label forced to `KNOWN` | PASS | **0**; label not gating | c2-unexp: rc 1 both, but `MISMATCH KNOWN R87-C1 kv:executed` replaces `MISMATCH UNEXPECTED`; `DEFECT F5-unexpected` still fires | **survived (rc)**; output-only label. Redundant with `F5-unexpected` (defect line still fires) |
| m04 | F6-norecords check removed | PASS (no zero-record claim has a passing counter at BASE) | **0** | c2-f6: unmut rc 1 `DEFECT F6-norecords R80-C1 rc=0 (before-state must fail at BASE)` → mutant rc 0 | **killed** on the fixture only; necessary (sole catcher); unreachable on the frozen tip |
| m05 | `CONVO_RE` widened to `\w+=\w+` alternative | PASS if extra spans are benign | **0** | rc 0 everywhere; RECORDS changes from `prose=0` to `prose=3`; records/checked unchanged at 56 | **survived (rc)**; output-only (prose count not gated, O3) |
| m06 | dedupe disabled | PASS (no duplicates) | **0**; records=56 unchanged | selftest T4 still passes (`T4-dedupe pass defects=7 records=1`), selftest rc 0 | **survived everywhere**; undetected by any leg and by selftest T4 (O5) |
| m07 | FAIL_RE requirement dropped | PASS | **0**; records unchanged | selftest rc 0 | **survived everywhere**; undetected (no frozen before-span lacks a fail marker) |
| m08 | backward `at BASE` direction disabled | PASS on predicate (I did not predict it) | **0** with `RECORDS … records=51 checked=51` (was 56) | selftest T3 fails: `SELFTEST T3-atbase-backward fail spans=[]`, selftest rc 1 | **survived predicate; killed by selftest only**; five records vanish silently (O2, O3) |
| m09 | KNOWN value check removed | PASS | **0** | c2-kv4: unmut rc 1 `DEFECT F5-known-value R87-C1:defects frozen-measured=3 now=4` → mutant rc 0 | **killed**; necessary (sole catcher of a drifted KNOWN measured value) |
| m10 | F5-missing-known check removed | PASS | **0** | c2-missing: unmut rc 1 `DEFECT F5-missing-known R87-C1 kv:defects` → mutant rc 0 | **killed**; necessary |

Tally Q66: 6 killed (m01, m02, m04 on its fixture, m08 by selftest only, m09, m10); 4 survived (m03 output-only, m05 output-only, m06 and m07 undetected).

Predictions: all 9 tip predictions I wrote down before running matched the observed outcome (m08 had no prediction). Separately, my first c2-f6 fixture commit (8e7d676d) placed the forged R80 PREDICATE line above `from __future__ import annotations`, which is a SyntaxError; every mutant then failed with a spurious `F3-nopredicate` on that fixture. That fixture was fixed in dd432f3d and the whole c2-f6 column re-run; the numbers above are from the re-run.

## 3. Frozen-element and instrument observations (reported, not repaired)

O1. **KNOWN's claimed value is not enforced.** The frozen KNOWN entry is `(R87-C1, kv:defects): (claimed 7, measured 3)`, and the predicate reads "the mismatch set equals the frozen KNOWN set {(R87-C1, kv:defects): claimed 7, measured 3} exactly". Code compares `(claim, key)` pairs and the measured value only. Fixture c2-claimed9 (round-87 claim text `defects=7` → `defects=9` at both mentions): unmutated rc **0**, `MISMATCH KNOWN R87-C1 kv:defects claimed==9 … measured 3`, `PREDICATE R88-C2 pass`. Tested with one edited value (7→9); the claimed half of the KNOWN entry is never compared, so any other claimed value would pass the same way.

O2. **The predicate names the selftest, but `run_check` does not run it.** The R88-C2 predicate says "and the selftest battery exits 0". `run_check` does not call selftest. Observed: m08 (backward direction disabled) → check rc 0 with 5 records dropped while selftest rc 1.

O3. **Count figures are reported, not gated.** `records=56`, `checked=56`, `prose=N` are printed and never compared. Dropping 5 records (m08) still gives `PREDICATE R88-C2 pass`. The clause "every extracted before-figure record is checked" holds vacuously for records the extractor never produced.

O4. **Extraction gap: R83-C2's before-figure is invisible.** Its before-state text, "before eight unregistered ids plus missing index, fail", carries no counter output vocabulary (`CONVO_RE` requires one), so no span is extracted. R83-C2 contributes zero records. `prose=0` for that file (prose counts only spans that were found). Only F6 can see this claim, and only if its counter ever passes at BASE. The instrument's "every before-figure is extracted from claim bytes" overstates coverage.

O5. **Selftest T4 (dedupe) is vacuous.** Its duplicate fixture's second mention ("the counter at BASE must report `defects=7` (exit 1)") yields no span, so only one record exists whether or not dedupe runs. With dedupe disabled (m06), T4 still passes, and so does the whole check at tip.

O6. **C1 `executed_rows` (ledger movement 31 → 32) is not a leg.** It is printed on the TARGET line, but no leg checks it. L7 checks only the member's own row. Mutant m12 (constant 32) survives all fixtures; on c1-rows (extra executed row) the counter prints `executed_rows=33` and still passes. The claim's ledger movement figure is therefore unchecked by the predicate.

O7. **C1 L5 and L8 are redundant with L6** on every reachable fixture (m06, m11, m13). L6 catches the same change in the receipt, and the probe's own gate catches the grader-SHA change. This does not break the claim, but it inflates defect counts (two defect lines for one change). Noted for calibration only.

## 4. Result

- C1 counter: 13 mutants, 9 killed, 4 survived (3 redundant with L6, 1 output-only). Every L1–L8 leg has at least one fixture on which its removal flips the exit code, except L5/L8 which are only covered by L6.
- Q66 counter: 10 mutants, 6 killed (one by selftest only), 4 survived (2 output-only, 2 undetected by any leg or selftest).
- Frozen-element observations O1–O6 are the defects I found; O7 is redundancy only.

Scratch (`/fast/scratch/hyaku/kengaku-r88/MutTesterR88/`, ~200 GB of fixture clones) is deleted before yield. Evidence kept in this directory: `evidence/out/` (all 245 cell outputs), `evidence/mutant-diffs/` (23 diffs), `evidence/rc-matrices.txt`, `evidence/fixtures.txt`, `evidence/drivers/` (drivers, logs, base counter copies).

Report: .ufo/waves/round-88/w1/MutTesterR88/mutants.md
