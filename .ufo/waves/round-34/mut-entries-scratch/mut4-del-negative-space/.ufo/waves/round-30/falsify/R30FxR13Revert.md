# R30 falsify — R13 separability: revert one claim, watch the other counters

Seat: `L1Kengaku30.R30FxR13Revert-3` (leaf). Date: 2026-10-25. Assignment: QUALITY.md R13
("one artifact, one claim"), read at `corpus/QUALITY.md` §Round-closure criteria.

Scope of this report: **the R13 revert experiment only.** It is **not** a source re-read and
**not** the complete-set review: it carries no `VERDICT:` line on purpose, and it supplies no
QUALITY Q10/Q13 second-seat support for
`corpus/knowledge/contamination-transparency-card.md` (named here only because the R13 population
I reverted is that entry's path set). Source truth is untouched by everything below.

## 1. What was tested, and the tree it binds to

- Origin lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `HEAD`, tip
  `363a4eb` (`git rev-parse HEAD`), working tree **dirty** — the build wave's bytes were landed
  uncommitted (16 porcelain entries at copy time).
- Scratch: `/tmp/r30fx-R13Revert/kengaku-shokunin` (full copy, `.git` included,
  `cp -a --reflink=auto`, 548 MB). The lane itself was never edited.
- Because the landing is uncommitted in the lane, the copy's working tree was committed once to
  give the counters a HEAD to judge (`check_d1`/`check_d4` read `HEAD:<path>`; see F6):
  - pre-landing base `BASE = 363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db` (lane tip),
  - landed tree `LANDED = c7b6f6d35f80f2ca203482778296e2c27468f90f`, tree sha
    `519f77a09547e8215528eff626057a92d8c3888d`.
  All numbers below bind to tree `519f77a`. The lane moved **after** the copy (see F8), so they do
  not silently claim to describe later bytes.
- One environment file was needed to make C1's census clause resolve: the fleet
  `shokunin.conf` was copied *into the scratch root* (`/tmp/r30fx-R13Revert/shokunin.conf`).
  Without it `adoption_check.py --census` prints `census=fail` on a copy whose SOURCES.md is
  perfectly valid (F6). Read-only source: `/home/vgpnk/Projects/shokunin/shokunin.conf`.
- Tools installed or upgraded: **none**.

## 2. The three counting commands (unchanged, as frozen in `plans/round-30-claims.md`)

| claim | counting command |
|---|---|
| C1 | `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` |
| C2 | `python3 plans/round30_defects.py --lane .` |
| C3 | `python3 plans/sources_adopt.py --selftest` (+ the pre-change control `--quote-file/--artifact` → argparse exit 2) |

## 3. Results table

`C1` column is the exact seven-field line; `C2` is the defect ledger; `C3` is the selftest line.

| run | C1 line | C1 exit | C2 | C2 exit | C3 | C3 exit |
|---|---|---|---|---|---|---|
| baseline (landed) | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` | 0 | `defects=0` (D1–D5 all `ok`) | 0 | `cases=14 failed=0` | 0 |
| **(a) C1 paths reverted** | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` | 1 | `defects=0` | 0 | `cases=14 failed=0` | 0 |
| **(b) C2 paths reverted** | *baseline line, unchanged* | 0 | `defects=4` (D1, D2, D3, D5) | 1 | `cases=14 failed=0` | 0 |
| (b2) D4 blob reverted too | *baseline line, unchanged* | 0 | `defects=1` (D4 only) | 1 | `cases=14 failed=0` | 0 |
| **(c) C3 path reverted** | *baseline line, unchanged* | 0 | `defects=0` | 0 | `cases=10 failed=0` (+ quote mode: argparse exit 2) | 0 |
| C1+C2 | `entries=0 …` | 1 | `defects=4` | 1 | `cases=14 failed=0` | 0 |
| C1+C3 | `entries=0 …` | 1 | `defects=0` | 0 | `cases=10 failed=0` | 0 |
| C2+C3 | *baseline line* | 0 | `defects=4` | 1 | `cases=10 failed=0` | 0 |
| C1+C2+C3 | `entries=0 …` | 1 | `defects=4` | 1 | `cases=10 failed=0` | 0 |

Every joint row is the exact union of the single-revert rows: **no interaction term** in any of the
four combinations. Each counter moves only with its own path set, and each revert is proved to have
bitten (the reverted claim's own counter moves; §4.4 shows the three frozen controls reproduce).

## 4. The runs, pasted

### 4.1 Baseline — all three green

```
## state: baseline-landed  (tip c7b6f6d, dirty=0)
C1_OUT: entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
C1_EXIT: 0
C2_OUT: ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
C2_EXIT: 0
C3_OUT: SELFTEST cases=14 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_OUT: QUOTE cap=25 problem=--artifact names no file or directory: /tmp/r30fx-R13Revert/artifact.txt
C3_QUOTEMODE_EXIT: 2
```

Note on that last line: at baseline the exit code 2 comes from the **unreadable-artifact** branch of
the new quote mode (the fixture files do not exist), *not* from argparse. In (c) the same exit code
2 comes from argparse (`unrecognized arguments`). **The exit code alone does not separate the
reverted tool from the landed tool**; the selftest case count and the message text do. Recorded so
the `quote_mode_exit=2` control is not read as a discriminator by itself.

### 4.2 (a) C1's paths reverted

Revert set = exactly C1's declared population: the entry, its six registry rows, and the three
README rows (index + coverage + frontier bullet).

```
$ git rm corpus/knowledge/contamination-transparency-card.md
$ git checkout 363a4eb -- corpus/SOURCES.md corpus/README.md
$ git status --porcelain
 M  corpus/README.md
 M  corpus/SOURCES.md
 D  corpus/knowledge/contamination-transparency-card.md
S081-S086 rows now: 0
registry rows: 82
```
(the entry is 170 lines / 15 779 bytes; registry 88 → 82 rows; README `-4/+1`)

```
## state: A-revert-C1  (tip c7b6f6d, dirty=3)
C1_OUT: entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
C1_EXIT: 1
C2_OUT: ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
C2_EXIT: 0
C3_OUT: SELFTEST cases=14 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_EXIT: 2
```

**C2 and C3 do not move.** C1's own line is byte-identical to the frozen control
`.ufo/waves/round-30/claims/control-nothing.txt`, checked mechanically:

```
C1 control bytes == reproduced line+exit: True
control repr: 'entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok\nexit=1\n'
```

### 4.3 (b) C2's paths reverted

Revert set = the D1 receipt, and HEAD's (pre-repair) bytes of `corpus/lessons/round-29.md` (D2, D3)
and `.ufo/waves/round-29/attempt2/adoption-expect.json` (D5). D4 is handled in §4.3.1.

```
$ git rm corpus/evidence/round29-attempt2/control-nothing.txt
$ git checkout 363a4eb -- corpus/lessons/round-29.md .ufo/waves/round-29/attempt2/adoption-expect.json
$ git status --porcelain
 M  .ufo/waves/round-29/attempt2/adoption-expect.json
 D  corpus/evidence/round29-attempt2/control-nothing.txt
 M  corpus/lessons/round-29.md
```

```
## state: B-revert-C2  (tip c7b6f6d, dirty=3)
C1_OUT: entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
C1_EXIT: 0
C2_OUT: DEFECT D1 receipt-at-cited-path: receipt absent at the cited path corpus/evidence/round29-attempt2/control-nothing.txt
DEFECT D2 kappa-sweep-scope: kappa line names no measured scope (corpus/knowledge/*.md)
DEFECT D3 s078-line75-word-count: lesson prices the line-75 quote at 9 words, actual 8 (registry says 8)
ok D4 uncommitted-wave-evidence: repaired
DEFECT D5 s091-usedby-asymmetry: adoption-expect.json records no S091 used-by asymmetry note and the entry cites no S091
defects=4
C2_EXIT: 1
C3_OUT: SELFTEST cases=14 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_EXIT: 2
```

**C1 and C3 do not move** — C1 prints the identical seven-field line and exits 0 (the restore check
before this run printed the same line: `entries=1 indexed=1 cited_rows=6 … census=ok`, `exit=0`).

#### 4.3.1 D4 — the assignment's premise is wrong: the addendum *can* be reverted in a copy

The task said "the D4 addendum commit cannot be reverted in a copy". It can: `check_d4` judges
`HEAD:<path>` (addendum marker present) plus a clean `git status` for that path, so restoring the
base blob and committing the clean state in scratch reproduces the defect.

```
$ git checkout 363a4eb -- .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md
$ git commit -m "scratch: revert D4 addendum bytes to pre-round-30 base"   # → edebce6
D4 path status: ''
addendum present in worktree: 0
```
```
## state: B2-revert-C2-D4  (tip edebce6, dirty=0)
C1_OUT: entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
C1_EXIT: 0
C2_OUT: ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 s091-usedby-asymmetry: repaired
defects=1
C2_EXIT: 1
C3_OUT: SELFTEST cases=14 failed=0
C3_SELFTEST_EXIT: 0
```
So D4 is separable too, and C1/C3 are inert to it.

### 4.4 (c) C3's path reverted

```
$ git checkout 363a4eb -- plans/sources_adopt.py
$ git status --porcelain
 M  plans/sources_adopt.py
```
```
## state: C-revert-C3  (tip c7b6f6d, dirty=1)
C1_OUT: entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
C1_EXIT: 0
C2_OUT: ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
C2_EXIT: 0
C3_OUT: SELFTEST cases=10 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_OUT: sources_adopt.py: error: unrecognized arguments: --quote-file /tmp/r30fx-R13Revert/rows.txt --artifact /tmp/r30fx-R13Revert/artifact.txt
C3_QUOTEMODE_EXIT: 2
```

**C1 and C2 do not move.** The reverted tool reproduces the frozen control
`.ufo/waves/round-30/claims/gate-before.txt` line for line, modulo the fixture path strings:

```
gate-before selftest line match: True | mine: SELFTEST cases=10 failed=0
gate-before selftest_exit=0 | mine: 0
gate-before quote_mode_exit=2 | mine: 2
gate-before quote err text: sources_adopt.py: error: unrecognized arguments: --quote-file /tmp/x --artifact /tmp/y
mine quote err text       : sources_adopt.py: error: unrecognized arguments: --quote-file /tmp/r30fx-R13Revert/rows.txt --artifact /tmp/r30fx-R13Revert/artifact.txt
```

### 4.5 Joint reverts (all four subsets of two-plus)

```
## reverted: C1 C2  (tip c7b6f6d, changed paths: 6)
C1_OUT: entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
C1_EXIT: 1
C2_OUT: DEFECT D1 receipt-at-cited-path: receipt absent at the cited path corpus/evidence/round29-attempt2/control-nothing.txt
DEFECT D2 kappa-sweep-scope: kappa line names no measured scope (corpus/knowledge/*.md)
DEFECT D3 s078-line75-word-count: lesson prices the line-75 quote at 9 words, actual 8 (registry says 8)
ok D4 uncommitted-wave-evidence: repaired
DEFECT D5 s091-usedby-asymmetry: adoption-expect.json records no S091 used-by asymmetry note and the entry cites no S091
defects=4
C2_EXIT: 1
C3_OUT: SELFTEST cases=14 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_EXIT: 2
```
```
## reverted: C1 C3  (tip c7b6f6d, changed paths: 4)
C1_OUT: entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
C1_EXIT: 1
C2_OUT: ok D1 … ok D5 (all repaired)
defects=0
C2_EXIT: 0
C3_OUT: SELFTEST cases=10 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_EXIT: 2
```
```
## reverted: C2 C3  (tip c7b6f6d, changed paths: 4)
C1_OUT: entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
C1_EXIT: 0
C2_OUT: DEFECT D1 … ok D4 … DEFECT D5
defects=4
C2_EXIT: 1
C3_OUT: SELFTEST cases=10 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_EXIT: 2
```
```
## reverted: C1 C2 C3  (tip c7b6f6d, changed paths: 7)
C1_OUT: entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
C1_EXIT: 1
C2_OUT: DEFECT D1 … defects=4
C2_EXIT: 1
C3_OUT: SELFTEST cases=10 failed=0
C3_SELFTEST_EXIT: 0
C3_QUOTEMODE_EXIT: 2
```

## 5. Probes beyond the assigned reverts

### 5.1 Expectation files (P1) — inert keys are inert, round-29's counter is untouched

```
=== P1a: round-29 expect at the landed tree
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
exit=0
=== P1b: round-29 expect with C2's S091 note reverted
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
exit=0
=== P1c: round-30 expect with its usedby_notes key removed
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
exit=0
```
P1b confirms C2's kill-rule requirement (`cited_rows=5` unchanged, `adoption_check.py` ignores
unknown JSON keys). P1c confirms the round-30 expect's `usedby_notes` record — which the round-30
build seats wrote into **C1's counter input** for C2's D5 — cannot move C1's count.

### 5.2 Content-gated coupling mutant (P2) — the one direction the revert test cannot see

C2's D2 re-derives its number over the live glob `corpus/knowledge/*.md`, i.e. **the directory C1
adds a file to**. At the landed content the entry holds zero `kappa` lines, so the revert moves
nothing. Append one such line to C1's entry and C2 flips, with C2's own paths untouched:

```
=== P2: one 'kappa' line appended to C1's entry (C2 paths untouched)
 M corpus/knowledge/contamination-transparency-card.md
ok D1 receipt-at-cited-path: repaired
DEFECT D2 kappa-sweep-scope: kappa sentence states 0 hits, corpus/knowledge/*.md holds 1
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=1
C2_exit=1
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
C1_exit=0
SELFTEST cases=14 failed=0
```
C1 and C3 stay green; only C2 moves, and it moves because of *C1's artifact content*. The mechanism
is visible in the lesson itself, which prices a round-30-wide file count (65 files at `2ff4b6f`,
66 at round 30, the extra file being `corpus/lessons/round-29-verifier-spotcheck.md`) —
`corpus/lessons/round-29.md:232-236`.

## 6. Findings

**F1 — the R13 revert test passes, cleanly and additively.** Reverting exactly one claim's paths
moves that claim's counter and nothing else: C1 `0 → 1` exit with `entries=0`, C2 `0 → 4` defects
(D1, D2, D3, D5; `+1` for D4 alone in §4.3.1), C3 `cases=14 → 10` plus the argparse control at
exit 2. All seven revert subsets are exactly additive. The cells are not merely "still passing":
C1's and C3's printed lines are byte-identical to the baseline, and C2's five `ok` lines are
byte-identical.

**F2 — R13's population clause fails for C2/D2 (currently inert).** "No claim's counting command
counts an artifact another claim of the same round creates" is not satisfied by
`plans/round30_defects.py:check_d2`: it counts lines matching `kappa` in `corpus/knowledge/*.md`, the
population C1 writes its entry into. §5.2 shows the counter moving on C1's artifact alone. The
independence is therefore **contingent on the entry's current content**, not on the path boundary
that the revert test exercises. Severity: does not move any number today; it does mean the
separation is not structural, and a future round appending any `kappa` sentence to a knowledge entry
would re-red C2 through C1's file. A frozen file list (the round-29-tip set) instead of a live glob
would make it structural. Not applied — this seat writes no lane bytes.

**F3 — a reference-level coupling C1 carries into C3.** C1's `recheck:` line promises
`python3 plans/sources_adopt.py --quote-file <rows> --artifact <capture>`; with C3's bytes reverted
that promised command exits 2 ("unrecognized arguments", §4.4). C1's *count* never runs the command,
so the counters stay separate; the artifact's recheck instruction is nevertheless unrunnable without
C3's artifact. R13's revert test cannot see this, and R13's wording does not cover it.

**F4 — C2's D5 repair writes into round 29's frozen counter input.**
`.ufo/waves/round-29/attempt2/adoption-expect.json` gains a documentation-only `usedby_notes` key.
Round 29's own counter prints the identical line with and without it (§5.1 P1a/P1b), so no frozen
round-29 field moved — but the "one artifact, one claim" scope of R13 is round-local and does not
constrain this write; it is recorded because the adjacent round's frozen input is the artifact.

**F5 — the frozen `defects-before.txt` is a wording-stale receipt.** Reproducing the pre-repair
bytes and diffing against the committed control, item by item:

```
D1 IDENTICAL
D2 IDENTICAL
D3 IDENTICAL
D4 DIFFERS
  control : .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md is uncommitted: M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md
  reverted: repaired            (my copy commits the addendum; the lane's control was taken with it uncommitted)
D5 DIFFERS
  control : adoption-expect.json records no S091 used-by asymmetry note
  reverted: adoption-expect.json records no S091 used-by asymmetry note and the entry cites no S091
```
The D5 difference is tool drift, not tree state: the current code's message carries the extra
clause (`plans/round30_defects.py:179`), and the D4 form in the control (`is uncommitted:`) no longer
exists in the tool (the current branch prints `still differs from HEAD:`, line 163). The **count**
still reproduces (5 pre-repair, 4 without D4's commit-state item); the **bytes** do not. The claim
calls this file the control for a byte-shaped ledger, so it should be re-minted against the current
tool or the claim should stop treating it as byte-reproducible.

**F6 — two reproducibility traps for anyone re-running this experiment.**
(1) C1's `census` field is hosted-root state, not entry state: in a bare `/tmp` copy with a perfect
SOURCES.md, `adoption_check.py --census` prints `census=fail` and exits 1 because
`scripts/sources-census.sh` demands `shokunin.conf` at the root (`ERROR: config not found`, exit 2).
Only after copying the fleet conf into the scratch root does the tree's true baseline (`census=ok`)
appear. (2) C2's D1/D4 judge `HEAD:` blobs, so a revert harness must materialize the landing as a
commit before reverting, or it scores phantom defects that belong to git state, not to any claim.

**F7 — R13's paperwork clause is unmet by the pre-registration.** R13's Check requires that "the
round's pre-registration names each claim's population **and its freeze commit**".
`plans/round-30-claims.md` contains **no commit sha at all** (`grep -nE '\b[0-9a-f]{7,40}\b'` →
NONE), and C3's predicate carries the literal placeholder `git show <freeze-baseline>:plans/sources_adopt.py`.
The populations are named (C1: entry + S081–S086 + the README row; C2: the round-29 read set;
C3: `plans/sources_adopt.py`); the freeze commit is not. Populations here were reconstructed from
the controls and the working-tree diff, which is exactly what the clause exists to prevent.

**F8 — the lane moved during this run.** At copy time 16 porcelain entries (9 modified, 7 untracked
dirs/files) and `plans/sources_adopt.py` at `+336/-3`; afterwards 17 entries — the one new porcelain
entry is `M .ufo/waves/yield.tsv` — `plans/sources_adopt.py` at `+340/-3`, and the untracked
`.ufo/waves/round-30/falsify/` grew from 1 file to 20 (invisible to the porcelain count, since the
whole directory is one untracked entry). The `sources_adopt.py` delta is one guard in `main()` (+4 lines,
`--quote-file/--artifact cannot be combined with --registry/--package`), which does not touch the
selftest case list, so `cases=14` is unaffected by it — but every number above is bound to tree
`519f77a` (scratch commit `c7b6f6d`), and the C3 case count must be re-taken at whatever commit
actually lands.

## 7. Verdict on R13 separability

| claim | is its count independent of the other two claims' artifacts? | evidence |
|---|---|---|
| C1 (coverage) | **YES** at count level: unchanged under C2-revert, C3-revert and both. Coupled at reference level only via its `recheck:` command naming C3's CLI (F3). | §4.3, §4.4, §4.5 |
| C2 (calibration) | **YES** under every path revert (D1/D2/D3/D5 revert as a block, D4 separately), and unmoved by C3's revert. **NO** at population level: its D2 re-derivation globs the directory C1 creates its entry in, and moves on that entry's content alone (F2). | §4.2, §4.3, §4.3.1, §5.2 |
| C3 (operability) | **YES**, and hermetically: the selftest reads no corpus bytes (`tempfile` fixtures only), staying `cases=14 failed=0` through every combination and moving only with its own file (`cases=10` + argparse exit 2). | §4.2, §4.3, §4.5 |

**R13's prescribed revert test: PASS — all three counts are stable under the other claims' reverts,
additively, with each revert proved live by its own counter.**
**R13's stronger sentence ("no claim's counting command counts an artifact another claim of the same
round creates"): FAIL — C2/D2 counts a population that contains C1's artifact (F2), inert only
because the entry currently contains no `kappa` line.**
**R13's Check paperwork ("pre-registration names each claim's population and its freeze commit"):
FAIL — no freeze commit is named anywhere in the pre-registration, and C3's control still reads
`<freeze-baseline>` (F7).**

## 8. Limits of this result

- One host, one tree (`519f77a`). The lane's later bytes (F8) were not re-tested.
- The reverts were applied as `git checkout BASE -- <paths>` in a scratch copy; a file that another
  seat changed **after** `363a4eb` inside a reverted path would have been reverted with it. For
  these paths the diff against `BASE` consists only of round-30 bytes (measured: SOURCES.md `+6`,
  README `+4/-1`, lesson `+7/-3`, round-29 expect `+4/-1`, receipt `+15/-0`, entry `+170/-0`,
  `R29a2CritEntry.md` `+22/-0`, `sources_adopt.py` `+336/-3`; `git diff --numstat 363a4eb 519f77a`).
- D4's revert is a scratch-only commit (`edebce6`); it proves the check's mechanism, not what the
  lane will commit.
- Only the three declared counting commands were used. C1's entry quotes were **not** re-verified
  (§5.2 aside, no `--quote-file` run against real captures was made); nothing here should be read as
  Q10/Q13 second-seat support.
- Lane writes by this seat: **none**. The only lane write is this report. Scratch:
  `/tmp/r30fx-R13Revert/` (`00-baseline.txt`, `01-revert-C1.txt`, `02-revert-C2.txt`,
  `03-revert-C2-D4.txt`, `04-revert-C3.txt`, `05…08-revert-*.txt`, `09-probes.txt`,
  `run-counters.sh`, `combo.sh`, `probes.sh`, `BASE`, `LANDED`).
