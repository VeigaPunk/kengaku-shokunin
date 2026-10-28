# C1MutCounters — R52 mutation probe

## Scope and method

Mutation-tested isolated copies of the C1 and C2 counters. No lane source was edited. The C1 synthetic population fixture used all **184** frozen `capture_population` paths, synthetic bytes, matching SHA256SUMS, two quote-backed candidate confirmations, and three URLs. C1 control `blind-class` replaced primary graders with marker-free three-test bodies; `drop-capture` removed one capture and one other digest entry to reproduce the frozen expected counts. Separate minimal fixtures isolated a digest mismatch and one-confirmation boundary. The C2 proxy copied the self-assessment inputs/scripts, added 28 registry rows, and then applied each named control. These are logic fixtures, not claims about the upstream grader bytes or truthful final registry rows.

**Kill convention:** a mutant is killed when the stated control's expected output/verdict changes from the pristine counter; otherwise it survives that control. “Survived” marks control coverage gaps. The C1 `drop-capture` control's combined count deficit can mask the mismatch-leg mutation, so an isolated digest-only fixture is also reported.

## Mutant results

| Mutant | Expected killer control | Actual output / comparison | Killed? |
|---|---|---|---|
| C1: broaden PRESENCE regex to include `assert` | `c1-control-blind-class` | Pristine: `CLASS ... V0=89`, `CANDIDATES total=0`, `CONFIRMED new=0`. Mutant: `CLASS V1=89`, `CANDIDATES total=89`, `CONFIRMED new=0`. Predicate remained fail because there were no confirmations, but the control's class/candidate signature changed. | Yes (signature) |
| C1: change V4 boundary `ntests <= 2` to `<= 3` | `c1-control-blind-class` | Pristine: `V0=89`, candidates 0. Mutant: `V4=89`, candidates 89. | Yes (signature) |
| C1: drop `mismatched == 0` predicate leg | `c1-control-drop-capture` | Frozen control fixture: pristine and mutant both reported `CAPTURES expected=184 present=183 mismatched=1` and predicate fail; the missing capture alone still fails the predicate, so this control **did not distinguish** the mutant. Isolated digest-only fixture: pristine reported `present=2 mismatched=1`, fail; mutant reported the same counts but predicate pass. | No on named control; isolated digest-only probe distinguishes it |
| C1: lower CONFIRMED threshold from 2 to 0 | `c1-control-blind-class` | Both reported `CANDIDATES total=0`, `CONFIRMED new=0`; pristine predicate failed, mutant predicate passed. | Yes (verdict) |
| C2: drop MISSING from predicate conjunction | `c2-control-drop-row` | Pristine: `MISSING 1`, predicate fail. Mutant: `MISSING 1`, predicate pass. | Yes (verdict) |
| C2: widen ADVERTISED regex to any `python3 <path>.py` | `c2-control-nothing` | Pristine: `ADVERTISED 72`, `MISSING 28`. Mutant: `ADVERTISED 79`, `MISSING 34` (and `REGISTERED 45`). | Yes (signature) |
| C2: count MISSING only under `plans/` | `c2-control-drop-row` | Pristine and mutant both reported `MISSING 1`, predicate fail. On base state both reported `MISSING 28`; all 28 existing missing paths are `plans/*.py`. | No; survives all exercised controls (coverage gap / equivalent on current missing set) |

C2 control fixture measurements: green proxy `MISSING 0 / INCOMPLETE 0 / ENTRY-MISSING 0 / SELFTEST-UNBACKED 0`, pass; empty-cells `INCOMPLETE 28`, fail; drop-row `MISSING 1`, fail; false-selftest `SELFTEST-UNBACKED 1`, fail. Real lane base counter output was `ADVERTISED 72`, `REGISTERED 44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1`, predicate fail.

## C1 census/control note

On the synthetic full-capture fixture, pristine output was `CAPTURES expected=184 present=184 mismatched=0` and predicate pass. The `c1-control-drop-capture` fixture reproduced its frozen expected line `expected=184 present=183 mismatched=1`. However, because that control has both a missing-file deficit and a mismatch, removing the mismatch predicate leg still leaves it failing on `present`; it therefore does not independently cover the mismatch leg. The isolated digest-only probe did flip fail→pass when the mismatch leg was removed.

## Commands and evidence

Setup / detector commands included:

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1MutCounters/{tmp,mutants,fixtures,out}
cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c1_grader_audit.py /fast/scratch/hyaku/kengaku-r52/C1MutCounters/mutants/c1_base.py
cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py /fast/scratch/hyaku/kengaku-r52/C1MutCounters/mutants/c2_base.py
python3 mutants/<variant>.py --lane fixtures/<control>
python3 plans/round52_c1_grader_audit.py --lane .
python3 plans/round52_c2_registry.py --lane .
sha256sum plans/round52_c1_grader_audit.py plans/round52_c2_registry.py
```

The same detector invocations were run over the C1 and C2 fixture/control matrices described above. No tools were installed. Frozen-source hashes at the end of the probe match the pristine scratch copies (unchanged):

- `plans/round52_c1_grader_audit.py`: `c3f44dc26f7cb8eafe9ac01446cfcdf7acf95e0f473ea291f77e914d7eebc60d`
- `plans/round52_c2_registry.py`: `8cf1328a006b265e823a5e0a2980ffd8fa1c4e90dca759aae314fab46a046af0`

Mutant copies and synthetic fixtures were created only under `/fast/scratch/hyaku/kengaku-r52/C1MutCounters/` and removed before completion. Retained deliverable: this report. No tests/build/formatters were run.