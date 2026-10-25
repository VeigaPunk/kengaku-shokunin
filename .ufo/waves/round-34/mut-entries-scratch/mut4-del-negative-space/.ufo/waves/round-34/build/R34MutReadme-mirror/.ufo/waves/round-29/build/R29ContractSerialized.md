# R29 source contract — serialized-text replacement before `json.loads` vs decoded-leaf rewriting

**Seat:** `KengakuR28.R29ContractSerialized-2` (actual writer: same; leaf, no delegation)
**Scope:** read-only reconnaissance of the pinned generator's substitution *representation*: six global
`str.replace` passes on serialized text, then parse, versus an oracle that rewrites decoded string leaves.
Escape/domain boundary, hand-expected counterexamples to wrong interpretations, exact word-counted quotes.
**Prereg:** `plans/round-29-claims.md` (C1, one claim). Manifest
`plans/fixtures/r29/manifest.json` sha256 `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`.
**Production edits:** none. **Tool installs/updates:** none (stdlib Python 3, `sha256sum`, `nl` only).
**Writes:** this report only. No `config_files/*` artifact, no scratch output, nothing written to `plans/`.

Boundary rules honoured: the generator was **never imported or executed**; only `ast.parse` of its retained
bytes. `browser_env.env_config` was never resolved, imported, or read. No host env, credential, auth-state,
network or endpoint access. No URL was fetched: the pinned `raw.githubusercontent.com` URL is taken from the
manifest, and all bytes come from the lane-local pinned fixture.

**LSP note (recorded unavailability, not absence evidence):** this seat's tool inventory exposes no `lsp`
device, so `definition`/`references`/`hover` traces were impossible. Semantic claims below rest on
`ast.parse` of the pinned generator plus direct measurement on the pinned fixture bytes. No cold-empty LSP
result is reported as absence.

## 1. Pinned inputs opened (each read once, bytes retained)

| Path (lane-relative, absolute under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/`) | Bytes | sha256 |
|---|---:|---|
| `plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| `plans/fixtures/r29/profiles.json` | 1391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` |
| `plans/fixtures/r29/manifest.json` | 1061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` |

Source URL recorded by the manifest for the generator (accessed/opened as local pinned bytes on 2026-10-21):
`https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py`
at revision `dce04686a56253aefba7b18a4fa0937cf1dc987b`.

Raw fixture is pure ASCII: 880776 bytes = 880776 Unicode codepoints (`all(ord(c) < 128)`), so codepoint and
byte offsets coincide **for this input**; offsets are still reported below as codepoint offsets per contract.
All three frozen profile values are ASCII too, so projected text stays ASCII (3/3 checked).

## 2. Located quotes (exact substrings of pinned bytes; word count = `len(q.split())`, computed)

| Line | Quote (verbatim source line, indentation stripped) | Words |
|---|---|---:|
| 1 | `"""Replace the website placeholders with website domains from env_config` | 9 |
| 10 | `raw = f.read()` | 3 |
| 11 | `raw = raw.replace("__GITLAB__", GITLAB)` | 4 |
| 16 | `raw = raw.replace("__MAP__", MAP)` | 4 |
| 17 | `with open("config_files/test.json", "w") as f:` | 5 |
| 18 | `f.write(raw)` | 1 |
| 20 | `data = json.loads(raw)` | 3 |
| 23 | `json.dump(item, f, indent=2)` | 3 |

Every quote above was tested with `q in src` → `True`. Word counts computed as `len(q.split())`:
9, 3, 4, 4, 5, 1, 3, 3 (each ≤ 25). Lines 11–16 are the six consecutive `raw = raw.replace(...)`
assignments (11 and 16 shown; 12–15 verified identical in shape by the AST walk in §3). Reading order is
line 10 read → 11–16 replace → 17–18 write → 20 parse: the substituted text is written to disk before it
is ever parsed.

## 3. AST-extracted contract — one representation, no decoded-leaf stage

`ast.parse` of the 838 bytes yields one `main()` whose six consecutive assignments (lines 11–16) are
`raw = raw.replace(<Constant str>, <Name>)`, in this order, with these exact literals:

`__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`.

Observed call sites in statement order: `open`(9) → `f.read`(10) → six `raw.replace`(11..16) → `open`(17) →
`f.write`(18) → `json.loads`(20) → `enumerate`(21) → `open`(22) → `json.dump`(23). Imports are only
`import json` and `from browser_env.env_config import *` (line 5, star import; never resolved).

Consequences that follow from the AST alone:

1. The substituted representation is the **serialized file text**. There is exactly one string variable
   (`raw`); `json.loads` consumes the *same* replaced string. The generator has no decoded-value pass, so
   "decoded-leaf rewriting" is an **oracle-side abstraction**, never a source stage.
2. Replacement is representation-blind: it matches any literal occurrence in text — inside any string value,
   inside a key, and (in principle) inside escape-encoded regions — with no field or type filter.
3. Substituted values are **not re-escaped** and not validated: line 18 writes the substituted text to
   `config_files/test.json` *before* line 20 parses it. A projection that breaks JSON is still written.
4. `json.dump(item, f, indent=2)` re-serializes every task, so per-task artifacts are a re-encoding of the
   parsed object, not byte slices of the substituted text (§7).

## 4. Measured census on the frozen raw fixture (units kept separate)

Units: **occurrence** = one literal token match in a string; **leaf** = one JSON string value; **task** = one
array element; **task/profile projection** = one (task, profile) pair. These are never pooled below.

Per-token identity, serialized text vs decoded string values (this is the load-bearing measurement):

| Token | raw-text occurrences | decoded-value occurrences | decoded key occurrences |
|---|---:|---:|---:|
| `__GITLAB__` | 385 | 385 | 0 |
| `__REDDIT__` | 336 | 336 | 0 |
| `__SHOPPING__` | 281 | 281 | 0 |
| `__SHOPPING_ADMIN__` | 300 | 300 | 0 |
| `__WIKIPEDIA__` | **0** | 0 | 0 |
| `__MAP__` | 133 | 133 | 0 |
| **total** | **1435** | **1435** | **0** |

Occurrence distribution by owning field (field name = last string element of the JSON path):

| Field | URL-typed | Occurrences | Tokens |
|---|---|---:|---|
| `start_url` | yes | 818 | GITLAB 196, MAP 128, REDDIT 114, SHOPPING_ADMIN 182, SHOPPING 198 |
| `eval.program_html[*].url` | yes | 338 | GITLAB 132, REDDIT 85, SHOPPING_ADMIN 90, SHOPPING 31 |
| `eval.reference_url` | yes | 217 | GITLAB 49, MAP 5, REDDIT 83, SHOPPING_ADMIN 28, SHOPPING 52 |
| `eval.program_html[*].required_contents.must_include[*]` | **no** | **60** | GITLAB 8, REDDIT 52 |
| `eval.reference_answer_raw_annotation` | **no** | **2** | REDDIT 2 |

So **62 of 1435 occurrences (4.32%)** live in non-URL-typed fields, on **61 leaves** across **18 tasks**
(17 tasks with `must_include` hits: task_ids 552–555, 562–566, 681–688; 1 task with the annotation hit; no
overlap). 13 leaves carry more than one occurrence. 1416 leaves carry at least one occurrence.

Structural identities observed: 812 array elements, 812 distinct `task_id`, all `task_id` integers `0..811`;
`index == task_id` for all 812 (this is the frozen-input fact only, not the shuffled witness, which is a
selftest obligation of the production module, not of this seat).

Token-adjacency and escape checks on the raw text: 0 occurrences are immediately preceded by a backslash;
0 nested/adjacent token pairs matched `__[A-Z_]+__+(?=__)`. `t.count('__SHOPPING') == 581 == 281 + 300`, so
`__SHOPPING__` is **not** a substring of `__SHOPPING_ADMIN__` on this token set — the declared order between
those two is inert here, for a delimiter reason, not by luck of content.

Escape inventory in the serialized raw text: 1335 backslashes total = 1274 `\"`, 12 `\n`, 49 `\uXXXX` over 8
distinct codepoints (`u2019` 19, `u00ee` 8, `u00e9` 6, `u00fd` 6, `u2122` 4, `u2013` 4, `u00f3` 2). **No
`\u005f` (underscore) and no `\u0047`-class escape exists**, so no token on this input can be produced,
split, or hidden by JSON escape decoding. That is why the per-token identity in the table above holds exactly.

Runtime markers are outside the contract and survive every pass: `__last_url__` 65 occurrences and `__page__`
12 occurrences (77 total) remain in all three projected texts (checked 3/3).

Favorite provenance anchors (codepoint offsets into the raw text, first occurrence):
`__SHOPPING_ADMIN__` 172, `__MAP__` 6238, `__SHOPPING__` 20068, `__REDDIT__` 26080, `__GITLAB__` 42249,
`__WIKIPEDIA__` absent.

## 5. Observed equivalence on the frozen population — and its exact domain

In-memory, stdlib-only, six ordered passes on retained text vs a decoded-value six-ordered-pass leaf oracle
(same order, same values), then structural comparison:

| Profile | Tasks | Structure equal to leaf oracle | Remaining six tokens | Runtime markers left |
|---|---:|---:|---:|---:|
| `distinct_origins` | 812 | 812 | 0 | 77 |
| `path_prefix` | 812 | 812 | 0 | 77 |
| `trailing_slash_sensitivity` | 812 | 812 | 0 | 77 |
| **total pairs** | **2436** | **2436** | — | — |

Projected text length (codepoints): 905171 / 915216 / 906606; three distinct texts. These are hand computations
in a Python cell, **not** a run of `plans/config_projection.py` (that path is absent at lane HEAD:
`ls plans/config_projection.py` → "No such file or directory"), and not an oracle-agreement certification for
the delivered module.

The equality is contingent on four conditions, each measured above: (i) every occurrence lies in a decoded
string value, not a key; (ii) no occurrence is escape-produced or escape-split; (iii) substitution values are
JSON-serialization-safe (no `"`, `\`, control characters); (iv) the leaf oracle repeats the six ordered passes
rather than scanning once. Break any one and the two representations diverge — §6.

## 6. Hand-expected counterexamples to wrong interpretations

All cases are 20–60 byte literals written by this seat; stdlib `str.replace`/`json.loads` only; no fixture
write, no upstream import, no production module. "Expected" values are the measured outputs.

**A. Wrong reading: "text replacement is equivalent to replacing placeholders in the data; JSON escapes are irrelevant."**
Escape-encoded occurrence, `{"u": "\u005f_GITLAB__"}` (serialized; decodes to `__GITLAB__`):
- serialized-text projection → text unchanged (no literal `__GITLAB__` present) → `json.loads` → `{'u': '__GITLAB__'}`: a known placeholder **survives** into the output.
- decoded-leaf oracle → `{'u': 'http://gitlab.invalid:10101'}`.
Same with a fully forged escape form `{"u": "\u005f\u005fGITLAB__"}` → text path leaves `{'u': '__GITLAB__'}`.
So "0 remaining placeholders" is a claim about *this* input's ASCII serialization, not about the token set.

**B. Wrong reading: "a substituted value can never break the document."**
`{"u": "__GITLAB__", "n": 1}` with `GITLAB = http://x.invalid/a"b` → text
`{"u": "http://x.invalid/a"b", "n": 1}` → `json.JSONDecodeError: Expecting ',' delimiter` at pos 26.
With `GITLAB = C:\new\path` → `{"u": "C:\new\path", "n": 1}` →
`json.JSONDecodeError: Invalid \escape` at pos 13. With a tab in the value →
`json.JSONDecodeError: Invalid control character` at pos 25. The decoded-leaf path escapes and stays valid.

**B3. Stronger: a value can restructure the document and still parse.**
`GITLAB = x","evil":"y` → `{"u": "x","evil":"y", "n": 1}` → parses to `{'u': 'x', 'evil': 'y', 'n': 1}`.
A "json.loads succeeded, therefore the projection is faithful" check is therefore unsound; the audit needs
per-field provenance, not just parse success. This is also why the write at line 18 can land a
semantically restructured `test.json` before line 20 ever validates it.

**C. Wrong reading (present in the sibling design doc, refined here): "cascade distinguishes serialized from decoded-leaf."**
With `GITLAB = http://g.invalid/__MAP__`, `{"a":"__GITLAB__","b":"__MAP__"}` → both paths produce
`{"a": "http://g.invalid/http://map.invalid:10106", "b": "http://map.invalid:10106"}`, because cascade is a
property of *repeated ordered passes*, not of representation. A decoded-leaf oracle that also performs six
ordered passes agrees; only a **single-scan** leaf oracle diverges. Cascade is asymmetric in the other
direction: `MAP = http://m.invalid/__GITLAB__` leaves `http://m.invalid/__GITLAB__` intact, since `GITLAB`
ran first. Any oracle must declare "six ordered rescans" or "single scan", not "text vs leaf".

**D. Wrong reading: "every `__…__` is an environment placeholder."**
`{"a":"__last_url__","b":"__page__"}` is unchanged by all six passes, and 77 such markers survive in every
frozen projected text. A generic `__[A-Za-z0-9_]+__` sweep would corrupt runtime markers; the contract is the
closed set of six literals. Raw placeholder vocabulary observed: exactly the six tokens plus `__last_url__`
and `__page__` (7 distinct `__…__` forms, no others).

**E. Wrong reading: "keys and values are both 'leaves', so text and leaf rewriting agree."**
`{"__GITLAB__url": "v"}` → text path yields key `http://gitlab.invalid:10101url`; a values-only leaf oracle
leaves `__GITLAB__url` intact. Zero such key occurrences exist on the frozen input, so this divergence is
latent, not observed; an oracle's domain statement must say *values only* explicitly.

**F. Wrong reading: "all six replacements are exercised on the frozen input."**
`__WIKIPEDIA__` has **0 occurrences**. Substituting a completely different `WIKIPEDIA` value
(`http://totally-different.invalid:9/x`) changes **no projected byte** (`False` on equality test), while
changing `MAP` does (`True`). So the source has six passes, the population exercises five token classes, and
the occurrence census must report 0 for `__WIKIPEDIA__` rather than implying six active substitutions.

## 7. Serialization boundary: projected text is not the per-task artifact

`json.dump(item, f, indent=2)` (default `ensure_ascii=True`) re-encodes each parsed task. Measured on
`distinct_origins`: projected text 905171 codepoints and 29604 newlines; the concatenation of all 812
`indent=2` item dumps is 844724 codepoints and 28834 newlines; item 0's dump contains 2 `\u` escapes.
Therefore a per-task artifact's bytes are **not** a slice of the substituted text; only the parsed object is
comparable. Any audit that diffs artifacts against text offsets (rather than against parsed values) will
report spurious differences, and any claim that the written `test.json` "is" the per-task files is wrong.

## 8. Preserved unknowns and source-vs-runtime boundary

- **Source tier only.** The pinned raw JSON is a template fixture; the six names are resolved at runtime from
  `browser_env.env_config`, which this seat never reads. Nothing here is evidence about deployed hosts,
  credentials, benchmark reachability, scorer behavior, task validity, or model performance.
- **Synthetic profiles.** `distinct_origins` / `path_prefix` / `trailing_slash_sensitivity` are controlled
  `*.invalid` substitutions. Their agreement across representations is a fixture property, not a deployment
  observation, and not a sensitivity result about real endpoints.
- **Oracle agreement is bounded.** 2436/2436 structural equality is observed for these three benign profiles
  on these bytes. It does not extend to values containing `"`, `\`, control characters, tokens in keys, or
  escape-forged tokens (all latent divergence classes in §6). Exhaustive mutation coverage is not claimed.
- **Not measured here:** the production module's `--summary`/`--json`/`--selftest` behavior, its exit codes,
  its shuffled-ID witness, and any independent-oracle code. `plans/config_projection.py` is absent at lane
  HEAD; no production execution or capability is certified by this report.
- **Escaping is input-specific.** The exact per-token identity in §4 depends on the absence of
  underscore/letter escape forms in *this* ASCII fixture; a differently serialized fixture (e.g.
  `json.dumps(..., ensure_ascii=True)` of non-ASCII text, or any producer emitting `\u005f`) would change it.

## 9. Implications for the L1 instrument (no edits made here)

1. Model the projection as six ordered passes over serialized text — the only source stage — and derive the
   leaf diff by comparing parsed objects, never by string surgery on artifacts.
2. State the oracle's domain as: values only, six ordered rescans, JSON-serialization-safe substitution
   values; report divergence classes A/B/B3/E/C as explicit non-equivalence, and report cascade as an
   ordering property, not a representation property.
3. Keep the counting units separate: 1435 occurrences (385/336/281/300/**0**/133), 1416 leaves, 61 non-URL
   leaves / 62 occurrences / 18 tasks, 812 tasks, 2436 task/profile pairs.
4. Treat parse success as insufficient: a quote-comma value can inject fields and still parse (B3).
5. Report per-field provenance with codepoint offsets on the *pre-replacement* text; do not reuse them for
   projected text or artifacts (ASCII coincidence measured only for the raw input).

VERDICT: PASS

Scoped strictly to this seat's assigned reconnaissance: serialized-global-replacement-before-`json.loads`
versus decoded-leaf rewriting, with the measured escape/domain boundary, exact word-counted source quotes,
and hand-expected counterexamples. It does not admit round 29, does not certify
`plans/config_projection.py`, oracle agreement, capability rows, or any runtime/deployment fact, and leaves
production verification to L1 after all seats return.
