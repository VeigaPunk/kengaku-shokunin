# F37CritOverfit — attacking the meaning of C1's `BATTERY … wrong=0` line

Seat: critic (round-37 wave 2, falsify). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at tip
`357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`. Work done on a `--no-local` clone of the tip under
`/fast/scratch/hyaku/kengaku-r37/F37CritOverfit/` (removed before yield); nothing was written in the lane.
The lane HEAD has since moved to `dc90676`; `git diff --name-only 357deceb… HEAD` shows only `.ufo/` wave
artifacts plus `corpus/lessons/round-37.md`, and `plans/pkg_gate.py` is still at its freeze digest
`ea638822…`, so the measured surface is unchanged.

Targets named explicitly: the frozen predicate's first line (`BATTERY fixtures=<n> wrong=0
renamed_disagree=0`), the counter docstring's "battery check" paragraph, the claims file's `Battery:`
bullet, and the `plans/battery37/*.py` docstrings.

## What was built

`overfit_gate.py` — a drop-in `package` / `d4-line` / `d5-line` gate with **no clause logic**: no quote
parsing, no digest pins, no registry rows, no manifest, no probe, no `git` call, no subprocess. It reads
exactly two things (`overfit_gate.py:47-63`):

| cue | what it is | distinct values seen |
|---|---|---|
| 1 | invocation shape: subcommand + flag set | 3 subcommands, 3 flag sets |
| 2 | one canonical content fingerprint of the working files (relative path → sha256, skipping `.git/` and `__pycache__/`; `.git` presence recorded as one marker; `d5-line` also fingerprints `--capture-dir`) | 64 (one per fixture) |

and answers from a 64-entry literal table (`overfit_gate.py:64-129`). Table built by `derive_table.py`:
it calls the counter's own `r36_fixtures` / `battery37_fixtures` / `Ctx` / `run_gate`, records the frozen
gate's `(exit, DEFECT set)` per fixture, and checks the cue is (a) unchanged by the gate's own side effects
(`P10` byte-compiles the captured grader into `__pycache__/`, which the fingerprint skips) and (b) equal on
the counter's renamed copies (`.git/` contents are skipped and its presence kept as one marker, so the cue
is copy-invariant). Result: `TABLE keys=64 fixtures=64 problems=0` (`receipt-derive.txt`).

### It matches

`run_counter.py` imports `plans/round37_c1_verify.py` from the clone and calls its `main()` twice, then
cross-checks `run_gate` fixture by fixture (`receipt-counter.txt`):

```
=== A genuine gate, counter battery path ===
BATTERY fixtures=64 wrong=0 renamed_disagree=0 | exit 0
MUTANTS: MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
=== B overfit gate as the reference gate (module.GATE_REL/SHA256 monkeypatched to it) ===
BATTERY fixtures=64 wrong=0 renamed_disagree=0 | exit 1
MUTANTS: MUTANTS total=55 killed=0 survived=0 invalid=55 null_detected=0
WRONG/DISAGREE lines: 0
=== C per-fixture cross-check ===
CROSSCHECK fixtures=64 overfit_mismatches=0 renamed_mismatches=0 receipt_rows=64 unlisted=0
```

Line B is bit-identical to the landing's `BATTERY` line and to the receipt's 64 fixture rows. Exit 1 in B
is expected and is not a defect of the overfit: the counter mutates the *reference text*, and my gate
contains none of the 55 `old` strings, so all mutants read `invalid` — the gate is incapable of killing a
branch because it implements none. The 64 fixture rows, the renamed run and the null run are all clean.

Out-of-table behaviour is honest: the genuine package is accepted (`defects=0`, exit 0); the same tree with
one byte appended to the entry file is refused with exit 2 (`setup: fixture is outside the demonstrated
set`) — `receipt-drift.txt`. The gate is a table over this tip's fixture bytes, nothing more.

## Findings

**F1 (matched; primary).** `BATTERY fixtures=64 wrong=0 renamed_disagree=0` carries no information about
the advertised defect classes: a 2-cue, 64-key content lookup reproduces it exactly, on both the 50
battery37 fixtures and the 14 round-36 fixtures, including the renamed run. The line pins *which byte
strings* the fixtures are, not *what the gate checks*. 64 fixtures collapse to 18 output classes (1 accept +
17 distinct DEFECT sets), so the line's information content is the 64 identities, not the classes.

**F2 (provenance).** The declarations are transcriptions of the frozen gate's own output, not independent
predictions. `plans/battery37/p4.py:9`: "Declared `defects` are exactly the clauses the UNMODIFIED gate
prints `DEFECT` on the fixture"; `plans/battery37/d4.py:22`: "Every fixture declares defects ["D4"]: … the
unmodified gate prints exactly `D4 DEFECT …`"; `plans/battery37/p910.py:5-6` likewise. With the gate held
at its freeze digest, `wrong` can only move if a *fixture input* moves (the fixtures rebuild from the live
`corpus/` bytes) or a battery module is edited — it can never reveal a mis-specified class. F1 supplies the
matching operational proof: the checker of that line need not read any clause.
Claim text at `plans/round-37-claims.md` (Battery bullet) presents the match as a requirement on the gate
("the unmodified gate must match each declaration") without naming that provenance, so a reader can take
`wrong=0` for calibration evidence. It is a drift pin.

**F3 (closure is 1:1 by construction; identity is the only cheap cue).** 50 battery37 fixtures for the 50
mutants that survived at freeze (5 frozen demonstrations + 50 = the 55 total); the modules state "one
single-defect fixture per frozen mutant". So no class is demonstrated by a second, independent fixture.
The fixtures are also not separable by any coarse property: keying on "*which* working files differ from
the genuine package" leaves 17 of 64 fixtures ambiguous across 6 classes (all entry-file-only mutations);
adding the entry file's byte size and line count still leaves 4 fixtures ambiguous (`receipt-cues.txt`):

* `p4-one-char-off` (12654 bytes, 156 lines) → `['P4']` vs `p7-m30-verified-at` (same size/lines) → `['P7']`
* `p4-capture-unreadable` (12660, 156) → `['P4','P5']` vs `p7-m29-source-url` (same size/lines) → `['P7']`

That is why cue 2 had to be exact content identity: the fixture set is 64 isolated byte instances, not a
lattice of shared class-relevant structure. The cheap overfit exists, but only as a lookup table over the
fixtures themselves — which is precisely the sense in which the declarations do not pin the classes.

**F4 (small).** The predicate string leaves the fixture count unconstrained (`fixtures=<n>`); with F1 the
only remaining guard in that half of the line is `wrong=0`, and the count is not pinned by the printed
string. The kill line is what keeps the predicate sound: dropping fixtures that do not kill loses
`killed=55`, so the exposure is limited to how the line is read, not to the predicate's truth.

## What this does not show

The overfit lookup cannot kill mutants and does not show any gate check is wrong. Mutant kills compare the
genuine gate with one branch silenced on the same fixture bytes, so they remain valid evidence that each
branch is reachable and load-bearing — my gate reproduces the *reference outputs*, not the branches. The
attack is on the reading of `wrong=0` and on the independence of the declarations, not on `killed=55`.

Impacted axes: **calibration** (the C1 evidence channel's meaning; F1–F3), **depth** (the closure count is
a construction, not an accumulation of independent observations; F3). Coverage, novelty, freshness,
adjacency, operability unaffected. Severity: low — the frozen predicate still passes for the right reason
(kills), and the fix is documentary.

Smallest safe correction (no lane edit is possible from this seat; the gate and predicate are frozen):
in `plans/round37_c1_verify.py`'s "battery check" paragraph and in the claims file's `Battery:` bullet,
one sentence: *battery37 `defects` are transcribed from the frozen gate's own output; `wrong=0` detects
fixture-input drift, and class coverage is evidenced only by `killed=55`.* Optionally record in
`corpus/lessons/round-37.md` that the declaration channel is identity-satisfiable (this report's receipts).

## Reproduce

```
S=/fast/scratch/hyaku/kengaku-r37/F37CritOverfit      # scratch, removed after this report
git clone -q --no-local <lane> $S/fx/lane && git -C $S/fx/lane checkout -q 357deceb…
cd .ufo/waves/round-37/falsify/F37CritOverfit
python3 derive_table.py --lane $S/fx/lane --work $S/work2 --outdir .        # TABLE keys=64 problems=0
python3 run_counter.py  --lane $S/fx/lane --work $S/work3 --gate $PWD/overfit_gate.py \
        --receipt $S/fx/lane/.ufo/waves/round-37/integrate/measure-final.txt
python3 cue_reduction.py --lane $S/fx/lane --work $S/work4 --table overfit_table.json
```
Receipts in this directory: `receipt-derive.txt`, `receipt-counter.txt`, `receipt-cues.txt`,
`receipt-drift.txt`; artifacts: `overfit_gate.py`, `overfit_gate_template.py`, `derive_table.py`,
`run_counter.py`, `cue_reduction.py`, `overfit_table.json`, `probe.py`. No tool was installed or upgraded
for this seat.

VERDICT: overfit-gate-matches-cues-2
