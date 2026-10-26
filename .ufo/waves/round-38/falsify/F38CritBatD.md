# F38CritBatD — attack on `plans/battery38/p4a.py` and `p4b.py` (frozen mutants N03–N06)

Seat: F38CritBatD (critic, leaf). Round 38 wave 2 (falsify). Attacks the four P4 fixtures that the C1 landing
receipt credits with killing N03/N04/N05/N06.

Lane under attack: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a`. All work in a clone:

```
$ S=/fast/scratch/hyaku/kengaku-r38/F38CritBatD
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" \
    && git -C "$S/lane" checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
$ git -C "$S/lane" rev-parse --show-toplevel  →  /fast/scratch/hyaku/kengaku-r38/F38CritBatD/lane
$ git -C "$S/lane" rev-parse HEAD             →  8c7422d7a646515d80af44844e8ecc8a1fc1d30a
```

Artifacts under test (digests equal to the wave-1 build reports, so the landed bytes are the drafts):

```
60f34aa2…fbffbf  plans/battery38/p4a.py   (95 lines)
31d591f6…2edd332  plans/battery38/p4b.py   (74 lines)
ea638822…6edd41  plans/pkg_gate.py        (frozen; P4 clause at :138-150)
```

The four advertised behaviours being tested (`plans/round38_c1_verify.py:98-106`, `adv` cells):

| mutant | `adv` sentence | fixture credited |
|---|---|---|
| N03 | every quote is checked, not only the first | `p4a-second-row-line-outside` |
| N04 | verbatim on the CITED lines, not anywhere in the capture | `p4a-text-elsewhere` |
| N05 | verbatim is case-sensitive | `p4b-case-only` |
| N06 | a cited range past the capture's last line is a defect | `p4b-range-end-past-last` |

## 1. Subset run reproduces the landing attribution

```
$ export TMPDIR=$S; mkdir -p "$S/w"
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --only N03,N04,N05,N06 --work "$S/w"
PINS total=14 mismatched=0
FIXTURE p4a-second-row-line-outside expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4a-text-elsewhere expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4b-case-only expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4b-range-end-past-last expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N03 P4 silence killed by=p4a-second-row-line-outside -- …
MUTANT N04 P4 silence killed by=p4a-text-elsewhere -- …
MUTANT N05 P4 silence killed by=p4b-case-only -- …
MUTANT N06 P4 silence killed by=p4b-range-end-past-last -- …
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
```

Receipt: `F38CritBatD/only4.txt`. Nothing here is new information; it is the baseline the attacks below move.

## 2. Load-bearing: delete each fixture → its mutant SURVIVES (confirmed)

Method: `shutil.copytree` of the clone's `plans/battery38` per case, then one `FIXTURES` entry cut out of the
module text (assertion: `"fid": "<fid>"` no longer present); run through the counter's documented dev path
`--battery-dir`, so the clone itself stayed at the landed tip and every pinned input was untouched
(`PINS total=14 mismatched=0` in each run). Driver kept as `F38CritBatD/deltest.py`.

```
### drop p4a-second-row-line-outside -> --only N03 (exit=1)
BATTERY fixtures=85 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N03 P4 silence SURVIVED -- every quote is checked, not only the first
### drop p4a-text-elsewhere -> --only N04 (exit=1)
BATTERY fixtures=85 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N04 P4 silence SURVIVED -- verbatim on the CITED lines, not anywhere in the capture
### drop p4b-case-only -> --only N05 (exit=1)
BATTERY fixtures=85 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N05 P4 silence SURVIVED -- verbatim is case-sensitive
### drop p4b-range-end-past-last -> --only N06 (exit=1)
BATTERY fixtures=85 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N06 P4 silence SURVIVED -- a cited range past the capture's last line is a defect
### p4a.py + p4b.py absent -> --only N03,N04,N05,N06 (exit=1)
BATTERY fixtures=82 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N03 … SURVIVED / N04 … SURVIVED / N05 … SURVIVED / N06 … SURVIVED
MUTANTS total=4 killed=0 survived=4 invalid=0 null_detected=0
```

Receipt: `F38CritBatD/deltest.txt`. Each fixture is both necessary and sufficient for its own mutant; no fixture
carries a second mutant.

## 3. The kills are mechanism-level, not incidental (4×4 matrix)

Driver `F38CritBatD/probe.py` builds the four fixtures through the counter's own `Ctx`, then runs the untouched
gate and one gate per mutant carrying only that mutant's `old -> new`, printing rc, the raw `P4 …` line, and a
crash flag. Full output in `F38CritBatD/probe1.txt`; the whole matrix:

```
REF   p4a-second-row-line-outside   rc=1 defects=['P4'] p4=['P4 DEFECT checked=22 bad=1 first=test_outputs.py:1073-1073: line range outside the capture']
REF   p4a-text-elsewhere            rc=1 defects=['P4'] p4=['P4 DEFECT checked=22 bad=1 first=test_outputs.py:1: quote not verbatim there']
REF   p4b-case-only                 rc=1 defects=['P4'] p4=['P4 DEFECT checked=22 bad=1 first=test_outputs.py:13: quote not verbatim there']
REF   p4b-range-end-past-last       rc=1 defects=['P4'] p4=['P4 DEFECT checked=22 bad=1 first=instruction.md:34-35: line range outside the capture']

N03 … second-row-line-outside  rc=0 p4=['P4 ok checked=22 bad=0 first=0'] crash=False attributed=True
N03 … text-elsewhere           rc=1 p4=['P4 DEFECT … quote not verbatim there'] attributed=False
N04 … text-elsewhere           rc=0 p4=['P4 ok checked=22 bad=0 first=0'] crash=False attributed=True
N05 … case-only                rc=0 p4=['P4 ok checked=22 bad=0 first=0'] crash=False attributed=True
N06 … range-end-past-last      rc=0 p4=['P4 ok checked=22 bad=0 first=0'] crash=False attributed=True
(every other cell: attributed=False)
```

Three things this rules out:

- **No crash-based false kill.** In each attributed cell the mutant exits 0 and prints `P4 ok … bad=0`; the
  whole gate accepts the defaced package. It is not silence-by-exception (rc 1 with an empty clause set would
  also satisfy `attributed`, `plans/round38_c1_verify.py:191-204`).
- **No second clause doing the work.** The reference defect set on all four fixtures is exactly `{P4}` (`rc=1`,
  `defects=['P4']`); no P3/P5/P6 defect exists that could be mistaken for the kill.
- **No cross-kill.** The matrix is diagonal: each mutant is attributed to exactly one fixture, and each fixture
  kills exactly one mutant. This independently confirms p4a's docstring claims "Row 1 stays verbatim, so the
  fixture cannot kill any first-row mutant" and "this fixture cannot kill N03" (N03 on `p4a-text-elsewhere`
  still prints `P4 DEFECT`).

## 4. `defects` declaration is not tailored; no spec, no side channel, no name keying

- Declared vs observed: `wrong=0` in every run above, and each observed set is exactly `{P4}` (§1, §3). A
  declaration tailored toward a weaker fixture would have shown as `WRONG` (`round38_c1_verify.py:264-267`).
- Spec: neither module returns `--spec` (`p4a.py:53`, `p4b.py:39` return only
  `["package","--root",str(d),"--require-clean-tree"]`), so both are graded against the frozen
  `plans/pkg-spec-r35.json`; the counter's "spec lives inside the fixture dir" allowance
  (`round38_c1_verify.py:245-249`) is not used.
- Side channel beyond the token list (`SIDECHANNEL`, `round38_c1_verify.py:89`): both modules have **zero import
  lines** — `grep -nE '^(import|from)' plans/battery38/p4a.py plans/battery38/p4b.py` returns nothing (rc=1).
  No `os`, `sys`, `subprocess`, `time`, so no env/argv/timing/`/proc` channel exists at all. The only reads are
  files inside the built fixture tree plus `ctx.spec` (`p4a.py:37-38,50`; `p4b.py:60`), i.e. the frozen spec.
- Name/path keying: the fixtures receive only `(ctx, d)`; `d.name` and `str(d)` are never referenced (grep:
  none), and the counter's renamed re-run agrees (`renamed_disagree=0`, §1). My probe rebuilt the tree under a
  different scratch root with identical results (§3).

## 5. Counterexample that DID land — breadth of "every quote" (limit, not a count defect)

Driver `F38CritBatD/probe2.py` builds all 86 fixtures and applies the counter's own `attributed("P4",
"silence", …)` to three sibling mutants of the N03 sentence that the frozen list does not contain:

```
FIXTURES built=86
X1-skip-last-quote:  for q in p.quotes[:-1]:   killed_by=NONE
X2-last-quote-only:  for q in p.quotes[-1:]:   killed_by=['p4-capture-unreadable','p4-line-outside','p4-one-char-off',
                                                 'p4a-second-row-line-outside','p4a-text-elsewhere',
                                                 'p4b-case-only','p4b-range-end-past-last']
X3-skip-first-two:   for q in p.quotes[2:]:    killed_by=[… same seven …]
X4-first-two-only:   for q in p.quotes[:2]:    killed_by=NONE
```

Receipt: `F38CritBatD/probe2.txt`. Reading it exactly:

- **X4 survives the entire 86-fixture battery.** A gate that checks only the first two of 22 quotes — 20 quotes
  unread — is not caught by any fixture. So the battery demonstrates "quote #2 is checked", not "every quote is
  checked"; the P4 fixtures deface only data rows 0 and 1 (`test_outputs.py:13` and `:16`).
- **X1 survives too**: the last quote is never defaced, so a `[:-1]` mutant is invisible.
- X2/X3 are killed, but as subset mutants that happen to skip a defaced quote — the same clause, not evidence
  that quotes ≥2 are exercised.

This does not move the C1 count: the frozen mutant is `p.quotes[:1]`, `p4a-second-row-line-outside` kills it
attributably, and the round's kill rule ties a kill to the mutant's clause and direction
(`round38_c1_verify.py:29-38`), not to how wide the fixture's coverage is. Recorded as a **limit on what the
advertised sentence demonstrates**, not a defect of the fixture.

## 6. Smallest safe correction

None is required for the frozen predicate. If a later round wants the "every quote" half of N03's `adv` sentence
actually demonstrated, the smallest move that harms nothing is one more fixture in the same module — deface the
**last** data row, e.g. reuse `_second_row_outside`'s body with `rows[-1]` instead of `rows[1]`
(`p4a.py:56-65`), declared `defects=["P4"]`. That kills X1/X4 while leaving the 22-mutant list, the frozen gate,
the spec and both counters untouched. It is not proposed for this round: the predicate is already met for these
four ids and new fixtures cannot be added after the freeze without reopening C1.

## Impacted axes

- **calibration (8, chosen tie-break target):** no change. All four kills are attributable at clause and
  mechanism level, each fixture is load-bearing, no tailoring, no side channel, no name keying.
- **novelty / depth:** the X1/X4 survival is new evidence about the battery's *breadth* and should ride along in
  the round's limits, not in its score.

## Receipts (this seat's dir, all written under `.ufo/waves/round-38/falsify/F38CritBatD/`)

`only4.txt` · `deltest.txt` · `probe1.txt` · `probe2.txt` · drivers `probe.py`, `probe2.py`, `deltest.py`.
Scratch `/fast/scratch/hyaku/kengaku-r38/F38CritBatD` (clone + work dirs) removed after the copy. No lane file,
no git index, no jj state touched; no tool installed or upgraded.

VERDICT: battery-p4a-p4b-attack-0-defects
