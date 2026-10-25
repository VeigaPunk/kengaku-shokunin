# FP4d — frozen round-26 population assertions

Identity: KengakuR27.FP4d; reviewer, **not** candidate writer KengakuR27. Scope is calibration/P4d only; this yields no novelty evidence. Candidate was read at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`; canonical `corpus/knowledge/extraction-policy-comparison.md` is absent in this tree and is not reviewed/admitted here.

Observed worktrees: scratch clone HEAD `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`; exported base `b5719440e5eee46c1886fddbdf7bdc1624829454`.

## Executed results

`python3 -B plans/state_check.py --summary --root /tmp/kengaku-r27-base` (v4 script from the candidate clone): `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`, exit 0. Same command with `--root /tmp/kengaku-r27-FP4d`: same output, exit 0. P4d-only JSON filter (`python3 -B plans/state_check.py --json --root ROOT | jq -r '.assertions[] | select(.id|startswith("P4d.")) | [.id,.verdict] | @tsv'`, pipefail): exit 0 for both roots.

| P4d assertion | exported base | candidate |
|---|---|---|
| `P4d.population.records` | MATCH | MATCH |
| `P4d.population.files` | MATCH | MATCH |
| `P4d.population.verdicts` | MATCH | MATCH |
| `P4d.population.graders` | MATCH | MATCH |
| `P4d.family.F1` | MATCH | MATCH |
| `P4d.family.F2` | MATCH | MATCH |
| `P4d.family.F3` | MATCH | MATCH |
| `P4d.family.F4` | MATCH | MATCH |
| `P4d.family.F5` | MATCH | MATCH |
| `P4d.family.F6` | MATCH | MATCH |
| `P4d.family.F7` | MATCH | MATCH |
| `P4d.family.D1` | MATCH | MATCH |
| `P4d.family.G1` | MATCH | MATCH |
| `P4d.family.G2` | MATCH | MATCH |

P4d-specific mismatches: none. P4d-specific `OFFLINE_UNVERIFIABLE`: none. The separate `P4.population.assertion-inventory` is MATCH on both roots; whole-checker offline-unverifiable count 3 is outside P4d.

Independent rederivation from the four pinned base JSONL files: read-only `jq -s 'map(select(has("raw") and has("ok"))) as $r | {records:($r|length),pass:([$r[]|select(.ok==true)]|length),fail:([$r[]|select(.ok==false)]|length),cells:($r|map(.cell)|sort|group_by(.)|map({cell:.[0],n:length}))}' FILE` returned exit 0 for each. Results: round8 188 / 125 PASS / 63 FAIL; round9 128 / 75 / 53; round11 320 / 136 / 184; round12 1328 / 685 / 643. Totals: 1964, 1021 PASS / 943 FAIL. Cell-derived split: round8 has 172 state, 12 `grade_c`, 4 C-MONO `valid_latin`; round9 128 state; round11 320 state; round12 1088 state + 240 sequence. Totals are state=1708, seq=240, `grade_c`=12, `valid_latin`=4.

`python3 -B plans/grader_perturb.py --json --root /tmp/kengaku-r27-base` and the same command on candidate root both exited 0: population=1964, candidate_count=1964, excluded=0; all four input pins true; family outputs F1 1802/1819, F2 1802/1819, F3 1964/1964, F4 1720/1720, F5 1964/1964, F6 1964/1964, F7 1876/1876, D1 909/909, G1 1021/1021, G2 1021/1021. `python3 -B plans/fixtures/r26/perturb_oracle.py --root /tmp/kengaku-r27-base` exited 0 and independently returned the same population disposition and all ten family n/k pairs. Historic receipts agree: `corpus/evidence/round26-calibration/grader-perturb-final.txt:1-27` and `perturb-oracle-final.txt:1-15`; the original oracle discloses its read scope and limits at `perturb-oracle-build-observation.txt:5-7,29-34`.

## Findings

### Medium — P4d population `MATCH` overstates what its live comparators derive

The frozen promise is file totals, PASS/FAIL, grader split, and family n/k “against `grader_perturb.py --json` and the oracle” (`plans/round-27-claims.md:117-124`). But the JSON schema only emits aggregate population, format-class counts, pins and family results (`plans/grader_perturb.py:813-826`), not per-file totals, stored PASS/FAIL totals, or grader counts. P4d file comparison checks audit + TSV manifest + expected constants + pin-path set (`plans/state_check.py:3110-3127`); PASS/FAIL compares audit only with manifest/constants (`:3170-3181`); grader split derives solely from manifest grader counts and C-MONO (`:3191-3209`). Oracle output likewise has aggregate disposition and family results, not these three breakdowns (`perturb-oracle-final.txt:2-13`). Thus these subclaims are not dynamically cross-checked against either named command by state_check v4, despite all four IDs returning MATCH. My direct raw-file scan above independently confirmed the frozen values, so this is a comparator/provenance defect, **not** an observed numeric mismatch. Requested correction: derive those splits from the actual loaded, byte-pinned records (or mark them unavailable) rather than treating the build manifest as live truth.

### Low — unregistered measured numerics are not surfaced as unavailable

Amendment 1 requires unmapped numeric assertions to be exposed as offline-unverifiable (`plans/round-27-claims.md:184-186`). The population inventory only checks equality of the fixed assertion-ID tuples (`plans/state_check.py:3319-3324`); P4d's family parser reads only kind and k/n (`:3213-3239`). Consequently other measured values in the same frozen audit—e.g. CP95 bounds, 15168/909 totals, duplicate counts, pid-composite bounds and D1 strata (`corpus/knowledge/grader-perturbation-audit.md:64-87`) are neither checked by a P4d ID nor reported as offline-unverifiable. These are not mismatches to the narrowly listed P4d population/n/k promise, and I did not independently rederive them; the issue is their silent omission from the required inventory interpretation.

## Residual risk and disposition

All 14 registered P4d IDs match on the exported base and candidate; historic and current runs support the population and family numbers. The oracle is separately implemented, but its receipt discloses reading the extractor regex/context and using recorded C-cell diagnostics, so it is not source-blind authority. No arbitrary-population or future-sample claim follows. No novelty claim is evaluated here.

Installs/updates: none.

VERDICT: scoped FAIL — P4d numeric values rederive, but v4 does not independently check all promised population splits and silently omits unmapped measured numerics from its offline-unverifiable inventory.