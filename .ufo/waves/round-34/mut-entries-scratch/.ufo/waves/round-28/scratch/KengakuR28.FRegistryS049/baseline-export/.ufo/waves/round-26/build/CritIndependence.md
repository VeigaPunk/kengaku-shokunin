# CritIndependence: round 26 build (critic, read-only; novelty→coverage/constructs, calibration)
Seat KengakuR26-2.CritIndependence-4. Lane HEAD e0037a8. Target: the per-record CP95 for C1 (`plans/round-26-claims.md:69-73`).
`plans/grader_perturb.py` is not in any clone yet, so I re-ran C1 in a scratch script, `/tmp/critindep/indep.py` (sha256 f324226ab40a3e191742b357479b632b33d06c43fa128feb5221d18f2fe622a2). It imports the grader.py extract/grade functions and `attrib_calibration.clopper_pearson`/`verdict` with bytecode writing off, and writes nothing in the lane.
`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/critindep/indep.py` → exit 0. Population: 1964 records with `raw`+`ok`; the baseline reproduces on 1964/1964 and 0 are excluded.
`:58` "strip the code fence" can be read two ways, so F1 runs twice: F1all strips every fence; F1own strips only the fence around the extracted block. D1 applies at turn≥2.

## Counterexample: one format class decides the verdict
Five shape classes of `raw` (fence regex `grader.py:122`): FJ1, one ```json block on one line (1296) · FJM, one block over several lines (492) · MULTI, ≥2 fenced blocks (31) · DANGLE, bare JSON plus a dangling closing ``` (57) · BARE, no fence (88).
F1own, scored per record, is 1802/1819 = 0.9907, CP95 [0.9851, 0.9945] → **PASS**. All 17 non-invariant records are MULTI:
- MULTI is 31 of the 32 r8 B-cell records (8 pids). The B-cell prompt makes the model print one block per operation ("After operation N:").
- In MULTI's baseline-PASS stratum, F1own is 0/17, CP95 [0, 0.1951] → FAIL. With the last fence stripped, `blocks[-1]` becomes the operation-9 block. At results.jsonl:223 the extractor returns truth[-2], not the wanted state.
- The verdict depends only on MULTI's share; the grader never changes. At MULTI's share of 1.7% it is PASS. At 8.0% it is INDETERMINATE (1858/1943 [0.9462, 0.9649]). At 12.2% it is FAIL (1900/2036 [0.9215, 0.9437]).
- Drop round 8 and the result is 1637/1637 PASS, with no signal at all. F1all gives 1876/1876 PASS. The two F1 readings differ only inside MULTI.

## Why per-record CP95 is mis-specified for this data
1. **Outcomes are fixed by class and stratum.** In the family × class × baseline-stratum table, every cell is 0% or 100% (for example F3: FJ1/P 710/710 … BARE/F 79/79). The only exceptions are D1 no-op coincidences where the previous truth equals `want`: P-stratum 5/914, F-stratum 14 flips. No within-cell Bernoulli variation exists, so the per-record rate is just the weight of the failing cells.
2. **Format is a property of the conversation, not the record.**
   - Adjacent turns in a (file, cell, pid) conversation share a class in 1309/1310 pairs (0.9992). If turns were independent within file×cell the expected rate is 0.5657.
   - P(next turn is DANGLE | this turn is DANGLE) = 37/37, against a 0.029 population share. BARE is 52/52 and FJM 308/308.
   - The one switch is results-r12.jsonl:4047→4048 (A-INC pid 263, FJ1→DANGLE). The format then stays fixed for the rest of the conversation.
   - Within-conversation intraclass correlation (ICC) of class: 0.997 / 1.000 / 0.976 for FJ1 / FJM / DANGLE, a design effect (DEFF) of ≈3.0. The D1 outcome has ICC 0.657 and DEFF 2.54.
3. **Shared content means duplicated inputs.**
   - The 1964 records hold 1451 distinct (raw, want, grader) inputs. 807 records sit in 294 byte-identical groups of up to 7.
   - 273 of 320 r11 records are byte-identical (cell, pid, turn, raw) to an r12 record. Both rounds use pids 201–264 with identical truth (64/64 metas) at temperature 0.2 (results-r11.jsonl:1, results-r12.jsonl:1).
   - The 16 C-cell records contain 5 distinct raws.
4. **One model.** The r11 and r12 descriptor records each name one model, Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS. The class mix reflects that model's habits, not a designed format sample.
5. **MP invariance pools a stratum that carries almost no information.** 943/1964 records are baseline FAIL.
   - D1 is 829/1752 = 0.4732 (FAIL), but the strata are P 5/914 versus F 824/838.
   - The D1 rate tracks the baseline-FAIL share: r8 0.2917 vs 0.292, r9 0.4196 vs 0.402, r11 0.5656 vs 0.575, r12 0.4717 vs 0.478. The seq T-cells give 0.8958 [0.8501, 0.9314] against a FAIL share of 0.929.
   - With exact-match graders, a perturbed wrong answer stays wrong. The F stratum alone, 824/838 [0.9721, 0.9908], is a D1 PASS: a population of only wrong answers would PASS D1 with the same last-block extractor.
6. **G1/G2 restate a theorem.** For grade_state and grade_seq, sensitivity means `got == want` (`grader.py:225`, `:2121`), so 1008/1008 [0.9963, 1] repeats one proof. grade_c is the only non-tautological case: 13/13 [0.7529, 1] → INDETERMINATE, from ≤5 distinct raws.

## Same data, different units (record → conversation → class → min-class rule)
The min-class rule uses the baseline-PASS stratum with conversation units:
- F1all: PASS [lo 0.9980] → PASS [lo 0.9940] → 4/4 INDETERMINATE [lo 0.3976] → INDETERMINATE (MULTI 17/17 lo 0.805; DANGLE 7/7 lo 0.590)
- F1own: PASS [lo 0.9851] → PASS, 582/599 [lo 0.9549] → 2/3 INDETERMINATE → **FAIL** (MULTI 0/17)
- F2, F3, F4, F5, F6, F7: PASS → PASS → INDETERMINATE (lo 0.29–0.48) → INDETERMINATE (weakest observed cell lo 0.541–0.805)
- D1: FAIL at every level. G1/G2: PASS → PASS → 5/5 INDETERMINATE → INDETERMINATE (state/seq hold by construction)

Six classes have 0 records: a bare ``` opener, ```JSON, CRLF, prose containing brackets, same-type nesting deeper than 2 (the limit of the fallback regex at `grader.py:128`), and an unparseable raw. Any F-family PASS therefore covers FJ1 and FJM only (conversation-level lo 0.979 and 0.954).

## Impacted axes
- **Novelty/coverage:** the observable "families with an interval verdict, 0→10" counts per-record PASS verdicts. Those measure class weights, not format robustness, and they hide F1own's real MULTI failure.
- **Calibration:** CP95 overstates precision by DEFF≈3 plus the duplicated inputs. P1–P7 would be scored against inflated PASS events.

## Smallest safe correction (a fixable reporting defect, not a judge-level tradeoff)
File it as `## Amendment N` before any ExecPerturbCore output is read, and state that this critic run informed it.
- (a) Add `fmt_class(raw)` ∈ {FJ1, FJM, MULTI, DANGLE, BARE}, plus a list of unobserved classes. `family_stats` gains `by_class[cls][P|F]={n,k,convs,inputs}`, and `--summary` gains one `CLASS` line per cell.
- (b) For MP families, use baseline-PASS records as the verdict denominator. Print the FAIL stratum separately and never pool it.
- (c) Use the conversation (file, cell, pid) as the CP95 unit after collapsing byte-identical (raw, want) inputs. Print the cluster count next to the record count.
- (d) Family verdict = the minimum over observed class cells; unobserved classes are UNTESTED. Keep the per-record line, labelled as a census rate.
- (e) Pin F1 to one reading, or report both F1all and F1own. Report G1/G2 for state/seq as "by construction" and give a data verdict only on grade_c.

This correction follows existing practice; it is not a novelty claim. Miller, "Adding Error Bars to Evals" (https://arxiv.org/html/2411.00640v1 §2.2, fetched 2026-10-21): "scores within a cluster are perfectly correlated (in which case each cluster acts as a single independent observation)". The paper also recommends "including the cluster count alongside the question count".
If this is not corrected, the canonical judge should not accept per-record PASS as evidence of format robustness.
Installs: none. Wrote only this report; scratch is in /tmp/critindep/.

VERDICT: Independence fails. Outcomes are fixed by format class, the class is a property of the conversation (ICC≈1), and inputs are duplicated (1964→1451). F1own's per-record PASS hides a MULTI 0/17 FAIL that a share shift flips, so report by format class × baseline stratum with conversation units and a min-class verdict.
