# ProbeVulnSecretR81 — round 81 w1 seat report (role: executor)

Item: offline replay instrument for the Terminal-Bench 2.0 `vulnerable-secret` grader (R81-C1).
Judged on: coverage, calibration.

## Deliverable

- Path: `.ufo/waves/round-81/w1/ProbeVulnSecretR81.py`
- sha256: `aedcc297135110a158112cdc32c3fff1cccde1c33a4d2e6abfaf983fe6e69e0f`
  (`sha256sum .ufo/waves/round-81/w1/ProbeVulnSecretR81.py`, at lane tip `03affddfd9b4e976cb1c3f09336e11ee2dc33621`)

No tool installs were needed or performed (`/usr/bin/bwrap` and host python3 already present; pacman untouched).
Scratch used: `/fast/scratch/hyaku/kengaku-r81/ProbeVulnSecretR81/` (deleted before yielding).

## Instrument contract (as built)

- Replays the committed round-52 capture
  `corpus/evidence/round52/graders/vulnerable-secret/tests/test_outputs.py` (39 lines, three test
  functions, five asserts), byte-pinned: `PIN = f2b65f63ac81acd1e80e1ad4c59c1022131a0f9eb20f8ab3212c4ef8d8f0c753`
  (recomputed locally with `sha256sum`; a drift is a SETUP exit 2, never faked).
- Same bwrap recipe / leg rule as `plans/db_wal_probe.py` and `plans/round59_c1_openssl_probe.py`:
  capture staged and bound read-only at `/tests`, staged writable `/app` (`--bind`), harness ro-bound,
  `--unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session`, ro `/usr` + `/etc`
  (+ symlinked `/bin` `/sbin` `/lib` `/lib64`), `--proc /proc --dev /dev --tmpfs /tmp --tmpfs /home`,
  `--chdir /app`, pinned env (`PATH`, `HOME=/tmp`, `LANG`/`LC_ALL=C.UTF-8`, `PYTHONUTF8=1`,
  `PYTHONDONTWRITEBYTECODE=1`), host `/usr/bin/python3` runs the in-sandbox harness.
- Leg rule: the capture's own test functions called in file order
  (`test_results_file_exists`, `test_results_file_contains_secret_flag`, `test_results_file_format`);
  case observed `P` iff all three legs pass; `rc=0` iff all legs pass.
- Case table: the item's frozen eight (exact flag P; trailing newline + surrounding spaces P;
  missing file F; wrong flag F; `FLAG{` only F; `FLAG{x}` F; flag + trailing second line F;
  truncated flag F) plus two strip-variant P cases (`exact-flag-newline`, `exact-flag-spaces`)
  because the frozen eight floor at 2 P and the item requires >= 8 cases with >= 4 P and >= 4 F.
  Total 10 cases: 4 P / 6 F, every case stages `/app/results.txt` (or stages nothing for `missing-file`).
- Predictions DERIVED in code: `leg_truth()` evaluates the capture's five asserts on each case's
  staged content; case predicts P iff all hold. `--selftest` cross-checks the derived model against
  independently declared violated-assert tags per case (exact set equality), point flips, leg-order
  and the shape floors: 24 checks, 0 failures.
- Flags: `--lane`, `--work`, `--receipt` (also writes the stdout stream to the path), `--selftest`.
- Battery stdout is exactly the receiptable stream: `REV <hex>` first line, one
  `CASE <id> predicted=<P|F> observed=<P|F> rc=<0|1>` per case, the `cases=... mismatches=` line,
  then `PREDICATE R81-C1 pass|fail`. Exit 0 iff mismatches=0. Per-leg detail goes to stderr only,
  so the stdout/OBSERVATIONS projection stays deterministic.

## Environment pins (for a minted receipt's stamp block)

- `HOST_PYTHON`: `Python 3.14.8`
- `HOST_OPENSSL`: `OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)`
- bwrap: `/usr/bin/bwrap` present (`-rwxr-xr-x root root 84464 Oct 14 19:06`) — real runs, no faking.
- Measured at lane tip `REV 03affddfd9b4e976cb1c3f09336e11ee2dc33621` (worktree clean; the tip moved
  from `9298848` through `8eb887a` to `03affdd` during the wave as integration landed; the capture
  pin never drifted).

## Full run stdout (battery, run 1; run 2 byte-identical)

```
REV 03affddfd9b4e976cb1c3f09336e11ee2dc33621
CASE exact-flag predicted=P observed=P rc=0
CASE exact-flag-newline-spaces predicted=P observed=P rc=0
CASE exact-flag-newline predicted=P observed=P rc=0
CASE exact-flag-spaces predicted=P observed=P rc=0
CASE missing-file predicted=F observed=F rc=1
CASE wrong-flag predicted=F observed=F rc=1
CASE prefix-only predicted=F observed=F rc=1
CASE short-flag predicted=F observed=F rc=1
CASE flag-plus-second-line predicted=F observed=F rc=1
CASE truncated-flag predicted=F observed=F rc=1
cases=10 observed_pass=4 observed_fail=6 mismatches=0
PREDICATE R81-C1 pass
```

Commands:
```
python3 .ufo/waves/round-81/w1/ProbeVulnSecretR81.py --lane . --work <scratch>/wave/run1 --receipt <scratch>/wave/receipt1.txt   # rc 0
python3 .ufo/waves/round-81/w1/ProbeVulnSecretR81.py --lane . --work <scratch>/wave/run2 --receipt <scratch>/wave/receipt2.txt   # rc 0
python3 .ufo/waves/round-81/w1/ProbeVulnSecretR81.py --lane . --selftest                                                        # rc 0
```

## Determinism

- stdout1 sha256: `c0cf6e56a3a75a9da15b2b207d1d57b472b5a44eb1a7d252790d2f78a63e3b35`
- stdout2 sha256: `c0cf6e56a3a75a9da15b2b207d1d57b472b5a44eb1a7d252790d2f78a63e3b35`
- `diff stdout1.txt stdout2.txt` → identical; both runs exit 0.

## Per-leg evidence (stderr of run 1; order = capture file order)

```
LEG exact-flag                     ... PPP
LEG exact-flag-newline-spaces      ... PPP
LEG exact-flag-newline             ... PPP
LEG exact-flag-spaces              ... PPP
LEG missing-file                   ... FFF
LEG wrong-flag                     ... PFP
LEG prefix-only                    ... PFF
LEG short-flag                     ... PFF
LEG flag-plus-second-line          ... PFF
LEG truncated-flag                 ... PFF
```

Each F decays on exactly the asserts the static model derives: `wrong-flag` fails only the stripped
equality; `prefix-only` fails endswith+length; `short-flag` fails equality+length; `flag-plus-second-line`
fails equality (inner newline survives `.strip()`)+endswith; `truncated-flag` fails equality+endswith;
`missing-file` fails all three functions (FileNotFoundError in tests 2/3).

## Selftest stdout

```
REV 03affddfd9b4e976cb1c3f09336e11ee2dc33621
SELFTEST cases=10 checks=24 failures=0
```

## Notes for the L1 (integration)

- The frozen table's TOOL is `plans/round81_vulnerable_secret_probe.py` (tracked at master, sha-pinned
  by receipts); this deliverable matches that contract (same capture pin `f2b65f63…`, same bwrap family,
  same OBSERVATION-form-compatible stdout, `--lane/--work/--receipt/--selftest`) with the item's exact
  `CASE <id> predicted=<P|F> observed=<P|F> rc=<0|1>` line format. `plans/` was not edited.
- Two bring-up bugs were fixed in the deliverable before any green run (both mine, both caught by the
  run itself): case tuple unpack order (crash on first staged case) and leg-letter parse index
  (all legs misread as `sgt` → 4 mismatches → honest `PREDICATE R81-C1 fail` + exit 1). No run output
  was ever fabricated; the failing outputs above the fix were exit-1 honest failures.
- Counter fit: stdout lines are exactly `REV`/`CASE `/`cases=`/`PREDICATE R81-C1 pass`, so the counter's
  projection (drops `REV`, blanks, `cases=`) of a fresh run equals the projection of a minted receipt's
  OBSERVATIONS block, and `verdict` resolves to `predicate`.

Scope kept: wrote only the deliverable file and scratch; no plans/, ledger, SOURCES/SCORECARD/LOG/SKILL/QUALITY
or any tracked lane file touched; no git/jj mutations anywhere; no subagents spawned.
