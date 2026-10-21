# Round-27 source openings (2026-10-21)

Sources were opened by the named build seats before these rows were written. Quotes below are ≤25 words.
Existing SOURCES contract-v1 uses 11 content columns, 13 split fields including empty edge fields.

| id | URL | location/version | located quote | opening evidence |
|---|---|---|---|---|
| S049 | https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/filters/extraction.py | RegexFilter, extraction.py:47–49; d6de8164; accessed 2026-10-21 | `match = match[self.group_select]` | .ufo/waves/round-27/build/RowGsm8kYaml.md and SrcLmEvalDocs.md; extraction.py SHA-256 eb976bb36d5d3e93faafe6d065678e24b4474e78cd4fce1e730e2b8f49b9fda0 |
| S050 | https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py | pattern() docstring :62–64, v0.3.282 source identical to opened main; accessed 2026-10-21 | “If the pattern contains no capture groups, the full match is compared against the target.” | .ufo/waves/round-27/build/RowInspectPattern.md and SrcInspectJson.md; SHA-256 7974ddb436917ac97f78304ae071eef75115783938358a0578f8d2e30abaae6b |
| S051 | https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py | JsonMatch.eval_sample :80–82; last file-changing commit 4b7a66bd45f06156656e021e170e7574f6cde3f5; accessed 2026-10-21 | “If the sampled string is not valid JSON, it will never match” | .ufo/waves/round-27/build/RowOpenAIEvalsJson.md; SHA-256 6cc971f9a360a89b628595f1de5b030bd38969f2160cca75bcf11ee7aa0795e8 |
| S052 | https://docs.python.org/3/library/json.html#json.JSONDecoder.raw_decode | Python 3.15.0 docs, raw_decode paragraph; accessed 2026-10-21 | “This can be used to decode a JSON document from a string that may have extraneous data at the end.” | .ufo/waves/round-27/build/RowPyRawDecode.md; SHA-256 390c826f16e9d7350d09f87d06bec2d5d2adff8b09fd09c949611054eadfc383 |
| S053 | https://www.rfc-editor.org/rfc/rfc8259 | §2 JSON Grammar; accessed 2026-10-21 | `JSON-text = ws value ws` | .ufo/waves/round-27/build/RowRFC8259.md |
| S054 | https://spec.commonmark.org/0.31.2/#fenced-code-blocks | CommonMark 0.31.2 §4.5; accessed 2026-10-21 | “Closing code fences cannot have info strings” | .ufo/waves/round-27/build/RowCommonMarkFence.md; SHA-256 c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d |
| S055 | https://github.com/openai/simple-evals/tree/652c89d0ca9df547706735883097e9537d40dc47 | math_eval.py:53, commit 652c89d0; accessed 2026-10-21 | `match = re.search(ANSWER_PATTERN, response_text)` | .ufo/waves/round-27/build/RowSimpleEvals.md; math_eval.py SHA-256 845500fb5299620e158f12ae7d8618ca64a50dc69b5535cc793e8498bdcce136 |
| S056 | plans/parser_policy_compare.py | --summary TOTAL, opened/run 2026-10-21 | `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5` | .ufo/waves/round-27/build/ExecPolicyCore.md; rerunnable own-work, not outside validation |

## Curatorial decisions and limits

S049/S050/S055 are real harness extraction references, but only ordering/no-fallback precedents: they do not
implement the lane's JSON policies. S051 grounds the strict-whole policy class; its absence of `.strip()` is
explicitly disclosed. S052 documents decoding and end offsets, not the first/last scan algorithm. S053/S054
define grammar/boundaries, not what an answer grader should select. These limits are part of the sourced claim.

S044 xFinder was reopened this round by SrcXFinderReopen; it already measures extractor-dependent scores and
rankings. SrcPriorArtTooling found fixed-output rescoring and extractor sensitivity published in kind. Novelty
+1 is rejected; no exact nine-policy matrix match is required to recognize prior art. OLMES was opened by
SrcOLMES: the paper defers answer-extraction standardization; later code is ordering precedent, not the full
comparison. No new row is created solely for an unopened or inaccessible lead.
