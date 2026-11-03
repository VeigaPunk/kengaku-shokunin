# StrictGateBuild — R67-C2 strict-mode proposal

Proposal built and exercised; committed `plans/round65_c1_sqlite_probe.py` was not edited.
The `--strict` path adds only a new block; the default predicate code path is untouched
(`strict.diff` has no removed lines).

Verdicts:

- Proposal sha256 `27e8b41f…d857`; committed probe sha256 `f44b7283…b4eb`; diff only adds
  `strict_lane`/`strict_tokens`/`strict_failures`/`check_receipt_strict`, the `--strict`
  flag (:1153–1154) and its branch (:1159–1162).
- (a) strict on `corpus/evidence/round66/red/fabricated-r65.txt` → **rc 1**, 24
  `CHECK defect:` lines from s1/s4/s5 (`receipts/a-strict-fabricated.txt`).
- (b) strict on `corpus/evidence/round65/sqlite-gcov-probe.txt` → **rc 0**,
  `PREDICATE R65-C1 strict-pass` (`receipts/b-strict-committed.txt`).
- (c) default on the committed receipt → **rc 0**, `CHECK ok cases=5` +
  `PREDICATE R65-C1 pass` (`receipts/c-default-committed.txt`).
- (d) default on the fabricated fixture → **rc 0**, same pass lines — the pre-existing
  defect, unchanged by the claim (`receipts/d-default-fabricated.txt`).
- Default stdout from unmodified `L` vs proposal: `diff` rc 0, `cmp` rc 0, both sha256
  `a2031df7…fc52` (`receipts/f-default-diff.txt`); also identical on a failing mutant
  (`receipts/g-default-on-mutant-diff.txt`).
- Per-clause calibration: ten single-substitution mutants each exit 1 with exactly the
  intended clause defect (s1, s2 value, s2 lane-byte drift, s3, s4, s5 rc, s5 driver,
  s5 env-missing, s5 nobind delta, s6); `receipts/mutants.diff` + `mut-*.txt`.
- s1: :822–845; s2: :847–860; s3: :862–867; s4: :869–889; s5: :891–920; s6: :922–947.
- Named limitation, reported not narrowed: s5's literal “every `NOBIND` line carries
  `delta=0`” cannot hold for the committed receipt, whose `NOBIND before-battery` /
  `after-battery` session lines carry no `delta`; strict excludes exactly those two
  markers and enforces `delta=0` on every case-scoped `NOBIND G*` line.
- s2/s3/s6 pass on the fabricated fixture (it copies those values); s1/s4/s5 are the
  decisive clauses. A hand-copied full receipt still passes, as the claim states.
- No battery, no listener, no 12355 use, no install, no git mutation; scratch reaped.

Files: `proposed/round65_c1_sqlite_probe.py`, `strict.diff`, `report.md`,
`receipts/` (a–h, mutants, raw stdout).

Exact commands and exit codes:

```
cd S/StrictGateBuild/lane && PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict        # rc=1
cd S/StrictGateBuild/lane && PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt --strict       # rc=0
cd S/StrictGateBuild/lane && PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt               # rc=0
cd S/StrictGateBuild/lane && PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt               # rc=0
cd L && PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt                                     # rc=0
diff -u <proposal stdout> <L stdout>   # rc=0
cmp -s  <proposal stdout> <L stdout>   # rc=0
```
