# F38CritN21 — is N21's frozen `silence` direction unreachable, or is C1's honest stop a missing fixture?

Seat: critic `F38CritN21` (leaf). Under attack: the L1's N21 explanation —
`plans/round38_c1_verify.py:140` freezes `("N21", "D5", "silence", …)` with
`sums.splitlines()` → `sums.splitlines()[:1]` in `plans/pkg_gate.py` `cmd_d5`, and the landing reports
`MUTANT N21 D5 silence SURVIVED`, `MUTANTS total=22 killed=21 survived=1`, `PREDICATE C1 fail`
(`.ufo/waves/round-38/integrate/measure-final.txt`) plus the claim that it is "only killable as a mirror",
"not a missing fixture" (`.ufo/waves/round-38/build/R38BatD5.md` §BLOCKER) and "unreachable by any battery"
(`corpus/lessons/round-38.md:35`).

Lane clone: `git clone --no-local` of `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a`; `git -C "$S/lane" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r38/F38CritN21/lane`; `git status --porcelain | wc -l` → `0`. The counter at the
tip is byte-identical to the freeze: `sha256sum plans/round38_c1_verify.py` →
`8069739990c7d3a87f34f4398ea5dc78821193d9fa55499e11e28c84e79c0a4f`, the same line in
`.ufo/waves/round-38/claims/frozen-digests.txt`. `plans/pkg_gate.py` → `ea638822…` = the C1 `PINS` value.

## 1. The code argument — the mutant's DEFECT set contains the reference's on every input

`plans/pkg_gate.py:346-351` (clone):

```
        sums = read(capdir / d5["manifest_name"]) or ""
        pinned = any(len(parts) >= 2 and parts[0] == digest
                     and parts[-1].endswith(d5["capture_name"])
                     for parts in (row.split() for row in sums.splitlines()))
        if not pinned:
            bad.append("capture digest is not the one in the manifest")
```

The only difference in the mutant is line 349 — `diff` of my generated mutant against the frozen gate:

```
$ diff lane/plans/pkg_gate.py scratch/exhwork3/gates/N21.py
349c349
<                      for parts in (row.split() for row in sums.splitlines()))
---
>                      for parts in (row.split() for row in sums.splitlines()[:1]))
$ sha256sum scratch/exhwork3/gates/N21.py
22b968514644f7cafb9918356ef6b1a4e62b631448833f08b027aebda8583974
```

Let `S = sums.splitlines()`, `P(row)` the per-row predicate. The mutant's row sequence is
`S[:1]`, a **prefix** of the reference's `S`, and `P` is identical, so
`pinned_mut ⇒ pinned_ref` (a match on the first row is a match). `pinned` enters the clause at exactly one
place, `if not pinned: bad.append(…)`; every other defect source — the erratum-line returns/label/`require`/
`forbid` (lines 332-340), the `digest is None` early return (344-345) and the quote test (352-354) — is
outside the replaced text and byte-identical. Hence `bad_ref ⊆ bad_mut` and (`bad == []`) ⇔ `D5 ok`, so

> a silence kill needs `ref = D5 DEFECT ∧ mut = D5 ok`, i.e. `bad_ref ≠ ∅ ∧ bad_mut = ∅`, which contradicts
> `bad_ref ⊆ bad_mut`.

Equivalently: the mutation is monotone *toward rejection*; it can only ever add the pin defect, so it is a
mirror-direction mutant by construction. Not equivalent, never laxer.

## 2. Counterexample hunt — the four named shapes, plus exhaustive and randomized sweeps

I built the four classes the ticket names (multi-line manifests, duplicate names, digest collisions,
unreadable capture) and swept them three ways against the real gate and the real mutant, in-process via each
gate's own `cmd_d5` (same code path the counter runs through `python3 <gate> d5-line`).

**(a) Structured matrix, 23 manifest shapes × 7 capture shapes × 6 erratum shapes = 966 cases**
(`probe_n21_semantics.py`; receipt `matrix-966.txt`):

```
CASES 966
I1 superset violations (mut DEFECT, ref not DEFECT) = 14
I2 silence signatures (ref DEFECT, mut ok) = 0
MIRROR witnesses (ref ok, mut DEFECT) = 14
RC DIFFERENCES = 14
```

(The driver's `I1` label is inverted: those 14 are the *mirror* signature — mutant strict where the reference
passes — i.e. the superset property holding, not breaking. The property under test is `I2`.)

Manifest shapes covered: absent, empty, `"\n"`, genuine-row-1, decoy-1/genuine-2, genuine-1/decoy-2,
genuine-twice (duplicate names), digest-only row, `digest *name` binary marker, **digest with a decoy name
only (digest collision: the digest matches, the name does not)**, path-suffix name (`sub/<capture>`),
wrong suffix (`<capture>.bak`), genuine-row-3, blank-1/genuine-2, whitespace-1/genuine-2, CRLF row 2,
comment-1/genuine-2, tab-separated, no trailing newline, two rows with the genuine digest and different
names, name followed by junk, invalid-UTF-8 bytes, directory-as-manifest. Capture shapes: genuine, missing,
directory, empty, non-UTF-8 binary, `quote[:20]`, tag-split quote. The 14 mirror witnesses are exactly the
shapes where the matching row is not the first *while the rest of the input still passes*; the 952 remaining
cases are identical in (rc, clause verdict), including every unreadable-capture case (both gates return at line 344-345
before the manifest is read).

**(b) Exhaustive over a 10-row alphabet, all row sequences of length 0..3 = 1111 cases**
(`probe_n21_exhaustive.py`; receipt `exhaustive.txt`; genuine capture + genuine erratum so the accept space
is reached):

```
EXHAUSTIVE {'cases': 1111, 'silence': 0, 'mirror': 378, 'identical': 733} alphabet 10 rows<=3
  first mirror shapes: [('Dd', 'G'), ('Dd', 'G2'), ('Dd', 'Gpath'), ('X', 'G'), ('X', 'G2'), ('X', 'Gpath'), ('Z1', 'G'), ('Z1', 'G2')]
  silence shapes: []
```

Alphabet: `G`/`G2` genuine row, `Gpath` suffixed name, `Dd` digest with decoy name, `X` zero-digest genuine
name, `Z1` one-field digest, blank line, whitespace-only line, name+junk, `H` zero-digest name.

**(c) 4000 randomized inputs** (`probe_n21_fuzz.py`; receipt `fuzz-4000-and-battery.txt`), capture body
weighted to the genuine capture so the accept space is exercised:

```
FUZZ {'cases': 4000, 'silence': 0, 'mirror': 24, 'identical': 0, 'both_defect': 3942, 'mut_ok_ref_ok': 34}
```

Sum check: 24 mirror + 3976 identical (3942 both-defect + 34 both-ok) = 4000; the receipt's `'identical'`
field is unused, the two classes are counted separately. Across (a)+(b)+(c): **6077
inputs, 0 silence signatures**. The same receipt re-runs the whole battery's `d5-line` family (12 fixtures):

```
D5-LINE FIXTURES 12
   … r36-L4, r36-L5, r36-L6, d5-m48, d5-m49, d5-m50, d5-m51, d5-m52, d5-m53, d5-m55, d5m-n22-quote-prefix:
      ref tuple == mut tuple ("same")
   d5m-n21-manifest-row-2           ref rc=0 D=- | mut rc=1 D=D5 DIFFERS silence=False mirror=True
  silence-count: 0  mirror-count: 1
```

No fixture in the battery's `d5-line` family — the only family the counter runs for a `D5` mutant — exhibits the
silence signature for N21; exactly one (`d5m-n21-manifest-row-2`) exhibits the mirror signature.

## 3. Hand-run of N21 outside the counter on `d5m-n21-manifest-row-2`

`probe_n21_handrun.py` builds the battery's own fixture with the counter's real `Ctx`, then runs the real CLI
for both gates (no counter code in the measurement loop; `run_gate` only re-parses to cross-check). Receipt
`handrun-cli.txt`:

```
FIXTURE d5m-n21-manifest-row-2 expect= accept declared= []
MANIFEST bytes:
0000000000000000000000000000000000000000000000000000000000000000  geniac-s105-reopen.html\n
b60af7757074df9d0795f1fcb76a7f6eaf5e4d6470eb8a6c97571eceb9a262b1  nec-s091-reopen.html\n

-- ref rc=0
   | D5 ok directional=True digest_pinned=True bad=0
-- N21 rc=1
   | D5 DEFECT directional=False digest_pinned=False bad=['capture digest is not the one in the manifest']

-- counter predicate over this one fixture (declared dir: silence )
   silence:  False
   mirror:  True
   ref tuple (0, frozenset(), frozenset({'D5'}))
   mut tuple (1, frozenset({'D5'}), frozenset())
```

The mirror kill is confirmed independently: reference exits 0 with `D5 ok`, the mutant exits 1 with
`D5 DEFECT`, and the counter's own `attributed("D5", "silence", …)` is `False` while
`attributed("D5", "mirror", …)` is `True`.

## 4. My own control: the conviction is a one-cell freeze error, not a calibration gap

In a scratch copy of the counter (only `("N21", "D5", "silence",` → `("N21", "D5", "mirror",`; the frozen
lane file is untouched) run on the untouched landing clone (`control-corrected-cell.txt`):

```
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N21 D5 mirror killed by=d5m-n21-manifest-row-2 -- the capture digest is looked up in every manifest row, not only the first [F37XMutD5 X3]
MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

That reproduces the L1's post-hoc diagnostic (`.ufo/waves/round-38/integrate/n21-mirror-diagnostic.txt`)
without using it: all 22 frozen mutants are killed by the battery that landed; only the frozen **direction
cell** blocks the predicate. The frozen cell is unchanged at the tip (`git show 8c7422d7:plans/round38_c1_verify.py
| grep '"N21"'` → `("N21", "D5", "silence", …`), so the stop is not a relabel after scoring.

**Answer to the ticket's question: the honest stop is real; it is not a missing fixture.** No fixture can
satisfy the silence rule, and the fixture that demonstrates the defect already exists and is the one that
kills N21 under the reachable direction.

## 5. Attacking the explanation itself — two defects, one of them a wording overclaim

**D1 (wording, minor).** The lesson, QUALITY Q29 and the check's docstring state the mutant "makes D5
stricter on every input" (`corpus/lessons/round-38.md:35`; `corpus/QUALITY.md:506-507`: "makes the clause
stricter on every input, so its DEFECT set always contains the reference's"). The superset half is right; the
"on every input" half is false — the mutant is *identical* wherever the first manifest row already decides
(733/1111 exhaustive, 3976/4000 randomized, 952/966 matrix, identical in rc and clause verdict). Smallest correction: "never laxer; identical
wherever the first row already decides" (the docstring's own "STRICTER, never laxer" is already consistent).
No axis moves on this; it matters because lesson rows are reused as freeze rules.

**D2 (process, calibration-relevant).** QUALITY Q29's rule is executable only *after* a battery exists: the
check's own limit reads "`UNWITNESSED` … is not a verdict, so the check cannot run before some battery
exists" (`corpus/QUALITY.md:516-517`). So the rule as written cannot guard the freeze it is aimed at — N21
consumed the round's C1 even though the polarity was decidable from the source at freeze time. The freeze
list in fact contains the discriminating contrast: `N03`, `N07`, `N12`, `N14` all restrict "first row only"
inside a *defect-accumulating* loop and are correctly `silence` (`direction-check.txt`: every one `ok`); N21
is the only one whose restriction lands inside `any(...)`, which inverts the polarity. Smallest correction
for the next freeze: state the polarity argument per mutant (`[:1]`/`[1:]` inside `any()` ⇒ mirror;
inside an accumulating `for` ⇒ silence) and keep `mutant_direction_check.py` as the post-battery control.

**What the explanation gets right** (not a finding, recorded because it was checked): the survivor is not
equivalent (378/1111 shapes differ), it is reported as a limit and kept in the list, the counter stayed red
(`PREDICATE C1 fail`), the mutant row was not edited, and the diagnostic is labelled "NOT the frozen C1 rule
and NOT a claim result". Nothing in `PROVINCE.md`/`SCORECARD.md` presents `killed=21` as a calibration gap
(`grep -n "N21" PROVINCE.md` → no match).

## 6. Reachability boundary — the one construction that would produce the signature

The only way to make the reference print `D5 DEFECT` while the mutant prints `D5 ok` is to have the two
processes read *different manifest bytes*: the invariant is about one input, and the counter builds each
fixture once and re-runs the same argv for reference and mutants. Such an input is out of contract and does
not survive the counter: a named-pipe manifest (the obvious stateful read) breaks the renamed re-run —

```
$ shutil.copytree(dir_with_fifo, dst)
copytree raised Error : [… '…/quarantine-SHA256SUMS' is a named pipe]
```

and a pipe would also make `read_gate` return `("timeout", …)` at `timeout=900`, which `attributed()` rejects
for both directions. A timed in-process rewrite of the fixture directory (the module-import door that
`R38CritClaims` measured reaches `killed=20` with a monkeypatched `run_gate`) is the same class and is
already named as the counter's limit in `corpus/lessons/round-38.md`; producing N21's silence signature that
way would still not be attributable to the mutation. [INFERENCE] I did not build that hostile fixture: it is
the documented monkeypatch door, not a new one.

## Findings, axes, corrections

| # | finding | axis | smallest safe correction |
|---|---|---|---|
| C1 | The frozen `silence` direction of N21 is unreachable **as a property of the gate code**: `pinned_mut ⇒ pinned_ref`, `bad_ref ⊆ bad_mut`, so `ref DEFECT ∧ mut ok` is a contradiction. 6077 enumerated inputs (966 structured incl. all four ticket shapes, 1111 exhaustive, 4000 randomized), 0 silence signatures; 12/12 battery `d5-line` fixtures show none. | calibration (confirms the honest stop) | none — the frozen row stays as reported |
| C2 | It is **not a missing fixture**: `d5m-n21-manifest-row-2` (declared `accept`, ref `D5 ok`) is the mirror kill, hand-run confirmed, and the battery kills all 22 under the reachable direction (`killed=22`, `PREDICATE C1 pass`). | calibration / depth | when citing the stop, pair `PREDICATE C1 fail` with `n21-mirror-diagnostic.txt` (already landed) |
| D1 | "makes D5 stricter on every input" is false (66% of enumerated inputs are identical); text fix only. | depth (claim precision) | reword to "never laxer; identical wherever the first row already decides" |
| D2 | Q29's check cannot run at freeze, and the freeze list contained the polarity contrast (`N03/N07/N12/N14` vs `N21`) that would have caught it. | calibration (freeze procedure) | add the polarity argument per mutant to the freeze statement; keep the executable check post-battery |

Nothing here changes C1's verdict, the gate, the battery or the frozen list; the honest stop stands.

## Receipts

All under `.ufo/waves/round-38/falsify/F38CritN21/`:
`matrix-966.txt`, `exhaustive.txt`, `fuzz-4000-and-battery.txt`, `handrun-cli.txt`, `control-corrected-cell.txt`.
Driver scripts lived in `/fast/scratch/hyaku/kengaku-r38/F38CritN21/` (`probe_n21_semantics.py`,
`probe_n21_exhaustive.py`, `probe_n21_fuzz.py`, `probe_n21_handrun.py`) and were removed with the scratch
directory. No lane file, Git index, jj state, fleet-root file, sibling lane or corpus/plans tree was written
or copied; all git calls used `-C "$S/lane"`; the scratch dir
`/fast/scratch/hyaku/kengaku-r38/F38CritN21` was deleted. No tool was installed (pacman is paused host-wide
and none was needed).

VERDICT: n21-silence-unreachable
