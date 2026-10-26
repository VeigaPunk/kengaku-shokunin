# F38MutDirection — mutation-testing `plans/mutant_direction_check.py` (the N21 direction evidence)

Seat: mutation-tester, kengaku round 38 wave 2 (falsify). Pinned tip under attack:
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a`, clean `--no-local` clone at
`/fast/scratch/hyaku/kengaku-r38/F38MutDirection/lane` (`git rev-parse --show-toplevel` = the clone path;
`git status --porcelain | wc -l` → `0` at setup; never committed). Lane untouched — sha256 of both target
files identical before/after (§5). Tools installed: none (no pacman, no uv, no binary). Scratch deleted at
the end (§6).

**Invariant under test:** the landed run of `plans/mutant_direction_check.py` distinguishes the frozen N21
mislabel — `DIR N21 D5 declared=silence observed=mirror MISLABELLED`, `DIRECTIONS total=22 mislabelled=1`,
exit 1 (landed receipt `.ufo/waves/round-38/integrate/direction-check.txt`, measured by the L1 at `d93b7d6`,
an ancestor of the pinned tip). **Detector:** run the (mutated) checker on the landed tree; the invariant
holds iff the run still prints `N21 … MISLABELLED` and exits 1.

## 1. Baselines (pristine bytes) — reproduced

cwd = the clone; `TMPDIR` and `--work` under the scratch only.

```
$ python3 plans/round38_c1_verify.py --lane . --work …/w-base-c1
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
PREDICATE C1 fail
exit=1                                     receipt-baseline-c1-counter.txt (81.67 s)
```
Byte-matches the landed `measure-final.txt` summary (`MUTANTS total=22 killed=21 survived=1`,
`PREDICATE C1 fail`). All 21 kills reproduce with named fixtures — N01←`b1run-n01-empty-pins`,
N02←`p3m-exact-min-distinct-locations`, N03←`p4a-second-row-line-outside`, N04←`p4a-text-elsewhere`,
N05←`p4b-case-only`, N06←`p4b-range-end-past-last`, N07←`p5m-row-off-pin-later-row`,
N08←`p5m-manifest-blank-line`, N09←`p6m-n09-teaches-one-below-min`, N10←`p6m-n10-url-scheme-http`,
N11←`p7m-n11-empty-recheck`, N12←`p7m-n12-first-row-url`, N13←`p10a-n13-trailing-space`,
N14←`p10a-n14-first-line-only`, N15←`p10b-rerun-byte-equal-accept`, N16←`b1run-n16-clause-crash`,
N17←`mainx-root-not-a-directory`, N18←`mainx-spec-invalid-json`, N19←`d4m-n19-last-pattern-unmatched`,
N20←`d4m-n20-pattern-case-differs`, N22←`d5m-n22-quote-prefix`; N21 `D5 silence SURVIVED`.

```
$ python3 plans/mutant_direction_check.py --lane . --work …/w-base-dir
DIR N21 D5 declared=silence observed=mirror MISLABELLED
DIRECTIONS total=22 mislabelled=1
exit=1                                     out-baseline-direction.txt (78.44 s)
```
The 23-line DIR block is byte-identical to the landed receipt
(`sed -n '3,25p' …/integrate/direction-check.txt | diff - out-baseline-direction.txt` → identical), so the
wave-1-reports commit `8c7422d` did not move it.

## 2. The three checker mutations (copies in the clone, each exactly one line from pristine)

| # | mutation (line in the copy) | N21 line | DIRECTIONS | exit | landed run still distinguishes? |
|---|---|---|---|---|---|
| m1 | `for dname in ("silence", "mirror"):` → `("silence",)` (l.78) | `observed=- UNWITNESSED` | `mislabelled=0` | 0 | **NO — survives** |
| m2 | `if direction in seen:` → `if seen:` (l.83) | `observed=mirror ok` | `mislabelled=0` | 0 | **NO — survives** |
| m3 | `verdict = "UNWITNESSED"` → `verdict = "ok"` (l.89) | `observed=mirror MISLABELLED` | `mislabelled=1` | 1 | **YES — caught** |

- **m1 ignore mirror** (`out-m1-ignore-mirror.txt`, 78.51 s; diff in `diffs.txt`): with mirror dropped from
  observation, N21 — and the three mirror-declared mutants N02/N08/N15 — go `UNWITNESSED`; N16 also loses its
  mirror observation (`observed=mirror,silence` → `observed=silence`). Exit 0: the landed signal is gone.
  The checker's N21 detection has no path that does not run through the mirror observation.
- **m2 accept any observed direction** (`out-m2-any-direction.txt`, 78.38 s): the only changed line is N21,
  `MISLABELLED` → `ok` (mirror observed). Exit 0. The declared-vs-observed comparison is the only mechanism
  that flags N21; nothing else in the output reds.
- **m3 UNWITNESSED counts as ok** (`out-m3-unwitnessed-ok.txt`, 78.63 s): output **byte-identical** to the
  pristine baseline (`diff` exit 0). On the landed tree no mutant is UNWITNESSED, so the mutated branch never
  fires; N21 is still `MISLABELLED` and the exit is still 1. Caught under the task's criterion (the landed
  run still distinguishes). Honest nuance: as a classic output-diff mutant, m3 is observationally equivalent
  on this input — the landed run exercises no UNWITNESSED branch, so it cannot distinguish the pristine
  checker from one that silences unwitnessed mutants. The UNWITNESSED-as-ok policy is not load-bearing for
  the landed signal, and the landed run provides no evidence about that branch either way.

**Count: 1 of 3 caught by the landed run.**

## 3. Relabel diagnostic (never the frozen claim)

Scratch copy `plans/round38_c1_verify_relabel.py` — one line from the frozen counter (l.140, N21 `silence` →
`mirror`). The counter is not among its own 14 pins, so `PINS mismatched=0` stays green:

```
$ python3 plans/round38_c1_verify_relabel.py --lane . --work …/w-rel
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N21 D5 mirror killed by=d5m-n21-manifest-row-2
MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
exit=0                                     receipt-relabel-counter.txt (81.67 s)
```
- The checker exits 0 and kills 22/22 as the task's diagnostic asks; independent reproduction of the L1's
  committed post-hoc receipt `.ufo/waves/round-38/integrate/n21-mirror-diagnostic.txt` (same four summary
  lines, same killing fixture `d5m-n21-manifest-row-2` — the accept fixture whose manifest carries the
  genuine digest row second).
- Cross-check, pristine direction checker against the relabelled counter
  (`--counter plans/round38_c1_verify_relabel.py`): `DIR N21 D5 declared=mirror observed=mirror ok`,
  `mislabelled=0`, exit 0 (`receipt-relabel-direction.txt`, 78.51 s) — `mirror` is the direction the battery
  actually witnesses, so the relabel is not merely predicate-reachable but witnessed.
- **The frozen claim is NOT relabelled:** the pristine counter at the landing tip still prints
  `killed=21 survived=1`, `PREDICATE C1 fail` (§1) — C1 stays an honest stop. The scratch copy is deleted
  with the scratch (§6); nothing landed.

## 4. Secondary observation: a crashed run shares the detection exit code

```
$ python3 plans/mutant_direction_check.py --lane . --work …/no-such-dir
  File "…/mutant_direction_check.py", line 53, in main
    root = pathlib.Path(tempfile.mkdtemp(prefix="k38-dir-", dir=a.work))
FileNotFoundError: [Errno 2] No such file or directory: '…/no-such-dir/k38-dir-alit5k4u'
CRASH_EXIT=1                               receipt-crash-bad-workdir.txt
```
`tempfile.mkdtemp(dir=…)` needs an existing parent; the unhandled traceback exits 1 — the same code that
means "mislabel found". At exit-code granularity a crashed run is indistinguishable from a detecting run;
only the output text separates them. The same failure is already recorded by a sibling
(`.ufo/waves/round-38/falsify/F38NoHarmSweep/receipts/37-mutant-direction.log`). No frozen claim rests on
the direction check's exit code alone, so this is a robustness note on the new tool, not a claim defect.

## 5. Restoration evidence

- Lane `plans/mutant_direction_check.py` sha256
  `7e0e2b789819cc95cbc0b28bce3ae110d6907f62bd1109f90108e077deaa2c14` before (first command of the seat) ==
  after (last evidence command); lane `plans/round38_c1_verify.py`
  `8069739990c7d3a87f34f4398ea5dc78821193d9fa55499e11e28c84e79c0a4f` before == after. The lane was never
  written by this seat (all writes: this falsify dir + the scratch).
- Mutated copies (hashes in `hashes.txt`, one-line diffs in `diffs.txt`): m1 `16955799…`, m2 `482b5aa4…`,
  m3 `7b4e2aa6…`, relabel `fbd06ca3…` — all inside the scratch clone, deleted with it.

## 6. Cleanup

`rm -rf -- /fast/scratch/hyaku/kengaku-r38/F38MutDirection` after the receipts above were copied here;
absence verified after deletion.

## Findings for the round

1. **The N21 explanation survives the attack.** The direction check flags N21 only via
   declared(`silence`) ∉ observed({`mirror`}); the relabel diagnostic shows `mirror` is witnessed by
   `d5m-n21-manifest-row-2` and makes the frozen predicate reachable (22/22, exit 0). The landed honest stop
   (21/22, `PREDICATE C1 fail`) is the correct frozen state; the relabel remains diagnostic-only, exactly as
   the L1's `10d2e97` commit already recorded.
2. **Coverage finding (surviving mutants m1, m2):** the direction check's mislabel signal is a single point
   of failure — destroy the mirror observation or the declared-vs-observed comparison and the landed run
   goes green (exit 0) with no other line changing. If this tool is to be load-bearing for a round-39
   re-freeze of the N21 cell, its signal currently has no redundant path. A surviving mutant is a coverage
   finding, not permission to change the contract.
3. **m3 is caught per the task's criterion but observationally equivalent on this input** — the landed run
   exercises neither the UNWITNESSED branch nor any unwitnessed mutant, so it cannot testify about that
   policy; the checker's UNWITNESSED class stays silent-by-design and untested by this tree.
4. Minor robustness note: a crashed run (missing `--work` parent) exits 1, the same code as a detection;
   only the output text separates them.

Receipts (this dir): `receipt-baseline-c1-counter.txt`, `out-baseline-direction.txt`,
`out-m1-ignore-mirror.txt`, `out-m2-any-direction.txt`, `out-m3-unwitnessed-ok.txt`,
`receipt-relabel-counter.txt`, `receipt-relabel-direction.txt`, `receipt-crash-bad-workdir.txt`,
`hashes.txt`, `diffs.txt`.

VERDICT: direction-check-mutants-1/3
