# C2ChecksR81 — scoped handoff

Axes: coverage and calibration; this seat addresses calibration. No tool installs. No lane implementation files, registry rows, counters, or frozen plans edited. Deliverable: `.ufo/waves/round-81/w1/C2ChecksR81.py` (cwd-relative u1…u6 and --all). L1 requested immediate wrap-up before full completion.

## Important limitations — not a completed frozen-table implementation

The integrated `plans/round81_c2_checks.py` already existed when inspected. The seat deliverable independently reproduces its principal content checks, but **must not be treated as full frozen-table enforcement**:

- Frozen U1 says `lines 3-12`; the existing integrated checker and the delivered checker require `lines 2-12`, matching the currently registered close description. This is a discrepancy, not permission to amend the frozen predicate. L1 must resolve the implementation to the frozen requirement.
- U5 currently checks gate row names, `--lane .`, and `--selftest`, but not actual entry script names, pinned-value paths, or owner cells. It also requires two round-81 gate rows beyond the frozen two round-80 gates. These checks are insufficient and over-scoped relative to the frozen U5 table.
- U2 requires tokens anywhere in SCORECARD, not a dated, coherent erratum block.
- U1's superseded-value check can be satisfied by the old S258 row itself; it does not prove the lesson names the superseded text.
- U3 uses `git show` and a Python row regex rather than invoking the literal frozen `grep -cE` command. A git-less archive tree cannot support its historical re-derivation; this follows from the implementation and was not separately executed.
- No hand-built green fixture from the complete frozen table was finished. Green observations below are on the live lane; the integrated selftest builds its own smaller green fixture.
- Base-reverted red tests below change several repair files together. They demonstrate each subcommand returns nonzero on that tree, not independent one-file sensitivity. No claim of full counter sensitivity verification is made.

## Retained execution evidence

Commands executed from the lane unless otherwise stated. The live tip moved during work.

### Integrated checker

Command: `python3 plans/round81_c2_checks.py --all` at `e83963f895e42992573ff47c769d1ac86cb15363`:

```text
OK u1
OK u2
OK u3
OK u4
OK u5
OK u6
rc_all=0
```

Command: `python3 plans/round81_c2_checks.py --selftest --work /fast/scratch/hyaku/kengaku-r81/C2ChecksR81/st`:

```text
SELFTEST cases=12 red=6 failures=0
rc_selftest=0
```

The integrated selftest source builds a green fixture and deletes one repair file for each red arm. Its fixture's git commits did not contain an explicit pre-commit toplevel assertion; invoking that fixture builder was a process-rule miss by this seat.

### Red tree

Created one shared clone:

`git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r81/C2ChecksR81/clone`

Asserted `git rev-parse --show-toplevel` equalled that clone directory. Replaced SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md, and SKILL.md with `git show 4e833e9f:<path>` bytes in that clone; deleted the new census receipt, red-before receipt, and round-81 lesson there. No commits made by this seat.

Command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round81_c2_checks.py --lane /fast/scratch/hyaku/kengaku-r81/C2ChecksR81/clone --all`:

```text
FAIL u1 SOURCES: no row whose teaches opens 'supersedes S258 —'
FAIL u1 LESSON: corpus/lessons/round-81.md does not carry R80-U1
FAIL u2 SCORECARD: no erratum id (R80-U2)
FAIL u2 SCORECARD: no clean revision (e985e56a)
FAIL u3 census-rows receipt absent or unmarked
FAIL u4 r80-u4-red-before receipt absent or unmarked
FAIL u5 SKILL: registry block does not carry R80-U5
FAIL u5 SKILL: no registry row for round80-c1-located-replay
FAIL u5 SKILL: no registry row for round80-c2-spotcheck-debt
FAIL u5 SKILL: no registry row for round81-c1-new-members
FAIL u5 SKILL: no registry row for round81-c2-spotcheck-debt
FAIL u6 LESSON: no R80-U6 correction
FAIL u6 LESSON: cites 0/6 round-80 receipts
rc_red_integrated=1
```

### Seat deliverable

Command: `python3 .ufo/waves/round-81/w1/C2ChecksR81.py --all` at live tip `03affddfd9b4e976cb1c3f09336e11ee2dc33621`:

```text
OK u1
OK u2
OK u3
OK u4
OK u5
OK u6
rc_green=0
```

First red attempt used the relative script path after changing into the clone and failed for the wrong reason:

```text
python3: can't open file '/fast/scratch/hyaku/kengaku-r81/C2ChecksR81/clone/.ufo/waves/round-81/w1/C2ChecksR81.py': [Errno 2] No such file or directory
rc_red=2
```

All six subcommand attempts with that incorrect relative path likewise returned 2. Corrected command, cwd the red clone:

`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-81/w1/C2ChecksR81.py --all`

```text
FAIL u1 no row whose teaches opens 'supersedes S258 —'
FAIL u1 lesson does not carry R80-U1
FAIL u2 SCORECARD lacks R80-U2
FAIL u2 SCORECARD lacks e985e56a
FAIL u3 census-rows.txt absent or unmarked
FAIL u4 r80-u4-red-before.txt absent or unmarked
FAIL u5 SKILL registry block does not carry R80-U5
FAIL u5 no registry row for round80-c1-located-replay
FAIL u5 no registry row for round80-c2-spotcheck-debt
FAIL u5 no registry row for round81-c1-new-members
FAIL u5 no registry row for round81-c2-spotcheck-debt
FAIL u6 lesson has no R80-U6 correction
FAIL u6 lesson cites 0/6 round-80 receipts
rc_red=1
```

Then each `python3 <absolute-seat-script> uN` in that clone returned:

```text
u1 rc=1
u2 rc=1
u3 rc=1
u4 rc=1
u5 rc=1
u6 rc=1
```

## Row command recommendations

Retain the existing repo-relative command spellings **only after tightening their implementation against the frozen table**. These are already registered; this seat registered nothing.

| id | exact one-line check | evidence_path | evidence_literal |
|---|---|---|---|
| R80-U1 | `python3 plans/round81_c2_checks.py u1` | `corpus/SOURCES.md` | `supersedes S258` |
| R80-U2 | `python3 plans/round81_c2_checks.py u2` | `SCORECARD.md` | `e985e56a` |
| R80-U3 | `python3 plans/round81_c2_checks.py u3` | `corpus/evidence/round81/census-rows.txt` | `rows=249` |
| R80-U4 | `python3 plans/round81_c2_checks.py u4` | `corpus/evidence/round81/r80-u4-red-before.txt` | `ModuleNotFoundError: No module named 'Bio'` |
| R80-U5 | `python3 plans/round81_c2_checks.py u5` | `SKILL.md` | `round80-c1-located-replay` |
| R80-U6 | `python3 plans/round81_c2_checks.py u6` | `corpus/lessons/round-81.md` | `R80-U6` |

## Remaining work for integrator

Tighten U1/U2/U5, finish per-id green fixtures from the frozen requirements, then exercise each evidence file's independent base reversion and all named paired artifacts. Run the frozen C2 counter after integration. Scratch is removed before terminal handoff. No full counter/build/lint/formatter was run by this seat.
