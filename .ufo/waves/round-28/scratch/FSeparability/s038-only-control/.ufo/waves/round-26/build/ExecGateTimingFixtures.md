# Round 26 Q13 gate-timing fixtures

- Private clone base observed: `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`; branch `r26-ExecGateTimingFixtures-4`.
- Wrote only `plans/fixtures/r26/gate_timing/` in that clone (no lane implementation files).
- `late-report.md`: admit cites `.ufo/waves/round-26/falsify/SecondSeatA.md`; report arrives in a later commit, so the landing commit should fail.
- `generic-wave-2.md`: admit cites only “wave-2 seats”; should fail for lack of a concrete report path.
- `same-commit-report.md`: the cited different-seat report and admission land together; should pass.
- `same-writer-report.md`: cited report is by `SameSeatD`, matching `knowledge/case-d.md`'s `writer: SameSeatD`; should fail the second-seat condition.
- `recreate.sh` creates isolated scenario branches in `/tmp/kengaku-r26-ExecGateTimingFixtures-sbx`; it refuses to replace an unmarked existing path and permits repeat runs over its own sandbox.
- Fixture SHA-256 (every file written in clone):
  - `plans/fixtures/r26/gate_timing/late-report.md` `266378e956e9e4d9302dfdf03e7300939063d8a7737e75aa059c1efc40fd3188`
  - `plans/fixtures/r26/gate_timing/generic-wave-2.md` `40f4d122b259b5ae12c37f8d3a93d24735cd0da274fa3370f5a6001fec5f0e25`
  - `plans/fixtures/r26/gate_timing/same-commit-report.md` `ba1029bd4edb8da2e61caf4bc5925ddc1684986c0711f9420f69db7660127aa8`
  - `plans/fixtures/r26/gate_timing/same-writer-report.md` `47c3c9c64bdde4b179448a3f4f8c7bef2f5147ce9aefe21a4c1d06c29c0ea344`
  - `plans/fixtures/r26/gate_timing/recreate.sh` `5816471c9cb057f18dca44d7f7f32b301787dd6b1309257094441c6a06157379`
- Ran the requested recreation command `sh /tmp/kengaku-r26-ExecGateTimingFixtures-4/plans/fixtures/r26/gate_timing/recreate.sh`; output:
  ```text
  sandbox=/tmp/kengaku-r26-ExecGateTimingFixtures-sbx
  base=f40384909fad62da89354c9031f22d7af4d4f591
  case_a_landing=8eaef3e0bff8b23836715696f171ad6f7b60f79a
  case_a_report_later=50d49f8308ac0e77991fdd404ec0dbef96f9b2ce
  case_b_generic_only=50e3c1abd6f76350b78bc30b79623e5b7d4e5883
  case_c_same_commit=461127a1beb9a096f90a70d0c1c6a43ff5c89245
  case_d_same_writer=7da2ea97d65e1d88f4741eb8db16e3cd47541961
  expected=FAIL,FAIL,PASS,FAIL
  ```
- Evidence: script output records distinct landing/report commits for case A; B/C/D are isolated branches from the base so other fixture reports cannot satisfy an uncited row.
- Risk: these are fixture-side expected outcomes; `gate_timing_check.py` was not available in the base clone and was not run here. Main integration should run the checker against each listed lesson/commit and verify the four outcomes.
- Blockers: none for the assigned fixture work.
- Installs: none.

VERDICT: Four isolated, reproducible Q13 timing fixtures and the recreation script are present in the private clone; scoped work complete.