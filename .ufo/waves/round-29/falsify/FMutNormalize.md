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
