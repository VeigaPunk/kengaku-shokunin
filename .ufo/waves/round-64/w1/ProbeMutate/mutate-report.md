# Mutation report — R64-C1 probe and R64-C3 sweep (round 64, w1, seat ProbeMutate)

Seat: ProbeMutate (`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/ProbeMutate/`).
Scope: mutation-test the two round-64 instruments only. No lane file was written; no claim text
was edited; both originals were read-only and are byte-identical before and after (see
`receipts/restoration.txt`).

## Targets (bytes actually tested)

| target | path | sha256 at battery time |
|---|---|---|
| R64-C1 probe | `.ufo/waves/round-64/w1/ProbeBuild/round64_c1_kvstore_probe.py` | `9f56d25ddb33e14474c6439c16f25dd5545da99e542a051d342113a88b306843` |
| R64-C3 sweep | `.ufo/waves/round-64/w1/SweepBuild/round64_trio_sweep.py` | `56638ea1dfc0ca47ee91dfc0afec9c9fcbbefa9b15d3e163ad423b7f8dbf8bb0` |
| sweep dependency | `plans/round63_gate_checks.py` | `797085c242a63d0b38f875b6f67550848ddac34dd7f5dbd20861ad3849e7a18a` |

The probe source changed twice while this seat waited (sha `cea43c34…` → `6a3a0863…` → `9f56d25d…`);
the battery was re-run on the final bytes, and `restoration.txt` re-hashes all three inputs after the
battery to prove the tested bytes are the current bytes. Preserved copies are under `pristine/`.

## Method

For each mutation: exact-string edit of a **copy** in scratch (match-count asserted, bytes-changed
asserted, mutant compiled); then the same bounded detector on **pristine**, **mutant** and
**restored** bytes. Detection is text-only (`--check-receipt`, `--selftest`, `--sweep`); no live
gRPC battery, no port bind, no network. Fixtures and mutants are preserved under `fixtures/` and
`mutants/` so every receipt's bytes survive scratch removal. Each `receipts/mN.txt` carries the
command, cwd, exit code, stdout and stderr of every run plus the mutation diff.

Verdict rule: `KILLED` when a detector exits non-zero on the mutated tool; `SURVIVED` when the
mutated tool accepts the corruption its removed check guarded. A pristine baseline failure would
be `INCONCLUSIVE`; none occurred (all baselines matched their expected exits).

## Verdicts

| id | target | mutation (smallest behaviour-bearing edit) | detector (corrupt input) | pristine | mutant | verdict | mechanism |
|---|---|---|---|---|---|---|---|
| m1 | probe | `FROZEN_VECTORS["K3"]` leg 6 `F`→`P` | `--check-receipt` on the receipt of record | `0` | `1` | **KILLED** | external contract anchor |
| m2 | probe | delete both K2 leg-5 fragment guards from `receipt_failures` | `--check-receipt` on K2-FRAGMENT + leg-5 frag replaced | `1` | `0` | **KILLED** | only `--selftest` (leg `no-k2-fragment` 0≠1); `--check-receipt` survived |
| m3 | probe | delete the `PORTFREE before-battery True` guard | `--check-receipt` on `PORTFREE before-battery False` | `1` | `0` | **KILLED** | only `--selftest` (leg `port-not-free` 0≠1); `--check-receipt` survived |
| m4 | probe | accept a missing CASE line (`case-line-missing` guard removed) | `--check-receipt` on receipt with `CASE K4` deleted | `1` | `0` | **SURVIVED** | none (`--selftest` also green) |
| m5 | sweep | accept `## Freshness addendum (round 63)` as an addendum heading | `--sweep` on a round-63-only addendum lane | `1` | `0` | **SURVIVED** | none |
| m6 | sweep | drop the SETUP frozen-list cross-check (mismatch + absent-entry) | `--sweep` on a lane holding none of the frozen entries | `2` | `0` | **SURVIVED** | none |

Observed lines (verbatim from the receipts):

- m1 mutant on the receipt of record: `CHECK fail K3 vector P/P/P/P/P/F/F != P/P/P/P/P/P/F`,
  `CHECK fail K3 leg-verdicts PPPPPFF != PPPPPPF`, `PREDICATE R64-C1 fail` (rc 1).
  Anchor: ProbeBuild `kvstore-probe.txt` sha256 `a87cd119…`, pristine rc 0.
- m2 mutant on the corrupt receipt: `CHECK ok cases=5` / `PREDICATE R64-C1 pass` (rc 0);
  mutant `--selftest`: `SELFTEST no-k2-fragment observed=0 expected=1 FAIL`, `SELFTEST fail` (rc 1).
- m3 mutant on the corrupt receipt: `CHECK ok cases=5` / `PREDICATE R64-C1 pass` (rc 0);
  mutant `--selftest`: `SELFTEST port-not-free observed=0 expected=1 FAIL`, `SELFTEST fail` (rc 1).
- m4 pristine on the K4-missing receipt: `CHECK fail K4 case-line-missing` (rc 1);
  mutant: `CHECK ok cases=5` / `PREDICATE R64-C1 pass` (rc 0); both selftests rc 0.
- m5 pristine: `SWEEP files=1 trio_open=0 addendum=0 red=1` + `RED corpus/knowledge/wrong-date.md`
  + `PREDICATE R64-C3 fail` (rc 1); mutant: `SWEEP files=1 trio_open=0 addendum=1 red=0`
  + `ADDENDUM corpus/knowledge/wrong-date.md` + `PREDICATE R64-C3 pass` (rc 0). Round-64 control
  lane passes under both (rc 0), so the mutation is date-specific.
- m6 pristine on the vacuous lane: `SETUP frozen-entry-missing` (rc 2); mutant:
  `SWEEP files=1 trio_open=1 addendum=0 red=0` + `PREDICATE R64-C3 pass` (rc 0), while still
  printing `INFO frozen-list=… entries=3` — it reports the list and never compares it.
  Mismatch lane: pristine `SETUP frozen-list-mismatch` (rc 2), mutant graded it (rc 1).

## Surviving-mutation findings (coverage, not defects of the authored tools)

1. **m4 — the per-case `CASE` line has no redundant guard.** Deleting one line makes
   `--check-receipt` print `CHECK ok cases=5` and `PREDICATE R64-C1 pass` for a receipt with only
   four CASE lines. `VECTOR`, `LEG` and `PORTFREE` lines are checked independently and cannot
   notice the omission; the selftest fixture set has no missing-CASE case. Consequence for R64-C1:
   the CASE-line clause is load-bearing and single-point — a future regression there is silent, and
   the receipt's own `cases=5` line is computed from the count of `CASES`, not from parsed lines.
2. **m2/m3 — the two clauses the frozen predicate names explicitly are single-point inside
   `--check-receipt`.** With the K2-fragment block (both adjacent sites) or the
   `PORTFREE before-battery` guard removed, the claim's own counting command accepts a receipt that
   violates the frozen predicate; only `--selftest`, which the claim does not cite, still fails.
   The fix is evidential, not a contract change: cite `--selftest` next to `--check-receipt`, or add
   a `--check-receipt` cross-check that re-reads the same evidence twice.
3. **m1 — the in-tool selftest cannot see a changed frozen constant.** All seven selftest legs stay
   green after flipping a frozen cell (`render-table` compares the mutated table to the mutated
   constant; `tampered-vector` flips a different cell). The only anchor is `--check-receipt` against
   an independently produced receipt. This sharpens the declared limitation ("text fields only,
   cannot prove a live run"): constant drift is also invisible without an external receipt, so the
   receipt of record must stay the input of the counting command.
4. **m5 — the round-date token is single-point.** Accepting `## Freshness addendum (round 63)`
   turns a wrong-date entry from `TRIO-RED` (rc 1) into `TRIO-ADDENDUM` (rc 0) and the sweep prints
   `PREDICATE R64-C3 pass`; the round-64 control lane is unchanged. The selftest's ADDENDUM fixture
   only exercises round 64, and the SETUP cross-check does not help when the frozen list names that
   entry (it matched). A copy-pasted addendum block from round 63 — with `verified-at: 2026-11-03`
   and a live `recheck:` line — would be accepted as fresh.
5. **m6 — the frozen-list cross-check is the sole enforcement of R64-C3(b) and is removable
   invisibly.** Its removal leaves both `--sweep` (a lane containing none of the frozen entries
   prints `PREDICATE R64-C3 pass`, rc 0) and `--selftest` (both legs green) clean. The frozen list's
   sha is printed on stderr (`INFO frozen-list=… sha256=…`) but nothing asserts it equals the
   committed `trio-red-at-base.txt`, so the cross-check has no independent pin of its own input.

Report-only: findings 1–5 are evidence for the L1's closure. I changed no claim, no tool and no
lane file; the mutants exist only under `mutants/`.

## Restoration and integrity

`receipts/restoration.txt`:

- probe original sha now `9f56d25d…` = battery sha `9f56d25d…` = preserved copy `9f56d25d…`
  (`byte_identical_to_battery_source=True`), and the same triple equality holds for the sweep
  (`56638ea1…`) and the gate (`797085c2…`).
- Restored-bytes detector re-run from the preserved copies on the preserved fixtures:
  `probe --check-receipt` rc 0; `probe --selftest` rc 0; `sweep --sweep lane-m5` rc 1 (RED, the
  pristine baseline); `sweep --selftest` rc 0. `RESTORATION pass`.
- `manifest.sha256` lists every preserved file (44 lines). Scratch
  `/fast/scratch/hyaku/kengaku-r64/ProbeMutate` was removed after the copy; receipts keep the
  historical scratch paths in their `cmd=` fields, and the same bytes are preserved here.

## Artifacts

- `receipts/m1.txt` … `receipts/m6.txt` — one file per mutation (command, cwd, rc, stdout, stderr,
  diff, verdict), plus `mN-diff.txt`.
- `receipts/restoration.txt`, `manifest.sha256`
- `fixtures/probe/*` (receipt of record anchor + four corrupted receipts),
  `fixtures/sweep/{lane-m5,lane-m5-control,lane-m6-vacuous,lane-m6-mismatch}/`
- `mutants/m1..m6/` (mutated tools; m5/m6 carry `round63_gate_checks.py` for the import)
- `pristine/` (the exact tested bytes), `logs/probe-run.log`, `logs/sweep-run.log`
- `mutate_probe.py`, `mutate_sweep.py`, `restore_check.py`, `driver.py` — rerunnable harnesses
  (paths inside point at scratch; the preserved copies are the evidence of record)
