# FEntryNumbers — Q10 numeric reread

Identity: **FEntryNumbers**, not candidate writer KengakuR27. Observed private-clone base `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (`git rev-parse HEAD`, exit 0; initially clean). I read all 110 lines of the frozen draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`, including its full metadata line. The proposed canonical path is `corpus/knowledge/extraction-policy-comparison.md`; it is absent at this frozen revision (`test -e corpus/knowledge/extraction-policy-comparison.md`, exit 1), consistent with the disclosed deferred admission. Round-27 lesson lines 24–30 records that status. This is a reread of the candidate content, not an admitted-corpus entry.

LSP status: unavailable in this environment. `read xd://lsp` returned “No such tool: xd://lsp”; no LSP device is mounted. I made no caller/definition/diagnostics claims from grep; the numeric findings below use source line reads and offline record replay.

## Reproduction

- `python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FEntryNumbers --summary` — exit 0; reproduced E0..E8 and TOTAL; frozen summary receipt agrees at `corpus/evidence/round27-calibration/policy-build-summary.txt:2-74`.
- `python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FEntryNumbers --json` — exit 0; all four input pins match and `defects=[]` in output. Full independent structural comparison of policies, CP95, strata, files, cells, shifts, matrix and totals was exact.
- `python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FEntryNumbers --selftest` — exit 0; `SELFTEST total policies=9 cases=58 killed=9 failures=0`.
- `python3 plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FEntryNumbers` — exit 0; every per-policy agree/PF/FP/None count matches (also recorded at `corpus/evidence/round27-calibration/policy-build-oracle.txt:2-10`).
- `python3 /tmp/kengaku-r27-FEntryNumbers/independent_recheck.py` — exit 0. This standalone stdlib replay independently verifies all 1,964 records and rederived truths, implements E0–E8 without importing the comparator/oracle/production grader, computes CP95, then exact-compares all result structures with production JSON and oracle counts:
  `INDEPENDENT PASS population=1964 pins=4 E0=1964/1964 compared=15712 disagreements=1089 policies_with_flips=5 production_json=exact oracle=exact strata=45 files=36 cells=216 matrix=9x9 no_FP=9/9`.

## Numbers checked against candidate

Candidate draft `:25-28`, `:58-78`, `:82-91`; frozen claims `plans/round-27-claims.md:29-56`; reproduced output in `policy-build-summary.txt:2-74`.

| id | agree/1964 | PF / FP | None | PASS | delta pp | exact CP95 agree interval |
|---|---:|---:|---:|---:|---:|---|
| E0 | 1964 | 0 / 0 | 0 | 1021 | +0.00 | [0.998124, 1.000000] |
| E1 | 1947 | 17 / 0 | 0 | 1004 | -0.87 | [0.986177, 0.994950] |
| E2 | 1964 | 0 / 0 | 0 | 1021 | +0.00 | [0.998124, 1.000000] |
| E3 | 1947 | 17 / 0 | 0 | 1004 | -0.87 | [0.986177, 0.994950] |
| E4 | 952 | 1012 / 0 | 1876 | 9 | -51.53 | [0.462405, 0.507091] |
| E5 | 1938 | 26 / 0 | 145 | 995 | -1.32 | [0.980663, 0.991335] |
| E6 | 1964 | 0 / 0 | 0 | 1021 | +0.00 | [0.998124, 1.000000] |
| E7 | 1947 | 17 / 0 | 0 | 1004 | -0.87 | [0.986177, 0.994950] |
| E8 | 1964 | 0 / 0 | 0 | 1021 | +0.00 | [0.998124, 1.000000] |

All 45 format-stratum `agree/n` entries match: E0/E2/E6/E8 = FJ1 1296/1296, FJM 492/492, MULTI 31/31, DANGLE 57/57, BARE 88/88; E1/E3/E7 = 1296/1296, 492/492, 14/31, 57/57, 88/88; E4 = 586/1296, 224/492, 14/31, 40/57, 88/88; E5 = 1296/1296, 492/492, 31/31, 40/57, 79/88. In particular E1/E3/E7 have 14/31 MULTI agreement (candidate `:75`).

All per-file rates match in the full result comparison. Pass counts by file (r8 / r9 / r11 / r12): E0/E2/E6/E8 = 125/188, 75/128, 136/320, 685/1328; E1/E3/E7 = 108/188, 75/128, 136/320, 685/1328; E4 = 0/188, 0/128, 0/320, 9/1328; E5 = 123/188, 75/128, 132/320, 665/1328. All 216 per-cell entries also match.

`1089` is the sum of paired disagreement events over the eight alternative policies, not unique responses: `15712` comparisons, `17+17+1012+26+17=1089`, across five flip-bearing policies. The full 9×9 matrix matches (`policy-build-summary.txt:64-73`); E1/E3/E7 share the same 17 affected MULTI records. Every policy has `flip_fp=0` (candidate `:70-73`). E5 has 26 PASS→FAIL fallback losses: 17 DANGLE and 9 BARE; E5 extracts None on 145 records. Maximum cell shifts match all eight reported shifts: E1/E3/E7 75.00pp at `round8-horizon/results.jsonl:B-clean-hint` (6/8 to 0/8); E4 100.00pp at `C-MONO`; E5 6.67pp at `A-CKPT`; E2/E6/E8 0.00pp. Thus candidate `:75-78` is numerically accurate.

## Findings and residual scope

No actionable Q10 numeric discrepancy. The CP95 intervals are reproduced as nominal descriptive intervals for this fixed, correlated population—not independent future-response guarantees. Oracle/source independence remains only as disclosed in candidate `:100-104` and lesson `:71-74`; this reread independently implemented a record-level check but does not claim source-blind policy authorship. I did not assess novelty/prior-art merits, P4 assertions, Q15 authority, or admission/Q13–Q14 closure.

Installs: none.

VERDICT: Scoped Q10 numeric PASS for the frozen draft; no numeric finding. This does not admit the candidate or assert whole-round correctness.

## Corrected-candidate source and contract reread

Reread the entire corrected draft at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (snapshot `7BF3`, 111 lines). Canonical proposed path: `corpus/knowledge/extraction-policy-comparison.md`. Identity remains **FEntryNumbers**, not candidate writer KengakuR27. The corrected numeric table at `:59-79` is unchanged from the prior independent record-level replay. No outside/non-author closure is claimed or relied upon.

Reopened S049–S055, S057, and the additions S058/S059. S049 now correctly points to default `group_select=0` at extraction.py:25 and selection at :47-49. S058’s `_pattern.py` no-match branch and `_common.py:16-30` support `no_response` for empty/whitespace and `invalid_response_format` for nonempty no-hit output; draft `:18-20` is corrected. S051 parses the whole sampled completion with `json.loads(sampled)` without strip; S052 documents `raw_decode` with trailing extraneous data, not the scan/selection algorithm. S053 §2 supports the JSON whitespace distinction; S059 §6 excludes Infinity/NaN. S054’s CommonMark §4.5 supports the info-string/fence-boundary caveat. These claims are accurate.

Prompt contract checked directly: r8 `horizon.py:18-23`, r9 `replicate.py:18-25`, r11 `probe_r11.py:27-34`, r12 `probe_r12.py:31-38` use the same system instruction and prepend it to calls, including the `ok` exception. The E4 rejection as model-accuracy evidence is therefore sound for compliant fenced answers; E5 remains non-exact because it accepts multiple fences/prose. `round-27.md:31-34`’s reject reasons also align with the checked evidence: prior art in kind, prompt mismatch for E4, no iid future guarantee from this deterministic/correlated population, and E7/E8’s untrusted-input cost. The 285s observation is in `build/SentRegexCost.md:35,39`.

## Remaining source/scope findings

- **Low — S055 fallback is misstated.** Draft `:19-21` says simple-evals `math_eval` uses first `Answer:` matches “with task-specific fallback.” Reopened S055 `math_eval.py:53-55` uses `re.search(ANSWER_PATTERN, response_text)` and assigns `match.group(1) if match else None`; it shows no fallback or retry. `common.py` defines a regex, not a fallback. Narrow this to first `re.search` match / `None` if absent.
- **Low — S057 caveat is omitted from the candidate body.** Draft `:16-22` uses xFinder as prior art for extractor-dependent scores/rankings. The paper’s §5.3 setup says it replicated only framework RegEx methods; the source gate `corpus/evidence/round27-sources/gate.md:30-35` explicitly records that item-level saved-response pairing is not documented and some denominators are unresolved. Add that limit at the prior-art statement so “in kind” cannot be read as the same paired fixed-response measurement. This does not erase the broad prior-art support or change the held-7 conclusion.

## E6 follow-up and gaps

The current `parser_policy_compare.py:388-391` E6 targeted `PROBES` block still has three cases, matching the frozen clone; `policy_cases.py:58-66` has seven E6 hand cases. I did not find a newly added targeted `PROBES` case in the corrected-tree read. I did not execute the live lane: the prior selftest and independent metrics run were on the permitted private clone at the frozen base. The corrected table was reread and matches those independent metrics, but the purported follow-up selftest has no current-tree run in this report.

LSP remains unavailable (`read xd://lsp` reported no mounted device); no semantic proof is attributed to grep. No installs.

VERDICT: PARTIAL — the corrected Q10 numbers still pass the independent reread, but the S055 fallback wording and missing S057 pairing/denominator caveat are actionable source-scope corrections; this is not an admission or an outside closure.

## Final corrected-candidate reread

This append preserves the preceding PARTIAL record. I reread all 114 lines of corrected draft snapshot `A42E`, including the corrected numeric table (`:62-82`), source clauses (`:16-25`), and limits. Canonical proposed path: `corpus/knowledge/extraction-policy-comparison.md`. Identity remains **FEntryNumbers**, not candidate writer KengakuR27.

Both prior findings are closed in this snapshot: S055 now says `math_eval.py:53-54` uses the first `Answer:` match and returns None on no match (`:20-21`); S057’s undocumented item-level pairing and unresolved denominators are explicit at `:23-25`. Reopened S058 source again: `_pattern.py:122` returns `no_response` iff `empty`, otherwise `invalid_response_format`; `_common.py:16-30` defines empty/whitespace as `not completion.strip()`. The candidate’s no-response exception at `:18-20` is accurate.

Numeric table values remain identical to the independent record-level replay and summary receipt `corpus/evidence/round27-calibration/policy-build-summary.txt:2-74`. In the private clone, after applying the E6 hand case/probe/extra-mutant wiring read from the current source, `python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FEntryNumbers --selftest` exited 0: `SELFTEST KILLED E6 mutant=E6-first-any-label-fence by=two-distinct-any-label-fences`; final `SELFTEST total policies=9 cases=59 mutants=10 killed=10 failures=0`. The follow-on `--summary` run in that clone exited 0 with `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`. These runs were sandboxed in the private clone, not the live lane.

Scope remains limited to Q10; no P4/Q15/admission judgment or outside/non-author closure is claimed. Installs: none.

VERDICT: PASS — scoped Q10 corrected-candidate numeric and source reread; prior source findings are closed. This does not admit the candidate or claim whole-round correctness.
