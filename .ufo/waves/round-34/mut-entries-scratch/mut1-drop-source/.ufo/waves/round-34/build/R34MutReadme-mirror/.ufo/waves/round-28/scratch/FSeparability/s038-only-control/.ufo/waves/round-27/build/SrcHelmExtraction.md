# SrcHelmExtraction: HELM post-processing before exact match (round 27, C1 sourcing)

Pin: stanford-crfm/helm @63754d05db6f874e41a395880fb573890a13e791 (HEAD, committed 2026-06-05T13:23:33-07:00; `git clone --depth 1` into /tmp/r27-helm-src/helm, scratch; `git status` clean; accessed 2026-10-21). Paths are relative to `src/helm/`. Lane tree read-only; this report is the only file written.
Axes: novelty (HELM label to canonical construct to E0-E8, judged); source pinning; population exposure (census of the four pinned files).

## 1. Exact-match path performs no JSON extraction
- `benchmark/metrics/evaluate_reference_metrics.py:505` `preds=[completion.text.strip() ...]`; `:67-71` `exact_match` is `gold.strip()==pred.strip()`, empty pred gives 0; `:74-78` quasi normalizes both sides (`:43-64`); `:92-110` prefix is `pred.strip().startswith(gold.strip())`. Leniency lives in the grader (normalize, prefix), not in extraction: the same separation the lane freezes (graders fixed).
- grep `(?i)json|loads` over evaluate_reference_metrics.py, basic_metrics.py, adaptation/: no matches. grep `raw_decode|JSONDecoder` over src/helm: no matches.
- Quote: "return 1 if gold.strip() == pred.strip() else 0" (https://github.com/stanford-crfm/helm/blob/63754d05db6f874e41a395880fb573890a13e791/src/helm/benchmark/metrics/evaluate_reference_metrics.py#L71; accessed 2026-10-21).

## 2. Pre-metric transforms, in execution order
1. Provider output_processor: `clients/openai_client.py:361-362` applies `metrics/output_processors.py:4-15` `remove_deepseek_r1_thinking` (greedy `<think>.*</think>` with DOTALL; unclosed `<think>` gives ""). Set by `config/model_deployments.yaml:245,418`.
2. Stop cut: `clients/openai_client.py:393` calls `clients/client.py:51-133` `truncate_sequence`. Each stop, in list order, cuts at `text.index(stop)` (first occurrence; `:79-82`). Same cut in `truncate_and_tokenize_response_text` (`client.py:136-194`, `:169-172`), then a max_tokens cut (`:179-192`).
- Quote: "This method is unsafe and may produce warnings or incorrect results." (https://github.com/stanford-crfm/helm/blob/63754d05db6f874e41a395880fb573890a13e791/src/helm/clients/client.py#L62; accessed 2026-10-21).
3. Metric prep: `evaluate_reference_metrics.py:503-505` sorts completions by -logprob, then `.strip()`.
4. Output mapping (joint MC only): `:510-512` calls `_apply_output_mapping_pattern` (`:400-407`), which is a first `re.search`; no match gives ""; group(1) if groups else group(0); then dict lookup (`:513`).
- Quote: "If the pattern has no group, the output mapping will be applied to the first match." (https://github.com/stanford-crfm/helm/blob/63754d05db6f874e41a395880fb573890a13e791/src/helm/benchmark/adaptation/adapter_spec.py#L150; accessed 2026-10-21).
5. Score: `:450` `score_1 = max(... preds[0] ...)` is the top-logprob completion; `@k` runs over all preds (`:451`, `:454-455`).
- Stop defaults: `benchmark/adaptation/common_adapter_specs.py:257-258` (generation: none) vs `:314-315` (`["\n"]`). Display-only copy of step 4: `benchmark/presentation/run_display.py:268-272`. `ProcessOutputRunExpander` (`benchmark/run_expander.py:1583-1605`, registered `:1634`) has no other reference under src/helm.

## 3. Last/first-match extractors (non-JSON targets)
- `exact_match_indicator` `:131-142`: `pred.split(indicator)[-1]`, default " " gives the last token; used by `benchmark/run_specs/classic_run_specs.py:834` (dyck) and `lite_run_specs.py:154` (gsm).
- `final_number_exact_match` `:145-161`: `re.findall(r"-?[\d,]+(?:.\d+)?")[-1]` (last number; unescaped `.`). Pinned by `benchmark/metrics/test_evaluate_reference_metrics.py:30`.
- `benchmark/scenarios/math_scenario.py:41-70` last `\boxed`/`\fbox`; `:253-262` `get_answer`: absent gives None, no fallback; `:288-293` `is_equiv_chain_of_thought`.
- `benchmark/metrics/gpqa_chain_of_thought_metric.py:12-44`: four `re.search` patterns in priority order, first hit wins; run unstripped on `completions[0].text` (`:85-88`). Pattern 2 (`:29`) escapes its brackets, so it matches the literal `[aA]nswer:`.

## 4. Fence/brace extractors outside the exact-match path
- `benchmark/metrics/codeinsights_code_evaluation_metrics.py:261-264` (and `codeinsights_correct_code_metrics.py:333-335`): `re.findall(r"```(?:c\+\+)?\n(.*?)```", DOTALL)`, then `code_blocks[0]` (first fence); no fence keeps the raw text.
- `codeinsights_code_evaluation_metrics.py:143-148` `strip_code_fence` deletes every opener `^```\w*\n` and closer, keeping prose.
- `benchmark/annotation/financebench_annotator.py:68-74`: `find("{")` to `rfind("}")` as one slice, then `json.loads`; no fallback (`:75-78`).
- Quote: "This strips everything outside the outermost {} brackets." (https://github.com/stanford-crfm/helm/blob/63754d05db6f874e41a395880fb573890a13e791/src/helm/benchmark/annotation/financebench_annotator.py#L69; accessed 2026-10-21).
- `benchmark/annotation/image2struct/webpage_compiler_annotator.py:31-34,63-68` (and `latex_compiler_annotator.py:23-26,44-49`): DELIMITERS cascade `("```json","```")` then `("```","```")`; first opener with a closer after it; else whole text.
- `benchmark/metrics/ifeval/instructions.py:899-913` `JsonFormat.check_following`: strip; drop one ```json/```Json/```JSON/``` prefix; drop one ``` suffix; `json.loads` gives bool.
- `benchmark/annotation/czech_bank_qa_annotator.py:73-74` deletes all ```sql and ``` markers.

## 5. Mapping to E0-E8 (claims :37-45) and HELM label to construct
lane | HELM counterpart | verdict
E0 last fence then last bare | none | no mapping
E1 first fence + bare-last | codeinsights :263 (first fence, no fallback); webpage DELIMITERS | nearest, not exact
E2 bare-last | :140 `[-1]`; :159 `[-1]`; math :46 rfind | ordering analog only
E3 bare-first | :401 re.search; gpqa :24; adapter_spec.py:150 | ordering analog only (regex, not JSON)
E4 strict-whole | :505 + :67-71 (candidate and empty-to-0 rule); ifeval :900-908 adds outer-fence unwrap | analog; unwrap variant not in E0-E8
E5 fence-only, no fallback | math get_answer :253-262 (last span, None if absent) | analog only (LaTeX)
E6 any-label fence | strip_code_fence :146 drops any `\w*` label, keeps prose | partial only
E7 / E8 decode first / last | 0 raw_decode or JSONDecoder hits | no mapping
Label to construct (novelty read-out): `exact_match` is whole-output equality (evaluate_reference_metrics.py:460 to :67) but also the MC tie-split fraction (basic_metrics.py:342-347): one label, two constructs. `quasi_exact_match` and `prefix_exact_match` are grader-side (no E). `exact_match_indicator` is last-token (E2/E8 ordering). `final_number_exact_match` is last-number. `math_equiv_chain_of_thought` (:471) is last boxed, no fallback. `chain_of_thought_correctness` (gpqa:103) is an ordered regex cascade (no E).
Non-E constructs (candidates only; frozen table not edited; any addition is an amendment): N1 think-block removal (output_processors.py:4-15); N2 stop-string first-occurrence cut (client.py:79-82; default "\n" at common_adapter_specs.py:314-315); N3 outermost-brace span (financebench :70-74); N4 first fence with raw-text fallback (codeinsights :261-264); N5 ordered regex cascade (gpqa :23-41); N6 logprob-ranked candidate (evaluate_reference_metrics.py:504-505, :450); N7 IFEval outer-fence unwrap (ifeval :900-908); N8 json-label-priority delimiter cascade (webpage :31-34).

## 6. Population exposure (census, eval kernel, read-only)
Four pinned files (corpus/evidence/round{8-horizon,9-replication,11-power,12-ladder}): 6139 rows; 1964 with raw and ok (population candidates, plans/grader_perturb.py:216-218); 1021 stored ok=true; 1876 of 1964 raw contain a ``` fence.
- `<think>` in raw: 0 of 1964, so N1 is unexercised.
- Rows with any key matching stop, completions, choices, or num_out: 0, so N2's setting is not recorded and cannot be replayed (2 rows carry a bare key `n`, which is not a stop setting).
- Multi-completion rows: 0, so N6 is unexercised (one response per record).

## 7. Sources, gaps, and scope
- corpus/SOURCES.md has no HELM row (grep helm|crfm|stanford gives 0). Candidate for the integrator: stanford-crfm/helm @63754d05, accessed 2026-10-21, quote in section 1. Not written (non-writer seat).
- Prior-art read-out for C1: HELM applies first-match, last-match, and first-occurrence stop cuts; no inspected code path runs two extraction policies over the same outputs (grep-based, not exhaustive). No score claim: this is source-level evidence, and the +1 gate (claims :73-78) also needs publications and critic agreement.
- Not inspected: extract sites beyond the grep patterns; HELM tests not run.
Installs: none (git 2.56.0 pre-present at /usr/bin/git; no package transactions).
VERDICT: HELM implements none of E0-E8 and its exact-match path does no JSON extraction; nearest analogs are E4 (whole-output candidate) and E2/E3 (ordering), with E1/E5 only nearest; eight non-E constructs (N1-N8) are catalogued, and N1, N2 (config absent), and N6 are unexercised on the frozen 1964.
