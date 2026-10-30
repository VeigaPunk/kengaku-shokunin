# R7ProbeOracleAudit — round 55 wave 1 seat report

## Assignment
Oracle audit of `plans/round55_c3_chess_probe.py` (R55-C3 instrument): verify (1) the verdict
derives only from executing the captured grader's own test function in bwrap; (2) `/tests` is
bound read-only and the capture is a runtime-sha-checked byte-copy; (3) the 12-case table
matches the frozen list byte-for-byte; (4) a mismatch necessarily changes printed M and the
exit code; (5) no case's outcome can depend on wall-clock/network/env. No lane writes.

## Environment
- Lane tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (== freeze commit == remote master).
- Probe file sha256 `7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60`
  (matches the value E6ChessReceipt recorded).
- Host: bwrap 0.13.1 at `/usr/bin/bwrap`, python 3.14.8.
- Scratch: `/fast/scratch/hyaku/kengaku-r55/R7ProbeOracleAudit/` (created, used, deleted on
  exit of this seat's work; receipts copied here first).
- Installs: none (no tools installed or upgraded; nothing recorded).

## What I ran (commands, exit codes)
| Command | Exit | Result |
|---|---|---|
| read `plans/round-55-claims.md` + full probe source (255 lines) | 0 | frozen claims + instrument read |
| `git status` / `git diff 80afa613 -- plans/round55_c3_chess_probe.py` | 0 | probe **untracked** at tip (defect D1); capture dir clean |
| `sha256sum` on capture; `git cat-file` attempt | 0 | capture sha = `a540714e…30cb8f286` = frozen pin; probe not in any commit |
| read-only GET upstream grader at the TB2 pin (`harbor-framework/terminal-bench-2@2fd12b88…/chess-best-move/tests/test_outputs.py`) | HTTP 200 | upstream sha = frozen pin; `cmp` vs in-repo capture: byte-identical |
| read-only GET upstream `instruction.md` at pin | HTTP 200 | confirms `h1h8` example grounding the `instruction-example-h1h8` case |
| `compare_cases.py` (parse frozen card from `w1-spec.json` + `build_spec_w1.py` CASES, compare to probe table) | 0 | names/order/predictions identical; bytes identical after decoding the card's double-escape rendering |
| `python3 plans/round55_c3_chess_probe.py --selftest --work <scratch>` | 0 | `SELFTEST cases=2 failures=0` |
| `python3 plans/round55_c3_chess_probe.py --lane <lane> --work <scratch> --receipt <scratch>/probe-receipt.txt` | 0 | all 12 observed==predicted, `mismatches=0`, `PREDICATE R55-C3 pass` |
| `attacks.py` (14-check attack battery, scratch-only copies/lanes) | 0 | 14/14 PASS (see findings) |
| `/usr/bin/time` battery run | 0 | wall 0.38 s; `--work` dir auto-removed (verified) |

## Files written
- `.ufo/waves/round-55/w1/R7ProbeOracleAudit.md` (scoped findings — the Report trailer path)
- `.ufo/waves/round-55/w1/R7ProbeOracleAudit/report.md` (this file)
- `.ufo/waves/round-55/w1/R7ProbeOracleAudit/probe-stdout.txt` (my battery run, exit 0)
- `.ufo/waves/round-55/w1/R7ProbeOracleAudit/probe-receipt.txt` (its `--receipt` tee)
- `.ufo/waves/round-55/w1/R7ProbeOracleAudit/selftest-run.txt`
- `.ufo/waves/round-55/w1/R7ProbeOracleAudit/attacks-receipt.txt` (14/14 attack log)
- Scratch comparison/attack drivers (deleted with scratch): `compare_cases.py`, `attacks.py`.

No lane file was created, modified, or deleted. No git/jj mutation (read-only `git -C` only).
No subagents. No `agent://all` messages.

## Findings (the five checked properties)
All five hold; evidence summarized in `R7ProbeOracleAudit.md`. Attack battery results
(`attacks-receipt.txt`):
- `sha-gate-tampered-capture`: one-bit capture tamper → exit 2, `SETUP grader sha256 …`,
  zero CASE lines (verdicts never computed from a drifted grader).
- `sha-gate-alternative-grader`: a plausible alternate grader (accepts `h1h8`) → exit 2 at the
  sha gate. No oracle substitution possible.
- `tests-readonly-write`: `open('/tests/pwn.txt','w')` in the sandbox → `Errno 30 Read-only`.
- `tests-bytecopy-in-sandbox-sha`: sha of `/tests/test_outputs.py` inside the sandbox = pin.
- `no-network-in-sandbox` / `only-loopback-in-sandbox`: connect → OSError; `/proc/net/dev` = `lo:` only.
- `prediction-flip-counts-mismatch`: one wrong prediction → `mismatches=1`, exit 1,
  `PREDICATE R55-C3 fail`.
- `case-byte-flip-changes-observed-and-mismatch`: `empty-file` bytes → `g2g4 e2e4` →
  observed flips to P, `mismatches=1`, exit 1.
- `probe-verdicts-equal-direct-grader-executions`: 12/12 direct bwrap grader runs match the
  probe's recorded verdicts.
- `candidate-B-bytes-contradict-frozen-PASS`: the literal-backslash reading of the frozen card
  makes a PASS-predicted case FAIL under the pinned grader — the probe's real-newline reading
  is the only one consistent with the frozen predictions.
- `hostile-env-run-0/1` (PYTHONHASHSEED/LANG/TZ/TMPDIR/HTTPS_PROXY/PYTHONPATH): stdout
  byte-identical to baseline, exit 0.
- `determinism-two-runs-byte-identical`, `matches-landed-corpus-receipt`: byte-identical to
  each other and to the landed `corpus/evidence/round55/chess-best-move-probe.txt`.

## Defects found
1. **D1 — probe untracked at the frozen tip.** `plans/round55_c3_chess_probe.py` shows `??` in
   `git status`; it exists in no commit (`git log --all -- <path>` empty). A clean-clone
   after-run would lack the instrument and the C3 after-predicate could not be re-executed.
   L1 must commit it at/before landing. (E6ChessReceipt flagged the same.)
2. **D2 — frozen card's byte notation is double-escaped** (`build_spec_w1.py` holds
   single-escaped strings and emits `{b!r}` into the dispatch card). The probe's table is the
   semantically forced reading (proved by attack 7), but a mechanical copy of the card into
   source would produce bytes contradicting the frozen predictions. No probe change required.
3. **D3 — F/SETUP boundary keys on the literal `AssertionError` output string.** Exact for
   this capture (the only nonzero-exit path is the assert); for a different grader, other
   exceptions become SETUP (exit 2) — an honest failure, never a hidden mismatch.

## Dead ends
- Invalid-UTF-8 `move.txt` via the probe's write path is unreachable (`content.encode("utf-8")`
  can only emit valid UTF-8), so the SETUP path cannot be triggered by case bytes — SETUP is
  an infra-failure guard only. (Initial attack-draft used this; replaced with the direct
  differential check.)
- Upstream fetch against `laude-institute/terminal-bench` 404'd (repo moved to
  `harbor-framework/terminal-bench-2`, confirmed via the lane's own SOURCES.md rows and
  the GitHub API redirect); retry against the correct repo returned 200 with the matching
  pin.

## Verification status
Everything in scope was executed, not assumed. The only unrun item: none.
