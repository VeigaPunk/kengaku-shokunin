# R39LessonErrata — receipts (command → output, 2026-10-26)

All commands run in `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only Git use only: `log`, `diff`,
`grep`, `cat-file`, `ls-tree`; no `add`/`commit`/`checkout`/`reset`/`stash`, no jj). No clone, no scratch dir,
no write to the lane. Target lesson bytes: `corpus/lessons/round-38.md` at `ef2fba062069de4f29aea45cb2a03d29a131054b`
(2026-10-26 03:22:34 -0300), working tree equal to HEAD (`git diff --stat HEAD -- corpus/lessons/round-38.md` empty, rc 0).

## A. Defect 1 — the round-37 fix has two moves; the round-38 cell names one

A1. `sed -n '42p' corpus/lessons/round-37.md` (row landed in `21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9`, 2026-10-26 02:25:17 -0300);
head of the row:

```
| order-of-operations — the C2 skip-control executed the frozen probe before the first recorded run | `plans/round-37-
```

fix column tail (verbatim):

```
Rule forward: a control that executes a frozen instrument keeps the run as a receipt. |
```

A2. `grep -c "Rule forward: a control that executes a frozen instrument keeps the run as a receipt" corpus/lessons/round-37.md`
→ `1` (the sentence occurs once; it is the row's second move, after the re-pin/re-run machinery:
"The probe was at its frozen digest `63cb75cf…5eedf` before that run and is re-pinned every run by C2 V5 (digest +
`--dry` byte-equality) and by V2's `P10` fresh-run compare").

A3. `corpus/lessons/round-38.md:36`, Mistakes row 2, `captured-by` cell (verbatim):

```
the claims header itself (self-disclosed before the freeze commit); round 37's fix (re-pin and re-run every counter run) does not prevent the ordering, it only makes the discarded run harmless
```

A4. `plans/round-38-claims.md:10-11` (verbatim, the run the rule forward would have kept):

```
output was discarded unread; it is not the first recorded run and is not evidence
```

A5. `grep -n "order-of-operations — \*\*recurrence\*\*" corpus/lessons/round-38.md` → `36` (the row under test).

## B. Defect 2 — `census-before.txt` is the clean baseline, listed inside "all red"

B1. `awk 'NR>=11 && NR<=15' corpus/lessons/round-38.md`:

```
11: 
12: Controls, all red at the freeze (`.ufo/waves/round-38/claims/`): `control-c1-nothing.txt` (`PINS total=14 mismatched=0`,
13: `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=0 survived=22`, exit 1),
14: `control-c1-gate-edited.txt` (`invalid=22`), `control-c2-nothing.txt` (`checks=7 defects=4`), `control-c2-skip.txt`
15: (`checks=7 defects=2`, V2 and V6 red, V7 green — disclosed at freeze), `census-before.txt` (exit 0, 15 W04).
```

B2. `grep -c W04 .ufo/waves/round-38/claims/census-before.txt` → `15`; `tail -1` of the same file → `exit=0`;
the file's second-to-last line → `kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`.

B3. `grep -c census plans/round-38-claims.md` → `0`, rc 1 (the claims file never names the census baseline;
its only controls sentence is "Controls are committed with this file under `.ufo/waves/round-38/claims/`.").

B4. `grep -n "^## Census" corpus/lessons/round-38.md` → `58` (the lesson's own Census section reports it correctly:
"Before (freeze): exit 0, `kengaku ok`, 15 W04").

## C. Gate for the Defect-1 class — red-before and green-after, both real

Predicate: a committed control that asserts a probe run requires its round's receipt at the same commit.

C1. RED at the round-38 freeze `e0a378539a45cc9388c66cfba22f44275131de23`:

```
$ git grep -l "fresh probe" e0a378539a45cc9388c66cfba22f44275131de23 -- .ufo/waves/round-38/claims
e0a378539a45cc9388c66cfba22f44275131de23:.ufo/waves/round-38/claims/control-c2-skip.txt
$ git cat-file -e e0a378539a45cc9388c66cfba22f44275131de23:corpus/evidence/round38/build-pmars-probe.txt
fatal: path 'corpus/evidence/round38/build-pmars-probe.txt' exists on disk, but not in 'e0a378539a45cc9388c66cfba22f44275131de23'
rc=128
```

C2. GREEN at the round-39 freeze `088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8`:

```
$ git grep -l "fresh probe" 088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8 -- .ufo/waves/round-39/claims
(no output)
rc=1
$ git cat-file -e 088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8:corpus/evidence/round39/git-leak-probe.txt
fatal: path 'corpus/evidence/round39/git-leak-probe.txt' exists on disk, but not in '088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8'
rc=128
```

Green because no committed round-39 control claims a run (the receipt is absent too, which is the correct state
before the first recorded run `6a1eb5e1`); a skip-control committed before the receipt flips it red — the exact
round-38 failure.

C3. Claims dirs at both freezes (`git ls-tree --name-only <commit>:.ufo/waves/round-{38,39}/claims`):

```
== e0a37853
r38 census-before.txt  control-c1-gate-edited.txt  control-c1-nothing.txt
r38 control-c2-nothing.txt  control-c2-skip.txt  frozen-digests.txt
== 088f7c36
r38 (same six files)
r39 census-before.txt  control-c1-gate-edited.txt  control-c1-hostile-inproc-module.py
r39 control-c1-hostile-inproc.txt  control-c1-nothing.txt  control-c2-nothing.txt  frozen-digests.txt
```

## D. Forward state (round-39 side)

D1. `corpus/lessons/round-39.md` is untracked in the working tree (`git status --porcelain` → `?? corpus/lessons/round-39.md`;
no commit exists for it), so the quote below is a snapshot of live draft bytes, not landed text.

D2. `sed -n '13p' corpus/lessons/round-39.md` contains:

```
`census-before.txt` (exit 0, 15 W04 — a baseline, not a control)
```

i.e. round 39 already separates the baseline that round 38 listed as red — the forward half of Defect 2 is done in prose.

## E. Finding's own citations that do not resolve

E1. `F38RevLesson` §Defect 2 heads its quote "lines 11–13"; the quoted sentence is at `corpus/lessons/round-38.md:12-15`
(B1 above).

E2. `F38RevLesson` Defect 2 closes "the census baseline should be named outside the 'all red' list (the claims file
keeps it separate)". B3 shows the claims file never names it (`grep -c census` → 0). The separation it names does not
exist; the only correct placement in the lane is the lesson's §Census (:58).
