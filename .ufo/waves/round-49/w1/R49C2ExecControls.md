# R49C2ExecControls — C2 pre-receipt controls, P10 disabled (executor)

Axes named: **coverage** (R49-C2 only). No other axis assessed. No admission is claimed for R49-C1 or
R49-C2; this seat measures the three frozen do-nothing controls against a wave-1 counter candidate and
does not integrate anything.

Seat writes are confined to this report and `./R49C2ExecControls/receipts/` (named by the seat item);
all measurement trees live under `/fast/scratch/hyaku/kengaku-r49/R49C2ExecControls/` and were removed
after the receipts were copied here. No production file in the lane was created, modified or committed.

## 1. Freeze gate — checked before the first measurement

The stage-1 freeze exists in the committed lane tree and predates every run below (`receipts/freeze-gate.txt`):

```
$ git -C lane-base log -1 --format="%H %cI %s" 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
$ git -C lane-base merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD; echo $?
exit=0
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format="%H %cI %s"
af88aab193e6034cb9b386472064e3c18fa90128 2026-10-28T09:18:20-03:00 round-49: w1 v2 wave spec + dispatch evidence (64 seats, 40 attack, policy v2 accepted)
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD; echo $?
exit=0
$ git -C lane-base ls-tree -r --name-only HEAD | grep -cE "round49_c2_verify|round48_c2_verify"
0
```

Freeze instant `2026-10-28T09:14:40-03:00` = **`2026-10-28T12:14:40Z`**. Control runs carry
`run_utc=2026-10-28T12:24:36Z` / `…12:24:37Z` / `…12:24:41Z` — the freeze precedes the measurement by
~10 minutes, and no stage-2 counter, spec pin or mutant plan exists in the frozen tree (`grep -c` = 0).
Therefore **no scored counter or probe execution was made on claimed work**: every run below passes
`--no-p10` and measures a control tree, and the candidate refuses scored mode structurally (§3).

## 2. Instruments (wave-1 candidates; neither is the stage-2 pin)

Preserved byte-exact under `receipts/instruments/` with `SHA256SUMS`:

| instrument | sha256 | role |
|---|---|---|
| `receipts/instruments/round49_c2_verify.py` | `ed1b9c0cbaec39341f59fb88985e7ce21e10aec92ebb307166ba0cc091eafe28` | counter candidate: imports `plans/round46_c3_verify.py` digest-pinned (`sha256=a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`, verified at load) and adds the four frozen deltas — `V7P` (delta a), `--no-p10` gate path (delta b), `V15` (delta c), `V14` (delta d) |
| `receipts/instruments/run_controls.py` | `522154b053d66f2dc7f25c1b4fa537f0ad938f698cd978942a7b6cefb8ce5178` | builds each control as a `git clone --shared` of the freeze, commits the candidate plus the transform, pins each control's ordering receipt, runs the candidate, writes the receipt |
| `receipts/instruments/supp_probes.py` | `bce3b0d0d54be11ff7e17263865ba587d775f5fdf2765c0f5814d3657955ecfc` | supplementary discrimination probes (§6) |

The structural fence (verbatim, `receipts/refusal.txt`) — without `--no-p10` the file cannot be pointed at
the claimed work:

```
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
REV_DIRTY 0
SETUP wave-1 control instrument: scored mode (P10 enabled) refused; pass --no-p10
checks=0 defects=0
PREDICATE R49-C2 not-run
EXIT=2
```

`--no-p10` invokes `plans/pkg_gate.py package --root <clone> --spec <effective spec> --require-clean-tree`
**without `--rerun`**, i.e. gate clauses P1–P9 only. The gate's own output is echoed into each receipt as
`gate: P…` lines, so the P10 absence is visible in the evidence rather than asserted. `V5` invokes the
probe `--dry` only; no `CASE … observed=` line is produced by this wave.

## 3. Control transforms, measured revisions, verdicts

Each control is a `git clone --shared` of `9d2900af…`; the runner asserts
`git -C "$D" rev-parse --show-toplevel` equals `$D` before any write, commits
`plans/round49_c2_verify.py` (candidate sha `ed1b9c0c…`), then the transform, then runs the counter. All
three trees report `REV_DIRTY 0`, so the gate's P9 clean-tree clause is meaningful.

| control | transform | REV (measured) | checks | defects | content defects | predicate | exit |
|---|---|---|---|---|---|---|---|
| base | `plans/polyglot_c_py_probe.py` deleted (526 deletions) | `b589a772c55a5195bea9cc2f7675fbaab1733aca` | 16 | 7 | 2 (`V7,V7P`) | **`PREDICATE R49-C2 fail`** | 1 |
| filler | none; `plans/filler46/` scored via `--filler` | `eacb5e1928dbf1d8b5ae568f4827caa0aba9b956` | 11 | 8 | 6 (`V4,V7,V7P,V9,V10,V12`) | **`PREDICATE R49-C2 fail`** | 1 |
| echo | frozen dry table copied over `corpus/evidence/round46/polyglot-c-py-probe.txt` | `8765559980649443bef5013ea7f5aa16636b26b0` | 16 | 7 | 4 (`V4,V7,V7P,V9`) | **`PREDICATE R49-C2 fail`** | 1 |

Command (identical for each, `cwd=$D`):

```
python3 plans/round49_c2_verify.py --lane "$D" --work "$SCRATCH/work-<name>" --no-p10 [--filler]
```

Verbatim leg lines (full receipts in `receipts/control-{base,filler,echo}.txt`):

**base** — `receipts/control-base.txt` (`REV b589a772…`, run `12:24:36Z`):

```
    gate: P1 DEFECT pinned=2 mismatched=['plans/polyglot_c_py_probe.py']
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen p10=disabled gate_exit=1
V5 DEFECT probe or dry table not at its freeze digest
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V7P DEFECT tags=7 parsed_cases=18 map_rows=7 cited=5/7 bad=["frozen tags with no violating case: ['both-print', 'toolchain']", 'both-print: round-46 V7 offender still uncovered', 'toolchain: round-46 V7 offender still uncovered']
V8 DEFECT order_exit=1 result=not-PASS
V14 DEFECT mutation floor <N> unpinned (stage-2 plan plans/mutants49/plan.json absent); wave-1 mutants absent
V15 DEFECT inputs=17 unresolved=['probe'] tables_parsed=2 tags=7 bad=0
content_defects=2 (V7,V7P)
checks=16 defects=7
PREDICATE R49-C2 fail
```

**filler** — `receipts/control-filler.txt` (`REV eacb5e19…`, run `12:24:37Z`):

```
V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
V7P DEFECT tags=4 parsed_cases=16 map_rows=4 cited=0/4 bad=["frozen tags with no violating case: ['single-file', 'python-run', 'c-run', 'fib']"]
V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V14 DEFECT mutation floor <N> unpinned (stage-2 plan plans/mutants49/plan.json absent); wave-1 mutants absent
content_defects=6 (V4,V7,V7P,V9,V10,V12)
checks=11 defects=8
PREDICATE R49-C2 fail
```

**echo** — `receipts/control-echo.txt` (`REV 87655599…`, run `12:24:41Z`):

```
    gate: P1 ok pinned=2 mismatched=0
    gate: defects=0
V2 ok spec=frozen gate=frozen p10=disabled gate_exit=0
V4 DEFECT cases=18 mismatches_named=0/0 bad=['case ids differ from the frozen table', 'summary line count != 1']
V7 DEFECT rows=5 tags=7 bad=['single-file: no receipt case violates it', …  "unparsed row '| instruction.md:7 | both-print | not exercised | '", …]
V7P DEFECT tags=7 parsed_cases=0 map_rows=7 cited=0/7 bad=["frozen tags with no violating case: ['single-file', 'python-run', 'c-build', 'both-print', 'fib-kth', 'stdout-only', 'toolchain']", … 'receipt carries no parsable CASE ... observed= line']
V8 DEFECT order_exit=1 result=not-PASS
V9 DEFECT case_rows=18/0 bad=['case table rows=18 receipt cases=0 equal=False']
V15 DEFECT inputs=17 unresolved=0 tables_parsed=2 tags=7 bad=['receipt has no parsable CASE lines']
content_defects=4 (V4,V7,V7P,V9)
checks=16 defects=7
PREDICATE R49-C2 fail
```

The echo control is the honest discriminator: with P10 disabled the **gate accepts** (P1–P9 all ok,
`gate: defects=0`), so its fail verdict comes only from the counter's own content legs
(`V4,V7,V7P,V9`) plus `V15` — a gate-only check would have been fooled by a copied dry table.

None of the three fail verdicts rests on `V14` alone; each has ≥2 substantive content defects. `V14`
defects as designed before stage 2 (`<N>` and the plan are stage-2 literals).

## 4. Ordering receipts (`plans/order_check.py`), verbatim

`receipts/control-*.txt` carry both ORDER blocks per control. Observed identically for all three:

```
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt exit=1
ORDER claims=plans/round-49-claims.md round=49 freeze=9d2900af41e4d1fc6022eff99010436fde6dbd93
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt receipt_commit=8d7f74ce63c25ad200c69fe0d90158cc7099def6 claims_dir=.ufo/waves/round-49/claims/
ORDER FAIL freeze-contains-receipt 9d2900af41e4d1fc6022eff99010436fde6dbd93 already has corpus/evidence/round46/polyglot-c-py-probe.txt
ORDER FAIL receipt-before-claims 8d7f74ce63c25ad200c69fe0d90158cc7099def6 is an ancestor of 9d2900af41e4d1fc6022eff99010436fde6dbd93
ORDER scanned commits=0 file_entries=0 distinct_blobs=0
ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0
ORDER RESULT FAIL
ORDER receipt=corpus/evidence/round49/polyglot-c-py-probe.txt exit=2
ORDER RESULT ERROR
ORDER ERROR receipt not committed in HEAD: corpus/evidence/round49/polyglot-c-py-probe.txt
```

Read literally, `order_check` **cannot pass a control receipt**, and this is the frozen V8 fix working:
the round-46 receipt predates the round-49 freeze (both clauses fire) and the stage-3 receipt does not
exist yet (setup error 2, never a silent pass). A control that *passed* ordering would refuse the
counter. To prove the gate is not refuse-all on this host, its PASS path was exercised on scratch
histories (`receipts/order-selftest.txt`, extracted):

```
### POSITIVE: claims committed first, stage-3-shaped receipt after
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
EXIT=0

### NEGATIVE 2: a claims/ blob committed before the receipt shows P10 executed (the r48 V8 defect)
ORDER HIT .ufo/waves/round-49/claims/control-base.txt@da93c86d6045:1 kind=gate-p10 `gate: P10 ok probe_rerun=byte-equal bytes=123`
ORDER FAIL probe-executed-before-receipt hits=1
ORDER RESULT FAIL
EXIT=1
```

(Negative 1 — receipt and claims in one commit — prints `ORDER FAIL freeze-contains-receipt`, exit 1.)
`order_check.py` at the frozen base has `sha256=948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc`.

## 5. Repo hygiene

Four clones of the lane exist in scratch (one base + one per control); no full mirror; one shared clone
per seat tree. Nothing under `/tmp` is cited: every receipt path above is under this wave directory.
Lane `git status --porcelain` shows only the wave directory and its dispatch marker.

## 6. Supplementary discrimination probes (not frozen controls, not scored)

`receipts/supp-discrimination.txt` (candidate sha `ed1b9c0c…`):

```
A v7p-frozen  DEFECT tags=7 parsed_cases=18 map_rows=7 cited=5/7 bad=[…'both-print', 'toolchain'…]
B v7p-amended ok tags=7 parsed_cases=20 map_rows=7 cited=7/7 bad=0
C v14 2-flip+2-noop floor=2 ok total=4 caught=2 floor=2 verdict=met baseline_clean=['V3', 'V4', 'V9', 'V10', 'V12'] missed=['m-noop-a', 'm-noop-b']
D v14 0-flip floor=1 DEFECT MUTATION DEFECT total=2 caught=0 floor=1 verdict=unmet baseline_clean=['V3', 'V4', 'V9', 'V10', 'V12'] missed=['m-noop-a', 'm-noop-b']
SUPP ok failures=0
```

- **A/B (round-48 routed defect 3).** `V7P` is **satisfiable**: it defects on the frozen tables and goes
  `ok … cited=7/7` on the same tables after two violating cases are added for `both-print`/`toolchain`
  and the two unparsable map rows are repaired to the header's column count. A stage-2 amendment can
  therefore satisfy the leg; it is not unsatisfiable by construction.
- **C/D (mutation-leg mechanics).** The first candidate counted **every** mutant as caught, because the
  frozen table already defects `V7`/`V7P`, so a mutated copy "defects" for free. It was repaired to
  count a mutant only when it flips a leg that the **unmutated** package prints `ok` for, and to declare
  a `MUTATION DEFECT vacuous battery` when no substantive leg is clean at baseline. C then catches the
  two flipping mutants (`caught=2`) and ignores the two no-ops; D reports `unmet`.

This is the defect class the L1's stage-2 `V14` must not repeat: a battery scored against an
already-defective baseline is vacuous and would "meet" any floor for free.

## 7. Limits

- The candidate is **not** the stage-2 pin. `V10`'s `DECISIVE` map and `V12`'s row rule are the imported
  round-46 ones; a stage-2 case-table amendment must re-key `V10` (the candidate does not).
- `V14`'s mutant-plan schema (`{"N": int, "mutants":[{"id","file","find","replace"}]}`) is fixed by this
  candidate because no plan exists yet; the stage-2 counter owns the authoritative schema.
- Pre-receipt runs read the round-46 spec and its pins (`PINS spec=r46-spec probe=67a8f4a6 dry=99adfea6`);
  `plans/pkg-spec-r49.json` is honoured when present but does not exist at the freeze.
- `V6` shells out to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (outside the lane) exactly
  as the imported round-46 counter does; read-only.
- `V11` builds its state set per run inside `bubblewrap`; the echo control exercises it normally
  (`states=60 grader_pass=15 grader_fail=45 disagree=0`), so `V11` is live, not skipped.
- No external URL was opened by this seat, so no URL/access-date/quote is recorded; the claim's sourced
  basis S166 was not re-opened here and remains the L1's duty (§C2 "Sourced basis").

## 8. VERDICT

**All three frozen R49-C2 controls produce `PREDICATE R49-C2 fail` with exit 1, each with content defects
independent of the unpinned `V14`; the counter candidate refuses scored mode; the ordering gate refuses
both control receipts and its PASS path is proven reachable; the two frozen tag classes are satisfiable
by a table amendment; and one wave-1 defect was found and repaired in the mutation leg (baseline-relative
catching).** No stage-2 counter, spec pin, mutant plan or receipt was created, and no admission is
claimed for R49-C1 or R49-C2.
