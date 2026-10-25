# RowSimpleEvals — round 27 source opening (openai/simple-evals answer extraction)

Accessed 2026-10-21. Read-only seat; no lane tree, index, or gate.md write. Only this file was written.

## Behavior
Opened openai/simple-evals at pinned commit `652c89d0ca9df547706735883097e9537d40dc47` (main HEAD at access; committer date 2026-04-22T22:16:16Z). Fetched raw bytes by commit SHA into `/tmp/kengaku-r27-RowSimpleEvals/` (`common.py`, `mmlu_eval.py`, and `tree/` holding the other eval modules and samplers).

## Premise correction (brief said: `re.search` with `ANSWER_PATTERN`)
Partly wrong for `mmlu_eval.py`. Verified call sites:
- `common.py:26` `ANSWER_PATTERN_MULTICHOICE = r"(?i)Answer[ \t]*:[ \t]*\$?([A-D])\$?"`; `common.py:27` `ANSWER_PATTERN = r"(?i)Answer\s*:\s*([^\n]+)"`
- `gpqa_eval.py:59-60`: `re.search(ANSWER_PATTERN_MULTICHOICE, ...)`; no match → `None`.
- `math_eval.py:53-54`: `re.search(ANSWER_PATTERN, response_text)`; no match → `None`.
- `drop_eval.py:286-287`: `re.search(ANSWER_PATTERN, ...)`; no match → `extracted_answer = ... else response_text` (**whole-response fallback**).
- `mmlu_eval.py:108-113`: NOT `ANSWER_PATTERN`. Loops `MULTILINGUAL_ANSWER_REGEXES` (`common.py:32`, in order) and calls `re.search(MULTILINGUAL_ANSWER_PATTERN_TEMPLATE.format(answer_regex), response_text)`; first hit with `break`.
- Repo-wide `.py` grep at the pinned tree (17 files fetched): no `re.findall`/`finditer` over these patterns; `ANSWER_PATTERN` is not used by `mmlu_eval.py`.
- The `re.search` first-match semantics are inferred from the call shape (single call, `match.group(1)`, no iteration over matches); this is not a quote from the Python docs.

## (1) Draft SOURCES.md row (S0xx; 11 content cells; split on `|` gives 13 parts as in existing rows)
| S0xx | openai/simple-evals, harness answer-extraction call sites at commit 652c89d0ca9df547706735883097e9537d40dc47 — https://github.com/openai/simple-evals/tree/652c89d0ca9df547706735883097e9537d40dc47 | code | A | the reference harness's own extraction call sites at this commit, not evidence about how any model or grader behaves | common.py:26-27; math_eval.py:53-54; gpqa_eval.py:59-60; drop_eval.py:286-287; mmlu_eval.py:108-113 (commit 652c89d0, committer 2026-04-22) | harness extracts with `re.search` on a free-text `Answer:` pattern (one call, first match, no match-list scan); no-match handling differs by call site (math/gpqa → None; DROP → raw response); this is a first-match regex policy over text, not a JSON-block policy | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |

Notes for integrator: `kind` = `code` is not in the existing vocabulary (`paper`, `docs`, `tool`, `own-work`, `dataset`); decide whether to add it or use `docs`. Tier A is scoped to "this harness's own code at this commit."

## (2) gate.md line (for `corpus/evidence/round27-sources/gate.md`; not written by me)
| S0xx | https://raw.githubusercontent.com/openai/simple-evals/652c89d0ca9df547706735883097e9537d40dc47/math_eval.py (commit 652c89d0ca9df547706735883097e9537d40dc47; HTTP 200) | accessed 2026-10-21; math_eval.py:53 | “match = re.search(ANSWER_PATTERN, response_text)” (4 words; verified by `grep -nF`, match at line 53) | sha256 math_eval.py 845500fb5299620e158f12ae7d8618ca64a50dc69b5535cc793e8498bdcce136; common.py 84616c52821a30ae3f55f153a763153fd833cb41b547b09f547b46e6337f8f35; mmlu_eval.py e9165b54137cff50bf0afe30bfb343812335edcb5ae3f13ec78898871239af6c; drop_eval.py 90cceebebe914fa4e58dc676940cdb500ff34f97a6a3db20278c2c8df19d57ae; gpqa_eval.py f746e411bdbd3ec8cd0738e30fc0989ac0d6b5a1b988a454633553b419b724d3; bytes at /tmp/kengaku-r27-RowSimpleEvals/ |

## (3) Pre-registered policy grounding
**None of E1–E8.** All of E0–E8 parse JSON blocks (fenced or bare, `grader.py:121-134`). This source parses free-text `Answer:` lines with regexes. Closest shape is E3 (first match, fence-agnostic), but the target differs, so citing it as grounding E3 would overclaim. Use it only as harness-prior-art context for the knowledge entry.

## Observation (not a policy addition)
`drop_eval.py:287` falls back to the whole raw response when no match is found. None of E0–E8 includes a whole-response fallback (E4 and E5 return None). Recorded for the knowledge entry; not added, since the pre-registration is frozen.

## Installs / tools
None. Used `curl` and `grep`/`sed`/`python3` already present. No `pacman`, no `uv`, no packages.

## Files written (this seat)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/build/RowSimpleEvals.md` (this report)
- No clone under `/tmp/kengaku-r27-*` was created; saved bytes are read-only fixtures in `/tmp/kengaku-r27-RowSimpleEvals/`.

VERDICT: source opened at pinned commit 652c89d0; row S0xx drafted (kind `code` needs a vocab decision); gate line drafted with a 4-word quote verified at math_eval.py:53; grounds none of E1–E8; the brief's `ANSWER_PATTERN` premise is only partly true (mmlu uses the multilingual template).
