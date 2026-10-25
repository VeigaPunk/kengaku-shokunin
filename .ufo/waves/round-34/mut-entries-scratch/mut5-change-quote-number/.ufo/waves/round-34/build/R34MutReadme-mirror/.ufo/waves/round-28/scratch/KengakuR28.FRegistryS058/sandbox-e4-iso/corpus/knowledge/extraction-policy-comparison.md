source: S049 lm-evaluation-harness https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/filters/extraction.py:25,47–49; S958 inspect_ai pattern() https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py:62–79,119–124 and scorer/_common.py:16–30; S051 openai/evals https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py:76–83; S052 https://docs.python.org/3/library/json.html#json.JSONDecoder.raw_decode; S053/S059 https://www.rfc-editor.org/rfc/rfc8259 §2/§6; S054 https://spec.commonmark.org/0.31.2/#fenced-code-blocks §4.5; S055 https://github.com/openai/simple-evals/tree/652c89d0ca9df547706735883097e9537d40dc47 math_eval.py:53; S056 own-work plans/parser_policy_compare.py; S057 xFinder https://arxiv.org/abs/2405.11874 v3 §5.1/§5.3
verified-at: 2026-10-21 (source openings and offline byte-pinned response replay; no live model requests)
recheck: 90d — rerun python3 plans/parser_policy_compare.py --summary and --selftest; reopen source anchors in lessons/round-27.md Gate
writer: KengakuR27

# Extraction-policy comparison — fixed responses can receive different verdicts

## Claim, scope and prior art

Holding the response, expected answer and grader fixed does not hold the verdict fixed when the parser changes.
This entry compares nine explicitly defined parsers on the lane's pinned responses. Round 26 instead varied
response format under one fixed parser (`knowledge/grader-perturbation-audit.md`). Neither experiment establishes
which parser best recovers the model's intended answer. No new model capability, new trials, or independent
future-response precision is claimed.

This is a lane-specific measurement, **not a new method**. xFinder (S057, reopened this round) already measures
extractor-dependent scores and rankings. lm-eval (S049) exposes first/last `group_select` over regex matches;
inspect_ai `pattern()` (S958, correcting S050) takes a first regex hit; on no hit it reports
`invalid_response_format` for nonempty output or `no_response` for empty/whitespace output. Simple-evals
(S055 math_eval.py:53–54) uses a first `Answer:` match and returns None on no match. These are ordering precedents,
not faithful implementations of our JSON policies. openai/evals JsonMatch (S051) parses the whole completion;
E4 below is that policy class with a disclosed `strip()` difference. Novelty score stays 7.
xFinder §5.3 does not explicitly document item-level saved-response pairing, and some aggregate denominators
remain unresolved (S057). Its broad extractor-dependent outcome result is prior art; it is not treated as
proof of this study's paired-record provenance, exact rule variants or comparable denominators in every table.

## Frozen population and policies

The same four SHA-256-pinned input files and **1964 raw+ok records** as round 26 are loaded through
`plans/grader_perturb.py:build_population`. All 1964 stored E0 verdicts rederive: **1021 PASS / 943 FAIL**,
0 excluded. The baseline source files and `grader.py` remain unchanged. Formats: FJ1 1296, FJM 492,
MULTI 31, DANGLE 57, BARE 88. These are extractor-format labels, not independent response samples.

Exact definitions are frozen in `plans/round-27-claims.md` and Amendment 1:

| id | parser |
|---|---|
| E0 | Lane: last matched JSON/unlabelled fence if it parses, otherwise last parseable bare-regex candidate |
| E1 | First matched fence, otherwise whole-response bare-last fallback; not first parseable fence |
| E2 | Bare-last: non-overlapping original raw-string regex matches, last parseable candidate |
| E3 | Bare-first: same candidates, first parseable candidate |
| E4 | Whole stripped output through json.loads, otherwise None |
| E5 | Last matched fence only; failed/missing fence returns None, no fallback |
| E6 | Any-label-fence using the exact frozen restricted label regex, then bare-last fallback |
| E7 | Scan brace/bracket positions left to right; first successful JSONDecoder.raw_decode |
| E8 | Same scan but last successful top-level span; skip contained starts in already-decoded spans |

Successful JSON null returns None without triggering a fallback. Bare regex matching is the lane's bounded
nesting pattern, not arbitrary JSON parsing. E7/E8 use Python's decoder primitive (S052), but their scan and
selection rules are lane-defined. E6 is not a CommonMark parser: it omits valid info strings and fence-length
rules (S054). E4's Unicode `strip()` is broader than RFC 8259 whitespace (S053); comparison with source-exact
json.loads(raw) found no difference in the pinned population. Python also accepts NaN/Infinity by default,
unlike RFC8259 §6 (S059): “strict-whole” means whole-output Python decoding, not RFC-strict syntax. These policies are
research counterfactuals, not complete alternate harness implementations.

## Observed finite-population results

Command: `python3 plans/parser_policy_compare.py --summary` (same metrics in --json).
Agreement compares each policy's boolean verdict with stored E0; flips are PASS→FAIL / FAIL→PASS.
CP95 is nominal/descriptive on this finite, correlated corpus, not a sampling guarantee for future responses.

| policy | agree / 1964 | flips PF / FP | extracted None | PASS | delta vs E0 (pp) | nominal agreement CP95 |
|---|---:|---:|---:|---:|---:|---|
| E0 | 1964 | 0 / 0 | 0 | 1021 | 0.00 | [0.998124,1.000000] |
| E1 | 1947 | 17 / 0 | 0 | 1004 | -0.87 | [0.986177,0.994950] |
| E2 | 1964 | 0 / 0 | 0 | 1021 | 0.00 | [0.998124,1.000000] |
| E3 | 1947 | 17 / 0 | 0 | 1004 | -0.87 | [0.986177,0.994950] |
| E4 | 952 | 1012 / 0 | 1876 | 9 | -51.53 | [0.462405,0.507091] |
| E5 | 1938 | 26 / 0 | 145 | 995 | -1.32 | [0.980663,0.991335] |
| E6 | 1964 | 0 / 0 | 0 | 1021 | 0.00 | [0.998124,1.000000] |
| E7 | 1947 | 17 / 0 | 0 | 1004 | -0.87 | [0.986177,0.994950] |
| E8 | 1964 | 0 / 0 | 0 | 1021 | 0.00 | [0.998124,1.000000] |

Eight alternative policies give **15712 paired comparisons, 1089 disagreement events across five policies**.
Events are not unique responses: E1/E3/E7 share the same 17 affected records; the full 9×9 matrix is emitted.
No FAIL→PASS recovery occurs in this corpus. Equal verdict vectors do not imply equal extracted objects or
algorithmic equivalence beyond the pinned corpus.

The first-vs-last differences live entirely in MULTI: E1/E3/E7 agreement **14/31**, rather than 1947/1964's
apparently reassuring pool. The largest cell-level PASS-rate shift is **75pp** in r8 B-clean-hint.
E5 removes the fallback: it rejects 17 previously passing DANGLE and nine previously passing BARE records,
26 in total. All other FJ1/FJM/MULTI verdicts remain unchanged under E5.

## Interpretation: instruction compliance is not parser invariance

All four probe scripts carry the system instruction “Reply with exactly one fenced ```json code block and no
other text”, with an exception for 'ok' turns. Therefore E4 strict-whole JSON is **instruction-contradicting**
for compliant fenced answers, not a more faithful measure of model accuracy. Its -51.53pp is a counterfactual
consumer-contract mismatch, not a discovery of 1012 wrong model answers. Vendor constrained-output guarantees
also do not apply: these historical requests did not use a constrained-output mode.

E5 is closer to the requested format but still accepts multiple fences and surrounding prose. None of the
frozen policies enforces exactly one whole-response fence. Do not call E5 instruction-exact. E0's last-fence
choice was historically intentional to avoid illustrative/preamble blocks; r8 B contains scripted multiple
answers. The policy that is appropriate depends on the task contract, not on which maximizes PASS.

## Decision rule, falsifier and limits

When changing an extraction policy, freeze the responses and truths, publish per-record paired flips,
stratify by the format the policy acts on, and separately report prompt-format compliance. Keep the grader
fixed. A large strict-whole delta on fenced prompts is a contract mismatch; an ordering delta in MULTI
requires task-level answer-location semantics before labeling it a grader or model defect.

Falsifier: any changed population pin, E0 replay mismatch, independently reproduced different per-policy
counts, or policy reading the expected answer invalidates the reported measurement. Independent oracle code
is separately implemented but its seat disclosed reading the baseline regex and contextual grader lines;
no claim of source-blind authorship is made. Synthetic edge tests, mutations and source rereads are recorded
in the round's evidence, not implied by this prose.

No transfer claim follows for other models, formats, benchmarks, duplicate-free samples, or future responses.
E7/E8 have superlinear work on repeated unmatched brackets (about 285s for 200K in the sentinel probe).
The CLI is for the byte-pinned population; policy helpers are bounded research functions, not a production
untrusted-input API. Do not deploy them as a network parser. A future parser comparison should register
instruction-exact parsing and independently sampled formats rather than adding those after seeing scores.

## Round28 source-location and authority errata (2026-10-21)

The original provenance header's S049 `extraction.py:25` is superseded by **:27** for
`group_select: int = 0`; the operative47–49 range remains correct. The pinned d6de8164
bytes were reopened in `.ufo/waves/round-28/build/OpenS049.md`. This corrects round27
M61's mistaken “25, not27” reviewer correction, not the original registry anchor.

S050 occurs above only as the superseded reason corrected by S958. Round28 adds this
file to S050's used-by for **literal corrective-reference discoverability**, explicitly
superseding round27's lesson-only indexing decision; it does not revive S050 as support
for the inaccurate blanket no-hit reason. S958 remains the authority for that behavior.

S064 clarifies CommonMark's rule: same fence character type, closing length **at least**
the opening length (not necessarily equal). This leaves the paragraph's “fence-length
rules” limitation true while superseding S054's ambiguous shorthand. S065, Python3.15.1
JSON docs “Infinite and NaN Number Values”, supplies the Python-side authority for default
NaN/infinity acceptance; the RFC S059 supplies only the RFC-side prohibition. The Unicode
strip comparison is a lane inference/runtime comparison, not a quotation from the RFC.

S051 is a whole-output policy-class precedent, not identical exception handling:
upstream JsonMatch catches ValueError, whereas the lane's `_loads` catches broader
exceptions (`build/OpenS051.md`). No new behavior on the frozen response population is
asserted by this disclosure. All original numeric results remain historical measurements.
