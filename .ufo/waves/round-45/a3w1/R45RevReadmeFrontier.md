# R45RevReadmeFrontier — corpus/README.md round-45 edits review

Lane tip measured: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`master`).
Baseline for the diff: `c2ff211` (last round-44 commit touching corpus/README.md; `git log --follow` confirms the two round-45 commits `7d062c0` and `d4c0cdf` are the only later edits).
All checks are `git`/text reads on the lane at that tip; nothing that writes files was run, so no envelope was needed (host-safety rule applies to fixture builds/counters/probes, none executed here).

## Check 1 — Index row for the new entry

README.md:78:
`| knowledge/tb2-password-recovery-grader.md | An eleventh Terminal-Bench 2.0 task grader read and executed, and the second exemplar of the F1 constant-compare family after feal-linear-cryptanalysis: … | Pinned at terminal-bench-2 2fd12b88: S149, S150, S151, S152, S153, S154, S155, S156; captures + SHA256SUMS in evidence/round45/tb2-password-recovery/; receipt evidence/round45/password-recovery-probe.txt; executed under bwrap … |`

- Convention match: same three-column shape as rows 68–77 (path, one-sentence summary with probe stats, third cell = pin + SOURCES rows + captures + receipt). Appended at the end of the knowledge block (line 78, immediately after `tb2-feal-linear-cryptanalysis-grader.md`), matching the block's chronological append order.
- Target exists: `ls -la corpus/knowledge/tb2-password-recovery-grader.md` → `18861 Oct 26 23:42` bytes; `wc -l` → 208 lines.
- Every path inside the row resolves: `ls` confirms `corpus/evidence/round45/tb2-password-recovery/` (10 entries incl. SHA256SUMS) and `corpus/evidence/round45/password-recovery-probe.txt`.
- SOURCES rows cited (S149–S156) exist: `grep -nE '^\| S15[0-6]' corpus/SOURCES.md` → 8 rows at lines 164–171, all `password-recovery` at `2fd12b88`. PASS.

## Check 2 — §Frontier / coverage TB2 clause reads 11 of 89 with the task named

- Coverage bullet README.md:306: `Terminal-Bench 2.0 task grader (eleventh task, second F1 constant-compare exemplar): covered at source-code depth and executed offline (round 45, 2026-10-26) — knowledge/tb2-password-recovery-grader.md; S149–S156; probe plans/password_recovery_probe.py, receipt evidence/round45/password-recovery-probe.txt. An eleventh instance of the same ground (11 of the 89 TB2 task graders; not breadth, and no quality claim).` → "11 of the 89" ✓.
- §Frontier discharge sub-bullet README.md:430: `*Partly discharged round 45 (2026-10-26):* … reads and executes an eleventh Terminal-Bench 2.0 task's scoring code (password-recovery/tests/test_outputs.py @ 2fd12b88; S149–S156) … it stays open for the remaining TB2 task graders (11 of 89 read) …` → "11 of 89 read" ✓.
- Task named: `password-recovery` is named twice (filename `tb2-password-recovery-grader.md`, path `password-recovery/tests/test_outputs.py` in the discharge bullet). NOTE (minor, convention deviation): coverage bullets for tasks 2,3,4,5,6,7,8,9 (lines 297–303, 305) end `on \`taskname\` only:`; the new eleventh bullet and the round-44 tenth bullet (line 304) do not carry that phrase. The task is still named via the path, so not scored as a defect — flagged for the L1.
- Frozen-count convention verified: each prior discharge bullet pins the count at its own landing (lines for r37–r44 show `3 of 89 read` … `10 of 89 read`, `grep -o '[0-9]* of 89 read'` → one each). The r45 bullet correctly says `11 of 89 read`. Older bullets keeping their stale-at-landing numbers is the established pattern, not a defect. PASS (with the convention note above).

## Check 3 — Knowledge count cells vs `find corpus/knowledge -name '*.md' | wc -l`

- Measured count: `find … | wc -l` → **52**.
- README main index holds 50 `| \`knowledge/…\`` rows (lines 29–78); the two deferred entries `webarena-task-spec-audit.md` and `webarena-config-projection.md` live in their own admitted-knowledge tables (lines 504, 533) per the deferred-index statements at lines 513/542. `grep -o 'knowledge/[a-z0-9._-]*\.md' README | sort -u` = 52 unique names; `comm` against the `find` list → **zero unmentioned files, zero phantom mentions** (`/fast` scratch comparison, receipts below). 50 + 2 = 52 agrees with `find`. PASS.
- No explicit knowledge-total number cell exists in the README (the `62/62` parity string from commit `02287ee` was a lessons parity claim, not knowledge).

## Check 4 — No older line clobbered

`git diff --numstat c2ff211..master -- corpus/README.md` → `12  0` (twelve insertions, zero deletions across all of round 45's README edits). Every hunk verified as an add-only `@@` block: the knowledge row, the coverage bullet, the discharge sub-bullet, the lessons row, and the Round-45 evidence block. PASS.

## Defects found (in the round-45 additions)

D1 (major) — README.md:635 cites a phantom path and a wrong count, copied from the round-44 template: `` `../plans/battery45/` — the 33 honest fixtures ``. Measured: `ls plans/battery45/` → `No such file or directory`; `plans/round45_c1_verify.py:64` → `HONEST_RELS = ("plans/battery42", "plans/battery43", "plans/battery44")` and the C1 claim is `HONEST fixtures=104`. The honest set is the three prior batteries (104 fixtures), not a `battery45` of 33. Also on line 634: phantom `` `evidence/round45/frozen-digests.txt` `` — `ls corpus/evidence/round45/` shows no such file (7 txt receipts: c1-counter-run, counter-a-run, counter-b-run, gate-call, password-recovery-dry-cases-freeze, password-recovery-probe, probe-run-envelope); `grep frozen-digests plans/round-45-claims.md` → no match, so the claims file does not call for it either.

D2 (minor) — README.md:635 misspells four of the ten `plans/refusals45/` module names and omits `f2_deep.py`. Listed vs actual (`ls plans/refusals45/`): `f1_truncated_git.py`→`f1_gitfile.py`, `f4_fifos.py`→`f4_fifo.py`, `f6_move.py`→`f6_above.py`, `f8_worktree.py`→`f8_worktreecfg.py`, `f9_describe.py`→`f9_nodescribe.py`; `f2_deep.py` absent from the list; only `f3_abbrev`, `f5_alternates`, `f7_commondir`, `f10_laneinclude` match. The list also never states the module count is 10 (claim: `REFUSALS total=10`).

D3 (minor) — Two landed round-45 receipts are unindexed by the evidence block: `evidence/round45/c1-counter-run.txt` (the C1 counter run itself, head confirms `python3 plans/round45_c1_verify.py --lane .` ending `PREDICATE C1 pass`) and `evidence/round45/probe-run-envelope.txt` (the envelope-wrapped probe receipt that pairs with `password-recovery-probe.txt`). The block indexes 5 files + a phantom instead of the real 7 receipts + capture dir.

D4 (pre-existing, carried — noted not counted) — `corpus/lessons/round-44-verifier-spotcheck.md` (landed `9d5f971`) has no index row: 65 lesson files vs 64 `| \`lessons/\`` rows; every other `round-*-verifier-spotcheck.md` is indexed (rows for r24–r43). Not introduced by round-45 edits (zero deletions prove the diff is pure addition), but the convention gap persists.

Everything else verified clean: 9 pinned files + SHA256SUMS claim at line 632 matches `ls` (10 entries, flat names after the documented freeze amendment); `rows S149–S156 pin eight of them (gitignore is a capture, not a row)` matches SOURCES lines 164–171 exactly (8 rows); `16 frozen cases`, `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0` match the receipt head at `corpus/evidence/round45/password-recovery-probe.txt`/`probe-run-envelope.txt`; frozen claims/counters ancestor check `git merge-base --is-ancestor 52d7486a… master` → ANCESTOR, and claims/counter files unchanged in that range except the documented 2-line claims amendment + c2 re-pin (outside this seat's README scope, noted for the C2 reviewer).

Receipts (also under `.ufo/waves/round-45/a3w1/R45RevReadmeFrontier/`): `files.txt` (52 find names), `mentioned.txt` (52 README names), `lessons_files.txt`, `lessons_mentioned.txt`.

Count: D1 (two phantom/wrong assertions in one line: `battery45`/`33` + `frozen-digests.txt`) + D2 (refusals45 name list) + D3 (unindexed receipts) = 3 README defects attributable to the round-45 edits.

VERDICT: readme-defects-3
