# ProbeMutate — round 64 w1 scoped findings (mutation test of the R64-C1 probe and R64-C3 sweep)

Verdict: **6 mutations, 3 killed, 3 survived.** m1–m3 caught; m4 (probe), m5 and m6 (sweep)
survive every detector available. The three artifacts are otherwise sound: pristine baselines match
their expected exits in every run, both tools pass their own selftests, and the receipts of record
are re-derivable. Full detail with commands, exits, stdout/stderr and diffs:
`mutate-report.md` and `receipts/m1.txt … m6.txt`.

## Targets (bytes tested, byte-identical at report time)

| target | sha256 |
|---|---|
| `.ufo/waves/round-64/w1/ProbeBuild/round64_c1_kvstore_probe.py` | `9f56d25ddb33e14474c6439c16f25dd5545da99e542a051d342113a88b306843` |
| `.ufo/waves/round-64/w1/SweepBuild/round64_trio_sweep.py` | `56638ea1dfc0ca47ee91dfc0afec9c9fcbbefa9b15d3e163ad423b7f8dbf8bb0` |
| `plans/round63_gate_checks.py` (sweep import) | `797085c242a63d0b38f875b6f67550848ddac34dd7f5dbd20861ad3849e7a18a` |

Method: minimal exact-string edit of a copy in scratch; same bounded detector on pristine, mutated
and restored bytes; text-only detection (`--check-receipt`, `--selftest`, `--sweep`), no live
battery, no bind, no network. No lane file was modified; both originals hash identically before and
after (`receipts/restoration.txt`, `RESTORATION pass`).

## Verdicts

| id | mutation | corrupted input | pristine | mutant | verdict |
|---|---|---|---|---|---|
| m1 | probe: `FROZEN_VECTORS["K3"]` leg 6 `F`→`P` | receipt of record (`kvstore-probe.txt`, sha `a87cd119…`) | rc 0 | rc 1 (`CHECK fail K3 vector … != …`, `PREDICATE R64-C1 fail`) | **KILLED** |
| m2 | probe: delete both K2 leg-5 fragment guards | K2-FRAGMENT + `LEG K2 5 …frag=` replaced | rc 1 | `--check-receipt` rc 0 (`PREDICATE R64-C1 pass`); `--selftest` rc 1 (`no-k2-fragment observed=0 expected=1 FAIL`) | **KILLED** (selftest only) |
| m3 | probe: delete `PORTFREE before-battery True` guard | `PORTFREE before-battery False` | rc 1 | `--check-receipt` rc 0; `--selftest` rc 1 (`port-not-free observed=0 expected=1 FAIL`) | **KILLED** (selftest only) |
| m4 | probe: accept a missing CASE line | receipt with `CASE K4` deleted | rc 1 (`CHECK fail K4 case-line-missing`) | rc 0 (`CHECK ok cases=5`, `PREDICATE R64-C1 pass`); selftest rc 0 | **SURVIVED** |
| m5 | sweep: accept `## Freshness addendum (round 63)` | lane with a round-63-dated addendum | rc 1 (`SWEEP … red=1`, `RED …`, `PREDICATE R64-C3 fail`) | rc 0 (`SWEEP files=1 trio_open=0 addendum=1 red=0`, `PREDICATE R64-C3 pass`) | **SURVIVED** |
| m6 | sweep: drop the SETUP frozen-list cross-check | lane containing none of the frozen entries | rc 2 (`SETUP frozen-entry-missing`) | rc 0 (`SWEEP files=1 trio_open=1 red=0`, `PREDICATE R64-C3 pass`) | **SURVIVED** |

Controls: the round-64 addendum lane passes under both m5 tool and pristine (rc 0), so m5's effect
is date-specific; the m6 mismatch lane shifts from `SETUP frozen-list-mismatch` (rc 2) to a graded
`SWEEP … red=1` (rc 1), so both cross-check branches are gone; every pristine baseline reproduces
the expected exit, so no verdict is inconclusive.

## Findings for the L1 (report-only; no claim, tool or lane file edited)

1. **m4 — a missing CASE line is accepted once its guard is removed, with nothing else noticing.**
   `--check-receipt` prints `CHECK ok cases=5` (`cases=` is derived from `CASES`, not from parsed
   lines), and the selftest has no missing-CASE fixture. The CASE line is the only carrier of
   observed/expected; `VECTOR`, `LEG` and `PORTFREE` checks are independent. Load-bearing,
   single-point clause.
2. **m2/m3 — the two clauses the R64-C1 predicate names explicitly have no redundancy inside the
   counting command.** The mutant `--check-receipt` accepts receipts that violate the frozen
   predicate (fragment replaced; port recorded as not free at battery start). Only the tool's
   `--selftest`, which the claim's counting command does not cite, fails. Evidential fix: cite
   `--selftest` beside `--check-receipt` in the R64-C1 counting set.
3. **m1 — the selftest cannot detect a changed frozen constant.** All seven legs stay green after
   a cell flip because `render-table` and `tampered-vector` are self-consistent. Only
   `--check-receipt` against an externally produced receipt catches drift. This extends the named
   limitation beyond "cannot prove a live run": constant drift also needs the external receipt, so
   the counting command must keep using `corpus/evidence/round64/kvstore-probe.txt` and never a
   receipt synthesized by the same version.
4. **m5 — the round-date token is single-point.** A round-63 heading block carrying
   `verified-at: 2026-11-03` and a live `recheck:` line classifies TRIO-ADDENDUM and the sweep
   prints `PREDICATE R64-C3 pass`. The SETUP cross-check does not catch it when the frozen list
   names that entry, and the selftest's ADDENDUM fixture only exercises the round-64 heading.
5. **m6 — the SETUP cross-check is the sole enforcement of R64-C3(b) and is removable invisibly.**
   Without it the sweep passes a lane holding none of the frozen entries (`INFO frozen-list=…
   entries=3` is still printed but never compared), and both selftest legs stay green. The frozen
   list's own sha is printed on stderr but never asserted against the committed
   `trio-red-at-base.txt`.

Suggested (for the L1 to decide, not applied): add a missing-CASE fixture to the probe selftest and
a round-63-dated fixture to the sweep selftest; in the sweep, assert the frozen list's sha256
against a pinned value so the cross-check has an independent input pin.

## Integrity

- Every mutation is recorded three-way (pristine / mutant / restored) with command, cwd, rc,
  stdout, stderr and the diff in `receipts/`; `mN-diff.txt` holds the exact edit.
- `receipts/restoration.txt`: originals unchanged (`probe 9f56d25d…`, `sweep 56638ea1…`, `gate
  797085c2…` = preserved copies), and the preserved copies reproduce the baselines
  (`probe --check-receipt` rc 0, `probe --selftest` rc 0, `sweep` on the m5 lane rc 1,
  `sweep --selftest` rc 0).
- Evidence set: `manifest.sha256` (all preserved files), `pristine/`, `mutants/m1..m6/`,
  `fixtures/probe/`, `fixtures/sweep/`, `logs/`. Scratch `/fast/scratch/hyaku/kengaku-r64/ProbeMutate`
  was removed after copying; `cmd=` fields keep the historical scratch paths, and the same bytes
  are preserved here.

## Tooling

No installs or upgrades were made (no tool was needed: python3 3.14.8 and the stdlib only; pacman
untouched). No network call, no port bind.
