# FContractURLSchema — falsification of the URL-rule schema contract (round 28, C1)

- **Seat:** KengakuR28.FContractURLSchema (critic, author-side, leaf; no delegation)
- **Date:** 2026-10-21
- **Candidate reread:** frozen draft `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (observed with `sha256sum`). Canonical target `corpus/knowledge/webarena-task-spec-audit.md` is not admitted; I did not read or write it.
- **Instrument:** `plans/benchmark_spec_audit.py`, SHA256 `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8`. Lane git HEAD `18b192266389e8d6c74d0e1f1f2db337739e63dd`, which is the build package.
- **Pinned inputs (observed digests match manifest):** `test.raw.json` `7b50386f…37652`, `evaluators.py` `e23edb39…00c22`, upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`.
- **Scope:** URL matching rule types; empty, missing and unsupported `reference_url`/`url_note`; and whether the static inventory or its prose implies exact URL matching. Not covered here: string/HTML operators, registry (C2), or sources S061–S066.
- **Method:** I hand-derived scorer expectations from pinned `evaluators.py:187–239`. These are `clean_url = str(url).rstrip("/")`, base = `netloc + path`, `ref_base_path in pred_base_paths` (a str-in-str substring test), `parse_qs` query pooling, and `ValueError` for any rule other than `GOLD in PRED`. I re-expressed them with stdlib `urllib.parse` only. No upstream code was imported or executed, no site was contacted, and no browser was used. The production `audit_tasks` ran only on miniature in-memory tasks plus one read-only in-memory call on the pinned raw file. Bytecode was disabled (`-B`, `PYTHONDONTWRITEBYTECODE=1`, `sys.dont_write_bytecode`). The only `__pycache__` in `plans/` predates this seat (03:51/08:54 −0300) and has no `benchmark_spec_audit` entry. I did not rerun `--selftest` or the full suite.
- **Tooling:** no installs or updates. Python 3.14.8 (system).

## Scratch evidence (own seat directory only)

`.ufo/waves/round-28/scratch/FContractURLSchema/`:
- `census.py` → `census.out.json`: independent stdlib census that imports no production code or oracle.
- `probe.py` → `probe.out.json`: 17 miniature URL probes plus one record-provenance probe against production `audit_tasks`.
- `production-metrics.out.txt`: production `url_rules`, `eval_type_orders` and the synthesized-`url_note` count on the pinned raw file.

Commands:
```
S=.ufo/waves/round-28/scratch/FContractURLSchema
PYTHONDONTWRITEBYTECODE=1 python3 -B $S/census.py plans/fixtures/r28/webarena/config_files/test.raw.json > $S/census.out.json   # exit 0
PYTHONDONTWRITEBYTECODE=1 python3 -B $S/probe.py plans/benchmark_spec_audit.py > $S/probe.out.json                              # exit 0
```

## Independent census, reproduced before comparing to production

| observable | independent census | production / candidate | agree |
|---|---|---|---|
| url_match tasks | 205 (66 alone, 10 with string_match, 129 with program_html) | eval-type sets 66/10/129 | yes |
| url_note explicit | 196 × `"GOLD in PRED"`, no other value, no null | `url_rules {"GOLD in PRED": 205}` | yes, but merged (see F2) |
| url_note absent on url_match tasks | 9: tasks 174–182 (scorer default applies) | not distinguished | — |
| url_note on the 607 non-url_match tasks | absent on all 607 | records report `"GOLD in PRED"` (F2) | **no** |
| reference_url on non-url_match tasks | 599 `""`, 7 `null`, 1 non-empty (task 247); never read by the scorer | not flagged; correct | yes |
| OR alternatives per url_match task | 198×1, 3×2, 3×3, 1×4. The raw bytes contain only the exact ` \|OR\| ` delimiter (19 occurrences, no spacing variants) | not inventoried | n/a |
| alternatives with vacuous base after `clean_url` | 0 | 0 findings | yes |
| refs with an explicit scheme | 0; all 205 begin with a `__SITE__` placeholder, so the raw `urlparse` puts it in `path` | — | n/a |
| declared order in 129 combos | url_match before program_html in all 129; 60 of the 129 have at least one navigating (non-`last`) HTML target | `eval_type_orders {"url_match,program_html": 129}` | yes |
| schema findings | — | 0 | consistent |

Every measured URL-related number in the candidate (the 205 url_match tasks across 66/10/129) reproduces. The candidate's prose on the URL rule is also source-correct, including:
- substring containment over netloc+path;
- scheme and fragment ignored;
- query values pooled across alternatives (S062:199–235);
- the "exact URL identity" disclaimer.

The selected case reports (Task044, Task590, Task681, Task377, Task173) describe the rule as a substring test, never as equality. Task377's "equals" applies only to the decoded query value, which is correct per L228–235. **No text implies exact URL matching.**

## Findings

### F1 — Instrument defect (fixable): the emptiness check uses the raw split, but the scorer cleans first, so vacuous alternatives pass as SCHEMA_COMPATIBLE

The audit's check (`benchmark_spec_audit.py:104`) is `any(not alternative for alternative in reference_url.split(" |OR| "))`. The scorer first applies `rstrip("/")` to each alternative (L214), then compares `netloc + path` by substring (L195, L220–227). An alternative whose cleaned base is `""` therefore makes `"" in pred_base` true for every final URL. With no reference query, the score is 1.0 regardless of where the agent ends.

The audit flags only the raw-empty forms (`""` gives `reference_url_invalid`; `"x |OR| "` gives `reference_url_empty_alternative`). Alternatives that are non-empty in raw form but vacuous after cleaning produce **no finding**. Observed in `probe.out.json`:

| reference_url | audit findings | hand-derived scorer base |
|---|---|---|
| `""` | `reference_url_invalid` | vacuous (always 1.0) |
| `__GITLAB__/x \|OR| ` | `reference_url_empty_alternative` | vacuous |
| `/` | **none** | vacuous |
| `__GITLAB__/x \|OR| /` | **none** | vacuous |
| `//` | **none** | vacuous |
| `http://` | **none** | vacuous |
| `?q=a` | **none** | vacuous base; query still checked |
| `#frag` | **none** | vacuous |
| `__GITLAB__/x \|OR| ?q=a` | **none** | vacuous base; `q` pooled onto every alternative |
| `   ` | **none** | vacuous under Python 3.14.8, because `urlsplit` lstrips C0/space. Behavior under older Python versions was not tested [INFERENCE: may differ] |

The same scorer behavior (base check always passes) gets two different audit verdicts. The selftest case `empty_url_alternative` therefore covers a narrower predicate than the hazard it names. Impacted axis: C1 coverage/constructs, specifically instrument contract fidelity.

**Pinned-population impact is zero.** The census found 0 such alternatives, so the measured "schema findings 0" and all counters stand. This is a generality defect in the instrument, not a counter error. It mirrors the pinned scorer's own cleaning step, so it does not require any unsupported public-parser feature.

**Smallest bounded repair:** at line 104, test the cleaned base rather than the raw string:
```python
elif any(not (lambda p: p.netloc + p.path)(urllib.parse.urlparse(a.rstrip("/"))) for a in evaluation["reference_url"].split(" |OR| ")):
```
(Or use a two-line helper `url_base(a)`.) Also `import urllib.parse` and add selftest probes for `"/"` and `"x |OR| ?q=a"`. The finding id can stay, or be renamed `reference_url_vacuous_alternative`. The expected pinned output is unchanged (0 findings).

### F2 — False provenance in per-task records, plus a URL-note inventory the candidate never reports

`benchmark_spec_audit.py:148` writes `"url_note": evaluation.get("url_note", "GOLD in PRED")` for **every** record. On the pinned file, 616 of the 812 records report `url_note = "GOLD in PRED"` even though their raw `eval` has no such key (`production-metrics.out.txt`). Of those, 607 are non-url_match tasks, where the scorer never reads the field (L213–215 sit inside `URLEvaluator.__call__`). The derived field therefore attributes a URL rule to string-only and HTML-only tasks.

`raw_task` is preserved, so no raw field is lost and the candidate's "raw task field is lost" falsifier is not triggered. However, the derived field is synthesized rather than observed. Separately, the `url_rules` counter merges the 196 explicit notes with the 9 defaulted tasks (174–182).

The preregistration (round-28-claims.md:17) lists "URL notes" as an inventory item. The candidate's "Observed static inventory" table has no URL-rule row, and `--summary` does not print `url_rules`. Impacted axes: C1 coverage (inventory completeness) and provenance.

**Smallest bounded repair:**
- Change the record to `"url_note": evaluation.get("url_note", "GOLD in PRED") if "url_match" in kinds else None`, plus `"url_note_defaulted": "url_note" not in evaluation`. Alternatively, count the default under a distinct `url_rules` key.
- Add one candidate table row: `url rules | GOLD in PRED 205 = 196 explicit + 9 defaulted (tasks 174–182); no other value`.

### F3 — Contract disclosure gap (tradeoff, not a counter error): one finding id covers two different runtime behaviors

`reference_url_invalid` covers both cases:
- absent or non-string `reference_url`: the scorer fails when the evaluator is called (`KeyError` at L213, or `AttributeError` on `.split`);
- `""`: the scorer does not fail; it returns base_score 1.0 and query 1.0, so it always passes.

The `scorer_contract.failure_phases` block (line 179) lists `unknown_url_rule` but neither of these cases. The candidate correctly avoids calling either one a task failure. It would be more accurate to state that an empty reference URL is a vacuous acceptance, not an exception. Zero population impact. Repair: add one `failure_phases` entry, `"empty_reference_url_or_alternative": "base check vacuously true; not an exception"`, or a single candidate sentence saying the same.

### F4 — Order hazard has no finding; disclosure only (zero population impact)

A reversed declaration, `["program_html","url_match"]` with a navigating target, is SCHEMA_COMPATIBLE with no finding (probe `html_first_order`). In that case `URLEvaluator` would read the URL the HTML evaluator navigated to (L271–273), not the agent's URL. In the pinned population all 129 combos declare url_match first, and 60 of them have navigating targets, so the order dependency is live but correctly ordered.

The candidate already says "preserve order because page-content checks can navigate", and the JSON keeps `eval_type_orders`. This is acceptable as a disclosed semantic limitation. If wanted, the cheapest strengthening is a candidate sentence: "all129 url_match+program_html tasks declare url_match first; 60 have navigating targets".

### Non-findings (attacked, held)

- **Unsupported rule:** `url_note: "EXACT"` or `null` gives `url_rule_unsupported`, matching the scorer's `ValueError` (L215–239). A present `null` correctly bypasses `.get`'s default.
- **Missing rule:** defaults to `GOLD in PRED`, matching the scorer.
- **Non-string or list `reference_url`:** gives `reference_url_invalid`.
- **Spacing variants of the delimiter** (e.g. `x |OR|y`): not flagged, and the pinned bytes contain none. Not demanded.
- **Placeholder hosts:** raw `__SITE__` URLs parse with an empty netloc. The candidate and case reports (Task590 lines 55–56, Task681 line 40) state this, mark substitution as outside the snapshot, and never treat a raw parse as the scored URL.

## Verdict

All URL-related measured counters and the candidate's prose about URL matching are supported, and nothing in the inventory or its prose implies exact URL matching.

The production instrument has two fixable defects:
- **F1:** vacuous-after-cleaning `reference_url` alternatives pass the schema check, which contradicts the pinned `clean_url`/netloc+path contract.
- **F2:** per-task records synthesize `url_note` on 616 of 812 records, including 607 tasks that have no URL evaluator, and the preregistered URL-notes inventory is missing from the candidate table.

Neither defect changes any pinned counter. F3 and F4 are disclosure-level only. Each finding has a bounded repair above. I made no production edits; L1 resolves these.

VERDICT: PARTIAL
