# R49C1ExecControls — the six frozen C1 controls against the round-49 counter candidate

Seat `R49C1ExecControls` (executor, leaf). Axis served: **calibration** (claim R49-C1). Wave: kengaku round 49
(hyaku run 10), v2 wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Scratch
`/fast/scratch/hyaku/kengaku-r49/R49C1ExecControls` (removed after the receipts were copied; §12).

Item executed: *run the six frozen C1 controls against the counter candidate on scratch trees: no fence; base
fence @3a548330; round-45 keyed fence; admit-all; refuse-all; name-keyed variant. Each control must print
`PREDICATE R49-C1 fail`; transcribe REV-prefixed receipts into
`.ufo/waves/round-49/w1/R49C1ExecControls/receipts/`. Controls run only on base/control trees, never on claimed
work.*

## 1. Result

**All six frozen controls print `PREDICATE R49-C1 fail` and exit 1 against the round-49 counter candidate
(`.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py`, sha256 `9c7b73e3…`), each on its own clean
`git clone --shared` of the stage-1 freeze `9d2900af…`, with the delivered r49 honest population (124 fixtures)
staged.** No control passes, so the counter is not refused by its controls (§5). A second, independent
implementation of the same frozen contract reproduces all six fails at both the stage-1 freeze and the base tip
`3a548330…` (§6), and the counter's own pass line is reachable on a synthetic in-`d` probe fence under synthetic
mutants (§7a) — the controls fail because they are bad fences, not because the counter cannot pass anything.

One calibration finding for the L1 (§8): the base-fence control's failure is carried **entirely by the novel
honest half** of the frozen population. At the battery-only population (104) with the mutants leg armed, the
base-fence control prints `PREDICATE R49-C1 pass`, exit 0 (§7c). Stage 2 must therefore commit `plans/honest49/`
(20 novel modules, `<H>`=124) *and* the mutant declaration together; either alone is not enough to keep this
control honest.

**VERDICT: controls-pass-as-required — 6/6 `PREDICATE R49-C1 fail`, exit 1, against the wave-1 counter candidate
at `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`, plus a stage-2 constraint on the honest population (§8). No
scored run on claimed work; no R49-C1 admission claimed.**

## 2. Axes named (godspeed step 1)

| axis | this seat moves | this seat must not move |
|---|---|---|
| **calibration** (primary) | the six frozen C1 controls, each of which must print `PREDICATE R49-C1 fail` on a base/control tree | no predicate line, control or kill rule re-frozen after any seat scored; no edit of `plans/round-49-claims.md` |
| coverage (adjacent) | nothing — C1 and C2 share no input | no C2 probe run, no C2 receipt |
| novelty / depth / operability / freshness / adjacency | nothing — control receipts only | nothing |

## 3. Freeze and ordering check, before any measurement (Q30)

All commands run against the committed lane tree, before the first counter run (measurements 09:23–09:32
-0300, 2026-10-28):

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
af88aab193e6034cb9b386472064e3c18fa90128
$ git -C … log -1 --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
$ git -C … diff --stat 9d2900af HEAD -- plans/        # empty: no plan changed after the freeze
$ git -C … ls-tree -r HEAD --name-only | grep -E 'plans/(round49_c1_verify|honest49|sealed49|mutants49)'
none
$ git show 9d2900af:plans/round-49-claims.md | sha256sum
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  -
$ sha256sum plans/round-49-claims.md
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  plans/round-49-claims.md
$ git show 3a548330:plans/fixture_fence.py | sha256sum ; git show 9d2900af:plans/fixture_fence.py | sha256sum
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  -
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  -
```

The stage-1 freeze exists in the committed tree and predates every measurement below; the stage-2 amendment
commit does **not** exist, so **no receipt here is a scored receipt on claimed work** and **the landed fence (the
claimed work) was never measured by this seat**. Every run is a control run on a base/control tree, all inside
this seat's scratch.

## 4. Instrument

- **Counter candidate (measured)**: `.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py`, sha256
  `9c7b73e31e64ef61c021324af5a10dfdd42c1d23163b20f784c93ab0c0dd0daa` (33 320 bytes; committed by the counter
  seat; digest re-checked at 09:27 and 09:32 and unchanged). It imports `plans/round46_c1_verify.py`
  (`ef19380e…`, digest-pinned) for the harness, strace envelope, sandbox and builder, and adds deltas (a)–(f).
  Its stage-2 literals are **unfilled** at wave 1: `HONEST_NOVEL_EXPECTED=0`, `HONEST_TOTAL=104`,
  `PINS_EXTRA={}`, `SEALED_TOTAL=12`, no mutant declaration in the tree.
- **Fences under test** (fence selected with the testing-only `--fence` override, so no receipt measures an edit
  of the lane's fence):

  | control | fence | sha256 |
  |---|---|---|
  | no fence | a path never created (`…/fences/ABSENT_fence.py`) | ABSENT |
  | base fence | `plans/fixture_fence.py` @ `3a548330` (identical at `9d2900af`) | `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` |
  | round-45 keyed | `.ufo/waves/round-45/claims/fences/keyed_name.py` | `d21a6a173c68b13ce9abcd2716f37afaed1930646faa43a266adfd4258b9452e` |
  | admit-all | `.ufo/waves/round-45/claims/fences/admit_all.py` | `6c3b9a18566a7045d679263867b64ff0735bc79a39abe7e57dfffd724f05d912` |
  | refuse-all | `.ufo/waves/round-45/claims/fences/refuse_all.py` | `fc38325360ee7058401ff88c738ce4a7f5e0d8e97196b605b4b57dfed79ef867` |
  | name-keyed variant | `.ufo/waves/round-48/w1/R48C1ExecControls/fences/name_keyed_variant.py` | `560b746eb7049686983099e24b87987124f513c2f562a457086d122ba474963f` |

- **Honest population**: staged at `plans/honest49/` from the r49 honest seat's delivered modules
  (`.ufo/waves/round-49/w1/R49C1ExecHonest/plans/honest49/modules/`: `r46novel` 9 + `novel48` 7 + `novel49` 4 =
  20 modules), whose `builder-receipt.txt` records `fixtures=124` and `novel_modules=20`. With the 104 battery
  fixtures that is the frozen `<H>` candidate 124. Because the candidate's `PINS_EXTRA` is empty, those 20 staged
  modules are counted but unpinned (`PINS total=66`, vs the 82 an armed stage 2 will print).
- **Method per control**: `git clone -q --shared <lane> <scratch>/trees/<name>/lane` → assert
  `git -C <clone> rev-parse --show-toplevel` equals the clone root → `git checkout -q <rev>` → stage
  `plans/round49_c1_verify.py` (the candidate) and `plans/honest49/*.py` → run under the round-46 envelope
  (`2a484c28d5dabe45fce8d2309c6c719b0380982f5592a72848c99fe13e8912ab`, the committed
  `.ufo/waves/round-46/claims/envelope.sh`) with `TMPDIR=<scratch>/tmp`, `PYTHONDONTWRITEBYTECODE=1`:

  ```
  envelope.sh <scratch>/env/<name> python3 plans/round49_c1_verify.py --lane . \
    --work <scratch>/work/<name> --jobs 8 --fence <fence-under-test>
  ```

  The staged artifacts make the clone dirty by exactly two entries; the candidate prints `TREE dirty=2
  (override)`, so nothing is hidden. Runner: `run_controls.py` in the scratch (digest-asserts the candidate
  before every run); it also regenerated the receipts below at the second revision.

## 5. The six controls — primary table (candidate `9c7b73e3…`, `REV 9d2900af…`, population 124)

Every row: measured HEAD `9d2900af41e4d1fc6022eff99010436fde6dbd93`, `PINS total=66 mismatched=0`, exit 1, last
line `PREDICATE R49-C1 fail`.

| control | REFUSALS clean/total | SEALED clean/total | HONEST admitted/refused (of 124) | BENIGN | REASON (verbatim) | receipt |
|---|---|---|---|---|---|---|
| no fence | 0/20 | 0/12 | 0/0, errors=156 | 0 | `refusals-not-clean,sealed-not-clean,honest-fixtures=124!=104,honest-not-admitted,mutants-total=0<12,mutants-declared=1,errors=156` | `candpop-…-no-fence.txt` |
| base fence | 20/20 | 12/12 | **113/11** | 113 | `honest-fixtures=124!=104,honest-not-admitted,mutants-total=0<12,mutants-declared=1` | `candpop-…-base-fence.txt` |
| round-45 keyed | 0/20 | 0/12 | 124/0 | 173 | `refusals-not-clean,sealed-not-clean,honest-fixtures=124!=104,mutants-total=0<12,mutants-declared=1` | `candpop-…-fence-r45-keyed.txt` |
| admit-all | 0/20 | 0/12 | 124/0 | 173 | same as round-45 keyed | `candpop-…-fence-admit-all.txt` |
| refuse-all | 20/20 | 12/12 | 0/124 | 0 | `honest-fixtures=124!=104,honest-not-admitted,mutants-total=0<12,mutants-declared=1` | `candpop-…-fence-refuse-all.txt` |
| name-keyed variant | 0/20 | 0/12 | 124/0 | 173 | same as round-45 keyed | `candpop-…-fence-name-keyed-variant.txt` |

(The `honest-fixtures=124!=104` and `mutants-total=0<12,mutants-declared=1` reasons are the candidate's
**unfilled stage-2 literals and absent mutant declaration**, present in every row; they are not control signal.
The per-leg columns are the control signal, and each control is separated by exactly the leg it breaks.)

Verbatim, base-fence control (the do-nothing control of §9 of the frozen claims):

```
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
TREE dirty=2 (override)
PINS total=66 mismatched=0
FENCE source=…/trees/candpop-base-fence/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=124 admitted=113 refused=11 read=0 hung=0 build_errors=0
BENIGN total=113
MUTANTS total=0 caught=0 floor=0/2 verdict=unmet
CALIBRATION advertised=32 contradicted=0
REASON honest-fixtures=124!=104,honest-not-admitted,mutants-total=0<12,mutants-declared=1
PREDICATE R49-C1 fail
```

The 11 honest refusals are `n03-detached-head, n07-reflog-gc, n08-tag-detached, n12-local-config-user,
n13-remote-origin, n14-stash-entry, n15-commit-graph, n16-notes-ref, n17-replace-ref, n18-shallow-fetch,
n20-linked-worktree` — i.e. the base fence over-refuses 11 of the 20 novel classes and none of the 104 battery
fixtures, consistent with round-48's measured `112/120` (8 of the r48 16) plus 3 of the four `novel49` classes.

Verbatim, round-45 keyed control (§5 hostile-leg shape):

```
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=124 admitted=124 refused=0 read=0 hung=0 build_errors=0
BENIGN total=173
CALIBRATION advertised=32 contradicted=0
REASON refusals-not-clean,sealed-not-clean,honest-fixtures=124!=104,mutants-total=0<12,mutants-declared=1
PREDICATE R49-C1 fail
```

The keyed/admit-all/name-keyed fences admit all 32 hostile modules **with `touches=0` on every run** (BENIGN,
never LEAK: delta (b) working), so the hostile legs cannot print `clean=<total>`; `contradicted=0` everywhere.

Verbatim, no-fence control (excluding the per-fixture rows):

```
REFUSALS total=20 clean=0 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=0 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=124 admitted=0 refused=0 read=0 hung=0 build_errors=0
ERRORS total=156
REASON refusals-not-clean,sealed-not-clean,honest-fixtures=124!=104,honest-not-admitted,mutants-total=0<12,mutants-declared=1,errors=156
PREDICATE R49-C1 fail
```

Every fixture decision errors (`HARNESS-ERROR RuntimeError: fence absent`), 156 = 124 honest + 32 hostile.

## 6. Cross-implementation receipts (independent counter, population 120)

To exclude "one buggy counter says fail", this seat also wrote the same frozen contract independently in scratch
(`round49_c1_verify.py`, sha256 `e52c3b519773d45e0d677e4adabe0acd365069095a30a2dd73a90c91def0fb82`, 495 lines,
derived mechanically from the committed round-48 v2 counter `8726e99b…` with `plans/honest49/` +
`plans/sealed49/` + the mutants leg added; scratch-only, not a deliverable and **not** offered as a landing
candidate). Its honest population was the 16 r48-delivered modules (`PINS total=82`, all digest-verified),
`<H>`=120. Six controls at `REV 9d2900af…` (`s1-control-c1-*.txt`) and six again at the base tip
`REV 3a548330…` (`base-control-c1-*.txt`), each on its own clone:

```
s1-control-c1-no-fence                  exit=1 fail  REFUSALS 0/20  SEALED 0/12  HONEST 0/120   errors=152
s1-control-c1-base-fence                exit=1 fail  REFUSALS 20/20 SEALED 12/12 HONEST 112/8
s1-control-c1-fence-r45-keyed           exit=1 fail  REFUSALS 0/20  SEALED 0/12  HONEST 120/0   BENIGN 169
s1-control-c1-fence-admit-all           exit=1 fail  REFUSALS 0/20  SEALED 0/12  HONEST 120/0   BENIGN 169
s1-control-c1-fence-refuse-all          exit=1 fail  REFUSALS 20/20 SEALED 12/12 HONEST 0/120
s1-control-c1-fence-name-keyed-variant  exit=1 fail  REFUSALS 0/20  SEALED 0/12  HONEST 120/0   BENIGN 169
(base-control-c1-*: identical shape at REV 3a548330…, base fence 112/8 of 120, keyed/admit-all/name-keyed
 BENIGN 169 with REFUSALS 0/20 SEALED 0/12, refuse-all 0/120, no-fence errors=152.)
```

Across the four independent control batches run by this seat — my implementation at two revisions (12 runs) and
the wave candidate at two population settings (12 runs, §5 and §7c) — **24/24 control runs print
`PREDICATE R49-C1 fail`, exit 1**; the only run that printed `pass` is the explicit stage-2 trap of §7c.

## 7. Diagnostics (labelled; not controls, not claims)

- **(a) Satisfiability of the pass line** — my counter on a synthetic in-`d` probe fence
  (`probe_fence_v2.py`, sha256 `1e04fa75…`, extracted digest-verified from the committed round-48 counter-seat
  appendix) with two synthetic mutants (`synthetic-c1-mutants.json`, sha256 `e25d8721…`; one inserts an outside
  `os.listdir` of the fixture parent, one refuses every repo):
  `MUTANT id=s01-outside-read caught=1 … read=120`, `MUTANT id=s02-refuse-all caught=1 … honest_refused=120`,
  `MUTANTS total=2 caught=2 floor=2/2 verdict=met`, `CALIBRATION advertised=32 contradicted=0`, `REASON -`,
  `PREDICATE R49-C1 pass`, **exit 0** (`sat-probe.txt`). The pass path is reachable, and the mutants leg catches
  both an outside-access regression and an over-refusal regression.
- **(b) No fence, the counter's own default path** — `plans/fixture_fence.py` *deleted* from the clone, no
  `--fence`, default mode: `FENCE … absent`, `TREE dirty=3`, `COPY f1…f10 ok`,
  `ERRORS total=152`, `HONEST fixtures=120 admitted=0 refused=0`, `REASON
  tree-dirty=3,refusals-not-clean,sealed-not-clean,honest-not-admitted,errors=152,mutants-unfrozen`,
  `PREDICATE R49-C1 fail` (`diag-no-fence-default-mode.txt`). Both shapes of the no-fence control fail.
- **(c) The base-fence control at the battery-only population, mutants armed** — the stage-2 trap. Candidate
  `9c7b73e3…`, population 104 (`--honest <empty>` so the candidate's own unfilled literal matches), fence =
  base fence, mutants = a 12-entry scratch manifest (`12-c1-mutants.json`, sha256 `c6131aa0…`: six copies of
  the round-45 admit-all fence — caught — and six copies of the base fence itself — survived):

  ```
  REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
  SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
  HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
  BENIGN total=104
  MUTANTS total=12 caught=6 floor=12/2 verdict=met
  CALIBRATION advertised=32 contradicted=0
  REASON -
  PREDICATE R49-C1 pass
  ```

  **exit 0** (`cand104mut-s1-control-c1-base-fence.txt`). Without the mutant manifest the same configuration
  fails only on `mutants-total=0<12,mutants-declared=1` (`cand104-s1-control-c1-base-fence.txt`). This is the
  frozen claims' "a control that passes refuses the counter": with `<H>`=104 and a met mutant floor, the
  **base fence passes the counter**.

## 8. Calibration findings for the L1 (stage-2 fill constraints)

1. **`<H>` must be 124, not 104.** The do-nothing base-fence control is clean on the 104 battery fixtures
   (`HONEST 104 admitted=104 refused=0`, §7c). All of its over-refusal lives in the 20 novel classes (11/124,
   §5). If stage 2 committed `plans/mutants49/c1-mutants.json` but not `plans/honest49/`, or dropped the novel
   half from `<H>`, the base-fence control would print `pass` and, under the frozen rule, the counter would be
   refused. Commit the 20 novel modules and set `HONEST_NOVEL_EXPECTED=20`, `HONEST_TOTAL=124`.
2. **`PINS_EXTRA` must be filled together with them.** The candidate prints `PINS total=66` while the 20 staged
   modules are unpinned; an unpinned population cannot print `PINS mismatched=0` at its armed form, and the
   modules must be pinned at their delivered digests (all 16 of n01–n16 were verified equal to the r48
   `PINS_EXTRA` values; the four `novel49` modules as delivered are `n17_replace_ref.py` `9f38f07a…`,
   `n18_shallow_fetch.py` `64ecb769…`, `n19_template_less_init.py` `d28745b7…`, `n20_linked_worktree.py`
   `75cc4fff…`, per the honest seat's `modules.sha256`).
3. **The mutants leg is still unfrozen** (`plans/mutants49/c1-mutants.json` absent from the tree; `<M>`=0,
   `verdict=unmet/unfrozen`). Every wave-1 control receipt therefore carries a mutants reason; the six-control
   test must be **re-run at stage 2** on the armed candidate (novel population + pinned + `<M>`≥12), because
   only an armed candidate can show the controls failing for their own legs alone.
4. **`plans/sealed49/` is still absent** (`<S>`=12); the sealed leg of these receipts measures the 12 round-46
   modules only.
5. **The controls are still sound where it matters**: each of the five non-trivial controls fails a *different*
   leg (base fence: honest; keyed/admit-all/name-keyed: hostile legs not clean with `contradicted=0`; refuse-all:
   honest; no-fence: harness errors), so the counter's legs are individually load-bearing and the BENIGN/LEAK
   split (delta (b)) behaves as frozen — 169 BENIGN-ADMITs with zero LEAK.

## 9. Limits

- The claimed work (`plans/fixture_fence.py` repair, any candidate fence) was **never** run by this seat. The
  fence candidates in `.ufo/waves/round-49/w1/R49C1ExecFenceA/` and siblings were not opened as fences under
  test, and no stage-2 or stage-3 artifact exists to score.
- The measured counter is a **wave-1 candidate**, not `plans/round49_c1_verify.py` at a stage-2 pin; its literals,
  pins, mutants and sealed extras are unfilled (§8). No number above is a claim about R49-C1 admission.
- The mutants leg was exercised only with synthetic manifests authored by this seat (§7a, §7c); the 12-entry
  manifest is a satisfiability device, not the stage-2 `<M>` battery.
- The honest population used `plans/honest49/` staged from the honest seat's **wave-dir** modules; they are not
  committed, so `TREE dirty=2` is disclosed by every receipt. Population sizes 104 / 120 / 124 are all reported
  with the receipt that measured them; only 124 matches the r49 delivered population.
- One nondeterministic fixture-builder failure was observed in ~36 control runs: the first `admit-all` run at
  `s1` raised `BUILD-ERROR refusal f16_objects_hardlink_out.py … rc=1` (`rename … objects/maintenance.lock`), the
  counter counted it in `build_errors`, and the control still failed. The run was repeated and the clean receipt
  (build_errors=0, BENIGN 169) is the one landed.

## 10. Tooling

No tool was installed or upgraded; no `pacman` transaction was attempted (PACMAN GUARD). No PATH directory was
written. `strace`, `bwrap`, `python3 3.14.8` were used as installed.

## 11. Evidence index

`.ufo/waves/round-49/w1/R49C1ExecControls/receipts/` (22 receipts + `INDEX.sha256`), each with a `#` header
carrying the exact command, measured HEAD, counter digest and fence digest, then the measured output starting
with its `REV <40-hex>` line:

| receipt | sha256 |
|---|---|
| `candpop-s1-control-c1-no-fence.txt` | `597456267e7a0b1d65c057a25cbf150d79a950e0a10cb3f3c382ecdb9159380b` |
| `candpop-s1-control-c1-base-fence.txt` | `07af82d8396ce3267c6055c9900553a9e3a9578520e0a9d503bb020f9e7097f0` |
| `candpop-s1-control-c1-fence-r45-keyed.txt` | `880ae33c5b44d77dc3296545c89a21ec6f1f1af774b5758d83fc0aacb0fae68f` |
| `candpop-s1-control-c1-fence-admit-all.txt` | `3199680fce48e7ac6c1897b4d37b0a1052f501b44824ae7f92780ce2bf7e2eac` |
| `candpop-s1-control-c1-fence-refuse-all.txt` | `d13aaad96fe202f277ecbeddb09fd104d59a43d162a52eee0aa8f1bbc0bdffa1` |
| `candpop-s1-control-c1-fence-name-keyed-variant.txt` | `0b858ef7a362e62997e48f496220316eaf10e62cad53db2882fe61b5e3359be9` |
| `s1-control-c1-*.txt` (6, independent counter, 120) | see `INDEX.sha256` |
| `base-control-c1-*.txt` (6, independent counter, base tip) | see `INDEX.sha256` |
| `cand104-s1-control-c1-base-fence.txt` | `32a4391f25d1bfa19e1c642d351172b3c3d266dfd752b21c7199b824a220983f` |
| `cand104mut-s1-control-c1-base-fence.txt` | `224db5a66f531b56e92958853315e493cb43c091ee2ffdfba5e30cc50cf0eeb8` |
| `diag-no-fence-default-mode.txt` | `42d7829f41aa94a32b67a3aa49c9eadb01a91e6411aab00b734c54969d17567c` |
| `sat-probe.txt` | `b38933948e3cba9fd75509862bccce506a4298ca962737f4469ab22e7dbe0686` |

Sources opened: **no external URL was opened by this seat**, so there is no URL/access-date/quote row to record.
Every input is a committed lane artifact named above with its digest, or a wave-dir artifact named with its path
(`R49C1ExecCounter/candidate.py`, `R49C1ExecCounter` is the counter candidate; `R49C1ExecHonest/plans/honest49/…`
is the honest population). Write scope respected: this report and `receipts/` only; no production file, commit,
push or sibling repo touched.

## 12. Scratch

`/fast/scratch/hyaku/kengaku-r49/R49C1ExecControls` (clones `trees/*/lane`, `work/`, `env/`, `fences/`,
`staging/`, `inbox/`, `receipts/`, `tmp/`) was created under `TMPDIR` and **removed after the 22 receipts were
copied into `receipts/` and hashed into `INDEX.sha256`**; no scratch tree is left on disk. The final `ls` of the
wave receipts dir is the check that the copied set survives the removal.
