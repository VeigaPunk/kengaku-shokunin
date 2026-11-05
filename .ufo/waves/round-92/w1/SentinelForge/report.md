# SentinelForge — round-92 forgery battery (report)

Seat: SentinelForge (sentinel, leaf). Lane: kengaku-shokunin. Revisions: B2 `f0018773f507f363854123856990f8ff8a87eb8c`
(clone measured at B2; `git clone --shared` + detached checkout, scratch only). All forgeries are
plumbing-only commits (private index) on top of B2 inside the scratch clone; none pushed, none in the lane.
Scratch dir `/fast/scratch/hyaku/kengaku-r92/SentinelForge/` is removed before yield.

Counter bytes measured at B2 (sha256): `round92_c1_replay.py` ebce593e…, `round92_c2_conformance.py` 4aa6e310…,
`round92_burndown.py` c8a2c542…, `round92_bs_probe.py` 13e41e91…, `round91_counter_pin.py` 4c8d4aa4….

## Install / environment record

- Installs or updates performed: **none**. No `uv tool`, `npx`, `cargo`, pacman, or binary download. Only tools on PATH were used (python 3.14.8, git, openssl 3.6.5, bwrap at /usr/bin/bwrap).
- Environment temptations refused: `/proc/sys/user/max_user_namespaces` is 122865 (>0), so no sysctl was touched or needed. Not touched: any PATH directory, `~/.local/bin`, `/etc`, fleet root tracked files, lane index, lane jj state.
- Process hygiene: a recursive gate run I started left ~7k stray processes/dirs under my own scratch. I killed only processes whose cmdline matched my scratch path (`kengaku-r92/SentinelForge/`); no other seat's process was matched.
- Lane touched read-only only (`git clone --shared` reads; `git rev-parse`/`cat-file`).

## Summary table

```
FORGE 1 fabricated receipt: 10 CASE lines ok=True, invented PPPPPP vectors, invented TOOL_SHA/CASE_TABLE_SHA, real host, LANE_TIP=B2 (commit 436c36c3) expected=red-at-tip observed=red rc=1 L5 x9 mismatches vs frozen table, L6 rerun obs mismatch, L7 ledger unexecuted, L8 probe pin unreadable, L9 stamp mismatch; L4 green (table unchanged)
FORGE 2 stamp-consistent fabrication: same invented vectors, TOOL_SHA and CASE_TABLE_SHA = real rev bytes, host values real (commit 13af5e91) expected=red-at-tip observed=red rc=1 L5 x9, L6, L7, L8 red; L9 green
FORGE 2b (extra) FORGE 2 + ledger flip (36 executed, cells 4/27/4/5) + tool pin (commit d946b209) expected=red-at-tip observed=red rc=1 ONLY L5 (9 mismatches) and L6 (rerun obs differ): L5/L6 are the sole guards
FORGE 3 round-91 modernize receipt bytes copied as r92 receipt (commit e2b4e5fd) expected=red-at-tip observed=red rc=1 L2 subject-sha mismatch, L5 "unknown case" x9 + full-pass shape mismatch, L6, L7, L8, L9
FORGE 4 cheating probe: probe sets observed=predicted, never runs grader; receipt from it; ledger flipped; tool pin rewritten (commit 6e9642a8) expected=red-at-tip observed=PASS "PREDICATE R92-C1 pass" rc=0 executed_rows=36 mismatches=0 defects=0
FORGE 5a tampered plans/round91_counter_pin.py (selftest verdict forced True), pins untouched (commit 34d99cdc) expected=red-at-tip observed=red rc=1 "DEFECT PIN-MISMATCH bytes plans/round91_counter_pin.py" PINS 17 checked 16 matched "PREDICATE R91-C2 fail"
FORGE 5b same bytes + pins entry rewritten to match (commit 97d537fa) expected=red-at-tip observed=PASS rc=0 "PINS checked=17 matched=17 mismatched=0", "SELFTEST cases=9 red-green-ok=9", "PREDICATE R91-C2 pass" (disclosed in-tree residual, not a new finding)
FORGE 6a literal M7 rc-2 acceptance in round92_c2_conformance.py, run at BASE 4ba56182 expected=red-at-base observed=red rc=1 "M7-CASE-PARSER FAIL base-rc=1 base-L5=10 tip-rc=1 tip-pass=False" "PREDICATE R92-C2 fail" (no hole from this literal edit)
FORGE 6b one-line `passed = True` in round92_c2_conformance.py, run at BASE 4ba56182 expected=red-at-base observed=PASS rc=0 "M7 FAIL, M12 FAIL, M9 FAIL" printed beside "PREDICATE R92-C2 pass"
FORGE 7 gate (a) closed standalone row check "true" + override_reason, fixture lane expected=red-at-tip observed=red rc=1 "DEFECT closed-check-vacuous CL-A 'true'" "PREDICATE R92-C3 fail"
FORGE 8 gate (a2) closed override row check "true" over base check "grep -q anchor notes.md" expected=red-at-tip observed=PASS rc=0 "freeze=admitted ... overrides=1 checks_run=2" "PREDICATE R92-C3 pass"
FORGE 9 gate (a3) closed row check "true # grep" (FILE_OP word in comment) expected=red-at-tip observed=PASS rc=0 "freeze=admitted checks_run=1"
FORGE 10 gate (a4) closed row check "true 1.0" (PATH_TOKEN matches the number) expected=red-at-tip observed=PASS rc=0 "freeze=admitted checks_run=1"
FORGE 11 gate (a5) closed row with check null, close "closed by inspection" expected=red-at-tip observed=PASS rc=0 "freeze=admitted checks_run=0"
FORGE 12 gate (b) override check "cat ghost/absent.md" over base check, close/source lack the path expected=red-at-tip observed=red rc=1 "DEFECT override-unanchored OLD-1" + "DEFECT check-failed OLD-1 rc=1"
FORGE 13 gate (c) blocked row owner "nobody", fixture conf lists kama/kengaku expected=red-at-tip observed=red rc=1 "DEFECT owner-not-a-lane BL-1 nobody" "unowned_blocked=1"
FORGE 14 gate (c2) same row, SHOKUNIN_ROOT pointing at a conf that lists nobody (extra) expected=red-at-tip observed=PASS rc=0 "freeze=admitted unowned_blocked=0"
FORGE 15 gate (d) chain OLD-1 <- r1 (open) <- r2 (open), base opened 39 expected=red-at-tip (refused, pending naming chain-end) observed=refused rc=1 "freeze=refused oldest_pending_round=39 pending=1" — verdict right, chain-end id NOT named in output (report-format mismatch with the brief). Control chain ending closed: admitted rc=0.
FORGE 16 frozen C3 default command, unmodified B2, `--lane clone --rev HEAD --freeze-round 92` (extra, not a forgery) expected=red-at-tip (a verdict within bound) observed=NO VERDICT: timeout rc=124 after 120 s, 950 nested predicate-selftest dirs and still growing; an earlier child ran to nesting depth 103 and hit a 600 s TimeoutExpired
FORGE 17 marker spoof (extra): copy of gate with one selftest expectation flipped red; `--selftest` run rc=1 red; same copy via a python -c wrapper that writes `.predicate-selftest-child` (its own pid + sha of its argv) and runs the gate child: expected=red-at-tip observed=PASS rc=0 "PREDICATE R92-C3-BATTERY pass", zero SELFTEST lines printed
```

## Method notes

- C1 counter runs were `python3 -I -B plans/round92_c1_replay.py --lane <clone> --rev <forgery> --work <fresh dir>` from the B2 clone. The counter reads all inputs by `git show <rev>:<path>` and reruns the probe from `git archive <rev>`, so forgeries were evaluated at their own revs.
- The gate could not be run through its default path on fixtures (FORGE 16): the default path recurses (see Finding G1). Fixture verdicts (FORGE 7–15) were therefore taken from `evaluate()` imported from the B2 gate file, with `SHOKUNIN_ROOT` set to the fixture conf. That is the same function the default path calls; only the self-test wrapper is bypassed. FORGE 17 separately shows the default path's self-test wrapper.
- Fixture lanes: `fx/<name>/` git repos with `corpus/routed-findings.jsonl` and `notes.md` (`# notes` / `some anchor line`). Seeds: six base rows `SEED-n`, opened 88, status refused, blocker L0. Conf: `root-kk/shokunin.conf` (LANES kama, kengaku) and `root-nobody/shokunin.conf` (kama, nobody).
- Plumbing commits: `GIT_INDEX_FILE` private index in the scratch clone; the clone worktree was never modified for forgeries.

## Per-forgery evidence

### FORGE 1 — fabricated receipt (commit 436c36c3)
File `corpus/evidence/round92/bs-probe.txt`: header, stamp fields (SUBJECT_SHA true; TOOL_SHA and CASE_TABLE_SHA copied from round-91 files; HOST_* live; LANE_TIP=B2), `CASES 10 LEGS 60`, 10 `CASE <frozen id> predicted=PPPPPP observed=PPPPPP ok=True ...` lines, `mismatches=0`, `PREDICATE R92-PROBE pass`.
Observed (verbatim, abridged to head/tail):
```
TARGET executed_rows=35 member=llm-inference-batching-scheduler located=1 executed=0 cases=10 legs=60 mismatches=9 defects=13
DEFECT L5 case missing-plan-b1 predicted=PPPPPP observed=PPPPPP frozen=FPEEEE
  ... (9 such lines, one per non-full-pass case)
DEFECT L6 rerun rc=0 obs=10 want=10
DEFECT L7 ledger member=unexecuted round=None executed_total=35 cells_ok=False
DEFECT L8 probe pin unreadable vs bytes 13e41e91...
DEFECT L9 stamp fields mismatch (tool=d70210cb... table=89fab14b... ...)
PREDICATE R92-C1 fail
rc=1
```

### FORGE 2 — stamp-consistent (commit 13af5e91)
Same invented rows; TOOL_SHA=13e41e91…, CASE_TABLE_SHA=2249d5c0…, host strings copied live.
Observed: `TARGET ... mismatches=9 defects=12`; L5 x9, `L6 rerun rc=0 obs=10 want=10`, `L7 ledger ... cells_ok=False`, `L8 probe pin unreadable`; no L9 line; `PREDICATE R92-C1 fail` rc=1.

### FORGE 2b — stamp-consistent plus ledger flip plus tool pin (commit d946b209)
Ledger: member status executed, round 92 (cells recomputed by the counter's L7 rule: crypto-credential 4, file-artifact 27, filesystem-metadata 4, serialization-schema 5; executed total 36). Pins: `plans/round92_bs_probe.py` sha entry added.
Observed:
```
TARGET executed_rows=36 member=llm-inference-batching-scheduler located=1 executed=0 cases=10 legs=60 mismatches=9 defects=10
DEFECT L5 case ... (x9)
DEFECT L6 rerun rc=0 obs=10 want=10
PREDICATE R92-C1 fail
rc=1
```
Only L5 and L6 object. L7 and L8 and L9 pass when the forger flips the ledger and pins the tool in the same commit.

### FORGE 3 — round-91 receipt bytes as r92 receipt (commit e2b4e5fd)
Observed: `DEFECT L2 subject/input sha mismatch (... receipt=0c24195f...)`, `DEFECT L5 case full-pass predicted=PP observed=PP frozen=PPPPPP`, `DEFECT L5 receipt names unknown case missing-script` (x9 other ids), `L6 rerun rc=0 obs=10 want=10`, `L7 ... cells_ok=False`, `L8 probe pin unreadable`, `L9 stamp fields mismatch`, `PREDICATE R92-C1 fail` rc=1. The brief's "MEMBER/PREDICATE/CASE ids mismatch" is confirmed on the CASE ids; PREDICATE is not parsed by the counter at all (noted in Finding C1-d below).

### FORGE 4 — cheating probe (commit 6e9642a8) — PASSES
Probe `plans/round92_bs_probe.py` with one line changed: `observed, classes = run_case(...)` replaced by `observed, classes = case["predicted"], "cheat=ok"`. Stamp and receipt produced by running that cheat probe (TOOL_SHA 91467986…, CASE_TABLE_SHA 2249d5c0…, LANE_TIP=B2). Ledger flipped; `counter-pins-r91.json` entry for the probe set to the cheat sha. No grader is executed anywhere.
Observed:
```
TARGET executed_rows=36 member=llm-inference-batching-scheduler located=1 executed=1 cases=10 legs=60 mismatches=0 defects=0
PREDICATE R92-C1 pass
rc=0
```
Why it passes: L5 compares receipt to the frozen table (cheat copies the table); L6 reruns the same cheat probe, so reruns agree; L8 and L9 are self-consistency checks against bytes in the same commit. Nothing in the counter executes or independently checks the grader. This is the disclosed in-tree-pin residual class (L0 kengaku round-91) extended to the replay itself: the counter's L6 is not an oracle.

### FORGE 5a / 5b — pin ledger (commits 34d99cdc, 97d537fa)
Tamper: `selftest_ok = rc == 0` → `selftest_ok = True` in `plans/round91_counter_pin.py` (tamper sha 816c0166…). Run from a copy whose bytes equal the committed tamper (so SELF-PIN sees the same file).
5a (pin untouched) observed:
```
DEFECT PIN-MISMATCH bytes plans/round91_counter_pin.py
PINS checked=17 matched=16 mismatched=1
PREDICATE R91-C2 fail
rc=1
```
5b (pin rewritten in the same commit) observed:
```
SELFTEST-DETAIL cases=9 red-green-ok=9
SELFTEST cases=9 red-green-ok=9
PINS checked=17 matched=17 mismatched=0
PREDICATE R91-C2 pass
rc=0
```
5b is the disclosed residual. It is not a new finding, and the claim does not close it.

### FORGE 6a / 6b — conformance counter body (run at BASE 4ba56182)
Controls: real B2 counter at BASE: `M7 FAIL base-rc=1 base-L5=10 tip-rc=1 tip-pass=False`, `M12 FAIL`, `M9 FAIL base-flag-present=True base-table-absent=True tip-flag-absent=False ...`, `PREDICATE R92-C2 fail`, rc=1.
6a (literal: M7 accepts green rc in (0,2)): identical verdicts, `PREDICATE R92-C2 fail`, rc=1. Answer to the brief's question: **no**. Base leg is rc 1, and the M7 verdict also requires the `PREDICATE R91-C1 pass` string, which BASE does not print.
6b (6a plus `passed = all(...)` replaced by `passed = True`): output still shows `M7-CASE-PARSER FAIL`, `M12-HOST-PROBE-GUARD FAIL`, `M9-SELFTEST-ESCAPE FAIL`, then `PREDICATE R92-C2 pass`, rc=0. The counter file is not pinned: `round92_c2_conformance.py` is absent from `plans/counter-pins-r91.json` at B2, and the counter reads its own verdict line from the caller's working tree. Any one-line edit to the verdict line passes at BASE.

### FORGE 7–15 — gate fixtures (verdicts from `evaluate()`; exact rows in the wave evidence above)
- 7 (a): `{"id":"CL-A","status":"closed","close":"closed by inspection","check":"true","override_reason":"inspection", base fields}` → `DEFECT closed-check-vacuous CL-A 'true'`. Red as required.
- 8 (a2): base `OLD-1` open, opened 39, `check:"grep -q anchor notes.md"`; `OVR-V` closed, `supersedes:"OLD-1"`, `check:"true"`, `override_reason:"inspection"`. Output: `freeze=admitted pending=0 ... overrides=1 checks_run=2`, `PREDICATE R92-C3 pass`. Cause: `is_override` branch never calls `vacuous_check`, and the anchoring test is `if ovr_tokens and ...`, so an override with no path token is exempt from both rules.
- 9 (a3): closed row `check:"true # grep"` → `freeze=admitted checks_run=1`, pass. Cause: `vacuous_check` treats any FILE_OP word (here `grep` in a comment) as non-vacuous.
- 10 (a4): closed row `check:"true 1.0"` → pass. Cause: `PATH_TOKEN` matches the decimal `1.0`.
- 11 (a5): closed row, `check: null`, close "closed by inspection" → `freeze=admitted checks_run=0`, pass. Cause: `evaluate()` does `if not command: continue` before any vacuity test.
- 12 (b): `OVR-B` closed, supersedes `OLD-1`, `check:"cat ghost/absent.md"`, close "closed", override_reason set → `DEFECT override-unanchored OLD-1`, `DEFECT check-failed OLD-1 rc=1`, `PREDICATE R92-C3 fail`. Red as required.
- 13 (c): blocked `BL-1`, owner `nobody`, fixture conf without nobody → `DEFECT owner-not-a-lane BL-1 nobody`, `unowned_blocked=1`, red. As required.
- 14 (c2, extra): same row, `SHOKUNIN_ROOT` at `root-nobody` (conf lists nobody) → `freeze=admitted unowned_blocked=0`, pass. The lane-id trust root is an environment variable, not the lane's committed conf.
- 15 (d): `OLD-1` open opened 39; `OLD-1-r1` open supersedes OLD-1; `OLD-1-r2` open supersedes r1. Output `freeze=refused oldest_pending_round=39 pending=1 ... PREDICATE R92-C3 fail`, rc=1. The verdict matches. The output does not name the pending id or the chain-end, so the "naming the chain-end" expectation is unmet. Control (`OLD-1-r2` closed with a passing check): `freeze=admitted`, `PREDICATE R92-C3 pass`.

### FORGE 16 — the frozen C3 command never returns (not a forgery; unmodified B2)
Command: `SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin python3 -I -B plans/round92_burndown.py --lane clone --rev HEAD --work <dir> --freeze-round 92`, timeout 120 s → `rc=124`, 950 nested `predicate-selftest` directories, still growing. A separate run hit a 600 s `TimeoutExpired` in a child; `find` found 7223 nested dirs and maximum nesting depth 103.
Cause: `main()` calls `selftest()` on the default path. `gate()` writes the child marker, and the child's `in_child_mode()` requires the parent's argv to contain `--selftest`. The default invocation's argv does not contain it, so every child runs its own battery, recursively. `--selftest` mode (top-level argv contains `--selftest`) completes: `SELFTEST-DETAIL cases=10 red-green-ok=10`, rc=0.

### FORGE 17 — battery skip by marker spoof (extra)
Copy of the B2 gate with the `chain-two-level` expectation changed from 0 to 1 (a red case).
- `--selftest`: `SELFTEST chain-two-level rc=0 want=1 text-ok=True ok=False`, rc=1.
- Default path via wrapper `python3 -I -B -c "<wrapper>" <gate> <lane> <work>`, where the wrapper writes `<work>/.predicate-selftest-child` = `"<its pid> <sha256(/proc/self/cmdline)[:16]>"`, and its `-c` text contains `round92_burndown.py --selftest`. Output:
```
freeze=admitted ... pending=0 ...
PREDICATE R92-C3 pass
PREDICATE R92-C3-BATTERY pass
rc=0
```
No SELFTEST line appears, so the red case did not run and could not fail the predicate.

## Findings (severity by the brief's rule: a forgery that passes is High)

- **H1 (FORGE 8, 9, 10, 11): closed-row vacuity is bypassable.** Override checks skip `vacuous_check` entirely, and zero-path-token overrides skip the anchor rule. Comment-, number-, and check-less closed rows pass. Violates M10 as frozen (`not true/:/exit 0 and carrying a path token or a file operator`; "override row's check must share at least one path token"). Recipe: the row JSON given under FORGE 8 / 9 / 10 / 11.
- **H2 (FORGE 16): the frozen C3 command does not terminate.** The M8 selftest recursion means the default predicate run never returns a verdict. C3 cannot pass its frozen predicate at any rev, and the run consumes unbounded processes and disk.
- **H3 (FORGE 17): the M8 battery is skippable by a parent-argv spoof.** A red selftest case does not fail the predicate when the caller writes the child marker and its argv carries the right text. The brief's "no skip flag" holds only in the literal CLI sense.
- **H4 (FORGE 6b): the conformance counter's verdict is unpinned.** Single-line edit to the verdict prints `PREDICATE R92-C2 pass` at BASE. No `round92_*` file is pinned in `counter-pins-r91.json` at B2 (round92_bs_probe.py, round92_c1_replay.py, round92_c2_conformance.py, round92_burndown.py all absent). The literal M7-rc2 edit (6a) does not pass.
- **H5 (FORGE 4): C1 passes for a probe that never runs the grader** when probe, receipt, ledger and pin are rewritten in one commit. Same residual class as the disclosed in-tree pin (L0 kengaku round-91), but C1's L6 rerun is self-referential, so the replay claim has no independent oracle. Not closed by this round.
- **H6 (FORGE 14): lane-id trust root is `SHOKUNIN_ROOT`.** A blocked owner passes when the env var points at a conf listing that owner. Design-level; per the rule it is a pass.
- **Known residual, not new (FORGE 5b):** counter plus pin rewritten in one commit passes `round91_counter_pin.py`.

## Lower-severity observations (not forgeries; verified by code reading unless marked)

- L-a (FORGE 15): gate prints counts for pending rows but not their ids; the brief's "naming the chain-end" is not met.
- L-b (C1 L5): `l5` checks count and per-id match, but not id uniqueness. Ten copies of one passing id satisfy L5. L6 (rerun equality) is the only guard. [INFERENCE from code, not exercised.]
- L-c (C1 L6): `subprocess.run(..., timeout=900)` for the rerun is unguarded; a timeout raises `TimeoutExpired` to the top level, giving a traceback, rc 1, and no PREDICATE line. Same class as M12. [INFERENCE from code, not exercised.]
- L-d (FORGE 1–3 output): the counter does not parse the `PREDICATE` line of a receipt; the brief's "PREDICATE id mismatches" is not a counter check.
- L-e (FORGE 4 receipt): the cheat probe's stamp recorded `WORKTREE dirty` when it ran in the scratch clone; `git -C <clone> status --porcelain` returned empty when checked later in the run. The cause was not established; no process of mine is known to have written into the clone working tree. My FORGE 1–3 receipts were typed by hand with `WORKTREE clean`, not produced by the probe.
- L-f (C2 M9 pin): round92 counter bytes are not in the pin ledger, so the frozen M9 "PINS checked=17" counts only the round-91 pin set.

## Cleanup

Scratch dir `/fast/scratch/hyaku/kengaku-r92/SentinelForge/` (clone, fixtures, gate work dirs, forgery indices) is removed before yield. The forgery commits exist only in the scratch clone's object store and are discarded with it. Nothing pushed; nothing written to the lane's tracked files; nothing written to the fleet root.
