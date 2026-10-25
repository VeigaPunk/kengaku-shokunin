# FTask681 — author-side falsification of BUILD case681 (WebArena task_id 681)

Seat `KengakuR28.FTask681` (UFO-FSD scout, leaf, no delegation). Read-only over production; no
upstream import/exec/eval, no browser, no benchmark-site request, no scorer execution, no
production writes, no installs or tool updates (none were needed). All findings are author-side,
never outside non-author evidence.

## Frozen artifact identity

| artifact | identity |
|---|---|
| frozen candidate | `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` |
| candidate sha256 (recomputed) | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (matches brief) |
| canonical path | `corpus/knowledge/webarena-task-spec-audit.md` — **not admitted**; not read as evidence |
| build case | `.ufo/waves/round-28/build/Task681.md` (8858 bytes, 84 lines) |

Pinned inputs, local copies, `sha256sum` recomputed and equal to
`plans/fixtures/r28/webarena/manifest.json` (upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`,
manifest `opened` 2026-10-21):

| file | sha256 |
|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` |

No upstream URL was fetched; the pinned bytes above were the only source used. No site, DOM,
cookie, auth-state or repository-runtime evidence was touched.

## Task 681 record — independent re-read

`test.raw.json:23362-23400`: `task_id 681` (L23367); `sites ["reddit","gitlab"]` (L23363-23366);
`require_login: true` (L23368); `storage_state "./.auth/gitlab.reddit_state.json"` (L23369);
`start_url "__REDDIT__"` (L23370); `require_reset: false` (L23377); intent L23376;
`eval_types ["url_match","program_html"]` (L23379-23382); `reference_answers: null` (L23383);
`reference_url` `__REDDIT__/f/machinelearning |OR| __REDDIT__/f/deeplearning |OR|
__REDDIT__/f/technology` (L23384); `program_html` L23385-23395 with `url "last"` (L23387),
locator `document.querySelector('.submission__inner').outerText` (L23388), `must_include
["gan implementation","__GITLAB__/eriklindernoren/PyTorch-GAN"]` (L23390-23393);
`url_note "GOLD in PRED"` (L23397); `intent_template_id 116` (L23399).
`prep_actions` absent; one target; one required-content operator (`must_include`).
Independent census: `intent_template_id 116` is exactly `{681,682,683}`.

## Intent → clause / operator / target check

| clause | case681 report row | my re-read | status |
|---|---|---|---|
| routing | R: router L356-374; `EvaluatorComb` product L348-352; both 0/1 | `evaluator_router` maps `url_match`→`URLEvaluator` (367-368), `program_html`→`HTMLContentEvaluator` (369-370); product loop 348-352; both evaluators return 0.0/1.0 for this task | CONFIRMED |
| "in a relevant subreddit" | U: GOLD-in-PRED L212-236; `clean_url` rstrip L187-190; netloc+path L192-197; str-in-str L218-226; empty `ref_queries` ⇒ query_score 1.0 L228-235 | code is exactly as stated; no reference has `?`; scheme and fragment are dropped; case is not folded | CONFIRMED |
| "linking to it" | H1: URL `"last"` ⇒ no goto L271; `document.` ⇒ `page.evaluate` L279-291; exception ⇒ `""` L292-294; `html.unescape` L303; `must_include` L312-327 with `tokenize=False` L322 | code is exactly as stated; `querySelector` takes the first match; lowercasing via `clean_answer` L80-86, L98-111 | CONFIRMED |
| "related to gan implementation" | H2: same `must_include`; literal substring; plural extension | ref is the raw `instantiation_dict.topic` string; substring test is unanchored | CONFIRMED |
| "Find a GitLab repository" | G: no GitLab-side evaluator; one fixed repo string | `eval_types` contains no `string_match`; no helper reads GitLab; only the Reddit page is inspected | CONFIRMED |
| "make a Reddit post" | provenance not checked | no evaluator reads trajectory/actions; a pre-existing matching page passes | CONFIRMED |
| helpers/judges | none used | `reddit_get_post_url` (helper L97-112) is imported (evaluators L23) but not reached; no `llm_*`, no API helper | CONFIRMED |

Every intent clause has a row, and every row's "Checked"/"Not checked" split matches the pinned
branch structure. `StringEvaluator` is not routed (L361-372), so the final answer text is ignored.

## Source-line and numeric claim audit

All `L` anchors in `Task681.md` were re-read at those exact lines. Confirmed:

- record/fields: 23362-23400, 23376, 23379-23382, 23384, 23386-23395, 23397.
- evaluator: 356-374, 348-352, 212-236 (score body), 187-190, 192-197, 218-226, 228-235,
  258-333, 271, 279-294, 303, 80-86, 98-111, 312-327, 315-327.
- helper: `helper_functions.py:97-112`.
- census claim: tasks containing `machinelearning` in any case are exactly
  `[599,604,609,625,681,682,683,731]`; uppercase gold refs at L20026 (599), L20211 (604),
  L20401 (609); task 731 navigation URL at L26032; lowercase at 625/681/682/683. Matches.
- template siblings: 116 = `{681,682,683}`; 117 = `{684..688}`. Matches.
- scratch mirror `.ufo/waves/round-28/scratch/Task681-2/url_rule_mirror.py` exists and its six
  printed scores reproduce exactly (`1,0,1,1,1,0`).

Two loose anchors (precision, not mapping failure):

- **F681-1.** `Task 296 (L9268, exact_match …)` — L9268 is the `task_id` line; the `exact_match`
  value is L9284. `Task 395 (L12289, … target …)` — L12289 is the `task_id` line; the target URL
  `__GITLAB__/byteblaze/PyTorch-GAN` is L12308. Other field anchors in the same report are exact,
  so this is an inconsistent anchor convention, not a wrong task.
- **F681-2.** "storage `./.auth/…`" (L23369) — the raw key is `storage_state`; value and task are
  correct.

## Decisive controls (independent stdlib mirrors; upstream not imported)

Scripts: `.ufo/waves/round-28/scratch/FTask681/predicate_control.py` (sha256
`b3bb1d7c…3081ae7`), `predicate_control2.py` (sha256 `85216abe…dfef492`). Together they mirror
`URLEvaluator` L212-236 and `clean_answer`/`must_include` L80-111 at `tokenize=False`, exactly.

### URL control (reference string = task 681's three alternatives, host `r.example`)

| predicted URL | score |
|---|---|
| `http://r.example/f/machinelearning/999/x` | 1.0 |
| `http://r.example/f/deeplearning/999/x` | 1.0 |
| `http://r.example/f/technology/999/x` | 1.0 |
| `http://r.example/f/MachineLearning/999/x` | **0.0** (case; report L1) |
| `http://r.example/f/machinelearning2/999/x` | **1.0** (suffix lookalike, same class as report's `/f/technologyfoo`) |
| `http://r.example/f/deeplearningish/1/x` | 1.0 |
| `http://r.example/f/deeplearning` (listing) | 1.0 (report L3) |
| `http://r.example/f/machinelearning?sort=new` / `#frag` | 1.0 (no ref query; predicted query/fragment ignored) |
| `https://r.example/f/machinelearning/999/x` | 1.0 (scheme dropped) |
| `http://r.example:9999/f/machinelearning/999/x` | **0.0** (host:port must match the substituted base) |
| `http://r.example/f/machinelearning/999/x/` | 1.0 |

The decisive URL boundary is the case-sensitive forum path: a canonical `/f/MachineLearning`
post cannot match the `machinelearning` alternative. The audit states this and correctly marks
it `[INFERENCE]`/unproven.

### HTML control (`must_include`, tokenize=False; topic `gan implementation`, repo
`http://gitlab.local:9000/eriklindernoren/PyTorch-GAN`)

| selected text | topic | repo | pair |
|---|---|---|---|
| `organ implementation` | **1.0** | – | – |
| `vegan implementation` | **1.0** | – | – |
| `gan implementations` | 1.0 | – | – |
| `implementation of GANs` | 0.0 | – | – |
| `…/PyTorch-GAN-fork` | – | **1.0** | – |
| `…/PyTorch-GAN/-/tree/master` | – | 1.0 | – |
| `http://evil.example/?next=http://gitlab.local:9000/eriklindernoren/PyTorch-GAN` | – | **1.0** | – |
| `https://gitlab.local:9000/eriklindernoren/PyTorch-GAN` | – | 0.0 | – |
| `git@gitlab.local:eriklindernoren/PyTorch-GAN.git` | – | 0.0 | – |
| `organ implementation - http://gitlab.local:9000/eriklindernoren/PyTorch-GAN-fork` | 1.0 | 1.0 | **1.0** |

The combined last row is the strongest control: the full program_html target returns **1.0** for
a submission that neither discusses GANs (the topic literal is inside the word "organ") nor links
to the required repository (the repo literal is a prefix of a different fork path). This follows
directly from the stated substring semantics; it does not contradict any sentence of
`Task681.md`, but it is a positive-direction consequence the "Not checked" column does not
enumerate (see F681-3).

### Gold-reference casing conflict (strengthens report L1; not overreach)

The report's L1 cites only task 731's navigation URL. Its own census also contains the *gold*
`reference_url` values: `__REDDIT__/f/MachineLearning` at L20026 (599), L20211 (604), L20401 (609),
against lowercase `machinelearning` at 625/681/682/683. Under strict case-sensitive routing, at
least one of those two families' literal references is unreachable for the same forum; under
case-insensitive/redirecting routing, both are. Static bytes cannot decide which. The report's
unproven framing is therefore correct and not exceeded.

### Generator-scope boundary (F681-4)

H1's "exact target" is the **substituted** lowercase `__GITLAB__/…` string. That is only reachable
if the unpinned generator substitutes placeholders inside `program_html.required_contents`; if the
generator is field-scoped (only `start_url`/`reference_url`), the literal stays `__gitlab__/…`
after `clean_answer` lowercasing and the program_html score is permanently 0. The report flags an
unpinned generator and lists substitution as a dependency, but its H1 row states the substituted
string as the exact target without naming this satisfiability branch. No pinned byte decides it;
runtime/generator evidence is required, exactly as the report's "Runtime evidence required"
section says. Not a defect claim.

## Candidate's case-681-specific language

- `webarena-task-spec-audit.md:60` selected IDs: independently recomputed
  `[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]`; 681 is the minimum of stratum
  7, `(('gitlab','reddit'),('program_html','url_match'))`, n=8 (`681..688`). Match.
- `:71` label for 681, "cross-site literals": supported — the required content is a
  `__GITLAB__` URL literal evaluated on the Reddit final page. No phrase or scope exceeds the
  pinned bytes or `Task681.md`.
- `:62` "omit … OR-alternative content checks": independently confirmed 0/16 selected tasks carry
  `" |OR| "` inside `program_html` required content. Task 681's `|OR|` is in `reference_url` (URL
  alternatives), which the candidate does not claim is omitted and which `Task681.md` actually
  witnesses. No excess.
- Candidate metrics independently reproduced from raw JSON: 812 tasks/ID 0-811; evaluator-type
  sets 325/282/66/10/129; 27 strata; targets 651 = 188 exact_match + 463 must_include; locators
  105/524/22; target URLs 238 last/338 navigation/75 helper; string operators 45/176/118; 16
  build reports present for the 16 selected IDs. Adjacent check: all 36 `fuzzy_match == "N/A"`
  tasks carry only that key, supporting the candidate's N/A-assignment sentence.
  Not re-run (out of my assignment): `benchmark_spec_audit.py --summary/--selftest`,
  `--json` receipts, and registry/C2 counters.

## Findings

- **F681-1 (low, precision):** loose task anchors at L9268/L12289 (task_id lines; values at
  L9284/L12308). No mapping or numeric conclusion changes.
- **F681-2 (low, precision):** key name "storage" vs raw `storage_state` (L23369). Value correct.
- **F681-3 (low/medium, completeness):** the "Not checked" column does not spell out the
  positive-direction substring behavior demonstrated above (cross-word topic match, repo prefix
  such as `PyTorch-GAN-fork`, URL embedded as a query value). The report does say "substring
  test", so no statement is false; the unchecked inventory is under-enumerated for an auditor who
  needs the exact accept-set. L1 may append the control, but the pinned source already supports it.
- **F681-4 (boundary, not defect):** the H1 target's existence depends on the unpinned generator
  substituting placeholders inside `program_html.required_contents`; the report declares the
  generator unpinned and lists substitution as a dependency, so this is a disclosed unknown, not
  a contradiction.
- **F681-5 (support, not defect):** L1 under-cites the strongest evidence it already censused — the
  uppercase *gold* `reference_url` values at L20026/L20211/L20401 versus the lowercase family at
  625/681/682/683. This is a two-sided case conflict, still runtime-undecided; the report's
  `[INFERENCE]` framing is correct.

No claim in `Task681.md`, and no case-681-specific sentence in the frozen candidate, is
contradicted by the hash-verified pinned bytes. The intent→evaluator mapping is total for the
task's clauses, the operators and anchors are exact, and the candidate's label/metrics/selection
statements for this case are supported. Task validity remains **UNDETERMINED**; nothing here is
a runtime-invalid task finding, and no site/DOM/reset/generator evidence was gathered.

**VERDICT: PASS** (scoped to BUILD case681 and the candidate's case-681-specific language; no
falsifying defect found; F681-1..4 are non-contradicting precision/completeness notes for L1,
F681-5 is supporting evidence).
