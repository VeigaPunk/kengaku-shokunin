
## Re-check at dbcecded (follow-up)

Same seat (KengakuR29-2.FCritClaimMet-2), same item. Lane master dbcecded4a04247cf6fd12919327af973da10bdd; instrument sha256
135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142. The prereg is byte-unchanged (`git diff --quiet 56fd949 dbcecded --
plans/round-29-claims.md` exits 0). My earlier bytes equal the committed blob. No tools installed. Mutant and copy runs used
`mktemp -d /tmp/fcritclaimmet-v2-XXXX`, which I removed afterwards (`ls -d /tmp/fcritclaimmet*` finds nothing).

### Commands (lane root, read-only; outputs in scratch `v2-*`)

| command | exit | observation |
|---|---|---|
| `python3 plans/config_projection.py --summary` | 0 | `TOTAL findings=0 exit=0`; `diff` against repair-summary.txt differs only by that receipt's appended `exit=0` (line 54) |
| `… --json` | 0 | sha256 a4fb5d6d…d851 = repair-json-sha256.txt = candidate-freeze-v2 `json_output_sha256` |
| `… --selftest` | 0 | `SELFTEST clean cases=28` (was 20) |
| `python3 -O … --summary` | 2 | `FINDING {"detail": "python -O strips load-bearing checks", "id": "assertions_disabled"}` |
| `python3 plans/fixtures/r29/mutation_witness.py` | 0 | parsed JSON **equal** to repair-mutation-witness.json; 10/10 killed, restored sha = tool sha |
| `rederive.py` (unchanged since the first pass) on v2 JSON, with the renamed index key aliased in a /tmp copy | 0 | `MISMATCHES: 0`; per-task record mismatches **0 of 812** ×3, including key order (was 812 of 812 at 56fd949) |
| own old-vs-new comparison (scratch `out.json` c8da0c5a… vs `v2-out.json`) | 0 | see "Bridge" below |
| /tmp mutant: line 414 `return result, int(bool(findings))` → `return result, 0` | selftest **0** | **survives** (D5r below) |

### Bridge: are the oracles' pre-repair comparisons still valid?

All four oracle reports compared the pre-repair output (sha c8da0c5a…: FOracleText "Commands", FOracleProvenance
`instrumentjson`, FOracleLeaf A1, FOracleIndex baseline). repair-projection-equality.json claims the projections are
unchanged as objects. I checked this myself on both full JSONs. For every profile, 812/812 task records are equal and every
non-task profile field is equal. `occurrence_provenance` is equal. `population` is equal apart from one added key,
`duplicate_object_keys`. The only differences are new or renamed keys:
- a new top-level `witnesses`;
- `index_mapping` keys renamed to `index_equals_task_id_count` (812) and `index_task_id_mismatches` ([]), plus a new `unit`
  field ("input tasks (profile-invariant)"), with the same values as before;
- `limitations` (3 lines added);
- `source_contract.authority` wording.

`projected_task` key order now equals raw order in 812/812 ×3. The receipt's per-profile scope does not mention the
`index_mapping` rename, but the values are preserved, so the bridge holds. [OBSERVED]

### Status of my first-pass defects

| ID | first pass | now | evidence |
|---|---|---|---|
| D1 oracle agreement | UNMET | **MET (bounded)** | FOracleText: all 2436 records, 4248 changed leaves and 1435 provenance rows. Its one disagreement was a unit difference (2436 vs 812), now resolved by `index_mapping.unit`. FOracleLeaf A1 (2436/2436 three ways), FOracleProvenance (1435/1435, 6 fields), FOracleIndex (2436 rows × 9 checks), all `VERDICT: PASS`, all declaring no production read. The bridge above carries this to dbcecded. Limit, from FCritOracleIndependence §2–3: the oracles were output-conditioned, not blind (FOracleProvenance adopted the instrument's `[]` rendering after a 398-row first-run diff), and benign-population agreement cannot discriminate order or ID naming. The witnesses and mutants carry that part. Comparisons were made by the oracle seats, with Main's bridge receipt on top; prereg l.81 "Main compares every required metric and per-task object, not only totals." (11 words) is met in substance, not in authorship. Tradeoff, not a defect |
| D2 witness values not emitted | PARTIAL | **MET** | summary now has `INDEX_WITNESS hand [{"output_filename": "config_files/0.json", "task_id": 1, …}, {"output_filename": "config_files/1.json", "task_id": 0, …}]` and `ORDER_WITNESS … source_order_text=…https://map.invalid/order/probe… mapping_order_text=…__REDDIT__/probe…`, equal to the fixtures' `expected_records` / `expected_projected_text` / `predicted_mapping_order_mutant_text`. Witness raw text is asserted byte-equal to the fixtures (config_projection.py:507, 523), and the fixtures are sha-pinned (`HAND_SHA256`, case `hand_fixtures_authenticated`) |
| D3 `non_url_field` label | defect | **FIXED** | LIMIT "category is by JSON path, so non_url_field leaves may hold URL-shaped strings" (12 words); draft v2 l.50 gives the 60 + 1 split; l.57–58 says all 61 are URL-shaped |
| D4 sorted keys | tradeoff | **FIXED** | `sort_keys` removed from the `--json` print; LIMIT "projected_task keeps source key order…"; my record-level check is now 0 mismatches including order |
| D5 exits not checked | PARTIAL | **PARTIAL (narrower; D5r)** | new case `exit_mapping` (l.564–573) checks that `main()` maps a faked audit's findings to 1, `Unevaluable` to 2 and `RuntimeError` to 2 (`internal_error`). But it replaces `audit` itself, so the audit-level mapping at l.414 is never exercised |
| D6 errors hand-case file | PARTIAL | **still PARTIAL** | `plans/fixtures/r29/hand/` still has the same 4 files; no hand file carries expected errors. The divergence disclosure for prereg l.43–44 now exists only in FOracleLeaf A2 (H1–H3), and FCritOracleIndependence §4 flags two problems there that no repair has touched (FOracleLeaf.md is the same bytes at dbcecded): (a) single-pass instead of the assigned sequential decoded substitution, so H3 is a single-pass artefact; (b) FOracleLeaf.md:86–87 "upstream would produce no test.json at all" (7 words) contradicts generator l.17–18 (`f.write(raw)`), which writes test.json before `json.loads` at l.20 |
| D7 mutation receipt not reproducible | defect | **FIXED** | plans/fixtures/r29/mutation_witness.py persists 10 exact replacements; my rerun gives a byte-equal parsed receipt |
| D8 draft "identical except digests" | wording | **FIXED** | draft v2 l.41–42 "…except their text digests and the `//` junction row" |

### New finding D5r: findings→exit-1 mapping in `audit()` is untested (surviving mutant)

Location: plans/config_projection.py:414 `return result, int(bool(findings))`. Mutant (on a /tmp copy): `return result, 0`.
Observed: `--selftest` exit **0**; the mutant survives. Effect: any projection or invariant finding (`projection_json_invalid`,
`known_token_remaining`, `leaf_change_unexplained`, `input_population_mismatch`, …) would still print a `FINDING` line, but
the CLI would exit 0, against prereg l.53–54 ("exit1 = projection/invariant finding"). The frozen `--summary` cannot notice
either, because it has 0 findings. None of the 10 persisted mutants touches l.414. Classification: **fixable defect (small)**.
Smallest safe correction: in `selftest`, patch `audit_text` to return a minimal result plus `[{"id": "x"}]`, call the real
`audit(scratch)` on the pinned /tmp copy and assert code == 1. Then add this mutant to `mutation_witness.py`.

### C1 legs at dbcecded

| leg / prereg item | status |
|---|---|
| 812 / 3 / 2436, no hidden exclusions | MET (re-derived) |
| occurrence/field provenance, codepoint offsets | MET (re-derived; 4 oracles) |
| output-index vs task_id plus shuffled witness in output | MET (R9 now observed in `--summary`) |
| independent oracle agreement | MET (bounded: benign domain, output-conditioned, bridged across the repair) |
| Required output l.62–71 | 10/10 MET |
| Selftest l.73–77 | all MET except "findings and exits checked": PARTIAL (D5r) |
| hand-case file with errors; out-of-domain disclosure (l.43–44, l.82) | PARTIAL (D6) |
| failing wrong URL-only / wrong-order witness (l.100) | MET (persisted, reproduced) |

Scoped conclusion: the substantive C1 capability (correct projection, provenance, index mapping, oracle agreement) is
observed at dbcecded with 0 counterexamples. Two small fixable gaps remain against the frozen prereg contract: D5r (one
selftest assertion plus one mutant) and D6 (an errors hand case, plus correcting FOracleLeaf's single-pass/test.json claims
or replacing them). Neither changes any count.

VERDICT: PARTIAL
