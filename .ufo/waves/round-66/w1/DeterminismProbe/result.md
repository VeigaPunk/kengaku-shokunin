# DeterminismProbe — R66-C1 probe determinism check (round 66, wave 1)

Scope: one extra run of the frozen probe in a scratch mirror; the lane receipt of record was not
touched. Seat: `DeterminismProbe`. All paths absolute; `L` = `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
`S` = `/fast/scratch/hyaku/kengaku-r66/DeterminismProbe` (removed on exit).

## Mirror built (step 1)

`S/tree` has the lane layout: `plans/round66_c1_tensor_probe.py`, `corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py`,
`corpus/evidence/round66/tensor/{cases,junit}`. Verified with `sha256sum`:

| file | mirror sha256 | equals lane |
|---|---|---|
| plans/round66_c1_tensor_probe.py | `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3` | yes |
| graders/.../tests/test_outputs.py | `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290` | yes |
| cases/k1-ref/parallel_linear.py | `1537da2a2ea07293ec757641a0d2faee5e507518da9f96de45bebfd788193fc1` | yes |
| cases/k3-stub/parallel_linear.py | `316630cd45f0a3e2332bd38f98f4147977eba3d84aa54c5203edc5923986eadf` | yes |
| cases/k4-col-nogather/parallel_linear.py | `37a3c21b324c262a5a777389cd242b8b3129b33cc4d1adb31d715cd806082b83` | yes |
| cases/k5-row-noreduce/parallel_linear.py | `edf7cab1ee5798e135affe6ea9f884696cea4165d6f11d0e49bd3e458c291881` | yes |

`k2-none` is created by the probe itself under `--work` (empty `/app`), as in the lane run.

## Commands and exit codes (step 2)

Port 12355 free before start (`ss -ltnp | grep :12355` → no listener; no probe process in `ps`).

```
cd $S
TMPDIR=$S python3 $S/tree/plans/round66_c1_tensor_probe.py --run --work $S/run \
  --receipt $S/tree/corpus/evidence/round66/tensor/receipt.txt
```
→ **EXIT=0**, wall 62.76 s, stdout ends `PREDICATE R66-C1 pass`.
Receipt written: 9204 bytes, sha256 `dd70201f8a56ea3274bf63404c7afc3f80fe977ad37ee9f4d269d7b077bdedfd`
(copied to `mirror-receipt.txt`). Its `PROBE sha256=c5ef1b54…` and `GRADER sha256=4ae4285e…` lines match
the frozen probe and grader.

```
python3 $S/tree/plans/round66_c1_tensor_probe.py --check-receipt $S/tree/corpus/evidence/round66/tensor/receipt.txt
```
→ **EXIT=0**, `CHECK ok cases=5`, `PREDICATE R66-C1 pass` (mirror receipt is self-consistent against its
receipt-local junit).

Lane receipt untouched: observed after the mirror run as sha256
`8b164d5bddfc69e51413faebf60f05a9b4ee84ceac31798ce611013b946f2be2`, mtime 2026-11-03 18:04:49; the mtime
predates this seat's run (~18:11–18:12), so the seat wrote nothing there (a write would move the mtime).

## VECTOR comparison (step 3) — diff exit code 0

```
diff -u $S/cmp/prefreeze.vector $S/cmp/mirror.vector   → EXIT=0  (no differences)
diff -u $S/cmp/run1.vector      $S/cmp/prefreeze.vector → EXIT=0  (no differences)
```
Five `VECTOR` lines, 13 keys each, byte-identical to `prefreeze-run2.txt` and to `prefreeze-run1.txt`:

- k1-ref: `exists=P` and all 12 layer keys `P`
- k2-none: `exists=F` and all 12 layer keys `F`
- k3-stub: `exists=P`, all 12 layer keys `F`
- k4-col-nogather: `exists=P`, column ws1 `P`, column ws2/ws4 `F`, row all `P`
- k5-row-noreduce: `exists=P`, column all `P`, row ws1 `P`, row ws2/ws4 `F`

**No outcome differs between the mirror run and the frozen control. No flake finding.**

## FRAGMENT comparison by test key (step 3, text level)

33 fragment keys in both receipts; none missing, none extra. 17 messages are byte-identical;
16 differ by **exactly one character** — the spawn rank digit at offset 65 of
`torch.multiprocessing.spawn.ProcessRaisedException:   -- Process N terminated with the following error: …`
(messages are truncated to 160 chars). Every one of the 16 is a single `replace` opcode at offset 65
(`fragment-table.txt`). Cause: `torch.multiprocessing.spawn` surfaces the first worker that raised;
which rank reports is scheduler-dependent. The exception class and the rest of the text are unchanged.
Differing keys (run2 rank → mirror rank):

| case | key | run2 | mirror |
|---|---|---|---|
| k2-none | column-ws2-biasTrue | 1 | 0 |
| k2-none | column-ws4-biasFalse | 0 | 1 |
| k2-none | column-ws4-biasTrue | 2 | 1 |
| k2-none | row-ws2-biasTrue | 1 | 0 |
| k2-none | row-ws4-biasFalse | 3 | 2 |
| k2-none | row-ws4-biasTrue | 3 | 2 |
| k3-stub | column-ws4-biasTrue | 2 | 1 |
| k3-stub | row-ws2-biasFalse | 0 | 1 |
| k3-stub | row-ws2-biasTrue | 0 | 1 |
| k3-stub | row-ws4-biasTrue | 2 | 1 |
| k4-col-nogather | column-ws2-biasTrue | 1 | 0 |
| k4-col-nogather | column-ws4-biasFalse | 3 | 2 |
| k4-col-nogather | column-ws4-biasTrue | 2 | 0 |
| k5-row-noreduce | row-ws2-biasFalse | 1 | 0 |
| k5-row-noreduce | row-ws2-biasTrue | 1 | 0 |
| k5-row-noreduce | row-ws4-biasFalse | 3 | 0 |

## CASE lines: case_sha stable, junit_sha run-local

- `case_sha`: identical for all five (k2-none `none`), matching the frozen control.
- `junit_sha`: differs for all five between control, mirror and working tree (`junit-sha-table.txt`).
  Measured cause: pytest junit `timestamp=` and per-test `time=` attributes; failing cases additionally
  embed the spawn rank and `ProcessContext object at 0x…` heap addresses (ASLR). Normalising
  `timestamp`/`time`/`Process N` makes k1-ref XML byte-identical; k4-col-nogather keeps 7 residual
  regions, all `ProcessContext object at 0x…` addresses.

## Findings

- **D1 — no flake.** VECTOR lines are byte-identical across three runs (run1, run2, mirror); predicate
  outcome stable (`pass`). The frozen table is reproducible on this host.
- **D2 — `junit_sha` is a run-local binding, not a cross-run invariant.** `prefreeze-run2.txt` fails
  `--check-receipt` against the current working-tree junit (exit 1, five `CHECK defect: <case> junit_sha
  does not match committed junit bytes`) because a later run wrote its receipt into the evidence dir and
  replaced `corpus/evidence/round66/tensor/junit/`; HEAD `2c1ef88a` records exactly that ("junit replaced,
  pre-freeze junit retained at 9a07df6a"). The pre-freeze bytes are intact at `9a07df6a` and match the
  control's `junit_sha` values exactly for all five cases (`junit-sha-table.txt`). Consequence for the
  predicate wording "every `case_sha` and `junit_sha` equals the committed bytes": that clause holds only
  for the same run's bytes (receipt-local junit); it is not reproducible by a second run. Reported, not
  edited.
- **D3 — FRAGMENT text is not deterministic; only the key set is.** Any future check that binds FRAGMENT
  text (or `junit_sha`) across runs will flake; bind the key set and the VECTOR table instead.

## Verdict

`PREDICATE R66-C1 pass` reproduces: 5/5 case vectors equal the frozen table, 13/13 K1 tests pass,
case shas equal committed bytes, mirror receipt self-consistent. No outcome differs from
`prefreeze-run2.txt`. Confidence: high (byte-level diffs, three independent runs).
