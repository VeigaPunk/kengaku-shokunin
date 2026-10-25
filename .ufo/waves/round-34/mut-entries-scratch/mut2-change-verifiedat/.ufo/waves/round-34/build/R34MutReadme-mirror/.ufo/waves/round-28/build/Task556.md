# Task556 — WebArena case 556 static intent→evaluator audit (round28 C1, author-side)

Writer/seat: `KengakuR28.Task556-2` (read-only scout seat). Author-side advice, not outside closure.
Scratch: `.ufo/waves/round-28/scratch/Task556/siblings.jsonl` (jq projection of raw tasks 556–566).

## Inputs and integrity

Local pinned snapshot `plans/fixtures/r28/webarena/` (upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`, manifest `opened: 2026-10-21`). `sha256sum` observed equal to `manifest.json`:

| File | sha256 (observed = manifest) | Upstream URL (manifest) |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…37652` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…0c22` | …/dce04686…/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…e275` | …/dce04686…/evaluation_harness/helper_functions.py |

Access date 2026-10-21, local pinned copy only. I did not contact any upstream site or benchmark site, and I did not import, eval, or execute any upstream code. Commands run: `jq` and `grep` over the raw JSON, `sha256sum`, and `grep -n` over the evaluator files. I installed or updated no tools.

## Task record (raw JSON lines 18041–18082)

- `task_id` 556, `intent_template_id` 87, `sites` `["gitlab","wikipedia"]`, `require_login` true, `storage_state` `./.auth/gitlab_state.json`, `start_url` `__GITLAB__`, `require_reset` **false**.
- Intent (L18051), quoted: "Create a repo named nolan_honest_fans with movies directed by Christopher Nolan in a README file" (16 words).
- `eval_types` `["program_html"]`, `reference_answers` null, `reference_url` "".
- `program_html[0]` (L18061): `url` `__GITLAB__/byteblaze/nolan_honest_fans/-/raw/main/README.md`, `locator` "", `required_contents.must_include` (L18064–18076), 12 items: Following, Memento, Insomnia, Batman Begins, The Prestige, The Dark Knight, Inception, The Dark Knight Rises, Interstellar, Dunkirk, Tenet, Oppenheimer.
- Stratum: (gitlab+wikipedia, {program_html}) contains 6 tasks (556–561). 556 is the minimum ID, which matches the frozen selection rule.

## Evaluator path (evaluators.py)

1. `evaluator_router` L369–370 matches `case "program_html"` and appends `HTMLContentEvaluator()`, its only evaluator. `EvaluatorComb` L348–351 multiplies the scores. `StringEvaluator` and `URLEvaluator` are never constructed, so `reference_answers: null` and the empty `reference_url` are never read.
2. `HTMLContentEvaluator.__call__` L259–333: there is one target. The URL does not start with `func` (L263), so no `eval` and no helper call happen. Because the URL is not `"last"`, the evaluator runs `page.goto(target_url)` (L272) followed by a fixed `time.sleep(3)` (L273).
3. The locator is empty, so L276–277 sets `selected_element = page.content()`, which is the whole serialized DOM of the response document. L303 then applies `html.unescape`.
4. The `must_include` branch (L312–327) splits each item on `" |OR| "` (none of the 12 items contain it). It then calls `StringEvaluator.must_include(..., tokenize=False)` (L318–322). That function lowercases both sides after strip and quote-trim (`clean_answer` L80–86) and tests a plain substring with `clean_ref in clean_pred` (L111). The score is the product over all 12 items, so it is binary.
5. `helper_functions.py` is **not reached** for this task: there is no `func:` URL or locator and no fuzzy or ua match. No LLM judge is used and no `PseudoPage` is involved.
6. Neither the trajectory nor the final answer is read by this evaluator. Scoring depends only on end-state page content.

Located quotes (≤25 words):
- evaluators.py L277: "selected_element = page.content()"
- evaluators.py L111: "return float(clean_ref in clean_pred)"
- evaluators.py L86: "return answer.lower()"

## Case table (L1-usable)

| Intent element | Evaluator operator / target | Checked? | Notes |
|---|---|---|---|
| "Create a repo" | Indirectly, through a successful `goto` of the raw file URL (L272) | Partially | Only the existence of a readable file at the URL is checked. There is no check that creation happened in this episode, because `require_reset` is false. |
| "named nolan_honest_fans" | URL path segment `nolan_honest_fans` | Partially | The project **path** (slug) is checked, not the display name. The `byteblaze` namespace is hard-coded but not stated in the intent. Siblings encode slugification explicitly, for example 566 "Do it myself" maps to `Do-it-myself`. |
| "in a README file" | `/-/raw/main/README.md` | Stricter than the intent | The evaluator requires the exact filename `README.md` on branch `main`. A README with another name or extension (`README`, `readme.md`, `README.txt`) or on another default branch scores 0. |
| "movies directed by Christopher Nolan" | 12 × case-insensitive substring over the full DOM | Partially | Inclusion of each title is checked. Extras, wrong titles, ordering, formatting, and the list structure are not checked. |
| (implicit) visibility and auth | Inherited from the agent's browser context | Not checked | A private repo is readable only if the context is still authenticated. |
| Agent final answer | Not used | Not checked | — |

### Checked properties

- An HTTP navigation to `<GITLAB>/byteblaze/nolan_honest_fans/-/raw/main/README.md` yields a DOM that contains all 12 strings, case-insensitively.

### Unchecked properties

- The display name of the repo, its visibility and description, and that the repo was created in this episode.
- That README content is limited to Nolan-directed films. Extra or incorrect entries are not penalized.
- That each title appears as a title rather than as an incidental substring (see the limitation below).
- Any Wikipedia usage. The site is listed as an information source only and no target touches it.

## Dynamic state and judge dependencies

- **No LLM judge**, and no `helper_functions` path runs.
- **Placeholder substitution:** `__GITLAB__` is never substituted in the pinned evaluator. The only replace call is `__last_url__` at L265, confirmed by grep. Scoring therefore requires a generated config that is outside this snapshot. That dependency is unpinned and its correctness is unverified here.
- **Live GitLab state (unchecked inference, not observed):**
  - The instance default branch must be `main`.
  - The raw endpoint must serve `.md` inline. An attachment disposition would make `goto` raise instead of scoring.
  - The agent's page must still hold `byteblaze` auth if the repo is private.
  - The identity behind `gitlab_state.json` must be `byteblaze`. That file is not in the snapshot.
- **`require_reset: false`:** a `nolan_honest_fans` repo left over from an earlier run or sibling evaluation would make a no-op episode score 1. Initial absence of the repo is assumed, not verified.
- **Timing:** there is a fixed 3 s sleep. A raw blob is static once committed, so this is low risk.
- **Wikipedia snapshot:** the reference list includes Oppenheimer (released 2023). Whether the offline Wikipedia lists it as a Nolan-directed film is not evidenced in the snapshot. This is an unresolved inference.

## Task-specific potential validity limitation (not a proven defect)

Case-insensitive substring matching over the whole page makes several of the 12 required items non-discriminating:

- **"Following"** (Nolan's 1998 film) matches ordinary prose such as "the following movies…".
- **"The Dark Knight"** is satisfied by "The Dark Knight Rises".
- **"Tenet"** matches "tenets".

So a README that omits *Following* and *The Dark Knight* can still score 1 if it uses natural wording. This is a false-positive risk. In the other direction there is a false-negative risk: the intent's "a README file" is looser than the required `README.md` on `main`, and an Oppenheimer entry may be required that the offline Wikipedia does not support.

The same "The Dark Knight" overlap exists in sibling 557, and 556's list equals the union of 557 and 558, which shows the reference was assembled from the same list.

## Runtime evidence required before declaring 556 valid or invalid

1. The generated (substituted) config for 556 and the generator revision.
2. The live GitLab instance's default-branch setting, the raw-endpoint Content-Type and Content-Disposition for `README.md`, and the identity in the storage state.
3. Proof that the repo is absent at episode start (environment reset log).
4. The offline Wikipedia's Christopher Nolan filmography content, specifically Oppenheimer.
5. Scored trajectories that probe the substring hazard. One example is a README that omits *Following* but contains "following". This must be run only in a sanctioned environment, never by this seat.

Without these, the case is **UNDETERMINED**, not valid and not invalid.

## Limitations

- Static reading only. Chromium `page.content()` wrapping of text/plain and GitLab raw serving behavior are inferences.
- The sample is the frozen non-random 16. This is no statement about other tasks beyond the named siblings 557–566 that were read for contrast.
- No source row or knowledge admission is made by this seat.

## Verdict

**PASS (scoped):** the static mapping from task 556's intent to its evaluator operators and targets is complete and anchored, covering the checked and unchecked properties and the dynamic dependencies. Task validity itself remains **UNDETERMINED** pending the runtime evidence above. This is not a round-level PASS.

## Dated erratum — 2026-10-21

This appendix preserves the preceding report verbatim and corrects its scope:

- The intent quote contains **15 words**, not 16.
- `HTMLContentEvaluator.__call__` is defined at L248; its body relevant here runs L255–333, rather than L259–333.
- The evaluator replaces both `__last_url__` (L265) and `__page__` (L298). Neither replacement handles `__GITLAB__`; generated-config substitution remains outside the pinned snapshot.
- The within-list title overlap occurs in task **556 and 561**, not 557: task557 does not require “The Dark Knight Rises.” The earlier sibling557 overlap statement is withdrawn.
- File readability alone is not the scoring predicate: scoring requires **all 12 substring tests** over the selected serialized document. A successful navigation is not an explicit existence/status check.
- `require_reset: false` does not establish initial repository state or an actual leftover. A same-task prior state is only a conditional runtime concern; the earlier “sibling evaluation” mechanism is unsupported because tasks556–561 use distinct slugs and is withdrawn.
- The instance-wide default-branch setting need not itself be `main`: the exact scored branch is `main`; whether the creation workflow produces that branch requires runtime evidence.

These corrections leave the static twelve-test mapping intact. **Scoped verdict: PASS for the documented static mapping with this erratum; task validity remains UNDETERMINED.** No runtime probe, site contact, production/candidate edit, or additional verification was performed for this appendix.
