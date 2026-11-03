# Round 66 w1 — TensorRecon Findings

**Seat**: `TensorRecon` (read-only audit of R66-C1 table against the grader)  
**Date**: 2026-11-03  
**Lane Repo**: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`  
**Artifacts Audited**:
- `plans/round-66-claims.md` (R66-C1)
- `plans/round66_c1_tensor_probe.py`
- `corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py`
- Case files: `corpus/evidence/round66/tensor/cases/{k1-ref,k3-stub,k4-col-nogather,k5-row-noreduce}/parallel_linear.py` and `k2-none`
- Receipts: `corpus/evidence/round66/tensor/prefreeze-run2.txt`, `corpus/evidence/round66/tensor/receipt.txt`

---

## 1. Grounding of Frozen Vectors (K1–K5)

For each case K1..K5, the frozen outcome vector strictly follows from the grader's assertions and the case implementation (one line per case):

- **K1** (`k1-ref`, all 13 P): Follows from grader line 25 (`parallel_linear.py` exists), lines 72, 78, 87, 100, 106 (`ColumnParallelLinear` weight slice, bias, forward all-gather output, and backward gradients match reference), and lines 141, 146, 161, 174, 179 (`RowParallelLinear` weight slice, bias, forward all-reduce output, and backward gradients match reference).
- **K2** (`k2-none`, `exists=F` and all 12 layer tests `F`): Follows from grader line 25 (assertion failure: `/app/parallel_linear.py` does not exist), line 46 (all 6 column tests fail with `ModuleNotFoundError`), and line 115 (all 6 row tests fail with `ModuleNotFoundError`).
- **K3** (`k3-stub`, `exists=P` and all 12 layer tests `F`): Follows from grader line 25 (assertion passes: file exists), lines 60–65 (all 6 column tests fail with `NotImplementedError` on layer construction), and lines 129–134 (all 6 row tests fail with `NotImplementedError` on layer construction).
- **K4** (`k4-col-nogather`, `exists=P`, column ws1 P, column ws2/ws4 F, row all P): Follows from grader line 25 (assertion passes), lines 87, 100, 106 (column ws1 requires no gather and passes), line 87 (column ws2 and ws4 fail `allclose` assertion due to ungathered partial output dimension/values), and lines 141, 146, 161, 174, 179 (`RowParallelLinear` is unmodified K1 and passes all 6 tests).
- **K5** (`k5-row-noreduce`, `exists=P`, column all P, row ws1 P, row ws2/ws4 F): Follows from grader line 25 (assertion passes), lines 72, 78, 87, 100, 106 (`ColumnParallelLinear` is unmodified K1 and passes all 6 tests), lines 161, 174, 179 (row ws1 requires no reduction and passes), and line 161 (row ws2 and ws4 fail `allclose` assertion due to unreduced partial dot-products).

---

## 2. Numbered Findings

### Finding 1
- **Severity**: should-fix
- **Evidence line**: `plans/round66_c1_tensor_probe.py:221` (`jdir = receipt.parent / "junit"`) and `plans/round-66-claims.md:33` ("the junit directory is receipt-local, so a re-run cannot overwrite committed junit bytes").
- **Which file is wrong**: `plans/round66_c1_tensor_probe.py` (harness design defect) and `plans/round-66-claims.md` line 33 (claim premise violated in practice).
- **Detail**: The probe resolves its output junit directory as `receipt.parent / "junit"`. Because both `prefreeze-run2.txt` and `receipt.txt` are situated in `corpus/evidence/round66/tensor/`, running the post-freeze probe (`--run --receipt corpus/evidence/round66/tensor/receipt.txt`, committed in `2c1ef88a`) overwrote `corpus/evidence/round66/tensor/junit/*.xml` with the junit outputs of the post-freeze run. Consequently, running `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/prefreeze-run2.txt` in the current checkout fails with exit code 1 (`CHECK defect: k1-ref junit_sha does not match committed junit bytes...`). When tested against the original pre-freeze junit XMLs (commit `9a07df6a`), `prefreeze-run2.txt` passes with exit code 0 (`CHECK ok cases=5`, `PREDICATE R66-C1 pass`). The junit directory should either be keyed by the receipt name (e.g. `receipt.parent / f"junit-{receipt.stem}"`) or pre-freeze receipts should reside in their own subdirectory.

### Finding 2
- **Severity**: note
- **Evidence line**: `plans/round66_c1_tensor_probe.py:66-90`, `plans/round-66-claims.md:19`, and `corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py:18-211`.
- **Which file is wrong**: None (verified correct).
- **Detail**: The frozen table vectors in `plans/round66_c1_tensor_probe.py` match the claims doc specification and accurately reflect the pytest test suite execution for all 5 cases under offline bubblewrap sandboxing.

### Finding 3
- **Severity**: note
- **Evidence line**: `plans/round66_c1_tensor_probe.py:258-260` (`for case in CASES: if case not in seen: problems.append(...)`).
- **Which file is wrong**: None (verified correct).
- **Detail**: When a receipt is mutated by deleting `VECTOR k4-col-nogather`, `--check-receipt` refuses with exit code 1 and outputs first defect `CHECK defect: k4-col-nogather has no VECTOR line`. This verifies that the receipt checker enforces completeness across all frozen cases.

### Finding 4
- **Severity**: note
- **Evidence line**: `corpus/evidence/round66/tensor/receipt.txt:1-47` and `plans/round66_c1_tensor_probe.py:278-288`.
- **Which file is wrong**: None (verified correct).
- **Detail**: The post-freeze receipt of record `corpus/evidence/round66/tensor/receipt.txt` (committed in `2c1ef88a`) passes `--check-receipt` with exit code 0 (`CHECK ok cases=5`, `PREDICATE R66-C1 pass`), verifying that the post-freeze capability acquisition succeeds under the committed state.
