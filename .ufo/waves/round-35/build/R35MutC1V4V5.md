# R35MutC1V4V5 — mutation test of C1 checks V4 and V5 (round 35, wave 1, 2026-10-25)

Seat: mutation-tester, leaf. Target: `plans/round35_c1_verify.py` checks V4 (index/coverage/42-42)
and V5 (probe receipt byte-equality + green summary + entry carries summary) against the frozen C1
predicate (`checks=6 defects=0`, `PREDICATE C1 pass`, exit 0).

## Fixture (passing package)

Per the fixture rule: `D=$(mktemp -d /tmp/k35-XXXX)` → `/tmp/k35-h1HI`;
`git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/k35-h1HI/lane`;
`git -C /tmp/k35-h1HI/lane sparse-checkout set --no-cone '/corpus/**' '/plans/**'`;
`git -C /tmp/k35-h1HI/lane checkout -q master` (master = freeze commit `11d6453`);
`git -C /tmp/k35-h1HI/lane rev-parse --show-toplevel` = `/tmp/k35-h1HI/lane` (verified before any write).
Package copied from the lane's uncommitted round-35 state: `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/tb2-protein-assembly-grader.md`, `corpus/evidence/round35/tb2-eval/`,
`corpus/evidence/round35/tb2-grader-probe.txt`; the new entry was staged with
`git -C /tmp/k35-h1HI/lane add corpus/knowledge/tb2-protein-assembly-grader.md` (fixture only, never
committed) so V4's `git ls-files` count sees it: `staged knowledge files: 42`.

Baseline detector (`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round35_c1_verify.py
--lane /tmp/k35-h1HI/lane`, the same command for every probe below):

```
V1 ok / V2 ok / V3 ok / V4 ok / V5 ok / V6 ok
checks=6 defects=0
PREDICATE C1 pass
exit=0
```

Baseline conclusive, so every kill below is a real kill. Pristine sha256 (restoration anchors):
README `fd5568b8…f03f56`, SOURCES `a00684a4…1da1a`, entry `bce2be7e…2630d0`,
receipt `2359d906…25b8`, probe `acd7d38d…040d0` (full digests at bottom).

## Mutants

Detector output is quoted verbatim (only lines that changed from baseline are shown; all other
checks stayed `ok`). After each probe the mutated file was restored with `cp` from a pristine copy
and verified with `cmp` (silent) + `sha256sum` equal to the pristine digest — `RESTORED-OK` on all
eight. The fixture was `rm -rf`'d after the final restore; the lane was never written to.

### M1 — index row without S106 → KILLED
`corpus/README.md:68` last cell `| S105, S106, S107 (terminal-bench-2 @ 2fd12b88) |` → `| S105, S107 … |`.
Expected: V4 index-row clause. Observed: `V4 DEFECT index row absent or missing S105/S106/S107`,
`checks=6 defects=1`, `PREDICATE C1 fail`, `exit=1`. Restored: sha256 `fd5568b8…f03f56` = pristine.

### M2 — coverage bullet removed → KILLED
Deleted the whole round-35 bullet at `corpus/README.md:257` (§Coverage map).
Expected: V4 coverage clause. Observed: `V4 DEFECT coverage-map bullet absent`, `defects=1`,
`PREDICATE C1 fail`, `exit=1`. Restored: `fd5568b8…f03f56` = pristine.

### M3 — a 43rd knowledge file → KILLED (tracked form); untracked form SURVIVES
Primary (in-contract) form: `corpus/knowledge/zzz-r35-mutant-stray.md` created and staged
(`git add`, fixture only). Expected: V4 42/42 clause. Observed: `V4 DEFECT knowledge files=43
index rows=42 (want 42/42)`, `defects=1`, `PREDICATE C1 fail`, `exit=1`. Restored:
`git rm --cached` + `rm`; `git ls-files 'corpus/knowledge/*.md' | wc -l` → 42.
Secondary observation (untracked stray, no `git add`): `V4 ok … checks=6 defects=0 PREDICATE C1
pass, exit=0` — **survives**. V4 counts only `git ls-files` (index) files, so an untracked stray
knowledge file on disk is invisible to it. Coverage finding, not a contract change: the docstring
says "committed knowledge files", so this is in-contract behavior; the L1 may want an
untracked-file guard (`git status --porcelain corpus/knowledge/`) if stray files matter.

### M4 — index row duplicated → KILLED
Inserted an exact copy of `corpus/README.md:68` directly after it (two identical rows).
Expected: V4 `len(idx) != 1` clause. Observed: `V4 DEFECT index row absent or missing
S105/S106/S107`, `defects=1`, `PREDICATE C1 fail`, `exit=1`. Restored: `fd5568b8…f03f56` = pristine.

### M5 — one byte changed in the receipt → KILLED
`corpus/evidence/round35/tb2-grader-probe.txt` line 4: `case=uppercase … match=yes` → `match=yez`
(single byte `s`→`z`, mid-file, away from the summary line).
Expected: V5 byte-equality clause. Observed: `V5 DEFECT fresh probe output differs from receipt
(exit 0)`, `defects=1`, `PREDICATE C1 fail`, `exit=1`. Restored: `2359d906…25b8` = pristine.

### M6 — receipt line reordered → KILLED
Swapped receipt lines 4 and 5 (`case=uppercase` ↔ `case=no-trailing-newline`; both `match=yes`, so
only order changed).
Expected: V5 byte-equality clause. Observed: `V5 DEFECT fresh probe output differs from receipt
(exit 0)`, `defects=1`, `PREDICATE C1 fail`, `exit=1`. Restored: `2359d906…25b8` = pristine.

### M7 — summary line removed from the entry → KILLED
Deleted entry line 19 (`` `cases=18 observed_pass=5 observed_fail=13 mismatches=0` ``).
Expected: V5 verbatim-carry clause. Observed: `V5 DEFECT entry does not carry the receipt summary
line verbatim`, `defects=1`, `PREDICATE C1 fail`, `exit=1`. Restored: `bce2be7e…2630d0` = pristine.

### M8 — probe altered to print `mismatches=0` always → SURVIVED
`plans/tb2_grader_probe.py:158` `mism += not ok` → `mism += 0` (the probe now never counts a
mismatch and always exits 0, while still printing honest per-case `match=` fields).
Expected (if V4/V5 had an independent oracle): V5 red. Observed: `V4 ok / V5 ok`,
`checks=6 defects=0`, `PREDICATE C1 pass`, `exit=0` — **survives**.
Why: V5's oracle is the probe itself — it re-runs `plans/tb2_grader_probe.py` and byte-compares the
output with the committed receipt. A probe mutated to always claim `mismatches=0` is self-consistent
with a receipt that was generated by the same probe (here the natural run already has
mismatches=0, so the mutated output is byte-identical). Nothing in the counter pins the probe's
bytes: V1 pins only the three `tb2-eval/` captures, and no check hashes `plans/tb2_grader_probe.py`.
Coverage finding for the L1 (observation only, contract unchanged): V5 cannot detect a lying probe;
pinning the probe's sha256 in the counter (the way `FILES` pins the captures) or moving the
mismatch computation into the counter would close it.

## Restoration evidence

After the final restore, one more baseline run: `V1 ok … V6 ok, checks=6 defects=0, PREDICATE C1
pass, exit=0`. Pristine vs restored sha256 (identical pairs):

```
fd5568b83e73ea37237c39376c7bd0f69d5b04a5ba97a8013e800c57d4f03f56  pristine/README.md == lane/corpus/README.md
a00684a42d0effda23a036fadf35e1657646b3a66cd2c7b00755e69de491da1a  pristine/SOURCES.md (never mutated)
bce2be7e50d79585e5d2baa15f246125206dffcc767ed253474dc56cf72630d0  pristine/entry.md == lane/corpus/knowledge/tb2-protein-assembly-grader.md
2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8  pristine/receipt.txt == lane/corpus/evidence/round35/tb2-grader-probe.txt
acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0  pristine/probe.py == lane/plans/tb2_grader_probe.py
```

Teardown: `rm -rf /tmp/k35-h1HI` → `ls: cannot access '/tmp/k35-h1HI': No such file or directory`.
No lane file, no lane git/jj state was touched; no commits anywhere; build script kept at
`.ufo/waves/round-35/build/R35MutC1V4V5/build-fixture.sh`.

## Score

8 assigned mutants: 7 killed (M1, M2, M3-tracked, M4, M5, M6, M7), 1 survived (M8). Secondary
observation: M3-untracked survives V4. No baseline failures; no inconclusive probes.

VERDICT: v4v5-killed-7/8
