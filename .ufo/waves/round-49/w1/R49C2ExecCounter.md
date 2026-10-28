# R49-C2 executor seat — v4 counter for the TB2 `polyglot-c-py` admission (round 49, wave 1)

seat: `R49C2ExecCounter` (executor) · claim served: **R49-C2** (coverage) · milestone: kengaku round 49
(hyaku run 10), one v2 build-and-attack wave · write scope: this report, `w1/R49C2ExecCounter/candidate.py`
and `w1/R49C2ExecCounter/receipts/` only.

**Axes named: coverage.** Nothing else was measured or claimed; calibration (C1), novelty, depth, operability,
freshness and adjacency are outside this seat.

## 0. What this seat produced

The scratch candidate for the frozen v4 counter `plans/round49_c2_verify.py`: the digest-pinned import of
`plans/round46_c3_verify.py` (sha256 `a971c24d…`, verified at load) plus the four frozen deltas — V7 positive
tag/map preconditions, **V8 with the round-49 ordering rule replacing the round-48 inherited-receipt rule**,
V15 preconditions dry-run, V14 mutation battery — with the six stage-2 pin slots left as literal placeholders.

```
$ sha256sum .ufo/waves/round-49/w1/R49C2ExecCounter/candidate.py
9e9b47b027d82027f89ab149872b4807fda988c4b12dba88700294380d2b9c7b  candidate.py
$ wc -l candidate.py
740 candidate.py
```

**No scored counter or probe run was made.** No receipt under `receipts/` carries a `V2` leg line and none
carries a `P10 ok`/`P10 DEFECT` line (`grep -l '^V2 ' receipts/*.txt` → nothing; `grep -n 'P10 ok\|P10 DEFECT'` →
nothing). Only `--dry` and `--control` ran, both of which remove V2 — the only leg that executes the probe.

Diff against the round-48 Appendix A source: the import, the leg table, the mirror, V7, V14, V15's structure and
the driver are carried verbatim; the changes are (1) the four path repoints + the pin re-point at load, (2) the
predicate label `R49-C2`, (3) V8's ordering rule, (4) `plans/mutants49` mirrored for control trees, (5) a mirror
fix for files that live inside a copied directory. Nothing else in the file moved.

## 1. Freeze verified before measuring

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git rev-parse HEAD
af88aab193e6034cb9b386472064e3c18fa90128
$ git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD && echo "freeze is ancestor of HEAD"
freeze is ancestor of HEAD
$ git show --stat --oneline 9d2900af41e4d1fc6022eff99010436fde6dbd93 | head -3
9d2900a round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
 plans/round-49-claims.md | 167 +++++++++++++++++++++++++++++++++++++++++++++++
```

The freeze exists, it added `plans/round-49-claims.md`, and it precedes every measurement here: the frozen
clone measures `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` and the fixture clone's stage-1 ancestor is the
same commit. `plans/round46_c3_verify.py` (the imported contract), `plans/pkg_gate.py`, `plans/order_check.py`,
the probe and the round-46 package are byte-identical at the freeze. **The lane tree does not hold the stage-2
artefacts** — `plans/pkg-spec-r49.json`, `plans/mutants49/`, `corpus/evidence/round49/` and
`plans/round49_c2_verify.py` are all absent at HEAD — so a scored run is impossible by construction and, per the
claims' ordering clause, forbidden anyway.

## 2. The frozen contract, and where each clause went

From `plans/round-49-claims.md` §C2 and this seat's item:

| frozen clause | where it lives in `candidate.py` |
|---|---|
| `python3 plans/round49_c2_verify.py --lane .`; predicate `PREDICATE R49-C2 pass` | `main()`, exit 0 only on `checks=<V> defects=0`; `--dry`/`--control` print `dry`/`fail` and exit 1 |
| contract = `plans/round46_c3_verify.py` digest-pinned, imported | `load_base()` raises `SETUP`/exit 2 on any other sha256 |
| inputs repointed: `SPEC_REL`, `DRY_REL`, `CLAIMS_REL`, `MUT_PLAN_REL` | `SPEC_REL = "plans/pkg-spec-r49.json"`, `DRY_REL = "corpus/evidence/round49/polyglot-c-py-dry-cases.txt"`, `CLAIMS_REL = "plans/round-49-claims.md"`, `MUT_PLAN_REL = "plans/mutants49/plan.json"`; `load_base()` sets the imported module's `SPEC_REL/SPEC_SHA256/DRY_REL/DRY_SHA256/PROBE_REL/PROBE_SHA256/GATE_REL/GATE_SHA256/CLAIMS_REL` so every imported leg reads this round's inputs |
| (a) V7 fix — every frozen tag cited by a committed case, both-print/toolchain positively present, map rows parse | `v7()` — tag set from the dry table's `TAG` lines, violation sets from the receipt's `violates=` tokens, the two named tags re-checked by name, then the imported label/citation rule |
| (b) V8 fix — controls refuse with P10 disabled; **receipt first-commit == the stage-3 commit, a descendant of the stage-2 commit, receipt carries `CASE … observed=`** | `v8()` — gate run without `--rerun` (any `P10` line is a defect, exit must be 1), control receipts checked for the fail predicate/P10 absence/executed cases/`order_check`, then: `stage2 = first_commit(COUNTER_REL)`, `stage3 = first_commit(receipt)`, `stage2 != stage3`, `merge-base --is-ancestor stage2 stage3`, the spec blob at stage 3 pins the receipt blob at stage 3, the measured receipt equals that blob, and every `CASE` line of the receipt carries `observed=` |
| (c) V15 — every frozen input digest resolves and every frozen table parses before scoring | `preconditions()` — 11 pinned inputs + 7 table parses; a blocked leg prints `DEFECT precondition: …` and is never executed |
| (d) V14 — `<N>` mutants of committed package bytes, each must flip a substantive leg, floor `<N>/2` | `v14()` — plan/digest/target checks, one mutation at a time on a copied-directory/symlinked-file mirror, `MUTATION DEFECT` below the floor, baseline defects disclosed |
| (f) V13/V11 retained | imported unchanged |

The stage-3 rule is the round-48 defect's repair, so it is stated in the counter's own docstring: a stage-3
commit that lands the receipt without filling the spec's `receipt_sha256` is a DEFECT, and so is a receipt edited
after its landing commit (the pin and the ordering would then describe bytes nobody measured).

## 3. Stage-2 pin slots the L1 must fill (nothing else in the file is stage-2)

```python
SPEC_SHA256 = "<PIN:stage-2>"      # sha256 of plans/pkg-spec-r49.json with its receipt_sha256 value masked
PROBE_SHA256 = "<PIN:stage-2>"     # the amended probe revision's digest
DRY_SHA256 = "<PIN:stage-2>"       # corpus/evidence/round49/polyglot-c-py-dry-cases.txt
MUT_N = "<PIN:stage-2>"            # the frozen number of mutants (>= the claims' floor source)
MUT_FLOOR = "<PIN:stage-2>"        # the catch floor, claims freeze it at <N>/2
CONTROL_RECEIPTS = {name: "<PIN:stage-2>" for name in CONTROL_ORDER}
#   -> {"base": ".ufo/waves/round-49/claims/control-c2-base.txt",
#       "filler": ".ufo/waves/round-49/claims/control-c2-filler.txt",
#       "echo": ".ufo/waves/round-49/claims/control-c2-echo.txt"}
```

Mutation plan schema (`plans/mutants49/plan.json`, authored by wave-1 mutation-tester seats; V14 re-measures each
payload's sha256): `{"mutants": [{"name", "target", "payload", "sha256", "description"}]}`. Legal `target` values
are exactly `plans/pkg-spec-r49.json`, the spec's `entry`, the spec's `receipt`, the round-49 dry table,
`plans/polyglot_c_py_probe.py`, and the eight `corpus/evidence/round46/tb2-polyglot-c-py/*` captures; anything
else is `unmeasurable(target is not a frozen package byte)`.

## 4. Selftest (`--dry` and `--control` only, on scratch clones)

Fixture: a scratch clone of the lane at the freeze, with a *shape* stage-2/stage-3 history. The stage-2/stage-3
inputs are stand-ins derived from the round-46 package (dry table and receipt copied, entry/probe untouched) —
they exist to exercise the machinery, **not** as an amendment and not as admission evidence. The complete builder
is `receipts/build_fixture.sh` (scratch-only, rerunnable), and `receipts/fixture-history.txt` records its history:

```
$ git log --reverse --diff-filter=A --format='%H %s' -- plans/round49_c2_verify.py wave
d29e5f54ecb34ad56142d9cc30fa885260e82bf9 r49-c2 fixture: stage 2 (counter + pins + dry table + mutants + control receipts)
$ git log --reverse --diff-filter=A --format='%H %s' -- corpus/evidence/round49/polyglot-c-py-probe.txt wave
092e497d60b4c7870115efdff79a0616c45660af r49-c2 fixture: stage 3 (fresh receipt + its pin)
```

### 4.1 The delivered file, pins unfilled, on a clean clone of the freeze

```
$ python3 plans/round49_c2_verify.py --lane . --dry --work <scratch>/work-placeholder
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93 lane=<scratch>/lane
PACKAGE unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V15 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
…
checks=14 defects=13
PREDICATE R49-C2 fail
# exit=1
```

A placeholder pin refuses; it never passes, crashes or silently reads the round-46 spec. (`receipts/dry-placeholder.txt`.)

### 4.2 Happy ordering: stage 2 then stage 3 (pins filled in a scratch copy)

```
$ python3 plans/round49_c2_verify.py --lane . --dry --work <scratch>/work-wave
REV 092e497d60b4c7870115efdff79a0616c45660af lane=<scratch>/fixture
V15 ok inputs=11 tables=7 blocked=0
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0 registry=corpus/SOURCES.md
V7 DEFECT rows=7 tags=7 violated=5/7 bad=7 first=both-print:no committed case carries violates=both-print
V8 ok controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 stage2=d29e5f54ecb3 stage3=092e497d60b4 cases=18 observed=18 bad=0
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', …]
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', …]
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 ok mutants=5 caught=4 floor=2 baseline_defects=V7 receipt-observed-flip:caught(V4,V9) entry-case-row:caught(V9) spec-anchor-digest:caught(V3,V4,V9,V10,V12) package-unreadable capture-instruction:caught(V12) noop-receipt-comment:CLEAN
checks=14 defects=1
PREDICATE R49-C2 fail
# exit=1
```

The single defect is the **stage-1 V7 state** (the frozen tables violate 5 of 7 tags and the entry's two rows
are not in canonical shape) — the counter refuses the unamended tree, which is the claims' do-nothing control.
(`receipts/dry-wave.txt`.)

### 4.3 The ordering rule, clause by clause (one branch per broken clause)

```
$ for b in same-commit early-receipt no-pin echo-receipt edited-after v7-tags p10-receipt observed-receipt; do
    git checkout -q $b; python3 plans/round49_c2_verify.py --lane . --dry --work <scratch>/work-$b; done
```

| branch (HEAD) | V8 observed |
|---|---|
| `same-commit` 1f85de5 — receipt lands in the stage-2 commit | `V8 DEFECT … stage2=1f85de5dd5b8 stage3=1f85de5dd5b8 cases=18 observed=18 bad=1 the receipt's first commit is the stage-2 commit (stage 3 must be its own commit)` |
| `early-receipt` 2d243ea — receipt committed before the counter | `V8 DEFECT … stage2=2d243eaa8ed6 stage3=fdf073d3b40b … bad=1 receipt first-commit fdf073d3b40b is not a descendant of the stage-2 commit 2d243eaa8ed6` |
| `no-pin` 3a53bdc — stage 3 lands the receipt, pin left pending | `V8 DEFECT … stage2=d29e5f54ecb3 stage3=3a53bdc523bc … bad=1 the first commit adding the receipt does not carry its pin (receipt_sha256=PENDING-STAG blob=dd0e35464bc1)` |
| `echo-receipt` da017e4 — dry table copied over the receipt, pin coherent | `V8 DEFECT … cases=18 observed=0 bad=1 receipt CASE lines without observed=: 18/18` |
| `edited-after` e731327 — receipt edited after its stage-3 commit | `V8 DEFECT … cases=18 observed=18 bad=1 the receipt being measured is not the blob the stage-3 commit landed (a receipt edited after its landing commit)` |
| `v7-tags` a19f787 — both-print/toolchain each cited by a case | `V8 ok … bad=0` and `V7 DEFECT rows=7 tags=7 violated=7/7 bad=3 first=row not in canonical shape: '\| instruction.md:7 \| both-print \| not exercised \| …'` (tag citation now passes; the map-row/tags-missing rule still needs the stage-2 entry repair) |
| `p10-receipt` 3d75c76 — a committed control receipt carries a P10 line | `V8 DEFECT … bad=1 echo:receipt shows a P10 line (the control executed the gate's P10)` |
| `observed-receipt` e169bb4 — a committed control receipt carries a `CASE … observed=` line | `V8 DEFECT … bad=1 base:receipt shows an executed probe case` |

Receipts: `receipts/dry-same-commit.txt`, `dry-early-receipt.txt`, `dry-no-pin.txt`, `dry-echo-receipt.txt`,
`dry-edited-after.txt`, `dry-v7-tags.txt`, `dry-p10-receipt.txt`, `dry-observed-receipt.txt`.

### 4.4 V14 floor and V15 tamper paths

```
$ python3 fill.py <fixture> candidate.py plans/round49_c2_verify.py 5     # floor 5 > caught 4
MUTATION DEFECT
V14 DEFECT mutants=5 caught=4 floor=5 baseline_defects=V7 receipt-observed-flip:caught(V4,V9) entry-case-row:caught(V9) spec-anchor-digest:caught(V3,V4,V9,V10,V12) package-unreadable capture-instruction:caught(V12) noop-receipt-comment:CLEAN
checks=14 defects=2
PREDICATE R49-C2 fail

$ printf '# tampered\n' >> plans/polyglot_c_py_probe.py   # then --dry
V15 DEFECT inputs=11 tables=7 blocked=2
V5 DEFECT precondition: the probe pin is pending, or the probe is absent or not at its frozen digest
checks=14 defects=3
PREDICATE R49-C2 fail
```

A broken floor prints `MUTATION DEFECT` and fails; a tampered input is a named DEFECT of the legs that read it,
not a traceback. (`receipts/dry-floor5.txt`, `receipts/dry-tamper.txt`.)

### 4.5 The three frozen controls (`--control`, P10 removed from the run)

```
$ for c in base filler echo; do python3 plans/round49_c2_verify.py --lane . --control $c > …/control-c2-$c.txt; done
control=base   EXIT=1   PREDICATE R49-C2 fail   gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0
control=filler EXIT=1   PREDICATE R49-C2 fail   gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0
control=echo   EXIT=1   PREDICATE R49-C2 fail   gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0
```

Each control tree is refused by the package gate with `p10=0` (the gate is invoked without `--rerun`, so the
clause does not exist), and each control receipt prints the fail predicate. Control trees are mirrors, not git
work trees, so their own V8 line also reports `stage2=none stage3=none` and `order exit=2` — a control cannot
satisfy the package's stage-3 rule, which is exactly why a control can never be mistaken for an admission.
(`receipts/control-c2-{base,filler,echo}.txt`.)

## 5. Isolation

- Every run above executed inside `/fast/scratch/hyaku/kengaku-r49/R49C2ExecCounter/{lane,fixture}` with
  `TMPDIR` exported there; `git rev-parse --show-toplevel` was asserted equal to the clone before every write.
- After every counter run, including the mutation battery, `git -C fixture status --porcelain` was empty: the
  mirror copies directories and symlinks files, and `install_mutation()` refuses any target whose parent resolves
  outside the mirror (`receipts/fixture-history.txt` ends with the empty status).
- Two defects were found by these checks and fixed in the candidate: files living inside a *copied* directory
  (`corpus/knowledge/tb2-polyglot-c-py-grader.md`) collided with their own symlink (`FileExistsError`, first
  control run), and `plans/mutants49/` was not mirrored, so control trees reported the mutation plan absent.
- **Lane writes:** only the three artefact paths this seat owns —
  `.ufo/waves/round-49/w1/R49C2ExecCounter.md`, `.ufo/waves/round-49/w1/R49C2ExecCounter/candidate.py`, and
  `.ufo/waves/round-49/w1/R49C2ExecCounter/receipts/`. Nothing else in the lane was created, modified or deleted;
  no commit, push or mutating git/jj command touched the lane (all histories are in the scratch clones).
- Scratch `/fast/scratch/hyaku/kengaku-r49/R49C2ExecCounter` is removed before yield; every receipt cited here is
  copied into `receipts/`, so no `/tmp` or scratch path is citable evidence.

## 6. Sources

| source (opened this run, local unless a URL is given) | located quote (≤25 words) | use |
|---|---|---|
| `plans/round-49-claims.md` @ `9d2900af` (no URL) | `No full probe of the C2 package runs before the stage-3 commit lands the receipt; only --dry and --stage-check are run pre-receipt.` | binds this seat; forbids a scored run |
| `plans/round-49-claims.md` §C2 (b) @ `9d2900af` | `V8 verifies ordering from git log: the receipt's first-commit is the stage-3 commit, a descendant of the stage-2 commit` | the V8 rule implemented |
| `corpus/lessons/round-48-verifier-spotcheck.md` @ `9d2900af` (no URL) | `round48_c2_verify.py absent from the tip tree, as reported; no stage-2 freeze committed.` | the routed defect class this seat's report answers (report-artefact hygiene) |
| `plans/round46_c3_verify.py` @ `9d2900af` (no URL) | `Contract = plans/round46_c3_verify.py at its round-46 digest, imported` | imported contract; `load_base()` pins `a971c24d…` |
| `plans/pkg_gate.py` @ `9d2900af` (no URL) | `if (n != "P9" or args.require_clean_tree) and (n != "P10" or args.rerun)` | proves omitting `--rerun` removes P10 |
| `plans/order_check.py` @ `9d2900af` (no URL) | `FAIL when any file committed under .ufo/waves/round-NN/claims/ at or before the first commit that adds <receipt> proves the probe executed` | the ordering pin V8 calls for the control receipts |
| `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` + `…-probe.txt` @ `9d2900af` (no URL) | `TAG both-print instruction.md:7` … `TAG toolchain instruction.md:9` | the seven frozen tags; five violated, the two named ones not |

No external URL, remote capture or network source was opened by this seat; no credential, token or session
material was read.

## 7. Limits (named)

1. **Scored mode never ran** (`checks=15` = V15 + V1..V14 with V2). Every observation is `checks=14`. The claims
   reserve the first full probe run for stage 3.
2. **The fixture's stage-2/stage-3 inputs are stand-ins**, not the amendment: the dry table and receipt are the
   round-46 bytes copied to the round-49 paths, and the entry/probe are untouched. They exercise the machinery
   (V8's rule, V7's precondition, V14, V15) and say nothing about whether the real amendment is admissible. The
   fixture therefore also cannot reach `PREDICATE R49-C2 dry`: V7's stage-1 defect is real in it.
3. **V14 sensitivity is baseline-relative**; the fixture baseline has `baseline_defects=V7`, so mutants that
   would flip V7 read `CLEAN` there (`noop-receipt-comment:CLEAN` is a genuine non-flip; the V7-adjacent case is
   named by the leg, not hidden). V14 verifies payload digests, targets and the pinned count, never authorship.
4. **V8's stage-3 identification relies on the spec's `receipt_sha256`** (the round-46 package schema). If the L1
   pins the receipt somewhere else, the rule must be re-pointed at stage 2 — it is a declared part of the delta,
   not an inference the counter makes.
5. **V8 pins receipts, not provenance.** The live gate run proves a control is refused with P10 absent; the
   control-receipt checks prove the fail predicate, P10 absence, executed-case absence and ordering. A receipt
   produced by some other fail-printing command carrying no probe evidence is not distinguishable by bytes alone.
6. **`order_check` couples sibling claims** for the control receipts: a sibling receipt under
   `.ufo/waves/round-49/claims/` carrying a `P10` line or a `CASE … observed=` line fails V8 for a reason outside
   C2. The counter prints the offending `ORDER HIT` verbatim rather than hiding it.
7. Mirror cost ≈1.1 MB copied per control/mutation tree (four trees per scored run); no lane writes.

## 8. Handoff / risks

- **Landing order:** land `plans/round49_c2_verify.py` (this candidate) together with `plans/pkg-spec-r49.json`,
  the amended probe, `corpus/evidence/round49/polyglot-c-py-dry-cases.txt`, `plans/mutants49/` and the three
  control receipts at stage 2 → fill `SPEC_SHA256`, `PROBE_SHA256`, `DRY_SHA256`, `MUT_N`, `MUT_FLOOR`,
  `CONTROL_RECEIPTS` in the same commit → stage 3 lands the first full probe run's receipt **and** fills the
  spec's `receipt_sha256` in one commit → run the scored `checks=15` command on a clean clone of the landing tip.
- **V7 cannot pass until the stage-2 amendment** (a) adds committed cases violating `both-print` and `toolchain`
  (tag names must not change) and (b) rewrites the entry's two `| instruction.md:N | both-print | not exercised | …`
  rows into the canonical four-cell shape with a derived label and cited cases. The `v7-tags` variant shows the
  tag rule passing while the map-row rule still fails, so both repairs are needed and are measured separately.
- **The stage-3 commit must be its own commit and must carry the pin**; a receipt committed with the counter, or
  before it, or edited after landing, is refused by name.
- Candidate is delivered with six placeholder pins; transcribing it unchanged (as here) is safe — the placeholders
  refuse rather than guess.

## VERDICT

**VERDICT: R49-C2 v4 counter candidate BUILT and selftested — not an admission of R49-C2.** The 740-line
candidate implements the frozen contract's four deltas over the digest-pinned round-46 import with the required
repoints (`SPEC_REL`, `DRY_REL`, `CLAIMS_REL`, `MUT_PLAN_REL`) and the round-49 V8 ordering rule in place of the
round-48 inherited-receipt rule; on scratch clones it prints `V15 ok inputs=11 tables=7 blocked=0`, refuses the
unfilled-pin tree with `PACKAGE unreadable`, accepts a stage-2→stage-3 history (`stage2=d29e5f54ecb3
stage3=092e497d60b4 cases=18 observed=18 bad=0`) and refuses each broken clause by name (same-commit,
receipt-before-stage-2, pending pin, echo receipt, post-landing edit, P10-carrying control receipt,
executed-case control receipt), measures `mutants=5 caught=4 floor=2` and `MUTATION DEFECT` below the floor, and
records the stage-1 V7 defect rather than masking it. No scored counter or probe run was made; the stage-2 pins,
the real amendment and the stage-3 receipt remain the L1's (and the wave's) work.
