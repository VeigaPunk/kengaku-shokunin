# SrcBFCL — BFCL checker decode policy vs E4/E5/E6 (round 27, C1 mapping)

Seat KengakuR27.SrcBFCL · leaf scout · read-only · access date 2026-10-21 · only lane file written: this report.
Pin: github.com/ShishirPatil/gorilla @ 6ea57973c7a6097fd7c5915698c54c17c5b1b6c8 (2026-03-23, "[BFCL] Request to add MiniCPM-SALA to the leaderboard (#1315)"). Checker tree: berkeley-function-call-leaderboard/bfcl_eval/ (no bfcl/ path at this commit).
Clone: /tmp/kengaku-r27-SrcBFCL/gorilla (sparse, depth 1). Blob ids: model_handler/utils.py 7abd9a24 · eval_checker/eval_runner.py 2d5c41aa · model_handler/parser/json_parser.py 4924aedf · model_handler/local_inference/hammer.py 4c18b5b9.
Permalink (HTTP 200 on 2026-10-21): https://github.com/ShishirPatil/gorilla/blob/6ea57973c7a6097fd7c5915698c54c17c5b1b6c8/berkeley-function-call-leaderboard/bfcl_eval/model_handler/utils.py

## Findings (path:line at 6ea57973)
F1 Default prompting decoder: whole output, strict; fences trimmed at the edges only, never extracted. utils.py:469-480.
   :474 result = result.strip("`\n ")   :475-476 prepend "[" if no leading "["   :477-478 append "]" if no trailing "]"
   :479 decoded_output = ast_parse(result, language, has_tool_call_tag)
   PYTHON branch utils.py:262-263 ast.parse(cleaned_input, mode="eval"); elements must be Call (:269 assert).
   Callers: local_inference/base_oss_handler.py:67-68; api_inference/claude.py:38-40 (non-FC); gemini.py:57-60 (non-FC; :59 strips "```tool_code\n" and "\n```" first); nvidia.py:32-33; mistral.py:35-44 (non-FC); openai_completion.py:52-61 (non-FC). FC-mode decodes API tool_calls, not text (openai_completion.py:53-59).
F2 Selection constructs exist only on tags or in the JSON branch, never on fences.
   first: utils.py:254 <TOOLCALL> (only if has_tool_call_tag); :284, :293 <functions>; api_inference/nemotron.py:104; parser/json_parser.py:6 lazy first [{...}] span.
   JSON (ret_fmt=json): utils.py:301 greedy \[.*\] = first "[" to last "]"; json_parser.py:12-13 return [] on JSONDecodeError.
   last: qwen.py:188-190 split("</think>") then [-1]; minicpm_fc.py:303 rsplit(tool_call_end, 1).
   all: arch.py:199, functiongemma.py:338, granite_3.py:107, granite_4.py:295, nanbeige_fc.py:210, pelican_vl_fc.py:258, qwen_fc.py:296, phi_fc.py:174.
F3 Per-model fence code is marker/label trimming, whole-output: phi.py:19-23 (cuts leading ```json / ```python); falcon_fc.py:41-42, 70-71; minicpm_fc.py:308-313; hammer.py:97-101: result.replace("```", "") then json.loads, bare except sets result = [] (silent). eval_checker/ has no fence parsing (``` only in multi_turn_utils.py docstrings, :116-124).
F4 Verdict coupling: eval_runner.py:285-292 decode exception sets contain_func_call=False; :292 success = not contain_func_call (irrelevance), so a decode failure PASSes irrelevance; relevance failure is relevance_error:decoder_failed (:313). AST path eval_runner.py:336-346 maps decode exception to ast_decoder:decoder_failed (FAIL).
F5 Interpreter dependence: utils.py:342-345 isinstance(value, ast.NameConstant). [f(x=y)] gives ok1 on CPython 3.11.17 and 3.12.15, but exc:AttributeError on 3.14.8 (attribute absent).

## Probe (real utils.py functions extracted by AST and run unmodified; enums.py:32-41; json_parser.py; E4/E5/E6 from claims text, E0 fence regex grader.py:122, BARE_RE grader.py:128; kernel CPython 3.14.8)
case                  BFCL-PY             BFCL-JSON        E4     E5     E6
A plain-call-list     ok1                 ok0              None   None   None
B call-no-brackets    ok1                 ok0              None   None   None
C bare-fence          ok1                 ok0              None   None   None
D python-fence        exc:SyntaxError     ok0              None   None   None
E prose-prefix        exc:SyntaxError     ok0              None   None   None
F two-bare-fences     exc:SyntaxError     ok0              None   None   None
G two-py-lists        exc:AttributeError  ok0              None   None   None
H json-call-list      exc:AssertionError  exc:KeyError     list1  None   list1
I json-fence-fnparam  exc:SyntaxError     ok1              None   list1  list1
J two-json-lists      exc:SyntaxError     ok1 (call a)     None   None   list1 (call b)
K json-fence-object   exc:SyntaxError     ok0              None   dict1  dict1
L bare-json-object    exc:AssertionError  exc:KeyError     dict1  None   dict1

## Mapping to E4/E5/E6
- E4 (strict-whole, json.loads): CLASS MATCH; exact only for hammer.py:97-101 on fence-free input (by code reading: json.loads of the whole text; failure gives [] not None). The default decoder (F1) is the same construct on Python call grammar, so not exact. Accept sets are disjoint on the probe: BFCL-PY {A,B,C} vs E4 {H,L}.
- E5 (last fenced block, no fallback): none. No BFCL path selects a fenced block; C is accepted by BFCL only through edge trim, and E5 returns None.
- E6 (any-label fence + bare fallback): none. Labelled fences fail the default (D); phi.py label trim is whole-output, not block extraction. On J, BFCL-JSON takes call "a" (first list) while E6 takes call "b" (last candidate).
- E1/E2/E3/E7/E8: no exact match; first-match exists only on tags/JSON spans, with no fallback to later candidates.

## Novelty (judged axis)
- Prior art in kind: whole-output strict (E4 class) and first-match on tags (E1/E3 class) appear in this public harness (F1, F2). No fenced-block extraction (E1/E5/E6) appears anywhere in BFCL.
- Not in E0-E8: (i) Python call grammar with bracket-wrap (F1); (ii) deleting all fence markers before a whole-output parse (hammer.py:97); (iii) silent [] on parse failure and decode-failure-as-PASS on irrelevance (json_parser.py:13, hammer.py:101, eval_runner.py:292); (iv) interpreter-dependent decode (F5). Candidates only; the policy table is frozen and not amended here.
- Effect on the prior-art search (claims lines 73-78): BFCL is a published instance of strict-whole and first-match, but it supplies no verdict-agreement measurement, so it does not by itself justify a +1.

## SOURCES candidate (row data for gate.md; not written by this seat)
S-cand-1 URL: https://github.com/ShishirPatil/gorilla/blob/6ea57973c7a6097fd7c5915698c54c17c5b1b6c8/berkeley-function-call-leaderboard/bfcl_eval/model_handler/utils.py · accessed 2026-10-21 · location utils.py:474-479 · quote: result = result.strip("`\n ") ... decoded_output = ast_parse(result, language, has_tool_call_tag)
S-cand-2 URL: https://github.com/ShishirPatil/gorilla/blob/6ea57973c7a6097fd7c5915698c54c17c5b1b6c8/berkeley-function-call-leaderboard/bfcl_eval/eval_checker/eval_runner.py (HTTP 200) · 2026-10-21 · :292 · quote: success = not contain_func_call
Docs: CONTRIBUTING.md:83-90 fix only the decode_ast output shape, not an extraction rule.

## Installs / writes
- Installs: none. Pre-existing: git 2.56.0; kernel CPython 3.14.8; CPython 3.12.15 and 3.11.17 (~/.local/bin). No package transactions.
- Writes: this report only. Scratch: /tmp/kengaku-r27-SrcBFCL/ (clone and probe).

VERDICT: BFCL's default decoder is whole-output strict with edge-only backtick trim (no fence extraction, no first/last selection): E4 class only (Python grammar; hammer.py is exact E4 on fence-free input), E5 none, E6 none.
