# F38CritBatF — attack on battery38 `d4m` / `d5m` (wave 2, falsify)

Seat: critic `F38CritBatF` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip under attack
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a`. Scratch clone:
`/fast/scratch/hyaku/kengaku-r38/F38CritBatF/lane` (`git -C … rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r38/F38CritBatF/lane`). Every command below was run from that clone; nothing in the
lane was written.

Question attacked: for each fixture of `plans/battery38/d4m.py` (mutants N19, N20) and `plans/battery38/d5m.py`
(N21, N22), does it demonstrate the **advertised** behaviour named in the frozen `adv` cell of
`plans/round38_c1_verify.py` MUTANTS, or does it kill incidentally — a tailored `defects` declaration, a spec the
gate would never see, a second clause doing the work, a side channel the token scan misses, or fixture-name keying?
Plus: is the N21 `silence`→mirror explanation sound?

**Two defects** (§6), both pin/provenance claims, not fixture mechanics. The four fixtures themselves survive the
attack: each kill is single-cause, single-fixture, and attributable (§2–§4); the N21 unreachability claim is
confirmed, not falsified (§5).

---

## 0. Setup

```
$ git clone -q --no-local …/kengaku-shokunin "$S/lane" && git -C "$S/lane" checkout -q 8c7422d7a646515…
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r38/F38CritBatF/lane
$ git -C "$S/lane" rev-parse HEAD
8c7422d7a646515d80af44844e8ecc8a1fc1d30a
$ sha256sum plans/pkg_gate.py plans/battery38/d4m.py plans/battery38/d5m.py
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  plans/pkg_gate.py   # = freeze digest
4fd34339ab32627b65b2fd7ff11f0d1b99c45b02598c8591468b2badbc0d4488  plans/battery38/d4m.py
5af18f40f7543fd60c8f4926b8f73553804fd428e91d3700a40f351d3d4ddbd7  plans/battery38/d5m.py
```

Landing-receipt provenance check (the receipt names a different TIP):

```
$ git merge-base --is-ancestor d93b7d68dacfd6a23ec2cf732a4615d6c732c73e 8c7422d7…
d93b7d6 is ancestor of 8c7422d7
$ git diff --stat d93b7d6 8c7422d7 -- plans/battery38 plans/round38_c1_verify.py plans/pkg_gate.py
(no output)
```

So `measure-final.txt:1 TIP d93b7d68…` predates the tip under attack by two commits, but the three files the C1
calibration reads are byte-identical between them, and my own run at `8c7422d7` reproduces the receipt's four
MUTANT lines (§1). The receipt's numbers bind at the tip; its stated TIP does not name it.

## 1. Baseline: the four mutants at the tip under attack

```
$ S=/fast/scratch/hyaku/kengaku-r38/F38CritBatF; export TMPDIR="$S"
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --only N19,N20,N21,N22 --work "$S/w_a"
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N19 D4 silence killed by=d4m-n19-last-pattern-unmatched -- every directional pattern is checked, the last included [F37XMutD4 X3]
MUTANT N20 D4 silence killed by=d4m-n20-pattern-case-differs -- directional patterns match case-sensitively [F37XMutD4 X4]
MUTANT N21 D5 silence SURVIVED -- the capture digest is looked up in every manifest row, not only the first [F37XMutD5 X3]
MUTANT N22 D5 silence killed by=d5m-n22-quote-prefix -- the whole quote must be present, not a 20-character prefix [F37XMutD5 X4]
MUTANTS total=4 killed=3 survived=1 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=1
```

Same command into a second work dir is byte-equal (`cmp` exit 0, `exit_b=1`) — deterministic.
Receipts: `F38CritBatF/run_a.txt`, `run_b.txt`.

## 2. Per-fixture necessity — delete each fixture, its mutant must survive

Variants are scratch copies of `plans/battery38` (`$S/b38_<v>`), handed to the real counter with
`--battery-dir`; per-fixture variants keep one `FIXTURES` entry (`FIXTURES = [f for f in FIXTURES if …]`
appended to the module copy). Command shape:

```
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --battery-dir "$S/b38_<v>" \
    --only N19,N20,N21,N22 --work "$S/w_<v>"
```

| variant (scratch battery) | BATTERY | MUTANT result |
|---|---|---|
| `full` (control) | `fixtures=86 wrong=0` | N19 killed by `d4m-n19-…`, N20 killed by `d4m-n20-…`, N21 **SURVIVED**, N22 killed by `d5m-n22-…` |
| `no_d4m` (module deleted) | `fixtures=84` | **N19 SURVIVED**, **N20 SURVIVED**, N21 SURVIVED, N22 killed by `d5m-n22-…` |
| `no_d5m` (module deleted) | `fixtures=84` | N19 killed, N20 killed, N21 SURVIVED, **N22 SURVIVED** |
| `n19` (only `n19` fixture) | `fixtures=85` | N19 killed, **N20 SURVIVED**, N21 SURVIVED, N22 killed |
| `n20` (only `n20` fixture) | `fixtures=85` | **N19 SURVIVED**, N20 killed, N21 SURVIVED, N22 killed |
| `n21` (only `n21` fixture) | `fixtures=85` | N19 killed, N20 killed, N21 SURVIVED, **N22 SURVIVED** |
| `n22` (only `n22` fixture) | `fixtures=85` | N19 killed, N20 killed, N21 SURVIVED, N22 killed |

Elided lines are verbatim in `F38CritBatF/del-<variant>.txt`. Reading: each of the three kills (N19, N20, N22) is
produced by exactly one fixture, and removing that one fixture makes its mutant survive while the other two kills
stand. No fixture is a spare; no fixture's kill is a side-effect of another fixture's bytes.

## 3. Does each fixture kill for the *advertised* reason? (cross matrix)

Each fixture (built by the module's own `build`, with the same `Ctx` the counter uses) was run against the
reference gate and against all four mutant gates; observables are the counter's own `(rc, DEFECT set, ok set)`.

```
fixture                            expect  decl   ref        N19        N20        N21        N22
d4m-n19-last-pattern-unmatched     reject  D4     1/D4       0/-        1/D4       1/D4       1/D4
d4m-n20-pattern-case-differs       reject  D4     1/D4       1/D4       0/-        1/D4       1/D4
d5m-n22-quote-prefix               reject  D5     1/D5       1/D5       1/D5       1/D5       0/-
d5m-n21-manifest-row-2             accept  -      0/-        0/-        0/-        1/D5       0/-
```

(`F38CritBatF/matrix.txt`.) Every fixture separates **exactly one** mutant; no cross-kill, so none of the four
kills is the counter's loop picking up a neighbour's difference. Gate stdout proves the *sub-cause* is the one
the `adv` cell names, not a second clause doing the work:

```
d4m-n19-last-pattern-unmatched [ref] rc=1  D4 DEFECT patterns=3 failed=['pattern3'] | defects=1
d4m-n19-last-pattern-unmatched [N19] rc=0  D4 ok patterns=3 failed=0 | defects=0
d4m-n20-pattern-case-differs   [ref] rc=1  D4 DEFECT patterns=3 failed=['pattern1'] | defects=1
d4m-n20-pattern-case-differs   [N20] rc=0  D4 ok patterns=3 failed=0 | defects=0
d5m-n22-quote-prefix           [ref] rc=1  D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture'] | defects=1
d5m-n22-quote-prefix           [N22] rc=0  D5 ok directional=True digest_pinned=True bad=0 | defects=0
d5m-n21-manifest-row-2         [ref] rc=0  D5 ok directional=True digest_pinned=True bad=0 | defects=0
d5m-n21-manifest-row-2         [N21] rc=1  D5 DEFECT directional=False digest_pinned=False bad=['capture digest is not the one in the manifest'] | defects=1
```

Notes: the label check, the line-count check and (for D5) `directional` are identical in reference and mutant in
every row — only the sub-check the mutant touches moves. `patterns=3` is printed identically by N19 (the mutant
narrows the loop, not the count), so the D4 kills are not visible through the printed count. Each mutant's own
gate prints an explicit `ok` line, so the three kills are not crash-based silences (which the counter's silence
rule would also accept).

`defects` declarations are not tailored: `d4-line` and `d5-line` each run exactly one clause
(`plans/pkg_gate.py:315-355`, printed by `run_checks`), so `["D4"]` / `["D5"]` / `[]` is the only declaration the
subcommand can produce, and the counter's `wrong=0` compares the full DEFECT set, not a subset.

No fixture passes its own `--spec` (`matrix.txt` prints `spec_in_argv= False` for all four): `d4m` and `d5m` are
built against the frozen round-35 spec the counter appends (`ctx.spec_path`), so none of them is "a spec the gate
would never see".

## 4. Side channels and fixture-name keying — audited, none

Code-level surface of both modules (docstrings excluded):

```
$ grep -nE "^(import|from) " plans/battery38/d4m.py plans/battery38/d5m.py
d4m.py:35:import pathlib        d4m.py:36:import re
d5m.py:28:import hashlib       d5m.py:29:import pathlib     d5m.py:30:import re     d5m.py:31:import shutil
$ grep -n "ctx\." plans/battery38/d4m.py plans/battery38/d5m.py
d4m.py:47: ctx.d4_line()   d4m.py:50,56: ctx.spec[...]
d5m.py:39: ctx.d5_capture_dir()   d5m.py:40,45: ctx.spec["d5"][...]   d5m.py:51: ctx.d5_line()   d5m.py:62: ctx.spec["d5"]["quote"]
$ grep -n "write_text\|copy2\|copytree\|mkdir" plans/battery38/d4m.py plans/battery38/d5m.py
… every write target is `pathlib.Path(d)/<name>` or `dst = Path(d)/"captures"`
```

No `os`, `sys`, `subprocess`, `importlib`, `time`, `getenv`, `argv`, `/proc`, `ppid`, `cmdline`, `psutil`,
`environ`; no read of `plans/pkg_gate.py`, of any gate copy, or of the counter's temp root; no monkeypatch of the
counter's `run_gate`/`attributed`; no dependence on the directory name (`paths are composed from the handed-in
`d`), which the counter's rename pass independently confirms (`renamed_disagree=0`). The counter's
`sidechannel=0` (a five-token heuristic) therefore agrees with inspection for these two modules — a statement
about `d4m`/`d5m`, not about battery38 as a whole.

## 5. N21 — attacking the "frozen as silence, only killable as mirror" explanation

### 5.1 Unreachability of a silence kill: confirmed

Ten manifest shapes (genuine one-row capture dir, genuine erratum line, only the manifest varied) against the
reference and N21:

```
row1-true                ref=0/-   n21=0/-    SILENCE_KILL=False
decoy-then-true          ref=0/-   n21=1/D5   SILENCE_KILL=False   (mirror)
true-then-decoy          ref=0/-   n21=0/-    SILENCE_KILL=False
decoy-only               ref=1/D5  n21=1/D5   SILENCE_KILL=False
two-decoys               ref=1/D5  n21=1/D5   SILENCE_KILL=False
true-twice               ref=0/-   n21=0/-    SILENCE_KILL=False
empty                    ref=1/D5  n21=1/D5   SILENCE_KILL=False
true-digest-wrong-name   ref=1/D5  n21=1/D5   SILENCE_KILL=False
true-name-wrong-digest   ref=1/D5  n21=1/D5   SILENCE_KILL=False
blank-row-then-true      ref=0/-   n21=1/D5   SILENCE_KILL=False   (mirror)
```

Not just an enumeration: `pinned_mut = any(row1)`, `pinned_ref = any(all rows)`, and row1 ⊆ all rows, so
`pinned_mut ⇒ pinned_ref` on **every** input and every spec; the mutation only ever appends a `bad` entry, and the
clause prints one `D5`. Hence `mut ok ⇒ ref ok`, so no fixture (and no self-supplied `--spec`, which the counter
permits for battery38) can produce `ref DEFECT ∧ mutant ok`. The frozen `silence` cell is unsatisfiable — a freeze
defect, exactly as `corpus/QUALITY.md:499-511` (Q29) and the lesson row record, not a battery gap. **Confirmed.**

### 5.2 The one-word path is real

Using the counter's own attribution function on the d5m witness:

```
ref= 0 []  n21= 1 ['D5']
attributed(silence)= False
attributed(mirror) = True
```

So the frozen predicate's `killed=22` becomes reachable by changing N21's `direction` cell to `mirror` — i.e. the
`C1 fail` is a label defect in the frozen list, and the only thing that keeps it an honest stop is the round-38
rule against relabelling after scoring. The fixture already exists and already demonstrates the advertised
sentence observationally (`D5 ok` on a manifest whose matching row is row 2); it is not a kill because of a
declaration, not because of a missing input.

### 5.3 The Q29 witness guard is not independent of `d5m` — and goes green without it

`plans/mutant_direction_check.py` on the landed tip: `DIR N21 D5 declared=silence observed=mirror MISLABELLED`,
`DIRECTIONS total=22 mislabelled=1`, **exit 1**. On a second clone of the same tip with only
`plans/battery38/d5m.py` deleted:

```
DIR N19 D4 declared=silence observed=silence ok
DIR N21 D5 declared=silence observed=- UNWITNESSED
DIR N22 D5 declared=silence observed=- UNWITNESSED
DIRECTIONS total=22 mislabelled=0
nod5m-exit=0
```

So the round's "mined-mistake fix" reports **clean** (exit 0, `mislabelled=0`) when the single accept fixture that
witnesses the mislabel is absent, and its aggregate line carries no `unwitnessed` count. Q29's Limits call
`UNWITNESSED` "not a verdict", and `MUTANTS … survived>0` still fails C1, so I do **not** count this as a defect;
it is a limit of the guard that a reader of `DIRECTIONS total=22 mislabelled=0` cannot see. Receipts:
`dir-full.txt`, `dir-nod5m.txt`.

## 6. Defects

### D1 — `PINS total=14 mismatched=0` does not bind `d4m`/`d5m`: the predicate's first line certifies nothing about the calibration's fixtures

`plans/round38_c1_verify.py:72-87` PINS has 14 entries (gate, r37 counter, r36 counter, r35 spec, r37 attribution
audit, nine battery37 modules). `plans/battery38/*.py` — the fixtures that produce all 21 kills — are not among
them. Demonstrated on the clone:

```
$ printf '# tamper appended after the landing tip\n' >> plans/battery38/d5m.py
$ sha256sum plans/battery38/d5m.py
50680812a43fea055e715ba9ea2dd48cb5991d7852ae363c5d31faa9420e3bd1     # was 5af18f40…
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --only N22 --work "$S/w_t"
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N22 D5 silence killed by=d5m-n22-quote-prefix -- the whole quote must be present, not a 20-character prefix [F37XMutD5 X4]
```

An edited fixture module leaves `PINS … mismatched=0` and the kill intact. The mitigation is real but external to
the counter: the frozen predicate says "measured on a clean clone of the landing tip", and git binds battery38 at
`8c7422d7`; `corpus/lessons/round-38.md:40-43` also discloses that battery38 is "reviewed by wave-2 seats", not
pinned. But the printed `PINS` line and the docstring's "pins 14 inputs by digest" (`round-38-claims.md` §C1) are
what a reader uses as the evidence chain, and as soon as anyone edits a battery38 module in-tree — which is how
this round's modules were produced and how wave-2 fixes would land — the pin line stays green while the kill
evidence is no longer the bytes that produced the receipt.

### D2 — the docstring's universal "every input of this counter that exists at the freeze" is false; three unpinned lane data files are load-bearing for `d4m`/`d5m`

`plans/round38_c1_verify.py:50` (docstring of the PINS block at `:72-87`): "… — every input of this counter that
exists at the freeze." Every `d4m`/`d5m` builder reads lane text through `Ctx`, and none of it is pinned:
`ctx.d4_line()` → `SCORECARD.md` (`spec["d4_source_file"]`, the D4 correction line at `SCORECARD.md:1180`),
`ctx.d5_line()` → `corpus/lessons/round-34.md` (`spec["d5_source_file"]`), `ctx.d5_capture_dir()` →
`.ufo/waves/round-34/assimilation/captures/` (capture + `quarantine-SHA256SUMS`). All three existed at the
freeze. Editing the D4 line in a third clone:

```
$ python3 plans/round38_c1_verify.py --lane "$S/lane3" --only N19 --work "$S/w_l3"
PINS total=14 mismatched=0
Traceback (most recent call last):
  …
  File "…/plans/battery38/d4m.py", line 68, in _one_substitution
    raise RuntimeError(f"genuine line carries {line.count(needle)} copies of {needle!r}, expected 1")
RuntimeError: genuine line carries 0 copies of 'selftest was green', expected 1
```

`PINS` is green while a load-bearing input has been edited, and the counter dies with a traceback instead of
reporting a mismatch (fail-loud, but not a measured result; C1's predicate has no line for "the source text the
fixtures adapt to moved"). Receipt: `pins-vs-scorecard.txt`.

D1 and D2 share one root (pin completeness) but are separately fixable text/evidence surfaces; I count them
separately and would accept a judge merging them to one.

## 7. What survived the attack (confirmations, so the wave-2 record is complete)

- Each of the three kills (N19, N20, N22) is single-cause and single-fixture; each fixture is necessary (§2) and
  kills only its own mutant (§3).
- The `adv`-cell mismatch for N19/N20/N21/N22 (tier K / weak C, `adv` cells citing only round-37 report ids) is
  already filed by wave-1 `R38CritClaims` (`.ufo/waves/round-38/build/R38CritClaims.md:48-51,88`) and carried in
  the lesson (`corpus/lessons/round-38.md:38`); I did not re-file it, and nothing in `d4m`/`d5m`'s own docstrings
  contradicts it.
- `d5m`'s docstring claim that `d5m-n21-manifest-row-2` is the only battery fixture whose matching manifest row is
  not row 1 holds for D5: the genuine `quarantine-SHA256SUMS` has the D5 capture's digest on row 1
  (`b60af775…  …/nec-s091-reopen.html`, 2 rows total), `plans/battery37/d5.py:134` rewrites a one-row manifest,
  and `r36-L4`/`r36-L6` use the genuine dir.
- N19/N20 kill through `failed=['pattern3']` / `failed=['pattern1']` with `patterns=3` printed by both gates, so
  neither kill rides on the printed pattern count or on a second clause.
- N22's fixture is honest about its mechanics: it re-pins the manifest to the truncated capture
  (`digest_pinned=True` in both runs) so the only difference is the quote sub-check.
- Determinism: the four-mutant subset run is byte-equal on re-run (`cmp` exit 0); `renamed_disagree=0`.

## 8. Impacted axes

- **calibration (C1):** the 22-mutant denominator's *evidence chain*, not its arithmetic. D1 weakens "PINS … = the
  inputs" as the counter's audit line; D2 shows the universal is false and that a load-bearing source edit is
  reported as a traceback. Neither changes `killed=21 survived=1` at `8c7422d7`.
- **self-assessment / provenance:** `plans/round38_c1_verify.py:50` and the claims' "pins 14 inputs by digest"
  describe a pin set that excludes the fixtures and the data files the fixtures adapt to.
- **Not impacted:** the gate bytes (freeze digest), the frozen MUTANTS list, the four fixtures' mechanics, the N21
  freeze-defect explanation (confirmed), `mutant_direction_check`'s spec (limit confirmed, not a defect), C2.

## 9. Smallest safe corrections

1. D1: add the twelve `plans/battery38/*.py` digests to `PINS` (PINS total 14 → 26) — or, if wave-3 forbids
   changing pins, change the printed line to `PINS total=14 mismatched=0 battery38=unpinned` so the predicate's
   first line stops implying coverage it does not have.
2. D2: pin `spec["d4_source_file"]` (`SCORECARD.md`), `spec["d5_source_file"]` (`corpus/lessons/round-34.md`) and
   the D5 capture+manifest as fixture data, or weaken the sentence to "pins the counter's code inputs; the fixture
   data at the tip commit is bound by the clone, not by a digest", and have the builders report a `SETUP` line
   (exit 2 with a named reason) instead of a traceback when a source line moves.
3. Optional, for §5.3: print `unwitnessed=<n>` on the `DIRECTIONS` line (or exit non-zero when a mutant the
   counter scores as killed has no observed direction) so `mislabelled=0` cannot be read as "witnessed".

## Receipts

`F38CritBatF/`: `run_a.txt`, `run_b.txt` (baseline, byte-equal), `matrix.txt` (cross matrix, gate notes, N21 shape
enumeration, N22 quote variants), `del-full.txt`, `del-no_d4m.txt`, `del-no_d5m.txt`, `del-n19.txt`,
`del-n20.txt`, `del-n21.txt`, `del-n22.txt` (per-fixture necessity), `dir-full.txt`, `dir-nod5m.txt`
(`mutant_direction_check` with and without `d5m`), `pins-vs-scorecard.txt` (PINS green over an edited source
line). Scratch `/fast/scratch/hyaku/kengaku-r38/F38CritBatF` removed at the end; clones only, no lane writes, no
pacman (`uv`/`npx`/binary installs not needed).

VERDICT: battery-d4m-d5m-attack-2-defects
