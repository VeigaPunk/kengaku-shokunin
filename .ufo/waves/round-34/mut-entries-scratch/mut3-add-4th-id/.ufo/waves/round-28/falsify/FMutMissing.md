# FMutMissing — uncited frozen-source omission mutation

Seat: `KengakuR28.FMutMissing`. Round28 author-side falsification only; not outside/non-author evidence, a round judgment, or admission approval.

## Axes and scope

- Legacy novelty → canonical coverage/constructs **7, held**: one bounded failure-control coverage probe; no novelty or task-validity claim.
- Calibration **8, held**: distinguish stock-selftest survival from independently witnessed detection, and distinguish a coverage gap from a production defect.
- Contract read: `plans/round-28-claims.md`, including Amendment1, especially lines25–27; `corpus/lessons/round-28.md`. Missing **any frozen source row** must fail, regardless of citation count. Uncited queued/rejected rows being permitted does not permit absent frozen rows.
- Frozen draft: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, observed SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`. Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` remains outside this probe's admission authority. This seat hashed the draft, not a complete Q10 source/number reread.

All experiment writes were confined to `.ufo/waves/round-28/scratch/FMutMissing/`; this requested report is the sole additional output path. No production or sibling edits, delegation, Git/index operations, upstream-source execution/import, benchmark-site contact, or other agent/canonical judge-runtime invocation occurred. The owned recorder and copied lane checker were executed with the existing Python interpreter. No builds, linters, formatters, or broader suites ran.

## Mutant: skip a missing frozen source if it has no frozen citations

One two-line insertion in the isolated copy of `plans/registry_check.py`, immediately inside `check()`'s original line68 `if row is None:` branch:

```diff
         if row is None:
+            if not citing:
+                continue
             findings.append({"id": "source_missing", "source": sid})
```

This is a plausible conflation of “uncited rows need not be mined” with “uncited frozen rows need not exist.” It changes neither the population pin nor the stock selftest and contains no source-ID-specific exception. The original missing-row finding remains reachable for cited rows.

Preserved mutation: `scratch/FMutMissing/mutation.diff` and `scratch/FMutMissing/registry_check.mutant.py`, both under `.ufo/waves/round-28/`.

## Expected detectors and independent hand fixture

The stock detector was the unchanged CLI `--selftest`; adequate missing-source coverage would reject this mutant with a stable expected-finding assertion rather than an unrelated setup failure.

A separate hand-authored CLI fixture used the **unchanged pinned 13-ID/35-path population bytes**. All35 knowledge files exist and contain the same reference-free control sentence. Its registry has12 valid, uncited, queued rows with `used-by` set to `—`; only frozen **S060 is absent**. No real source contents, production knowledge contents, or baseline registry rows were copied into this fixture. The fixture's validity expectations were specified in `initial.json`: exit1 and exactly `[{"id":"source_missing","source":"S060"}]`.

The hand witness used the production CLI and its actual population digest check, not an imported checker, repinned population, alternate oracle, or upstream code. Its detector is the conjunction of the expected exit and exact stable finding. Thus an expected negative-fixture exit1 is a **successful baseline detector**, not an inconclusive baseline failure.

Same commands in pristine, mutated, and restored phases, with `W=.ufo/waves/round-28/scratch/FMutMissing` relative to the lane root:

```sh
/usr/bin/python3 -B "$W/plans/registry_check.py" --selftest
/usr/bin/python3 -B "$W/plans/registry_check.py" --root "$W/hand-fixture" --json
```

Each subprocess had a20-second bound, `PYTHONDONTWRITEBYTECODE=1`, and a `TMPDIR` beneath this seat's scratch directory. Pristine/restored independent commands ran concurrently. In the mutated phase the separate hand witness ran **after actual stock-selftest survival**. Three stock-selftest invocations and three hand-witness invocations were performed, once per byte state; none was rerun to confirm a reported failure.

## Actual outputs and finding FMISSING-01

| Byte state | Stock selftest exit / output | Hand CLI exit | Hand findings | Hand detector | Reported source count / result entries |
|---|---|---:|---|---|---|
| Pristine | 0 / `SELFTEST clean cases=12 ...` | 1 | exactly `source_missing`, source `S060` | GREEN: expected exit and ID match | 13 / 13 |
| Mutated | 0 / identical12-case output | 0 | `[]` | RED: expected exit1/finding absent | 13 / 12 |
| Restored | 0 / identical12-case output | 1 | exactly `source_missing`, source `S060` | GREEN: expected exit and ID match | 13 / 13 |

Exact stock stdout, identical in all three states:

```text
SELFTEST clean cases=12 valid_literal_fence,queued_and_missing,missing_used_by,duplicate,source_missing,unsafe_used_by,bad_enum,extra_queued_source,new_file_excluded,missing_frozen_file,cli_population_tampered,cli_population_missing
```

The mutant's hand CLI actually returned:

```json
{"finding_count":0,"findings":[],"knowledge_files_expected":35,"mismatch_sources":0,"reference_links":0,"source_rows_checked":13}
```

The complete output's `sources` array contains only S038 and S049–S059; S060 disappears even while `source_rows_checked` remains13. Pristine/restored instead return `finding_count:1`, `mismatch_sources:1`, and `findings:[{"id":"source_missing","source":"S060"}]`.

**FMISSING-01 — stock missing-source coverage does not distinguish a missing uncited frozen row from an optional uncited row.** The mutant **SURVIVED the stock selftest**. The existing selftest's missing-source case removes S049 while the hand knowledge fixture contains a standalone S049 inside a code fence (`registry_check.py:96,112`); that cited-row case still fails correctly after this mutation. It cannot exercise the new early continue for an uncited missing row. The claimed12-case selftest result therefore does not demonstrate this part of the unconditional frozen-row-presence contract.

The independent hand detector **KILLED the same mutant**: its exact expected `source_missing`/exit1 witness changes to empty findings/exit0 and returns to the expected behavior on restored bytes. All recorded subprocesses have `setup_error:null`; no unrelated setup error is being counted as a kill.

This is a **stock-selftest coverage finding**, not evidence that pristine production currently omits source_missing. Pristine and restored production-equivalent bytes satisfy this witness. No production repair was made, no contract was relaxed, and no broader missing-knowledge-path sensitivity is inferred from this single source-row mutation. The stock `missing_frozen_file` case ran unchanged, but was not independently mutated here. L1 owns disposition.

## Hashes and exact restoration

| Object/state | SHA256 |
|---|---|
| Pristine scratch checker / production checker before and after | `41561dfb63a7761efc5c89128ccebbd741718ba9675d59a7f9191130aaba79a4` |
| Mutated scratch checker / saved mutant | `982f53682af235ce2c73a506b66d3b4ba5ca8f86e6f5431239ff546ab2aec6fa` |
| Restored scratch checker | `41561dfb63a7761efc5c89128ccebbd741718ba9675d59a7f9191130aaba79a4` |
| Original pinned population / hand-fixture copied population | `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` |
| Production SOURCES before and after | `014175dd88f679a23b0f70f88ef10332007b554c88684ba4d0e1532812c619a1` |
| Frozen draft before and after | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` |

The exact two inserted lines were removed from the working scratch copy before the restored runs. `restoration.json` records direct byte equality with `original/registry_check.py` (`exact_byte_restoration:true`), identical before/after hashes for the four guarded production inputs (`guarded_production_unchanged:true`), and unchanged fixture bytes (`fixture_unchanged:true`). The original fixture's37 per-file hashes are retained in `initial.json`; each phase checks and records that same manifest. No fixture restoration was necessary because its bytes were never mutated.

## Evidence and tooling

Evidence root: `.ufo/waves/round-28/scratch/FMutMissing/`.

- `probe.py`: finite recorder and hand-fixture constructor; never mutates or restores the checker itself.
- `initial.json`: hand expectations, input digests,37 fixture-file digests, Python version and initial production guards.
- `{pristine,mutated,restored}.receipt.json`: exact commands, exits, captured stdout/stderr, finding comparisons, script digests before/after each phase, fixture stability.
- `{pristine,mutated,restored}.selftest.stdout.txt` and adjacent `.stderr.txt`: actual stock output; stderr empty in each state.
- `{pristine,mutated,restored}.witness.stdout.json` and adjacent `.stderr.txt`: complete negative-fixture CLI output; stderr empty in each state.
- `mutation.diff`, `registry_check.mutant.py`, `original/registry_check.py`, `plans/registry_check.py`: exact mutation, saved mutant, pristine evidence and restored working bytes.
- `restoration.json`: final byte-equality and guarded-production preservation receipt.

Existing `/usr/bin/python3` **3.14.8** was used. Tool installations/updates: **none**. No pacman transaction or host-service change.

## Final result

Mutation experiment complete: **stock SURVIVED; independent hand witness KILLED; restoration exact**. The stock-selftest coverage claim is incomplete for uncited missing frozen sources; the tested pristine source_missing behavior is supported. No candidate admission or whole-round PASS is asserted.

VERDICT: PARTIAL

## Same-identity replay — current 15-case checker

Requested by L1 `KengakuR28` after the original finding: replay the **same** uncited-missing-row mutant against current checker SHA256 `fc388c332d4e37f8f0f7118d15a0baed8d86cd99b345ab9255e2b9dc6bd7379b`. This section is an append-only disposition of FMISSING-01 for those new bytes, not a rewrite of the original survival.

### Isolation and unchanged experiment

New evidence is confined to `.ufo/waves/round-28/scratch/FMutMissing/v2/`. The current checker and unchanged pinned population were freshly copied there. The hand fixture has the **same37 file hashes as v1**:13 frozen source IDs,35 existing reference-free knowledge files,12 valid queued source rows, absent uncited S060. The mutation is precisely the same two-line `if not citing: continue` insertion inside `if row is None:`, now following current pristine line70. No stock selftest, fixture, population pin, or production code was mutated.

Both detectors ran once per pristine/mutated/restored byte state, with20-second subprocess bounds and bytecode disabled:

```sh
/usr/bin/python3 -B .ufo/waves/round-28/scratch/FMutMissing/v2/plans/registry_check.py --selftest
/usr/bin/python3 -B .ufo/waves/round-28/scratch/FMutMissing/v2/plans/registry_check.py --root .ufo/waves/round-28/scratch/FMutMissing/v2/hand-fixture --json
```

Within each phase the independent stock and hand commands ran concurrently. The hand witness was run even after the stock mutant rejection, as explicitly requested for this replay. No broader suite, production mutation, delegation, installation/update, or host-service action occurred.

### Actual red/green result

| Current-checker byte state | Stock selftest | Separate hand CLI | Hand result entries |
|---|---|---|---:|
| Pristine | exit0; clean15 cases | exit1; exactly `source_missing` for S060 | 13 |
| Same mutant | **exit1; assertion on `uncited_source_missing`** | **exit0; findings `[]`**, violating the expected exit1/`source_missing` contract | 12 |
| Restored | **exit0; clean15 cases** | exit1; exactly `source_missing` for S060 | 13 |

Pristine/restored stock stdout is identical:

```text
SELFTEST clean cases=15 valid_literal_fence,queued_and_missing,missing_used_by,duplicate,source_missing,uncited_source_missing,unsafe_used_by,bad_enum,extra_queued_source,outside_duplicate_excluded,outside_malformed_excluded,new_file_excluded,missing_frozen_file,cli_population_tampered,cli_population_missing
```

Mutated stock stdout is empty. Its actual stderr ends with the stable, expected case/finding mismatch:

```text
    run("uncited_source_missing", row("S038"), ["source_missing"])
    assert actual == set(expected), (name, actual, expected)
AssertionError: ('uncited_source_missing', set(), ['source_missing'])
```

All six subprocess records have `setup_error:null`. The stock red is therefore a real behavioral kill, not a setup error. The hand witness independently still kills the mutant by its expected exit/finding mismatch. Its deliberately invalid fixture yields expected exit1 both before and after mutation restoration; this is not a failed baseline. The mutant still falsely reports13 rows checked while omitting S060 from the12 emitted source results, just as in v1.

**Replay disposition:** the **current stock detector KILLS this same mutant**, and the independent hand detector also KILLS it. The added current `uncited_source_missing` case (`plans/registry_check.py:115–117` in pristine current bytes) directly exercises the previously uncovered uncited branch. FMISSING-01's specific current-checker coverage gap is resolved by this observed replay; its historical v1 survival remains retained and true. This does not establish general mutation completeness or independently validate the parser's other new boundaries.

### Replay hashes, restoration and preservation

| Object/state | SHA256 |
|---|---|
| Current pristine checker / restored working copy / production checker before and after replay | `fc388c332d4e37f8f0f7118d15a0baed8d86cd99b345ab9255e2b9dc6bd7379b` |
| Current same-mutant working bytes / preserved mutant | `7554954af4999a07532bc21861393d62c01f205fe27aca78affda93372b2211b` |
| Unchanged pinned population | `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` |
| Production SOURCES before and after this replay | `255105f39134c9e427dccd9200c5f5a74bcb0d068de53643fdc3745fa944f8bf` |
| Draft candidate before and after this replay, hash-only observation | `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182` |

`v2/restoration.json` records `exact_byte_restoration:true`, `fixture_unchanged:true`, `fixture_identical_to_v1:true`, `guarded_production_unchanged:true`, and `v1_evidence_unchanged:true`. The working current scratch copy was restored by removing the exact inserted lines before the restored detectors ran. The complete before/after manifests in `v2/v1-preservation-{before,after}.json` show every v1 scratch evidence file unchanged. No original receipt was overwritten.

Evidence under `v2/`: `initial.json`, `{pristine,mutated,restored}.receipt.json`, matching `.selftest.stdout.txt` / `.selftest.stderr.txt` and `.witness.stdout.json` / `.witness.stderr.txt`, `mutation.diff`, `registry_check.mutant.py`, `original/registry_check.py`, restored `plans/registry_check.py`, `restoration.json`, and both v1-preservation manifests. `v2/probe.py` reuses only this seat's owned v1 recorder; it never executes upstream source or edits/restores the checker.

The different current SOURCES/draft digests are L1-side state observed at the replay's start, not changes made by this seat; each remains identical throughout this replay. Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is not admitted or source/number-approved by this experiment. The verdict below is **only** complete support for this requested same-mutant replay on the stated checker hash, superseding the earlier PARTIAL for that narrow current-detector question, not for historical v1 or the whole round.

VERDICT: PASS
