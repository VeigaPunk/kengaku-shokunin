# F37XMutP8 — new P8 (c_readme) mutants against `plans/battery37/p8.py` and the full C1 battery

Seat: critic, kengaku round 37 wave 2 (falsify). Target: `plans/battery37/p8.py` (5 single-defect
fixtures, frozen mutants M34-M38) and the calibration observable in `plans/round37_c1_verify.py`.
Lane tip under test: `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`, tested on my own clone; no lane file
was written.

Axes: (A1) kill coverage of P8 mutants beyond the frozen five; (A2) validity of the isolation
claim in p8.py; (A3) scope of what the C1 observable can prove.

## Method

`harness.py` (this dir) imports the frozen counter as a module from the clone
(`load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures`, `run_gate`), builds the **full** battery
once (`BATTERY fixtures=64 (r36=14 battery37=50)`), runs the reference gate over all of it, then runs
each `old -> new` mutant (asserted to occur exactly once, compiled) over the same built fixtures.
Observable per run is the counter's own: `(exit code, set of clause ids printed DEFECT)`.

Independent re-measurement before mutation: all 64 fixtures reproduce their declarations under the
unmodified gate (`parsed=64 mismatches=0`), gate digest = freeze
(`sha256_match_freeze=True`, `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`).

## A1 — four new non-frozen P8 mutants

| id | class | result | killing fixture (mutant result vs reference) |
|---|---|---|---|
| X1 | quantifier loosened: every registry row cited → any one cited | killed | `p8-index-row-missing-sid` — `(0, ∅)` vs `(1, {P8})` |
| X2 | check applied to the first registry row only | killed | `p8-index-row-missing-sid` — `(0, ∅)` vs `(1, {P8})` |
| X3 | regex loosened: `INDEX_ROW` un-anchored (over-firing) | killed | 42 fixtures; decisive = `r36-P0` (accept → reject), `(1, {P8})` vs `(0, ∅)` |
| X4 | off-by-one threshold, lower side (`!= 1` → `< 1`) | killed | `p8-index-row-duplicated` — `(0, ∅)` vs `(1, {P8})` |

Exact pairs (each occurs once in `plans/pkg_gate.py`):

```
X1  elif not all(sid in rows[0] for sid in p.spec["rows"]):
 -> elif not any(sid in rows[0] for sid in p.spec["rows"]):

X2  elif not all(sid in rows[0] for sid in p.spec["rows"]):
 -> elif not all(sid in rows[0] for sid in list(p.spec["rows"])[:1]):

X3  INDEX_ROW = re.compile(r"^\|\s*`(knowledge/[^`]+\.md)`\s*\|")
 -> INDEX_ROW = re.compile(r".*?(knowledge/[^`]+\.md)")

X4  if len(rows) != 1:
 -> if len(rows) < 1:
```

Detail lines (from `probe_detail.py`), `p8-index-row-missing-sid`:

```
ref P8: P8 DEFECT index_rows=44 knowledge_files=44 bad=1 first=index row does not cite every registry row
X1  P8: P8 ok index_rows=44 knowledge_files=44 bad=0 first=0
X2  P8: P8 ok index_rows=44 knowledge_files=44 bad=0 first=0
```

X3 over-fires on the genuine package without any fixture edit — the un-anchored pattern also matches
the two prose mentions of the entry in `corpus/README.md` (lines 259, 286):

```
genuine-package: ref=(0, frozenset())  X3=(1, frozenset({'P8'}))
X3 P8: P8 DEFECT index_rows=44 knowledge_files=44 bad=1 first=index rows for knowledge/tb2-protein-assembly-grader.md=3
```

Note on X3's kill set: 42 of 64 fixtures kill it, but **none of the five `p8.py` fixtures do** — they
already declare `{P8}`, so an over-firing `c_readme` is invisible from inside the module. The single
fixture that protects the genuine package is the accept control `r36-P0` (the two other accepts,
`r36-L1`/`r36-L4`, run the `d4-line`/`d5-line` subcommands and never reach `c_readme`).

## A1b — one survivor probe, and why it is NOT a battery hole

A fifth mutant (same `old` as X4, the mirrored half) **survived all 64 fixtures**:

```
S1  if len(rows) != 1:  ->  if len(rows) > 1:        SURVIVED
```

Diagnosis (`probe_n1.py`, three packages built from the genuine bytes):

```
a-control:         ref=(0, ∅) n1=(0, ∅)  -> same
b-zero-index-row:  ref=(1, {P8}) n1=(1, {P8})  -> same
   ref P8: P8 DEFECT ... bad=2 first=index rows for knowledge/tb2-protein-assembly-grader.md=0
   n1  P8: P8 DEFECT clause error IndexError: list index out of range
c-unindexed-entry: ref=(1,{P3,P4,P7,P8}) n1=(1,{P3,P4,P7,P8}) -> same
   n1  P8: P8 DEFECT clause error IndexError: list index out of range
```

With `rows == 0` the mutated `if` is false and the following `elif` dereferences `rows[0]`; the gate's
driver converts the exception into a defect (`plans/pkg_gate.py:299`,
`except Exception as e:  # a clause cannot run is a defect, never a pass`), so the mutant's tuple is
identical to the reference on **every** possible package (rows 0 → crash → DEFECT; rows ≥ 2 and
rows = 1 → byte-identical to the reference). S1 is therefore observationally equivalent, not a
coverage gap: adding the missing zero-row fixture to `p8.py` would **not** kill it (measured, case b).
This is why S1 is excluded from the /4 count.

Counterexample to the counter's own interpretation, though: a survivor is documented as "advertised
but undemonstrated" clause coverage, and nothing in `round37_c1_verify.py` checks that a survivor is
killable at a finer observable. Impacted axis: A3 (measurement scope), not the frozen pass.
Smallest safe correction (proposal only, not applied): have the counter also compare the clause's
detail line (e.g. the `first=` / `bad=` fields) when a mutant survives, and label the survivor
`survived(message-level)` — or state in the docstring that message-level and crash-as-DEFECT mutants
are out of scope of the clause-set observable.

## A2 — does each `p8.py` fixture isolate one defect?

Measured, not asserted: the frozen five are killed 1:1 by exactly their own fixture (my run of
M34-M38 over the same built battery).

```
M34 killed by=1 ['p8-readme-deleted']              M35 killed by=1 ['p8-index-row-duplicated']
M36 killed by=1 ['p8-index-row-missing-sid']       M37 killed by=1 ['p8-coverage-bullet-removed']
M38 killed by=2 ['p7-m28-entry-deleted', 'p8-extra-knowledge-file']
```

Reference results: all five fixtures `rc=1 defects=P8`, matching their declared `{"P8"}` exactly
(`p8-readme-deleted`, `p8-index-row-duplicated`, `p8-index-row-missing-sid`,
`p8-coverage-bullet-removed`, `p8-extra-knowledge-file`). So the docstring's branch↔fixture mapping
and the "every declared defects set is {P8}" claim both hold; each fixture reaches one and only one
P8 branch. M38 is additionally killed by another module's fixture (`p7-m28-entry-deleted` deletes the
entry file, so `files != indexed` fires); that fixture declares `{P3,P4,P7,P8}`, so it is declared, not
leakage.

One docstring sentence is factually wrong (A2, documentation-level):

- Claim: `plans/battery37/p8.py` — "no other clause reads corpus/README.md or corpus/knowledge/\*".
- Counter-evidence: `plans/pkg_gate.py:70` `pkg.entry = read(root / spec["entry"])`, and the spec's
  entry is `corpus/knowledge/tb2-protein-assembly-grader.md`; P3/P4/P7 consume it. Measured:
  `p7-m28-entry-deleted` reference defects are `{P3,P4,P7,P8}` — `c_readme`'s directory scan and P7's
  entry read both observe that file.
- The part that matters for fixture safety is true: only `c_readme` globs the directory
  (`plans/pkg_gate.py:252`), so `p8-extra-knowledge-file`'s added file is read by no other clause
  (observed `{P8}`).
- Smallest safe correction: reword to "no other clause reads corpus/README.md, and only c_readme
  globs corpus/knowledge/\*.md (P3/P4/P7 read the entry file there)".

Coverage limit worth naming (not a defect): X2 (`[:1]`, first registry row only) is killed only
because `p8-index-row-missing-sid` removes the **last** sorted sid (S107). No fixture removes S105, so
the citation check is demonstrated for one registry-row position only; the same single fixture is the
sole killer of X1 and X2, i.e. the whole "cites every registry row" branch has one witness.

## Reproduction

```
S=/fast/scratch/hyaku/kengaku-r37/F37XMutP8; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/fx/lane"
git -C "$S/fx/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
python3 F37XMutP8/harness.py      --lane "$S/fx/lane" --work "$S/work"      # 64 fixtures, ref + 9 mutants
python3 F37XMutP8/probe_n1.py     --lane "$S/fx/lane" --work "$S/probe"     # S1 equivalence, 3 packages
python3 F37XMutP8/probe_detail.py --lane "$S/fx/lane" --work "$S/probe2"    # P8 detail lines
```

Receipts in this directory: `harness-out.txt`, `probe-n1.txt`, `probe-detail.txt`. Scratch
`/fast/scratch/hyaku/kengaku-r37/F37XMutP8` removed after copying receipts. No lane file touched; no
git/jj state command run in the lane.

VERDICT: extra-mutants-p8-killed-4/4
