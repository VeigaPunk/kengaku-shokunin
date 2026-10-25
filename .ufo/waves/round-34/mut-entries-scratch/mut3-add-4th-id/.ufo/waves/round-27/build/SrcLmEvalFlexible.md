# SrcLmEvalFlexible — lm-evaluation-harness GSM8K filters (round 27, build)
Scout KengakuR27.SrcLmEvalFlexible · accessed 2026-10-21 · read-only · scratch clone /tmp/kengaku-r27-SrcLmEvalFlexible-lmeval

## Answer
- `strict-match` in gsm8k.yaml, gsm8k-cot.yaml, gsm8k-cot-zeroshot.yaml = FIRST match → nearest pre-registered E3 bare-first (axis only).
- `flexible-extract` in all four variants = LAST match → nearest E2 bare-last (axis only; not E0, which takes the last fenced block).
- Exception: gsm8k-cot-llama.yaml `strict-match` = LAST (`group_select: -1`). The label "strict" does not fix position.

## 1. Pin
- Commit `d6de81643928d653435c431bae19945d41d32520` on `main` (committer 2026-09-14T15:51:05+05:00; "fix(basqueglue): load the f1 metric with evaluate (#4076)"). Confirmed by `git ls-remote … refs/heads/main` and by raw reads of gsm8k.yaml and gsm8k-cot-llama.yaml at this hash (lines match the clone).
- sha256 gsm8k.yaml `82eb1780b263bc040729032b3e076990c7933f42163c91e359f38820dd1d8833`; gsm8k-cot.yaml `7c9dd2561fe334a55f62bdc6a876f045e6dc7f53714c7a9db506b89c6de6bc96`; gsm8k-cot-zeroshot.yaml `c506c7f5c19da2817db443f7e6d943421dfc9237510a70991d2667cf8efce1e0`
- sha256 gsm8k-cot-llama.yaml `c295bc7e942e8f3a51b91d14d5e592d2b037330c831f4ab5b2f8ddca27e031d6`; filters/extraction.py `eb976bb36d5d3e93faafe6d065678e24b4474e78cd4fce1e730e2b8f49b9fda0`; filters/selection.py `5f8264dce91dd1282b84487d703e7e2bb11bef5fd6c93f91b4e51342a4fb76ab`

## 2. Filter definitions (lm_eval/tasks/gsm8k/; lines at d6de8164)
| file (version) · lines | filter | regex_pattern (line) | group_select | selects |
|---|---|---|---|---|
| gsm8k.yaml (3.0) · 33-37 | strict-match | `#### (\\-?[0-9\\.\\,]+)` (:36) | unset → 0 (extraction.py:27) | first |
| gsm8k.yaml · 38-43 | flexible-extract | `(-?[$0-9.,]{2,})\|(-?[0-9]+)` (:42) | -1 (:41) | last |
| gsm8k-cot.yaml (3.0) · 47-51 | strict-match | `The answer is (\\-?[0-9\\.\\,]+).` (:49) | unset → 0 | first |
| gsm8k-cot.yaml · 52-57 | flexible-extract | as gsm8k (:55) | -1 (:54) | last |
| gsm8k-cot-zeroshot.yaml (3.0) · 32-36 | strict-match | as cot (:35) | unset → 0 | first |
| gsm8k-cot-zeroshot.yaml · 37-42 | flexible-extract | as gsm8k (:41) | -1 (:40) | last |
| gsm8k-cot-llama.yaml (4.0) · 46-51 | strict-match | `The final answer is ((-?[$0-9.,]{2,})\|(-?[0-9]+))` (:49) | **-1 (:48)** | **last** |
| gsm8k-cot-llama.yaml · 52-57 | flexible-extract | as gsm8k (:55) | -1 (:54) | last |
- Mechanics: extraction.py:26-27 default `group_select: int = 0`; :47-49 `findall`, then `match[self.group_select]`; :50-53 first non-empty group of tuple matches; selection.py:23 take_first = `r[0]`; api/task.py:763-767 and filters/__init__.py:22 forward every yaml key as constructor kwargs. gsm8k-cot-self-consistency.yaml (2.0) has neither name.

## 3. Quotes (access 2026-10-21; each ≤25 words)
- gsm8k.yaml:33-37 `regex_pattern: "#### (\\-?[0-9\\.\\,]+)"` — https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/tasks/gsm8k/gsm8k.yaml#L33-L37
- gsm8k.yaml:41-42 `group_select: -1` / `regex_pattern: "(-?[$0-9.,]{2,})|(-?[0-9]+)"` — same URL, #L41-L42
- gsm8k-cot-llama.yaml:48-49 `group_select: -1` / `regex_pattern: The final answer is ((-?[$0-9.,]{2,})|(-?[0-9]+))` — .../d6de81643928d653435c431bae19945d41d32520/lm_eval/tasks/gsm8k/gsm8k-cot-llama.yaml#L48-L49
- extraction.py:27 `group_select: int = 0,`; :49 `match = match[self.group_select]` — .../d6de81643928d653435c431bae19945d41d32520/lm_eval/filters/extraction.py#L27, #L49
- extraction.py:147 (MultiChoiceRegexFilter docstring): "Selects the (group_select)th match from the findall result." — same base, #L147

## 4. Exercised outputs (real RegexFilter + TakeFirstFilter from clone; only lm_eval.api stubbed)
| response | gsm8k strict | gsm8k flexible | cot / zeroshot strict | cot-llama strict |
|---|---|---|---|---|
| "She has 5 + 2 = 7 apples.\n#### 7" | 7 | 7 | invalid | invalid |
| "Draft: #### 5 looks wrong.\nRecount: 3 * 24 = 72.\n#### 72" | 5 | 72 | invalid | invalid |
| "Total cost: $1,250.00. Done..." | invalid | `...` | invalid | invalid |
| "The answer is 42.." | invalid | `42..` | `42.` | invalid |
| "The answer is 8.\nNo, correction: The answer is 9." | invalid | `9.` | `8` | invalid |
| "The final answer is 8.\nNo, correction: The final answer is 9." | invalid | `9.` | invalid | `9.` |
"invalid" = `[invalid]` fallback. The unescaped final `.` in the CoT regex is part of the match ("The answer is 8. Thus done." → `8.`).

## 5. Lane population control (four pinned files, read-only)
- round8 (268 lines), round9 (284), round11 (1473), round12 (4114): "```" in 204/168/731/2038 lines; "####", "The answer is", "final answer" in 0 lines.
- So every marker-keyed strict-match pattern returns `[invalid]` on every lane record: first/last is vacuous for strict-match here.

## 6. Mapping to frozen policies (plans/round-27-claims.md table :35-45; prior art :73-78)
- flexible-extract → E2 bare-last (last match, fence-agnostic). Not E0: E0 takes the last fenced block.
- strict-match (gsm8k/cot/zeroshot) → E3 bare-first (first match, fence-agnostic). Axis only; no E0–E8 policy is keyed to an answer marker.
- cot-llama strict-match (last) → E2 by axis. lm-eval's strict/flexible pair is marker-required vs any-number; the claims' "strict whole-output" is E4 (whole output must be JSON), a different sense, so no E-policy counterpart exists for the harness "strict" label.
- E0/E1/E5/E6 (fence-aware) and E7/E8 (decoded spans) have no lm-eval GSM8K counterpart.
- Prior-art clause (:73-78) holds: `group_select` 0/-1 switches first/last. Gap: adding a marker-keyed first-match policy needs an appended `## Amendment N`, not an edit.

## 7. Unknowns, installs, writes
- Not traced: how exact_match applies regexes_to_ignore (gsm8k.yaml:18-22); `\.$` strips one trailing "." only (inference from the regex, not run). Versions before d6de8164 and repeats>1 not checked.
- Installs: none (git, sha256sum, python3 + PyYAML already present; lm_eval.api stubbed in memory). Writes: this file only.

VERDICT: flexible-extract is last-match (E2 by axis) and strict-match first-match (E3 by axis) except cot-llama strict = last; no frozen policy is marker-keyed and the pinned population has zero markers.
