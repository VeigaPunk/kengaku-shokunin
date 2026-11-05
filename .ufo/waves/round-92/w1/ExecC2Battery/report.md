# ExecC2Battery-3 — R92-C2 conformance battery (scratch clones only)

Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin (read-only against the lane; no lane git mutation, no commits, no subagents).
Clone: detached at B2 f0018773f507f363854123856990f8ff8a87eb8c under /fast/scratch/hyaku/kengaku-r92/ExecC2Battery (removed before yield).
Receipts: controls.txt (same directory). Frozen inputs read: plans/round92_c2_conformance.py, plans/round91_c1_replay.py, plans/round91_counter_pin.py, plans/round92-selftest-expectations.json, plans/counter-pins-r91.json, plans/round-92-claims.md (R92-C2 section).

## Results

| # | Control | Expected | Observed | Verdict |
|---|---|---|---|---|
| 1 | base-all-red (`--rev 4ba56182`) | rc 1, all three FAIL | rc 1; M7 FAIL (base-L5=10), M12 FAIL, M9 FAIL (base-flag-present=True, base-table-absent=True) | MATCH |
| 2 | tip-all-green (`--rev f0018773`) | rc 0, all three pass | rc 1; M7 pass, M12 pass, **M9 FAIL** (tip-flag-absent=False) | **FINDING F1** |
| 3 | tip-openssl-masked (round91_c1_replay, masked PATH) | rc 2, `DEFECT SETUP host probe absent`, `PREDICATE R91-C1 could-not-evaluate` | exactly that, rc 2 | MATCH |
| 4 | base-openssl-masked-unguarded (BASE copy of round91_c1_replay) | rc 1, traceback, no PREDICATE line | rc 1; Traceback, `FileNotFoundError: 'openssl'` at line 243; 0 PREDICATE lines | MATCH |
| 5 | flag-gone | `git grep -c skip-selftest` empty, exit 1; CHILD_ENV >= 1 | grep prints `plans/round91_counter_pin.py:2` (exit 0); CHILD_ENV count 3 | **FINDING F2** |
| 6 | table-pin-rewrite | leg1 rc 2 `expectations-pin mismatch`; re-pin rerun rc 0 | leg1 MATCH (rc 2); re-pin rerun rc 1 | **FINDING F3** |

Counts: 3 controls matched as expected (1, 3, 4); 3 findings (F1, F2, F3). No control was patched or re-tuned to pass.

## Findings

**F1 — M9 tip check fails at B2; the frozen claim's literal predicate is not met.** The `--skip-selftest` flag is functionally gone: `round91_counter_pin.py` argparse at f0018773 has only `--lane --rev --work --selftest --self-entry-path`, and `--skip-selftest` is rejected (`unrecognized arguments`, rc 2). But the literal string survives in the checker bytes at lines 16 (usage docstring: `[--selftest] [--skip-selftest] ...`) and 211 (selftest docstring: "Children run the production entry point with --skip-selftest"). `round92_c2_conformance.py` M9 tests `"--skip-selftest" not in tip_c2_text`, so `tip-flag-absent=False` and the whole R92-C2 predicate is red at B2 (rc 1). The claim text (`the checker bytes contain no --skip-selftest`) is literally false at B2, and the expected control-2 result (rc 0) does not hold. Everything else at tip is green: M7 pass (tip-rc 0, PREDICATE R91-C1 pass), M12 pass (tip rc 2, DEFECT SETUP, could-not-evaluate), M9 tip-table-present=True, tip-table-pinned-match=True, and the default counter run is rc 0 with PINS 17/17 and SELFTEST 9/9. Not repaired: editing those two docstring lines or re-freezing the predicate is an integration/L0 decision.

**F2 — control 5 first half is red for the same reason.** `git grep -c 'skip-selftest' f0018773 -- plans/round91_counter_pin.py` prints `...:2` (exit 0), not empty/exit 1. The second half (`CHILD_ENV` count 3) is green.

**F3 — control 6 leg 2 does not pass; the residual is real but a consistent rewrite must be used to reproduce it.** Leg 1 (clean-green rc flipped 0→1 in the table, committed at 153903a7): `DEFECT SETUP expectations-pin mismatch plans/round92-selftest-expectations.json`, rc 2 — as expected. Leg 2 (ledger sha for the table re-pinned to fc8b5cc4…, committed at 8fbd68e1): all 17 pins match, but the selftest fails — `SELFTEST clean-green rc=0 want=1 ok=False`, `SELFTEST-DETAIL cases=9 red-green-ok=8`, rc 1. The control predicted rc 0. The selftest's own honest child run of the clean fixture is rc 0, so a rewritten row that contradicts the honest outcome is caught even after re-pinning. The "passes rc 0" prediction therefore does not hold for that rewrite.
  Extra leg 3 (disclosed residual, NOT a pass of control 6): table at a2c1cd1f restores clean-green rc 0 and weakens counter-byte-mutated's expected defect text from `PIN-MISMATCH bytes plans91/a.txt` to `PIN-MISMATCH` (selftest matches by substring); ledger re-pinned at dfcf4f0e to e116e156…. Checker bytes unchanged. Result: `PINS checked=17 matched=17`, `SELFTEST cases=9 red-green-ok=9`, `PREDICATE R91-C2 pass`, rc 0. So a weakened table whose pin is regenerated in one commit still passes the default run. This is the known residual the claim says it does not close; it is owned by the L0 kengaku round-91 in-tree-pin question and is disclosed here, not closed.

## Observations (not controls; lower priority)

- O1 [INFERENCE, not exercised]: `round91_counter_pin.py` takes the expectations table from the `--rev` blob for the parent run but builds the selftest fixtures' `real_bytes` from `Path(__file__).with_name(...)`, i.e. the working tree of the running checker. When the running checker's tree differs from `--rev`, the parent and the fixtures can read different tables. All my runs had tree == rev (verified clean before each run), so this did not change any result.
- O2 [minor]: `round92_c2_conformance.py` M9 `tip-table-pinned-match` hashes `tip_expect.encode("utf-8", errors="replace")` (text re-encoded), not the raw blob bytes. Harmless for the ASCII table (sha 4453495a… matches the ledger), but it is not a byte hash in general.
- O3 [observed]: control 1's expected "tip" fields are BASE-valued by construction when `--rev 4ba56182` is passed, since the conformance script treats `--rev` as the tip; the expected output is still reproduced.
- O4: the first concurrent launch of controls 1 and 2 failed to redirect (a `mkdir` raced into a backgrounded chain); control 2 was then re-run cleanly. Control 1's result is from the completed background job (same command, same work dir), not a repeated run.

## Tool installs / host

- No tools installed or updated (uv/npx/pacman untouched; pacman paused host-wide and not used).
- No host sysctl touched: `/proc/sys/user/max_user_namespaces` read-only (122865 at run time). bwrap at /usr/bin/bwrap was present; controls 3/4 did not depend on the sandbox outcome.
- Masked-PATH fakebin lives in scratch only (symlinks to absolute tool paths, no openssl).
- Scratch commits (clone only, never in the lane): 153903a7, 8fbd68e1, a2c1cd1f, dfcf4f0e. The clone and its work dirs are removed before yield.

## Checks the main agent should run

- `python3 plans/round92_c2_conformance.py --lane . --rev f0018773f507f363854123856990f8ff8a87eb8c --work DIR` in a clean clone: expect the current rc 1 with M9 FAIL on `tip-flag-absent=False` (F1) unless the two docstring references are removed or the predicate is re-frozen.
- `git grep -c 'skip-selftest' f0018773f507f363854123856990f8ff8a87eb8c -- plans/round91_counter_pin.py` (F2 evidence).
