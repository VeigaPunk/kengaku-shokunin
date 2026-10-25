# Round 29 — draft lesson and mistake (proposal only, not admitted)

Status: DRAFT. Writer seat KengakuR28.R29DraftLesson-2. Not canonical. Not a lesson file, not a QUALITY,
SOURCES, or knowledge edit. No row here is admitted, and no witness below has been executed.
Baseline ed26bdf5d924755697cd6812129be2fa441c42a3; preregistration 31934e5660f1814326c6472eefdfa0c41e642a2f.
Round-29 claim C1 only: lowest legacy novelty7 → canonical coverage/constructs, generated-config projection
capability. Score7 held; calibration8 unchanged. No method, model, runtime-validity, or contamination claim.

## 1. Principal: source-versus-derived attribution in a control

r28 mistakes that bear on this round (their fixes stay credited to r28 and are not re-credited here):

| id | what r28 learned | what it does NOT cover |
|---|---|---|
| M74 | attribution: population pin checked by hash, but the instrument re-read bytes after the check (fixed by retaining authenticated bytes) | does not test whether a derived view matches the upstream operation |
| M75 | attribution: invented defaults and projections in URL-note fields (fixed by separating raw, presence, and effective fields) | separates raw from effective, but says nothing about text-level versus leaf-level operations |
| M81 | reference-drift: citation ranges, false universals, and runtime assumptions in task reports (fixed by dated errata) | a documentation fix; no control was tested against an operation |

Gap these leave open (the principal of this draft): the r29 projection must reproduce an upstream operation whose
unit is the serialized text (`raw.replace(...)` over the whole file), not the decoded JSON leaf. A convenient
derived control — a URL-only, decoded-leaf, one-pass substitution — can agree with the implementation on every
frozen benign input while disagreeing with the source on any input where a placeholder appears outside a URL
leaf or where one replacement's output is another token. Agreement on the benign domain is then mistaken for
source fidelity. The fix would be a control whose failure witness is exactly that disagreement.

Proposed mistake row (provisional label; L1 assigns the final id, and the next free number after M84 is M85):

| id | class | evidence pointer · captured-by | proposed disposition (not executed) |
|---|---|---|---|
| M85 (proposed) | attribution | `plans/fixtures/r29/generate_test_data.py:11-16` applies six whole-text `str.replace` calls; the r29 plan requires an independent oracle that is a URL-only leaf walk. Captured-by: this draft, from source reading only. | Keep the production implementation on serialized text in the source order. Make the independent oracle a second implementation of that same text contract, and add a URL-only single-pass decoded-leaf oracle only as a named *negative control* that must disagree on the cascade and non-URL witnesses below. A control counts only after its witness is observed to fail. |

## 2. Source opening records (structure; rows not written)

Structure for any S-row this round (each field required; the writer must fill every one from an actual opening):

| field | required content |
|---|---|
| row id | next free S-number; round-29 proposed start is S070; a row is written only after its source is opened |
| URL or pinned locator | live URL with commit or pinned local path plus sha256 |
| accessed | ISO date of the actual opening (2026-10-21 for this round) |
| located quote | ≤25 words, checked programmatically with `len(q.split())`; quoted text only, no paraphrase |
| location | line number(s) for code and data; section/paragraph/page for prose; the line is printed by the opening seat |
| opened-by | seat id that actually opened it |
| scope and tier | what the row supports and what it does not; tier A/B/C per SOURCES contract v1 |
| supersedes | older row id if the anchor changes; old row bytes are not rewritten |
| used-by | canonical entries that cite it (empty until admission) |

Candidate sources and status (no row written by this draft):

| candidate | status | note |
|---|---|---|
| `plans/fixtures/r29/generate_test_data.py` (pinned, sha256 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd, 838 bytes) | locally verified this seat by `sha256sum` and `grep -n`; a live re-open by URL is still required before a row | the file is inert data; its wildcard import `from browser_env.env_config import *` (line 5) must never execute |
| Python `json` documentation (`json.loads`, `enumerate`-driven output) | not opened by this seat; no row | needed before any row cites json behaviour |
| workflow README and prepare caller (where `generate_test_data.py` is invoked) | not opened; no row | the r29 plan lists these as required openings before source rows |

Candidate located quotes from the local generator (counts from `len(q.split())`, run by this seat; these are
candidate anchors for a future row, not yet admitted):

| location | exact text | words |
|---|---|---|
| line 1 | `Replace the website placeholders with website domains from env_config` | 9 |
| line 11 | `raw = raw.replace("__GITLAB__", GITLAB)` | 4 |
| line 20 | `data = json.loads(raw)` | 3 |
| line 21 | `for idx, item in enumerate(data):` | 5 |
| line 22 | `with open(f"config_files/{idx}.json", "w") as f:` | 5 |
| line 5 | `from browser_env.env_config import *` | 4 |

Source-scope boundary: these quotes establish what the pinned generator text does, not what a deployed
benchmark config contains, not that its output is runnable, and not that `env_config` values are valid.
`__last_url__` and `__page__` runtime markers are not among the six environment tokens and are not counted.

## 3. Gate candidates

| candidate | decision | reason | flip condition |
|---|---|---|---|
| Lesson: "a control must reproduce the source operation's unit, not a convenient derived view" | defer | the principle is motivated by the r28 pattern and by reading line 11–16, but no URL-only oracle has yet been run against the production projection, so disagreement is unobserved | observed disagreement between the URL-only negative control and the sequential-text production on the cascade or non-URL witness, with the control failing before it counts |
| M85 (proposed) as an admitted mistake row | defer | proposal text is authored; the failure is not observed | the witness in §4 fails when run against the URL-only oracle and passes against the sequential-text oracle, with both outputs recorded |
| Reuse of r28 M74/M75 fixes as credit for r29 projection | reject (double credit) | the r28 fix covered hash/re-read and raw/effective URL-note fields, not text-versus-leaf units | none; r29 credit comes only from its own witness |
| "Frozen 812 × 3 benign projections show the generator's behaviour on the benchmark" | reject | the three profiles are controlled synthetic `*.invalid` fixtures, and the claim covers the offline projection, not any deployed config or runtime | observed projection of deployed configs with its own pinned provenance and a sanctioned runtime check |
| "index equals task_id on the frozen input, so output mapping is correct" | reject as a general claim | `enumerate` maps output filenames by position; equality holds only for the frozen order | shuffled-ID hand witness shows the index behaviour; that witness, not the frozen equality, is the control |
| "Projection increases the novelty score of the method" | reject | it is a local instrument over an already-published generator and does not add a distinct construct | a registered distinct construct with property-matching prior art |
| Writing S070+ rows before opening the sources | reject (procedure) | the plan forbids unopened rows | an opening record with access date and located quote, per §2 |
| Admitting the lesson in this round | defer to L1 | the draft has no observed witness | L1 decision after the round-29 measurements and complete second-seat re-reads |

## 4. Expected failure witness (proposal; NOT run; expected outcomes are predictions)

The witnesses below are hand cases. Each has an expected output that is stated before running, so a later run
can refute it. Nothing here counts as observed evidence.

W1 — later-token cascade (wrong-order witness). Synthetic profile: `GITLAB = "http://gitlab.invalid:1/__MAP__"`,
`MAP = "http://map.invalid:2"`. Serialized input fragment: `{"url": "__GITLAB__/x"}`.
- Sequential-text production (order GITLAB then MAP): expected `{"url": "http://gitlab.invalid:1/http://map.invalid:2/x"}`.
- URL-only single-pass decoded-leaf oracle (no rescan): expected `{"url": "http://gitlab.invalid:1/__MAP__/x"}`.
- Expected result: the two differ. The URL-only oracle is a valid negative control only if it fails this comparison.

W2 — non-URL placeholder (global-versus-URL-only witness). Input fragment: `{"intent": "open __MAP__ first"}`
with the same profile as W1 but MAP is `http://map.invalid:2`.
- Sequential-text production: expected `"intent": "open http://map.invalid:2 first"` (non-URL field changed).
- URL-only oracle: expected unchanged `"open __MAP__ first"`.
- Expected result: differ. Forecast F3 ("global replacement changes at least one non-URL field" on the real
  812) is a separate prediction; W2 only tests the mechanism.

W3 — serialized-text quote (domain disclosure). Profile value `http://q.invalid:3/"a"`. Text replacement yields
invalid JSON (`json.loads` raises). Expected: projection reports `projection_json_invalid` and does not repair the
text. Leaf-level oracle expected to succeed. This is the documented domain boundary; it is not a defect of the
production implementation.

W4 — index-versus-task_id (output mapping). Raw list in order `[task_id 5, task_id 2]`.
- Expected filenames: `0.json` holds task_id 5 and `1.json` holds task_id 2 (`enumerate` index, not `task_id`).
- Expected result: differs from a task_id-keyed mapping; this is the shuffled-ID hand witness the plan requires.

W5 — missing or non-string map entry. Expected: `profile_missing_key` or type finding; no fallback value. Not
claimed as exhaustive.

Each witness is a fixture file to be written later by its owner, with its expected output persisted, and each must
be observed to fail against the negative-control oracle before the control counts. This draft writes no fixture and
no code.

## 5. Unknowns and boundaries

- Unobserved: every expected output in §4; F1–F5 forecasts; whether the pinned `test.raw.json` contains
  placeholders in non-URL fields ([INFERENCE] from the generator text only).
- Source versus runtime: the generator text is source. Nothing here observes runtime config, a benchmark
  deployment, browser behaviour, or task validity.
- No credential, environment value, cookie, profile store, or private URL is recorded. Profile strings are
  synthetic `*.invalid` values.
- No double credit: M74/M75/M81 remain credited to r28. The proposed M85 is not credited anywhere until observed.
- Pending: Python `json` docs and the workflow README/prepare caller must be opened before any row cites them.
