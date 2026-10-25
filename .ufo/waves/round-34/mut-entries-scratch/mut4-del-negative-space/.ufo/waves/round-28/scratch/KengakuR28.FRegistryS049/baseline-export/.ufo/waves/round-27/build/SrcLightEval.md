# SrcLightEval — lighteval extractive-match policies (round 27, C1 source mapping)
Source: https://github.com/huggingface/lighteval/tree/7fa19dc6f53a713ba8bb6541e7ed66dad2e24fd7 (main HEAD at clone; commit 2026-10-06; git describe v0.10.0-182; pyproject 0.13.1.dev0). Accessed 2026-10-21 via `git clone`; paths below are under `src/lighteval/`. Blobs: extractive_match_utils.py da0d718d · dynamic_metrics.py 66ed91c3 · metrics.py 82cfbb70 · normalizations.py ef55681b · tasks/tasks/lcb/codegen_metrics.py e2617ed4. F = triple backtick.

## 1. First or last? LAST by text position, inside a fixed priority order
- Tiers ascend by priority (`metrics/utils/extractive_match_utils.py:599`). Boxed default 55 (:67); `metrics/metrics.py:87,270,393,412` sets 0.
- Within a tier, quote: “# Sort matches by end position (rightmost first) and then by start position (leftmost first)” ([extractive_match_utils.py#L607-L610](https://github.com/huggingface/lighteval/blob/7fa19dc6f53a713ba8bb6541e7ed66dad2e24fd7/src/lighteval/metrics/utils/extractive_match_utils.py#L607-L610), accessed 2026-10-21); actual sort at :608 uses `reverse=True`; source then says “# Try to extract from each match, starting from rightmost” (same location).
- Naming trap: `extraction_mode="first_match"` (:622-623) stops after the first element of that rightmost-first list, i.e. the last occurrence. Docstrings still say "first" (:571; `dynamic_metrics.py:190`).
- Other in-tree picks: gsm8k_normalizer FIRST (`ANS_RE.search`, `normalizations.py:389-392`); math_normalizer LAST `\boxed` (`rfind`, :156, :316); LCB `extract_code` last two fence lines (`tasks/tasks/lcb/codegen_metrics.py:661-664`); swiss_legal: “Use the last extracted letter as the "final" answer.” ([metrics.py#L620-L625](https://github.com/huggingface/lighteval/blob/7fa19dc6f53a713ba8bb6541e7ed66dad2e24fd7/src/lighteval/tasks/multilingual/tasks/swiss_legal/metrics.py#L620-L625), accessed 2026-10-21).

## 2. Fence handling: none in the extraction engine
- Grep for F over extractive_match_utils.py, dynamic_metrics.py, metrics.py, normalizations.py → "No matches found". All patterns run on raw completion text.
- Fence-aware code found: `codegen_metrics.py:659-664` (any line containing F; text between the last two such lines; "" if fewer than two). Not exhausted: the grep over src/ for F was truncated at 26+ files; the claim covers the four engine files plus LCB only.
- No LSP device/route is exposed in this seat’s tool inventory; semantic queries unavailable, so the source check is reported with direct file/line citations.

## 3. Boxed handling
- Env-boxed patterns (`$…\boxed{…}…$`, `\[…\]`, `\(…\)`) sit at boxed priority (:275) and keep the default `boxed="all"` (:51, :68).
- Plain `(?P<first_latexBoxed>\\boxed{.+})`, DOTALL (:278): one match from first `\boxed{` to last `}` (executed). Only this group is named `latexBoxed` and switched to `boxed="last"` (:493-496); env groups are `latexDisplayDollar`, `latexInlineDollar`, etc. (:212-217).
- latex2sympy2_extended 1.0.6 (pinned, `pyproject.toml:92`), `math_normalization.py:256-260`: “If mode is "all", return all boxed contents joined by commas.” ([wheel source](https://files.pythonhosted.org/packages/15/f3/ea8c08d9c279e9088a039cc9a7eaf9d036fff216d79b608483e7fd906fe0/latex2sympy2_extended-1.0.6-py3-none-any.whl), `latex2sympy2_extended/math_normalization.py:256-260`, accessed 2026-10-21). `:258` searches right to left; `:441-442` dispatch.
- math_normalizer: `\fbox` used only when no `\boxed` (:156-158); no box → "" (:133-134, :316).

## 4. Scoring (code-read, not executed)
- `dynamic_metrics.py:228-268`: PASS if ANY (extracted pred, extracted gold) pair matches, max over predictions (`aggregation_function` default max, :161). The fallback string is a candidate (`extractive_match_utils.py:629-630`). Pair test: `math_comparison.py:578-611` (sympy equality or stripped string equality).
- inspect scorers (`metrics/metrics.py:97-105`) compare the extracted prediction and gold lists directly, returning C or I; Python list equality.

## 5. Executed harness (verbatim function text via ast; parser stubbed, so ordering only)
- T1 one tier, both parse, "A1 then B2 then A3" → ['A3']. T2 any_match skips unparseable rightmost → ['Y1']; first_match → []. T2b default metric config → ['Y1','X2'] (fallback union). T3 tier-0 leftmost beats tier-1 rightmost → ['P1']. T4 first_match no fall-through → []; any_match → ['Q2'].
- LCB vs lane E0 (`grader.py:122` regex, identical text; `json.loads(blocks[-1])` at :125):
  - B = F json {"a":1} F noise F json {"b":2} → LCB 'noise'; E0 {"a":1}.
  - E = F json {"a":1} F use F here → LCB ''; E0 {"a":1}.
  - C = two aligned blocks (4 fence lines) → both agree ('[2]').
- Not exercised: sympy/latex2sympy parsing; the library boxed mode was read, not run.

## 6. Map to E-policies (structural fit; frozen table not edited)
| lighteval behaviour (site) | nearest E | fit |
|---|---|---|
| any_match: tier order, rightmost-first, skip unparseable (:599-620) | E2 (single tier); E0 similar but has a fence tier | same ordering within one tier; default metric additionally unions fallback |
| extraction_mode first_match (:622-627) | E5 (last, strict, no fall-through) | partial: no fence tier; falls through only if tier empty |
| fallback_mode first_match (:629-630) | none | union candidate; not in E0–E8 |
| any-pair candidate scoring (dynamic_metrics.py:256-268) | none | E-table scores one value |
| inspect list `==` (metrics.py:105) | none | grader-side |
| fence-agnostic engine | E2 / E3 family | exact |
| LCB last-two fence lines (codegen:661-664) | E5 minus parse check; pairs from right | diverges on B, E; agrees on C |
| gsm8k `ANS_RE.search` (normalizations.py:392) | E3 (first, fence-agnostic) | partial; no parse check |
| math_normalizer rfind; plain boxed span | none | boxed-specific |
| E1 / E4 / E7 / E8 | none (no first-fence rule; no json.loads/raw_decode/JSONDecoder in metrics/) | — |
| E6 | only LCB (label-agnostic, line-based) | partial |

## 7. Gaps for integrator (candidate appended Amendment; nothing applied)
G1 candidate union with raw-string fallback. G2 right-to-left fence pairing (every E fence policy pairs left to right by regex). G3 regex-priority tiers (E0 has only fence-vs-bare). G4 fall-through only on an empty tier. G5 boxed policies (no E reads `\boxed`).

## 8. Novelty
- Shipped in code: last-in-tier, fence-agnostic default, raw-first-match union, strict first_match mode. This supports "published in kind" (claims file expected verdict); it is not a measurement.
- Grep of src/ for disagree|agreement|flip|policy comparison|extraction policy|first_match|last_match: no cross-policy verdict-agreement measurement (hits are blimp task names, flipped-inequality code, mode flags). Not searched: docs, issues, papers, other harnesses.
- Proposed S049 (integrator writes; SOURCES.md untouched): lighteval @7fa19dc6, [extractive_match_utils.py#L607](https://github.com/huggingface/lighteval/blob/7fa19dc6f53a713ba8bb6541e7ed66dad2e24fd7/src/lighteval/metrics/utils/extractive_match_utils.py#L607), quote “# Sort matches by end position (rightmost first) and then by start position (leftmost first)” (14 words), accessed 2026-10-21.

## Installs / scratch
- None installed (git, curl, python3 3.14.8 pre-existing).
- Scratch only: /tmp/le-lighteval (clone); /tmp/le-l2s/l2s.whl (latex2sympy2_extended==1.0.6, sha256 036da4b24c73c4b13566ef4e347be08232c6539ddd75b38f083cc5821e738bba, equals PyPI digest); /tmp/le-l2s/wheel (extracted, read-only).

VERDICT: lighteval’s core selector is last-parseable within priority tiers; in a single-tier/no-fallback comparison it is structurally closest to E2 (not JSON-equivalent), while the default metric adds a raw fallback candidate. E1/E4/E7/E8 have no counterpart, E6 only partial via LCB; right-to-left fence pairing diverges from E0 when an unpaired fence trails (B, E).
