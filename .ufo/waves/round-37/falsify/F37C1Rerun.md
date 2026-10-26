# F37C1Rerun — C1 calibration re-run (kengaku r37, wave 2 falsify, 2026-10-26)

Seat: F37C1Rerun (executor, leaf). Target: the landing's C1 predicate, its receipt and the frozen digests.
All runs on my own clone under `/fast/scratch/hyaku/kengaku-r37/F37C1Rerun` (TMPDIR exported); no lane file
written, no lane git/jj command run, no counter run on the lane.

## Setup (fixture rule, verified before any write)

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
$ git -C "$D/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
TOPLEVEL=/fast/scratch/hyaku/kengaku-r37/F37C1Rerun/fx/lane
HEAD=357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
$ git -C "$D/lane" status --porcelain | wc -l
0
```

Clean clone of the assigned tip, clean working tree.

## 1. C1 counter re-run at 357deceb — PASS

```
$ cd "$D/lane" && python3 plans/round37_c1_verify.py --lane .   # TMPDIR in scratch
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
exit=0
```

Wall time 82.5 s. Full output 123 lines, 10416 bytes, sha256 `651bcf54…0d` (receipt copy
`F37C1Rerun/c1-rerun-357deceb.txt`). All three predicate lines present as frozen in
`plans/round-37-claims.md:38-41`; the battery figure `fixtures=64` is the `<n>` of the frozen predicate.

## 2. Diff against `.ufo/waves/round-37/integrate/measure-final.txt` (C1 part)

Extracted the receipt's C1 block (from `$ python3 plans/round37_c1_verify.py --lane .` up to the next `$`)
and diffed it against my run:

```
$ diff -u receipt-c1-section.txt c1-out.txt ; diff_exit=1 ; diff_bytes=385
@@ -121,4 +121,3 @@
 MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
 PREDICATE C1 pass
-exit=0
```

The single difference is the receipt's wrapper line `exit=0` (the receipt appends the shell status; my run
recorded `exit=0` separately). All 123 counter lines are byte-identical: every `FIXTURE`, `MUTANT`, `BATTERY`,
`MUTANTS` and `PREDICATE` line matches, including each mutant's `killed by=` fixture id. `c1-vs-receipt.diff`
retains the hunk.

One receipt-vs-assignment note: `measure-final.txt:1` records `TIP 5c7d5d75c2f36eb3477594432afe186b8b220086`,
not 357deceb. `git diff --stat 5c7d5d75 357deceb` touches only `.ufo/`, `SCORECARD.md`,
`corpus/lessons/round-37.md`, `plans/round37_c1_attribution.py` — no gate, counter, spec or battery file — and
the re-run at 357deceb reproduces the receipt byte for byte, so the TIP label lags by two commits without
changing the measurement.

## 3. Frozen digests (gate + instrument)

```
$ sha256sum plans/pkg_gate.py plans/round37_c1_verify.py plans/pkg-spec-r37.json plans/round36_c1_verify.py   # in clone
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  plans/pkg_gate.py
dbc9f7199381f5bbd708458bedc45cd199cee38a6440a2968a886229173413cc  plans/round37_c1_verify.py
4c61d103cff74021fec4dcedb27b6f5d85a3b5d6b11c1b4eda7df0ebe909c9b6  plans/pkg-spec-r37.json
d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73  plans/round36_c1_verify.py
```

`plans/pkg_gate.py` = `ea63882240e6…edd41`, identical to the frozen digest in `plans/round-37-claims.md:29`
(`ea63882240e67e9…` — "the gate at its freeze digest") and to `.ufo/waves/round-37/claims/frozen-digests.txt:5`.
The counter, the r37 spec and the round-36 battery module also match `frozen-digests.txt` lines 1, 4, 6 exactly.
The same `sha256sum` run read-only against the lane (`/home/vgpnk/Projects/shokunin/kengaku-shokunin`) gives the
same four digests, so the landing's gate is the frozen gate, not a look-alike.

## 4. Digest clause is machine-enforced, not merely printed

Perturbed copy (my clone only): `pkg_gate.py` sha256 `2ed702fb…b61c`.

```
$ python3 plans/round37_c1_verify.py --lane . --only M01
GATE plans/pkg_gate.py sha256=NOT-AT-FREEZE-DIGEST
MUTANT M01 P1 invalid -- frozen instrument digest mismatch
MUTANTS total=1 killed=0 survived=0 invalid=1 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=1
```

`plans/round37_c1_verify.py:357-360` makes every mutant `invalid` when `not gate_ok`, and `good` (line 385)
requires `invalid == 0`, so an off-digest gate cannot print `PREDICATE C1 pass`. This matches the frozen
skip-control (`plans/round-37-claims.md:49-50`: "editing the gate so mutants stop applying gives invalid=55").

## 5. Battery composition and mutant list

```
r36_fixtures= 14 battery37= 50 sum= 64
battery37 ids= 50
MUTANTS= 55 TOTAL= 55 unique= 55
per-clause: {'P1': 1, 'P2': 2, 'P3': 5, 'P4': 4, 'P5': 7, 'P6': 8, 'P7': 6, 'P8': 5, 'P9': 2, 'P10': 3, 'D4': 4, 'D5': 8}
```

`ls plans/battery37/*.py | wc -l` = 9 (d4, d5, p23, p4, p5, p6, p7, p8, p910). Per-clause counts sum to 55 and
all 12 advertised classes (P1–P10, D4, D5) carry at least one mutant, so no advertised class is unreachable by
construction. Fixture ids are unique (the counter itself would `SETUP duplicate fixture id` → exit 2).

Observation (wording, not a predicate defect): 7 of the 50 battery37 fixtures declare more than one `DEFECT`
clause — `p7-m28-entry-deleted` declares `P3,P4,P7,P8`, `p4-capture-unreadable` `P4,P5`,
`p910-probe-exits-1` `P1,P10`, `p910-receipt-deleted`/`p910-receipt-one-byte` `P10,P2`,
`p23-p3-heading-renamed`/`p4-no-quote-row` `P3,P4`. So "single-defect fixtures" (assignment wording, commit
a3163e6 subject) is loose; the frozen rule only requires each fixture's exact declared set, and all 64
declarations match observation (`wrong=0`).

## 6. Determinism and tip drift: identical output at the live lane HEAD

The lane HEAD has moved past the assigned tip: `git log --oneline -1` → `dc90676 round-37: close lesson (wave 2
dispatched, not integrated under the request budget), falsify ready marker`, and
`merge-base --is-ancestor 357deceb dc90676` → 357deceb IS ancestor of dc90676.

```
$ git clone -q --no-local <lane> "$S/fx/head"; git -C "$S/fx/head" checkout -q dc90676…
HEAD_CLONE=dc90676b0a01bcb278dba3b5231b504fe2a9ff03 TOP=/fast/scratch/hyaku/kengaku-r37/F37C1Rerun/fx/head
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  plans/pkg_gate.py
dbc9f7199381f5bbd708458bedc45cd199cee38a6440a2968a886229173413cc  plans/round37_c1_verify.py
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
exit=0
$ diff c1-out.txt c1-head.txt && echo IDENTICAL
IDENTICAL 357deceb-vs-dc90676
```

Both runs are byte-identical (`sha256 651bcf54…`), so the drift of `corpus/lessons/round-37.md` and
`SCORECARD.md` between 357deceb and dc90676 does not change the C1 reading, and the run is reproducible across
invocations (two independent clones, two runs, same 123 lines).

## 7. Kill attribution re-run (does `killed=55` mean 55 demonstrated clauses?)

Re-ran the non-frozen post-hoc audit at 357deceb:

```
$ python3 plans/round37_c1_attribution.py --lane . --work "$S"
ATTRIBUTED 55/55 UNATTRIBUTED=0
exit=0                                  # 14.4 s
```

Diff against `.ufo/waves/round-37/integrate/c1-attribution.txt` is again only the trailing wrapper `exit=0`
line (`attribution-vs-receipt.diff`, 423 bytes), i.e. all 55 `ATTR <mid> <clause> by=<fixture>` lines match,
fixture id for fixture id. Each kill therefore has a fixture that (a) declares the mutant's clause, (b) prints
that clause as `DEFECT` in the reference run, and (c) stops printing it under the mutant.

## 8. Falsification of the kill criterion itself (my own probe, scratch only)

The frozen counter kills a mutant on the first fixture whose `(exit code, DEFECT set)` differs
(`plans/round37_c1_verify.py:361-382`, `differs` at 339-345). That admits two degenerate kills: a gate **crash**
(traceback, exit 1, no `DEFECT` lines) and a kill where the mutant's clause is **still** reported. I re-implemented
the counter's own first-diff ordering and classified each first kill (`F37C1Rerun/crashprobe.py`, kept as evidence):

```
$ python3 crashprobe.py "$D/lane" "$S"
PROBE mutants=55 clause_gone=55 crashkill=0 clause_still_reported=0 survived=0
exit=0                                  # 76.7 s
```

No mutant's first kill is a traceback or a non-0/1 exit, and in every case the mutant's own clause is absent
from the resulting `DEFECT` set while the gate exits cleanly. So on this battery `killed=55` is not obtained
through crashes and not through "other clauses changed, mine still printed". This closes the two cheap ways to
inflate the kill count that the frozen rule leaves open.

## 9. Retained limits (unchanged, already frozen)

- The kill criterion is observational: `killed=55` plus attributed 55/55 shows each branch is reached and its
  result visible, not that each check is the right check (`plans/round-37-claims.md:59-60`).
- For an *arbitrary* battery the criterion stays gameable: the landing records a hostile side-channel battery
  that still kills `55/55` while attributing only `6/55` (`.ufo/waves/round-37/integrate/c1-attribution-hostile.txt`,
  first three lines `BATTERY fixtures=17 wrong=0 renamed_disagree=0` / `MUTANTS total=55 killed=55 …` /
  `ATTRIBUTED 6/55 UNATTRIBUTED=49`). The predicate is safe only because it fixes the battery path
  (`plans/battery37`), which is what this re-run measured.
- Excluded branches named at freeze (P1 `frozen_instruments` empty branch, setup paths, P10 `OSError`, crash
  handlers, option gating) remain uncounted; I did not attempt them.

## Files changed by this seat

None in the lane. Written only:
`.ufo/waves/round-37/falsify/F37C1Rerun.md` (this report) and
`.ufo/waves/round-37/falsify/F37C1Rerun/` — `c1-rerun-357deceb.txt`, `c1-rerun-dc90676.txt`,
`receipt-c1-section.txt`, `c1-vs-receipt.diff`, `attribution-rerun.txt`, `attribution-vs-receipt.diff`,
`crashprobe.py`, `crashprobe.txt`, `gate-edit-preflight.txt`. Scratch `/fast/scratch/hyaku/kengaku-r37/F37C1Rerun`
deleted after the receipts were copied out.

## Risks / blockers

- No blocker. C1 satisfies its frozen predicate on a clean clone of the assigned tip, on the live lane HEAD, and
  with the gate/counter/spec/round-36 module all at their freeze digests.
- Residual risk is only the frozen limit above (observational demonstration; battery-path dependence), both
  already disclosed at the landing.
- Tooling: nothing installed or upgraded; no pacman transaction attempted.

VERDICT: c1-rerun-pass-killed-55/55
