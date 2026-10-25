# R33FN1Newlines — C2/N1 filename serialization (falsify)

Round 33, hyaku run 7, 2026-10-25. Seat: `KengakuR33.R33FN1Newlines`.
Target: N1 of `plans/round33_defects.py` (sha256
`6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6`, mtime
`2026-10-25 14:06:40 -0300`, 11817 bytes — unchanged by this seat).
Frozen predicate `plans/round-33-claims.md:87-88`:
"every file under `.ufo/waves/round-32/` is git-tracked and **no untracked path
remains beneath it**".
Method: isolated `/tmp/r33fn1nl/repo` git repo; every git command carries
`-C /tmp/r33fn1nl/repo`. No lane/fleet file touched (see §10).

## 1. The named defect, restated

N1's own docstring says "Every file under .ufo/waves/round-32/ is tracked;
nothing untracked remains" (`plans/round33_defects.py:68-69`). The check builds
two path sets and subtracts:

- `on_disk` from `find <wave> -type f -printf '%P\n'` (`:70-73`), split with
  `str.splitlines()` (`:76`);
- `tracked` from `git ls-files -- <wave>` (`:77`), also split with
  `str.splitlines()` (`:80-84`).

Both sides are newline-delimited text, but neither is NUL-delimited, and
`str.splitlines()` splits on more characters than `\n`. A filename that carries
a line separator therefore does not survive either side intact.

## 2. Mechanism (three independent faults)

1. `find -printf '%P\n'` is a **record format with no escaping**: a filename
   containing `\n` is emitted as two records.
2. `git ls-files` (no `-z`) **C-quotes** such a path: it prints
   `".ufo/waves/round-32/c1.md\nc2.md"` with a literal backslash-n, so the
   tracked side holds one quoted string, not the path.
3. `str.splitlines()` splits on `\n`, `\r`, `\v`, `\f`, `\x1c-\x1e`, `\x85`,
   `\u2028`, `\u2029` — so even a filename with **no newline at all** (U+2028)
   is mangled after `find` emitted it correctly.

Result: the subtraction compares different name spaces. When the fragments
happen to equal tracked names, the difference is empty → **silent green**. When
a genuinely committed separator-named file is quoted by git, the difference is
non-empty → **false red**.

## 3. Counterexamples (exact commands and outputs)

Sandbox baseline: `git init -q /tmp/r33fn1nl/repo`; commit of
`.ufo/waves/round-32/{seat.md,stray.md,receipts/status.txt}`. Then one file at a
time, untracked unless stated.

```
$ python3 plans/round33_defects.py --lane /tmp/r33fn1nl/repo
checks=6 defects=0                     # full-green mirror, clean tree (§4)
```

| # | fixture under `.ufo/waves/round-32/` | `find -printf '%P\n'` emits | N1 result |
|---|---|---|---|
| A | untracked `zz-alpha<LF>zz-beta.md` | 2 records | RED — but **"2 untracked files"** for **1** file, names `zz-alpha, zz-beta.md` |
| B | untracked `seat.md<LF>stray.md` (halves are tracked names) | `seat.md`,`stray.md` | **GREEN (silent miss)** |
| C | **committed** `c1.md<LF>c2.md`, `git status` empty | `c1.md`,`c2.md` | **RED (false positive)**, `c1.md, c2.md` |
| D | untracked `seat.md<U+2028>stray.md` (no newline in name) | 1 correct record, then `splitlines()` splits it | **GREEN (silent miss)** |
| F | untracked `seat.md<LF>` (trailing LF only) | `seat.md` + terminator | **GREEN (silent miss)** |
| G | untracked `<LF>seat.md` (leading LF only) | ``, `seat.md`; empty filtered at `:76` | **GREEN (silent miss)** |
| H | untracked `seat.md<CR>stray.md` | 1 record, `splitlines()` splits on `\r` | **GREEN (silent miss)** |

Scenario B, verbatim:

```
$ git -C /tmp/r33fn1nl/repo status --porcelain=v1 -z | tr '\0' '\n'
?? .ufo/waves/round-32/seat.md
stray.md
$ git -C /tmp/r33fn1nl/repo ls-files --others --exclude-standard | od -c | head -4
0000000   "   .   u   f   o   /   w   a   v   e   s   /   r   o   u   n
0000020   d   -   3   2   /   s   e   a   t   .   m   d   \   n   s   t
0000040   r   a   y   .   m   d   "  \n
$ python3 plans/round33_defects.py --lane /tmp/r33fn1nl/repo
checks=6 defects=0
[rc=0]
```

The file exists, is untracked, is named by git (quoted), and N1 is green.

Scenario C, verbatim (the opposite failure):

```
$ git -C /tmp/r33fn1nl/repo add -A && git -C /tmp/r33fn1nl/repo -c user.name=t -c user.email=t@e commit -qm nl   # rc=0
$ git -C /tmp/r33fn1nl/repo status --porcelain=v1 -z | tr '\0' '\n'      # empty: clean tree
$ git -C /tmp/r33fn1nl/repo ls-files -- .ufo/waves/round-32
".ufo/waves/round-32/c1.md\nc2.md"
.ufo/waves/round-32/receipts/status.txt
.ufo/waves/round-32/seat.md
.ufo/waves/round-32/stray.md
$ python3 plans/round33_defects.py --lane /tmp/r33fn1nl/repo | grep 'DEFECT N1'
DEFECT N1 round32-wave-tree-committed: 2 untracked files remain under .ufo/waves/round-32: c1.md, c2.md
```

Every file is tracked **and committed**, `git status` is empty, and N1 still
reports two untracked files. N1's repair narrative is "the repair commits the
whole `.ufo/waves/round-32/` tree" (`plans/round-33-claims.md:157-158`); a tree
containing one separator-named file therefore can **never** reach `defects=0`.
`git add`/`commit` accept such a name (rc=0 above), so this is not a
hypothetical state.

## 4. Receipt-level falsification

Full-green `/tmp` mirror (N2/N5/N6 fixtures written verbatim from the shipped
selftest's green fixture, `plans/round33_defects.py:216-232`; N3/N4 read the
absolute fleet reports, which are currently green — the known B6 blind spot),
then **one** untracked wave file named `seat.md<LF>`:

```
$ python3 plans/round33_defects.py --lane /tmp/r33fn1nl/repo   # clean tree
checks=6 defects=0
[rc=0]
$ printf 'untracked\n' > '/tmp/r33fn1nl/repo/.ufo/waves/round-32/seat.md
'
$ git -C /tmp/r33fn1nl/repo status --porcelain=v1 -z | tr '\0' '\n'
?? .ufo/waves/round-32/seat.md
$ python3 plans/round33_defects.py --lane /tmp/r33fn1nl/repo
checks=6 defects=0
[rc=0]
```

The frozen counting command prints `checks=6 defects=0` and exits 0 while an
untracked path remains beneath `.ufo/waves/round-32/` — the exact state the
frozen predicate forbids. Same with `seat.md<LF>stray.md` (`defects=0`, rc=0).

## 5. This falsifies build-wave claim B7

`R33CounterAttack.md:120` asserts: "filenames containing newlines split
differently in `find` vs `ls-files` output (**false RED at worst — conservative
direction**)". Scenarios B, D, F, G, H are false **GREEN**: the direction is not
conservative. A C2 receipt on a tree with one separator-named untracked wave
file is indistinguishable from the repaired state.

## 6. Selftest evidence gap

```
$ python3 plans/round33_defects.py --selftest | tail -3
CASE N1-red-untracked PASS
SELFTEST checks=14 failed=0
[rc=0]
```

The N1 cases only use plain names (`plans/round33_defects.py:229` green,
`:234-235` `stray.md`). No fixture exercises a separator in a filename, so the
artifact's own evidence cannot see this class. The green fixture is also the
`git init` + `git add .` no-commit shape already reported by `R33FN1Index`.

## 7. Real-lane reachability (read-only)

```
$ git -C <lane> rev-parse --short HEAD
77ac8c1
$ find <lane>/.ufo/waves/round-32 -type f | wc -l ; git -C <lane> ls-files -- .ufo/waves/round-32 | wc -l
89
89
$ find <lane>/.ufo/waves/round-32 -type f -name '*[[:cntrl:]]*' | wc -l
0
$ python3 plans/round33_defects.py --lane <lane>
checks=6 defects=0
[rc=0]
```

The live round-32 tree is clean and separator-free, so N1 is currently **green
and correct by luck of the name set**. The defect is latent: it triggers on the
first wave artifact whose name carries a line separator (which git happily
commits), and it triggers in both directions.

## 8. Verdict

**Caught.** N1 is falsified in both directions:

- **Silent miss (uncaught untracked path)**: untracked wave files named
  `seat.md<LF>`, `<LF>seat.md`, `seat.md<LF>stray.md`, `seat.md<CR>stray.md`,
  `seat.md<U+2028>stray.md` leave `check_n1` green, and the full C2 receipt
  prints `checks=6 defects=0` / exit 0 (§3, §4).
- **False positive**: a **committed**, clean-tree file named `c1.md<LF>c2.md`
  makes N1 report `2 untracked files` (§3 C), so the claim's own repair
  ("commit the whole tree") cannot satisfy N1 for such a name.
- **Miscount/garble**: one untracked newline file is reported as "2 untracked
  files" with truncated names (`zz-alpha, zz-beta.md`) — the counting line the
  frozen predicate relies on is not a file count (§3 A).

Not claimed: the live landing is fake — §7 shows 89/89 tracked. This is a
counter-condition defect, not an observation about the round-32 repair itself.

## 9. Smallest safe correction (verified in scratch)

NUL-terminate both sides and split on NUL only:

```python
disk = subprocess.run(["find", str(lane / WAVE32), "-type", "f", "-printf", "%P\\0"],
                      capture_output=True, check=False).stdout
on_disk = {p.decode() for p in disk.split(b"\x00") if p}
proc = subprocess.run(["git", "-C", str(lane), "ls-files", "-z", "--", WAVE32],
                      capture_output=True, check=False).stdout
```

Scratch implementation (`/tmp/r33fn1nl_fixed_check.py`) against the same
sandbox:

```
A/B  untracked 'seat.md<LF>stray.md'  -> disk=4 tracked=3 missing=1 first=['seat.md\nstray.md']
F    untracked 'seat.md<LF>'          -> disk=4 tracked=3 missing=1 first=['seat.md\n']
G    untracked '<LF>seat.md'          -> disk=4 tracked=3 missing=1 first=['\nseat.md']
H    untracked 'seat.md<CR>stray.md'  -> disk=4 tracked=3 missing=1 first=['seat.md\rstray.md']
C    committed 'c1.md<LF>c2.md'       -> disk=4 tracked=4 missing=0 first=[]
```

Both directions close, and the committed case stops being a false alarm. A
selftest case per direction (untracked `seat.md<LF>` red; committed
`c1.md<LF>c2.md` green) should be added beside `:229-235`, otherwise the fix is
again unguarded by the artifact's own evidence.

## 10. Environment / hygiene

- No tool installed or updated; no lane/fleet write; no commit/stage in the
  lane. Fixtures confined to `/tmp/r33fn1nl/` plus helpers
  `/tmp/r33fn1nl_run.py`, `/tmp/r33fn1nl_fixed_check.py`; every git command
  used `-C /tmp/r33fn1nl/repo`.
- `plans/round33_defects.py` sha256 constant at
  `6ef17abc…64d5b6`, mtime `14:06:40`; `plans/__pycache__/round33_defects.cpython-314.pyc`
  mtime `14:23` predates this seat's first run (`14:51`), so this seat wrote no
  bytecode — the check was always invoked as a script (`python3 <path> --lane`),
  never imported.
- Lane round-32 counts unchanged (`89` on disk / `89` tracked), zero
  control-character names; lane worktree's 17 pre-existing dirty entries belong
  to sibling seats and this seat did not touch them.
- Cross-references: `R33CounterAttack.md:120` (B7, falsified in §5),
  `R33ClaimsReview.md` residual-risk line (index-vs-commit), `R33FN1Index.md`
  (staged-not-committed, disjoint from this item).
