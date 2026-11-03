# ProbeMutate — R67-C1 receipt checker, mutate-run-revert (round 67, w1)

Seat: `ProbeMutate`. Target: the frozen checker `plans/round67_c1_pipeline_probe.py`
(sha256 `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836`, version `r67-c1/1`),
`--check-receipt` path only. No grader run, no pytest, no listener on 127.0.0.1:12355, no `flock`
(the checker opens no socket; `check_receipt` at `plans/round67_c1_pipeline_probe.py:236-300` reads
the receipt, the sibling junit dir, the committed case files and the grader bytes only).

Scratch: `/fast/scratch/hyaku/kengaku-r67/ProbeMutate` (removed after this file was written).
Lane writes: only this directory and `.ufo/waves/round-67/w1/ProbeMutate.md`.

## Base copy (byte-identical to the files of record)

| file | sha256 |
|---|---|
| base/receipt.txt (copy of `corpus/evidence/round67/pipe/receipt.txt`) | `a9b9735bcc42fa673540de6e7c70cdfc45b97e008b033492033942261554f1e7` |
| base/receipt.junit/q1-ref.xml | `d3ebcfd9d6ceb0df48b88e7fa4a4de4b6bec703b2e5dd7736d77e59c054a0b83` |
| base/receipt.junit/q2-none.xml | `7745544727a1cf4890b01acbece03165b2f6a25d8de1cbc1be02c0e374dc4522` |
| base/receipt.junit/q3-stub.xml | `5e15cf01ba02794ee7a6afdfbf892a7867b961c07d88a1db18019dc59e29e65c` |
| base/receipt.junit/q4-hooks-noop.xml | `4f27c5621d7566ee0cbeafdc1c068eab3748dcd77af11fac6e4a5789376615c3` |
| base/receipt.junit/q5-full-model.xml | `a132830bd79974005382a803a106cd5aba697e109a3e47891318dbf0daadb1fa` |
| base/receipt.junit/q6-unscaled-loss.xml | `3b711f67dac0a82009008f7c017d7ad918732d9d9685a6e6d171828f82afae66` |

Every mutant is `base` with exactly one change, asserted at build time (one changed line, or one
removed line, or one removed junit file): `make_mutants.py` aborts if a mutant differs on more than
one line. Per-mutant diffs are in `diffs/`.

## Detector

Detector command, run as root `python3` (3.14.8, `/usr/bin/python3`) with cwd = the lane and
`PYTHONDONTWRITEBYTECODE=1`:

```
python3 plans/round67_c1_pipeline_probe.py --check-receipt <target>/receipt.txt
```

Exit semantics: 0 predicate pass, 1 predicate fail (defect found), 2 could-not-evaluate.

## Results

`verdict` is killed (rc 1 with at least one `CHECK defect:`), survived (rc 0), or
inconclusive (baseline failure). Base was run first and last: rc 0 both times.
Predictions were formed from reading `check_receipt` before the mutants were generated
(`predicted` column); a wrong prediction is a calibration datum.

| # | mutant (single change) | expected rc | predicted | observed rc | finding text | verdict |
|---|---|---|---|---|---|---|
| 0 | base (unmodified copy) | 0 | 0 | **0** | `CHECK ok cases=6` / `PREDICATE R67-C1 pass` | baseline green |
| m01 | `VECTOR q1-ref exists=P`→`F` | 1 | 1 | **1** | `CHECK defect: q1-ref vector FPPP != frozen PPPP`; `CHECK defect: VECTOR q1-ref FPPP disagrees with its junit PPPP` (2) | killed |
| m02 | delete the `VECTOR q3-stub` line | 1 | 0 | **0** | `CHECK ok cases=6` / `PREDICATE R67-C1 pass` | **survived** |
| m03 | delete the `CASE q4-hooks-noop` line | 1 | 1 | **1** | `CHECK defect: missing CASE/VECTOR for q4-hooks-noop` (1) | killed |
| m04 | `CASE q1-ref case_sha256` → 64 zeros | 1 | 1 | **1** | `CHECK defect: case_sha mismatch for q1-ref` (1) | killed |
| m05 | `CASE q6-unscaled-loss junit_sha256` → 64 zeros | 1 | 1 | **1** | `CHECK defect: junit sha mismatch for q6-unscaled-loss` (1) | killed |
| m06 | `PROBE sha256` → 64 zeros | 1 | 1 | **1** | `CHECK defect: PROBE sha does not match committed probe bytes` (1) | killed |
| m07 | `PROBE version=r67-c1/1` → `r67-c1/9` | 1 | 1 | **1** | `CHECK defect: PROBE version does not match the probe` (1) | killed |
| m08 | `GRADER sha256` → 64 zeros | 1 | 1 | **1** | `CHECK defect: GRADER line missing or not the pinned sha` (1) | killed |
| m09 | `VECTOR q5-full-model ws2=F` → `P` (row `PPPP`) | 1 | 1 | **1** | `CHECK defect: q5-full-model vector PPPP != frozen PPPF`; `CHECK defect: VECTOR q5-full-model PPPP disagrees with its junit PPPF` (2) | killed |
| m10 | delete `receipt.junit/q3-stub.xml` (receipt bytes unchanged, sha `a9b9735b…`) | 1 | 1 | **1** | `CHECK defect: junit missing for q3-stub` (1) | killed |
| m11 | `CASE q4-hooks-noop rc=1` → `rc=7` (extra) | 1 | 0 | **0** | `CHECK ok cases=6` / `PREDICATE R67-C1 pass` | **survived** |
| m12 | `VECTOR q4-hooks-noop frozen=match` → `frozen=mismatch` (extra) | 1 | 0 | **0** | `CHECK ok cases=6` / `PREDICATE R67-C1 pass` | **survived** |
| X | compound diagnostic: m02 **plus** `receipt.junit/q3-stub.xml` replaced by the `q1-ref` bytes (`d3ebcfd9…`; the `CASE q3-stub` line still claims `junit_sha256=5e15cf01…`) | 1 | 0 | **0** | `CHECK ok cases=6` / `PREDICATE R67-C1 pass` | **survived** |

Tracebacks: **0 of 14** runs (`grep -c Traceback` over every captured stdout+stderr). No run printed
`SETUP` and none exited 2. Run 1 and run 2 of the whole matrix produced byte-identical stdout.

Killed: **9 of 12** single-change mutants (m01, m03, m04, m05, m06, m07, m08, m09, m10).
Survived: **3 of 12** (m02, m11, m12), plus the compound diagnostic.

## What the survivors are (coverage findings; contract not changed)

1. **m02 — the `VECTOR`/`CASE` pairing is checked in one direction only.** `check_receipt` records
   cases from `CASE` lines into `seen` (`:263-276`) and validates the frozen vector, the junit sha
   and the case sha *inside* the `VECTOR` branch (`:277-295`). The completeness check is
   `missing = [c for c in CASES if c not in seen]` (`:296`) — `seen` is CASE-derived, so a receipt
   with five `VECTOR` lines and six `CASE` lines passes, and `CHECK ok cases=6` still prints
   (the count is `len(seen)`, i.e. CASE lines). There is no `VECTOR`-count or `VECTOR`⊇`CASE` check,
   so deleting a `VECTOR` line silently disables the junit-sha, junit-parses and vector-vs-junit
   checks for that case. The frozen predicate text ("the receipt carries six VECTOR lines whose
   outcome vectors equal the frozen table") is therefore **not** what the counter enforces; the
   counter enforces five-or-more. The receipt of record carries all six, so the C1 predicate over
   that receipt is unaffected.
2. **X — the gap is exploitable, not cosmetic.** Dropping the `VECTOR q3-stub` line and replacing
   `receipt.junit/q3-stub.xml` with a different junit (the all-passing `q1-ref` bytes) still prints
   `CHECK ok cases=6` and `PREDICATE R67-C1 pass`, rc 0, although the `CASE q3-stub` line's
   `junit_sha256` no longer matches the file on disk. A failing leg of a case can be hidden by
   removing one line.
3. **m11 — `rc=` on a `CASE` line is parsed and discarded.** The regex accepts `rc=(-?\d+)`
   (`:269`) but the value is never compared to anything (no rc is derivable without re-running the
   case, so this is arguably an acknowledged limit; it is nonetheless unvalidated evidence text).
4. **m12 — `frozen=` on a `VECTOR` line is parsed and discarded.** The regex accepts
   `frozen=(match|mismatch)` (`:271`) but the recomputed `vec == FROZEN_TABLE[case]` verdict is not
   compared to the receipt's own label, so a receipt that says `frozen=mismatch` on a vector that
   matches frozen still passes. The label is presentation, not evidence.

Severity for this round: all three survivors are in the *forward* direction (a receipt can be
weaker than it looks). The receipt of record is intact — six `VECTOR` lines, all `frozen=match`,
all junit shas recomputed — so **R67-C1's predicate over `corpus/evidence/round67/pipe/receipt.txt`
is not contradicted by this probe**. What is contradicted is the strength the predicate prose
attributes to the counter for any other receipt. Per the seat role, this is reported as a coverage
finding; the frozen predicate, the frozen table and the receipt were not edited.

## Restoration evidence

- Mutants were reverted by deleting the scratch mutant directories (`rm -rf mut compound` before
  the final base re-run); no committed byte was ever written. The checker reads the receipt given on
  the command line and writes nothing.
- Base copy sha256 before the matrix and after: `a9b9735bcc42fa673540de6e7c70cdfc45b97e008b033492033942261554f1e7`
  (identical to the committed receipt at both ends).
- Committed files, sha256 unchanged before and after the whole seat:
  `corpus/evidence/round67/pipe/receipt.txt` = `a9b9735b…f1e7`;
  `plans/round67_c1_pipeline_probe.py` = `32bacf1d…b836`.
- `git -C <lane> status --porcelain -- plans corpus/evidence/round67/pipe` printed only the two
  pre-existing `??` entries (the round's receipt and its junit dir, mtime 18:54, before this seat
  started at 19:00); no modified tracked file, no `__pycache__` under `plans/`
  (`PYTHONDONTWRITEBYTECODE=1` on every run).
- Scratch `/fast/scratch/hyaku/kengaku-r67/ProbeMutate` removed after the receipts below were
  copied into this seat dir.

## Commands (exact, with exit codes)

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /fast/scratch/hyaku/kengaku-r67/ProbeMutate/make_mutants.py   # rc 0, 12 mutants
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /fast/scratch/hyaku/kengaku-r67/ProbeMutate/run_all.py        # rc 0, 14 targets
PYTHONDONTWRITEBYTECODE=1 python3 plans/round67_c1_pipeline_probe.py --check-receipt /fast/scratch/hyaku/kengaku-r67/ProbeMutate/base/receipt.txt      # rc 0
PYTHONDONTWRITEBYTECODE=1 python3 plans/round67_c1_pipeline_probe.py --check-receipt /fast/scratch/hyaku/kengaku-r67/ProbeMutate/mut/<m>/receipt.txt    # rc per table
PYTHONDONTWRITEBYTECODE=1 python3 plans/round67_c1_pipeline_probe.py --check-receipt /fast/scratch/hyaku/kengaku-r67/ProbeMutate/compound/receipt.txt   # rc 0
```

Machine-readable matrix with receipt shas: `results.tsv`. Mutant build manifest: `manifest.tsv`.
Captured stdout for every target: `out/<target>.txt`. Single-change diffs: `diffs/`.
