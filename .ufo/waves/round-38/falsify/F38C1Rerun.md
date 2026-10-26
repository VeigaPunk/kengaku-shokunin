# F38C1Rerun — attack on frozen C1 (calibration), round 38 wave 2

Seat: executor `F38C1Rerun`. Target: the round-38 C1 claim — 22 frozen gate mutants, `killed=21 survived=1`,
`PREDICATE C1 fail` (`plans/round-38-claims.md` §C1; freeze `e0a37853`). Attacked: the 21 kills, the N21
explanation, the "before" count, and the landing receipt itself. Read-only on the lane; every write is under
`/fast/scratch/hyaku/kengaku-r38/F38C1Rerun` (deleted at the end) or this report dir.

## 1. Setup — clean clone of the tip under attack

```
S=/fast/scratch/hyaku/kengaku-r38/F38C1Rerun; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
```
```
TOP=/fast/scratch/hyaku/kengaku-r38/F38C1Rerun/lane
HEAD=8c7422d7a646515d80af44844e8ecc8a1fc1d30a
STATUS_lines=0
```
(`receipts/reproduction-and-instrument.txt` §1.)

## 2. Re-run of the frozen C1 counter — reproduces the landing receipt byte for byte

```
cd "$S/lane" && python3 plans/round38_c1_verify.py --lane . --work "$S/w"   # exit=1
```
```
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
PREDICATE C1 fail
```
survivor: `MUTANT N21 D5 silence SURVIVED -- the capture digest is looked up in every manifest row, not only
the first [F37XMutD5 X3]`. 112 lines of output; the per-mutant `killed by=` cells are identical to the receipt
(`receipts/rerun-c1-r38.txt`).

Diff against `.ufo/waves/round-38/integrate/measure-final.txt` (its C1 block, minus the shell's trailing
`exit=1` echo):

```
diff -u <(sed '$d' measure-c1-block.txt) c1-r38.out && echo IDENTICAL
IDENTICAL
receipt_block_lines=113 rerun_lines=112
```

So: the counter's output at `8c7422d` is byte-identical to the receipt's; the predicate is red at 21/22, as
the L1 reports.

**Receipt-vs-tip gap (attack on "measured on a clean clone of the landing tip").** The receipt's own
`TIP` line names `d93b7d68`, not the tip under attack:

```
git diff --name-only d93b7d68 8c7422d | grep -v '^\.ufo/'
LOG.md
SCORECARD.md
corpus/lessons/round-38.md
git cat-file -p <tip>:plans/pkg_gate.py | sha256sum      # both tips
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
```
No pinned input (`plans/pkg_gate.py`, the counters, spec, battery37) changed between the measured tip and the
attack tip, and my run at `8c7422d` is byte-identical — the gap is a receipt-label imprecision, closed by this
re-run, not a reproducibility failure.

## 3. No-harm check — the round-37 counter still passes at this tip

```
cd "$S/lane" && python3 plans/round37_c1_verify.py --lane .    # exit=0
```
```
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```
(`receipts/rerun-c1-r37.txt`.) The frozen no-harm sentence holds.

## 4. The "before" count — do-nothing control reproduced

The claim's control (`claims/control-c1-nothing.txt`) is `killed=0 survived=22` on the freeze tree. My first
attempt used `--battery r37`, which is the counter's *dev* path and prints `PREDICATE C1 n/a`; the faithful
control is full mode with `plans/battery38` absent. In the clone (scratch only, restored afterwards):

```
mv plans/battery38 plans/battery38.absent
python3 plans/round38_c1_verify.py --lane . --work "$S/w"    # exit=1
mv plans/battery38.absent plans/battery38
```
```
PINS total=14 mismatched=0
BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0
PREDICATE C1 fail
```
`diff` of the four summary lines against `control-c1-nothing.txt` → no output (`CONTROL-IDENTICAL`,
`receipts/rerun-do-nothing-control.txt`). Before = 0/22, after = 21/22: the calibration delta is real.

## 5. Attack on the 21 kills — independent attribution pass

I wrote a harness that loads the lane's own fixtures and gate copies but records what the counter does not:
for **every** mutant, **every** fixture in the whole 86-fixture battery that attributes a kill (both
directions), the gate rc, and whether the mutant run died with a Python traceback
(`scripts/attrib.py`, `receipts/attrib-killers.txt`, `attrib-killers.json`).

```
N01 P1 silence killers=1 tb=[] ['b1run-n01-empty-pins']
N02 P3 mirror killers=1 tb=[] ['p3m-exact-min-distinct-locations']
...
N22 D5 silence killers=1 tb=[] ['d5m-n22-quote-prefix']
```
per mutant: `fid / declared / killers=1 / dirs / b38=True / rc=(ref,mut)`:

| mutant | declared | killer (1, unique over 86 fixtures) | dirs observed | ref→mut rc |
|---|---|---|---|---|
| N01 | silence | b1run-n01-empty-pins | silence | 1→0 |
| N02 | mirror | p3m-exact-min-distinct-locations | mirror | 0→1 |
| N03 | silence | p4a-second-row-line-outside | silence | 1→0 |
| N04 | silence | p4a-text-elsewhere | silence | 1→0 |
| N05 | silence | p4b-case-only | silence | 1→0 |
| N06 | silence | p4b-range-end-past-last | silence | 1→0 |
| N07 | silence | p5m-row-off-pin-later-row | silence | 1→0 |
| N08 | mirror | p5m-manifest-blank-line | mirror | 0→1 |
| N09 | silence | p6m-n09-teaches-one-below-min | silence | 1→0 |
| N10 | silence | p6m-n10-url-scheme-http | silence | 1→0 |
| N11 | silence | p7m-n11-empty-recheck | silence | 1→0 |
| N12 | silence | p7m-n12-first-row-url | silence | 1→0 |
| N13 | silence | p10a-n13-trailing-space | silence | 1→0 |
| N14 | silence | p10a-n14-first-line-only | silence | 1→0 |
| N15 | mirror | p10b-rerun-byte-equal-accept | mirror | 0→1 |
| N16 | silence | b1run-n16-clause-crash | silence, mirror | 1→0 |
| N17 | silence | mainx-root-not-a-directory | main (exit) | 2→1 |
| N18 | silence | mainx-spec-invalid-json | main (exit) | 2→0 |
| N19 | silence | d4m-n19-last-pattern-unmatched | silence | 1→0 |
| N20 | silence | d4m-n20-pattern-case-differs | silence | 1→0 |
| N21 | silence | d5m-n21-manifest-row-2 | **mirror only** | 0→1 |
| N22 | silence | d5m-n22-quote-prefix | silence | 1→0 |

Three properties the receipt does not state, now measured:

1. **Load-bearing / no free kills.** Each of the 22 mutants is separated by exactly **one** fixture out of 86.
   Deleting that fixture cannot leave the mutant killed, so no kill is a chance overlap — this is stronger
   than a delete-one-fixture test.
2. **No crash kills.** `tb=[]` for every mutant×killer: no kill is produced by a traceback that merely removes
   the clause line. Every mutant exits 0/1 as the attribution rule requires.
3. **The mutated sub-check is the one that flips.** `scripts/notes.py` prints the clause line of the reference
   and of the mutant on the killer fixture (excerpts, `receipts/attrib-clause-notes.txt`):

```
N01 ref P1 DEFECT pinned=0 mismatched=0            | mut P1 ok pinned=0
N03 ref P4 DEFECT checked=22 bad=1 first=test_outputs.py:1073-1073: line range outside the capture | mut P4 ok bad=0
N07 ref P5 DEFECT manifest_entries=6 bad=1 first=S107: manifest digest differs from the spec pin       | mut P5 ok
N09 ref P6 DEFECT rows=3 bad=1 first=S105: teaches words=7                                            | mut P6 ok
N13 ref P10 DEFECT fresh probe output is not byte-equal to the receipt                               | mut P10 ok probe_rerun=byte-equal bytes=52
N16 ref P3 DEFECT clause error ValueError: not enough values to unpack (expected 2, got 1)            | mut P3 ok clause error …
N22 ref D5 DEFECT directional=False bad=['quote absent from the capture']                              | mut D5 ok directional=True
```

The kill text matches the mutant's advertised sentence in every row I checked, and the note that flips is the
sub-check named in the `adv` cell.

**One instrument margin (found here, not claimed by the lane).** For the two `MAIN` mutants the counter's
attribution branch ignores the direction cell entirely (`plans/round38_c1_verify.py:195`):

```
attributed('MAIN', 'silence') = True
attributed('MAIN', 'mirror')  = True
attributed('MAIN', 'main')    = True
attributed('MAIN', 'garbage') = True
cells: [('N17','silence'), ('N18','silence'), ('N21','silence')]
```
and `plans/mutant_direction_check.py:81` echoes the *declared* name into `observed=` for `MAIN`, so its
`DIR N17 MAIN declared=silence observed=silence ok` line cannot detect a MAIN mislabel — the check is vacuous
for 2 of 22 mutants. The *kills* are still honest (exit 2→1 and 2→0, exit-code based, table above); the
direction cell for N17/N18 is inert rather than wrong. No count is affected.

## 6. Attack on the N21 explanation — "frozen as silence, only killable as a mirror"

The claim (task brief; `corpus/lessons/round-38.md` Mistakes row 1; wave-1 `R38BatD5` §BLOCKER) is that the
N21 replacement (`sums.splitlines()` → `sums.splitlines()[:1]`, counter line 140) makes D5 *stricter*, so a
silence witness cannot exist. I re-derived it independently.

**(a) Exhaustive manifest-shape enumeration** over the genuine capture and erratum line (the only two inputs
D5's pin test reads), rows from {genuine, decoy same-name, wrong-suffix, blank, junk}, lengths 0–3:
`scripts/n21_shapes.py`, `receipts/n21-manifest-shapes.txt`:

```
shapes=156 subset_violations=0 silence_witnesses=0 mirror_witnesses=40
```
i.e. on all 156 shapes the mutant's DEFECT set contains the reference's (mutant stricter), no `ref DEFECT ∧
mutant ok` exists, and 40 shapes give `ref ok ∧ mutant DEFECT` (mirror). Representative rows:

```
-     ref 1 D5 DEFECT          mut 1 D5 DEFECT          subset=True  silence=False mirror=False
G     ref 0 D5 ok              mut 0 D5 ok              subset=True  silence=False mirror=False
DG    ref 0 D5 ok              mut 1 D5 DEFECT          subset=True  silence=False mirror=True
```

**(b) Direct witness of the landed fixture** (`receipts/attrib-clause-notes.txt`):

```
== N21 D5 silence killer=d5m-n21-manifest-row-2
   ref   rc=0 | D5 ok directional=True  digest_pinned=True
   mut   rc=1 | D5 DEFECT directional=False digest_pinned=False bad=['capture digest is not the one in the manifest']
```

**(c) The decisive control: the battery is sufficient — the frozen cell is what refuses the kill.**
In a scratch copy of the counter with one token changed (`line 140: "silence"` → `"mirror"`; the lane file is
untouched) and the **full 86-fixture battery**:

```
python3 scratch/counter_n21_mirror.py --lane . --only N21 --work "$S/w"   # exit=0
MUTANT N21 D5 mirror killed by=d5m-n21-manifest-row-2 -- the capture digest is looked up in every manifest row, not only the first [F37XMutD5 X3]
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
```

So `killed=22` is reachable with the *landed* battery once the cell is relabelled; the stop is a one-cell
freeze defect, and the L1's description ("silence but only killable as a mirror… honest stop, not relabelled")
is accurate. I confirm the lane did not relabel: `plans/round38_c1_verify.py:140` at `8c7422d` still reads
`"silence"`, and `PREDICATE C1 fail` is printed.

## 7. Landing-battery review (the admission the counter cannot make)

`plans/battery38` = 12 modules, 919 lines, 22 fixtures (86 − 64). Imports are stdlib builders only — `hashlib`,
`json`, `pathlib`, `re`, `shutil`, `copy`; no `sys`, `os`, `subprocess`; no `sys.modules` / `__main__` /
monkeypatch / `ctx.lane` shapes (grep over all 12 modules). So the disclosed in-process-loader hole
(lesson, note on the C1 counter: a module can patch the counter's own globals, invisible to the token scan)
is not exercised by the landed battery — but the counter's `sidechannel=0` remains a token heuristic, and the
guard against that hole is code review, not the predicate. My pass above is that review for the shipped bytes.

## 8. Minor operability defect (no effect on the count)

`--work DIR` crashes if `DIR` does not exist: `tempfile.mkdtemp(..., dir=a.work)` →
`FileNotFoundError: … /w/k38-c1-s5z7cv9z` (first attempt). The documented invocation does not say to create it.
Creating `$S/w` first made the run proceed. Cosmetic; worth a docstring token next time the counter is touched.

## 9. Limits of this attack

* Attribution is judged at (exit code, DEFECT set, clause note) granularity; a mutant whose observable differs
  only inside the note text would be scored the same. The note diffs in §5 show the mutated sub-check, but I
  did not read all 919 battery lines line-by-line as an adversarial reviewer.
* My shape enumeration covers D5's pin test for one capture and one erratum line; it does not cover a capture
  whose bytes make `sha256` collide or a manifest with exotic whitespace beyond blank/decoy/junk rows.
* The `pkg_gate.py` digest was verified against the counter's pin and both tips, not against an upstream source.
* I ran on python3.14 on this host; the counter fixes the interpreter for the gate, so the rc/defect sets are
  interpreter-stable in the same sense as the receipt.

## 10. Tooling and cleanup

No tool installed (nothing needed; no pacman transaction, no `uv`/`npm`/binary install). Scratch
`/fast/scratch/hyaku/kengaku-r38/F38C1Rerun` deleted after the receipts were copied here; the clone was never
committed to, and `git status --porcelain` in it was empty at the end. No lane file, lane index, jj state, fleet
root or sibling lane was written.

Receipts in this directory: `rerun-c1-r38.txt`, `rerun-c1-r37.txt`, `rerun-direction-check.txt`,
`rerun-do-nothing-control.txt`, `rerun-battery-r37-flag.txt`, `reproduction-and-instrument.txt`,
`attrib-killers.txt`/`.json`, `attrib-clause-notes.txt`, `n21-manifest-shapes.txt`,
`n21-relabel-control.txt`, `measure-final-c1-block.txt`, `scripts/attrib.py`, `scripts/notes.py`,
`scripts/n21_shapes.py`, `scripts/counter_n21_mirror.py`.

VERDICT: c1-rerun-fail-killed-21/22
