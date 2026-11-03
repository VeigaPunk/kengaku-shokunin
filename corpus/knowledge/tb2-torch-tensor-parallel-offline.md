source: S183 (corpus/SOURCES.md) — Terminal-Bench 2.0 torch-tensor-parallelism grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-tensor-parallelism/tests/test_outputs.py — anchor: tests/test_outputs.py lines 18-25 and 43-211 — sha256 4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290
verified-at: 2026-11-03 (receipt corpus/evidence/round66/tensor/receipt.txt; control corpus/evidence/round66/tensor/control-a1.txt)
recheck: python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt

# TB2 `torch-tensor-parallelism` — the grader replayed offline against a lane-built `parallel_linear.py`

## What the grader checks

The grader is Terminal-Bench 2.0 task `torch-tensor-parallelism`'s `tests/test_outputs.py` at pin
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`, sha256
`4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290` (`sha256sum
corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py`; the same value is line 171
of `corpus/evidence/round52/graders/SHA256SUMS`, and the round-66 capture
`corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py` hashes to it).

It has three test functions and thirteen outcomes. `test_parallel_linear_exists` (lines 18-25) asserts only that
`/app/parallel_linear.py` exists. `test_column_parallel_linear` and `test_row_parallel_linear` (lines 185-211) are each
parametrised over `bias` in `[True, False]` and `world_size` in `[1, 2, 4]`, giving six outcomes each; each runs
`mp.spawn(..., nprocs=world_size, join=True)`. The junit node names are exactly `test_parallel_linear_exists`,
`test_column_parallel_linear[<ws>-<bias>]` and `test_row_parallel_linear[<ws>-<bias>]` (the parameter order in the
node id is world size first). Counting command: `python3 -c "import xml.etree.ElementTree as ET; print(len(list(ET.parse('corpus/evidence/round66/tensor/receipt.junit/k1-ref.xml').iter('testcase'))))"` → `13`.

**Distributed mechanics.** `_setup_process_group` (lines 28-35) sets `MASTER_ADDR=localhost`, `MASTER_PORT=12355`
and calls `dist.init_process_group("gloo", ...)`. Each child tears down with `dist.barrier()` and
`dist.destroy_process_group()` (lines 37-40). The grader needs a gloo-capable torch and a free `127.0.0.1:12355`.

**The `master_weight` interface.** The grader builds a reference `nn.Linear(64, 48, bias=bias)` (seed 42, uniform
weight init), then constructs the candidate as `ColumnParallelLinear(in, out, bias=bias, master_weight=<reference
weight clone>)` (and `RowParallelLinear` likewise). The candidate must accept a `master_weight` keyword and expose
`weight` and `bias` as parameters. Its assertions compare, with `torch.allclose(..., atol=1e-5)`: the weight slice
per rank, the bias slice (column) or full bias (row), the forward output against the reference, and the weight and
bias gradient slices.

**Leg rule (frozen in `plans/round-66-claims.md`).** P iff the junit `testcase` has no `failure` or `error` child; F
otherwise. Setup failures (grader sha drift, missing venv, port 12355 busy, bwrap refusal, missing junit) are SETUP,
exit 2 — could-not-evaluate, never a verdict.

## The five frozen cases and their vectors

`plans/round66_c1_tensor_probe.py` freezes the table in its `frozen()` function. Keys: `exists` plus
`<kind>-ws<N>-bias<B>` (kind column or row; N in 1, 2, 4; B in True, False) — 13 keys. Case files are under
`corpus/evidence/round66/tensor/cases/`.

| case | what it is | frozen vector | `case_sha256` |
|---|---|---|---|
| K1 `k1-ref` | the lane's compliant reference build | all 13 P | `1537da2a2ea07293ec757641a0d2faee5e507518da9f96de45bebfd788193fc1` |
| K2 `k2-none` | do-nothing: `/app` empty | `exists` F, all 12 layer tests F | none (no file) |
| K3 `k3-stub` | stub: the module exists, both classes raise `NotImplementedError` | `exists` P, all 12 layer tests F | `316630cd45f0a3e2332bd38f98f4147977eba3d84aa54c5203edc5923986eadf` |
| K4 `k4-col-nogather` | mutant: `ColumnParallelLinear.forward` never gathers | `exists` P; column ws1 P, column ws2 and ws4 F; row all P | `37a3c21b324c262a5a777389cd242b8b3129b33cc4d1adb31d715cd806082b83` |
| K5 `k5-row-noreduce` | mutant: `RowParallelLinear.forward` never reduces | `exists` P; column all P; row ws1 P, row ws2 and ws4 F | `edf7cab1ee5798e135affe6ea9f884696cea4165d6f11d0e49bd3e458c291881` |

The receipt of record `corpus/evidence/round66/tensor/receipt.txt` carries these five vectors (`grep -c '^VECTOR'` → `5`;
each ends `frozen=match`) and ends `PREDICATE R66-C1 pass`. Its junit bytes are in `receipt.junit/`; each `CASE` line
names the junit sha256 of the file it refers to, and the counter re-derives the outcomes from those bytes.

**Counting command (after):** `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt; echo $?`
→ `CHECK ok cases=5`, `PREDICATE R66-C1 pass`, exit 0.

**Counting command (before):** `grep -c torch-tensor-parallelism corpus/evidence/round52/graders/executed17.lst` → `0`.

## The mutant design

K4 and K5 are K1 with one method body changed each. K4 replaces `ColumnParallelLinear.forward` with a bare
`F.linear(x, self.weight, self.bias)`, so each rank returns only its own slice. K5 removes the all-reduce from
`RowParallelLinear.forward`, so each rank returns its partial product plus bias. The lane's diff of each mutant
against K1 shows the method-body hunk and a module-docstring hunk (FreezeReview, `.ufo/waves/round-66/w1/FreezeReview.md`).

Both mutants are indistinguishable from K1 at world size 1, where no collective is needed, and fail at world sizes
2 and 4 on the side they break. A check that only looked at world size 1, or only at `exists`, would accept a broken
tensor-parallel layer. The receipt's `FRAGMENT` lines name the failure: K4 and K5 layer failures are
`torch.multiprocessing.spawn.ProcessRaisedException`; K2's `exists` failure is the `AssertionError` for the missing file.

K2 alone cannot satisfy the predicate: a receipt carrying only K2's `VECTOR` line is refused with
`CHECK defect: k1-ref has no VECTOR line` (and the other four), exit 1. The probe's selftest
(`python3 plans/round66_c1_tensor_probe.py --selftest --work <scratch>`) refuses a mutated vector, a receipt with no
`CASE` lines, and a malformed `VECTOR` token by name (`SELFTEST` all True, exit 0).

## Limits (named, not hidden)

- **The grader is the oracle.** Every P/F above is read from the grader's own junit XML by the counter. The lane's reading of the assertions is not evidence of the verdict.
- **K1 is the lane's reference build, not a Terminal-Bench 2.0 solution.** It was written by the lane to satisfy the grader. This entry prices an offline replay of the grader, not whether any agent can write this file.
- **The grader sees the API surface, not sharded execution.** A cheating K1 variant that keeps the whole master weight locally and reconstructs the output passes 13/13 with the same junit outcomes (ClaimFalsifier attack A4, measured before amendment A1; A1 does not change this, since the grader's assertions are unchanged).
- **The receipt check is not proof of execution.** It binds case bytes and junit bytes by sha and binds each `VECTOR` line to the outcomes its junit bytes record. A receipt hand-written with the committed bytes and frozen vectors still passes (ClaimFalsifier A5). Amendment A1 in `plans/round-66-claims.md` records this limit.
- **Torch install channel.** Official PyTorch CPU index, `torch==2.15.0+cpu`, installed with `uv pip install --index-url https://download.pytorch.org/whl/cpu` into `~/.local/share/kengaku-r66/venv-torch` (the venv is outside the scratch reaper's scope); `transformers==5.22.1` and `pytest==9.2.0` from PyPI into the same venv. Observed 2026-11-03: `torch.__version__` → `2.15.0+cpu`; `torch.distributed.is_gloo_available()` → `True`; python 3.14.8.
- **Port 12355 is a fixed constant in the pinned grader.** Two concurrent probes on the host collide; the probe refuses (SETUP, exit 2) rather than grading.
- **Coverage stays L0-capped at 7.** Executing this grader does not answer the open L0 question `kengaku | round-25/33/51`.
