# R90-C2 control battery — ExecC2Battery

Seat: ExecC2Battery (leaf, executor). Item: R90-C2 control battery in scratch clones only.
Rev under test: B `664435cfcb9419c4e8ac7828a55aec11a1f36ec4`. BASE: `dcdd494ef4b4a6c0ae349ecb597527124ee54f91`.
Full transcript with every rc and defect line: `controls.txt` (same directory).

## Verdict per control

| # | Control | Expected | Observed | Result |
|---|---------|----------|----------|--------|
| 1 | Positive at B | rc0, PINS 7/7/0, record matched, pass | rc0, `PINS checked=7 matched=7 mismatched=0`, `RECORD-TABLE blob=163f284316141a83 matched`, `PREDICATE R90-C2 pass` | as predicted |
| 2a | One byte of real `round90_c1_replay.py` mutated at c2 | rc1 `PIN-MISMATCH bytes` | rc1, `PIN-MISMATCH bytes plans/round90_c1_replay.py got=83305219ab815ff6 want=611226af23d5831c`; pristine c1 rc0 | as predicted |
| 2b | Counter restored; one byte of `round89-q66-records.json` mutated | rc1 record-table mismatch | rc1, `RECORD-TABLE blob=4cad67dcc1b1e260 != pinned 163f284316141a83`; restored c1 rc0 | as predicted |
| 3a | Ledger names only a path committed nowhere | rc1 `PIN-MISMATCH absent`, never skip | rc1, `PIN-MISMATCH absent plans/round90-ghost-counter.py` plus six missing-entry lines | as predicted |
| 3b | Six real pins + one ghost | rc1, only ghost line red | rc1, only the ghost line is a bytes/absence defect | as predicted |
| 3c | Checker at BASE | nonzero, no pass line, rc2 SETUP | rc2, `DEFECT SETUP unreadable plans/counter-pins-r90.json at dcdd494ef4b4`, `PREDICATE R90-C2 could-not-evaluate`, no PINS line | fail-closed confirmed; frozen-text mispredict recorded (see F1) |
| 4a | Ledger names 1 of 6 | one missing-entry per missing path | rc1, 5 missing-entry lines for 5 missing paths | as predicted |
| 4b | Ledger names 5 of 6 (omits counter) | one missing-entry line | rc1, exactly `pin-file-missing-entry plans/round90_c1_replay.py` | as predicted |
| 5 | One hex digit of counter pin changed, bytes unchanged | rc1 `PIN-MISMATCH bytes` for that path | rc1, `PIN-MISMATCH bytes plans/round90_c1_replay.py got=611226af… want=011226af…` | as predicted |
| 6 | Separation: C1 ledger flip without receipt | C2 verdict unchanged | rc0, pass, identical to unmodified B (rc0, 7/7/0) | unchanged, as predicted |
| 7 | `--selftest` at B | rc0, 5/5 red-green ok | rc0, `SELFTEST cases=5 red-green-ok=5` | as predicted |

No control that could fail stayed green. Every red control exited nonzero with the expected defect line. Every green control had an unmodified-bytes twin that was also green.

## Prechecks (read-only, recorded in controls.txt §0)

- Receipt `corpus/evidence/round90/merge-diff-probe.txt`: absent at B (`git cat-file -e` rc=128). Nothing to delete; the separation control therefore flips the grader-ledger row without creating a receipt, rather than deleting one.
- Grader-population ledger, member `merge-diff-arc-agi-task`: `status=unexecuted`, `reason=unattempted` at B. Unflipped, as the claim requires at B.
- Pinned bytes at B recompute to the ledger values for all six paths; record-table blob at B equals the pinned blob.
- Pin ledger `plans/counter-pins-r90.json`: absent at BASE (ls-tree empty), present at B.

## Defects and findings

**F1 — frozen-text mispredict (recorded, not repaired).** Claims predicted BASE exits 1 with `PIN-MISMATCH absent` for each new path and four `PIN-OK` lines. Observed: rc2 `could-not-evaluate` from a `DEFECT SETUP unreadable` line, because the pin ledger itself does not exist at BASE, so no per-path check runs. The rc2 is nonzero with no pass line, so it is fail-closed; the prediction text is what is wrong.

**F2 — `PIN-OK` has no producer.** The checker never prints a `PIN-OK` line for any path, passing or failing. The claim's BASE prediction ("printed `PIN-OK`") describes output the instrument does not emit. Frozen text; not repaired.

**F3 — "external" overstates the anchor.** The checker's own header discloses the residual, but I measured the consequence: the pin values, the set of required paths (`EXPECTED_PINS`), and the checker itself all live in the same tree. A single commit that rewrites `plans/counter-pins-r90.json` and the checker's `EXPECTED_PINS` constant would pass with rc0. Only the record-table blob has an anchor that is out of the rewritten tree, and only because the checker's `RECORD_BLOB` constant is also in-tree; so even that is one-commit rewritable. The checker is not in the pinned set at all, so editing it to skip checks is not caught by any pin. I did not test the one-commit rewrite (it is the disclosed residual, and running it would be an adversarial edit against the lane, which is out of my scope). The claim's word "external" should read "in-tree, outside the pinned bytes".

**F4 — cosmetic count.** `PINS checked=N` equals `len(pins)+1` because the record table is counted as a pin. The claim's wording "PINS checked=7" for six paths plus the record table is consistent with this, so not a defect against the frozen text, but a reader could misread it.

**F5 — selftest clean-green uses stubs.** Selftest T4 proves the green path with synthetic file contents. The real-bytes proof of green is control 1 and the pristine twins in 2a and 2b.

## Instruments, installs, host

- No tools installed or upgraded. No pacman, no sysctl, no write to `~/.local/bin` or any PATH directory.
- No write to the lane's `plans/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, or `.scratch/`.
- All fixtures were `git init` in fresh directories under `$S`; each fixture's `rev-parse --show-toplevel` was asserted equal to its own directory before its first commit. Author `t <t@t>`.
- Mutations were single-byte XOR `0x01` at offset 0 of the target file.
- Scratch `$S` removed at the end of this seat (receipts copied into this directory first).

## Checks the main agent should run

- `python3 plans/round90_counter_pin.py --lane . --rev 664435cfcb9419c4e8ac7828a55aec11a1f36ec4` → expect rc0, `PREDICATE R90-C2 pass`.
- `python3 plans/round90_counter_pin.py --lane . --selftest --work <tmpdir>` at B → expect rc0, 5/5.
- `python3 plans/round90_counter_pin.py --lane . --rev dcdd494ef4b4a6c0ae349ecb597527124ee54f91` → expect rc2 (see F1).

Report: .ufo/waves/round-90/w1/ExecC2Battery/report.md and .ufo/waves/round-90/w1/ExecC2Battery/controls.txt
