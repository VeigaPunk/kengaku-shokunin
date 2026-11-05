# ExecC3TriageB — report (round 91, wave w1)

Scope: routed-findings triage, half B, drafts only. Lane clone at `a8de3e69` (scratch, removed on exit). The ledger was read, not edited. No commit, no push, no mutating git in the lane. No subagent dispatch.

Outputs:
- `.ufo/waves/round-91/w1/ExecC3TriageB/resolutions.jsonl` (16 rows, each `supersedes` its base id)
- `.ufo/waves/round-91/w1/ExecC3TriageB/triage-B.md` (per-finding command, exit code, observation)

Verdicts (base id → status → basis):

| base id | status | basis |
|---|---|---|
| R87-V1 | refused | standing L0 question `.ufo/l0-questions.md:312` unanswered; round-88 dispatch marker present |
| R87-V5 | closed | SCORECARD round-87 C1 row states the verdict beside the held score (check rc 0) |
| R87-V6 | blocked (kengaku) | round-87 report names the mission but not progressing or silent |
| R88-2 | blocked (kengaku) | no "four SELFTEST" correction at tip |
| R88-3 | blocked (kengaku) | bundle; residuals R89-A2-1, -2, -3, -5 open |
| R89-A2-1 | blocked (kengaku) | `plans/round91_counter_pin.py` has no ancestry test |
| R89-A2-2 | blocked (kengaku) | no after-figure comparison in `plans/round89_claim_figures.py` |
| R89-A2-3 | blocked (kengaku) | M1–M4 survive on the tip (`mutants.md` lines 16–19) |
| R89-A2-4 | closed | Mistake 10 reported, not repaired; corrections in LOG (check rc 0) |
| R89-A2-5 | blocked (kengaku) | Sentinel hostile cases not re-tested |
| R89-A2-6 | closed | HOST_USERNS in round-90 and round-91 probe receipts (check rc 0) |
| R89-A2-7 | closed | not a finding (row's own text); candidate list consumed by round 90 (check rc 0) |
| R89-D2 | closed | LOG round-90 correction; `selftest-in-path` at `plans/round89_claim_figures.py:546` (check rc 0) |
| R89-D3 | closed | LOG round-90 correction (check rc 0) |
| R89-D4 | blocked (kengaku) | round-89 Gate has no reject row; round-90 S280 row is a different source |
| R89-D6 | closed | LOG round-90 correction; `d1c4f1b0` has no record-table blob (check rc 0) |

Checks: 7 closed rows, each check exit 0 from the clone root; each re-run with an absent anchor token exits 1. Source lines: all 16 resolve (non-blank) at `a8de3e69`.

Observation for the round-91 integrator (not a resolution input): the round-91 claim text places `TRUSTED_TOOL_SHA` in `plans/counter-pins-r91.json`; at `a8de3e69` the constant is in `plans/round89_c1_replay.py:46` and `counter-pins-r91.json` has no such entry (`grep -n TRUSTED_TOOL_SHA plans/counter-pins-r91.json` exit 1).

Tooling: none installed.
