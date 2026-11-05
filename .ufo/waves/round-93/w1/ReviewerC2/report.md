# ReviewerC2 — R93-C2 review (freeze-integrity gate, calibration + capability)

Reviewed at T = 22972a317185216596b3dfe1c189e98d1eb86787 (measured tip), against the frozen claims at F = d8d0a4b849f3d031a6ad5525e18611a097e08bfe. Lane clone detached at T under /fast/scratch/hyaku/kengaku-r93/ReviewerC2/lane (removed before yield). Read-only lane access; no lane git mutation; no subagents.

## Verdict on the claim

**No finding flips the R93-C2 verdict at T.** I reproduced the frozen predicate: `python3 plans/round93_c2_counter.py --lane . --rev T --work DIR` prints `W1 pass`, `W2 pass`, `W3 pass`, `W4 pass`, `TARGET legs_passed=4 of 4`, `PREDICATE R93-C2 pass`, rc 0 (receipts/c2_counter_T.txt). The four forgeries all reach rc 1 through the same `--tool-file` path (receipts/forgery_*.counter.txt).

The gate has real defects that the claim does not disclose and the battery does not catch. They are routed to round 94 and do not change the T verdict: F..T contains zero merges and touches no instrument (below).

## Frozen-rule and table integrity (checked, clean)

- `git diff --stat F T -- plans/` touches only `plans/grader-population-ledger.json`; none of the nine tabled instruments changed (`git rev-list F..T -- <path>` = 0 for all nine; receipts/probe_last.txt).
- Claims blob identical at F and T (`git rev-parse` equal; probe_last.txt line 4).
- Every row of the frozen table matches the blob at F and at T (9/9, both checked with sha256 of `git cat-file`-equivalent `git show`).
- The claims file was added exactly once in history (`git log --diff-filter=AD`: only d8d0a4b8). W4's selector therefore resolves to F.
- F..T has 1 commit and 0 merges (probe_last.txt line 3).
- The in-path battery is not skippable from the CLI: `main` (plans/round93_freeze_integrity.py:254) calls `battery()` unconditionally, and `passed` requires `bat_ok == len(bat)` (line 273). Mutant M4 (battery replaced with `[]`) is killed by W3 (mutants.txt lines 37-48).

## Findings

### F1 — major (gate correctness) — merge-topology false `intact`; does NOT flip T
- Where: plans/round93_freeze_integrity.py:110 — `git rev-list f..t -- p` uses default history simplification. A merge whose result for `p` is TREESAME to parent 1 is followed only along parent 1, so the feature-branch commit that edited `p` is dropped from the count. Violates the docstring's rule (c), "no commit in --freeze..--rev touches the path" (lines 17-18).
- Reproduction (receipts/probe_merge.txt lines 1-7): feature branch from F edits `c.py`; main touches another file; merge resolves `c.py` back to the F bytes; `c.py` at T = table value. Default count = 0; `--full-history` count = 2. Gate output: `INSTRUMENT c.py ... touched=0 verdict=intact`, `PREDICATE freeze-integrity pass`, rc 0. This is the "edit later reverted is still a breach" case, which the gate says it catches.
- Test-net gap: no battery case or W2 fixture uses merge topology, so the gap is invisible. Mutant M8 (`--full-history`) passes every W leg (mutants.txt lines 85-96), so the suite cannot distinguish the fixed and broken gates.
- Verdict impact at T: none. `git rev-list --merges F..T` = 0 (probe_last.txt line 3).
- Route to round 94: fix candidate is `--full-history` (plus a battery case with this topology). Not repaired in round.

### F2 — major (gate correctness) — second `frozen-instruments` block silently ignored; does NOT flip T
- Where: plans/round93_freeze_integrity.py:72-76 — `parse_table` stops at the first closing fence (`break`, line 76) and returns; rows in any later block are never read, and no error is raised.
- Reproduction (receipts/probe_fixtures.txt lines 1-6): claims with two valid blocks; `b.py` (second block) edited after freeze → `FREEZE-INTEGRITY instruments=1 intact=1 broken=0`, rc 0. A second block that is malformed is also silently skipped (receipts/probe_parse_rename.txt, `second-block-malformed: rows=[('96257f25','c.py')]`).
- Verdict impact at T: none. The F claims file has exactly one opener (probe_last.txt line 1).
- Route to round 94: a second opener must be a could-not-evaluate (rc 2), and the battery needs a two-block case.

### F3 — minor (calibration) — duplicate rows inflate the W4 count
- Where: plans/round93_freeze_integrity.py:81 and 121 (no dedupe); plans/round93_c2_counter.py:39 (`MIN_SELF_INSTRUMENTS = 6`) and :172 (`s[0] >= MIN_SELF_INSTRUMENTS`).
- Reproduction (probe_fixtures.txt lines 7-19): one unchanged file listed eight times → `instruments=8 intact=8 broken=0`, rc 0. W4's "instruments >= 6" can be met by one file.
- Verdict impact at T: none (table has nine distinct paths). The threshold measures row count, not coverage.

### F4 — minor (test-net gap) — the battery and W2 do not cover the failure modes above
- A post-freeze edit to the claims table itself is not tested. The gate reads the table at F (plans/round93_freeze_integrity.py:93), which is correct. Mutant M5 (table read at T instead) survives every leg (mutants.txt lines 49-60: `PREDICATE R93-C2 pass`). The real gate handles the case correctly: a table rewritten to match edited bytes is `broken:rev-bytes-differ+touched-after-freeze=1` (probe_last.txt lines 6-8). The gap is in the test net, not in the verdict.
- Killed mutants (for the record): M1 no-touched-check (W2, W3, W4), M2 no-rev-bytes-check (battery + W3), M3 unscoped touched (W1-W4), M4 battery skipped (W3), M6 no-freeze-bytes-check (battery + W1/W4), M7 no-ancestor-check (battery + W3). Mutation harness: mutate.py; mutants.txt.

### F5 — minor (calibration framing) — W1 measures agreement with the lane's own past record
- Where: plans/round93_c2_counter.py:36-38 (R92 paths and the intact literal) and :128 (`s == (4, 1, 3)`).
- The constants are author-chosen: the round-92 spot-check lists ten edited files (corpus/lessons/round-92-verifier-spotcheck.md line 36); W1 uses a four-path subset. My independent recomputation confirms the split is real (receipts/probe_parse_rename.txt, W1 section: `same plans/round92_c1_replay.py`; `differ` for the other three). But W1 is a regression fixture against the lane's own historical self-assessment, and W2 and the forgeries are authored by the same lane. The claim text discloses this ("a count of the lane's own past self-assessment mismatches"). Calibration here is internal consistency, not an external oracle. Read the score accordingly.

### F6 — minor (W4 selector) — `commits[-1]` picks the oldest add, undocumented
- Where: plans/round93_c2_counter.py:166-169 — `git log --diff-filter=A` lists newest-first; `[-1]` is the oldest add, which is correct only if the first add is the freeze the round means.
- Reproduction (in-session fixture, delete then re-add of the claims file): selector list `[re-add, original]`, `[-1]` = original freeze, not the re-add. The gate then reports broken (conservative). At T there is one add, so no effect. The ordering is git default (commit-date), not ancestry; under date skew it is not guaranteed to be the topologically first add.
- Routing: document the choice or select by ancestry; no effect at T.

### F7 — info — parser limits (honest failures, not false passes)
- Path containing a space: `ROW` (plans/round93_freeze_integrity.py:41, `\S+`) → rc 2 `could-not-evaluate` (probe_parse_rename.txt, `path-with-space`). A round cannot freeze such a path; no false pass.
- Uppercase hex rejected (rc 2). CRLF and trailing spaces accepted (`crlf`, `trailing-spaces` rows parse).
- Duplicate rows with a wrong sha are evaluated per row (`duplicate-path-wrong-sha` gives two rows), so a lie in a duplicate is still caught.

### Checked, no defect
- Renames: instrument renamed a.py → b.py after freeze → `broken:absent-at-rev+touched-after-freeze=1`, rc 1 (probe_parse_rename.txt, rename section).
- Mode-only change (chmod +x, bytes identical): counted as touched → broken (probe_fixtures.txt, T6). Over-count, not a hole.
- Glob metacharacters in pathspec: `probe[1].py` gives the same count with default and `--literal-pathspecs` (2 and 2; probe_merge.txt lines 8-9). No under-count found.
- Ancestor and missing-table paths: battery B07/B08 present; M7 killed.
- Forgeries: always-broken (W1, W2, W4 fail), always-intact (W1, W2 fail), bytes-only (W2 fail on edit-then-revert), log-only (W2 fail on lying table). All rc 1.
- W1 expected values: hard-coded constants, not derived from the tool; independent sha256 of `git cat-file blob` at B2 and B9 reproduces 1 same / 3 differ (F5).

## Residual risk and verification gaps

- Not verified: the C1 counter, the probe itself, and the ledger flip (out of scope for C2).
- Not verified: behaviour on a real merge-heavy history beyond the fixture.
- No tools installed or updated.
- Host sysctls were not touched.

## Receipts (receipts/ in this directory)

- c2_counter_T.txt — real counter at T, PREDICATE pass.
- forgery_*.py and forgery_*.counter.txt — the four forgeries through `--tool-file`, rc 1.
- probe_fixtures.sh / probe_fixtures.txt — table, duplicate, second-block, glob, path-with-space, mode probes.
- probe_merge.sh / probe_merge.txt — merge topology, `--full-history` comparison, literal vs glob, census.
- probe_last.sh / probe_last.txt — block count, CR/trailing, merges F..T, claims blob equality, selector list, post-freeze table rewrite.
- probe_parse_rename.sh / probe_parse_rename.txt — W1 independent recomputation, parse probes, rename probe.
- mutate.py / mutants.txt — eight gate mutants through the counter tool-file path.
- round93_freeze_integrity.T.py and round93_c2_counter.T.py — the instruments as read at T (sha256 18b01b42… and ac0e26a5…, matching the frozen table).

## Routed to round 94 (no repair in round)

1. F1: `--full-history` plus a merge-topology battery case (mutant M8 is the candidate).
2. F2: a second opener must be could-not-evaluate; add a two-block battery case.
3. F3: count distinct paths for the W4 threshold, or reject duplicates.
4. F4: add battery and W2 cases for a post-freeze table edit (catches M5) and for merge topology (catches M8 vs current).
5. F6: document or ancestry-select the W4 freeze.
