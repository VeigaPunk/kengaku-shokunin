# F37XMutP5 — four new P5 mutants beyond the frozen M13–M19

Seat: critic (wave 2, falsify). Target: `plans/battery37/p5.py` and clause P5 (`c_captures`) of
`plans/pkg_gate.py`. No lane file was edited; the counter ran on a clone.

Axes attacked, named up front:
- **Calibration** — does the battery kill P5 mutants that the frozen 55 do not contain?
- **Isolation** — does each `p5.py` fixture fire exactly one P5 branch, as its docstring claims?
- **Claim integrity** — survivors stay reported as battery limits, never repaired into the frozen claim.

## Setup

```
git clone -q --no-local <lane> /fast/scratch/hyaku/kengaku-r37/F37XMutP5/lane
git -C "$S/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r37/F37XMutP5/lane
sha256sum "$S/lane/plans/pkg_gate.py" -> ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
```

Harness `harness.py` (this dir) imports the frozen counter as a module
(`load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures`, `run_gate`), builds all 64 fixtures once
(14 r36 + 50 battery37), runs the untouched gate as reference, then each new mutant over those same
built fixtures. Observable is the counter's own: (exit code, set of `DEFECT` clause ids); the P5
detail line is also captured. Reference observation was re-checked against the counter's `run_gate`
for every fixture: `OBSERVE reference vs plan-run_gate mismatches=0`. Battery declarations re-checked:
`DECLARATIONS wrong=0`.

Run: `python3 harness.py --lane "$S/lane" --work "$S"` (receipt `receipt-frozen-battery.txt`).

## Four new P5 mutants (each `old` occurs exactly once in the gate; each compiles)

| id | mutation | exact `old -> new` (gate core) | result on the full battery |
|----|----------|-------------------------------|----------------------------|
| X1 | row loop applied to the **first registry row only** | `for sid, row in p.spec["rows"].items():` -> `for sid, row in list(p.spec["rows"].items())[:1]:` (multi-line, anchored at `if name not in pinned:`) | **SURVIVED** — 0/64 killers |
| X2 | operator flip on the bytes/digest comparison (the `>=`->`>` class) | `if sha256(capdir / name) != digest:` -> `if sha256(capdir / name) == digest:` | **killed** — 40/64 fixtures, first `r36-P0` (accept, ref rc=0/no clause, mutant rc=1 `P5` `bad=6`) |
| X3 | uncovered-file sweep applied to the **first directory entry only** | `for f in sorted(capdir.iterdir()):` -> `for f in sorted(capdir.iterdir())[:1]:` | **killed** — 1/64: `p5-extra-capture-file` (ref rc=1 `P5``bad=1`, mutant rc=0/no clause `bad=0`) |
| X4 | row branches reordered so the off-pin check **shadows** the unpinned check | `if name not in pinned: … elif pinned[name] != row["sha256"]: …` -> `if pinned.get(name) != row["sha256"]: … elif name not in pinned: …` | **SURVIVED** — 0/64 killers |

killed = 2/4. Both survivors are real defects, not no-op edits — witnesses below.

### X1 is live; the battery simply never looks past the first row

Both row fixtures pick `sorted(ctx.spec["rows"])[0]` — `plans/battery37/p5.py:73-76`, used at `:122`
(M16) and `:153` (M17) — and both defect `S105` (`ISOLATION … first=S105 …`). Witness probe
(`probe.py` section A) repeats M17's mechanism on the **last** row (`S107`/`instruction.md`: append a
line, move the manifest digest to the new bytes, spec pin unchanged):

```
A_row_S107 ref: rc=1 defects=[P5]  P5 DEFECT manifest_entries=6 bad=1 first=S107: manifest digest differs from the spec pin
A_row_S107 X1 : rc=0 defects=[]    P5 ok      manifest_entries=6 bad=0 first=0
```

A gate that checks one row accepts a genuine off-pin defect, and no fixture of the 64 sees it. This is
a **battery limit** (fixable in `p5.py`), not a gate defect.

### X4 is invisible by construction of the observable

`probe.py` section B runs the battery's own `p5-row-capture-unpinned` fixture under reference and X4:

```
ref P5 DEFECT bad=1 first=S105: capture test_outputs.py is not pinned in the manifest
X4  P5 DEFECT bad=1 first=S105: manifest digest differs from the spec pin
```

Same exit code, same clause set, different reason: the advertised class "row capture not pinned"
is no longer the reason P5 fires (the unpinned branch is dead for unpinned rows). Clause-set
observation cannot see any reason-level mutant; only *silencing* mutants (the frozen class) flip P5
green. So X4 is a **counter-design limit** for P5, not a `p5.py` gap — a stricter harness comparing
the P5 `first=` note would kill it.

## Does each `p5.py` fixture isolate one defect? Yes, at P5-branch level — 7/7

Reference run, per fixture (`receipt-frozen-battery.txt`): only `P5` is in the clause set, and each
carries exactly one P5 reason:

```
p5-manifest-absent            rc=1 clauses=P5  (early return) capture manifest absent: …/SHA256SUMS
p5-manifest-unparsed-line     rc=1 clauses=P5  bad=1 first=unparsed manifest line 'a note the manifest parser cannot read'
p5-capture-bytes-stale-digest rc=1 clauses=P5  bad=1 first=task.toml: manifest digest does not match the bytes
p5-row-capture-unpinned       rc=1 clauses=P5  bad=1 first=S105: capture test_outputs.py is not pinned in the manifest
p5-manifest-digest-off-pin    rc=1 clauses=P5  bad=1 first=S105: manifest digest differs from the spec pin
p5-quote-cites-unpinned       rc=1 clauses=P5  bad=1 first=quote capture .quote-extra.txt is not pinned in the manifest
p5-extra-capture-file         rc=1 clauses=P5  bad=1 first=extra-note.txt: capture file not covered by the manifest
```

`bad=1` on every accumulating fixture means the disclosed M16/M17/M18 bookkeeping (byte-identical
copy, quote re-citation, digest move) does remove the second branch it claims to remove. The
docstring's single-defect claim ("the second edit only removes a *second P5 branch*") holds. One
positional gap follows from it, and it is the cause of X1: **only one registry row (`S105`) is ever
defected** by the battery, so the row loop's coverage is not demonstrated beyond that row.

## Smallest safe corrections (tested in scratch, never applied to the lane)

Scratch copy of `plans/battery37` (`battery37-fix`), two edits:

1. `_row_capture(ctx, d, last=False)` with `sorted(...)[-1 if last else 0]`, and M17's call becomes
   `_row_capture(ctx, d, last=True)`. Re-run of the same harness:
   `MUTANT X1 P5 killed killers=1 first=p5-manifest-digest-off-pin` (`receipt-corrected-battery.txt`),
   with `DECLARATIONS wrong=0` and `p5-manifest-digest-off-pin … bad=1 first=S107: …` — isolation kept,
   and the two row branches now probe two different rows.
2. Sweep bound: `EXTRA_FILE = "extra-note.txt"` -> a name that sorts last (`zz-extra-note.txt`). With
   that, the supplementary tail mutant `sorted(capdir.iterdir())[:-1]` is also killed:
   `ref rc=1 P5 bad=1 first=zz-extra-note.txt` vs `X3b rc=0 P5 ok bad=0`
   (`receipt-sweep-tail-witness.txt`). On the frozen battery that tail mutant **survives**, because
   `extra-note.txt` sorts *before* `instruction.md`, so `[:-1]` never drops it: the sweep is pinned at
   its head (`X3` killed by one fixture) and not at its tail.

Neither correction is part of the frozen claim; both are reported for the wave-2 fold, not applied.

## Side observation (attribution, not a defect)

`measure-final.txt` prints `MUTANT M18 P5 killed by=p4-capture-unreadable`, but M18's designed fixture
`p5-quote-cites-unpinned` also kills it, and `p4-capture-unreadable` is affected because it also trips
P5 (`bad=1 first=quote capture no-such-capture-37.py is not pinned in the manifest`; under the
M18-silenced gate that fixture becomes `clauses=P4`, `P5 ok`). The receipt's `killed by=` is
first-match attribution over fixture order; per-mutant killer sets are larger than the label suggests
(X2: 40). No action required for C1's predicate.

## Evidence index

- `harness.py` — new-mutant harness (imports the frozen counter), `--battery-dir` for the scratch test.
- `probe.py` — witnesses A (X1 on last row), B (X4 reason swap), C (sweep head/tail).
- `receipt-frozen-battery.txt` (sha256 `b8680f49…e8b8`), `receipt-witnesses.txt` (`531298d4…eb6c`),
  `receipt-corrected-battery.txt` (`48530463…bab0`), `receipt-sweep-tail-witness.txt` (`dac49ba7…a009`).
- Scratch `/fast/scratch/hyaku/kengaku-r37/F37XMutP5` deleted after the receipts were copied out.
- Tooling: no installs; python3 stdlib only (`py_compile`, `importlib`, `subprocess`).

VERDICT: extra-mutants-p5-killed-2/4
