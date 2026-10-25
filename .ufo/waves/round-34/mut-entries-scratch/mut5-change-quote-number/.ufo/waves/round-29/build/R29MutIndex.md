# R29MutIndex — shuffled-ID filename mutation design

Seat and actual writer: `KengakuR28.R29MutIndex-2`.
Assignment: design-only first wave, round29 C1 attempt1. No production implementation, upstream source, sibling file, index, or runtime was mutated or executed. This report does not claim a killed mutant or round admission.

## Axes

- **Source fidelity:** output filenames use the zero-based enumeration position, while task IDs remain unchanged.
- **Detector discrimination:** compare filename-to-full-task associations; equal counts and equal filename sets must not conceal a swapped association.
- **Isolation and evidence integrity:** persist literal hand expectations and one semantic mutation; distinguish predicted detector results from observed commands.

These are bounded construct-coverage design axes, not a new method, score increase, model result, deployment observation, or runtime-validity claim. Legacy novelty7 and calibration8 are unchanged.

## Exact sources opened

All accesses were to local frozen files on 2026-10-21; no endpoint request occurred.

1. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-29-claims.md`, read first, lines 35–47 and 63–82: sequential serialized-text substitution, enumeration-based filenames, and the required hand witness.
2. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py`, lines 11–16 and 20–23: replacement order, JSON parsing, enumeration, and filename expression. Read as inert source data; its environment import was never run.
3. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json`, lines 6–16 and 19–26: pinned source/profile digests and replacement order.
4. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json`, lines 2–11: the six `distinct_origins` values copied literally into the synthetic witness.

Located source quotations, generator lines 21–22:

> for idx, item in enumerate(data):

> with open(f"config_files/{idx}.json", "w") as f:

Programmatic whitespace-split quotation count, executed with `functions.eval` using the two literal source lines:

```text
source_quote_word_counts=[5, 5]
source_quote_total_words=10
```

## Concrete persisted hand case

Fixture:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29MutIndex-2/index-shuffled-ids.fixture.json`

This contains literal raw JSON text, all six frozen profile values and their replacement order, exact expected projected text, full expected task records, and the expected filename-to-ID map. It is a minimal synthetic projection input, not a claim that either object is an executable benchmark task.

| Input position / expected ordinal | Unchanged task_id | Expected logical filename | Wrong-ID mutant filename |
| --- | --- | --- | --- |
| 0 | 1 | `config_files/0.json` | `config_files/1.json` |
| 1 | 0 | `config_files/1.json` | `config_files/0.json` |

The first object's intent is `ID 1 occurs first` and its expected projected start URL is `http://gitlab.invalid:10101/index-witness/first`. The second object's intent is `ID 0 occurs second` and its expected projected start URL is `http://reddit.invalid:10102/index-witness/second`. Each entire object stays with its own input position; the correct result does not sort or relabel IDs.

Units: **2 input tasks × 1 synthetic profile = 2 task/profile projections**. Correct and mutant outputs both have two distinct filenames and the identical filename set. The IDs are a permutation of the ordinal set, making count-only or filename-set-only checking insufficient. The expected ordinal-equals-task-ID flags are `[false, false]`; inequality is deliberate, not itself a failure.

These `config_files` names describe source-equivalent planned artifacts only. No actual `config_files` output was created.

## One mutant and its expected detector

Specification:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29MutIndex-2/wrongoutputfilenamebasedontask_id.mutant.json`

Mutant: **wrongoutputfilenamebasedontask_id**. At the filename-materialization expression of a later isolated projection implementation, replace use of `idx` with `item['task_id']`. Keep input order, original IDs, output ordinals, replacement behavior, and exact task objects unchanged. The frozen upstream source is the reference, not a mutation target. No production function or nonexistent CLI fixture flag is assumed.

Expected bounded detector: supply this fixture to an in-memory hand-case adapter; compare the complete ordered actual `(task_id, output_ordinal, output_filename, projected_task)` records against the literal expected records. Additionally compare the filename-to-task-ID associations. The adapter must observe actual planned/emitted filenames and associated objects, never regenerate a correct filename from the ordinal or rebuild objects from expectations. Structural object equality is required; incidental `json.dump` whitespace is not the tested behavior.

Predicted results below are **hand expectations, not observed execution output**:

```text
pristine/restored: exit 0
PASS r29_index_shuffled_ids_1_0: 2 ordered task/filename/object associations match

mutated: exit 1
FAIL r29_index_shuffled_ids_1_0 record[0].output_filename: expected config_files/0.json; got config_files/1.json
```

The specification records the identical pristine/mutated/restored detector protocol, capture of actual stdout/stderr/status and SHA256 values, and finally-style exact-byte restoration even after a detector failure. A passing baseline, mutation-specific association failure, and passing exact-byte-restored run are required before KILLED is justified. A failed baseline, unrelated error, unapplied mutation, or failed restoration is INCONCLUSIVE. Three passing runs mean SURVIVED, a coverage finding rather than permission to change the contract.

## Actual outputs and fingerprints

Actual behavioral execution for this design-only assignment:

| State | Observed detector output | Mutation-target hash |
| --- | --- | --- |
| Pristine | NOT RUN | Not collected; implementation not selected |
| Mutated | NOT RUN | Not applicable; no mutation applied |
| Restored | NOT RUN | Not applicable; no target changed |

**Mutation verdict: INCONCLUSIVE — NOT RUN.** Neither KILLED nor SURVIVED is claimed.

Observed checksum command before creating the scratch artifacts:

```text
sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json
```

Observed checksum command after creating the scratch artifacts:

```text
sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29MutIndex-2/index-shuffled-ids.fixture.json /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29MutIndex-2/wrongoutputfilenamebasedontask_id.mutant.json
```

Both commands returned the following same source/profile SHA256 values, matching the opened preregistration/manifest pins:

| Absolute source path | Before SHA256 | After SHA256 |
| --- | --- | --- |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` |

Observed final scratch artifact hashes:

- Fixture SHA256: `938771045ddbe6bdf6323858bc2c3204e38d028f1086bf83758b79a255fc9254`.
- Mutant specification SHA256: `3bae691a271c50fa66291216887e41da971be3793859da1564407c9e3236a5c4`.

Restoration evidence is limited to **no mutation having occurred** and equal before/after hashes for the frozen inputs. These are not hashes of an executed mutant or evidence of a pristine/mutated/restored behavioral experiment.

## Boundaries

- This seat did not read the full raw812 population or measure its index/ID agreement. The 2436-projection census remains outside this two-projection design result.
- No projection implementation, build, selftest, lint, formatter, browser, environment import, host environment, auth state, credential store, network endpoint, model, or alternate runtime was invoked. The commands above computed file digests; the Python cell counted quoted words only.
- No tool installation/update was needed or performed. No production files, canonical knowledge, source registry, scorecard, P4 classes, Git/JJ state, or sibling scratch were edited.
- The detector adapter and actual behavioral outcome remain unobserved. The specification is complete as a design artifact, not evidence of implemented coverage, runtime file-writing, benchmark validity, method novelty, or external closure.

VERDICT: PASS — scoped design-only shuffled-ID hand fixture and single-mutant detector specification delivered; mutation execution remains INCONCLUSIVE (NOT RUN), with no round-admission claim.
