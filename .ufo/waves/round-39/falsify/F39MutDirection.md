# F39MutDirection — mutation-testing the landed `plans/mutant_direction_check.py` (round-39 wave 2, falsify)

Seat F39MutDirection, mutation-tester. Target: the **landed** two-leg copy of `plans/mutant_direction_check.py`
(wave-1 seat R39DirCheckLeg's fix, landed by the L1 this round; sha256 `e471630abd27da4147c69d3feccdf6e5ad7969a47eae2fa053423636a412b09b`
at the tip — identical to the copy that report shipped). Pinned tip under attack:
`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch master), clean `--no-local` clone at
`/fast/scratch/hyaku/kengaku-r39/F39MutDirection/lane` (`git rev-parse --show-toplevel` = the clone path;
`git status --porcelain | wc -l` → `0` before and after; never committed). Lane untouched — sha256 of both
target files identical before/after (§5). Tools installed: none (no pacman, no uv, no binary). Scratch deleted
at the end (§6).

**Invariant under test** (wave-1 `R39DirCheckLeg.md` §2): mutating one leg "changes that leg's vote, and the
other leg's `MISLABELLED` still wins" — concretely, the landed run still prints
`DIR N21 D5 declared=silence observed=mirror MISLABELLED` **and exits 1**. The exit code is load-bearing by
Q29: "`DIRECTIONS total=<n> mislabelled=<m>`, exit 1 iff `m > 0`" (`corpus/QUALITY.md:511`).
**Detector:** run the (mutated) checker on the landed tree; the invariant holds iff the run still prints
`N21 … MISLABELLED` and exits 1 (same criterion F38MutDirection used, so the rounds are comparable).

Run template for every row below (S = the scratch; `TMPDIR=$S`; each run its own `--work` dir):

```
python3 <copy>.py --lane "$S/lane" --work "$S/w-<tag>"     # stdout+stderr → receipts/out-<tag>.txt, then "EXIT=<rc> WALL=<s>" appended
```

## 1. Baseline (pristine bytes) — calibration at the tip

```
$ python3 "$S/lane/plans/mutant_direction_check.py" --lane "$S/lane" --work "$S/w-base"
DIR N21 D5 declared=silence observed=mirror MISLABELLED
LEGS mutants=22 disagree=0 invalid=0
DIRECTIONS total=22 mislabelled=1
EXIT=1 WALL=88s                                    receipts/baseline.txt
```

All 22 `DIR` lines are byte-identical to the landed round-38 receipt
(`.ufo/waves/round-38/integrate/direction-check.txt`; diff of the `DIR `-prefixed lines → identical,
`receipts/calibration-vs-round38.txt`); the only additions are the `LEGS` line and the exit marker.
**Answer to task question 1: yes — the landed copy still prints `N21 … MISLABELLED` at the round-39 tip, exit 1.**

Note: `.ufo/waves/round-39/integrate/` contains no `direction-check.txt` — wave-1 §7's recommendation to
commit a fresh receipt at the landing was not taken; this baseline is the at-tip evidence.

## 2. The six mutants (copies in the scratch, each exactly one line from pristine; combo: two lines)

| copy | mutation (one line) | `DIR N21` line | `DIRECTIONS` | exit | caught? |
|---|---|---|---|---|---|
| pristine | — | `declared=silence observed=mirror MISLABELLED` | `mislabelled=1` | 1 | baseline |
| m1 (replay) | `for dname in ("silence", "mirror"):` → `("silence",)` | `observed=mirror MISLABELLED legs=UNWITNESSED,MISLABELLED` | `mislabelled=1` | 1 | **YES** |
| m2 (replay) | `if direction in seen:` → `if seen:` | `observed=mirror MISLABELLED legs=ok,MISLABELLED` | `mislabelled=1` | 1 | **YES** |
| m3 (replay) | `first = "UNWITNESSED"` → `first = "ok"` | unchanged (byte-identical) | `mislabelled=1` | 1 | **YES** (invariant sense) |
| n1 (new) | `other.update(second_leg(clause, direction, fx, argv, ref[j], mut))` → `pass` | `observed=mirror MISLABELLED legs=MISLABELLED,UNWITNESSED` | `mislabelled=1` | 1 | **YES** |
| n2 (new) | `if "MISLABELLED" in (first, second):` → `if first == "MISLABELLED":` | unchanged (byte-identical) | `mislabelled=1` | 1 | **YES** (invariant sense) |
| n3 (new) | `return 1 if mis else (3 if (split or invalid) else 0)` → `return 0 if mis else …` | unchanged (byte-identical) | `mislabelled=1` | **0** | **NO — survives** |

**Count: 5/6 caught; 1 survivor (n3).** Every single-mutant diff is exactly `+1/-1` line, combo `+2/-2`
(`receipts/diffs-*.txt`, sizes in `receipts/byte-identity-and-diffsizes.txt`); hashes in `receipts/hashes.txt`.

- **m1** (F38's survivor on the old copy): leg 1 loses the mirror observation — N02/N08/N15 fall to
  `LEGS-DISAGREE legs=UNWITNESSED,ok` (`disagree=3`) and N21's leg 1 says `UNWITNESSED` — but leg 2 still
  reports `MISLABELLED` on N21, so the verdict and the exit survive. The wave-1 claim holds under replay.
- **m2** (F38's survivor on the old copy): leg 1 accepts any observation as the declared one (`ok`); leg 2
  keeps the strict comparison; verdict `MISLABELLED`, exit 1. Holds.
- **m3**: F38's line `verdict = "UNWITNESSED"` no longer exists in the landed copy; the analog is leg 1's
  `first = "UNWITNESSED"` (the same choice wave-1 made for its new-m3). Output byte-identical to the baseline
  (`diff` → 0 lines): on this input no mutant is UNWITNESSED, so the branch never fires. Caught per the
  detector; the honest nuance is F38's: observationally equivalent on this tree, the branch untested by it.
- **n1** (sever leg 2 entirely): leg 1 alone still flags N21 (`MISLABELLED legs=MISLABELLED,UNWITNESSED`) and
  the severed leg leaves a loud fingerprint — 21 `LEGS-DISAGREE legs=ok,UNWITNESSED` rows,
  `LEGS mutants=22 disagree=21 invalid=0`, exit 1. Destroying the *new* leg is caught both by the verdict
  and by the noise.
- **n2** (merge demoted to leg-1-only): byte-identical to the baseline on this input — N21's leg 1 says
  `MISLABELLED` anyway, so the demoted merge still wins. Caught per the detector; the "either leg suffices"
  merge path is not exercised by any single mutant here — see the compound probe (§3).

## 3. The survivor is a coverage finding: the exit-code channel is a single point of failure

n3 flips the final exit mapping (`return 1` → `return 0` when `mis > 0`). Every printed line — including
`DIR N21 … MISLABELLED` and `DIRECTIONS total=22 mislabelled=1` — stays byte-identical to the baseline
(`receipts/out-n3-exit-flip.txt`, `EXIT=0`); only the exit code breaks. Q29's contract is
"exit 1 iff `m > 0`" (`corpus/QUALITY.md:511`), and the two-leg design protects the *printed verdict* but
nothing protects the *exit code*: the final `return` maps `mis` to the exit in one line with no redundant
derivation, so a consumer keying on the exit code sees green on a mislabelled run. (Context: F38 §4 already
recorded that exit 1 is also what an uncaught crash produced; the landed copy narrowed that to setup failures
exiting 2, but the detection exit itself remains one edit from silence.) A surviving mutant is a coverage
finding, not permission to change the contract.

**Compound probe** (bonus, two lines — `combo-m1n2`, not one of the six): leg 1's observation destroyed (m1)
**and** the merge demoted (n2) together: N21 prints `LEGS-DISAGREE legs=UNWITNESSED,MISLABELLED`,
`DIRECTIONS total=22 mislabelled=0`, `LEGS mutants=22 disagree=4 invalid=0`, **exit 3**
(`receipts/out-combo-m1n2.txt`). So the "either leg suffices" merge is load-bearing for the verdict *text*
(losing it plus leg 1 loses the word `MISLABELLED`), but the design fails closed: exit 3, never 0. No
one-line or two-line attack on the verdict path measured here can turn the run green; only the exit-code
channel (n3) breaks the invariant.

## 4. Round-39 list: cannot load (measured on the landed copy at the tip)

```
$ python3 "$S/lane/plans/mutant_direction_check.py" --lane "$S/lane" --counter plans/round39_c1_verify.py --work "$S/w-r39"
SETUP counter plans/round39_c1_verify.py is not a round-38-list counter: missing=battery38_fixtures,attributed non_6_tuple_rows=7; this check reads the round-38 MUTANTS rows (id, clause, dir, adv, old, new) and its battery38 loader only
EXIT=2                                             receipts/out-r39-counter.txt
```

Fails closed with the named-surface message (no traceback), exit 2. R39CritClaims §7's finding reproduces on
the landed copy: the tool cannot load the round-39 list (`module_fixtures` loader, 7-tuple `MUTANTS` rows);
for that list the redundancy Q29 wants is the counter's own `exhibits=` line. **Answer to task question 3: no.**

## 5. Restoration evidence

- `sha256sum` before (first evidence command of the seat) == after (last): lane
  `plans/mutant_direction_check.py` `e471630abd27da4147c69d3feccdf6e5ad7969a47eae2fa053423636a412b09b`,
  lane `plans/round38_c1_verify.py` `8069739990c7d3a87f34f4398ea5dc78821193d9fa55499e11e28c84e79c0a4f`
  (`receipts/restoration-hashes.txt`).
- `git -C "$S/lane" status --porcelain | wc -l` → `0`; `git -C "$S/lane" rev-parse HEAD` → `a6832f53…`
  (the clone was never mutated; all mutant copies live outside it in `$S/mut`).
- Mutant copies (all inside the scratch, deleted with it): m1 `29fac5da…`, m2 `86ab30a0…`, m3 `286fa5d4…`,
  n1 `e21f53a9…`, n2 `74dd5b94…`, n3 `dcebbb69…`, combo `084ec030…` (`receipts/hashes.txt`).

## 6. Cleanup

`rm -rf -- /fast/scratch/hyaku/kengaku-r39/F39MutDirection` after the receipts were copied here; absence
verified after deletion. No process left running. No tool installed or upgraded (none needed; pacman
untouched). No lane file, fleet-root file or git index written by this seat; all writes were this report dir
and the scratch.

## Findings for the round

1. **The landed two-leg copy holds its claimed invariant under all three F38 replays.** m1 and m2 — which
   turned the round-38 copy green (exit 0) — now leave `N21 … MISLABELLED` intact with a visible `legs=`
   fingerprint; m3 stays observationally equivalent on this input (branch unexercised), the same nuance
   round 38 recorded.
2. **Coverage finding (surviving mutant n3):** the exit-code channel is a single point of failure — one line
   (`return 1` → `return 0` under `mis`) breaks Q29's "exit 1 iff `m > 0`" while every printed line stays
   byte-identical. If the exit code is to stay load-bearing it needs what the verdict got (a redundant
   derivation, e.g. from both legs' counts), or Q29/QUALITY should name the printed lines as the primary
   channel. Not fixed here — a surviving mutant is a finding, not a mandate.
3. **Compound probe:** destroying leg 1's observation *and* the merge degrades the verdict to
   `LEGS-DISAGREE` (`mislabelled=0`) but exits 3 — fail-closed. The verdict path cannot be turned green by
   any one-line or two-line attack measured here.
4. **r39-list: no** — confirmed on the landed copy at the tip (`SETUP …`, exit 2), matching R39CritClaims
   §7; the port (7-tuple rows + `module_fixtures`) remains unlanded and is not this seat's to write.
5. Minor: no fresh `.ufo/waves/round-39/integrate/direction-check.txt` was committed at the landing
   (wave-1 §7's recommendation); the round-38 receipt stays historical and this seat's baseline is the at-tip
   evidence. Also Q29's Check sentence (`corpus/QUALITY.md:509-511`) names only
   `ok|MISLABELLED|UNWITNESSED` — the landed copy can additionally print `LEGS-DISAGREE` and `legs=` tails;
   the doc delta R39DirCheckLeg §7 flagged still stands.

Receipts (this dir): `baseline.txt`, `out-m1-ignore-mirror.txt`, `out-m2-any-direction.txt`,
`out-m3-unwitnessed-ok.txt`, `out-n1-sever-leg2.txt`, `out-n2-merge-leg1-only.txt`, `out-n3-exit-flip.txt`,
`out-combo-m1n2.txt`, `out-r39-counter.txt`, `diffs-m1-ignore-mirror.txt`, `diffs-m2-any-direction.txt`,
`diffs-m3-unwitnessed-ok.txt`, `diffs-n1-sever-leg2.txt`, `diffs-n2-merge-leg1-only.txt`,
`diffs-n3-exit-flip.txt`, `diffs-combo-m1n2.txt`, `hashes.txt`, `calibration-vs-round38.txt`,
`byte-identity-and-diffsizes.txt`, `restoration-hashes.txt`.

VERDICT: direction-check-mutants-5/6-r39-list-no
