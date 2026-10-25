# ExecP3Oracle — round 26 build: independent P3a/P3b/P3e oracle (KengakuR26-2.ExecP3Oracle-4)

Clone `/tmp/kengaku-r26-ExecP3Oracle`, branch `r26-ExecP3Oracle`; observed base `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`. Base fixture: `git archive f11bffbf | tar -x -C /tmp/kengaku-r26-ExecP3Oracle-base`. I never opened `plans/state_check.py`.

## Files written
- Clone only: `plans/fixtures/r26/p3_oracle.sh`, sha256 `f7f9311c8bed8ee89362c98733c8a29adf4864355a417d14d55eb17aecf0e0b1`, 431 lines. POSIX sh+grep+awk; selftest additionally uses mkdir/cp/mv/rm.
- Exclusive advisory report: `.ufo/waves/round-26/build/ExecP3Oracle.md` (this file). No production files changed; no installs.

## Behavior
- Checks the unchanged numeric scope: P3a every digit-bearing token in SCORECARD:558/:559 against round-25 v2 receipts; P3b PROVINCE:112/:116/:117/:119; P3e the frozen five README rows and five corresponding files in both directions.
- **Amendment 1:** P3b verifies each dated SOURCES id S001–S042 appears exactly once, and uses that frozen set as the count. S043+ are ignored, not counted. Missing or duplicate ids make the existing P3b count assertions fail.
- A later correction supersedes only when it contains the exact P3 assertion id and the observed value as a literal backticked token. This selects SCORECARD R26-E5/E6 and PROVINCE R26-E8/E7 respectively.
- `X.*` number-drift probes remain outside registered totals/exit code. `UNVERIFIED` means no receipt exhibits the claimed token.

## Required runs and per-assertion results
Base `f11bffbf`: `sh p3_oracle.sh /tmp/kengaku-r26-ExecP3Oracle-base` → exit 1; `TOTAL assertions=63 match=57 mismatch=5 superseded=0 unverified=1 skipped_tokens=11 extension_match=6 extension_mismatch=2`.
- MISMATCH `P3a.interval-reverdict.selftest-checks:558`: 14 claimed, 18 in `attrib-calibration-selftest-v2.txt:19` (R26-E1).
- MISMATCH `P3a.state-assertion-check.base-mismatch:559`: 11 claimed, 10 in `state-check-before-6180e4f-v2.txt:2` (R26-E2).
- MISMATCH `P3b.registry-row.rows:112`: 25 claimed, frozen exact id-set count 42; cited round-24 receipt says 25 (R26-E3).
- MISMATCH `P3b.round25-correction.after-r25-rows:119`: 37 claimed, frozen exact id-set count 42; `round25-census-after.txt:3` says 42 (R26-E3).
- MISMATCH `P3e.file.lessons/round-25-verifier-spotcheck.md`: exists but was not indexed in base README.
- UNVERIFIED `P3a.state-assertion-check.exit-contract-2:559`: no committed state-check receipt exhibits exit 2.

Live read-only lane: `sh p3_oracle.sh /home/vgpnk/Projects/shokunin/kengaku-shokunin` → exit 0; `TOTAL assertions=63 match=58 mismatch=0 superseded=4 unverified=1 skipped_tokens=11 extension_match=6 extension_mismatch=2`.
- SUPERSEDED `P3a.interval-reverdict.selftest-checks:558` → SCORECARD:748 R26-E5.
- SUPERSEDED `P3a.state-assertion-check.base-mismatch:559` → SCORECARD:749 R26-E6.
- SUPERSEDED `P3b.registry-row.rows:112` → PROVINCE:185 R26-E8.
- SUPERSEDED `P3b.round25-correction.after-r25-rows:119` → PROVINCE:184 R26-E7.
- No registered mismatches; P3e `corpus/lessons/round-25-verifier-spotcheck.md` has its index row at README:94.
- UNVERIFIED exit-contract-2 remains unverified.

## Selftest and extra observations
`sh p3_oracle.sh --selftest /tmp/kengaku-r26-ExecP3Oracle-base` → `selftest: 14 checks, 0 failed`, exit 0. R1–R13 cover changed receipt values, exact supersession, S043 exclusion, missing+duplicate frozen ids, index both-directions, correction position/id/value, unchecked tokens and extension-only drift. R3 adds S043 and leaves P3b values unchanged; R13 changes S042 to S041, creating a duplicate plus missing id, and correctly fails the frozen-id-set assertion.
- Extension-only MISMATCH README:169 S027–S037 vs gate row keys through S042; MISMATCH README:93 M23–M30 vs lesson rows M23–M38. Both remain excluded from exit status. F1–F14 and six other extension values match.

VERDICT: Amendment 1 implemented in the independent oracle; base retains exactly 5 registered mismatches, live has 0 registered mismatches and 4 exact supersessions, and the updated 14-case selftest passes. No production edits or installs.