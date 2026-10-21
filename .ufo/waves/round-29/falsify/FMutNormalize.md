writer: KengakuR29-2.FMutNormalize-2

# FMutNormalize — trailing-slash normalization survives both built-in detectors

## Scope and result

Axes: serialized-text fidelity; detector sensitivity; isolated mutation and exact restoration.

**Observed mutant verdict: SURVIVED.** One behavior-bearing line was changed in a complete `/tmp` copy of the lane's `plans/` tree. Pristine, mutated and restored runs all returned exit 0 for `--selftest`, `--summary` and supplementary `--json`. The mutated selftest reported 20 clean cases. No assertion failed and no traceback was emitted. This is a conclusive survivor, not a baseline-failure/inconclusive result.

The survivor is a coverage finding: removing profile-value trailing slashes changes every one of the 812 task objects under the already-frozen trailing-slash profile, but neither built-in detector rejects it. This scoped FAIL concerns normalization detection, not round admission or the pristine implementation's source fidelity.

Production source was read (`plans/config_projection.py:140-147,266-359,385-521`). This is a mutation probe, **not an independent-oracle report**. No production source, fixture, corpus, registry, Git index or lane state was edited. One mutant only; no JSON-escape mutant was also tried.

## Attack and expected detector

Copied root: `/tmp/r29-FMutNormalize-2.9YapCw`.

Mutation location: `/tmp/r29-FMutNormalize-2.9YapCw/plans/config_projection.py:146`, inside `project()`.

Original:

```python
text = text.replace(token, values[name])
```

Mutant:

```python
text = text.replace(token, values[name].rstrip("/"))
```

This plausible URL-cleanup defect strips trailing `/` from each replacement value before its ordered global insertion, including insertions into non-URL metadata. It does not change token order, pinned inputs or tests.

Expected detector: the source-faithful projection tests/invariants should reject the altered literal values; mutant `--selftest` or `--summary` exit 1 would kill it. The no-normalization requirement is in `plans/round-29-claims.md:42-46`; frozen trailing-slash values are at `plans/fixtures/r29/profiles.json:24-32`. The actual pinned generator directly replaces the six values at `plans/fixtures/r29/generate_test_data.py:11-16`.

Actual failing assertion: **none**. The selftest at `config_projection.py:385-521` completed successfully, so there is no failing assertion location to invent. Its quote/backslash assertion at line 422 is not a trailing-slash normalization detector.

## Exact execution and outputs

Copy command, exit 0:

```sh
cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans /tmp/r29-FMutNormalize-2.9YapCw/plans
```

The following identical CLI commands were executed once in each phase, with a 120-second subprocess timeout per command and cwd `/tmp/r29-FMutNormalize-2.9YapCw`. Independent modes ran concurrently; the pristine/mutated/restored phases were necessarily sequential.

```sh
/usr/bin/python3 -B /tmp/r29-FMutNormalize-2.9YapCw/plans/config_projection.py --root /tmp/r29-FMutNormalize-2.9YapCw --selftest
/usr/bin/python3 -B /tmp/r29-FMutNormalize-2.9YapCw/plans/config_projection.py --root /tmp/r29-FMutNormalize-2.9YapCw --summary
/usr/bin/python3 -B /tmp/r29-FMutNormalize-2.9YapCw/plans/config_projection.py --root /tmp/r29-FMutNormalize-2.9YapCw --json
```

Capture invocations, each exit 0:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/capture.py pristine
python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/capture.py mutated
python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/capture.py restored
```

| Phase | selftest exit | summary exit | JSON exit | selftest cases | summary findings | stderr bytes, each mode |
|---|---:|---:|---:|---:|---:|---:|
| Pristine | 0 | 0 | 0 | 20 | 0 | 0 |
| Mutated | 0 | 0 | 0 | 20 | 0 | 0 |
| Restored | 0 | 0 | 0 | 20 | 0 | 0 |

Actual selftest output prefix in all phases: `SELFTEST clean cases=20`.
Actual summary final line in all phases: `TOTAL findings=0 exit=0`.

All phases reported 812 input tasks, 3 profiles and 2436 task/profile projections. Per profile, the summary retained 812 parsed tasks, 1416 changed string leaves and 812 changed tasks; those structural identities did not distinguish the mutant.

## Every mismatch, with exact locations and values

Evidence directory, absolute: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/`.

The report's exhaustive mismatch appendix is [`all-json-mismatches.jsonl`](../scratch/falsify/FMutNormalize-2/all-json-mismatches.jsonl), lines 1-3645. Each line records the exact output JSON Pointer, pristine expected value, mutant observed value, profile and, for task records, output index/task ID. Its SHA-256 is `de324cc9de0135d416d636c905e85f907f2a4534c63feae193570dbaa68a2216`. This appendix includes all differences, not only the examples below.

Observed units, from the complete recursive output comparison:

| Mismatch class | Count and unit |
|---|---:|
| Exact projected-task string values | 1416 JSON scalar fields |
| Corresponding changed-leaf projected values | 1416 JSON scalar fields |
| Would-be per-task-file SHA-256 values | 812 digest fields |
| Projected serialized-text SHA-256 | 1 digest field |
| **Total** | **3645 differing JSON scalar fields** |

All mismatches are within `/profiles/trailing_slash_sensitivity`; 812 distinct task objects differ. There are zero output mismatches for `distinct_origins` and `path_prefix`. The 3645 fields are not 3645 independent tasks or failures: the output repeats projected values in provenance and adds derived digests.

Exact examples from the exhaustive appendix:

| Appendix line | Output JSON Pointer | Expected pristine value | Observed mutant value |
|---:|---|---|---|
| 3 | `/profiles/trailing_slash_sensitivity/tasks/0/projected_task/start_url` | `http://shopping-admin.invalid:10304/` | `http://shopping-admin.invalid:10304` |
| 136 | `/profiles/trailing_slash_sensitivity/tasks/44/projected_task/eval/reference_url` | `http://gitlab.invalid:10301//dashboard/todos` | `http://gitlab.invalid:10301/dashboard/todos` |
| 1325 | `/profiles/trailing_slash_sensitivity/tasks/389/projected_task/eval/program_html/0/url` | `http://gitlab.invalid:10301//primer/design/-/merge_requests/450` | `http://gitlab.invalid:10301/primer/design/-/merge_requests/450` |
| 208 | `/profiles/trailing_slash_sensitivity/tasks/66/projected_task/eval/reference_answer_raw_annotation` | `http://reddit.invalid:10302//f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10302//f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter` | `http://reddit.invalid:10302/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10302/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter` |

The sole summary-line mismatch is line 39 in `pristine.summary.stdout.txt` versus `mutated.summary.stdout.txt`; every field on that line remains equal except `projected_text_sha256`:

- Expected: `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2`.
- Mutant: `fa983a913b7556c595eaf440d6451ac5ee7e9cddc5ef001450ca04bc5ae23057`.

Full exact before/after line values are in [`summary-mismatches.json`](../scratch/falsify/FMutNormalize-2/summary-mismatches.json). Selftest stdout has zero byte differences. All stderr streams are empty.

### Can frozen real data detect this survivor?

**Yes, with an exact source-faithful comparison; no, by the current CLI exit/findings checks alone.** No additional hand stimulus or fourth profile is necessary. `analyze.py` used the pinned raw text and frozen values to perform six direct ordered replacements without running/importing the generator. Its comparison with the already-captured projected task objects observed:

| Frozen profile | Pristine agrees | Mutant agrees | Restored agrees | Mutant task-object mismatches |
|---|---|---|---|---:|
| distinct_origins | true | true | true | 0 |
| path_prefix | true | true | true | 0 |
| trailing_slash_sensitivity | true | false | true | 812 |

This post-capture literal-replacement comparison detects the defect, but it is not a kill by the assigned built-in detectors and is not represented as independent authorship.

[INFERENCE] The gap is assertion coverage, not an unexercised input population: frozen P3 exercises trailing slashes, while selftest exact-value fixtures use replacement values without trailing slashes. The post-read audit assertion at `config_projection.py:515` checks exit/population rather than exact projected objects. No contract was relaxed and no tests were changed to accommodate the survivor.

Analysis command, exit 0, consumes captured outputs only:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/analyze.py
```

## Restoration and reproducibility evidence

The copied line was reverted immediately after the mutant capture and before the restored detector run.

| Copied instrument phase | SHA-256 |
|---|---|
| Pristine | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |
| Mutated | `e20988114231bf63cb7d465373611b9c27792828f9ccf1442ead543913e7bc03` |
| Restored | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |

The lane instrument retained the pristine hash at all six before/after capture snapshots. The 8 recorded non-instrument files—manifest, generator, raw population, profiles and 4 adopted hand fixtures—retained their respective original hashes in both lane and copy throughout. Full per-file values are recorded in each phase's capture JSON.

Pristine/restored stdout was byte-identical in every mode:

| Mode | Pristine/restored stdout bytes | Pristine/restored stdout SHA-256 | Mutant stdout bytes | Mutant stdout SHA-256 |
|---|---:|---|---:|---|
| selftest | 599 | `1fa3c1fcb6d6b3f7b2a83097b8473343bf278fb20b88c1fcfa99161878058d44` | 599 | `1fa3c1fcb6d6b3f7b2a83097b8473343bf278fb20b88c1fcfa99161878058d44` |
| summary | 6914 | `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f` | 6914 | `b551a579b803cc50e2e45db82f6c4fa6d5fb4ba84ea52000584ea0e75e51e112` |
| JSON | 3881050 | `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` | 3878180 | `cada33a67cc0e10663c43c10201d5cfaf53524e6c1846a9f223274e318c1b723` |

Receipts in the evidence directory:

- `capture.py`: reproducible bounded CLI capture harness; does not mutate source.
- `pristine.capture.json`, `mutated.capture.json`, `restored.capture.json`: exact commands, exit codes, before/after source/input hashes and output hashes.
- `<phase>.<mode>.stdout.txt` and `<phase>.<mode>.stderr.txt`: complete actual output for the three named phases and modes.
- `analyze.py`, `analysis.json`: complete mismatch counts, exact examples, literal-replacement comparison and restoration booleans.
- `all-json-mismatches.jsonl`, `summary-mismatches.json`: exhaustive exact mismatch appendices.
- `quote-counts.json`: report code/output/value quotations counted programmatically with `len(text.split())`, 24 whitespace words total, within 25.

The referenced author receipt `corpus/evidence/round29-calibration/mutation-witness.txt:1-6` lists order, URL-only and index mutants, not normalization. Its control hash matched this probe's observed pristine hash; none of its claimed mutation outcomes was treated as proof for this new mutant.

Tooling: existing `/usr/bin/python3` reports Python 3.14.8. No tool was installed or updated; no package transaction, service action, network access, REA device, subagent, formatter or linter was invoked. The assigned mutation probe and restoration are complete.

VERDICT: FAIL

## Re-check at dbcecded (follow-up)

Follow-up writer: KengakuR29-2.FMutNormalize-2. Scope: the same trailing-slash normalization mutant against the repaired instrument, plus execution of the requested persisted mutation-witness runner. Earlier findings above are historical and remain unchanged.

Observed checkout identity from `git rev-parse HEAD`: `dbcecded4a04247cf6fd12919327af973da10bdd` (exit 0). Production source was read for the mutation location and new assertion; this remains a mutation re-check, not an independent-oracle report.

**Observed result: KILLED by repaired `--selftest`.** The repaired pristine detector passed, the same one-line mutant failed at the new literal-slash assertion, and the restored detector passed. Frozen-data `--summary` still exits 0 for this mutant; that remaining distinction is explicitly reported, not called a summary kill.

### Copy, commands and exact exits

Copied the complete repaired `plans/` tree with:

```sh
cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans /tmp/r29-FMutNormalize-dbcecded.66jCWc/plans
```

The only mutation was at `/tmp/r29-FMutNormalize-dbcecded.66jCWc/plans/config_projection.py:179`: add the same `.rstrip("/")` to the replacement value before substitution. No tests, inputs or lane files were changed.

Identical bounded commands ran once per pristine/mutated/restored phase, using a 240-second per-process timeout and cwd `/tmp/r29-FMutNormalize-dbcecded.66jCWc`:

```sh
/usr/bin/python3 -B /tmp/r29-FMutNormalize-dbcecded.66jCWc/plans/config_projection.py --root /tmp/r29-FMutNormalize-dbcecded.66jCWc --selftest
/usr/bin/python3 -B /tmp/r29-FMutNormalize-dbcecded.66jCWc/plans/config_projection.py --root /tmp/r29-FMutNormalize-dbcecded.66jCWc --summary
```

Capture invocations, each harness exit 0:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/recheck-dbcecded/capture.py pristine
python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/recheck-dbcecded/capture.py mutated
python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/recheck-dbcecded/capture.py restored
```

| Phase | selftest exit | summary exit | selftest completed cases | selftest stdout bytes | selftest stderr bytes |
|---|---:|---:|---|---:|---:|
| Repaired pristine | 0 | 0 | 28 | 794 | 0 |
| Normalization mutant | 1 | 0 | Aborted at line 534 | 0 | 648 |
| Restored | 0 | 0 | 28 | 794 | 0 |

The pristine/restored selftest output prefix is `SELFTEST clean cases=28`. The mutant traceback ends with `AssertionError` at `config_projection.py:534`, in the new case defined at lines 530-537. The recorded diagnosis used exactly that case's raw text and values through the same copied instrument; findings were an empty list, isolating the failed string equality:

| Exact hand-case JSON Pointer | Required literal value | Observed mutant value |
|---|---|---|
| `/0/start_url` | `http://gitlab.invalid:1//a` | `http://gitlab.invalid:1/a` |
| `/0/eval/program_html/0/required_contents/must_include/0` | `http://gitlab.invalid:1//b` | `http://gitlab.invalid:1/b` |

Both fields matched their required values in pristine and restored diagnoses. The selftest fails on the first at line 534; the second is also wrong but its later assertion is not reached. Full traceback and both exact-value records are retained in `mutated.selftest.stderr.txt` and `mutated.capture.json`.

All summary runs still finish with `TOTAL findings=0 exit=0` and empty stderr. The sole summary mismatch is line 45, `trailing_slash_sensitivity.projected_text_sha256`: expected `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2`, mutant `fa983a913b7556c595eaf440d6451ac5ee7e9cddc5ef001450ca04bc5ae23057`. Its complete exact before/after line is recorded in the follow-up `analysis.json`. Thus the frozen population still exposes a byte-level difference, but the new hand-case selftest—not frozen-summary findings—kills this defect.

### Requested mutation-witness receipt

Executed the lane's persisted runner, which was read beforehand and creates its experiments only under `/tmp`:

```sh
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/mutation_witness.py
```

The capture harness's `witness` mode ran that exact command concurrently with the repaired pristine capture, before this leaf mutated its separate copy. Runner exit: 0. Receipt stdout: 5131 bytes; stderr: 0 bytes. Receipt SHA-256: `8c5afbe6a8ef9d58303239a6c5f567cc7f454ced372165d92e6fd471ef63b815`. Runner source SHA-256: `70c36f7596f9fc5d3776a0b355769b18bdaa4ed6f6621b76263ff977871c8e25`.

Observed receipt: control selftest exit 0 with 28 clean cases; control summary exit 0; 10 mutants enumerated and 10 reported killed. Exact exit matrix from that receipt:

| Persisted mutant | selftest exit | summary exit | summary finding count | Receipt killed |
|---|---:|---:|---:|---|
| wrong_order_reversed | 1 | 0 | 0 | true |
| url_only_substitution | 1 | 1 | 6 | true |
| index_by_task_id | 1 | 0 | 0 | true |
| value_normalized_rstrip | 1 | 0 | 0 | true |
| category_by_value_shape | 1 | 0 | 0 | true |
| hash_then_reread | 1 | 0 | 0 | true |
| decoded_census_drops_wikipedia | 1 | 0 | 0 | true |
| runtime_marker_counted_as_token | 1 | 1 | 3 | true |
| exact_contract_check_removed | 1 | 0 | 0 | true |
| unexpected_error_not_caught | 1 | 0 | 0 | true |

The persisted runner's normalization row agrees with this leaf's independently executed one-line mutation probe: selftest exit 1, summary exit 0, killed true, frozen-summary-alone-detects false. The table reports the runner's receipt; this leaf did not expand its own assigned mutation set or claim exhaustive coverage.

### Restoration, append-only history and cleanup

| Copied instrument phase | SHA-256 |
|---|---|
| Repaired pristine | `135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142` |
| Mutated | `38f993014ba47a8b2b4f9189cce78b8cdba1e33f425ddce41310cc985ea514e3` |
| Restored before deletion | `135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142` |

The runner independently reports its restored source hash as the same repaired-pristine hash. The lane instrument and every recorded input, hand fixture and runner hash remained unchanged throughout both experiments.

Restored selftest and summary stdout were byte-identical to repaired pristine. Their respective SHA-256 values are `4dc3b86679000ef8a6c9802fbb09de3c4e570277371c58955c700a87ee16d3b4` and `9e074be313d7b15839fd82a39a038c9d0bfd0e32f281024830c3e0780ea2d7ba`. The mutant selftest stderr hash is `cabd218d9347c2defab4e39e2591332639c2d8e7d102e7fe681a6dca62654d88`.

Before this append, the entire earlier report was 11912 bytes with SHA-256 `d28e0ec3c743570ac6c0acb59c850797adfaf3d6e3d1e3f6859625133bba9413`; this section is added only at EOF, leaving that historical FAIL intact.

Both owned `/tmp` plan copies were deleted after restoration evidence was captured: `/tmp/r29-FMutNormalize-2.9YapCw` and `/tmp/r29-FMutNormalize-dbcecded.66jCWc`. The final deletion/check command returned exit 0, with both absence checks true; its exact command/output are in `cleanup.json`. The persisted runner removed its own temporary directory on normal context exit.

Follow-up evidence directory: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/recheck-dbcecded/`.

- `pristine.capture.json`, `mutated.capture.json`, `restored.capture.json` and their mode stdout/stderr files: exact commands, exits, source/input hashes, traceback and literal-value diagnosis.
- `official-witness.stdout.txt`: full 10-mutant JSON receipt; `official-witness.receipt.json`: runner command, exit, output hashes and unchanged lane snapshots.
- `analysis.json`: exact summary mismatch, exit matrix, restoration comparisons, witness receipt summary and programmatic count of the follow-up's code/output/value excerpts (11 whitespace words).
- `prior-report-metadata.json`: hash/length of the historical report before appending; `cleanup.json`: owned-copy removal evidence.
- `capture.py`, `summarize.py`: retained evidence-capture/analysis scripts, not production changes. No supplementary `--json` rerun was needed for this follow-up.

No tools were installed or updated; no package transaction, service action, network access, REA device, subagent, formatter or linter was used. Scoped conclusion: the repaired selftest closes the observed rstrip-normalization survivor; the frozen-summary-only limitation remains disclosed.

VERDICT: PASS
