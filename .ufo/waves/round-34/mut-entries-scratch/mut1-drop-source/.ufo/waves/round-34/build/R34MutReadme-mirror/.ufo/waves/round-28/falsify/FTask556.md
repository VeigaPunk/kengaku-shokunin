# FTask556 — falsification of BUILD case 556 and of the candidate's 556-specific language

Seat: `KengakuR28.FTask556` (author-side scout). Read-only over production. No browser, no
network, no benchmark-site request, no upstream import/eval/execution, no scorer run.
No tool installs. Writes: this report only.

## Candidate identity

- Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
  sha256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (rehashed this run).
- Canonical path `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted**.
  Nothing here is an admission, a validity seal, or a round-level PASS.
- Candidate bytes examined for 556: line 60 (selected IDs) and line 72 (556 row
  `Task556.md … README substrings`). No other 556-specific claim exists in the candidate.

## Source anchors (pinned local bytes only; no live fetch)

- S061 `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json` — accessed 2026-10-21 via `plans/fixtures/r28/webarena/`, sha256 `7b50386f…37652` (= manifest).
- S062 `…/dce04686…/evaluation_harness/evaluators.py` — accessed 2026-10-21, sha256 `e23edb39…0c22` (= manifest).
- S063 `…/dce04686…/evaluation_harness/helper_functions.py` — accessed 2026-10-21, sha256 `ec758da4…e275` (= manifest).
- LICENSE sha256 `c71d239d…0ab4` (= manifest), Apache License 2.0 header observed.

All four fixture digests were re-derived and match `manifest.json` exactly. The manifest records
`upstream_revision` and `opened: 2026-10-21`; it does **not** record the commit date `2025-11-26`,
which comes from the round context and the audit-summary LIMIT line, not from fixture bytes.

## Verified against raw task_id 556 (S061:18041–18082)

Observed: `task_id` 556 (L18041), `intent_template_id` 87 (L18082), `sites` `["gitlab","wikipedia"]`,
`require_login` true, `storage_state` `./.auth/gitlab_state.json`, `start_url` `__GITLAB__`,
`require_reset` false; `eval_types` `["program_html"]`; `reference_answers` null; `reference_url` "";
one `program_html` target (L18061) with URL `__GITLAB__/byteblaze/nolan_honest_fans/-/raw/main/README.md`,
`locator` "" and `required_contents.must_include` at L18064–L18076, 12 items in the exact order
claimed. Intent at L18051 is character-for-character the quoted string.

Stratum census (independent jq/python over S061): the `(gitlab,wikipedia ; program_html)` stratum
contains exactly `[556,557,558,559,560,561]`; 556 is its minimum and is the 9th selected group
(index 8 of the first 16 lexicographically sorted `(sorted site set, sorted evaluator-type set)`
tuples). An exact tuple-sort reproduction returns
`[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]`, byte-identical to
`selected-task-ids.json` and to candidate line 60. Supported.

## Verified evaluator/helper mapping (S062, S063)

Supported line by line: router `case "program_html"` at L369–370; `EvaluatorComb` product at
L348–351; one evaluator constructed, so `StringEvaluator`/`URLEvaluator` never run and
`reference_answers: null` + empty `reference_url` are unread. HTML path: `if target_url.startswith("func")`
L263 false; `if target_url != "last":` L271, `page.goto(target_url)` L272, `time.sleep(3)` L273;
`if not locator.strip():` L276, `selected_element = page.content()` L277;
`selected_element = html.unescape(selected_element)` L303; `elif "must_include" in ...` L312;
`content.split(" |OR| ")` L316 (none of the 12 items contains the delimiter);
`StringEvaluator.must_include(ref=content, pred=selected_element, tokenize=False)` L319–323;
`score *= float(cur_score)` L327. `clean_answer` L80–86 strips one outer quote pair and lowercases;
`must_include` L98–111 returns `float(clean_ref in clean_pred)` at L111. Twelve boolean factors
multiply, so the score is binary. `helper_functions.py` is unreachable for 556 (no `func` URL, no
`func:` locator, no fuzzy/ua branch); no LLM judge, trajectory, or final answer is read.
`__GITLAB__` is not substituted anywhere in S062; the fixture contains no generator or `run.py`,
so the substituted config is indeed outside the snapshot, as the build states.

`556`'s 12 items equal `557`'s six items followed by `558`'s six items — not merely a set union:
`557 = [Following, Memento, Insomnia, Batman Begins, The Prestige, The Dark Knight]`,
`558 = [Inception, The Dark Knight Rises, Interstellar, Dunkirk, Tenet, Oppenheimer]`.

## Falsifications (each reproduced from pinned bytes)

### F1 — decisive: the sibling-557 overlap claim is false (Task556.md:85)

Build line 85: "The same "The Dark Knight" overlap exists in sibling 557, and 556's list equals the
union of 557 and 558, which shows the reference was assembled from the same list."

Second clause is true (indeed exact ordered concatenation). First clause is false. S061 sibling
records: 557's required contents are the six items above and **do not contain**
"The Dark Knight Rises" (`'The Dark Knight Rises' in 557_items == False`), so no within-557
substring overlap exists. The overlap the build names exists in 556 itself and in sibling **561**,
whose list (`Batman Begins, The Dark Knight, Inception, The Dark Knight Rises, Interstellar,
Dunkirk, Tenet`) contains both strings. This is a reproducible source misattribution, not a
wording preference; it is the decisive control for this case because the whole sentence is a
source-comparison claim. It does not alter the 556 operator map or the UNDETERMINED validity
status, but it must be corrected before Task556.md is used as an anchor.

### F2 — intent word count is 15, not 16 (Task556.md:21)

Line 21 says the quoted intent is "(16 words)". The pinned L18051 string splits on whitespace into
15 tokens (`Create a repo named nolan_honest_fans with movies directed by Christopher Nolan in a
README file`). Numeric drift of the M72 class; the quote itself is exact.

### F3 — "only replace call" is false (Task556.md:65)

Line 65: "The only replace call is `__last_url__` at L265, confirmed by grep." S062 has a second
replace: `func = func.replace("__page__", "page")` at **L298**. The substantive claim in the same
bullet — `__GITLAB__` is never substituted in the pinned evaluator, so scoring needs a generated
config outside this snapshot — remains true. The `__page__` branch is inside the `func:` locator
branch and is unreachable for 556 (empty locator), so the mapping conclusion is unaffected.

### F4 — `HTMLContentEvaluator.__call__` anchor is off (Task556.md:29)

Line 29 cites "`HTMLContentEvaluator.__call__` L259–333". The `def __call__` is at **L248**;
the body opens at L255 (`with open(config_file, "r")`), and `targets = configs["eval"]["program_html"]`
is L258. L259 is blank, and the cited range excludes the `targets` line the next sentence relies
on. Candidate S062:258–333 is the correct body range. Anchor error only.

### F5 — two bounded overstatements in the case table / dynamic-state notes

- Task556.md:44 ("Create a repo"): "Only the existence of a readable file at the URL is checked."
  The actual score input is the twelve substring predicates over the fetched DOM; a reachable page
  without those strings scores 0. Playwright resolves a 4xx navigation to a response rather than
  raising, so "successful `goto`" is not the scored condition either [INFERENCE: Playwright 4xx
  behavior is outside the pinned bytes]. The cell's conclusion — no episode-creation check — is
  correct.
- Task556.md:71: "an earlier run **or sibling evaluation**" leaving `nolan_honest_fans`. All six
  template-87 siblings (556–561) target distinct repo slugs (`nolan_honest_fans`, `nolan_old_fans`,
  `nolan_young_fans`, `nolan_followers`, `nolan_academy_awards`, `bafta_awards_nolan`); a sibling
  evaluation is not a supported mechanism for leaving this slug. An earlier run of 556 itself is.
  Still an inference, but the named mechanism is unsupported by the sibling rows.

## Decisive boundary / control

**C1 (sibling-list control).** Recompute exact `must_include` membership for 556/557/558/561 from
S061: `557 ∩ {"The Dark Knight","The Dark Knight Rises"} = {"The Dark Knight"}`;
`558 ∩ … = {"The Dark Knight Rises"}`; `561 ∩ … = both`; `556 ∩ … = both`. This flips F1's
attribution while confirming the union/concatenation claim. No runtime needed.

**C2 (predicate-closure control).** Using only the quoted `clean_answer`/`must_include` semantics
(tokenize=False), cleaned references are compared by substring: `"the dark knight"` is a strict
substring of `"the dark knight rises"`. Therefore, for **every** possible page P, satisfying the
"The Dark Knight Rises" item implies satisfying "The Dark Knight"; this item is permanently
non-discriminating, stronger than the report's "can still score 1 … natural wording" phrasing at
line 83. Independent thresholds observed with pairwise witnesses (not a complete answer payload,
which would be a bypass recipe): `"Following"` matches `"the following list"` but not
`"the films below"`; `"Tenet"` matches `"tenets"`; `"The Dark Knight"` matches
`"The Dark Knight Rises"`. So 556 has 12 declared items but at most 11 independently discriminating
ones (and 2 more are satisfiable by incidental prose). Static predicate property, not a score.

**C3 (selection-rule control).** Exact lexicographic tuple sort over 27 strata reproduces the 16
selected IDs and 556's minimum/position; supports the build's stratum sentence and candidate line 60.

**C4 (replace-call control).** `grep -n 'replace('` on S062 yields exactly L265 (`__last_url__`) and
L298 (`__page__`), refuting F3's absolute while leaving its main claim true.

## Independent census corroboration (candidate numbers)

Derived with stdlib/jq directly from S061 before reading the delivered receipt; the delivered
`corpus/evidence/round28-calibration/audit-summary.txt` agrees on every counter. I did **not** rerun
`benchmark_spec_audit.py` or its selftest (no unassigned test), so the selftest-21 and `--json`
claims are not re-executed here.

| observable | observed | candidate |
|---|---|---|
| tasks / distinct IDs (range) | 812 / 812 (0–811) | 812 / 812, 0–811 |
| evaluator-type sets | 325 / 282 / 66 / 10 / 129 | same |
| site/evaluator strata / selected | 27 / 16 | 27 / 16 |
| selected IDs | exact tuple-sort match | exact match |
| page-content targets | 651 | 651 |
| exact_match / must_include targets | 188 / 463 (both=0, other=0) | 188 / 463 |
| locator classes full/JS/helper | 105 / 524 / 22 | 105 / 524 / 22 |
| URL classes last/navigation/helper | 238 / 338 / 75 | 238 / 338 / 75 |
| string operator tasks | 45 / 176 / 118 | 45 / 176 / 118 |

Because no target carries both `exact_match` and `must_include`, the candidate's "effective
operators" denominator is exact even though the source uses `if exact_match / elif must_include`.
No aggregate candidate number failed. LICENSE Apache-2.0 is retained and matches the manifest.
Credential-like strings in S061 are task prose (`token`, `Cookie`, `Secret` in intents/headings),
not account/token/cookie values; the fixture contains only `.auth/*_state.json` path strings and
no auth-state files, consistent with the candidate's access statement.

## Candidate's 556-specific language

Candidate line 72 says only `README substrings` for 556. That is within S061/S062: the target is a
README raw URL and the operator is substring containment. The candidate's line 60 selection is
exactly reproducible. The candidate makes no 556 claim about sibling 557, so F1 is a defect of
`Task556.md`, inherited only through the candidate's reference to that audit path; it does not
expand the candidate's own 556 prose beyond source. No site request, no browser, no scorer.

## Remaining unknowns (not resolved by static bytes)

1. The generated config that substitutes `__GITLAB__`, and its generator revision.
2. Live GitLab default branch, raw-endpoint `Content-Type`/`Content-Disposition`, and the identity
   behind `gitlab_state.json` (auth state not opened).
3. Absence of `nolan_honest_fans` at episode start / reset log (`require_reset: false`).
4. The offline Wikipedia's Christopher Nolan filmography, specifically Oppenheimer.
5. Chromium's `page.content()` wrapping of raw text/plain and GitLab's actual raw serving.
6. The `2025-11-26` commit date: not in fixture-manifest bytes; supplied by round context and the
   audit-summary LIMIT line.

Task validity therefore remains **UNDETERMINED**: this is a static spec audit, not proof of a
runtime-invalid or runtime-valid task. No browser action or bypass demonstration was performed.

## Verdict

**VERDICT: PARTIAL.** The core intent→target/operator/unchecked-clause mapping for task 556, the
helper/judge unreachability, the binary product, the placeholder dependency, the stratum/selection
facts, all case-specific candidate metrics, and the candidate's own 556 language (`README
substrings`) are supported by pinned bytes. The build report nevertheless contains one decisive
false source attribution (F1: 557 does not contain "The Dark Knight Rises"; 561 does), one numeric
drift (F2: 15 vs 16 words), one false absolute (F3: a second `replace` at L298), one off anchor
(F4), and two bounded overstatements (F5). L1 should correct F1–F5 before using `Task556.md` as an
admission anchor; none of them changes the task's UNDETERMINED validity status or the candidate's
own 556 prose. No production edit, source admission, or round-level PASS is claimed.
