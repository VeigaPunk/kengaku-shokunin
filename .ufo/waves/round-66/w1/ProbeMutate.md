# ProbeMutate — kengaku round-66 wave 1 (v1), seat findings

Date: 2026-11-03. Scope: mutate-run-revert probe on the R66-C1 counter
`plans/round66_c1_tensor_probe.py` (frozen sha256 `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`),
executed only against a self-contained mirror under
`S=/fast/scratch/hyaku/kengaku-r66/ProbeMutate/` (deleted before yield; logs copied to
`W/ProbeMutate/logs/`). The lane was never written; no frozen case, junit byte, table entry,
predicate or rule was edited. Tooling: nothing installed or upgraded. Network: none. The only
listener was the M6 port holder on 127.0.0.1:12355, killed and verified closed.

Detailed method, hashes and log index: `W/ProbeMutate/report.md`.

## Mirror

`cp -a` from `L=/home/vgpnk/Projects/shokunin/kengaku-shokunin` into `$S/tree`:
`plans/round66_c1_tensor_probe.py` (sha `c5ef1b54…`), `corpus/evidence/round66/tensor/**`,
`corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py` (sha `4ae4285e…`).
The probe derives `LANE` from `Path(__file__).resolve().parents[1]`, so all checks ran against the
mirror. Detector: `/usr/bin/python3 $S/tree/plans/round66_c1_tensor_probe.py --check-receipt <r>`;
exit 0 pass / 1 failed / 2 could-not-evaluate.

## Baselines (pristine)

| fixture | exit | observed |
|---|---|---|
| `corpus/evidence/round66/tensor/receipt.txt` (receipt of record) | 0 | `CHECK ok cases=5`; `PREDICATE R66-C1 pass` |
| `corpus/evidence/round66/tensor/prefreeze-run2.txt` (its receipt-local junit dir) | 1 | 5× `CHECK defect: <case> junit_sha does not match committed junit bytes`; `PREDICATE R66-C1 fail` |
| `--selftest --work $S/selftest-work` | 0 | `SELFTEST {'good_accepted': True, 'mutated_refused': True}` |

The second row is a **baseline failure** (finding F-A): the frozen pre-freeze control receipt is not
re-checkable from the committed junit bytes, so a mutant run on those bytes is inconclusive by the
seat rule.

## Mutants (all commands `--check-receipt <fixture>` unless noted)

| # | mutation | exit | first finding | verdict |
|---|---|---|---|---|
| M1 | `prefreeze-run2.txt` copy: `k1-ref column-ws2-biasTrue P→F` | 1 | `CHECK defect: k1-ref vector differs from the frozen table` (+5 junit defects from the red baseline) | **inconclusive as assigned** (baseline already red) |
| M1-control | same edit on a copy of `receipt.txt` (clean baseline) | 1 | `CHECK defect: k1-ref vector differs from the frozen table` (only) | **KILLED** |
| M2 | one byte in mirror k4 case (`Mutant K4`→`Mutant K5`) | 1 | `CHECK defect: k4-col-nogather case_sha does not match committed bytes` | **KILLED** (restored `37a3c21b…`) |
| M3 | one byte in receipt-local k5 junit (`plazir27`→`plazir28`) | 1 | `CHECK defect: k5-row-noreduce junit_sha does not match committed junit bytes` | **KILLED** (restored `d1141289…`) |
| M4 | delete `CASE`+`VECTOR` lines of k3-stub | 1 | `CHECK defect: k3-stub has no VECTOR line` | **KILLED** |
| M5 | mirror `frozen()`: k4 explicitly expects `row-ws2 P` (already P ⇒ no-op; table identical on import) | 1 | `CHECK defect: probe sha does not match the committed probe` (+5 junit; no vector defect) | **inconclusive-by-construction** (non-behavior-bearing edit) |
| M5b | mirror `frozen()`: k4 column `F→P` (table diff = 4 column-ws2/ws4 keys); receipt `PROBE` line recomputed so sha cannot mask it | 1 | `CHECK defect: k4-col-nogather vector differs from the frozen table` (only) | **KILLED** |
| M5c | mirror `frozen()`: k5 row `F→P` (diff = 4 row-ws2/ws4 keys); receipt `PROBE` line recomputed | 1 | `CHECK defect: k5-row-noreduce vector differs from the frozen table` (only) | **KILLED** |
| M6 | hold 127.0.0.1:12355 (`$S/listener.py`), then `--run --work $S/run --receipt $S/run/r.txt` | 2 | `SETUP port 12355 busy before k1-ref`; `PREDICATE R66-C1 could-not-evaluate`; 0 VECTOR lines; no receipt written | **KILLED** (could-not-evaluate path) |

Restoration: probe `c5ef1b54…` (mutated `001b6968…`/`faf6de64…`/`2435e05f…`), k4 case
`37a3c21b…` (mutated `3e806538…`), k5 junit `d1141289…` (mutated `ff875312…`) — all restored to the
exact frozen bytes; post-restore `receipt.txt` check rc 0 and every mirror input sha equals the lane
sha. Listener killed (rc 0, port closed).

## SURVIVORS

**None.** M5-literal is a no-op (cannot be a killed/survived behavior-bearing mutant); M1-as-assigned
is inconclusive because its byte-set baseline is already red. The vector channel is proven live by
M1-control, M5b and M5c, each with exactly one named defect.

## Findings

- **F-A (baseline/fixture drift, report only).** `--check-receipt prefreeze-run2.txt` exits 1 with
  five `junit_sha` defects. The committed junit files equal `receipt.txt`'s `CASE … junit_sha=`
  values (`7e7ccace, f2987493, ef592bad, 87797c92, d1141289`), not run2's (`9c02c973, f1f42b55,
  8e5c4d5c, 28267e68, 8f7fa27b`); mtimes are run2 18:02, junit k1 18:03, k2–k5 and receipt.txt
  18:04. Cause: `check_receipt()`/`cmd_run()` place junit at `receipt.parent/"junit"`, so every
  receipt in `corpus/evidence/round66/tensor/` shares one junit dir and the receipt-of-record run
  overwrote run2's bytes. The claim's predicate names `receipt.txt` (which passes), and the frozen
  table/cases/probe are unaffected; what is lost is re-verification of the artifact the claims file
  calls the "control of record". Not a missing-junit could-not-evaluate (kill rule c) but a wrong-
  bytes named defect; reported, not fixed. A receipt-scoped junit dir (e.g. `receipt.stem + ".junit"`)
  or one receipt per directory would restore re-checkability.
- **F-B (assignment defect, report only).** M5 as written cannot kill: `k4-col-nogather` already
  expects `row-ws2 = P` in `frozen()`, so the edit leaves `FROZEN_TABLE` identical (verified by
  import) and no vector finding can occur. The actually-`F` row expectation is k5's
  `row-ws2/ws4` (M5c); k4's `F` side is `column-ws2/ws4` (M5b); both kill. No rule edited.
- Calibration: `check_receipt()` re-derives every vector against the frozen table independently of
  the receipt's `frozen=match` token; the probe-sha binding is checked first, so table mutations
  were observed only after recomputing the `PROBE` line in a receipt copy (fixture accommodation,
  documented). The counter's wording is `vector differs from the frozen table` (never `MISMATCH`
  from `--check-receipt`). M6 shows a busy port yields exit 2, no VECTOR and no receipt.

## Log receipts

`W/ProbeMutate/logs/`: `m1.txt` `662235fa…`, `m1-baseline.txt` `58b8d3eb…`, `m1b.txt` `2485d903…`,
`m2.txt` `ef144cda…`, `m3.txt` `7e29cbab…`, `m4.txt` `ef051164…`, `m5.txt` `458183af…`,
`m5b.txt` `c6bc257d…`, `m5c.txt` `804568b9…`, `m6.txt` `39206eb2…`, `baseline-receipt.txt`
`79412db0…`, `baseline-run2.txt` `58b8d3eb…`, `baseline-selftest.txt` `9882e61c…`
(full shas in `W/ProbeMutate/report.md`).
