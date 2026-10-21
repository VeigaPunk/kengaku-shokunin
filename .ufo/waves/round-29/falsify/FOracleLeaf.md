# FOracleLeaf — decoded-leaf oracle attack on the round-29 projection domain

writer: KengakuR29-2.FOracleLeaf-2
Item: decoded-leaf oracle vs the integrated `plans/config_projection.py` text projection, round 29 only. Date: 2026-10-21.

## Independence

I did **not** read, import, or open `plans/config_projection.py` source. Derivation inputs were the
prereg text (`plans/round-29-claims.md`), the pinned generator bytes, and the pinned data; the
instrument was used only through its CLI (`--help`, `--summary`, `--json`, `--selftest`) and its
captured `--json` OUTPUT. `scratch/falsify/FOracleLeaf/oracle.py` header states the same. The only
Python modules my scripts import are stdlib and the sibling `oracle.py` itself.

## Inputs verified (observed)

`sha256sum` over the four pinned files, all matching manifest pins:
- `plans/fixtures/r29/manifest.json` → `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`
- `plans/fixtures/r29/generate_test_data.py` → `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`
- `plans/fixtures/r29/profiles.json` → `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`
- `plans/fixtures/r28/webarena/config_files/test.raw.json` → `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`

## Method (axes: A1 frozen coverage, A2 boundary cases, A3 exact domain, A4 evidence quality)

Leaf oracle (`oracle.py`): parse raw JSON once; walk decoded structure in document order; substitute
all six tokens in every decoded string (dict keys and values) with a **single-pass** combined-regex
scan; replacement text is never rescanned (no cascade). Text oracle (mine, from the prereg sentence
"Decoded-leaf rewriting is an independently implemented oracle only within the frozen benign profile domain"
context and generator bytes, 14 words): six sequential `str.replace` over raw text in order
GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP, then `json.loads`.

## A1 — frozen-domain result: leaf == text == instrument on all 2436 (observed)

Commands: `python3 plans/config_projection.py --summary` (rc=0, stdout 6914 B, stderr 0 B);
`--json` (rc=0, stdout 3881050 B, stderr 0 B); `--selftest` (rc=0, 599 B); then
`python3 .ufo/waves/round-29/scratch/falsify/FOracleLeaf/oracle.py` (rc=0, stdout 11446 B,
retained as `oracle_frozen.out`).

Per profile (all three: distinct_origins, path_prefix, trailing_slash_sensitivity), over 812 tasks each:
- objects compared 2436; leaf==text 2436; leaf==instrument 2436; text==instrument 2436; mismatches [].
- my projected-text sha256 == instrument `projected_text_sha256` per profile
  (distinct_origins `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4`,
  path_prefix `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b`,
  trailing_slash_sensitivity `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2`).
- my independent provenance reconstruction: 1435 (token, Unicode-codepoint offset, json_pointer,
  role=value) records, multiset-equal to the instrument's `occurrence_provenance` (mine 1435,
  instr 1435, diff empty).
- changed-leaf sets equal per task (my deep-diff vs instrument `changed_leaves`), totals 1416 per
  profile on both sides; per-token changed leaves mine {GITLAB 385, REDDIT 323, SHOPPING 275,
  SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133} == instrument `changed_leaves_by_token`.
- all 2436 `would_be_file_sha256` reproduced by `sha256(json.dumps(task, indent=2))` — 0 mismatches.
- index==task_id 812/812, 812 distinct IDs, violations [] (mine, matches instrument INDEX).
- census: raw occurrences == decoded value occurrences per token {385, 336, 281, 300, 0, 133};
  decoded KEY occurrences 0 for all tokens; string value leaves 10869 (== instrument
  `string_leaf_count`), string key leaves 18140.

**Answer to the ticket question: yes — on the three frozen benign profiles, decoded-leaf
substitution equals text substitution for all 2436 task/profile projections, object-exact.**

## A3 — exact equivalence domain (observed preconditions, all true on frozen input)

Equivalence of single-pass leaf substitution and sequential text substitution holds iff:
- **D1 escape-safety**: raw-text token count == decoded token count per token (no token straddles or
  is formed/broken by JSON escapes). Observed true for all six tokens.
- **D2 JSON-verbatim values**: every profile value has `json.dumps(v) == '"'+v+'"'`, no `"`, `\`,
  or control chars. True for all 18 values (6 tokens x 3 profiles).
- **D3 no cascade**: no profile value contains any token marker. True (checked per token per profile).
- **D4 token disjointness**: no token is a substring of another. True (`__SHOPPING__` does not occur
  inside `__SHOPPING_ADMIN__`; checked pairwise, zero hits).
- **D5 key involvement**: zero token occurrences in keys on frozen input (subsumed by D1 when true).

[INFERENCE] Under D1–D5 any substitution ORDER also coincides, because match sets are identical and
disjoint; outside D3, equivalence becomes order-asymmetric (H3 vs H4 below).

## A2 — hand inputs where the methods differ (observed; retained `oracle_hands.out`)

Raw inputs are minimal docs in my scratch; profiles are hand-made (not the frozen profiles). The
instrument itself refuses tampered inputs by design (persisted manifest digest ⇒ `--root` rebinding
cannot feed it new profiles), so the text side is my own re-derivation of the generator's exact
six-replace semantics; corroboration: the instrument's selftest names the same classes
(`escaped_token_not_replaced`, `quote_backslash_decode_failure_and_escape_semantics` — identifiers,
1 whitespace-word) and prereg requires "quotes/backslashes causing JSON decode failure rather than
repair" (8 words).

- **H1 quote in value** (`{"task_id": 0, "start_url": "__GITLAB__", ...}`, GITLAB →
  `http://gitlab.invalid:10101/"q"`): text projection raises `JSONDecodeError: Expecting ','
  delimiter` at line 1 column 59 (pos 58) — upstream would produce no test.json at all; leaf
  projection parses with `start_url = http://gitlab.invalid:10101/"q"`. Location: `/start_url`.
- **H2 backslash escape** (`start_url: "__REDDIT__"`, REDDIT → `http://reddit.invalid:10102\nfast`
  with a real U+005C+U+006E pair): both parse, values differ at codepoint index 27 of the value:
  leaf U+005C (33 chars) vs text U+000A (32 chars) — the text layer silently consumes the escape.
  Would-be per-task file digests differ: leaf `0bdf64ecca5712142b05a3a04c72ccedc12fdc93b21b0a7d028cb05ae379118e`
  vs text `8417ec83f211b43b1d5b35e20147092bf4f6d536a1381e5d8c4e640cd9d10c00`. Location: `/start_url`.
- **H2b trailing backslash** (`start_url: "__MAP__"`, MAP → `http://map.invalid:10306/\`): text
  projection raises `Unterminated string` at line 1 column 29 (pos 28); leaf parses fine.
  Location: `/start_url`.
- **H3 later-token cascade** (`start_url: "__GITLAB__"`, GITLAB →
  `http://gitlab.invalid:10101/__MAP__`, MAP → `http://map.invalid:10306`): text step 1 injects
  `__MAP__`, step 6 substitutes it → `/start_url = http://gitlab.invalid:10101/http://map.invalid:10306`;
  single-pass leaf leaves the literal marker → `http://gitlab.invalid:10101/__MAP__`. Locations/values exact.
- **H4 control (earlier token in later value)**: MAP value containing `__GITLAB__` — both methods
  leave it literal (order asymmetry: only LATER tokens cascade in text mode).
- **H5 escape-adjacency control** (`\u2122` in the same string as `__WIKIPEDIA__`): both agree —
  the D1 direction where escapes merely sit adjacent to tokens is safe.

## Unit discrimination (observed, `units.py`/`units.out`)

1435 token occurrences (raw text) ≠ 1416 changed leaves ≠ 13 leaves with ≥2 occurrences ≠ 0 leaves
with ≥2 distinct tokens ≠ 812 tasks. Extras 19 = repeated same-token leaves only (6 extra
`__SHOPPING__`, 13 extra `__REDDIT__`), consistent with per-token leaf counts above. Instrument
`changed_leaves_with_multiple_occurrences` = 13 matches my ≥2-occurrence leaf count.

## Tooling record

No tool installed or upgraded (stdlib Python 3.14.8 sufficed; no pacman, no uv, no downloads).
No lane files mutated; hand experiments ran in-memory on minimal docs (no /tmp copy of the lane was
needed because the instrument cannot accept modified inputs by design, and benign `--root` copies
would be byte-identical and uninformative).

## Files produced (all under `.ufo/waves/round-29/scratch/falsify/FOracleLeaf/`)

`oracle.py` (the deliverable), `units.py`, `units.out`, `oracle_frozen.out`, `oracle_hands.out`,
`instr_summary.out`, `instr_json.out`, `instr_selftest.out`, `instr_*.err` (all empty).

## Risks / notes

- H-case text semantics are my re-derivation, not the instrument executing those inputs (impossible
  by its own tamper design); the instrument's selftest case names corroborate the classes. [INFERENCE]
  the production implementation matches my text oracle on the hand classes.
- My leaf oracle is single-pass by construction; a leaf oracle that re-scans after each token would
  cascade like text mode and H3 would not differentiate. The report's domain statement is tied to
  the single-pass definition, which is the reading fixed by the prereg's cascade-disclosure duty.

Attack outcome: the frozen-domain equivalence claim survives; the boundary is exactly D1–D5, with
quote/backslash (H1, H2, H2b) and later-token cascade (H3) as the demonstrated failure classes of
the decoded-leaf alternative outside it.

VERDICT: PASS
