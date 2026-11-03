# Round 66 w1 — Seat TensorRecon Scoped Report

**Seat**: `TensorRecon`  
**Role**: `scout` (read-only audit of the frozen R66-C1 table against the grader; no edits outside seat dir)  
**Lane**: `kengaku` (round 66, wave 1)  
**Host**: Arch Linux, kernel 7.2.11, python 3.14.8, gcc/gcov 16.2.1, bwrap 0.13.1, host sqlite3 3.54.0, uv 0.13.0  
**Tools installed or upgraded**: None (all tools present; pacman paused; no tool mutations)  
**Network opened**: None (read-only local audit)  
**Ports bound**: None (port 12355 unmolested)  

---

## 1. Executive Summary & Verdicts Table

| Check | Command | Observed Output / Exit Code | Verdict |
|---|---|---|---|
| K1..K5 grounding in grader | Inspection of `test_outputs.py` lines 18–26, 43–110, 112–182, 185–211 | All 5 frozen vectors follow from grader assertions | **MATCH** |
| Control check (`prefreeze-run2.txt` on repo checkout) | `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/prefreeze-run2.txt` | First finding: `CHECK defect: k1-ref junit_sha does not match committed junit bytes`, exit 1 | **FAIL (Overwritten junit)** |
| Control check (`prefreeze-run2.txt` with original pre-freeze junit at `9a07df6a`) | `python3 plans/round66_c1_tensor_probe.py --check-receipt <prefreeze-isolated>/prefreeze-run2.txt` | `CHECK ok cases=5`, `PREDICATE R66-C1 pass`, exit 0 | **PASS** |
| Negative mutant check (`mutant.txt` without `VECTOR k4-col-nogather`) | `python3 plans/round66_c1_tensor_probe.py --check-receipt <scratch>/mutant.txt` | First finding: `CHECK defect: k4-col-nogather has no VECTOR line`, exit 1 | **REFUSED (Expected)** |
| Post-freeze receipt of record (`receipt.txt` at `2c1ef88a`) | `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt` | `CHECK ok cases=5`, `PREDICATE R66-C1 pass`, exit 0 | **PASS** |

---

## 2. K1..K5 Grounding Against Grader Assertions (One Line Per Case)

- **K1** (`k1-ref`, all 13 P): Follows from grader line 25 (`parallel_linear.py` exists), lines 72, 78, 87, 100, 106 (`ColumnParallelLinear` weight slice, bias, forward all-gather output, and backward gradients match reference), and lines 141, 146, 161, 174, 179 (`RowParallelLinear` weight slice, bias, forward all-reduce output, and backward gradients match reference).
- **K2** (`k2-none`, `exists=F` and all 12 layer tests `F`): Follows from grader line 25 (assertion failure: `/app/parallel_linear.py` does not exist), line 46 (all 6 column tests fail with `ModuleNotFoundError`), and line 115 (all 6 row tests fail with `ModuleNotFoundError`).
- **K3** (`k3-stub`, `exists=P` and all 12 layer tests `F`): Follows from grader line 25 (assertion passes: file exists), lines 60–65 (all 6 column tests fail with `NotImplementedError` on layer construction), and lines 129–134 (all 6 row tests fail with `NotImplementedError` on layer construction).
- **K4** (`k4-col-nogather`, `exists=P`, column ws1 P, column ws2/ws4 F, row all P): Follows from grader line 25 (assertion passes), lines 87, 100, 106 (column ws1 requires no gather and passes), line 87 (column ws2 and ws4 fail `allclose` assertion due to ungathered partial output dimension/values), and lines 141, 146, 161, 174, 179 (`RowParallelLinear` is unmodified K1 and passes all 6 tests).
- **K5** (`k5-row-noreduce`, `exists=P`, column all P, row ws1 P, row ws2/ws4 F): Follows from grader line 25 (assertion passes), lines 72, 78, 87, 100, 106 (`ColumnParallelLinear` is unmodified K1 and passes all 6 tests), lines 161, 174, 179 (row ws1 requires no reduction and passes), and line 161 (row ws2 and ws4 fail `allclose` assertion due to unreduced partial dot-products).

---

## 3. Empirical Receipt Check Executions

### 3.1 Pre-freeze control receipt on current repo checkout
```bash
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round66_c1_tensor_probe.py \
  --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round66/tensor/prefreeze-run2.txt ; echo $?
```
**Output**:
```
CHECK defect: k1-ref junit_sha does not match committed junit bytes
CHECK defect: k2-none junit_sha does not match committed junit bytes
CHECK defect: k3-stub junit_sha does not match committed junit bytes
CHECK defect: k4-col-nogather junit_sha does not match committed junit bytes
CHECK defect: k5-row-noreduce junit_sha does not match committed junit bytes
PREDICATE R66-C1 fail
1
```
- **Exit code**: `1`
- **First finding line**: `CHECK defect: k1-ref junit_sha does not match committed junit bytes`
- **Cause**: Commit `2c1ef88a` ran `--run --receipt corpus/evidence/round66/tensor/receipt.txt`, which wrote newly generated junit XMLs to `corpus/evidence/round66/tensor/junit/`, overwriting the pre-freeze junit XMLs. When tested against the original pre-freeze junit XMLs from commit `9a07df6a`, `prefreeze-run2.txt` exits 0 with `PREDICATE R66-C1 pass`.

### 3.2 Mutant receipt (VECTOR line for k4-col-nogather deleted)
```bash
cp -r /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round66/tensor/junit /fast/scratch/hyaku/kengaku-r66/TensorRecon/junit
grep -v "^VECTOR k4-col-nogather" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round66/tensor/prefreeze-run2.txt > /fast/scratch/hyaku/kengaku-r66/TensorRecon/mutant.txt
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round66_c1_tensor_probe.py \
  --check-receipt /fast/scratch/hyaku/kengaku-r66/TensorRecon/mutant.txt ; echo $?
```
**Output**:
```
CHECK defect: k4-col-nogather has no VECTOR line
CHECK defect: k1-ref junit_sha does not match committed junit bytes
CHECK defect: k2-none junit_sha does not match committed junit bytes
CHECK defect: k3-stub junit_sha does not match committed junit bytes
CHECK defect: k4-col-nogather junit_sha does not match committed junit bytes
CHECK defect: k5-row-noreduce junit_sha does not match committed junit bytes
PREDICATE R66-C1 fail
1
```
- **Exit code**: `1`
- **First finding line**: `CHECK defect: k4-col-nogather has no VECTOR line`

### 3.3 Post-freeze receipt of record
```bash
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round66_c1_tensor_probe.py \
  --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round66/tensor/receipt.txt ; echo $?
```
**Output**:
```
CHECK ok cases=5
PREDICATE R66-C1 pass
0
```
- **Exit code**: `0`
- **Verdict**: `PREDICATE R66-C1 pass`

---

## 4. Numbered Findings

1. **Finding 1 (Severity: should-fix)**
   - **Evidence line**: `plans/round66_c1_tensor_probe.py:221` and `plans/round-66-claims.md:33`.
   - **Which file is wrong**: `plans/round66_c1_tensor_probe.py` and claim premise in `plans/round-66-claims.md`.
   - **Details**: `plans/round-66-claims.md` line 33 states "the junit directory is receipt-local, so a re-run cannot overwrite committed junit bytes". However, in `round66_c1_tensor_probe.py`, `jdir` is computed as `receipt.parent / "junit"`. Because both `prefreeze-run2.txt` and `receipt.txt` live in `corpus/evidence/round66/tensor/`, the post-freeze run over `receipt.txt` overwrote the committed junit XML files in `corpus/evidence/round66/tensor/junit/`. Consequently, `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/prefreeze-run2.txt` fails on the current tree. The probe should isolate junit directories by receipt stem (e.g. `receipt.parent / f"junit-{receipt.stem}"`) or receipt paths should be in separate subdirectories.

2. **Finding 2 (Severity: note)**
   - **Evidence line**: `plans/round66_c1_tensor_probe.py:66-90`, `plans/round-66-claims.md:19`, and `corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py:18-211`.
   - **Which file is wrong**: None (verified correct).
   - **Details**: The frozen table vectors in `plans/round66_c1_tensor_probe.py` match the claims doc specification and accurately reflect the pytest test suite execution for all 5 cases under offline bubblewrap sandboxing.

3. **Finding 3 (Severity: note)**
   - **Evidence line**: `plans/round66_c1_tensor_probe.py:258-260`.
   - **Which file is wrong**: None (verified correct).
   - **Details**: Deleting `VECTOR k4-col-nogather` causes `--check-receipt` to fail with exit code 1 and first finding line `CHECK defect: k4-col-nogather has no VECTOR line`, confirming completeness verification.

4. **Finding 4 (Severity: note)**
   - **Evidence line**: `corpus/evidence/round66/tensor/receipt.txt:1-47` and `plans/round66_c1_tensor_probe.py:278-288`.
   - **Which file is wrong**: None (verified correct).
   - **Details**: Post-freeze receipt of record `corpus/evidence/round66/tensor/receipt.txt` passes with exit code 0 (`CHECK ok cases=5`, `PREDICATE R66-C1 pass`).

---

## 5. Artifacts and Evidence Written
- `.ufo/waves/round-66/w1/TensorRecon/findings.md`
- `.ufo/waves/round-66/w1/TensorRecon/check-prefreeze-run2.txt`
- `.ufo/waves/round-66/w1/TensorRecon/check-mutant.txt`
- `.ufo/waves/round-66/w1/TensorRecon/check-receipt-record.txt`
- `.ufo/waves/round-66/w1/TensorRecon/check-prefreeze-isolated.txt`
- `.ufo/waves/round-66/w1/TensorRecon/check-mutant-isolated.txt`
- `.ufo/waves/round-66/w1/TensorRecon.md` (this report)
