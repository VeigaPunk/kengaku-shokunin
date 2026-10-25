writer: KengakuR29-2.FCritNovelty-2

# FCritNovelty — is the round-29 projection a new construct or established practice?

Seat FCritNovelty (critic, judged on novelty), actual writer KengakuR29-2.FCritNovelty-2. Lane master
`git rev-parse HEAD` = 56fd949a6478342531e61f4feecb4a685d831640. Candidate under attack
`.ufo/waves/round-29/drafts/webarena-config-projection.md` sha256 7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc
(matches the freeze). Prereg `plans/round-29-claims.md` sha256 6b4ffee35ddf706a4a77e9daf9c647cbd85b484f8b652b7dbd84dbd6289e92c1.

**Production source:** I did NOT read `plans/config_projection.py`. I ran it read-only once
(`python3 plans/config_projection.py --summary`, exit 0, 47 lines, saved as
`scratch/falsify/FCritNovelty/instrument-summary.stdout`). All other numbers come from my own scripts over pinned
or fetched bytes.

**Tooling:** no installs or updates. Used python3 (stdlib), curl, sha256sum, grep, cmp. No pacman, no REA MCP.

## Axes named

- **novelty**: is the projection itself a new construct, or established public practice, and does "score 7 held" survive?
- **provenance honesty**: does the candidate fail to mention prior practice that bounds what it claims?
- **scope transfer**: do the candidate's decision-rule claims hold for the main public consumers of the same raw file?

## Bounded prior-art search

Question: do public WebArena forks or harnesses (BrowserGym, VisualWebArena, WebArena-Verified) already perform
or audit the same placeholder projection over the same raw task file?

- **Identified 30 fetches, all opened.** The count is the 30 manifest entries and 30 files in `fetch/`. One URL returned 404 (`pypi.org/pypi/webarena`, wrong package name). The
  real BrowserGym dependency is `libwebarena==0.0.5` (`bg_wa_requirements.txt:2`).
- **Manifest:** `scratch/falsify/FCritNovelty/fetch-manifest.txt` has the URL, HTTP status, byte count and sha256
  for each fetch. Access time was 2026-10-21T16:47:59Z onward.
- **Repository heads:**

| repository | main head | date |
|---|---|---|
| webarena | dce04686… | 2025-11-26 |
| BrowserGym | 4ccc7233… | 2026-10-21 |
| VisualWebArena | 89f5af29… | 2024-11-09 |
| WebArena-Verified | 6473f72d… | 2026-02-07 |

- **GitHub issue searches:**
  - `repo:web-arena-x/webarena generate_test_data`: total_count 0.
  - `repo:web-arena-x/webarena __SHOPPING__`: total_count 0.
  - `repo:ServiceNow/BrowserGym test.raw.json`: total_count 2. Issue #407 is an evaluator empty-read audit. Issue #66 is about custom tasks.
- **Included as prior-art evidence:**
  - BrowserGym webarena `task.py` and `instance.py`
  - BrowserGym visualwebarena `task.py`
  - the `libwebarena` 0.0.5 wheel
  - VisualWebArena `scripts/generate_test_data.py` and its `test_webarena.raw.json`
  - WebArena-Verified `types/config.py`, `test_dataset_integrity.py`, `assets/dataset/test.raw.json` and `webarena-verified.json`
  - WebArena `run.py` at the pin
- **Stop rationale:** the three named ecosystems were each opened at their WebArena config entry point. Each
  answered the question with source lines.
- **No global absence claim.** I did not search papers, PyPI broadly, or other forks (for example WebArena-Lite,
  AgentLab).

## Observed facts (command output)

1. **The same raw population is shipped byte-identically by two public consumers.**
   - The sha256 is 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 for all of these: the lane pin
     `plans/fixtures/r28/webarena/config_files/test.raw.json`, webarena main, WebArena-Verified
     `assets/dataset/test.raw.json`, and `webarena/test.raw.json` inside the `libwebarena-0.0.5` wheel (wheel sha256
     5cfdf8ab… equals the PyPI digest).
   - VisualWebArena's copy differs: sha256 fb1e4273…, same 880776 bytes. 810 of 812 task objects are equal. Tasks 240
     and 353 differ only in `instantiation_dict`/`intent` ("competative" vs "competitive"). Token counts are identical
     (385/336/281/300/0/133).
2. **The projection operation itself is published practice in BrowserGym.**
   - `bg_wa_task.py:55-69` reads `test.raw.json` as text, then runs one serialized-text `replace` per token, then `json.loads`.
   - Line 66 quote (4 words): `all_configs_str = all_configs_str.replace(pattern, self.webarena_instance.urls[url_key])`.
   - The dict order at `:58-65` is GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP. This is identical to the
     pinned generator's `plans/fixtures/r29/generate_test_data.py:11-16`.
   - VisualWebArena's generator (`vwa_generate_test_data.py:21-29,54-62`) does the same text replacement plus
     `enumerate` filenames, and adds `__HOMEPAGE__`. That token occurs 0 times in the pinned raw file.
3. **BrowserGym does not use the enumerate-index naming.**
   - It selects by ID at `bg_wa_task.py:82` (11 words): `task_configs = [conf for conf in all_configs if conf["task_id"] == task_id]`.
   - It then writes the single selected config to a tempfile (`:97-101`).
   - The index-consuming path is upstream `run.py:420-423` (1-word quote `test_file_list.append(f"config_files/{i}.json")`).
4. **Own re-typed rule comparison** (`scratch/falsify/FCritNovelty/consumer_compare.py` → `.stdout`). It uses
   synthetic `*.fcritnovelty.invalid` values and imports no upstream or lane code.
   - On the frozen order, the generator's per-index objects equal BrowserGym's task_id selection for 812 of 812 tasks.
     index==task_id holds for 812.
   - After a seed-29 shuffle, generator index==task_id holds for only 3. BrowserGym's selection still equals the frozen
     generator object for 812 of 812.
5. **WebArena-Verified uses a different published design.**
   - It renders per value, only when the value starts with the site placeholder: `wav_types_config.py:198` (3-word
     quote) `if not url_template.startswith(site.url_name_template):`, then replaces at `:207`. It also derenders
     (`:209-228`).
   - In its re-authored `webarena-verified.json` (812 tasks, index==task_id 812), the 1619 token-bearing leaves sit
     under `start_urls`, `expected.url`, `headers.referer` and `post_data`. 0 sit under any `must_include` path
     (`wav_census.stdout`).
6. **My census of WebArena-Verified's byte-identical raw file matches the candidate.** It gives 1435 occurrences,
   1416 token-bearing leaves and 61 leaves on non-URL key paths (60 `must_include[]`, 1 annotation). This matches
   candidate lines 41-46 and instrument summary lines 18-19 (`non_url_field 61, url_field 1355`). No mismatch.
7. **Value shape of the 61 "non_url_field" leaves** (`nonurl_shape.stdout`).
   - All 61 start with a token. The 60 `must_include` values have no whitespace. Example task 552:
     `'__REDDIT__/f/space/134164/…'`.
   - The 1 annotation (task 66) is two comma-separated relative URLs.
   - Across all 1416 token-bearing leaves, 0 do not start with a token.
   - A hypothetical WebArena-Verified-style prefix render applied to every leaf of the pinned raw file differs from the
     generator on 0 of 812 tasks and leaves 0 token occurrences.
8. **No round-29 entry exists in the `corpus/SOURCES.md` "Search log" section** (entries at lines 107-118 end with
   "Round28 task-spec…" at :118). The build-wave prior-art seat R29CritPriorArt is recorded dead with `"report": null`
   (`build-dead-seats.json:161-167`). Rounds 26 and 28 both carry tooling or task-spec search-log entries (:117, :118).
   The candidate has 0 case-insensitive hits for `browsergym|webarena-verified|visualwebarena|prior`.

## Attack and verdicts on the novelty-7-held statement

**Counterexample A (strongest): the projection is not a new construct.**
- BrowserGym performs the identical ordered serialized-text projection over byte-identical raw bytes on every task
  instantiation (facts 1-2). The VisualWebArena generator does the same.
- The round's statement survives: score 7 is held and no +1 is sought. The rubric's +1 needs a construct "the lane
  could not previously observe" and a prior-art verdict (`SCORECARD.md:244`; quote 10 words: "the claim carries a
  prior-art verdict with a fetched URL").
- The lesson draft already says (`drafts/lesson-and-mistake.md:81`, 16 words): "it is a local instrument over an
  already-published generator and does not add a distinct construct".
- Classification: **no defect in the score**. Prior art strengthens "held".
- What is lane-new [INFERENCE, bounded to the opened sources]: the *audit* layer, not the projection. That layer is
  per-occurrence codepoint provenance, unit-separated census, three synthetic sensitivity profiles, the shuffled-index
  witness and the independent oracle. None of the opened consumers or tests computes it. WebArena-Verified's
  `test_dataset_integrity.py:15-141` checks count, site, intent-template rendering and evaluator presence, not
  placeholder projection.

**Mismatch N1: candidate omits prior practice** (fixable defect, provenance honesty).
- Location: candidate lines 10-13. Quote (12 words): "The acquired repertoire is an **offline, source-faithful
  projection** of the pinned generator".
- The candidate reads as if the projection were the acquisition. Public consumers already do it in-process (facts 2-3).
- Value: 0 prior-art mentions in the candidate (fact 8).
- Smallest safe correction: add one sentence to "What this adds". It should say the text projection is established
  practice, citing BrowserGym `task.py:55-69` (same order, same raw sha256) and the VisualWebArena generator `:54-62`.
  It should say the lane acquires an audited census of that projection. No novelty claim and no absence claim.

**Mismatch N2: decision rule overgeneralizes to "a WebArena run"** (fixable defect, scope transfer).
- Location: candidate line 70. Quote (15 words): "Before interpreting a WebArena run, reproduce its generated configs
  from pinned generator and raw bytes".
- Also line 72-73. Quote (11 words): "compare per-task filenames with `task_id` whenever the raw order may differ".
- Counterexample: BrowserGym-hosted WebArena runs never call `generate_test_data.py`. They select by `task_id`
  (`bg_wa_task.py:82`), so step (3) does not apply. My shuffle comparison keeps 812/812 identical objects under
  BrowserGym while the generator's index==task_id falls to 3 (fact 4).
- Steps (1), (2) and (4) do transfer on the frozen population. [INFERENCE: same bytes and same order; I did not
  execute BrowserGym.]
- Smallest safe correction: scope the rule to "runs that consume generator output by index (`run.py:420-423`)". Add:
  "harnesses that select by `task_id` (e.g. BrowserGym `task.py:82`) need only checks 1, 2 and 4".

**Mismatch N3: the "non-URL fields" headline holds only under a key-path reading** (fixable wording, already captured as M89).
- Location: candidate line 56 (6 words): "Global text replacement reaches non-URL fields." Also line 56-57 (7 words): "61
  changed leaves are `must_include` answer strings".
- Value: all 61 are URL-valued strings beginning with a token (fact 7). A published value-prefix renderer
  (WebArena-Verified `config.py:198-207`) would produce generator-identical output on 812/812 tasks.
- So the generator-versus-"URL-only" distinction separates only a *key-path-scoped* reimplementation. It does not
  separate a value-scoped one. "Answer strings" mislabels URL paths.
- The F3 category problem is already captured as mistake M89 (`corpus/lessons/round-29.md:17`, untracked in the lane
  working tree per `git status`). The candidate's line 56-57 wording is still unchanged.
- Smallest safe correction: replace "answer strings" with "URL-valued strings under non-URL keys". Add: "a
  value-prefix renderer is equivalent on this population; only key-path-scoped substitution diverges".

**Open precondition (not a defect yet): no round-29 search-log entry.** Prereg `:90` (8 words): "Search log is
bounded, no global absence/novelty claim." There is no r29 row in SOURCES.md Search log, and the prior-art seat died
(fact 8). S070-S073 are still `queued`, so this may be appended at admission; I do not count it as a failure.
Smallest safe correction: append one bounded r29 Search-log entry. It should include this report's question,
identified/opened counts, issue-search totals and stop rationale, and no global absence claim.

**Tradeoff (must not be "fixed" by changing semantics).** The positional-filename and global-text semantics are
faithful to the pinned generator. BrowserGym's task_id lookup and WebArena-Verified's prefix render are different
designs. Making the instrument adopt either would break source-faithfulness (prereg `:42-46`). Corrections N1-N3 are
wording or scope only.

## Impacted axes

- **novelty:** unharmed. Prior art confirms "held 7". There is no argument for an increase, or for a decrease below
  the existing anchor.
- **provenance and scope (coverage/constructs wording):** N1 and N2 are fixable before admission.
- **calibration:** N3 interacts with F3. It is already ruled under M89, so no new calibration finding.

## Not done / limits

- I did not execute BrowserGym, VisualWebArena, WebArena-Verified or upstream code. Rule comparisons are my own
  re-typed implementations of the quoted lines.
- No paper search and no other forks. No claim that no audit tool exists anywhere.
- I did not read production source.
- Issue #407's author identity relative to this fleet is unknown and not used.

Artifacts (my scratch only): `.ufo/waves/round-29/scratch/falsify/FCritNovelty/` contains `fetch/` (30 fetched
files), `fetch-manifest.txt`, `consumer_compare.py`/`.stdout`, `wav_census.py`/`.stdout`, `nonurl_shape.py`/`.stdout`
and `instrument-summary.stdout`.

VERDICT: PARTIAL
