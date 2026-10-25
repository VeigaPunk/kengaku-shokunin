# R29MutOrder — later-token-cascade mutation design

Seat / actual writer: `KengakuR28.R29MutOrder-2`.
Access date: 2026-10-21.
Scope: first-wave **design only**, for round29 C1's offline generated-config projection. No production code was required, read, edited, imported, or executed. No behavioral detector or mutation experiment was run. This report does not admit the round, raise a score, or establish runtime/model/task validity.

## Axes

- Source-semantic fidelity: serialized text must receive the six source-ordered replacements before JSON parsing.
- Discrimination: a deliberately cascading hand case must distinguish canonical order from profile-mapping order and single-pass simultaneous substitution.
- Isolation/restorability: only this assigned report and this seat's scratch artifacts are written; the probe specification requires exact restoration in a later isolated experiment.
- Evidence precision: hand predictions, actual static observations, raw occurrences, dynamic replacement hits, and task counts remain separate.

## Exact sources opened

The first read was `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-29-claims.md`, lines 1–108. Relevant contract locations: lines 35–47 (order/serialized-text semantics), 73–77 (hand cases), and 98–101 (wrong-order control must actually fail before counting).

Additional local reads:

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py`, lines 1–27: six replacements at 11–16; JSON parse at 20. The wildcard import at 5 was treated as inert source data, never executed.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json`, lines 1–27: source/input pins and replacement order at 19–26.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json`, lines 1–35: frozen synthetic profile values. None was modified or used as a live endpoint.

One source quotation, from generator line 11:

> raw = raw.replace("__GITLAB__", GITLAB)

Programmatic quotation count: Python `len(quote.split())` returned **4 words**, within 25. No other source prose is quoted. The source URL recorded in the manifest was not requested. No raw812-task corpus census was performed by this seat; 812/2436 are preregistration context, not newly measured results here.

## Concrete hand-expected fixture

Artifact:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29MutOrder-2/cascade-order.case.json`

This is an adversarial hand fixture, **not a fourth frozen profile**. It contains one input task and one string leaf. Its `raw_serialized_text` is the following JSON string literal; `\n` denotes the actual final LF in the decoded input text:

```json
"[{\"task_id\":0,\"start_url\":\"__GITLAB__/probe\"}]\n"
```

Six string values are inserted into the test mapping in reverse source order:

| Mapping insertion position | Name | Hand value |
| --- | --- | --- |
| 1 | MAP | `https://map.invalid/order` |
| 2 | WIKIPEDIA | `__MAP__` |
| 3 | SHOPPING_ADMIN | `__WIKIPEDIA__` |
| 4 | SHOPPING | `__SHOPPING_ADMIN__` |
| 5 | REDDIT | `__SHOPPING__` |
| 6 | GITLAB | `__REDDIT__` |

The detector specification explicitly constructs that mapping order; it does not treat JSON object order as semantic authority. Source order remains GITLAB → REDDIT → SHOPPING → SHOPPING_ADMIN → WIKIPEDIA → MAP regardless of mapping order.

Hand-expected `start_url` after each canonical step:

| Source step | Expected value |
| --- | --- |
| GITLAB | `__REDDIT__/probe` |
| REDDIT | `__SHOPPING__/probe` |
| SHOPPING | `__SHOPPING_ADMIN__/probe` |
| SHOPPING_ADMIN | `__WIKIPEDIA__/probe` |
| WIKIPEDIA | `__MAP__/probe` |
| MAP | `https://map.invalid/order/probe` |

Exact hand-expected final serialized text, expressed as a JSON string literal:

```json
"[{\"task_id\":0,\"start_url\":\"https://map.invalid/order/probe\"}]\n"
```

Expected parsed value:

```json
[{"task_id":0,"start_url":"https://map.invalid/order/probe"}]
```

Expected units, **not observed projection metrics**: one original placeholder occurrence (GITLAB), six dynamic replacement hits (one per stage), one changed string leaf, one task, zero remaining six-known-token occurrences. Six hits must not be reported as six original raw occurrences or six tasks.

## One selected mutant and expected detector

Full specification:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29MutOrder-2/mutant-spec.json`

Selected mutant `R29_M_ORDER_01`: change only the serialized replacement-loop iterator from source order to profile-mapping iteration order. Conceptual one-line defect:

```python
# Pristine iterator
for name in SOURCE_ORDER:
# Mutated iterator, with the same replacement body
for name in values:
```

The unchanged body performs `raw.replace` using the selected name and string value. This is a mutation specification, not a claim about an inspected production function or line number. Source-contract validation, frozen pins, parsing, and output handling must not be changed merely to make the mutant reachable.

**[INFERENCE / hand prediction]** Reverse mapping order consumes no tokens until its last GITLAB step, which inserts `__REDDIT__` after the REDDIT step has already passed. The mutant therefore yields valid JSON with `start_url` equal to `__REDDIT__/probe`, rather than the expected endpoint.

**[INFERENCE / related defect, not a second assigned probe]** One simultaneous substitution pass over the original serialized input also inserts `__REDDIT__` without rescanning replacement text. It must fail the same exact-output witness.

With each name applied exactly once, successful completion requires every predecessor to run before its successor; those five constraints uniquely determine the source order. An unordered implementation that happens to choose the canonical order can still pass a particular run. The reverse insertion fixture makes the selected mapping-order defect deterministic; this report does not claim universal detection of nondeterminism.

Bounded detector specification:

1. Bind the actual implementation's serialized substitution behavior in the fresh falsifier's own scratch. A test-owned reference transform is not a substitute for the system under test.
2. Supply exactly the fixture input and six string values in the explicit mapping insertion order.
3. Require exact serialized-output equality with the persisted hand literal, including final LF; then require JSON-parsed equality with the persisted object and zero occurrences of the six exact known placeholders.
4. Proposed fixed harness outcomes: exit0 `R29_ORDER_CASCADE_01 PASS`; exit1 for behavioral mismatch; exit2 for inability to bind/evaluate. These are proposed outputs, not observations.
5. Run the same bounded command and identical detector/fixture bytes on pristine, mutated, and restored implementation bytes. Hash/retain original bytes before mutation; restore in finally-style cleanup even after failure and verify direct byte equality. A baseline failure is INCONCLUSIVE. Only a passing baseline, expected behavioral mismatch under mutation, passing restored run, and exact restoration justify KILLED. Passing mutation means SURVIVED; binding/runtime/restoration errors are not behavioral kills.

A future probe must bind the real implementation/selftest seam and record its actual command/file/line. This design does not invent a production API. It must not rewrite pinned profiles or weaken manifest authentication to inject the hand case. A benign frozen-profile `--summary` run alone is not this detector. No HTTP request, benchmark output file, browser state, or upstream import is necessary.

## Actual executions and outputs

Only local source inspection, AST parsing as inert data, hashing, byte counting, and byte-identity census were executed. Python standard-library `Path.read_bytes`, `hashlib.sha256`, `json.loads`, and `ast.parse` retained source bytes; no upstream code was imported/evaluated. The `Fingerprinting inert source contract` eval cell produced:

```text
manifest_hash_matches_declared_pin = true
generator_hash_matches_manifest = true
profiles_hash_matches_manifest = true
static_replacement_calls = [(11, __GITLAB__, GITLAB), (12, __REDDIT__, REDDIT), (13, __SHOPPING__, SHOPPING), (14, __SHOPPING_ADMIN__, SHOPPING_ADMIN), (15, __WIKIPEDIA__, WIKIPEDIA), (16, __MAP__, MAP)]
source_order_matches_manifest = true
source_quote.word_count_split = 4
```

The hash command actually executed was:

```sh
sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-29-claims.md /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29MutOrder-2/cascade-order.case.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29MutOrder-2/mutant-spec.json
```

Hash outputs, in that argument order:

```text
6b4ffee35ddf706a4a77e9daf9c647cbd85b484f8b652b7dbd84dbd6289e92c1
f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd
90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018
4f957db3c3a8c19e951b6b225e9520cfc631fc09f864c9b4aad72464d9639fb3
b6813ffaaff1f8d421df82b57e7ded6ea7e51fb6ee3a7a91232308e23c9ce586
```

The byte-count command actually executed was:

```sh
wc -c /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29MutOrder-2/cascade-order.case.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29MutOrder-2/mutant-spec.json
```

Observed bytes: case **2306**, specification **5411**, total **7717**. These are artifact byte counts, not source quotation word counts or projected task counts.

## Before/after identity and restoration evidence

The initial retained-byte census and final `Recording unchanged source bytes` eval cell reported the following. Each source's before SHA256 and after SHA256 were identical to the corresponding hash above; direct `after == before` was also true, not merely hash equality:

| Absolute source path | Retained bytes | Before/after SHA256 | Direct exact bytes equal |
| --- | ---: | --- | --- |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-29-claims.md` | 8160 | `6b4ffee35ddf706a4a77e9daf9c647cbd85b484f8b652b7dbd84dbd6289e92c1` | true |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json` | 1061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | true |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | true |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json` | 1391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | true |

Actual mutation-probe status:

| Phase | Actual behavioral output | Observed mutation status |
| --- | --- | --- |
| Pristine | NOT RUN | No baseline established |
| Mutated | NOT RUN | No implementation bytes mutated |
| Restored | NOT RUN | No restoration operation needed; nothing mutated |

Final identity-census output also recorded `behavioral_experiments_executed = 0` and `implementation_files_mutated = 0`. Mutation verdict: **INCONCLUSIVE / NOT EXERCISED**, because this assignment is design-only, not because a baseline failed. There is no observed KILLED or SURVIVED result. Report/scratch creation is not a pristine→mutated→restored implementation experiment.

No builds, selftests, linters, formatters, model calls, network/site requests, host environment/credential reads, production config outputs, Git/jj mutations, commits, delegation, installs, updates, or service changes were performed. No runtime validity, comprehensive mutation coverage, novelty-score increase, or round admission follows from this design.

VERDICT: PASS

Scoped to completion of the assigned hand-expected fixture, one concrete mapping-order mutant specification, bounded detector/restoration protocol, and truthful design-only evidence. Actual behavioral falsification remains unobserved and cannot be counted as a killed control.
