# Task681 — C1 case audit (author-side, read-only scout)

Writer/seat: `KengakuR28.Task681-2` (UFO-FSD scout, leaf, no delegation). Author-side advice, not outside closure.
Scope: one pinned WebArena raw task (task_id 681) traced statically through the pinned scorer. No upstream import/exec/eval, no browser, no benchmark-site contact, no production writes, no installs.

## Inputs and integrity

Pinned upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`, opened 2026-10-21 (per `plans/fixtures/r28/webarena/manifest.json`). Observed `sha256sum` matches the manifest for all three inputs:

| File | sha256 (observed = manifest) |
|---|---|
| `config_files/test.raw.json` | `7b50386f…02537652` |
| `evaluation_harness/evaluators.py` | `e23edb39…77e00c22` |
| `evaluation_harness/helper_functions.py` | `ec758da4…e275` |

Source opening (S061-class raw tasks): URL `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json`, accessed 2026-10-21, located quote at `test.raw.json:23376`: "Find a GitLab repository related to gan implementation and make a Reddit post linking to it in a relevant subreddit". Scope: task 681 record only.

## Task record (`test.raw.json:23362-23400`)

- sites `["reddit","gitlab"]`; `require_login: true`; storage `./.auth/gitlab.reddit_state.json`; `start_url: "__REDDIT__"`; **`require_reset: false`**; `intent_template_id: 116` (siblings 682, 683 share it).
- `eval_types: ["url_match","program_html"]` (L23379-23382); `reference_answers: null`; `url_note: "GOLD in PRED"` (L23397).
- `reference_url`: `__REDDIT__/f/machinelearning |OR| __REDDIT__/f/deeplearning |OR| __REDDIT__/f/technology` (L23384).
- `program_html[0]`: `url: "last"`, `locator: document.querySelector('.submission__inner').outerText`, `must_include: ["gan implementation", "__GITLAB__/eriklindernoren/PyTorch-GAN"]` (L23386-23395).

## Case table (intent → operator → target)

| # | Intent clause | Evaluator / operator (anchor) | Exact target | Checked | Not checked |
|---|---|---|---|---|---|
| R | (routing) | `evaluator_router` L356-374 → `URLEvaluator`, `HTMLContentEvaluator`; `EvaluatorComb` multiplies the scores, L348-352 | both must be 1.0 | Both evaluators run; product is 0 or 1 | `StringEvaluator` is not routed, so the final answer text is ignored |
| U | "in a relevant subreddit" | `URLEvaluator` GOLD in PRED, L212-236. `clean_url` only does `rstrip("/")` (L187-190). `parse_url` uses netloc+path (scheme dropped) (L192-197). `ref_base_path in pred_base_paths` is a **str-in-str substring** test because `parse_url` returns a str (L218-226). No reference has a query, so `query_score` stays 1.0 (L228-235). No case folding. | final `page.url` contains `<host>/f/machinelearning`, `/f/deeplearning` or `/f/technology` | The final URL path contains one of the 3 lowercase forum paths | Whether the post is in that forum (listing pages also pass); whether other forums are "relevant"; URL case variants |
| H1 | "linking to it" | `HTMLContentEvaluator`, L258-333. `url == "last"` means no `goto` (L271). The locator starts with `document.`, so it runs `page.evaluate`; on exception the selection becomes `""` (L279-294). Then `html.unescape` (L303). `must_include` lowercases both sides with `clean_answer` and does a substring test (L80-86, L98-111, L312-327, `tokenize=False`). | `outerText` of the **first** `.submission__inner` on the final page contains the substituted lowercase `__GITLAB__/eriklindernoren/pytorch-gan` | The literal repo URL string appears in visible text of the first submission block | Whether it is a clickable link or the submission URL field; whether the post was created by the agent in this episode |
| H2 | "related to gan implementation" | same must_include, L315-327 | `"gan implementation"` substring (case-insensitive) | The topic phrase appears literally (it also matches inside "gan implementations") | Semantic relatedness. Paraphrases such as "implementation of GANs" score 0 |
| G | "Find a GitLab repository" | none (no GitLab-side evaluator) | — | Only one fixed repo string (H1) | GitLab browsing; any other qualifying GAN repo |

Helper functions: none are used. `reddit_get_post_url` (`helper_functions.py:97-112`) is imported, but task 681 uses `"last"`, not `func:`. There is no LLM judge (`llm_fuzzy_match`/`llm_ua_match` are not reached), and no API helper.

## Dynamic state / judge dependencies

1. **Final page state.** Both checks read the agent's terminal page (`page.url`, plus DOM `outerText` with no navigation). The outcome depends on where the episode ends.
2. **Placeholder substitution.** `__REDDIT__`/`__GITLAB__` are rewritten outside the pinned snapshot; the generator script is not pinned. [INFERENCE] The substituted GitLab base (scheme://host:port) must equal the text the agent posts.
3. **Postmill DOM.** The `.submission__inner` class and what its `outerText` shows for a link post (title only, domain, or full URL) are runtime site facts. They are not in the snapshot.
4. **Forum URL canonical casing.** Runtime site fact (see limitation L1).
5. **No reset.** `require_reset: false` on a state-mutating task means posts from earlier episodes can persist.
6. **GitLab inventory.** Task 296 (L9268, exact_match `…/eriklindernoren/PyTorch-GAN.git`) and task 395 (L12289, "Fork the Pytorch GAN repo with most stars", target `__GITLAB__/byteblaze/PyTorch-GAN`) show the benchmark itself treats several PyTorch-GAN repos as present. [INFERENCE] More than one repo plausibly satisfies "related to gan implementation".

## Observed commands

- `sha256sum` of the 3 inputs (all matched the manifest).
- A python3 `json` census of every task whose JSON contains `machinelearning` in any case. Result: 599, 604 and 609 use `/f/MachineLearning`; task 731 targets the concrete post `__REDDIT__/f/MachineLearning/1/nvidia-rtx-4090` (L26032); tasks 625, 681, 682 and 683 use lowercase `/f/machinelearning`.
- A scratch stdlib re-statement of the GOLD in PRED rule (it does not import upstream code), using hypothetical host `r.example`: `.ufo/waves/round-28/scratch/Task681-2/url_rule_mirror.py`. Outputs:

| URL path | Score |
|---|---|
| `/f/deeplearning/999/…` | 1.0 |
| `/f/MachineLearning/999/…` | **0.0** |
| `/f/machinelearning/999/…` | 1.0 |
| `/f/technologyfoo/999/x` | 1.0 |
| `/f/deeplearning` (listing page) | 1.0 |
| `/submit?forum=deeplearning` | 0.0 |

  This illustrates scorer semantics only; it is not site behaviour.

## Potential validity limitations (task-specific, not proven defects)

- **L1 (primary): case-sensitive URL alternative.** The URL check does not fold case (L212-226). Task 731 (L26032) records a real post at `/f/MachineLearning/1/…`. If the site's canonical post URL keeps that casing, a correct post in that forum would score 0 on the `machinelearning` alternative. Only `deeplearning` and `technology` would remain effective. [INFERENCE] This is unproven: Postmill may normalise or redirect forum names.
- **L2: lexical and fixed-target proxy.** The literal phrase "gan implementation" plus one fixed repo string stand in for "related" and "relevant". Valid paraphrases or other GAN repos (see dependency 6) produce false negatives.
- **L3: provenance not checked.** The URL substring also accepts forum listing pages and lookalike prefixes (`/f/technologyfoo`). `querySelector` takes the first `.submission__inner` only. With `require_reset: false`, a leftover matching post at the top of a listing could pass without a new post from this episode. "Linking" is satisfied by plain text.

## Runtime evidence required before any valid/invalid declaration

1. The canonical post URL casing produced by submitting to the MachineLearning forum in the pinned Reddit image: does `/f/machinelearning` resolve, redirect, or get rewritten?
2. The forum inventory (do any forum names have the three references as prefixes?) and whether those three are the only topical forums.
3. Rendered `.submission__inner` `outerText` for a link post compared with a text post: does the full GitLab URL appear?
4. The substituted `__GITLAB__` value compared with the URL an agent would copy from the GitLab UI (scheme, port, trailing path such as `/-/tree/master`).
5. The GitLab repo inventory matching "gan implementation".
6. The reset policy actually used between episodes.

None of this was gathered (out of scope: no site contact).

## Verdict

**PASS (scoped)** for the deliverable: the case-681 static intent→evaluator mapping is complete and anchored on hash-verified inputs.
**Task validity: UNDETERMINED.** L1–L3 are potential limitations pending the runtime evidence above. This is not a defect finding and not a round-level PASS.
Remaining unknowns: the placeholder generator is not pinned; site DOM, URL casing and GitLab inventory have not been observed.
