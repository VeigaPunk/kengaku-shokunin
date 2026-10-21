# MutGateTiming — round-27 bounded mutation probe

Axes: novelty → canonical coverage/constructs; calibration through falsifiable admission-check coverage.
Scope: only `/tmp/kengaku-r27-MutGateTiming/plans/gate_timing_check.py` mutated; no lane source/index/jj changes.
Prescribed clone/branch observed base: `11a7fc8c64dc5d634331be24ccf5936f84a11f03` (`r27-MutGateTiming`).
Read preregistration and operator rules before probing; offline stdlib Python with `PYTHONDONTWRITEBYTECODE=1`.

## Detector and expected results
All commands ran with cwd `/tmp/kengaku-r27-MutGateTiming`; `--lesson` is necessarily repository-relative.
S: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-MutGateTiming/plans/gate_timing_check.py --selftest` → expected exit 0.
R: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-MutGateTiming/plans/gate_timing_check.py --repo /tmp/kengaku-r27-MutGateTiming --commit 8ea41f9 --lesson corpus/lessons/round-25.md` → expected exit 1.
G: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-MutGateTiming/plans/gate_timing_check.py --repo /tmp/kengaku-r27-MutGateTiming --commit b5719440 --lesson corpus/lessons/round-26.md` → expected exit 0.
Kill criterion: expected admission/selftest exit vector `(S,R,G)=(0,1,0)` violated; diagnostic stdout is recorded, not a golden-output assertion.
Each three-command suite ran concurrently; mutations were sequential and independently restored in the same private file.
Ran 39 detector invocations: 3 pristine + 18 mutated + 18 restored; no timeouts, crashes, or inconclusive baselines.

## Pristine and restored output
S stdout: `[selftest] ALL PASS (five allowed roles; connector/mutation-tester/simplifier and unknown roles rejected; declared writer/author/agentId conflicts red; missing report identity with registered reader green)`; exit 0.
R stdout: `FAIL line 29 Gate admit: candidate='knowledge/attribution-interval-calibration.md'`; `cited seat-report paths: none`; generic reference `'wave-2 seats'`; exit 1.
R final stdout: `gate_timing_check: commit=8ea41f9 lesson=corpus/lessons/round-25.md admissions=1 passed=0 failed=1 second-seat-reports=0`.
G stdout: `PASS line 77 Gate admit: candidate='knowledge/grader-perturbation-audit.md'`; three existing returned reports: `FxEntryAll.md`, `FxEntryNumbers.md`, `FxSourceCheckList.md`; exit 0.
G final stdout: `gate_timing_check: commit=b5719440 lesson=corpus/lessons/round-26.md admissions=1 passed=1 failed=0 second-seat-reports=53`.
Pristine stderr was empty for all three commands; every restoration reproduced all stdout, stderr, and exit codes exactly.

## Six independent mutants (locations refer to pristine plans/gate_timing_check.py)
| Mutant | Smallest coherent change | S,R,G exits | Actual selftest output / outcome |
|---|---|---|---|
| M1 role allowlist widened | :23 adds `executor` to `ALLOWED_REPORT_ROLES` | 1,1,0 | stderr `selftest: disallowed role 'executor' was accepted`; KILLED |
| M2 writer-identity check removed | :350–351 deletes seat-name equals candidate-writer rejection; agentId/report-author checks retained | 1,1,0 | stderr `selftest: self-review excluded: expected FAIL, got PASS`; KILLED |
| M3 commit presence replaced by working-copy presence | :654 builds wave inventory via working-copy `rglob`/`lstat`, preserving regular/symlink modes; :663–664 reads wave report/registry blobs from working copy, keeping lesson/candidate at requested commit | 0,1,0 | S stdout identical to pristine ALL PASS; SURVIVED verdict checks |
| M4 generic-reference detection disabled | :229 returns `()` instead of regex matches | 1,1,0 | stderr `selftest: explicit path plus generic red: expected FAIL, got PASS`; KILLED |
| M5 empty-report accepted | after :341 inserts `elif meta.mode == "100644" and meta.size == 0: existing.add(path)` before remaining validation | 1,1,0 | stderr `selftest: empty report excluded: expected FAIL, got PASS`; KILLED |
| M6 registry lookup bypassed | :337 replaces member lookup with `SeatMember("reviewer", None)` | 1,1,0 | stderr `selftest: unregistered INDEX excluded: expected FAIL, got PASS`; KILLED |
Every mutant R retained `admissions=1 passed=0 failed=1`; every mutant G retained `admissions=1 passed=1 failed=0 second-seat-reports=53` and the same three returned reports.
M1/M2/M5/M6 R stdout matched pristine; M4 R omitted the generic-reference diagnostic/reason but still failed for no cited returned report.
M3 R final stdout: `gate_timing_check: commit=8ea41f9 lesson=corpus/lessons/round-25.md admissions=1 passed=0 failed=1 second-seat-reports=87`.
M3 R also printed `missing: Gate does not name a valid second-seat report by path; the commit has 87 second-seat report(s)`; this is working-copy leakage, not actual historical inventory.

## Before / mutated / restored SHA-256
P = `1b748e52a35a5bd900462cd34d0cc3660d06a770b8d06cf05e22b348c4b3f69d`; pristine scratch and live detector hashes initially matched P.
Every mutant's before and restored hash was P; mutated hashes were:
M1 `a0557e75b74048634f9af3a1ddee56b6b34a161d5f9c0b18b44f78f144a17234`.
M2 `714b8f420ab579227cd9d697db1632418826badc79753d2df814e01ad0ecf7d2`.
M3 `d2c50e08992e757cc6d047eef5fda2d89c9b099a5a5e62cfb3ec94c0da1c2f02`.
M4 `f2aa597a3a45956adb108c088d6c2fa4947112062c71ae6a69a192fd6fb0655c`.
M5 `9fee85c8ea7e76d11bc1ed68fc44a1a5385f84bb8ec24377785107c7795b87b1`.
M6 `bfb0cbf08f69d96f725ce57580bc2333c080255b0a41ca91565f769cfbd33e4f`.
Restoration comparisons for M1–M6 each produced `hash_equal=True outputs_equal=True` against pristine; final scratch detector is P.
Only edited source file in clone: `/tmp/kengaku-r27-MutGateTiming/plans/gate_timing_check.py`; final sha256=P. No additional fixture/source files written.

## Round-27 risk
M3 is a coverage finding: the in-memory selftest bypasses production snapshot loading (:605–690); R has no explicit report citation, so independent missing-citation/generic checks still reject; G's cited reports exist both at the commit and in the working copy.
[INFERENCE] A commit-vs-working-copy disagreement case with an explicit cited report, otherwise-valid identity/return data, and different committed/on-disk presence is needed to kill this substitution through admission behavior; this probe did not add or run that unassigned case.
Installs/updates: none. No live model/endpoint, service, package, or other-runtime actions; no implementation or admission decision made.
VERDICT: 5 KILLED, 1 SURVIVED (M3 working-copy substitution); all six exactly restored; survivor remains a round-27 admission-check coverage risk.
