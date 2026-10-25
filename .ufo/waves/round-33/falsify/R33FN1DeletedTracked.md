# N1 tracked-file deletion — R33FN1DeletedTracked

## Target and frozen claim

Frozen claim (`plans/round-33-claims.md:86-88`):

> N1 every file under `.ufo/waves/round-32/` is git-tracked and no untracked path
> remains beneath it (inherited-state resolution per §5 of the round contract)

Implementation (`plans/round33_defects.py:68-88`): `on_disk` = `find <lane>/.ufo/waves/round-32 -type f -printf '%P\n'`;
`tracked` = `git -C <lane> ls-files -- .ufo/waves/round-32`; return a defect only when
`on_disk - tracked` is non-empty. The reverse difference is never computed.

## Fixture (fresh, /tmp only)

All git commands were scoped with `git -C /tmp/r33n1del/...`; nothing in the lane, index,
fleet repo or sibling repos was written. No tools installed or updated.

```text
$ mkdir -p /tmp/r33n1del/a/.ufo/waves/round-32 && cd /tmp/r33n1del/a && git init -q .
$ printf 'seat\n' > .ufo/waves/round-32/seat.md
$ printf 'shard\n' > .ufo/waves/round-32/shards/s1.md
$ git -c user.name=t -c user.email=t@t add . && git -c user.name=t -c user.email=t@t commit -qm "round 32 wave tree"
5e16b54c6848367545c14dba05e95e58512d5c3d
$ git ls-files -- .ufo/waves/round-32
.ufo/waves/round-32/seat.md
.ufo/waves/round-32/shards/s1.md
```

Then the tracked file is deleted from disk only (index untouched):

```text
$ rm .ufo/waves/round-32/seat.md
$ git status --porcelain
 D .ufo/waves/round-32/seat.md
$ git ls-files -- .ufo/waves/round-32
.ufo/waves/round-32/seat.md
.ufo/waves/round-32/shards/s1.md
$ git diff-index --name-status HEAD -- .ufo/waves/round-32
D	.ufo/waves/round-32/seat.md
```

The check itself, imported unmodified from `plans/round33_defects.py` (git 2.56.0,
CPython 3.14.8):

```text
$ python3 -c "import sys; sys.path.insert(0,'/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans');
from pathlib import Path; import round33_defects as d;
print(repr(d.check_n1(Path('/tmp/r33n1del/a'))))"
''
```

`check_n1` returns the empty string — green — while `git status` reports ` D`.

## Behaviour matrix (observed)

| # | Fixture state | `git status --porcelain` | `check_n1` |
|---|---|---|---|
| A | committed file deleted from disk, deletion unstaged | `' D .ufo/waves/round-32/seat.md\n'` | `''` (green) |
| B | deletion staged with `git rm` | `'D  .ufo/waves/round-32/seat.md\n'` | `''` (green) |
| B2 | deletion committed at HEAD | `''` | `''` (green) |
| C | untracked file present (control) | `'?? .ufo/waves/round-32/stray.md\n'` | `'1 untracked files remain under .ufo/waves/round-32: stray.md'` (red) |
| D | deleted-tracked and untracked coexist | `' D ...seat.md\n?? ...z_new.md\n'` | `'1 untracked files remain ...: z_new.md'` — mentions only the untracked path |
| E | whole `.ufo/waves/round-32` directory removed | two ` D` lines | `'.ufo/waves/round-32 is not readable on disk: find: ‘...’: No such file or directory'` (red, but only because `find` fails, not because tracked paths vanished) |
| F | a tracked subdirectory (`shards/`) deleted from disk, parent left | `' D .ufo/waves/round-32/shards/s1.md\n'` | `''` (green) |
| G | every tracked file deleted, wave directory left as an empty dir | three ` D` lines | `''` (green) |

Set differences for fixture F, printed side by side:

```text
on_disk: ['seat.md']
index  : ['seat.md', 'shards/s1.md']
HEAD   : ['seat.md', 'shards/s1.md']
on_disk - index : []                        <- only set N1 tests
index - on_disk : ['shards/s1.md']           <- asymmetry N1 ignores
HEAD  - on_disk : ['shards/s1.md']           <- what a tree-vs-disk check would see
```

## Why it happens (exact mechanism)

`git ls-files` enumerates the **index**. A file committed and then removed from the
worktree but not staged stays in the index, so `tracked` still contains it. `on_disk`
loses it. Since `check_n1` computes only `on_disk - tracked`, the missing path falls into
the untested `tracked - on_disk` direction and the check stays green. Staging the deletion
(`git rm`) moves the removal into the index and commit, but `on_disk` shrinks
correspondingly, so the one-directional difference is again empty. Only a path that is on
disk and *not* in the index can ever redden N1 — the direction round 32 actually produced.

The selftest cannot expose this: its green fixture is `git add .` with **no commit**
(`plans/round33_defects.py:228`, which models index-only tracking), and its only red case
adds a stray untracked file (`:233-235`). No deleted-tracked case is constructed, so the
`N1-green-tracked` / `N1-red-untracked` pair passes while the blind spot stands.

Live lane, read-only, for baseline: `check_n1(lane)` → `''`, and
`git -C . status --porcelain -- .ufo/waves/round-32` is empty. The lane's wave tree is
currently clean, so the live green is genuine there — this attack is about what the check
would report under a state it claims to rule out.

## Relation to prior build-wave findings

`R33CounterAttack.md` E1 already covers index-without-commit (`git add` only), E1c/E1d
cover non-regular files and a symlinked wave root, and `R33ClaimsReview.md:19` notes N1
demonstrates index tracking rather than committed-tree membership. This seat tests a
different edge, not covered by any of them: the **index/HEAD holds a path that the
worktree no longer has**. The repair narrative for N1 (`plans/round33_defects.py:12-13`)
is about a pushed tip diverging from what should be committed; a worktree that has lost
tracked files is the same class of divergence in the opposite direction, and N1 reports
`defects=0` for it.

## Verdict

**uncaught** — the N1 check does not see the on-disk/index asymmetry it is asked about.
Concretely: with a committed `round-32` file deleted from disk (and even with the whole
tree emptied, cases A/F/G), `check_n1` returns `''`, indistinguishable from a clean tree,
while `git status` says ` D` and `git diff-index HEAD` says the path is gone. Qualifying
note for honest scoring: under a strict literal reading of the frozen predicate ("every
file *under* the directory is git-tracked, no untracked path remains") the empty-disk
state is vacuously satisfiable, so this is not a textual contradiction of the claim; it is
a false negative against the property the repair exists to certify — that the committed
wave tree is present and committed at the tip. Rated **uncaught** on the attack question
and a **limitation** of the predicate's wording.

Smallest safe hardening, if the parent wants one line: also compute
`tracked - on_disk` (equivalently, require `git ls-files -d -- .ufo/waves/round-32` to be
empty) and red with e.g. `N tracked paths under … are missing from the worktree`; for the
stricter committed-tree reading, diff `git ls-tree -r --name-only HEAD -- .ufo/waves/round-32`
against `on_disk` instead of using `git ls-files`. That would have reddened cases A, B, F
and G and left C red.

VERDICT: <attack-finished>
