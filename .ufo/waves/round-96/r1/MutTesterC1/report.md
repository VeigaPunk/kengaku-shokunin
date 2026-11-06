# MutTesterC1 — mutation test of the R96-C1 counter (`plans/round96_c1_replay.py`)

Seat: MutTesterC1 (leaf, round 96 RESIDUAL r1). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(branch master). Measured revision **T = `09717e49ff46fad5b255619d671aaaae52dfc180`**. Scratch clone
(`git clone --shared`, detached at T, toplevel asserted) and both venvs lived under
`/fast/scratch/hyaku/kengaku-r96/MutTesterC1/` and were removed after the receipts below were copied.

## 1. What was mutated

The counter bytes at T hash to
`0752287902145fe1adc49f985978905244dc906f1015eb88874b39182bf8940c`, the frozen-instruments row for
`plans/round96_c1_replay.py` in `plans/round-96-claims.md`. **43 single-point mutants** were generated
from exactly those bytes: one substring replacement each, the anchor's occurrence count asserted
`== 1`, and every mutant diff verified to be a single hunk (`mutants.json` carries the anchor and the
sha256 of each mutant; `mut/` holds the bytes). Nothing was written to the lane, and no instrument was
repaired in round (frozen rule).

**Detector.** For each (mutant, input) pair the mutant counter is run exactly as the frozen predicate
runs the real one — cwd = clone root, `--lane .`, absolute `--work` outside the lane, the same E/G
venvs, `/usr/bin/bwrap`:

```
cd <clone> && python3 <mutant>.py --lane . --rev <rev> --work <dir> \
    --env-venv <E> --grader-venv <G> --bwrap /usr/bin/bwrap
```

A mutant is **killed** if some input makes its `PREDICATE` line or exit code differ from the pristine
counter's on that same input. Full stdout is compared as a secondary signal, because the `TARGET` line
is not predicate-bearing.

**Inputs (31).** 27 fixture commits on T (each = T + exactly one edit, committed with a throwaway
clone-local identity after asserting `git rev-parse --show-toplevel` == the clone; `fixtures.json`),
plus 4 argument inputs: bad `--bwrap`, `--work` inside the lane, unresolved `--rev`, wrong cwd. The two
committed P2 controls were rebuilt: **do-nothing at P1b `e8a80c0e`** and the **forged receipt** (one
CASE `observed` edited in a fixture commit).

**175 pairs** were executed: every mutant at T, at P1b and at the forged receipt, plus the targeted
fixtures per mutation point.

## 2. Controls reproduced (calibration)

| control | receipt | result |
|---|---|---|
| T (pristine) | `runs/M00-orig--I0-T.txt` | byte-identical to `.ufo/waves/round-96/L1/c1-tip.txt` (diff clean): 9/9 legs, `TARGET executed_rows=40 … legs=68 mismatches=0 defects=0`, `PREDICATE R96-C1 pass`, rc 0 |
| P1b do-nothing | `runs/M00-orig--I1-P1b.txt` | byte-identical to `L1/controls/c1-do-nothing.txt` (diff clean): all 9 legs fail, 9 defects, rc 1 |
| forged receipt | `runs/M00-orig--I2-forged-case.txt` | L5+L6 fail, `mismatches=1 defects=2`, rc 1 — same shape as `L1/controls/c1-forged-receipt.txt`, which applied the edit twice (`mismatches=2 defects=3`, disclosed in the controls README) |

The pristine counter at T is therefore the same instrument the L1 measured, and both committed C1
controls reproduce.

## 3. Result — 43 mutants, 28 killed, 15 survived

| mutant | single-point change | killed by | verdict | pristine → mutant |
|---|---|---|---|---|
| M01-L1-true | `l1 = receipt_bytes is not None` → `l1 = True` | — | survived | rc1/fail → rc1/fail |
| M02-L2-true | `l2 = (all(` → `l2 = True or (all(` | I15-receipt-subjectsha | killed | rc1/fail → rc0/pass |
| M03-L3-true | `l3 = bool(tip)` → `l3 = True or bool(tip)` | I6-receipt-lanetip | killed | rc1/fail → rc0/pass |
| M04-L4-true | `l4 = bool(frozen.get(TABLE))` → `True or …` | I11-table-stamped | killed | rc1/fail → rc0/pass |
| M05-L5-true | `l5 = bool(predicted)` → `True or …` | — | survived | rc1/fail → rc1/fail |
| M06-L6-true | `l6 = rerun.returncode == 0 and` → `True or (…) and` | I23-receipt-obs-note | killed | rc1/fail → rc0/pass |
| M07-L7-true | `l7 = (member.get("status") == "executed"` → `True or (…` | I4-ledger-remove | killed | rc1/fail → rc0/pass |
| M08-L8-true | `l8 = bool(frozen.get(TOOL))` → `True or …` | I10-probe-stamped | killed | rc1/fail → rc0/pass |
| M09-L9-true | `l9 = (f.get("TOOL_SHA")` → `True or (…` | I7-receipt-hostbash | killed | rc1/fail → rc0/pass |
| M10-set-ge-eq | `rev_set >= base_set \| {MEMBER}` → `==` | I3-ledger-grow | killed | rc0/pass → rc1/fail |
| M11-cwd-flip | `if Path.cwd().resolve() != lane:` → `==` | IT-cwdtmp | killed | rc2/C-N-E → rc0/pass |
| M12-rc-flip | `return 0 if ok else 1` → `return 1 if ok else 0` | I0-T | killed | rc0/pass → rc1/pass |
| M13a-target-rows | `% (exec_total, MEMBER,` → `% (len(members), MEMBER,` | — | survived | rc0/pass → rc0/pass |
| M13b-target-member | `% (exec_total, MEMBER,` → `% (exec_total, "wrong-member",` | — | survived | rc0/pass → rc0/pass |
| M14-ancestor-dir | `--is-ancestor tip rev` → `--is-ancestor rev tip` | I0-T | killed | rc0/pass → rc1/fail |
| M15-l5-seen-subset | `seen == set(predicted)` → `seen <= set(predicted)` | — | survived | rc1/fail → rc1/fail |
| M16-round-95 | `member.get("round") == 96` → `== 95` | I13-ledger-round95 | killed | rc1/fail → rc0/pass |
| M17-drop-notinbase | drop `MEMBER not in base_set` | — | survived | rc0/pass → rc0/pass |
| M18-drop-legacy | drop `and legacy_ok` | I5-ledger-legacy | killed | rc1/fail → rc0/pass |
| M19-pins-first-only | pin loop over `list(PINS.items())[:1]` | — | survived | rc2/C-N-E → rc2/C-N-E |
| M20-l9-drop-hostbash | drop `HOST_BASH` equality | I7-receipt-hostbash | killed | rc1/fail → rc0/pass |
| M21-stamps-drop-graderside | drop `GRADER_SIDE` from `RERUN_STAMPS` | I8-receipt-graderside | killed | rc1/fail → rc0/pass |
| M22-work-guard-weaken | `work == lane or lane in work.parents` → `work == lane` | IB-workin | killed | rc2/C-N-E → rc0/pass |
| M23-drop-rev-guard | replace `raise CouldNotEvaluate(unresolved-revision)` with `pass` | — | survived | rc2/C-N-E → rc2/C-N-E |
| M24-drop-bwrap-check | `if not (bwrap is file and X_OK)` → `if False and …` | — | survived | rc2/C-N-E → rc2/C-N-E |
| M25-all-any | `ok = all(legs)` → `any(legs)` | I2-forged-case | killed | rc1/fail → rc0/pass |
| M26-exit2-to-0 | `sys.exit(2)` → `sys.exit(0)` | IC-revbogus | killed | rc2/C-N-E → rc0/C-N-E |
| M27-L2-drop-testsh | drop `TEST_SH_SHA` equality | I16-receipt-testsh | killed | rc1/fail → rc0/pass |
| M28-L2-drop-subjectsha | drop `SUBJECT_SHA` equality | I15-receipt-subjectsha | killed | rc1/fail → rc0/pass |
| M29-L5-pred-only | `obs != pred or pred != predicted[cid]` → `obs != pred` | — | survived | rc1/fail → rc1/fail |
| M30-L7-drop-receiptfield | drop `member.get("receipt") == RECEIPT` | I20-ledger-receiptpath | killed | rc1/fail → rc0/pass |
| M31-L7-drop-verdict | drop `member.get("verdict") == "cases"` | I21-ledger-verdict | killed | rc1/fail → rc0/pass |
| M32-L9-drop-tablesha | drop `CASE_TABLE_SHA` equality in L9 | — | survived | rc1/fail → rc1/fail |
| M33-L6-drop-obseq | `rerun_obs == receipt["obs"]` → `True` | I23-receipt-obs-note | killed | rc1/fail → rc0/pass |
| M34-L6-drop-rc | `l6 = rerun.returncode == 0 and` → `l6 = True and` | — | survived | rc0/pass → rc0/pass |
| M35-L3-drop-booltip | `l3 = bool(tip) and` → `l3 =` | — | survived | rc1/fail → rc1/fail |
| M36-L7-round-ge | `member.get("round") == 96` → `>= 96` | I18-ledger-round97 | killed | rc1/fail → rc0/pass |
| M37-L7-classes-superset | `classes == MEMBER_CLASSES` → `⊆` | I19-ledger-classes | killed | rc1/fail → rc0/pass |
| M38-L6-stamps-drop-envside | drop `ENV_SIDE` from `RERUN_STAMPS` | I25-receipt-envside | killed | rc1/fail → rc0/pass |
| M39-parse-observed-fallback | `parts.get("observed", "?")` → `parts.get("predicted", "?")` | — | survived | rc1/fail → rc1/fail |
| M40-L5-drop-len | drop `len(receipt["cases"]) == len(predicted)` | — | survived | rc1/fail → rc1/fail |
| M41-rerun-rc2-mapping | `if rerun.returncode == 2:` → `== 3` | I9-cap-dockerfile | killed | rc2/C-N-E → rc1/fail |
| M42-L2-drop-solvesha | drop `SOLVE_SHA` equality | I17-receipt-solvesha | killed | rc1/fail → rc0/pass |

Every killed mutant's receipt is `runs/<mutant>--<input>.txt`; the pristine side of each comparison is
`runs/M00-orig--<input>.txt`. The killing input is the one shown; several mutants are killed by more
than one input (M02 by I15 and I16; M03 by I6 and I26; M06 by I23 and I8; M07 by I4 and I5; M16 by I13
and T itself; M26 by IC and IT).

**Positive calibration on the round-95 repair.** The growth-tolerant set check is live: `>=` → `==`
(M10) is killed by a fixture that adds an executed member (`I3-ledger-grow`, executed 41), and the
removal direction is live too (`I4-ledger-remove` kills M07/M10). The ledger's `round`, `classes`,
`receipt`, `subject` and `verdict` fields each have a killing fixture (M16, M37, M30, M18, M31).

## 4. The 15 survivors — and which matter

In **every** surviving pair the pristine and mutant agree on `(PREDICATE, rc)`; no survivor lets the
counter print `pass` where the pristine prints `fail`. They are redundant checks, not holes in the
pass/fail boundary. Grouped by cause:

**A. L5 is subsumed by L4 ∧ L6 (M05, M15, M29, M39, M40).** L6 passes only if the rerun's observation
block equals the receipt's and the rerun exits 0 with the four stamps equal. The probe emits exactly
one `CASE <id> predicted=<table[cid]> observed=<measured> ok=<bool>` line per table case, in table
order, and nothing else inside `OBSERVATIONS_BEGIN/END` (the T receipt's block is exactly 17 CASE
lines). A passing L6 therefore forces the receipt's CASE lines to be the table's cases with the
table's predicted vectors — exactly what L5 checks, including `seen == set(predicted)` and the count.
L5 can only fail when L4 or L6 already fails. *Matters:* a case-level forgery is reported as an L6
defect, never as L5; the counter's nine legs overstate their independence. It does not weaken the
composite predicate.

**B. L1 is subsumed (M01).** L6 requires `bool(receipt["obs"])`, and L2/L9 also read receipt fields, so
an absent receipt always fails at least three legs. L1 has no unique detector.

**C. L2's pin loop cannot produce a `fail` (M19).** The probe re-checks all seven captured files
against its own PINS and exits 2 on any mismatch; the counter turns a rerun rc 2 into
`could-not-evaluate`. A tampered capture therefore yields rc 2 regardless of L2's loop (pristine I9
receipt: `runs/M00-orig--I9-cap-dockerfile.txt`, rc 2). *Matters:* the kill rule "a frozen file changes
after F" is still enforced (the predicate is not `pass`), but it is reported as could-not-evaluate, not
as a leg failure.

**D. L9's tool/table stamps are subsumed by L6 (M32).** `TOOL_SHA` and `CASE_TABLE_SHA` are in
`RERUN_STAMPS`, so a mismatch fails L6 first. Only `HOST_BASH` is unique to L9 — and it is live (M20
killed by I7).

**E. Dead or unreachable conditions (M17, M23, M24, M34, M35).**
- M17: `MEMBER not in base_set` is unreachable — BASE is a fixed historical commit (`45740a61`) whose
  ledger has the member unexecuted; the counter reads the ledger blob at that constant, so no input can
  make `base_set` contain the member.
- M23: without the unresolved-revision guard, `rev` becomes `""`, `git show ":path"` reads the index and
  `git archive ""` fails → `CouldNotEvaluate`, rc 2, same as with the guard.
- M24: without the bwrap check, the probe's own sandbox check exits 2 → the counter returns
  could-not-evaluate, same rc.
- M34: the probe exits 1 only when some case mismatched, which makes the observation block differ from
  the receipt's all-ok block, so L6 fails on the observation comparison anyway.
- M35: `git merge-base --is-ancestor "" rev` errors, so L3 fails even without `bool(tip)`.

**F. The TARGET line is not predicate-bearing (M13a, M13b).** Both mutants change only the printed
`TARGET` line; `PREDICATE` and rc are identical to pristine on all inputs, and they are killed only by
full-stdout comparison. *Matters:* the claim quotes the TARGET text, so that text is guarded by the
receipt diff (L1 `c1-tip.txt`), not by any leg. A TARGET-only defect would pass the predicate.

## 5. Measurement hazard found while running the matrix (fail-direction only)

Under host contention (load average 9–18 from concurrent seats; 5–6 of my own runs in parallel), the
probe's `Box.run` exceeded `CASE_TIMEOUT = 300` s and raised an **uncaught `subprocess.TimeoutExpired`**
at `run_case` (probe lines 226/315), or a pandas/pyarrow variant aborted with rc 134
(`terminate called without an active exception`). The probe then exits **1** with a partial observation
block, which the counter maps to **L6 fail** (`DEFECT L6 rerun rc=1 obs=N want=17`), i.e. a predicate
`fail`, not `could-not-evaluate`. 26 such receipts are preserved in `runs/crashed/`
(`probe-timeout-traceback.err` has the full traceback; `probe-load-diag.rc` shows 5 of 8 concurrent
probes failing this way).

Every affected pair was re-run serially and the final matrix uses the clean receipts. **Direction:** the
counter can only turn a true could-not-evaluate into `fail`, never into `pass`, so this cannot make a
not-met claim read as met. It can produce a spurious not-met under load. At T both the L1 receipt and
my independent run pass in ~16 s serial; R96-C1's verdict is unaffected.

## 6. Verdict on R96-C1 (mutation axis)

- The pristine counter at T reproduces the frozen predicate byte-identically (9/9 legs, the exact
  TARGET line, `pass`, rc 0) and both committed C1 controls reproduce.
- **No defect found that would flip R96-C1's verdict at T.** The pass/fail boundary survived all 43
  single-point mutants: every surviving mutant is a redundant check, and none lets the counter pass an
  input the pristine counter fails on.
- The round-95 repairs exercised here (growth-tolerant member-set check, subject re-pin to
  `tb2-header`) are live and bite in both directions.
- Findings below are routed to round 97; no instrument was changed in round (frozen rule).

## 7. Findings

- `FINDING M1 minor` — L5 has no independent kill power: five single-point mutants of L5 survive all
  175 pairs because L6's exact observation-block comparison (with L4) subsumes it; a case-level forgery
  is reported as L6, not L5. Predicate unaffected.
- `FINDING M2 minor` — a tampered captured file cannot produce a leg `fail`: the probe's own PINS check
  exits 2, so the counter reports `could-not-evaluate` (rc 2), not `fail` (rc 1). The frozen-file kill
  rule is still enforced (not `pass`), but the verdict class changes. Evidence:
  `runs/M00-orig--I9-cap-dockerfile.txt`, `runs/M19-pins-first-only--I9-cap-dockerfile.txt`.
- `FINDING M3 minor` — under load the probe's uncaught `TimeoutExpired` (or a pyarrow abort) exits 1
  with a partial observation block, which the counter reports as L6 `fail` rather than
  `could-not-evaluate`. Fail-direction only; no verdict flip. Evidence: `runs/crashed/`,
  `probe-timeout-traceback.err`.
- `FINDING M4 info` — L1, L9's `TOOL_SHA`/`CASE_TABLE_SHA`, L3's `bool(tip)`, L6's rerun-rc check,
  L7's `MEMBER not in base_set`, the unresolved-rev guard and the explicit bwrap check are each
  redundant with another leg or with the probe's own setup check (M01, M32, M35, M34, M17, M23, M24).
- `FINDING M5 info` — the `TARGET` line is not predicate-bearing: two TARGET-only mutants survive the
  `(PREDICATE, rc)` criterion and are killed only by full-stdout comparison (M13a, M13b).

## 8. Tooling

No installs or upgrades. Used the host's `python3 3.14.8`, `git 2.56.0`, `bubblewrap 0.13.1`, and the
pre-installed `uv` to stage the two venvs (`E` python 3.11.17 / pandas 2.2.3 / pyarrow 17.0.0 /
numpy 2.4.6; `G` python 3.13.16 / pandas 2.3.3 / pyarrow 22.0.0 / numpy 2.5.4). No pacman.

## 9. Receipts (all under `.ufo/waves/round-96/r1/MutTesterC1/`)

- `runs/` — 206 run receipts: `M00-orig--<input>.txt` (pristine per input) and
  `<mutant>--<input>.txt` (header carries the exact command and rc).
- `runs/crashed/` — 26 receipts of the load-induced probe crashes (preserved, superseded by serial
  re-runs).
- `mut/` — the 43 mutant source files plus `M00-orig.py`; `mutants.json` — anchor + sha256 per mutant.
- `fixtures.json` — the 27 fixture commits; `fixtures.py`, `fixtures2.py` — their builders.
- `plan.json` — the (mutant, input) matrix; `analysis.json` — every pair's verdict.
- `gen.py`, `gen2.py` — mutant generators; `driver2.py` — runner; `analyze.py` — comparison.
- `probe-timeout-traceback.err`, `probe-load-diag.rc` — the load-flake evidence.
