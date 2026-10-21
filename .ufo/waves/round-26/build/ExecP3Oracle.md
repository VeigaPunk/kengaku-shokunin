# ExecP3Oracle — round 26 build: independent P3a/P3b/P3e oracle (writer, KengakuR26-2.ExecP3Oracle-4)

Clone `/tmp/kengaku-r26-ExecP3Oracle`, branch `r26-ExecP3Oracle`; observed base `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d` (`git rev-parse HEAD` after `switch -c`).
Measured tree: `git -C kengaku-shokunin archive f11bffbf | tar -x -C /tmp/kengaku-r26-ExecP3Oracle-base`.
Independence: the `plans/state_check.py` source was never opened; v2 was run only after the oracle and its base output were frozen (§Cross-check).

## File written (clone only; uncommitted)
- `plans/fixtures/r26/p3_oracle.sh`: sha256 `9c3d3efe22ca1feeb218a37d14ef2a7204060860aa4fb7538932bdaf07a90f6c`, 415 lines, POSIX sh+grep+awk; `--selftest` also uses mkdir/cp/mv/rm.

## Behavior
- `sh plans/fixtures/r26/p3_oracle.sh [ROOT]` prints one `STATUS: id:line — claimed=… observed=…` line per assertion, then TOTAL and VERDICT. Exit 0 = no registered MISMATCH, 1 = at least one, 2 = not a lane root.
- P3a: compares every digit-bearing token in SCORECARD `:558`/`:559` with `corpus/evidence/round25-calibration/*-v2.txt`. A per-row token-coverage guard consumes each token with a rule; any digit left over is a MISMATCH.
- P3b: checks PROVINCE `:112/:116/:117/:119` against the measured-tree census `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` and the r25 receipts.
- P3e: a frozen list of 5 README rows and 5 entries, derived from `git diff --name-status 6180e4f f11bffbf -- corpus/`. It checks row → target exists and entry → index row exists.
- `SUPERSEDED` only applies when a *later* line of the same file matches `R2[5-9]-E[0-9]`, names the subject and carries the re-derived value. `UNVERIFIED` means no receipt exhibits the token (not a contradiction). `SKIP` covers labels, names, dates and commit ids. `X.*` is an oracle-only extension; it is printed but kept out of the totals and exit code.

## Base f11bffbf — `sh p3_oracle.sh /tmp/kengaku-r26-ExecP3Oracle-base` → exit 1
`TOTAL assertions=63 match=57 mismatch=5 superseded=0 unverified=1 skipped_tokens=11 extension_match=6 extension_mismatch=2`
The e0037a8 clone tree (default ROOT) gives byte-identical output apart from the header line.
- MISMATCH `P3a.interval-reverdict.selftest-checks:558`: claimed 14, observed 18 (`attrib-calibration-selftest-v2.txt:19`). This is R26-E1.
- MISMATCH `P3a.state-assertion-check.base-mismatch:559`: claimed 11, observed 10 (`state-check-before-6180e4f-v2.txt:2`). This is R26-E2.
- MISMATCH `P3b.registry-row.rows:112`: claimed 25, observed 42 (census). The receipt it cites, `round24-census/after.txt:29`, says 25, so the row is stale rather than miswritten. Part of R26-E3.
- MISMATCH `P3b.round25-correction.after-r25-rows:119`: claimed 37, observed 42 (census; `round25-census-after.txt:3` `sources_rows=42`). Part of R26-E3.
- MISMATCH `P3e.file.lessons/round-25-verifier-spotcheck.md`: the file exists (added in `f11bffbf`) but has no `corpus/README.md` row. **Not in R26-E1..E4.**
- UNVERIFIED `P3a.state-assertion-check.exit-contract-2:559`: col2 says "exit 0/1/2". Exits 0 and 1 are exhibited (after-v2, before-v2); no state-check receipt exhibits exit 2.
- MATCH (57):
  - P3a `:558` (13): unique_samples 4, scored_trials 92, correct 92, transitions `FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4`, mismatches 0, summary-exit 0, selftest-failed 0, red-runs R1..R6, receipts-dir, round 25, cp95, sha256-pinned, token-coverage (14 rules).
  - P3a `:559` (10): base-commit 6180e4f, base-exit 1, landed-mismatch 0, landed-superseded 1, landed-exit 0, selftest ALL PASS, exit-contract-0, exit-contract-1, round 25, token-coverage (9).
  - P3b `:112` (3): census-receipt exists, gate-receipt exists, token-coverage (4).
  - P3b `:116` (9): summary-exit 0, selftest-exit 0, unique-samples 4, correct 92/92, FAIL>UNTESTED 2, PASS>INDETERMINATE 1, sha256-pinned, round 25, token-coverage (9).
  - P3b `:117` (7): landed-summary-exit 0, selftest-exit 0, base-commit, base-exit 1, base-mismatch 10, round 25, token-coverage (5).
  - P3b `:119` (6): quoted-rows 25, base-rows 26 (`round25-census-before-6180e4f.txt:3`), base-last-id S026, absent-markers "Five" = 5 dated `ABSENT` rows (PROVINCE:12,13,14,16,17), QUALITY R4 exists, token-coverage (9).
  - P3e (9): rows → file at README:61, 92, 93, 167, 168; entries → row for round25-calibration/, round25-sources/, attribution-interval-calibration.md, round-25.md.
- SKIP (11): python3 ×4, P1, contract-v1, and five `:119` tokens (Round-25 label, 2026-10-20, `e21f9ea`, "round 25" label, census command text).
- X (oracle-only), 2 MISMATCH:
  - README:167 says "S027–S037", but gate.md row keys run S027–S042 (cf. `lessons/round-25.md:118`).
  - README:93 says "M23–M30", but the lesson holds M23–M38 (M31–M38 are under §Falsify-wave corrections, `:63`).
- X, 6 MATCH: F1–F14; README:61 tokens (4, 92/92, TARGET hyper 10/10 PASS→INDETERMINATE, "two" 0/0 FAIL→UNTESTED); README:168 contents in both directions (14 files).

## Selftest — `sh p3_oracle.sh --selftest /tmp/kengaku-r26-ExecP3Oracle-base` → `selftest: 13 checks, 0 failed`, exit 0
- G1 appends R26-E1/E2/E3 rows plus the README row → exit 0; the 4 stale tokens become SUPERSEDED and P3e matches.
- R1–R11 each go red (exit 1) on the named id: R1 selftest count +1, R2 `superseded=2`, R3 one extra SOURCES row, R4 one ABSENT marker dropped, R5 base `mismatch=9`, R6 entry deleted, R7 row deleted, R8 correction placed above the row, R9 correction carrying the stale value, R10 an `R24-E` id, R11 an extra token in `:558`.
- R12 (extension-only red) keeps exit 0. The scratch dir is removed by the trap.

## Cross-check (after freezing)
- I ran v2 (`python3 plans/state_check.py --summary`) on a separate f11bffbf archive: `mismatch=0 superseded=1`, exit 0.
- Its OUT_OF_POPULATION list is exactly the oracle's P3e set (rows @61/92/93/167/168 plus the same 5 files) and P2a `:558/:559`.
- v2 is silent on the unindexed spot-check lesson only because that file is out of population for v2. The scratch copy was deleted.

## Risks for the L1
1. Prediction "≥3" holds: 5 registered mismatches. R26-E3 counts at both `:112` and `:119`, and the P3e lesson row is extra. A v3 that checks P3e in both directions must also go red on `corpus/lessons/round-25-verifier-spotcheck.md`.
2. Separability (claims §Separability): P3b measures the census *at the measured tree*, and C1 adds SOURCES rows. Selftest R3 shows that one added row turns both registry assertions MISMATCH even with a correct R26-E3. The revert test will move C2's count unless P3b freezes the census at S001–S042, or R26-E3 is re-derived at landing and the revert-test treatment of SOURCES is made explicit.
3. Out of P3 scope: v2 reports P2a `sources-registry:557` as SUPERSEDED by R25-E1 "rows 26", with `observed: rows 26` on a 42-row tree. [INFERENCE] v2 checks a frozen S001–S026 subset, so the census-wide staleness of `:557` is invisible to it.
4. Supersession matching is single-line. A wrapped R26-E row reads MISMATCH here (strict) but may read SUPERSEDED in v3, so compare per-id rather than totals only.
5. Portability: only bash (`/bin/sh` → bash) is on the host; dash/busybox are absent and pacman is paused, so the oracle has been run only under bash's sh mode.

Installs: none.
VERDICT: oracle delivered (selftest 13/0). At f11bffbf: 5 registered P3 mismatches — R26-E1, R26-E2, R26-E3 (×2) and the unindexed round-25 spot-check lesson (not covered by R26-E1..E4) — plus 1 UNVERIFIED and 2 extension number-drift findings.
