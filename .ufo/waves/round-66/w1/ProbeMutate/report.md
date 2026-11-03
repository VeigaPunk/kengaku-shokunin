# ProbeMutate — kengaku round-66 wave 1 (v1), seat findings

Date: 2026-11-03. Scope: mutate-run-revert probe on the R66-C1 counter
`plans/round66_c1_tensor_probe.py` (frozen sha256 `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`),
run only against a self-contained scratch mirror. The lane was never written; no rule, predicate,
case, junit byte, or frozen table entry in the lane was edited. Scratch
`/fast/scratch/hyaku/kengaku-r66/ProbeMutate/` (deleted before yield; the log receipts below were
copied to `W/ProbeMutate/logs/` first). Tooling: nothing installed or upgraded. Network: none.
Listener on 127.0.0.1:12355: started for M6 only, killed immediately after; verified closed.

Detector (one command shape for every mutant):

```
S=/fast/scratch/hyaku/kengaku-r66/ProbeMutate
/usr/bin/python3 "$S/tree/plans/round66_c1_tensor_probe.py" --check-receipt <receipt>; echo rc=$?
```

Exit 0 = predicate pass, 1 = predicate failed, 2 = could-not-evaluate. Kill = nonzero exit or a
named `CHECK defect:` finding.

## Mirror

Built with `cp -a` from `L = /home/vgpnk/Projects/shokunin/kengaku-shokunin` into `$S/tree` with the
same relative layout, so the probe's `LANE = Path(__file__).resolve().parents[1]` resolves inside
the mirror:

- `plans/round66_c1_tensor_probe.py` — sha256 `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`
- `corpus/evidence/round66/tensor/**` — cases, junit, prefreeze-run1/2.txt, receipt.txt
- `corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py` — sha256 `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`

Fixture receipts are copies placed beside a copy of the committed junit directory (the check derives
junit from `receipt.parent/"junit"`).

## Baselines (pristine mirror, before any mutation)

| # | fixture | exit | observed |
|---|---|---|---|
| B1 | `corpus/evidence/round66/tensor/receipt.txt` (receipt of record) | 0 | `CHECK ok cases=5`, `PREDICATE R66-C1 pass` |
| B2 | `corpus/evidence/round66/tensor/prefreeze-run2.txt` (its receipt-local junit dir) | 1 | 5× `CHECK defect: <case> junit_sha does not match committed junit bytes`, `PREDICATE R66-C1 fail` |
| B3 | `--selftest --work $S/selftest-work` | 0 | `SELFTEST {'good_accepted': True, 'mutated_refused': True}` |

B2 is a **baseline failure**: the frozen control receipt cannot be re-verified from the committed
junit bytes (finding F-A). Under the seat rule, any mutant whose baseline is red is inconclusive,
not killed. B1 is the clean baseline used for M2/M3/M4 and for the M1 control variant.

## Mutants

### M1 — one VECTOR value in a copy of `prefreeze-run2.txt`
Edit: on the `VECTOR k1-ref` line only, `column-ws2-biasTrue=P` → `column-ws2-biasTrue=F`
(one token; receipt sha `c66db859…` → `dfd5e639…`).

Command: `--check-receipt $S/fixtures/m1/receipt.txt` → **rc 1**
First finding: `CHECK defect: k1-ref vector differs from the frozen table`
(also the 5 pre-existing junit defects from B2).

Verdict: **INCONCLUSIVE as assigned** — the same bytes minus the mutation already fail (B2, rc 1,
same 5 junit defects); the vector defect is new but the detector was already red.
Not a survivor: the vector channel demonstrably fires (M1-control below, M5b, M5c).

### M1-control — the same edit on a clean baseline (receipt of record)
Edit: same token change on a copy of `receipt.txt` (sha `8b164d5b…` → `37475843…`).
Command: `--check-receipt $S/fixtures/m1b/receipt.txt` → **rc 1**
Only finding: `CHECK defect: k1-ref vector differs from the frozen table`
Verdict: **KILLED** (single named defect, clean baseline).

### M2 — one byte in the mirror's k4 case file
Edit: `corpus/…/cases/k4-col-nogather/parallel_linear.py`, docstring `Mutant K4` → `Mutant K5`
(exactly one byte; `37a3c21b…` → `3e806538…`).
Command: `--check-receipt $S/fixtures/m2/receipt.txt` → **rc 1**
Finding: `CHECK defect: k4-col-nogather case_sha does not match committed bytes`
Verdict: **KILLED**. Restored: `37a3c21b324c262a5a777389cd242b8b3129b33cc4d1adb31d715cd806082b83`.

### M3 — one byte in the receipt-local k5 junit
Edit: `fixtures/m3/junit/k5-row-noreduce.xml`, `hostname="plazir27"` → `plazir28` (exactly one
byte; `d1141289…` → `ff875312…`).
Command: `--check-receipt $S/fixtures/m3/receipt.txt` → **rc 1**
Finding: `CHECK defect: k5-row-noreduce junit_sha does not match committed junit bytes`
Verdict: **KILLED**. Restored: `d1141289b23710842971f8bf92db1ff9db2120088dbdf8f33a3cdf482f8c7920`.

### M4 — no VECTOR for k3-stub
Edit: delete `CASE k3-stub …` and `VECTOR k3-stub …` from a copy of `receipt.txt`
(2 lines; sha `8b164d5b…` → `c19f67f5…`).
Command: `--check-receipt $S/fixtures/m4/receipt.txt` → **rc 1**
Finding: `CHECK defect: k3-stub has no VECTOR line`
Verdict: **KILLED**.

### M5 — assigned `frozen()` edit: k4 expects row-ws2 P
Edit (mirror probe only): in the `k4-col-nogather` branch of `frozen()`, append
`v["row-ws2-biasTrue"] = "P"` (mutated probe sha `001b6968…`).
Observed before the run: importing pristine and mutated probes gives identical
`FROZEN_TABLE` (`== True`) and `k4 row-ws2-biasTrue = P` was already the value — **the assigned
edit is a no-op because k4's frozen row side is already all `P`.**
Command: `--check-receipt $S/fixtures/m5/receipt.txt` (untouched copy of `prefreeze-run2.txt`,
sha `c66db859…`) → **rc 1**
First finding: `CHECK defect: probe sha does not match the committed probe`
(plus the 5 B2 junit defects; **no vector defect**, as expected from an unchanged table).
Verdict: **INCONCLUSIVE-BY-CONSTRUCTION** — the only kill is the probe-sha binding, not the frozen
table comparison. The assignment's expected "MISMATCH/vector defect" cannot arise from this edit.
Reported, not edited; behavior-bearing variants below.

### M5b — behavior-bearing k4 table mutation (column side)
Edit: k4 branch, column `v[k] = "P" if "-ws1-" in k else "F"` → `v[k] = "P"`; table diff vs pristine
is exactly `column-ws2-biasTrue/False` and `column-ws4-biasTrue/False` `F→P` (probe sha `faf6de64…`).
To keep the probe-sha binding from masking the table check, the receipt copy's `PROBE sha256=` line
was recomputed to the mutated probe's sha (documented second edit; the vector bytes are unchanged).
Command: `--check-receipt $S/fixtures/m5b/receipt.txt` → **rc 1**
Only finding: `CHECK defect: k4-col-nogather vector differs from the frozen table`
Verdict: **KILLED** (vector comparison isolated).

### M5c — behavior-bearing row-side mutation (k5)
Edit: k5 branch, row `v[k] = "P" if "-ws1-" in k else "F"` → `v[k] = "P"`; diff exactly
`row-ws2-*`/`row-ws4-*` `F→P` (probe sha `2435e05f…`); receipt `PROBE` line recomputed as in M5b.
Command: `--check-receipt $S/fixtures/m5c/receipt.txt` → **rc 1**
Only finding: `CHECK defect: k5-row-noreduce vector differs from the frozen table`
Verdict: **KILLED**. Probe restored to `c5ef1b54…`.

### M6 — port 12355 held (SETUP path), run once
Listener: `/usr/bin/python3 $S/listener.py` binding `127.0.0.1:12355`; verified connectable before
the run (`port_open=True`).
Command: `--run --work $S/run --receipt $S/run/r.txt` against the pristine mirror → **rc 2**
Output (exact bytes, `logs/m6.txt`):
```
SETUP port 12355 busy before k1-ref
PREDICATE R66-C1 could-not-evaluate
```
Observed: 0 `VECTOR` lines; `run/r.txt` not written (SETUP returns before any case).
Listener killed: rc 0, `port_open=False` after kill; probe sha unchanged `c5ef1b54…`.
Verdict: **KILLED** (could-not-evaluate path behaves as frozen: exit 2, no verdict, no receipt).

## Restoration evidence

| object | pristine | mutated | restored |
|---|---|---|---|
| mirror probe | `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3` | `001b6968…` (M5), `faf6de64…` (M5b), `2435e05f…` (M5c) | `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3` |
| k4 case file | `37a3c21b324c262a5a777389cd242b8b3129b33cc4d1adb31d715cd806082b83` | `3e80653852f1513ffd07eebd958547fa92d494a1400a9a9c1e052a5eabd759d5` | `37a3c21b324c262a5a777389cd242b8b3129b33cc4d1adb31d715cd806082b83` |
| k5 junit (receipt-local copy) | `d1141289b23710842971f8bf92db1ff9db2120088dbdf8f33a3cdf482f8c7920` | `ff875312fd602b8bac18bf54c45a3355b526a803165a0ea632f3b1de0f04b4f7` | `d1141289b23710842971f8bf92db1ff9db2120088dbdf8f33a3cdf482f8c7920` |

Post-restore detector over the mirror: `receipt.txt` → rc 0, `CHECK ok cases=5`,
`PREDICATE R66-C1 pass`; `prefreeze-run2.txt` → rc 1, 5 junit defects (unchanged baseline).
Every mirror input sha equals the lane sha (probe, grader, 4 case files, 5 junit files — all
compared with `sha256sum`, all equal). Mutated fixture receipt shas: m1 `dfd5e639…`, m1b `37475843…`,
m4 `c19f67f5…`, m5b `31ee2542…`, m5c `e16d0641…` (baseline copies: `receipt.txt` `8b164d5b…`,
`prefreeze-run2.txt` `c66db859…`).

## SURVIVORS

**None.** Every behavior-bearing mutant was killed by a named finding or a nonzero exit. M5 as
literally specified is a no-op (not a survivor: it cannot be a killed/survived mutant at all); M1 as
assigned is inconclusive because its byte-set baseline is already red.

## Findings

### F-A — baseline defect: the frozen pre-freeze control receipt is no longer checkable
`--check-receipt corpus/evidence/round66/tensor/prefreeze-run2.txt` exits 1 with five
`junit_sha does not match committed junit bytes` defects. The committed junit files
(`k1-ref 7e7ccace…`, `k2-none f2987493…`, `k3-stub ef592bad…`, `k4 87797c92…`, `k5 d1141289…`)
equal **receipt.txt's** `CASE … junit_sha=` values, not run2's (`9c02c973…`, `f1f42b55…`,
`8e5c4d5c…`, `28267e68…`, `8f7fa27b…`). Mtimes: run1 17:56, run2 18:02, receipt.txt 18:04;
junit k1 18:03, k2–k5 18:04.

Cause: `check_receipt()` and `cmd_run()` both place junit at `receipt.parent / "junit"`. Every
receipt written into `corpus/evidence/round66/tensor/` shares one junit directory, so the
receipt-of-record run (18:04) overwrote the bytes run2 (18:02) had written. The pre-freeze note
"the junit directory is receipt-local, so a re-run cannot overwrite committed junit bytes" holds
only across directories, not across two receipts in one directory.

Effect: the claim's predicate names `receipt.txt`, which passes (B1); the frozen table, the five
cases, the probe sha and the vectors are unaffected. What is lost is independent re-verification of
the artifact the claims file calls the "control of record" (`prefreeze-run2.txt` with junit dir
`corpus/evidence/round66/tensor/junit/`). The kill rules do not cover this shape: the junit is
present but carries the wrong bytes (a named defect), not missing (could-not-evaluate). Reported,
not fixed; a receipt-scoped junit directory (e.g. `receipt.parent / (receipt.stem + ".junit")`) or
one receipt per directory would restore re-checkability.

### F-B — assignment defect (M5): the specified mutation is not behavior-bearing
In `frozen()`, `k4-col-nogather` already sets all `row-*` keys to `P`, so "change frozen() so that
k4 expects row-ws2 P" produces an identical table (verified by import: `FROZEN_TABLE == True`), and
the expected vector finding cannot occur. The row-side expectation that is actually `F` is k5's
`row-ws2`/`row-ws4` (M5c) and k4's `F` side is `column-ws2/ws4` (M5b); both kill. No rule edited.

## Calibration notes

- `check_receipt()` does not re-derive the receipt's `frozen=match` token; it requires the token to
  read `match` and separately recomputes each vector against `FROZEN_TABLE`. M1/M5b/M5c show the
  recomputation is the effective check; a receipt that says `match` with a wrong vector still fails.
- The probe-sha binding is evaluated before the vector scan, so any probe edit is refused on the
  sha channel first. M5b/M5c recomputed the `PROBE` line in a receipt copy solely to isolate the
  table channel; that is a fixture accommodation, not a counter behavior.
- M6 confirms the port check runs inside the flock before the first case, so a busy port yields
  exit 2 with no VECTOR and no receipt — the "never a verdict" rule holds.
- The counter's finding vocabulary is `vector differs from the frozen table`; it never prints
  `MISMATCH` from `check_receipt` (that token is only written by the run path). Expected wording in
  the seat spec differs from observed wording; the check is correct.

## Log receipts (copied to `W/ProbeMutate/logs/`)

| file | bytes | sha256 |
|---|---|---|
| m1.txt | 440 | `662235fa0b52127afa510f6a8924c507f74632782c531966f55cf70fbd63e756` |
| m1-baseline.txt | 382 | `58b8d3eb2217073bfd43a1325dc64407f5944582fdfeb4790190900e50548463` |
| m1b.txt | 80 | `2485d9031e4729b9ccec15286259114078fc998382d47c29d2e379e7704d4635` |
| m2.txt | 92 | `ef144cdad5eeeb72bd0f83279bf508e4ff536f6ba3fee6d11bf8f345b9c51a0d` |
| m3.txt | 99 | `7e29cbaba6cf786b87d35085aa84aeb107ab71e77f002a5551b322e4869542ca` |
| m4.txt | 63 | `ef0511646a30f391b4e795c5ae30f3eea930229e8c601610d3e915f99186675a` |
| m5.txt | 441 | `458183af3ab2410bffeb5b03cd81f53f703ced1948ab6980bc09bdbaf58c3ee4` |
| m5b.txt | 89 | `c6bc257d7d2579c0c1d2c883143a75013403a9cfc76e386887755ecadf503104` |
| m5c.txt | 89 | `804568b9b78af9ae221898a4e1d05463ab49c9c308dc4f6babaaee6981981e0d` |
| m6.txt | 72 | `39206eb20db9e9c17ad9649c2abf0570b030ef081c093100c1fce317b6aefd3e` |
| baseline-receipt.txt | 39 | `79412db07612c2acad4dc8b26108331378999aa10bdc2bcef5005c8d02ddc9ec` |
| baseline-run2.txt | 382 | `58b8d3eb2217073bfd43a1325dc64407f5944582fdfeb4790190900e50548463` |
| baseline-selftest.txt | 58 | `9882e61cb3cbc1514782247bd96658e8b641c3bc425480396ca54488f8e5aa56` |
