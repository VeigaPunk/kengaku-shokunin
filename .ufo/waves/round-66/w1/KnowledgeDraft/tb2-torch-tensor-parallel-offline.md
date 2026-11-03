source: S183 (corpus/SOURCES.md) — Terminal-Bench 2.0 torch-tensor-parallelism grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-tensor-parallelism/tests/test_outputs.py — anchor: tests/test_outputs.py lines 18-25 and 43-211 — sha256 4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290
verified-at: 2026-11-03 (receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round66/tensor/receipt.txt)
recheck: python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt

# TB2 `torch-tensor-parallelism` — a tensor-parallel grader replayed offline against a lane-built `parallel_linear.py`

## What the grader checks

The grader is Terminal-Bench 2.0 task `torch-tensor-parallelism`'s `tests/test_outputs.py` at pin
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`: sha256
`4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`
(`sha256sum corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py`;
the same line is `corpus/evidence/round52/graders/SHA256SUMS` line 171, and the lane's
round-66 capture `corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py`
hashes to the same sha — 7171 bytes, 211 lines, `wc -c` / `wc -l`). The probe runs the grader's
own pytest module — never a copy, never a rewrite — once per frozen case, inside a bubblewrap
sandbox whose `/app` is the case directory and whose `/tests/test_outputs.py` is the byte-pinned
grader.

Three test functions, 13 test outcomes per case (counted by parsing the junit XML:
`python3 -c "import xml.etree.ElementTree as ET; print(len(list(ET.parse('corpus/evidence/round66/tensor/junit/k1-ref.xml').iter('testcase'))))"`
→ `13`; the same count holds for all five junit files):

| # | grader test name (exact) | lines | what it asserts |
|---|---|---|---|
| 1 | `test_parallel_linear_exists` | 18-25 | only `assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"` — that `/app/parallel_linear.py` exists; nothing about its content |
| 2 | `test_column_parallel_linear` | 187-199 | `@pytest.mark.parametrize("bias", [True, False])` × `@pytest.mark.parametrize("world_size", [1, 2, 4])` → 6 outcomes; each calls `mp.spawn(_test_column_parallel_linear, args=(world_size, bias), nprocs=world_size, join=True)` (193-198) |
| 3 | `test_row_parallel_linear` | 203-211 | same parametrisation → 6 outcomes; `mp.spawn(_test_row_parallel_linear, args=(world_size, bias), nprocs=world_size, join=True)` (209-210) |

The junit node names are exact (`test_parallel_linear_exists`,
`test_column_parallel_linear[1-True]`, `test_column_parallel_linear[1-False]`,
`test_column_parallel_linear[2-True]`, `test_column_parallel_linear[2-False]`,
`test_column_parallel_linear[4-True]`, `test_column_parallel_linear[4-False]`,
`test_row_parallel_linear[1-True]`, `test_row_parallel_linear[1-False]`,
`test_row_parallel_linear[2-True]`, `test_row_parallel_linear[2-False]`,
`test_row_parallel_linear[4-True]`, `test_row_parallel_linear[4-False]`) — read from
`corpus/evidence/round66/tensor/junit/*.xml`.

**Distributed mechanics (the inner functions, lines 43-182).** `_setup_process_group` (28-35) sets
`os.environ["MASTER_ADDR"] = "localhost"` and `os.environ["MASTER_PORT"] = "12355"` and calls
`dist.init_process_group(backend, rank=rank, world_size=world_size)` with `backend = "gloo"`
(line 33). Every layer test runs its child processes through `mp.spawn` — one child per rank,
`nprocs=world_size` — and each child tears down with `dist.barrier()` then
`dist.destroy_process_group()` (`_cleanup_process_group`, 37-40). The grader therefore needs a
gloo-capable torch and a free `127.0.0.1:12355`; the probe refuses to run (SETUP, exit 2) when
that port is busy, and takes `flock` on `~/.local/share/kengaku-r66/port-12355.lock` around the battery.

**The `master_weight` interface.** The grader builds the reference with `nn.Linear(in_features,
out_features, bias=bias)` at `batch_size, in_features, out_features = 2, 64, 48`, seeds
`torch.manual_seed(42)` and uniform-inits the weight with `bound = math.sqrt(1 / in_features)`,
then constructs the candidate as `ColumnParallelLinear(in_features, out_features, bias=bias,
master_weight=reference_layer.weight.clone().detach())` (and the same for `RowParallelLinear`).
The candidate must therefore accept a keyword `master_weight` tensor and expose `self.weight` /
`self.bias` as parameters. The grader's own assertions, all `torch.allclose(..., atol=1e-5)`: the
weight slice equals `reference_layer.weight[start_idx:end_idx, :]` for column
(`start_idx = rank * (out_features // world_size)`) and `reference_layer.weight[:, start_idx:end_idx]`
for row (`start_idx = rank * (in_features // world_size)`); the bias slice equals
`reference_layer.bias[start_idx:end_idx]` for column and the *full* `reference_layer.bias` for row;
the forward output equals the reference output; the weight gradient slice equals the reference
gradient slice; and the bias gradient matches for column (slice) and row (full).

Leg rule (frozen in `plans/round-66-claims.md`): **P** iff the junit `testcase` has no
`failure`/`error` child; **F** otherwise. Setup failures (grader sha drift, missing venv, port 12355 busy, bwrap refusal, missing junit) are SETUP / exit 2 — could-not-evaluate, never a verdict.

## The five frozen cases and their vectors

`plans/round66_c1_tensor_probe.py` freezes the outcome table in its `frozen()` function; the receipt's `VECTOR` lines are compared against it. Outcome keys are `exists` plus `<kind>-ws<N>-bias<B>` with kind ∈ {column,row}, N ∈ {1,2,4}, B ∈ {True,False} — 13 keys.

| case | setup | frozen vector | `case_sha256` (`sha256sum corpus/evidence/round66/tensor/cases/*/parallel_linear.py`) | junit sha (from the receipt's `CASE` line) |
|---|---|---|---|---|
| K1 `k1-ref` | compliant lane reference build of `ColumnParallelLinear` + `RowParallelLinear` | 13/13 P | `1537da2a2ea07293ec757641a0d2faee5e507518da9f96de45bebfd788193fc1` | `7e7ccace84d1bb366676b005750672866e77d5604ebfb07a9ebef6f2b5f1360a` |
| K2 `k2-none` | do-nothing: `/app` empty (probe builds it at run time, `case_sha=none`) | `exists` F, all 12 layer tests F | none | `f2987493329fe2f8c32afa60e3566803c9753e1328c50ef40f9c4848392f3ad9` |
| K3 `k3-stub` | stub control: the module exists, both layer classes `raise NotImplementedError` | `exists` P, all 12 layer tests F | `316630cd45f0a3e2332bd38f98f4147977eba3d84aa54c5203edc5923986eadf` | `ef592bad63e0cef702e7a0d56be4ada641c64dbfdb0eaa68c160b1e0dc3b97dc` |
| K4 `k4-col-nogather` | mutant: `ColumnParallelLinear.forward` never all-gathers | `exists` P; column ws1 P, column ws2/ws4 F; row all P | `37a3c21b324c262a5a777389cd242b8b3129b33cc4d1adb31d715cd806082b83` | `87797c920c5a3f5c6389963c552759e0a7c62f31de32ae941209c01bcfdd7660` |
| K5 `k5-row-noreduce` | mutant: `RowParallelLinear.forward` never all-reduces | `exists` P; column all P; row ws1 P, row ws2/ws4 F | `edf7cab1ee5798e135affe6ea9f884696cea4165d6f11d0e49bd3e458c291881` | `d1141289b23710842971f8bf92db1ff9db2120088dbdf8f33a3cdf482f8c7920` |

The receipt of record carries the same five vectors: `grep '^VECTOR' corpus/evidence/round66/tensor/receipt.txt`
prints five lines, each ending `frozen=match`, and the file ends `PREDICATE R66-C1 pass`. The
pre-freeze control receipt `corpus/evidence/round66/tensor/prefreeze-run2.txt` has
**byte-identical `VECTOR` lines** (`diff <(grep '^VECTOR' receipt.txt) <(grep '^VECTOR' prefreeze-run2.txt)`
→ no output) but different junit shas: the junit XML carries run-local paths and child-process
ids, so the junit bytes are not reproducible across runs even when the vectors are.

**Counting command (after):** `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt; echo $?`
→ `CHECK ok cases=5`, `PREDICATE R66-C1 pass`, exit 0 (observed 2026-11-03).

**Counting command (before):** `grep -c torch-tensor-parallelism corpus/evidence/round52/graders/executed17.lst`
→ `0`; `grep -n 'CLASS process-environment' corpus/evidence/round62/class-survey.txt` → line 14,
`CLASS process-environment count=3 members=install-windows-3.11,torch-pipeline-parallelism,torch-tensor-parallelism`,
still in the uncovered list at line 21 (`EXECUTED-COVERAGE executed=17 classified=17 classes-covered=12 classes-uncovered=network-service,process-environment,db-state,container-image`).

## The mutant design

K4 and K5 are the discrimination cases: each is K1 with exactly **one method body** changed, and
each fails only where the removed collective is actually needed.

- **K4** replaces `ColumnParallelLinear.forward`'s gather block (`dist.all_gather(gathered,
  local.detach().contiguous()); gathered[_rank()] = local; return torch.cat(gathered, dim=-1)`)
  with a bare `return F.linear(x, self.weight, self.bias)` — the rank returns only its own output
  slice. `RowParallelLinear` is the K1 build unchanged.
- **K5** deletes `RowParallelLinear.forward`'s reduce block (`dist.all_reduce(reduced,
  op=dist.ReduceOp.SUM); local = local + (reduced - local).detach()`) — each rank returns its own
  partial product plus the bias. `ColumnParallelLinear` is the K1 build unchanged.

Measured: an AST comparison of the class-qualified method bodies
(`python3 -c "import ast,pathlib; ..."` over
`corpus/evidence/round66/tensor/cases/*/parallel_linear.py`) reports
`k4-col-nogather: differing method bodies = ['ColumnParallelLinear.forward'] (n=1)` and
`k5-row-noreduce: differing method bodies = ['RowParallelLinear.forward'] (n=1)`; the same
comparison reports K3 differing in 4 method bodies (both `__init__`s and both `forward`s) plus
the dropped module-level helpers. A plain `diff` of K1 against K4 shows the module docstring also
differs — the *behavioural* delta is the one method body in each mutant.

**The failure is world-size-selective.** Both mutants are indistinguishable from K1 at world size
1 (no collective is needed there) and fail at world sizes 2 and 4, on the side they break:
K4 → `column-ws2-*` and `column-ws4-*` F, all `row-*` P; K5 → `row-ws2-*` and `row-ws4-*` F, all
`column-*` P (receipt `VECTOR` lines). A counter that only looked at world size 1, or that
checked only the `exists` leg, would call K4 and K5 identical to K1 and would accept a broken
tensor-parallel implementation. The receipt's `FRAGMENT` lines name the mechanism: every failing
K4/K5 outcome is `torch.multiprocessing.spawn.ProcessRaisedException`, while K2's `exists`
failure is `AssertionError: File /app/parallel_linear.py does not exist` (receipt
`corpus/evidence/round66/tensor/receipt.txt`).

**K2 cannot satisfy the predicate alone.** `--check-receipt` requires a `VECTOR` line for each of
the five cases: a receipt carrying only K2's `VECTOR` line is refused with
`CHECK defect: k1-ref has no VECTOR line` (and one each for K3, K4, K5), exit 1 — observed
2026-11-03 on a scratch copy. The probe's own self-test
(`python3 plans/round66_c1_tensor_probe.py --selftest --work <scratch>`) prints
`SELFTEST {'good_accepted': True, 'mutated_refused': True}`, exit 0 — a mutated vector
(`exists=P` → `exists=F`) is refused.

## Limits (named, not hidden)

- **The grader is the oracle; this entry does not re-implement its verdict.** Every P/F above is
  read out of the grader's own junit XML. The lane's own reading of the assertions is not
  evidence.
- **K1 is the lane's own reference build, not a Terminal-Bench 2.0 solution.** It was written by
  the lane to satisfy the grader ("no grader text copied; the grader's own assertions decide" —
  `plans/round-66-claims.md`). This entry prices a *replay*, not task solvability by any model,
  and says nothing about whether an agent can write this file.
- **The receipt check binds case and junit bytes, but a fully hand-written receipt with copied
  bytes is not refused by it.** Observed 2026-11-03: a receipt written by hand in scratch that
  copies the committed `case_sha`/`junit_sha` values and the committed probe sha, and states the
  frozen vectors verbatim, passes `--check-receipt` with `CHECK ok cases=5` and exit 0. The gate
  refuses *value-free* and *value-mismatched* fabrication, not a fully value-copied receipt.
  (The round-65 sqlite gate, which this round's R66-C2 adds a `--strict` mode to, is a different
  gate and is not covered by this entry.)
- **The torch install channel is the official PyTorch CPU index, version `2.15.0+cpu`**
  (`uv pip install --index-url https://download.pytorch.org/whl/cpu torch==2.15.0` into
  `~/.local/share/kengaku-r66/venv-torch`; host observation
  `~/.local/share/kengaku-r66/venv-torch/bin/python -c "import torch; print(torch.__version__)"`
  → `2.15.0+cpu`, and `torch.distributed.is_gloo_available()` → `True`). No PyPI torch was used.
  Host versions observed 2026-11-03: python 3.14.8 (`/usr/bin/python3`), pytest 9.2.0 (in the
  venv), bubblewrap 0.13.1 (`bwrap --version`), uv 0.13.0 (`~/.local/bin/uv --version`).
- **Port `12355` is shared.** The grader's `MASTER_PORT` is a fixed constant in the pinned file;
  two concurrent probes on this host collide, and the probe's guard is a refusal
  (`SETUP port 12355 busy before <case>`, exit 2), never a verdict.
- **Coverage stays L0-capped at 7.** Executing this grader does not answer the open L0 question
  `kengaku | round-25/33/51` (coverage L0 cap); nothing here is assumed to have answered it.
