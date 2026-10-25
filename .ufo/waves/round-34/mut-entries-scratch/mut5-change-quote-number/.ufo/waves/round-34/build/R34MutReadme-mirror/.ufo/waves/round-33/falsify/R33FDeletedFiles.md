# R33FDeletedFiles — N1 disk/index asymmetry for deleted files

Seat: `KengakuR33.R33FDeletedFiles` (leaf, falsify wave 36, hyaku run 7)
Target: `plans/round33_defects.py::check_n1` (lines 68-88) — C2/N1,
frozen predicate at `plans/round-33-claims.md:87-88`.
Date: 2026-10-25. No lane/fleet file was edited, staged, committed, or removed.
No tool installed or updated (nothing was needed).

**Verdict: UNCAUGHT — one-directional set difference.** A file tracked in the index
(or in HEAD) and deleted from disk is *invisible* to `check_n1`; the counting command
still prints `checks=6 defects=0` and exits 0. One rider: the frozen predicate text is
itself one-directional ("every file under … is git-tracked"), so this is **not** a
claim/code mismatch; it is a real blind spot against the repair narrative and against
the defect class N1 inherits, and it silently costs the check its `tracked == on_disk`
teeth.

## 1. Exact comparison semantics (as written)

```
:70-76  disk  = find <lane>/.ufo/waves/round-32 -type f -printf '%P\n'
        if find returncode != 0 -> return "<WAVE32> is not readable on disk: ..."
        on_disk = set(non-empty lines)                      # paths relative to WAVE32
:77     proc = git -C <lane> ls-files -- .ufo/waves/round-32   # THE INDEX, never HEAD
:80-84  tracked = {line minus WAVE32+"/" prefix}             # paths relative to WAVE32
:85     missing = sorted(on_disk - tracked)                  # <-- the only predicate
:86-87  if missing -> "<n> untracked files remain under ..."
:88     return ""
```

So N1 is `on_disk − tracked` and **nothing else**. `tracked − on_disk` is never formed,
`git ls-tree HEAD` is never consulted, and the failure vocabulary ("untracked files
remain") can only express disk-side surplus. Two independent blindnesses:

| Direction | Set expression | Git source it would need | N1 |
|---|---|---|---|
| file on disk, not indexed | `on_disk − tracked` | `ls-files --others` | **checked** |
| file indexed, absent on disk | `tracked − on_disk` | `ls-files --deleted` / `--diff-filter=D` | **never formed** |
| file in HEAD, absent from index and disk | `head − tracked` | `ls-tree -r HEAD` | **never formed** |

The `find` return-code guard is the only thing that ever notices a *deletion*, and only
when the whole `round-32` directory is gone (then `find` fails and N1 goes red
fail-closed). Hence the exact blind region is `0 < deleted < all files under the tree`.

## 2. Fixture and observations (fresh `/tmp`, all git scoped there)

`SANDBOX=/tmp/r33-deleted-files-nVJfjL`; `GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_SYSTEM=/dev/null`; repo `lane/` with three committed round-32 files
(`build/keep1.md`, `build/keep2.md`, `claims/receipt.txt`) at HEAD. Probe loads the lane
module read-only via `importlib` and prints both set differences plus `check_n1`'s
return value. Each case resets with `git reset --hard HEAD; git clean -fd` inside the
sandbox only.

```
== S1 control clean ==
  on_disk - tracked = []   tracked - on_disk = []
  check_n1 => ''

== S2 control: one untracked file on disk (positive control) ==
  on_disk - tracked = ['build/stray.md']
  check_n1 => '1 untracked files remain under .ufo/waves/round-32: build/stray.md'

== S3 tracked in index, deleted from disk (plain rm) ==
  on_disk  = ['build/keep2.md', 'claims/receipt.txt']
  tracked  = ['build/keep1.md', 'build/keep2.md', 'claims/receipt.txt']
  in_HEAD  = ['build/keep1.md', 'build/keep2.md', 'claims/receipt.txt']
  on_disk - tracked (N1's only predicate) = []
  tracked - on_disk (NEVER computed)      = ['build/keep1.md']
  git status: [' D .ufo/waves/round-32/build/keep1.md']
  check_n1 => ''

== S4 HEAD-only: rm + `git rm --cached` (in HEAD, in neither index nor disk) ==
  in_HEAD = ['build/keep1.md', 'build/keep2.md', 'claims/receipt.txt']
  tracked = ['build/keep1.md', 'claims/receipt.txt']
  on_disk - tracked = []   tracked - on_disk = []
  git status: ['D  .ufo/waves/round-32/build/keep2.md']
  check_n1 => ''

== S5 staged deletion (`git rm`, still in HEAD) ==
  on_disk - tracked = []   tracked - on_disk = []
  git status: ['D  .ufo/waves/round-32/build/keep1.md']
  check_n1 => ''

== S6 every file deleted from disk, directory survives ==
  on_disk  = []
  on_disk - tracked = []
  tracked - on_disk = ['build/keep1.md', 'build/keep2.md', 'claims/receipt.txt']
  git status: [' D ...keep1.md', ' D ...keep2.md', ' D ...claims/receipt.txt']
  check_n1 => ''

== S7 whole .ufo/waves/round-32 directory removed ==
  check_n1 => '.ufo/waves/round-32 is not readable on disk: find: '/tmp/r33-deleted-files-nVJfjL/lane/.ufo/waves/round-32': No such file or directory'
```

S2 proves the disk→index direction is live (so the empty verdicts are asymmetry, not a
broken fixture). S3/S6 are the target: the largest possible deletion short of removing
the directory — the tree's entire content — still returns `''`.

## 3. End-to-end at the claim's counting command

Green fixture `$SB/green` reproducing the module's own selftest green tree
(round-32 wave file + `## Round 32` + both lesson corrections), committed; N3/N4 read
the live fleet reports (read-only) as `main()` always does.

```
== P1 green fixture, N1 clean ==
checks=6 defects=0
exit=0

== P2 same fixture, the tracked round-32 file deleted from disk ==
 D .ufo/waves/round-32/build/seat.md
checks=6 defects=0
exit=0

== P3 same, plus a HEAD-only file (`git rm --cached`) ==
D  .ufo/waves/round-32/build/note.md
 D .ufo/waves/round-32/build/seat.md
checks=6 defects=0
exit=0
```

The frozen predicate's two receipts (`defects=6` before / `defects=0` after) are
unperturbed by deletions in either direction, so C2's calibration score is not moved by
this finding — but the N1 label "round32-wave-tree-committed" overstates what N1 can
see: it certifies *the index ⊇ the disk*, never *the committed tree == the disk*.

## 4. Why it is reachable, not hypothetical

- Not a git limitation: the same sandbox state is reported by three primitives that N1
  does not call —
  `git ls-files --deleted -- .ufo/waves/round-32` → `build/keep1.md`;
  `git diff --name-only --diff-filter=D HEAD -- …` → `build/keep1.md`;
  `git status --porcelain` → ` D .ufo/waves/round-32/build/keep1.md`.
- Live lane, this tip: exact set comparison for round-32 is currently symmetric —
  `disk 89 / index 89 / head 89`, `tracked − disk = []`, `head − index = []`, N1 `''`.
  So there is no live N1 false-green today; the defect is latent.
- The same mechanism is observably present one directory over: `git status --porcelain`
  at this tip shows ` D .ufo/waves/round-33/assimilation/append-package.md` and
  ` D .ufo/waves/round-33/assimilation/quotes-rows.txt` (tracked, absent on disk,
  independently noted in `build/R33WaveBook.md:210-212`). Round-33 paths are outside
  N1's scope by design, but they show the state occurs in this lane during normal work
  — a wave-tree file can be deleted from the worktree while remaining tracked, and the
  class N1 was repaired for ("wave-tree paths in the wrong state at a pushed tip") would
  be re-opened in that direction without N1 noticing.

## 5. Overlap and scope boundaries

- `build/R33CounterAttack.md:119-121` (B7) names the same asymmetry in one line without a
  fixture; this report supplies the fixture, the exact set algebra, the two-direction
  table, and the end-to-end exit-0 receipts. No contradiction with B7.
- `build/R33ClaimsReview.md:19` already observes N1 tests the index, not the commit.
  `head − tracked` (S4) is the confirming case for that observation.
- Not attacked here (sibling seats own them): non-regular files / symlinked root
  (`N1SpecialFiles`, counter's B5), newline-in-filename splitting (`N5Newline`),
  content-vs-index drift (`LandedBytes`). The `find`-returncode guard's incidental
  fail-closed behaviour on a missing directory is reported above only because it bounds
  the blind region for *this* item.

## 6. Operability note (no fix applied — falsify wave)

Minimal closure of the asymmetry, if the lane wants N1 to mean its label, is two lines
next to `:85`: form `vanished = sorted(tracked - on_disk)` and redden on it, and/or
compare `git ls-tree -r --name-only HEAD -- WAVE32` against `tracked`. One caveat that
must travel with any such change: the frozen predicate text at
`plans/round-33-claims.md:87-88` is directional, so widening N1 changes the predicate
and cannot be scored under the round-33 freeze — it belongs to a later round's claim,
not to a silent edit of `round33_defects.py`.

## 7. Reproducer

```
SB=$(mktemp -d /tmp/r33-deleted-files-XXXXXX); export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
mkdir -p "$SB/lane/.ufo/waves/round-32/build"; cd "$SB/lane"; git init -q -b main .; git config user.email t@t; git config user.name t
printf 'alpha\n' > .ufo/waves/round-32/build/keep1.md; git add -A; git commit -qm tree
rm .ufo/waves/round-32/build/keep1.md
git ls-files --deleted -- .ufo/waves/round-32   # names the file
git status --porcelain                          #  D .ufo/waves/round-32/build/keep1.md
python3 - "$SB" <<'PY'
import sys, importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location("m","/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round33_defects.py")
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
print("check_n1 =>", repr(m.check_n1((Path(sys.argv[1])/"lane").resolve())))
PY
```

Observed: `check_n1 => ''` (that is the whole finding).

## 8. Evidence retained

- Sandbox: `/tmp/r33-deleted-files-nVJfjL` (`lane/`, `green/`, `probe.py`).
- All quoted outputs above are verbatim from this session; every command was run with
  `git -C`/cwd inside `/tmp` and `GIT_CONFIG_GLOBAL=/dev/null
  GIT_CONFIG_SYSTEM=/dev/null`, so no lane Git state was read as writable or touched.
- Read-only lane reads: `plans/round33_defects.py:1-266`,
  `plans/round-33-claims.md:1-120`, `git ls-files`/`ls-tree`/`status`/`log` on the lane
  (no write subcommand), `.ufo/waves/round-33/claims/defects-before.txt`,
  `build/R33CounterAttack.md:108-130`, `build/R33ClaimsReview.md:19`,
  `build/R33WaveBook.md:205-226`.
- No installs, no plugin/config changes, no commits, no staged paths, no branch moves.
