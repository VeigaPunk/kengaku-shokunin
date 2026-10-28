# R49C2Filler — committed filler attack on the C2 counter

**Axes:** coverage (R49-C2 only). **Verdict:** `VERDICT: v4 counter not available at frozen base; strongest plausible filler does not clear the v3 predecessor, and the frozen V8 ordering rule independently prevents a pre-committed filler receipt from clearing v4. Not an admission judgment.**

## Freeze and limits

The required freeze exists in the committed lane tree: `9d2900af41e4d1fc6022eff99010436fde6dbd93`, committed `2026-10-28T09:14:40-03:00`, before all measurements below. The wave-1 lane tree available during this seat had no `plans/round49_c2_verify.py`, `plans/pkg-spec-r49.json`, or `plans/mutants49/plan.json`; therefore there was no actual v4 counter to execute. I used `plans/round46_c3_verify.py` as the code-level predecessor and the frozen round-49 claims for v4-only projections. No lane files were changed. The candidate packages and all command work products were scratch-only.

The strongest filler candidate used the seven real S166–S172 captures and their hashes, the actual 18-case receipt and frozen table, the real entry (including requirement map, case table, mechanism, and predictor), a copied registry with valid entry references, a filler-specific README index/frontier, and a pinned trivial dry-output probe. It is deliberately stronger than a plausible but ungrounded filler: it demonstrates that structural/content checks can be copied or satisfied. The scratch `filler49/` layout was one level below lane root because census `--file` resolves used-by paths under the file's grandparent; this allowed census and the gate's entry-path check to agree.

## Exact commands and observed outputs

All initial source reads were the full `plans/round-49-claims.md` and full `corpus/lessons/round-48-verifier-spotcheck.md`; tooling rules read from `/home/vgpnk/.omp/agent/RULES.md`. Freeze check:

```text
git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
git log -1 --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
```

Scratch clone was checked with `git -C "$L" rev-parse --show-toplevel` and returned `/fast/scratch/hyaku/kengaku-r49/R49C2Filler/lane`; its `HEAD` was the freeze commit. Core measurements (paths abbreviated here only for readability; literal executed commands shown):

```text
cd $L && timeout 600 python3 plans/round46_c3_verify.py --lane . --filler --work $TMPDIR/work
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V6 ok census_exit=0 registry=plans/filler46/SOURCES-filler.md
V7 DEFECT rows=7 tags=7 bad=['both-print: no receipt case violates it', 'toolchain: no receipt case violates it']
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V12 ok rows=7 defective=0 live=0
checks=7 defects=1
PREDICATE C3 fail
```

This is the informed filler against the r46 frozen artifacts after fixing the requirement-map rows to be syntactically parsed. Before fixing those two map rows, V7 reported them unparsed/missing; the observed remaining defect shows the more substantive unsatisfiable-tag condition. The input is r46, so this V7 result is not a measurement of the amended r49 V7 table.

All applicable predecessor legs plus V11 were separately run through a scratch-only driver against the best one-level layout:

```text
cd $L && python3 $TMPDIR/filler_legs.py . filler49/pkg-spec.json V11
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V6 ok census_exit=0 registry=filler49/SOURCES.md
V7 DEFECT rows=7 tags=7 bad=['both-print: no receipt case violates it', 'toolchain: no receipt case violates it']
V8 DEFECT order_exit=2 result=not-PASS
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V12 ok rows=7 defective=0 live=0
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
```

The gate was run with rerun/P10 disabled, matching the frozen pre-receipt control shape:

```text
cd $L && timeout 900 python3 plans/pkg_gate.py package --root . --spec filler49/pkg-spec.json
P1 ok pinned=1 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4 ok checked=20 bad=0 first=0
P5 ok manifest_entries=8 bad=0 first=0
P6 ok rows=7 bad=0 first=0
P7 ok source_lines=7 bad=0 first=0
P8 ok index_rows=1 knowledge_files=1 bad=0 first=0
defects=0
gate_exit=0
```

The exact V8 ordering check against an already committed receipt in the frozen tree was:

```text
cd $L && python3 plans/order_check.py --lane . --claims plans/round-49-claims.md --receipt corpus/evidence/round46/polyglot-c-py-probe.txt
ORDER claims=plans/round-49-claims.md round=49 freeze=9d2900af41e4d1fc6022eff99010436fde6dbd93
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt receipt_commit=8d7f74ce63c25ad200c69fe0d90158cc7099def6 claims_dir=.ufo/waves/round-49/claims/
ORDER FAIL freeze-contains-receipt 9d2900af41e4d1fc6022eff99010436fde6dbd93 already has corpus/evidence/round46/polyglot-c-py-probe.txt
ORDER FAIL receipt-before-claims 8d7f74ce63c25ad200c69fe0d90158cc7099def6 is an ancestor of 9d2900af41e4d1fc6022eff99010436fde6dbd93
ORDER scanned commits=0 file_entries=0 distinct_blobs=0
ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0
ORDER RESULT FAIL
order_exit=1
```

For the v3 fixed filler control (restored from the committed base in scratch), the observed V13 legs were:

```text
cd $L && timeout 600 python3 plans/round46_c3_verify.py --lane . --filler --work $TMPDIR/work
V3 ok rows=7 bad=0
V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
V12 DEFECT rows=7 defective=7 live=7 first=S166:capture_unresolved capture=0
checks=7 defects=6
PREDICATE C3 fail
```

The committed baseline filler therefore satisfies the predecessor's V13 requirement of at least three substantive failures (observed failures V4, V7, V9, V10, V12); V3 is okay and V6 is non-substantive to the V13 floor.

## V1–V15 effect table

The counter file absent at measurement means only V1–V13 predecessor behavior is measured; V14/V15 and v4 deltas are projections from the frozen contract, explicitly not executed results.

| Leg | Effect of strongest plausible filler | Evidence / status |
|---|---|---|
| V1 capture manifest | **Pass** with the 8 real captures and manifest. | Measured `listed=8 wrong=0 extra=0` on best layout. |
| V2 gate | **Pass** with correct frozen-format inputs when P10 rerun is disabled. | Measured `pkg_gate` P1–P8 all okay on best layout. P10 itself not executed, per frozen pre-receipt ordering. |
| V3 anchor digests | **Pass** by using the real pinned S166–S172 rows/captures. | Measured `rows=7 bad=0`. |
| V4 receipt/table consistency | **Pass** by copying the receipt and matching case table; r46 table's `float-c` false `match=yes` is only a defect in the *old committed filler*. | Measured pass on best layout. |
| V5 probe/dry-table | **Can be made to pass** by shipping a probe whose `--dry` output exactly matches the package table and pinning both. | Not in predecessor's filler subset; scratch candidate probe outputs the copied dry table. v4 pin semantics unavailable to execute. |
| V6 census | **Pass** with one-level registry layout and valid used-by path. | Measured `census_exit=0`; nested `plans/filler46/SOURCES-filler.md` initially failed E12/E11 before layout correction. |
| V7 requirement map | **Fails on r46 table** because `both-print` and `toolchain` have no violating receipt cases, even with parseable labels. | Measured two exact `no receipt case violates it` defects. Frozen v4 V7 requires amended table to violate all seven; an informed committed filler can copy an amended table/receipt and could pass if the amended predicate permits the content. |
| V8 ordering | **Fails for an already committed filler receipt.** A receipt first committed before stage 3 cannot meet the frozen rule that its first-commit is stage 3. | Existing committed receipt produced `freeze-contains-receipt` + `receipt-before-claims`; scratch receipt was uncommitted and produced `order_exit=2` (missing committed receipt). Exact v4 stage-3 first-commit test not executable without counter. |
| V9 case-table/provenance | **Pass** by using the real entry and a task+entry naming line in PROVINCE. | Measured `case_rows=18/18 bad=0`. |
| V10 mechanism | **Pass** by copying real mechanism rows and captures. | Measured `mechanism_rows=18/18 bad=0`. |
| V11 held-out predictor | **Pass** for copied predictor on this host. | Measured `states=60 grader_pass=15 grader_fail=45 disagree=0`. |
| V12 anchor-line rule | **Pass** with genuine capture quotes and digests. | Measured `rows=7 defective=0 live=0`. |
| V13 filler control | Existing filler **passes V13's discriminator** (six V13 subleg defects, including five substantive). Replacing the fixed filler with this informed package would leave only V7 defective on r46 artifacts, below its ≥3-substantive floor, so V13 itself would defect. | Existing baseline measurement above; one-defect projection follows measured informed filler. This is a second counter-design trap if the v4 V13 behavior retains the predecessor floor and the filler path is attacker-controlled. |
| V14 mutation floor | **Not measured.** A realistic filler may copy all current bytes, but V14 must independently show the frozen `<N>` mutants flip substantive package legs and reach `<N>/2`; copied package inputs do not by themselves prove sensitivity. | Stage-2 plan / mutants file absent at base during this run. No V14 claim. |
| V15 preconditions | **Likely satisfiable by a complete filler** with all frozen digests resolving and parsable tables. | Projection only; v4 leg unavailable. The contract requires missing/tampered inputs to be DEFECT, which is the counter behavior to preserve. |

## Strongest counterexample and correction

**Counterexample:** a committed, plausible filler package can make the ordinary content checks and gate accept copied evidence (measured V1/V2/V3/V4/V6/V9/V10/V11/V12 all pass on the best candidate), but it cannot satisfy the frozen C2 requirement that its receipt's first commit be stage 3 after the receipt already exists in a pre-committed filler. Separately, if a copycat filler is made so strong it fails fewer than three substantive checks, inherited V13 logic itself defects. Thus the claimed filler control remains failable, but the current V8/V13 combination risks an unsatisfiable or self-referential gate rather than serving as independent evidence of package quality.

**Smallest safe correction:** retain the first-commit-at-stage-3 rule for the *real package's fresh receipt* (the actual claim ordering), but exclude the fixed filler package from V8 receipt-order measurement; keep the filler as a semantic discriminator under V13. Ensure V13's threshold is not asked to reject a filler that independently passes the same legs; use a separately frozen adversarial semantic control with an explicit expected set of substantive defects, not a control whose success is defined by how many defects it has. No predicate or control was edited by this seat.

## Source and limits

No external URL was fetched. The local capture and entry record the source as accessed 2026-10-27:

- URL: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`
- Access date: 2026-10-27 (as recorded in the captured entry)
- Located quote: `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` (10 words)

Limits: v4 counter, amended r49 dry table/receipt, stage-2 mutant plan, and stage-3 receipt did not exist in this seat's available tree, so V5/V7/V8/V13/V14/V15 statements about v4 are projections where marked. No external-source re-fetch, full v4 run, or admission judgment was performed. Tool installs/updates: none.

Scratch was removed before yield; report is the only lane write.