# FMutStatus — disable the cited-not-mined status condition

Seat: `KengakuR28.FMutStatus`. Author-side round28 falsification only.
Axes: legacy novelty → canonical coverage/constructs7; calibration8. Scores held; this probe supplies bounded detector evidence, not method novelty or outside discernment.

## Assignment and invariant

Challenge only `plans/registry_check.py:81–82`: a frozen source row cited by a frozen knowledge file must be `mined`, even when its used-by index is already complete and live. Read the round28 claims, including Amendment1, and the round28 lesson. Production was read-only; every mutation and fixture write was inside `.ufo/waves/round-28/scratch/FMutStatus/`.

## Mutant and isolated witness

One behavior-bearing line changed in the scratch script, then changed back:

```diff
-        if citing and row["status"] != "mined":
+        if False and citing and row["status"] != "mined":
```

This disables only emission of `cited_not_mined`. The `missing_used_by` computation and emission were untouched. The exact change is retained in `scratch/FMutStatus/mutation.patch` under the round28 wave.

Copied only the lane-owned registry checker and its byte-identical frozen population input. Constructed a hand-authored synthetic registry and all35 frozen knowledge-path files under the owned scratch root; production knowledge contents were not copied or evaluated. The pinned population remains the original13 IDs/35 paths. The synthetic witness has exactly one literal reference link:

- `S038`: status `queued`.
- Citing file: `corpus/knowledge/attribution-interval-calibration.md`.
- Used-by: exactly that same existing file.
- `missing_used_by: []` throughout all three runs.
- The other12 rows are valid, uncited queued controls with no used-by paths.

This is a status-only witness, not the historical baseline fixture and not a missing-used-by test. All37 fixture inputs—the population, synthetic registry and35 synthetic knowledge files—are hash-pinned in `expected.json` and remained identical across the experiment.

## Expected detector and actual commands

`detect_status.py` compares the real CLI exit and complete JSON result against hand-authored expectations in `expected.json`. The sole expected finding is:

```json
{"id": "cited_not_mined", "source": "S038", "status": "queued"}
```

Expected checker exit: **1**. Expected counters:13 rows,35 files,1 reference link,1 mismatched source,1 finding. The expectation contains the complete per-row result, including S038's matching citing-files/used-by and empty missing-used-by.

Same bounded detector command for pristine, mutated and restored bytes, from the owned scratch directory:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python -B detect_status.py
```

The detector invokes the same scratch checker command each time:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python -B plans/registry_check.py --root "$PWD" --json
```

The recorded commands use the equivalent absolute scratch paths. Exactly three checker invocations were executed. No stock selftest, general build, lint, formatter, benchmark-site request or upstream execution was run. Existing Python3.14.8 was used; no tools were installed or updated.

## Actual output and verdict

| Bytes | Checker exit | Findings | Mismatched rows | Behavioral detector exit |
|---|---:|---|---:|---:|
| Pristine | 1 | `cited_not_mined`, S038, queued | 1 | 0 |
| Mutated | 0 | `[]` | 0 | 1 |
| Restored | 1 | `cited_not_mined`, S038, queued | 1 | 0 |

All checker and detector stderr captures are empty. In every run, S038 remains `queued`, its citing-files and used-by both contain the same single existing path, and `missing_used_by` remains empty. The only changed result keys from pristine to mutated are `finding_count`, `findings` and `mismatch_sources`. No population/setup error contributed to the mutant's rejection.

**Mutant verdict: KILLED.** The mutant incorrectly returns a clean exit and omits the sole stable expected status finding; the hand-expected detector goes red. Restoring the exact original script makes the same detector green again. The pristine checker's intentional exit1 is the expected negative-fixture result, not an inconclusive baseline failure: the pristine behavioral detector exits0.

This establishes failure-capability for this one disabled-status mutant using an isolated hand fixture. It does not establish that the stock12-case selftest contains this exact status-only witness; that selftest was not run. No production defect beyond the deliberate scratch mutant is claimed, and no survival was observed in this assigned probe.

## Hashes and restoration evidence

SHA256 of the scratch registry checker:

| State | SHA256 |
|---|---|
| Pristine | `41561dfb63a7761efc5c89128ccebbd741718ba9675d59a7f9191130aaba79a4` |
| Mutated | `85ff29c6223b4c49aeddc1e3bc2a91519ee6d133cff02d70c5004a4e0bab1bd9` |
| Restored | `41561dfb63a7761efc5c89128ccebbd741718ba9675d59a7f9191130aaba79a4` |

The restored SHA256 exactly matches pristine and the frozen checker digest. Pristine/restored CLI stdout is byte-identical; both stderr streams are empty. All37 input hashes match the pinned contract in every phase.

The following production guards were hashed before and after the experiment, with identical results. No production source, candidate, baseline fixture, index or version-control state was edited:

| Production path | Before = after SHA256 |
|---|---|
| `plans/registry_check.py` | `41561dfb63a7761efc5c89128ccebbd741718ba9675d59a7f9191130aaba79a4` |
| `plans/fixtures/r28/registry/population.json` | `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` |
| `corpus/SOURCES.md` | `014175dd88f679a23b0f70f88ef10332007b554c88684ba4d0e1532812c619a1` |
| `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` |

## Retained evidence

All paths below are under `.ufo/waves/round-28/scratch/FMutStatus/`:

- `detect_status.py`: finite CLI behavioral detector; SHA256 `23307a30a737e6d42205589409968d044239cf80ec10697ed5f9b90b6d262e3b`.
- `expected.json`: hand-expected full result plus37 fixture pins; SHA256 `93f3bc1dff44dc81e955c0128293a96cde60e77f2e4dd40ac8a000124bef8530`.
- `pristine.detector.json`, `mutated.detector.json`, `restored.detector.json`: raw detector outputs, including actual checker commands, script/input hashes, checker exit, full stdout/stderr and full actual/expected results.
- `pristine.cli.stdout.json`, `mutated.cli.stdout.json`, `restored.cli.stdout.json`: unmodified checker stdout; matching `*.cli.stderr.txt` and `*.detector.stderr.txt` capture the empty stderr streams.
- `probe-summary.json`: observed phase outcomes, three changed result keys, restoration comparisons, input hashes, runtime version and scoped verdict.
- `mutation.patch`: exact one-line mutation, retained without leaving the live scratch script mutated.
- `production-before.sha256`, `production-after.sha256`: actual protected-file hash receipts.
- `plans/registry_check.py`, `plans/fixtures/r28/registry/population.json`, `corpus/SOURCES.md`, `corpus/knowledge/`: restored scratch checker and isolated synthetic witness inputs.

Canonical candidate path: `corpus/knowledge/webarena-task-spec-audit.md`, not admitted by this seat. The draft was hash-guarded only; this is not a Q10 complete source/number reread or a candidate-support verdict. Findings are handed to L1; no judgment, integration or production repair was performed.

VERDICT: PASS
