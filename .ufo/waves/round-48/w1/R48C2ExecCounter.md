# R48-C2 executor seat — v4 counter for the TB2 `polyglot-c-py` admission (round 48, wave 1)

seat: `R48C2ExecCounter` (executor, route `@m_mim`) · claim served: **R48-C2** (coverage) · milestone:
kengaku round 48 hyaku run 10, one v2 wave · write scope: this report only (the candidate lived in scratch, is
now removed, and is reproduced verbatim in Appendix A).

**Axes named: coverage.** Nothing else was measured or claimed; C1, novelty, depth, operability, freshness and
adjacency are outside this seat.

## 0. What this seat produced

A scratch candidate for the frozen v4 counter `plans/round48_c2_verify.py`: the digest-pinned import of
`plans/round46_c3_verify.py` plus exactly the four frozen deltas (V7 positive preconditions, V8 P10-disabled
pre-receipt controls with ordering pins, V15 preconditions dry-run, V14 mutation battery with a frozen floor),
with the stage-2 pin slots left as literal placeholders. Selftested on scratch clones of the stage-1 freeze.

Candidate: 652 lines, `sha256 7611883b7004c4b5fabb728ff3448a2d1eedf3b49151dbcde67d0f29dfead227`
(source in Appendix A; the L1 lands it at `plans/round48_c2_verify.py` unchanged, then fills the stage-2 pins).

**No scored counter/probe execution was made on claimed work.** The lane tree does not hold the counter
(`plans/round48_c2_verify.py` ABSENT at HEAD), the mutation plan (`plans/mutants48/plan.json` ABSENT) or any
`.ufo/waves/round-48/claims/control-c2-*.txt`: stage 2 has not happened. Per the claims' ordering clause ("No
probe of the C2 package runs before the stage-2 commit") the only runs made were `--dry` stage-checks and
`--control` receipts, both of which exclude V2 — the only leg that executes the probe.

## 1. Freeze verified before measuring

Frozen base given by the assignment: `a543d92083557dd9b33ee674e9b99b03411f80af`. It exists, the frozen claims
were added *by* it, and it is an ancestor of the lane tip this wave sits on:

```
$ git log --oneline -3                      # in /home/vgpnk/Projects/shokunin/kengaku-shokunin
bf783c1 round-48: w1 ready handoff marker
453ddfd round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)
a543d92 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims

$ git merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD && echo "freeze ancestor of lane HEAD $(git rev-parse --short HEAD)"
freeze ancestor of lane HEAD bf783c1

$ git log --reverse --diff-filter=A --format='%H %ci %s' -- plans/round-48-claims.md | head -1
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims

$ git diff --stat a543d92083557dd9b33ee674e9b99b03411f80af HEAD -- \
    plans/round-48-claims.md plans/pkg-spec-r46.json corpus/knowledge/tb2-polyglot-c-py-grader.md \
    corpus/evidence/round46 plans/polyglot_c_py_probe.py plans/pkg_gate.py plans/order_check.py \
    plans/round46_c3_verify.py
(empty: every C2 input is byte-identical to the freeze)
```

The freeze predates every measurement here (`REV a543d920…` on the frozen clone; the fixture clone measures
`REV f60339cd6c17…`, whose parent is the freeze). All work was read-only against clones under
`/fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter` (`lane`, `fixture`, `adv`); `git rev-parse --show-toplevel`
was asserted equal to each clone before any write, and the lane repo itself was never written (§6).

## 2. The frozen contract, and where each clause went

From `plans/round-48-claims.md` §C2 (verbatim fragments):

- "Counter `python3 plans/round48_c2_verify.py --lane .` (written in wave 1, pinned at stage 2) =
  `plans/round46_c3_verify.py` (digest-pinned, imported)" → `load_base()` refuses any other digest with
  `SETUP`/exit 2, so an edited import can never silently change what is certified.
- "(a) **V7 fix (Q24)** — … every frozen requirement tag is cited by at least one committed case `violates=`
  line; every requirement-map row parses to the census column count; violating cases exist for `both-print` and
  `toolchain`" → `v7()` takes the tag set from the frozen dry table's `TAG` lines, the violation sets from the
  committed receipt's `violates=` tokens, re-checks the two named tags by name, and requires every map row to
  parse to the header's column count *and* to the canonical shape (`| 'instruction.md:N' | 'tag' | label |
  cases |`) — the two round-46 rows that failed are exactly the rows an unanchored regex used to skip. The
  imported label rule (`enforced`/`unenforced`/`partly`, DERIVED from the receipt) and citation rule follow
  unchanged.
- "(b) **V8 fix (Q30/Q40)** — the base/filler/echo controls run the package gate with P10 (fresh probe re-run)
  disabled; `plans/order_check.py` pins each control's ordering receipt; the first full probe run follows the
  stage-2 commit" → `v8()` builds each frozen control tree as a mirror and invokes the gate **without
  `--rerun`**. `plans/pkg_gate.py:308` shows that this removes the clause rather than skipping it silently:
  `if (n != "P9" or args.require_clean_tree) and (n != "P10" or args.rerun)]`. Any `P10` line in a control's
  output is a defect; each control must be *refused* (exit 1), never accepted or error. Each pinned control
  receipt must print `PREDICATE R48-C2 fail`, carry no `P10` line and no `CASE … observed=` line, and pass
  `plans/order_check.py --claims plans/round-48-claims.md`. The inherited round-46 package receipt cannot be
  order-checked against a later round's claims (its bytes predate them); V8 asserts instead that the receipt was
  added at or before the round-48 freeze, which fires if any round-48 seat produced it early. The scored run's
  V2 keeps the imported `--rerun` leg, so the first full probe run *is* the post-stage-2 scored run.
- "(c) **V15 (new, preconditions dry-run)** — every frozen input digest resolves and every leg's frozen table
  parses before any leg scores; a missing/tamper-pinned input is a DEFECT of that leg, not a crash" →
  `preconditions()` resolves 11 pinned inputs (captures, gate, probe, dry table, receipt, entry, registry,
  README, PROVINCE, order_check, claims) and parses 6..7 tables; a blocked leg prints
  `DEFECT precondition: …` and is never executed.
- "(d) **V14 (new, mutation battery)** — `<N>` fresh mutants … each mutant must flip at least one substantive leg
  (V3/V4/V7/V9/V10/V12) to DEFECT; fewer than `<N>/2` caught → the counter prints `MUTATION DEFECT` and the
  predicate fails" → `v14()` checks the plan, each payload digest and each target against the frozen byte set,
  applies one mutation at a time to a **copied-directory, symlinked-file mirror** (never the lane), counts a
  mutant caught iff a leg that was ok at baseline flips, scores a mutant the frozen spec pin refuses outright as
  caught by every content leg (a leg that cannot run is a defect, never a pass), reports the baseline's own
  defects, and prints `MUTATION DEFECT` below the floor.
- "(e) V13 filler control retained; V11 held-out predictors retained with the round-46 refusal lint" → imported
  `base.v13`/`base.v11` unchanged, as are V1–V6, V9, V10, V12.

The scored leg count is `checks=15` (V15 + V1..V14). `--dry` and `--control` exclude V2 and print `checks=14`,
and their predicate line is `PREDICATE R48-C2 dry` or `fail` — **never `pass`** — and both exit 1, so a
stage-check can never be cited as an admission.

## 3. Stage-2 pin slots the L1 must fill (nothing else in the file is stage-2)

```python
MUT_N = "<PIN:stage-2>"       # -> "<N>"     the frozen number of mutants
MUT_FLOOR = "<PIN:stage-2>"   # -> "<floor>" catch floor; the claims freeze it at <N>/2
CONTROL_RECEIPTS = {name: "<PIN:stage-2>" for name in CONTROL_ORDER}
#   -> {"base": ".ufo/waves/round-48/claims/control-c2-base.txt",
#       "filler": ".ufo/waves/round-48/claims/control-c2-filler.txt",
#       "echo": ".ufo/waves/round-48/claims/control-c2-echo.txt"}
```

Mutation plan schema (`plans/mutants48/plan.json`, authored by wave-1 mutation-tester seats; V14 re-measures each
payload's sha256):

```json
{"mutants": [{"name": "<id>", "target": "<lane-relative frozen package byte>",
              "payload": "plans/mutants48/<file>", "sha256": "<payload sha256>"}]}
```

Legal `target` values are exactly the package's committed bytes: `plans/pkg-spec-r46.json`,
`corpus/knowledge/tb2-polyglot-c-py-grader.md`, `corpus/evidence/round46/polyglot-c-py-probe.txt`,
`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, `plans/polyglot_c_py_probe.py`, and the eight
`corpus/evidence/round46/tb2-polyglot-c-py/*` captures. Anything else is `unmeasurable(target is not a frozen
package byte)` — never a silent pass.

Each control receipt is produced by exactly one command, which cannot execute P10:

```
python3 plans/round48_c2_verify.py --lane . --control base   --work <scratch>
python3 plans/round48_c2_verify.py --lane . --control filler --work <scratch>
python3 plans/round48_c2_verify.py --lane . --control echo   --work <scratch>
```

## 4. Instrument pins verified

```
$ sha256sum plans/round46_c3_verify.py                     # the imported contract
a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4  plans/round46_c3_verify.py

$ python3   # the masked-digest check real_pkg() applies, run over the committed spec
  spec = pathlib.Path("plans/pkg-spec-r46.json").read_text()
  print(hashlib.sha256(re.sub(r'"receipt_sha256": "[^"]*"', '"receipt_sha256": "PENDING-STAGE-2"',
                              spec, count=1).encode()).hexdigest())
masked spec sha 560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e
```

Both equal the constants hard-coded in the imported counter, so `load_base()` accepts the contract and
`real_pkg()` accepts the frozen package.

## 5. Observations (verbatim)

### 5.1 `--dry` on a clean clone of the freeze (`REV a543d920…`) — the expected pre-stage-2 state

```
$ python3 plans/round48_c2_verify.py --lane . --dry --work <scratch>
REV a543d92083557dd9b33ee674e9b99b03411f80af lane=<scratch>/lane
V15 ok inputs=11 tables=6 blocked=0
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0 registry=corpus/SOURCES.md
V7 DEFECT rows=7 tags=7 violated=5/7 bad=7 first=both-print:no committed case carries violates=both-print
V8 DEFECT controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 inherited=receipt_first=8d7f74ce63c2 freeze=a543d9208355 bad=3 base:control receipt pending (stage-2 pin) | filler:control receipt pending (stage-2 pin) | echo:control receipt pending (stage-2 pin)
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 DEFECT mutation literals pending (stage-2 pins MUT_N and MUT_FLOOR)
checks=14 defects=3
PREDICATE R48-C2 fail
# exit=1
```

Three defects, each one a clause the claims say stage 2 exists to fill, and none a crash: `V7` (the
`both-print`/`toolchain` rows and their missing violating cases — the round-46 V7 class, now reported as
`violated=5/7` with the row-shape defect as the named first cause), `V8` (control receipts not yet pinned) and
`V14` (mutation literals not yet pinned). Everything else is green on the frozen tree, including
`V5 dry_byte_equal=True` (the probe's `--dry` output, not a probe run) and `V11 disagree=0` over 60 generated
states.

### 5.2 `--control base` — the freeze tree with `plans/polyglot_c_py_probe.py` removed

```
$ python3 plans/round48_c2_verify.py --lane . --control base
REV a543d92083557dd9b33ee674e9b99b03411f80af lane=<scratch>/fixture
CONTROL base tree=<scratch>/w-base/k48-c2-3j25vnkn/ctl-base p10=disabled
V15 DEFECT inputs=11 tables=6 blocked=2
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 DEFECT precondition: the probe is absent or not at its frozen digest
V6 ok census_exit=0 registry=<scratch>/w-base/k48-c2-3j25vnkn/ctl-base/corpus/SOURCES.md
V7 DEFECT rows=7 tags=7 violated=5/7 bad=7 first=both-print:no committed case carries violates=both-print
V8 DEFECT controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 inherited=receipt_first=8d7f74ce63c2 freeze=a543d9208355 bad=3 base:control receipt pending (stage-2 pin) | filler:control receipt pending (stage-2 pin) | echo:control receipt pending (stage-2 pin)
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 DEFECT mutation literals pending (stage-2 pins MUT_N and MUT_FLOOR)
checks=14 defects=5
PREDICATE R48-C2 fail
```

`--control echo` (the frozen dry table copied over the receipt): `V15 DEFECT blocked=4`, then

```
V7 DEFECT precondition: the receipt parses to zero CASE lines
V8 DEFECT controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 inherited=receipt_first=8d7f74ce63c2 freeze=a543d9208355 bad=3 base:control receipt pending (stage-2 pin) | filler:control receipt pending (stage-2 pin) | echo:control receipt pending (stage-2 pin)
checks=14 defects=7
PREDICATE R48-C2 fail
```

`--control filler` (the committed round-46 filler package scored as the package):

```
V5 DEFECT filler mode: no probe is pinned for the control package
V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
checks=14 defects=10
PREDICATE R48-C2 fail
```

In all three runs the V8 gate half measured the same three refusals with no P10 line (this is the field from
§5.5's pinned rerun; the control runs printed the same values while their receipt pins were still pending,
`bad=3 base:control receipt pending (stage-2 pin) | …`):

```
gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0
```

### 5.3 Ordering pins accepted, and the round-46 V8 class refused on sight

With the three control receipts committed in the fixture (a fixture commit inside scratch, guarded by
`rev-parse --show-toplevel`), each receipt passes `order_check` against the round-48 claims:

```
$ python3 plans/order_check.py --lane . --claims plans/round-48-claims.md --receipt .ufo/waves/round-48/claims/control-c2-base.txt
ORDER claims=plans/round-48-claims.md round=48 freeze=a543d92083557dd9b33ee674e9b99b03411f80af
ORDER receipt=.ufo/waves/round-48/claims/control-c2-base.txt receipt_commit=f60339cd6c17ad0a6e5dc5b1d16e9720fe96ceb4 claims_dir=.ufo/waves/round-48/claims/
ORDER scanned commits=1 file_entries=3 distinct_blobs=3
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
# exit=0
```

Then the round-46 V8 class was injected into copies of two committed receipts — a `gate: P10 DEFECT …` line into
`control-c2-echo.txt` (the exact `control-c3-echo` defect the round-46 spot-check found) and a `CASE … observed=`
line into `control-c2-base.txt`:

```
V8 DEFECT controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 inherited=receipt_first=8d7f74ce63c2 freeze=a543d9208355 bad=2 base:receipt shows an executed probe case | echo:receipt shows a P10 line (the control executed the gate's P10)
```

### 5.4 V14 mutation battery measured on the fixture (`MUT_N=7`, `MUT_FLOOR=3`)

Excerpt of §5.5, verbatim:

```
V8 ok controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 inherited=receipt_first=8d7f74ce63c2 freeze=a543d9208355 bad=0
V14 ok mutants=7 caught=4 floor=3 baseline_defects=V7 receipt-observed-flip:caught(V4,V9) spec-anchor-digest:caught(V3,V4,V9,V10,V12) package-unreadable dry-case-id:caught(V4,V10) dry-tag-line:CLEAN entry-requirement-label:CLEAN capture-instruction:caught(V12) outside-target:unmeasurable(target is not a frozen package byte)
```

All seven mutants are this seat's own synthetics, built only to exercise the machinery:
`receipt-observed-flip` → V4/V9; `spec-anchor-digest` → refused by the frozen spec pin, scored as caught by every
content leg (`package-unreadable`); `dry-case-id` → V4/V10; `capture-instruction` → V12; `outside-target` →
`unmeasurable` (not a package byte); `dry-tag-line` and `entry-requirement-label` read `CLEAN` **only because V7
is already DEFECT at the stage-1 baseline** (`baseline_defects=V7`) — the two mutants that become measurable once
the stage-2 case-table / requirement-map amendment makes V7 green. The leg reports the baseline instead of hiding
it, so a stage-2 run cannot confuse a broken baseline with low mutation sensitivity.

### 5.5 Full pinned fixture run (the scored command, minus V2)

```
REV f60339cd6c17ad0a6e5dc5b1d16e9720fe96ceb4 lane=<scratch>/fixture
V15 ok inputs=11 tables=7 blocked=0
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0 registry=corpus/SOURCES.md
V7 DEFECT rows=7 tags=7 violated=5/7 bad=7 first=both-print:no committed case carries violates=both-print
V8 ok controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 inherited=receipt_first=8d7f74ce63c2 freeze=a543d9208355 bad=0
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 ok mutants=7 caught=4 floor=3 baseline_defects=V7 receipt-observed-flip:caught(V4,V9) spec-anchor-digest:caught(V3,V4,V9,V10,V12) package-unreadable dry-case-id:caught(V4,V10) dry-tag-line:CLEAN entry-requirement-label:CLEAN capture-instruction:caught(V12) outside-target:unmeasurable(target is not a frozen package byte)
checks=14 defects=1
PREDICATE R48-C2 fail
# exit=1
```

`V15 ok inputs=11 tables=7 blocked=0`; the only defect is the stage-1 `V7` state, so the predicate correctly
fails — the counter refuses the frozen tree, which is what the claims' do-nothing control requires.

## 6. Lane untouched, scratch isolated

```
$ git status --porcelain | sort > status-before.txt     # inside the frozen clone
$ python3 plans/round48_c2_verify.py --lane . --control base --work <scratch>
$ git status --porcelain | sort > status-after.txt
$ diff status-before.txt status-after.txt && echo "LANE-WRITES: none"
LANE-WRITES: none
?? plans/round48_c2_verify.py        # the candidate copy itself, the only difference
```

Mutation isolation — after the battery ran, every frozen byte was still the freeze's:

```
$ git -C <scratch>/fixture diff --name-only a543d92083557dd9b33ee674e9b99b03411f80af HEAD -- \
    corpus/evidence plans/filler46 corpus/knowledge PROVINCE.md corpus/SOURCES.md
(empty)
$ git -C <scratch>/fixture diff --stat a543d920… HEAD
 .ufo/waves/round-48/claims/control-c2-base.txt   |  27 +
 .ufo/waves/round-48/claims/control-c2-echo.txt   |  27 +
 .ufo/waves/round-48/claims/control-c2-filler.txt |  27 +
 plans/mutants48/*.payload, plans/mutants48/plan.json | new
 plans/round48_c2_verify.py                       | 652 +++++++++++++++++++++++
```

The first draft of the mirror symlinked capture *directories*, so a mutant could write through the directory
symlink into the measured tree; this check caught it, and the mirror now copies directories
(`corpus/knowledge`, the capture dir, `plans/filler46` ≈ 1.1 MB) while symlinking individual files, with
`install_mutation()` refusing any target whose parent resolves outside the mirror.

## 7. Sources

| source | opened | located quote (≤25 words) | use |
|---|---|---|---|
| `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` (S166) | 2026-10-27T11:42:07Z, HTTP 200 | `:17 polyglot_files = os.listdir("/app/polyglot")` (4 words) | confirms the frozen capture is the pinned grader: fetched bytes are `sha256 b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` = `CAPTURES["test_outputs.py"]`; `:27 test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` is the three-fixed-point surface |
| `plans/round-48-claims.md` @ `a543d92` | this run (local, no URL) | `Ordering (Q30). No probe of the C2 package runs before the stage-2 commit.` | binds this seat; no scored run made |
| `corpus/lessons/round-46-verifier-spotcheck.md` @ `a543d92` | this run (local, no URL) | `C3: freeze violating receipt cases for every requirement tag, make pre-receipt controls unable to run P10, and improve mutation sensitivity (0/13 mutants killed).` | the routed defect the V7/V8/V14 deltas answer |
| `plans/round46_c3_verify.py` @ `a543d92` | this run (local, no URL) | `V8  order (QUALITY Q30): plans/order_check.py … exits 0 and prints ORDER RESULT PASS.` | the imported contract, digest-pinned |
| `plans/pkg_gate.py` @ `a543d92` | this run (local, no URL) | `:308 if (n != "P9" or args.require_clean_tree) and (n != "P10" or args.rerun)]` | proves omitting `--rerun` removes P10 rather than skipping it silently |
| `plans/order_check.py` @ `a543d92` | this run (local, no URL) | `FAIL  when any file committed under .ufo/waves/round-NN/claims/ at or before the first commit that adds <receipt> proves the probe executed` | the ordering pin V8 calls |
| `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, `…-probe.txt` @ `a543d92` | this run (local, no URL) | `TAG both-print instruction.md:7` … `TAG toolchain instruction.md:9` | the seven frozen tags; five are violated by the committed receipt, the two named ones are not (V7's defect at the freeze) |
| `corpus/knowledge/tb2-polyglot-c-py-grader.md` @ `a543d92` | this run (local, no URL) | `| instruction.md:7 | both-print | not exercised | no frozen case violates it |` | the two unparsable map rows V7's row-shape rule now catches |

No other external source was opened; no credential, token or session material was read.

## 8. Limits (named)

1. **Scored mode was never executed.** `checks=15` (V2 → gate `--rerun` → the probe) is reserved for the
   post-stage-2 run; every observation here is `checks=14`. The claims forbid anything else.
2. **V14 sensitivity is baseline-relative and the baseline is stage-1-broken.** Two synthetic mutants read
   `CLEAN` because V7 is already DEFECT before the stage-2 amendment; `baseline_defects=` makes this visible.
   The real `<N>` mutants must come from wave-1 mutation-tester seats; V14 verifies payload digests, targets and
   the pinned count, never authorship.
3. **V8 pins receipts, not provenance.** The live gate run proves refusal with P10 absent; the receipt checks
   prove the fail predicate, P10-absence, CASE-line absence and ordering. A receipt produced by some other
   fail-printing command carrying no probe evidence is not distinguishable by bytes alone.
4. **`order_check` couples sibling claims.** It scans every blob ever committed under
   `.ufo/waves/round-48/claims/` up to the control receipt's commit; a sibling receipt carrying a `P10` line or a
   `CASE … observed=` line fails V8 for a reason outside C2. The counter prints the offending `ORDER HIT`
   verbatim rather than hiding it.
5. **"census column count"** is implemented as the requirement-map header's own cell count (a header naming
   `Instruction line` and `Tag` is required; an absent header is a DEFECT). Recorded so the rule cannot be
   loosened later.
6. **The tag set is frozen by the dry table's `TAG` lines**; V7 re-checks `both-print` and `toolchain` by name,
   so a stage-2 edit of the tag list cannot drop them, and the claims forbid re-wording tags at stage 2.
7. Mirror cost: ≈1.1 MB copied per control/mutation tree (four trees per scored run); no lane writes.
8. `V6` runs `scripts/sources-census.sh` on the measured tree; under `--control` its note prints the mirror path,
   which is expected, not a leak.

## 9. Risks / handoff

- **Blocker for admission (C2, not this seat):** V7 cannot pass until the stage-2 amendment adds or re-words
  committed cases so that `both-print` and `toolchain` are each violated, and rewrites the two
  `| … | both-print | not exercised | … |` rows into the canonical `| 'instruction.md:N' | 'tag' | label |
  cases |` shape. Tag lines must not change.
- **Stage-2 commit shape matters:** the three `control-c2-*.txt` receipts must be committed after the claims
  freeze and must not share a commit with a receipt that shows P10 execution or a probe `CASE … observed=` line,
  or V8 (through `order_check`) fails.
- **Landing order:** land `plans/round48_c2_verify.py` (Appendix A verbatim) → commit the three control receipts
  produced by `--control` → commit `plans/mutants48/` (plan + payloads) → fill `MUT_N`, `MUT_FLOOR` and
  `CONTROL_RECEIPTS` in one amendment → run the scored `checks=15` command on a clean clone of the tip.
- Scratch `/fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter` is removed at the end of this seat; the candidate
  survives only as Appendix A plus the hash above.

## VERDICT

**VERDICT: R48-C2 v4 counter candidate BUILT and selftested — not an admission of R48-C2.** The scratch
candidate (`sha256 7611883b7004c4b5fabb728ff3448a2d1eedf3b49151dbcde67d0f29dfead227`, 652 lines) implements the
frozen contract's four deltas over the digest-pinned round-46 import; on scratch clones of the freeze it reports
`V15 ok inputs=11 tables=6 blocked=0`, refuses all three frozen controls through the gate with `p10=0` and
`exit=1`, accepts all three ordering receipts (`ORDER RESULT PASS`), catches a P10-carrying and an
observed-case-carrying receipt by name, and measures the mutation battery (`caught=4 floor=3`, baseline defect
disclosed). No scored counter or probe run was made: the freeze `a543d92` is committed, predates every
measurement, and lacks the stage-2 artefacts, so the scored `checks=15` run remains blocked on the stage-2 pin
commit exactly as the claims require.

---

## Appendix A — candidate source (verbatim, `plans/round48_c2_verify.py`)

```python
#!/usr/bin/env python3
"""Round-48 C2 counter (v4): the round-46 TB2 `polyglot-c-py` package admitted under a Q40 re-frozen counter.

The graded surface is unchanged from round 46 (plans/round-46-claims.md §C3): one file
`/app/polyglot/main.py.c` executed by two toolchains, three fixed points, an exact-directory precondition,
graded by `tests/test_outputs.py` at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. This round
claims its **admission**, not a new class (plans/round-48-claims.md §C2).

Frozen predicate (same sentence in plans/round-48-claims.md §C2 and in this receipt label):
  C2 passes iff `python3 plans/round48_c2_verify.py --lane .` prints `checks=<V> defects=0`, then
  `PREDICATE R48-C2 pass`, exit 0, on a clean clone of the landing tip.

Contract = `plans/round46_c3_verify.py` at its round-46 digest, imported (never copied, so a change to the
imported file is a setup error, not a silent change of what this counter certifies), plus four frozen deltas:

  V7 (Q24 fix, replaces the imported V7). Before any label is derived, this leg positively verifies, from the
     frozen tables alone: (i) every frozen tag (the `TAG` lines of the frozen dry table) is cited by at least one
     committed receipt case `violates=` token; (ii) the two tags the round-46 failure named — `both-print` and
     `toolchain` — are in the frozen set and each is so cited; (iii) every `## Requirement map` row parses to
     the header's column count and to the canonical table shape (`| 'instruction.md:N' | 'tag' | label | cases |`).
     Rows that fail (iii) are defects even when the derived-label rule would have ignored them — round 46's
     `both-print`/`toolchain` rows were skipped by an unanchored regex and reported only as "missing".
     The imported label rule (enforced/unenforced/partly, DERIVED from the receipt) and the citation rule are
     then applied unchanged.

  V8 (Q30/Q40 fix, replaces the imported V8). Three frozen controls — `base` (the tree with
     `plans/polyglot_c_py_probe.py` removed), `filler` (the committed round-46 filler package) and `echo` (the
     frozen dry table copied over the receipt) — are run through the package gate **with `--rerun` omitted**, so
     the gate's `P10` (fresh probe re-run) clause does not exist in the run: any `P10` line at all in a control's
     output is a defect. Each control must be *refused* by the gate (exit 1), never accepted, and never error.
     The control receipts committed under `.ufo/waves/round-48/claims/` (paths frozen at stage 2) must print
     `PREDICATE R48-C2 fail`, must carry no `P10` line and no executed-probe `CASE … observed=` line, and each
     must pass `plans/order_check.py` against the round-48 claims (the ordering receipt that pins it).
     The package's own receipt is inherited round-46 evidence, so it is not order-checked against the round-48
     freeze (its bytes predate it by construction): V8 requires instead that the receipt was added at or before
     the round-48 freeze commit, which fails if any round-48 seat produced a receipt before stage 2.

  V15 (new, preconditions dry-run). Before any leg scores, every frozen input digest is resolved and every
     leg's frozen table is parsed. A missing or tamper-pinned input is a DEFECT *of the legs that read it*:
     those legs are not executed and print the precondition reason, so a missing file is a named defect and
     never a traceback. V15 itself is ok only when nothing is blocked.

  V14 (new, mutation battery). `<N>` fresh mutants of committed package bytes (capture, entry, receipt, dry
     table, spec, probe) declared in `plans/mutants48/plan.json` (payload path + digest + target per mutant,
     authored by wave-1 mutation-tester seats). Each payload's digest is re-measured, each target must be one of
     the frozen package bytes, and the mutant is applied to a symlink mirror of the lane, never to the lane. A
     mutant is *caught* iff at least one substantive leg (V3/V4/V7/V9/V10/V12) that was ok on the unmutated
     mirror becomes DEFECT on the mutant; a mutant the frozen spec pin refuses outright (the package no longer
     loads) is caught by every content leg, since a leg that cannot run is a defect and never a pass. The leg
     reports the legs that were already DEFECT at baseline, because a broken baseline cannot measure anything.
     Fewer than the frozen floor caught prints `MUTATION DEFECT` and the leg fails.

Ordering (QUALITY Q30, plans/round-48-claims.md §C2): no probe of this package runs before the stage-2 commit.
`--dry` is the stage-check: it scores every leg except V2 (the only leg that runs the probe, via the gate's P10),
prints `PREDICATE R48-C2 dry` — never `pass` — and exits 1. `--control {base,filler,echo}` builds that control's
mirror, measures the same legs with V2 excluded, and prints a fail receipt: it is the command that produces a
stage-2 control receipt, and it cannot execute P10.

Exit: 0 pass · 1 fail (also dry/control) · 2 setup error.

Named limits.
  * V14 measures the mutants it is given: payload digests, targets and the pinned count are checked, but the
    claim that a human/seat authored them against the committed bytes is not machine-checkable here.
  * V8's live gate run proves a control is refused with P10 absent; it does not prove the committed control
    receipt was produced by that exact command. The receipt is checked for the fail predicate, for P10 absence
    and for ordering, so a receipt from a P10-carrying run cannot pass.
  * V7's row-shape rule needs a header row naming `Instruction line` and `Tag`; a map with no header is a
    defect, and a row carrying `instruction.md:` that does not match the canonical shape is a defect.
  * The imported V11 predictor rules and their named limit stand unchanged (a small hand-coded verdict table
    is not distinguishable from a reader by sample equivalence alone; non-author review stays part of admission).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

# ---- frozen literals ---------------------------------------------------------------------------
BASE_REL = "plans/round46_c3_verify.py"
BASE_SHA256 = "a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4"  # round-46 bytes, unedited

SPEC_REL = "plans/pkg-spec-r46.json"
PROBE_REL = "plans/polyglot_c_py_probe.py"
DRY_REL = "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
GATE_REL = "plans/pkg_gate.py"
ORDER_REL = "plans/order_check.py"
CLAIMS_REL = "plans/round-48-claims.md"

MUT_PLAN_REL = "plans/mutants48/plan.json"
MUT_N = "<PIN:stage-2>"      # stage-2 literal: the number of frozen mutants
MUT_FLOOR = "<PIN:stage-2>"  # stage-2 literal: the catch floor (claims freeze it at >= N/2)

CONTROL_ORDER = ("base", "filler", "echo")
CONTROL_RECEIPTS = {name: "<PIN:stage-2>" for name in CONTROL_ORDER}  # stage-2 pins, lane-relative

NAMED_TAGS = ("both-print", "toolchain")  # the two tags the round-46 V7 failure named
SUBSTANTIVE = ("V3", "V4", "V7", "V9", "V10", "V12")

# What the legs and the gate read: a control/mutation mirror costs a few symlinks, never a copy of the lane.
MIRROR_DIRS = ("corpus/knowledge", "corpus/evidence/round46/tb2-polyglot-c-py", "plans/filler46")
MIRROR_FILES = ("corpus/SOURCES.md", "corpus/README.md", "PROVINCE.md", SPEC_REL, GATE_REL, PROBE_REL,
                ORDER_REL, BASE_REL, CLAIMS_REL, DRY_REL,
                "corpus/evidence/round46/polyglot-c-py-probe.txt")

GATE_P10 = re.compile(r"^\s*(?:gate:\s*)?P10\b")
CASE_OBSERVED = re.compile(r"^\s*CASE\s+\S+.*\bobserved=")
SEPARATOR = re.compile(r":?-{2,}:?")


class SetupError(Exception):
    """An instrument that is not the frozen instrument: exit 2, never a silent pass."""


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load_base(lane):
    """Import the round-46 counter from the lane at its frozen digest."""
    path = pathlib.Path(lane) / BASE_REL
    got = sha256(path)
    if got != BASE_SHA256:
        raise SetupError(f"{BASE_REL} is not at its round-46 digest: got {got} want {BASE_SHA256}")
    spec = importlib.util.spec_from_file_location("round46_c3_verify_r48c2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- the requirement map's own shape rule (V7 delta) -------------------------------------------

def map_rows(text):
    """(header column count, data rows) for `## Requirement map`; (None, []) when the section or header is absent."""
    m = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return None, []
    header, rows = None, []
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and all(SEPARATOR.fullmatch(c) for c in cells):
            continue
        if header is None and any("Instruction line" in c for c in cells) and any(c == "Tag" for c in cells):
            header = len(cells)
            continue
        rows.append((cells, line))
    return header, rows


def v7(base, pkg):
    """Positive preconditions over the frozen tables, then the imported label/citation rule."""
    try:
        tags, _ids = base.dry_table(pkg)
    except (OSError, ValueError) as e:
        return False, f"dry table unusable: {e}"
    receipt = base.text_or_none(pkg.receipt)
    entry = base.text_or_none(pkg.entry)
    if receipt is None or entry is None:
        return False, "receipt or entry absent"
    parsed = base.receipt_cases(receipt)
    bad = []
    violated = {t: sorted(cid for cid, (_o, v) in parsed.items() if t in v) for t in tags}
    # (i) every frozen tag is cited by at least one committed case `violates=` token
    for t in sorted(tags):
        if not violated[t]:
            bad.append(f"{t}:no committed case carries violates={t}")
    # (ii) the two tags the round-46 failure named
    for t in NAMED_TAGS:
        if t not in tags:
            bad.append(f"{t}:not a frozen tag")
        elif not violated[t]:
            bad.append(f"{t}:unexercised-by-any-case")
    # (iii) every row parses to the header's column count and to the canonical shape
    header, rows = map_rows(entry)
    if header is None:
        return False, "no parsable '## Requirement map' header (needs 'Instruction line' and 'Tag' columns)"
    seen = {}
    for cells, line in rows:
        if len(cells) != header:
            bad.append(f"row parses to {len(cells)} cells not {header}: {line.strip()[:40]!r}")
        m = base.MAP_ROW.match(line)
        if not m:
            if "instruction.md:" in line:
                bad.append(f"row not in canonical shape: {line.strip()[:50]!r}")
            continue
        ln, tag, label, rest = m.groups()
        seen[tag] = seen.get(tag, 0) + 1
        if tag not in tags:
            bad.append(f"{tag}:not a frozen tag")
            continue
        if tags[tag] != f"instruction.md:{ln}":
            bad.append(f"{tag}:line {ln} is not the frozen {tags[tag]}")
        if not violated[tag]:
            bad.append(f"{tag}:no receipt case violates it")
            continue
        want = base.derive({parsed[c][0] for c in violated[tag]})
        if label != want:
            bad.append(f"{tag}:labelled {label}, receipt derives {want}")
        cited = re.findall(r"`([a-z0-9_-]+)`", rest)
        if not cited or any(c not in violated[tag] for c in cited):
            bad.append(f"{tag}:cites no case or a case that does not violate it")
    missing = sorted(set(tags) - set(seen))
    dup = sorted(t for t, n in seen.items() if n > 1)
    if missing:
        bad.append(f"tags missing={missing}")
    if dup:
        bad.append(f"tags duplicated={dup}")
    note = (f"rows={len(rows)} tags={len(tags)} violated={sum(1 for t in tags if violated[t])}/{len(tags)}"
            f" bad={len(bad)}")
    return not bad, note + (f" first={bad[0]}" if bad else "")


# ---- mirrors: what the legs read, symlinked; the lane is never written --------------------------

def mirror(lane, dest):
    """A read-through mirror: directories are copied (a mutant must never write through a dir symlink into the
    lane), individual files are symlinked and replaced by a real file only when a mutant installs one."""
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for rel in MIRROR_DIRS:
        src = pathlib.Path(lane) / rel
        if src.is_dir():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dest / rel, dirs_exist_ok=True)
    for rel in MIRROR_FILES:
        src = pathlib.Path(lane) / rel
        if src.is_file():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            os.symlink(src, dest / rel)
    return dest


def unlink_any(p):
    if p.is_symlink() or p.exists():
        p.unlink()


def control_tree(lane, work, name, pkg_spec_rel=SPEC_REL):
    """The frozen control tree for `name`, built as a symlink mirror of `lane`."""
    tree = mirror(lane, pathlib.Path(work) / f"ctl-{name}")
    if name == "base":
        unlink_any(tree / PROBE_REL)  # the base tree: no plans/polyglot_c_py_probe.py
    elif name == "echo":
        spec = json.loads((tree / pkg_spec_rel).read_text())
        receipt = tree / spec["receipt"]
        data = (tree / DRY_REL).read_bytes()
        unlink_any(receipt)
        receipt.write_bytes(data)  # the frozen dry table copied over the receipt
    return tree


def gate_control(base, tree, name):
    """Run the package gate on a control tree with `--rerun` omitted: the P10 leg does not exist."""
    spec = (tree / base.FILLER_SPEC) if name == "filler" else (tree / SPEC_REL)
    argv = [sys.executable, str(tree / GATE_REL), "package", "--root", str(tree), "--spec", str(spec)]
    r = subprocess.run(argv, capture_output=True, text=True, timeout=1800)
    p10 = [l for l in r.stdout.splitlines() if GATE_P10.match(l)]
    return r, p10


def order(root, receipt_rel):
    r = subprocess.run([sys.executable, str(pathlib.Path(root) / ORDER_REL), "--lane", str(root),
                        "--claims", CLAIMS_REL, "--receipt", receipt_rel],
                       capture_output=True, text=True, timeout=300)
    return r, r.returncode == 0 and "ORDER RESULT PASS" in r.stdout.splitlines()


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def first_commit(root, rel):
    """The oldest commit that adds `rel`; '' when never added."""
    rc, out = git(root, "log", "--reverse", "--diff-filter=A", "--format=%H", "--", rel)
    lines = out.split() if rc == 0 else []
    return lines[0] if lines else ""


def inherited(root, receipt_rel):
    """True iff the receipt was added at or before the round-48 freeze commit (it is inherited evidence)."""
    receipt = first_commit(root, receipt_rel)
    freeze = first_commit(root, CLAIMS_REL)
    if not receipt or not freeze:
        return False, f"receipt_first={receipt or 'none'} freeze={freeze or 'none'}"
    rc, _ = git(root, "merge-base", "--is-ancestor", receipt, freeze)
    return rc == 0, f"receipt_first={receipt[:12]} freeze={freeze[:12]}"


def v8(base, root, work):
    """Pre-receipt controls with P10 disabled, plus the ordering receipt that pins each control."""
    root = pathlib.Path(root)
    bad, note_inherited = [], "?"
    try:
        receipt_rel = json.loads((root / SPEC_REL).read_text())["receipt"]
    except (OSError, KeyError, json.JSONDecodeError) as e:
        return False, f"spec unreadable: {e}"
    # The package receipt is inherited round-46 evidence: it must have been added at or before this round's
    # freeze. It is not order-checked against the round-48 claims (its bytes predate them by construction);
    # what this round owns is that no round-48 probe runs before stage 2, which the three controls carry.
    inh, note_inherited = inherited(root, receipt_rel)
    if not inh:
        bad.append(f"package receipt was added after the round-48 freeze ({note_inherited})")
    gates = []
    for name in CONTROL_ORDER:  # the gate half: P10-omitted runs, measured on every invocation
        tree = control_tree(root, work, name)
        r3, p10 = gate_control(base, tree, name)
        gates.append(f"{name}:exit={r3.returncode},p10={len(p10)}")
        if p10:
            bad.append(f"{name}:gate printed a P10 line with --rerun omitted")
        if r3.returncode != 1:
            bad.append(f"{name}:gate exit={r3.returncode} (a control must be refused, not accepted or error)")
    for name in CONTROL_ORDER:  # the ordering half: the committed receipt each control pins
        rel = CONTROL_RECEIPTS[name]
        if not base.ready(rel):
            bad.append(f"{name}:control receipt pending (stage-2 pin)")
            continue
        text = base.text_or_none(root / rel)
        if text is None:
            bad.append(f"{name}:control receipt absent: {rel}")
            continue
        if "PREDICATE R48-C2 fail" not in text:
            bad.append(f"{name}:receipt does not print the fail predicate")
        if any(GATE_P10.match(l) for l in text.splitlines()):
            bad.append(f"{name}:receipt shows a P10 line (the control executed the gate's P10)")
        if any(CASE_OBSERVED.match(l) for l in text.splitlines()):
            bad.append(f"{name}:receipt shows an executed probe case")
        r2, ok2 = order(root, rel)
        if not ok2:
            hits = [l.strip() for l in r2.stdout.splitlines() if l.startswith("ORDER HIT")]
            bad.append(f"{name}:order exit={r2.returncode} {hits[0][:80] if hits else ''}".strip())
    note = (f"controls={len(CONTROL_ORDER)} gates={' '.join(gates)} inherited={note_inherited}"
            f" bad={len(bad)}")
    return not bad, note + (" " + " | ".join(bad[:3]) if bad else "")


# ---- V14: mutation battery over the committed package bytes ------------------------------------

def load_plan(root):
    try:
        plan = json.loads((pathlib.Path(root) / MUT_PLAN_REL).read_text())
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(plan, dict) or not isinstance(plan.get("mutants"), list):
        return None
    return plan


def mutable_bytes(root, base):
    """The set of lane-relative paths a mutant may target: the package's own committed bytes."""
    try:
        spec = json.loads((pathlib.Path(root) / SPEC_REL).read_text())
        capdir = spec["capture_dir"]
        return {SPEC_REL, spec["entry"], spec["receipt"], base.DRY_REL, PROBE_REL} \
            | {f"{capdir}/{name}" for name in base.CAPTURES}
    except (OSError, KeyError, json.JSONDecodeError):
        return set()


def substantive(base, pkg):
    """The substantive content legs, one bool each; a leg that raises is a defect, never a pass."""
    table = {
        "V3": lambda: base.v3(pkg),
        "V4": lambda: base.v4(pkg),
        "V7": lambda: v7(base, pkg),
        "V9": lambda: base.v9(pkg),
        "V10": lambda: base.v10(pkg),
        "V12": lambda: base.v12(pkg),
    }
    out = {}
    for name in SUBSTANTIVE:
        try:
            ok, _note = table[name]()
        except Exception:  # a leg that cannot run cannot certify the mutant
            ok = False
        out[name] = ok
    return out


def install_mutation(tree, rel, data):
    p = pathlib.Path(tree) / rel
    parts = pathlib.PurePosixPath(rel)
    if parts.is_absolute() or ".." in parts.parts:
        raise ValueError(f"mutation target escapes the mirror: {rel}")
    parent = p.parent.resolve()
    root = pathlib.Path(tree).resolve()
    if parent != root and root not in parent.parents:
        raise ValueError(f"mutation target's directory escapes the mirror: {rel} -> {parent}")
    unlink_any(p)  # a symlink would otherwise write through into the lane
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def restore_mutation(tree, root, rel):
    p = pathlib.Path(tree) / rel
    unlink_any(p)
    os.symlink(pathlib.Path(root) / rel, p)


def v14(base, root, work):
    if not (base.ready(MUT_N) and base.ready(MUT_FLOOR)):
        return False, "mutation literals pending (stage-2 pins MUT_N and MUT_FLOOR)"
    try:
        n, floor = int(MUT_N), int(MUT_FLOOR)
    except ValueError:
        return False, f"mutation literals are not integers: N={MUT_N!r} floor={MUT_FLOOR!r}"
    plan = load_plan(root)
    if plan is None:
        return False, f"mutation plan absent or unparsable: {MUT_PLAN_REL}"
    muts = plan["mutants"]
    if len(muts) != n:
        return False, f"plan mutants={len(muts)} but the frozen N={n}"
    mutable = mutable_bytes(root, base)
    if not mutable:
        return False, "spec unreadable: the mutable-byte set is empty"
    tree = mirror(root, pathlib.Path(work) / "mut")
    try:
        base_map = substantive(base, base.real_pkg(tree))
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
        return False, f"mutation mirror unusable: {e}"
    caught, notes = [], []
    for m in muts:
        name = str(m.get("name", "?"))
        target = str(m.get("target", ""))
        payload_rel = str(m.get("payload", ""))
        why = []
        if target not in mutable:
            why.append("target is not a frozen package byte")
        try:
            payload = (pathlib.Path(root) / payload_rel).read_bytes()
        except OSError:
            payload = None
            why.append("payload unreadable")
        if payload is not None and sha256_of_payload(payload) != str(m.get("sha256", "")):
            why.append("payload digest differs from the plan")
        if why:
            notes.append(f"{name}:unmeasurable({';'.join(why)})")
            continue
        unreadable = False
        try:
            install_mutation(tree, target, payload)
            try:
                pkg_m = base.real_pkg(tree)
            except (ValueError, OSError, KeyError, json.JSONDecodeError):
                # a frozen spec pin refuses the mutant: every content leg reads the package and cannot run,
                # which the imported counter scores as a defect, never a pass
                got, unreadable = {leg: False for leg in SUBSTANTIVE}, True
            else:
                got = substantive(base, pkg_m)
        except Exception as e:  # a mutant the counter cannot even install proves nothing about sensitivity
            notes.append(f"{name}:unmeasurable(install {type(e).__name__}: {e})")
            continue
        finally:
            restore_mutation(tree, root, target)
        flipped = [leg for leg in SUBSTANTIVE if base_map[leg] and not got[leg]]
        if flipped:
            caught.append(name)
            notes.append(f"{name}:caught({','.join(flipped)})" + (" package-unreadable" if unreadable else ""))
        else:
            notes.append(f"{name}:CLEAN")
    ok = len(caught) >= floor
    if not ok:
        print("MUTATION DEFECT")
    baseline_bad = sorted(leg for leg, good in base_map.items() if not good)
    note = (f"mutants={len(muts)} caught={len(caught)} floor={floor}"
            f" baseline_defects={','.join(baseline_bad) or 0} " + " ".join(notes))
    return ok, note


def sha256_of_payload(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---- V15: preconditions dry-run ----------------------------------------------------------------

def preconditions(base, tree, pkg):
    """Resolve every frozen input and parse every leg's frozen table before any leg scores."""
    root = pathlib.Path(tree)  # the tree being measured (the lane, or a control mirror of it)
    blocked = {}
    counts = {"inputs": 0, "tables": 0}

    def need(legs, ok, what):
        counts["inputs"] += 1
        if not ok:
            for leg in legs:
                blocked.setdefault(leg, what)

    def parse(legs, fn, what):
        counts["tables"] += 1
        try:
            ok = bool(fn())
        except Exception:
            ok = False
        if not ok:
            for leg in legs:
                blocked.setdefault(leg, what)

    # Real-package pins exist only for the pinned package; a control package has no probe or capture pin.
    if pkg.pinned:
        need(("V1", "V10", "V12"), all(sha256(pathlib.Path(pkg.capdir) / n) == d for n, d in base.CAPTURES.items()),
             "a capture does not resolve to its frozen digest")
        need(("V2", "V5"), sha256(root / PROBE_REL) == base.PROBE_SHA256,
             "the probe is absent or not at its frozen digest")
        need(("V4", "V5", "V7", "V10"), sha256(pkg.dry) == base.DRY_SHA256,
             "the dry table is absent or not at its frozen digest")
    need(("V2", "V8"), sha256(root / GATE_REL) == base.GATE_SHA256, "the gate is not at its frozen digest")
    receipt = base.text_or_none(pkg.receipt)
    need(("V4", "V7", "V9", "V10"), receipt is not None, "the receipt is unreadable")
    entry = base.text_or_none(pkg.entry)
    need(("V4", "V7", "V9", "V10", "V11"), entry is not None, "the entry is unreadable")
    need(("V3", "V6", "V9", "V12"), base.text_or_none(pkg.registry) is not None, "the source registry is unreadable")
    need(("V9",), base.text_or_none(pkg.readme) is not None, "the README is unreadable")
    need(("V9",), (root / "PROVINCE.md").is_file(), "PROVINCE.md is absent")
    need(("V8",), (root / ORDER_REL).is_file(), "order_check.py is absent")
    need(("V8",), (root / CLAIMS_REL).is_file(), f"{CLAIMS_REL} is absent")

    def tags_cases():
        tags, ids = base.dry_table(pkg)
        return tags and ids

    parse(("V4", "V7", "V10"), tags_cases, "the frozen dry table parses to zero tags or zero cases")
    parse(("V4", "V7", "V9", "V10"), lambda: base.receipt_cases(receipt or ""), "the receipt parses to zero CASE lines")
    parse(("V7",), lambda: map_rows(entry or "")[0] is not None, "the requirement map has no parsable header")
    parse(("V9",), lambda: re.search(r"^## Case table\n", entry or "", re.M), "the case table is absent")
    parse(("V10",), lambda: re.search(r"^## Mechanism\n", entry or "", re.M), "the mechanism section is absent")
    parse(("V11",), lambda: len(base.PRED_BLOCK.findall(
        (base.PRED_SECTION.search(entry or "") or [None, ""])[1])) == 1,
          "the predictor section does not hold exactly one python block")
    if base.ready(MUT_N) and base.ready(MUT_FLOOR):
        parse(("V14",), lambda: load_plan(root) is not None, f"the mutation plan is absent or unparsable: {MUT_PLAN_REL}")
    note = f"inputs={counts['inputs']} tables={counts['tables']} blocked={len(blocked)}"
    return not blocked, note, blocked


# ---- driver ------------------------------------------------------------------------------------

def run_legs(base, root, lane, pkg, work, which):
    table = {
        "V1": lambda: base.v1(pkg),
        "V2": lambda: base.v2(lane, pkg, work),
        "V3": lambda: base.v3(pkg),
        "V4": lambda: base.v4(pkg),
        "V5": lambda: base.v5(lane, pkg),
        "V6": lambda: base.v6(pkg),
        "V7": lambda: v7(base, pkg),
        "V8": lambda: v8(base, root, pathlib.Path(work) / "gate"),
        "V9": lambda: base.v9(pkg),
        "V10": lambda: base.v10(pkg),
        "V11": lambda: base.v11(pkg, work),
        "V12": lambda: base.v12(pkg),
        "V13": lambda: base.v13(lane, work),
        "V14": lambda: v14(base, root, pathlib.Path(work) / "mutation"),
        "V15": lambda: None,
    }
    blocked = {}
    if "V15" in which:
        ok15, note15, blocked = preconditions(base, lane, pkg)
        print(f"V15 {'ok' if ok15 else 'DEFECT'} {note15}")
        res = [("V15", ok15, note15)]
    else:
        res = []
    for name in which:
        if name == "V15":
            continue
        if name in blocked:
            ok, note = False, f"precondition: {blocked[name]}"
        else:
            try:
                ok, note = table[name]()
            except Exception as e:  # a leg that cannot run is a defect, never a pass
                ok, note = False, f"error {type(e).__name__}: {e}"
        print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
        res.append((name, ok, note))
    return res


LEGS = ("V15", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14")


def main(argv=None):
    ap = argparse.ArgumentParser(description="round-48 C2 counter (v4) — TB2 polyglot-c-py package admission")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--dry", action="store_true",
                    help="stage-check: score every leg except V2 (the probe re-run); never prints `pass`, exits 1")
    ap.add_argument("--control", choices=CONTROL_ORDER, default=None,
                    help="measure a frozen control tree instead of the package; never prints `pass`, exits 1")
    a = ap.parse_args(argv)
    root = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    try:
        base = load_base(root)
    except SetupError as e:
        print(f"SETUP {e}")
        print("PREDICATE R48-C2 fail")
        return 2
    dry = a.dry or bool(a.control)
    which = [leg for leg in LEGS if not (dry and leg == "V2")]
    rc, head = git(root, "rev-parse", "HEAD")
    print(f"REV {head.strip() if rc == 0 else 'none (not a git work tree)'} lane={root}")
    with tempfile.TemporaryDirectory(prefix="k48-c2-", dir=a.work) as work:
        lane = root
        if a.control:
            lane = control_tree(root, work, a.control)
            print(f"CONTROL {a.control} tree={lane} p10=disabled")
        try:
            pkg = base.filler_pkg(lane) if a.control == "filler" else base.real_pkg(lane)
        except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
            print(f"PACKAGE unreadable: {e}")
            defects = 0
            for name in which:
                if name == "V13":
                    try:
                        ok, note = base.v13(lane, work)
                    except Exception as e2:
                        ok, note = False, f"error {type(e2).__name__}: {e2}"
                else:
                    ok, note = False, f"package unreadable: {e}"
                defects += not ok
                print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
            print(f"checks={len(which)} defects={defects}")
            print(f"PREDICATE R48-C2 {'fail' if defects else 'dry'}")
            return 1
        res = run_legs(base, root, lane, pkg, work, which)
        defects = sum(1 for _n, ok, _note in res if not ok)
        print(f"checks={len(res)} defects={defects}")
        if defects:
            print("PREDICATE R48-C2 fail")
            return 1
        if dry:
            print("PREDICATE R48-C2 dry")  # a stage-check is structurally clean; it is never an admission
            return 1
        print("PREDICATE R48-C2 pass")
        return 0


if __name__ == "__main__":
    sys.exit(main())
```
