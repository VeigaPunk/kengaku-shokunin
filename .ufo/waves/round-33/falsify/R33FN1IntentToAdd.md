# R33FN1IntentToAdd — N1 ("no untracked path remains") is satisfied by the git index alone

## Scope and result

Attacked item: C2 / N1, frozen text "every file under `.ufo/waves/round-32/` is
git-tracked and no untracked path remains beneath it", implemented as
`check_n1` at `plans/round33_defects.py:68-88`. The check derives the on-disk path
set with `find <lane>/.ufo/waves/round-32 -type f -printf '%P\n'` (line 70-73) and the
"tracked" set from `git ls-files -- .ufo/waves/round-32` (line 77), then subtracts.

All work was done in fresh `/tmp` repositories with every git invocation scoped by
`-C`/`cwd` there. The lane tree, lane index, JJ state and fleet repo were never
read-modified, staged or committed; the lane's own index was not consulted.

**VERDICT: false-negative.** A single `git add -N` on an uncommitted wave file — an
index entry with the empty blob and nothing in any commit — returns `''` (green) from
`check_n1`. With zero commits in the repository, a plain `git add .` is also green
(the counter's own selftest "fixed" case). The predicate therefore binds to the
index, not to the committed tree that N1's repair is supposed to produce, so C2's
`checks=6 defects=0` is reachable while the inherited `.ufo/waves/round-32/` bytes
remain absent from history.

## Reproduction — intent-to-add

```text
$ SB=$(mktemp -d /tmp/r33n1-intent-to-add.XXXXXX)
$ git -C "$SB" init -q .
$ git -C "$SB" config user.email t@t; git -C "$SB" config user.name t
$ printf 'base\n' > "$SB/README.md"
$ git -C "$SB" add README.md && git -C "$SB" commit -qm base
$ mkdir -p "$SB/.ufo/waves/round-32/sub"
$ printf 'uncommitted wave byte\n' > "$SB/.ufo/waves/round-32/planted.md"
$ printf 'nested\n' > "$SB/.ufo/waves/round-32/sub/nested.md"
$ git -C "$SB" add -N .ufo/waves/round-32/planted.md .ufo/waves/round-32/sub/nested.md
```

Git's own view of the resulting state — everything is *not committed*, nothing is
staged for the next commit:

```text
$ git -C "$SB" status --short
 A .ufo/waves/round-32/planted.md
 A .ufo/waves/round-32/sub/nested.md
$ git -C "$SB" ls-files -s -- .ufo/waves/round-32
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	.ufo/waves/round-32/planted.md
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	.ufo/waves/round-32/sub/nested.md
$ git -C "$SB" ls-tree -r --name-only HEAD
README.md
$ git -C "$SB" diff --cached --stat
(empty)
$ git -C "$SB" cat-file -e HEAD:.ufo/waves/round-32/planted.md
fatal: path '.ufo/waves/round-32/planted.md' exists on disk, but not in 'HEAD'
$ git -C "$SB" status --porcelain=v2 -- .ufo/waves/round-32
1 .A N... 000000 000000 100644 0000000000000000000000000000000000000000 0000000000000000000000000000000000000000 .ufo/waves/round-32/planted.md
1 .A N... 000000 000000 100644 0000000000000000000000000000000000000000 0000000000000000000000000000000000000000 .ufo/waves/round-32/sub/nested.md
```

The empty blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` is the intent-to-add tell:
`git ls-files` lists the paths with the empty blob and mode `100644`, stage 0, and no
HEAD entry exists. `git diff --cached` is empty (nothing would be committed);
`git diff` shows the content as a new unstaged file.

The counter:

```text
$ python3 - "$SB" <<'PY'
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("r33d", "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round33_defects.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print("check_n1 ->", repr(m.check_n1(Path(sys.argv[1]))))
PY
check_n1 -> ''
```

Control, same sandbox, only the two index entries removed (`git rm --cached`), bytes
unchanged on disk:

```text
$ git -C "$SB" rm -q --cached .ufo/waves/round-32/planted.md .ufo/waves/round-32/sub/nested.md
$ ...same import...
check_n1 -> '2 untracked files remain under .ufo/waves/round-32: planted.md, sub/nested.md'
```

So the entire difference between red and green for the same uncommitted bytes is the
presence of an index entry, not the presence of a commit. The intent-to-add state can
also be reached after the file is already fully written, and later content edits do
not change the answer (probed: content appended after `add -N`, still `''`).

## Reproduction — staged, zero commits

The counter's own selftest asserts this shape as a *fixed* tree
(`plans/round33_defects.py:228-229`: `git init` then `git add .`, no commit, then
`cases.append(("N1-green-tracked", not check_n1(empty)))`):

```text
$ SB=$(mktemp -d /tmp/r33n1-staged.XXXXXX); git -C "$SB" init -q .
$ mkdir -p "$SB/.ufo/waves/round-32"; printf 'a\n' > "$SB/.ufo/waves/round-32/f.md"
$ git -C "$SB" add .
$ git -C "$SB" rev-list --count HEAD
0
$ ...check_n1...
check_n1 -> ''
```

Zero commits, wave file staged only, N1 green. This is not an exotic escape: the
selftest's own green fixture establishes index-only state as satisfying "tracked".

## Second false-negative channel — untracked symlink

`find ... -type f` (line 71) omits symlinks, so a non-regular untracked path beneath
the wave tree is invisible to the disk set and can never appear in `missing`, even
with no index entries at all:

```text
$ ln -s /etc/hostname "$SB/.ufo/waves/round-32/link.md"
$ git -C "$SB" status --short -- .ufo/waves/round-32
?? .ufo/waves/round-32/
$ ...after deleting the two regular untracked files...
check_n1 -> ''
```

This contradicts the claim's second clause ("no untracked path remains beneath it")
for symlinks and other non-regular entries (dangling symlinks, fifos, sockets), which
`find -type f` drops silently.

## Affected code paths and the selftest's blind spots

- `plans/round33_defects.py:70-73` — disk enumeration restricted to `-type f`.
- `plans/round33_defects.py:77-84` — "tracked" = `git ls-files` output = index
  membership, including intent-to-add entries and uncommitted staged entries.
- `plans/round33_defects.py:85-88` — a set difference over names only; no content,
  HEAD, or blob identity is consulted.
- `plans/round33_defects.py:228-235` — the selftest's green N1 fixture stages without
  committing, and its red fixture (`wave/stray.md` written and left untracked) only
  exercises a plain regular untracked file. No `add -N` case and no symlink case
  exist, so the selftest cannot fail on either channel; it prints
  `SELFTEST checks=14 failed=0` (observed).

## What a commit-binding check would need (probe, not a lane edit)

`git diff --cached --name-only` is *not* sufficient — it is empty under intent-to-add
(observed `[]`), while `git diff --name-only` is non-empty (`[.ufo/waves/round-32/planted.md]`).
Two detectors were probed that do bind to history:

- `git ls-files -s` empty-blob `e69de29…` — distinguishes intent-to-add entries but
  not staged-but-uncommitted non-empty content.
- Compare the disk set against `git ls-tree -r --name-only HEAD` restricted to the
  wave prefix. Observed:

```text
intent state:     hardened missing -> ['planted.md']
after real commit: hardened missing -> []
```

i.e. the HEAD-tree formulation reddens on exactly the state N1 exists to ban and greens
only when the bytes are in a commit. (A correct version must also cover the symlink
gap, e.g. `find ... \( -type f -o -type l \)` or `git status --porcelain -uall`
cross-checked against HEAD.)

## Claim impact

- `plans/round-33-claims.md` C2 lists N1 among the six checks whose transition from
  `defects=6` to `defects=0` is the repair receipt. As implemented, N1's green does
  not witness the inherited-state repair described in "Inherited state: the untracked
  `.ufo/waves/round-32/` tree … is committed under this round's entry via N1". An
  operator can run `git add .` (or `git add -N`) over `.ufo/waves/round-32/`, get
  `checks=6 defects=0`, exit 0, and still have landed none of those bytes.
- This is a false-negative of the counter, not a mutation of its inputs: no file
  content, claim text, or fleet report was touched. Whether the lane currently holds
  such an index-only state was **not** examined (lane index off-limits by contract);
  that question is unobserved here.

## Retained evidence

- `/tmp/r33n1-intent-to-add.TrB3Ud` — intent-to-add sandbox (paths, `ls-files -s`,
  `ls-tree HEAD`, `status --porcelain=v2`, `check_n1` red/green).
- `/tmp/r33n1-fixprobe.bW8CqS` — committed control + hardened HEAD-tree detector.
- `/tmp/r33n1-fixprobe2.J39s61` — hardened detector on intent state.
- `/tmp/r33n1-staged.XXXXXX` — zero-commit staged sandbox.
- Lane: no writes apart from this report; no `git`/`jj` command run against the lane;
  no tool installed.
