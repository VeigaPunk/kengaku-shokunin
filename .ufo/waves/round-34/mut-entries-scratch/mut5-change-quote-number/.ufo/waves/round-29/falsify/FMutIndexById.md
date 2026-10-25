writer: KengakuR29-2.FMutIndexById-2

# FMutIndexById — task-ID filename mutation

## Scope and axes

Assigned probe only: challenge enumerate-index output filenames with one task-ID-keyed mutant. Probe axes: mapping fidelity, detector sensitivity, and exact restoration/isolation. This is not a round-admission judgment or a claim of exhaustive mutation coverage.

**Observed result: KILLED by the integrated `--selftest`; SURVIVED the frozen-data `--summary` and `--json` detectors.** The pristine and restored selftests passed. The kill was the intended shuffled-ID assertion, not an unrelated exception.

I read the production source for mutation placement and assertion attribution. This is a mutation probe, not a source-independent oracle. The author's receipt at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round29-calibration/mutation-witness.txt:5` was treated as a hypothesis and reproduced rather than accepted as evidence of my execution.

## Isolation and the one mutant

The lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/` was copied with Python stdlib `shutil.copytree`, preserving symlink semantics, into:

`/tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0/plans/`

The copy contained 119 files, zero symlinks, and zero file-byte mismatches against the lane at copying. Only the copy was edited. The only changed file was `config_projection.py`, and the only changed line was 330. No lane source, fixture, corpus, candidate, Git index, or runtime state was edited.

Source authority: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py:21-23` enumerates tasks and names files by `idx`. The preregistered mapping and shuffled witness requirements are at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-29-claims.md:66-77`.

Mutation location: `/tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0/plans/config_projection.py:330`.

Before, 4 whitespace-delimited words:

```python
"output_filename": "config_files/%d.json" % i
```

Mutated, 5 whitespace-delimited words:

```python
"output_filename": "config_files/%d.json" % task.get("task_id", i)
```

This replaces only the filename interpolation operand. All ID-bearing tasks use `task_id`; the default preserves existing keyless hand cases so an unrelated missing-key exception cannot masquerade as the intended mapping kill. Output index, task ID, projected task contents, source-contract parsing, and assertions were not changed.

## Bounded detector and actual outputs

Harness: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutIndexById-2/probe_detector.py`.

The harness was run with `--phase pristine`, then `--phase mutated`, then `--phase restored`, always using these same absolute root and receipt arguments:

- `--root /tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0`
- `--receipts /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutIndexById-2`

Within each phase it concurrently launched the following exact commands, each bounded to 120 seconds. Phases were sequential; restoration preceded the final phase.

```sh
/usr/bin/python3 -B /tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0/plans/config_projection.py --selftest --root /tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0
/usr/bin/python3 -B /tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0/plans/config_projection.py --summary --root /tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0
/usr/bin/python3 -B /tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0/plans/config_projection.py --json --root /tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0
```

The harness additionally called the copied module's `audit_text` on the unchanged integrated shuffled-ID fixture to expose exact record differences. It did not execute or import the upstream generator. It also enumerated every frozen raw task ID and every returned profile filename.

| Byte state | `--selftest` exit | `--summary` exit | `--json` exit | Shuffled expected-record field mismatches |
|---|---:|---:|---:|---:|
| Pristine | 0 | 0 | 0 | 0 |
| Mutated | 1 | 0 | 0 | 2 |
| Restored | 0 | 0 | 0 | 0 |

| Byte state | Selftest elapsed seconds | Summary elapsed seconds | JSON elapsed seconds |
|---|---:|---:|---:|
| Pristine | 0.646761 | 0.182607 | 0.203034 |
| Mutated | 0.036752 | 0.184887 | 0.195213 |
| Restored | 0.706805 | 0.224656 | 0.249011 |

No command timed out. These are detector process exits, not the harness's own exit status.

Pristine/restored selftest stdout each began `SELFTEST clean cases=20` (3 words), contained `hand_index_r29_index_shuffled_ids_1_0`, and was byte-identical: 599 bytes, SHA-256 `1fa3c1fcb6d6b3f7b2a83097b8473343bf278fb20b88c1fcfa99161878058d44`. Both had empty stderr.

Mutated selftest stdout was empty. Its stderr was 850 bytes, SHA-256 `a33e24926cd653a48468ae01885efff7f2138578195ccff15074d142c074d8d2`, ending in `AssertionError` (1 word). The traceback identified `/tmp/KengakuR29-2.FMutIndexById-2.1fo31gh0/plans/config_projection.py:456` in `selftest`, with this exact failing assertion (15 words):

```python
assert [{"task_id": t["task_id"], "output_ordinal": t["output_index"], "output_filename": t["output_filename"], "projected_task": t["projected_task"]} for t in tasks] == index_case["expected_records"]
```

## Every shuffled-record mismatch

Unchanged fixture: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/hand/index-shuffled-ids.fixture.json`, SHA-256 `938771045ddbe6bdf6323858bc2c3204e38d028f1086bf83758b79a255fc9254`.

Its input at line 16 orders task IDs `[1, 0]`. Expected output ordinals are `[0, 1]` at line 25. The following are all differences across the fixture's expected record fields; task IDs, output ordinals, and projected task objects matched.

| Actual result JSON path | Fixture expectation location | Output ordinal | Task ID | Expected filename | Mutant filename |
|---|---|---:|---:|---|---|
| `/profiles/distinct_origins/tasks/0/output_filename` | `/expected_records/0/output_filename`, fixture line 31 | 0 | 1 | `config_files/0.json` | `config_files/1.json` |
| `/profiles/distinct_origins/tasks/1/output_filename` | `/expected_records/1/output_filename`, fixture line 41 | 1 | 0 | `config_files/1.json` | `config_files/0.json` |

The diagnostic returned no invariant findings even on this shuffled hand input; the explicit expected-record selftest assertion supplied the kill. This distinction is observed, not an assertion that the audit reports its own filename consistency.

## Can frozen real data alone detect it?

**No, for this mutant and this frozen population.** The direct raw-data enumeration observed 812 tasks and zero positions where `task_id` differed from the enumeration index. Each of the three profile outputs contained 812 tasks and zero filename-versus-index mismatches, including in the mutated state. The observed total remained 2,436 task/profile projections.

All three summaries contained these exact lines:

- `INDEX {"index_equals_task_id": 812, "violations": 0}` (5 words).
- `TOTAL findings=0 exit=0` (3 words).

The complete summary outputs were byte-identical across pristine, mutated, and restored states: 6,914 bytes, SHA-256 `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`.

The complete frozen `--json` outputs were also byte-identical across all states: 3,881,050 bytes, SHA-256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`. Thus the frozen-data result is not merely an unchanged summary total. The shuffled hand witness is necessary to distinguish the two filename rules in this probe. No broader input-domain or exhaustive mutation claim follows.

## Byte identity and restoration evidence

| Instrument state | Bytes | SHA-256 |
|---|---:|---|
| Pristine copied instrument | 34,007 | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |
| Mutated copied instrument | 34,028 | `579f57d09e5f4c50da7d2de36f9fed5779b99328b3451d4378463701ac5b870b` |
| Restored copied instrument | 34,007 | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |
| Lane instrument, after restoration | 34,007 | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |

Direct pristine-versus-restored instrument byte equality was true. The restored copied tree contained the same 119 file-byte hashes, with zero missing, added, or changed file entries. The lane's `plans/` tree also had zero file-hash differences from the initial copy.

Tree fingerprint definition: SHA-256 of sorted compact JSON mapping plans-relative filenames to SHA-256 of their file bytes.

- Pristine/restored tree fingerprint: `bfa950bb6e606b3a642924933a2cb917c17e0aeed8f1d48e3a2f37819814e79f`.
- Mutated tree fingerprint: `bcbfbc824a4444646a2a6ccdbaae331c8425482807684555d087387f65d7cc3d`.

## Durable evidence and tooling

All probe receipts are in `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutIndexById-2/`:

- `initial-identity.json`: all copied file hashes, copy mismatch count, symlinks, and original tree fingerprint.
- `mutation.diff`, `mutation-identity.json`: the one-line mutant and before/after instrument identities.
- Each of `pristine/`, `mutated/`, `restored/`: exact command argv, elapsed seconds, exits, stdout/stderr bytes and hashes in `detector-result.json`; untrimmed `selftest.stdout`, `selftest.stderr`, `summary.stdout`, `summary.stderr`, `json.stdout`, `json.stderr`; complete `hand-diagnostic.json` and `frozen-diagnostic.json`.
- `final-comparison.json`: direct stdout byte comparisons and observed exit/mismatch counts.
- `restoration.json`: direct restored byte equality, tree mismatches, and lane identity.
- `quote-counts.json`: programmatic whitespace word counts for the source/output quotations above; maximum 15 words.

Tool installs/updates: none. Used the existing `/usr/bin/python3`, version 3.14.8, and stdlib only. No pacman transaction, service restart, REA device, delegation, or other runtime was invoked.

Scoped verdict: the assigned task-ID filename mutant was killed by the integrated shuffled-ID selftest, the author-reported behavior was reproduced, and exact bytes were restored. Frozen real data alone supplied no discriminating signal. No production change or round admission is proposed.

VERDICT: PASS
