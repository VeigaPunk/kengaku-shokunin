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

S057 adds the narrower comparison scope for that reopened paper, leaving S044's original abstract-only row
unchanged. URL https://arxiv.org/pdf/2405.11874v3, accessed2026-10-21, §5.3 Setup PDFp9:
“we replicated only the RegEx methods on each framework and ensured consistency in other settings.”
Opening receipt `.ufo/waves/round-27/build/SrcXFinderReopen.md`; §5.3 does not explicitly document item-level
saved-response pairing, and some table denominators remain unresolved. Broad extractor-dependence prior art
does not require claiming those unresolved details established. Nine new tierA rows total S049–S057.

## Independent-reread corrections (opened 2026-10-21, before admission)

- S058 supersedes S050's blanket no-hit reason, not its ordering scope. URL
  https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py,
  no-match return branch:122: `reason="no_response" if empty else "invalid_response_format"`.
  `scorer/_common.py:16–30` defines empty/whitespace via `not completion.strip()`.
  Independent opening FSourceS050 plus L1 directly reopened pinned raw code; corrected draft states exception.
- S059 extends S053's §2 anchor to the candidate's numeric-grammar statement. URL
  https://www.rfc-editor.org/rfc/rfc8259 §6 Numbers, txt377–378:
  “Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted.”
  Opening RowRFC8259 plus independent FSourceS053; text SHA25661a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7.
- S049 default-selector declaration is extraction.py:25, not27; operative code47–49 and quote remain correct.
  FSourceS049 independently located it. Earlier row retained; candidate provenance corrected to25.

Total additions S049–S059:11 rows, all tierA. No source or quote is inferred from a planned/future reread.

S060 retains the opened but rejected repair-policy candidate. URL https://pypi.org/project/json-repair/,
accessed2026-10-21, version0.64.1, PyPI summary: “A package to repair broken json strings”.
Opening/probes `.ufo/waves/round-27/build/SrcJsonRepair.md`; wheel SHA256
1e1022f8d9b5a24433f7e28c2ee5c4ef42256e11ff0eef8abf7cad17fc8b9e0a.
TierB tool self-description/probes, rejected only for this frozen stdlib policy set. Flip: preregistered
pinned repair-specific experiment with truth-sensitive controls and separate oracle. It is not an E9.
Final additions S049–S060:12 rows (11A/1B); earlier11-row snapshot is superseded.
