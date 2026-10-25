# R33FN1SpecialFiles — N1 filesystem census vs special files (falsify seat)

- Seat: `KengakuR33.R33FN1SpecialFiles` (mutation tester, falsify wave, round 33, hyaku run 7)
- Date: 2026-10-25
- Frozen claim under test: round-33-claims.md **C2**, check **N1**: "every file under
  `.ufo/waves/round-32/` is git-tracked and **no untracked path remains beneath it**".
- Target artifact: `plans/round33_defects.py`, `check_n1()` — sha256
  `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6` (identical before and
  after all probes; the source was never opened for write — the detector ran from a copy).
- No tools installed; no lane/fleet file mutated, staged, or committed. All git commands
  explicitly scoped with `-C /tmp/r33fn1special/lane`.

## Detector surface (observed, unmodified source)

`check_n1` builds the on-disk set with
`find <lane>/.ufo/waves/round-32 -type f -printf '%P\n'` (no `-L`; default `-P`), the
tracked set with `git -C <lane> ls-files -- .ufo/waves/round-32`, and reports
`on_disk - tracked`. Only **regular files** can ever enter `on_disk`.

## Fixture and baseline (detector liveness)

`/tmp/r33fn1special/lane`, git repo (commit `0ab84db`, message
"fixture: tracked round-32 tree"), containing exactly
`.ufo/waves/round-32/subdir/tracked-a.txt` (sha256
`914e9b1e6acb954e186817ed12a0b63b8b36b61185730d48a5513fe3aa80b98f`) as a tracked file.

Detector run from the copy:

```
python3 -B -c "import sys; sys.path.insert(0,'/tmp/r33fn1special'); \
from pathlib import Path; from round33_defects import check_n1; \
print(repr(check_n1(Path('/tmp/r33fn1special/lane'))))"
```

- Pristine: `check_n1` → `''` (pass). `find -type f` → `['subdir/tracked-a.txt']`;
  `git ls-files` → `['.ufo/waves/round-32/subdir/tracked-a.txt']`; `git status --porcelain`
  → empty. Baseline passes, so all verdicts below are conclusive.
- Liveness on this fixture (regular untracked file redds N1): with
  `.ufo/waves/round-32/stray-regular.txt` present, `check_n1` →
  `'1 untracked files remain under .ufo/waves/round-32: stray-regular.txt'`.

## Probe A — untracked fifo under round-32

Mutation: `mkfifo .ufo/waves/round-32/subdir/untracked-fifo` (no index change).

- Expected detector (per frozen wording "no untracked path remains"): a defect line, exit 1.
- Observed: `check_n1` → `''` — **UNCAUGHT (surviving mutant / coverage escape)**.
  `find -type f` output unchanged (`['subdir/tracked-a.txt']`, rc=0), so the fifo never
  enters `on_disk`; `ls-files` unchanged. The `find` failure guard (`is not readable on
  disk`) does not fire — find exits 0.
- Calibration note: `git status --porcelain` was also empty here — git itself does not
  list an untracked fifo. N1 is blind in the same direction as git, but the on-disk tree
  does contain an untracked path that the census cannot ever enumerate.

## Probe B — untracked symlink under round-32

Mutation: `ln -s /tmp/r33fn1special/outside-target.txt .ufo/waves/round-32/subdir/untracked-link`.

- Observed: `check_n1` → `''` — **UNCAUGHT (surviving mutant / coverage escape)**.
  `find -type f` (default `-P`) lstats the link, which is type `l`, not `f`.
- Calibration: git **does** see it — `git status --porcelain` →
  `['?? .ufo/waves/round-32/subdir/untracked-link']` while N1 passes. This is a direct
  divergence between N1's census and git's: an untracked path git flags is invisible to N1.

## Probe C — symlinked root directory (`.ufo/waves/round-32` itself a symlink)

Mutation: moved the real `round-32` tree aside, replaced it with a symlink to
`/tmp/r33fn1special/round32-real/` containing `subdir/tracked-a.txt` (same bytes) plus
`extra-untracked.txt` ("untracked bytes hidden behind root symlink"). Index unchanged.

- Observed: `check_n1` → `''` — **UNCAUGHT (surviving mutant / coverage escape)**.
  `find <lane>/.ufo/waves/round-32 -type f -printf '%P\n'` → empty output, rc=0
  (with `-P`, find does not descend a symlinked starting point), so `on_disk = ∅` and
  `on_disk - tracked = ∅` regardless of what the symlink target holds.
- Calibration: git reports the breakage — `git status --porcelain` →
  `[' D .ufo/waves/round-32/subdir/tracked-a.txt', '?? .ufo/waves/round-32']` — while N1
  passes. The "not readable on disk" guard does not fire because find exits 0 with no
  output; N1 cannot distinguish "empty/clean tree" from "root replaced by a symlink".

## Control — lane root reached via a symlink (no escape, no behavior change)

With `/tmp/r33fn1special/lane-link -> lane`: pristine `check_n1(lane-link)` → `''`; with a
regular untracked file present → `'1 untracked files remain under .ufo/waves/round-32:
stray-regular.txt'`. Lane-root aliasing changes nothing on either side; it is not a
defect vector for N1 (recorded to separate it from probes A–C).

## Restoration evidence

- Working-tree manifest (types + sha256 per path, `.git` excluded) after removing fifo and
  symlink and moving the real `round-32` tree back: **byte-identical to pristine**
  (`RESTORED manifest matches pristine working tree: True`).
- `check_n1` after restore → `''` (matches pristine baseline).
- `plans/round33_defects.py` sha256 before `6ef17abc…7064d5b6` == after
  `6ef17abc…7064d5b6`. Detector copy hash identical to source.
- Sandbox `/tmp/r33fn1special/` left in place as the disposable fixture; no lane path
  other than this report file was written.

## Verdict

All three assigned mutants **survive** N1 as implemented:

| Probe | Mutant | Detector output | Verdict |
|---|---|---|---|
| A | untracked fifo under `round-32` | `''` (pass) | uncaught |
| B | untracked symlink under `round-32` | `''` (pass; git shows `??`) | uncaught |
| C | `round-32` root replaced by symlink | `''` (pass; git shows ` D` + `??`) | uncaught |
| ctrl | lane root via symlink | unchanged on both sides | no effect |

This corroborates build-wave rows E1c/E1d (R33CounterAttack.md, marked GAMED) and
limitation B5 ("`find -type f` ignores non-regular files… and a symlinked
`.ufo/waves/round-32` root"): N1's frozen wording "no untracked path remains beneath it"
is broader than what its `find -type f` / `ls-files` comparison can observe. Per the
kill-rule framing this is a coverage finding against the counter's census, not a change
to the C2 contract; the C2 freeze predicate's counting command is unchanged by this seat.
