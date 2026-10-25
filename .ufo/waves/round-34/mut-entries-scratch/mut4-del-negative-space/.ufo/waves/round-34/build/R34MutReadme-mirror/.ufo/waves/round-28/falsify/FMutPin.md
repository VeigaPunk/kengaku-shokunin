# FMutPin — manifest trust-root mutation probe

Seat: KengakuR28.FMutPin. Author-side round28 falsification only; no admission decision.

## Scope and axes

- Axes: legacy novelty → canonical coverage/constructs7, and calibration8; scores held. This probe challenges source-byte pinning, not benchmark validity or model ability.
- Read `plans/round-28-claims.md`, including Amendment1, and `corpus/lessons/round-28.md`. Tested the delivered `plans/benchmark_spec_audit.py` on isolated scratch copies only.
- Frozen draft: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, observed SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`.
- Canonical candidate: `corpus/knowledge/webarena-task-spec-audit.md`; not admitted by this report. This is not a complete Q10 source/number reread or an overall C1/C2 verdict.

## Mutant and expected detector

One behavior-bearing code point changed: scratch `plans/benchmark_spec_audit.py:185`.

```diff
-    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
+    if False and hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
```

This disables only the manifest trust comparison. Per-source digest comparison, selection pin, schema audit and scorer AST analysis remain intact. The code mutation was not applied to production. Exact patch: `.ufo/waves/round-28/scratch/FMutPin/mutation.patch`.

Expected detectors:

1. Shipped `--selftest`: pristine/restored exit0 with 21 cases; mutant must be rejected at its stable manifest-pin expectation.
2. Independent coherent-input witness: alter a known raw task field and correctly rebind its manifest digest, leaving the script's trusted manifest constant unchanged. Pristine/restored must return exit2 / `manifest_tampered`; a mutant exit0 / no findings is a detector mismatch and kills the mutant. No unknown API is executed.

## Independent raw-task witness

Scratch task0 `eval.reference_answers.exact_match`, raw source line23: `Quest Lumaflex\u2122 Band` → `Quest Lumaflex\u2122 Bond`. Exactly one ASCII byte changes; the 880776-byte file length, task IDs, schema and selection remain unchanged. The raw annotation at line28 is intentionally unchanged. The manifest's raw-task `sha256` is rebound to the actual altered bytes; its `bytes` remains correctly 880776, with all other manifest entries unchanged.

Source location for the original value: S061, <https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json>, local pinned source read 2026-10-21, task0:23. No remote request was made for this probe.

The coherent tamper is the same byte sequence in all three code states. Before the independent witness, all declared source hashes match the rebound manifest. Therefore the original-code rejection is specifically the manifest trust root, not a malformed task, missing input or per-source digest mismatch.

## Commands and actual outputs

All detector stdout/stderr and input hashes are retained under `.ufo/waves/round-28/scratch/FMutPin/`. Actual full commands and outputs are recorded in `probe-evidence.json`. Equivalent command expansion:

```sh
R=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/FMutPin
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp" /usr/bin/python -B "$R/lane/plans/benchmark_spec_audit.py" --root "$R/lane" --selftest
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp" /usr/bin/python -B "$R/lane/plans/benchmark_spec_audit.py" --root "$R/lane" --json
```

Each of those two bounded detectors ran on pristine, mutated and restored script bytes, with the appropriate identical input state for each detector. One final `--summary` ran after restoring both script and input bytes. Each external invocation had a 25-second bound; none timed out.

| Evidence prefix | Code / input state | Actual exit | Actual output / finding |
|---|---|---:|---|
| `01-pristine-selftest` | pristine / pristine | 0 | `SELFTEST clean cases=21`, including `cli_snapshot_pin`, `cli_missing_input`, `cli_manifest_pin` |
| `02-pristine-coherent-tamper` | pristine / coherent raw+manifest tamper | 2 | JSON `findings: [{"id":"manifest_tampered"}]`; no metrics computed |
| `03-mutant-coherent-tamper` | mutant / identical coherent tamper | 0 | JSON `findings: []`; emitted task0 exact-match value is `Quest Lumaflex™ Bond` |
| `04-mutant-selftest` | mutant / pristine | 1 | `AssertionError` at `cli_manifest_pin`: expected child exit2 / `manifest_tampered`, observed child exit2 / `input_missing` |
| `05-restored-selftest` | restored / pristine | 0 | Same complete 21-case stdout as `01`; stderr empty |
| `06-restored-coherent-tamper` | restored / identical coherent tamper | 2 | Same complete JSON stdout as `02`: `manifest_tampered`; stderr empty |
| `07-restored-clean-summary` | restored / fully restored | 0 | `TOTAL task_count=812 distinct_task_ids=812 site_eval_strata=27 selected_count=16 program_html_targets=651 findings=0 exit=0` |

The mutant accepts the altered reference answer and reports its rebound source digest while retaining the familiar aggregate denominators: 812 tasks, 27 strata, 16 selected and 651 HTML targets. These counters are observations from this run, not a new independent whole-population census or evidence that content identity is unchanged.

### Calibration finding: shipped manifest selftest is coupled to a missing-input control

Production selftest lines279–283 delete the raw task for `cli_missing_input`, then append a space to the manifest without first restoring the task. With the manifest guard disabled, its final child reaches that intentionally missing task and emits `input_missing`. The outer selftest assertion correctly rejects the mutant on the expected finding-ID mismatch, but this witnesses **manifest-vs-missing-input precedence**, not an isolated manifest-only corrupt-input case.

I do not count a generic file-not-found or unrelated setup failure as a kill. The decisive independent witness above has every input present and coherent source digests; its stable `2/manifest_tampered → 0/[] → 2/manifest_tampered` result establishes the kill independently of the selftest's combined-error state. No baseline detector failed its declared expectation. No production repair was made.

## Exact hashes and restoration

| Artifact | Original / final restored SHA256 | Mutated / coherently rebound SHA256 |
|---|---|---|
| `plans/benchmark_spec_audit.py` | `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8` | `8d75e5827037055601cf90a80e2d62608ec36171f4aab4c3aec88e2c4e0ddf76` |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | `aaca483891db5b9bdc19f5da20f090e3c4d681d362f7bcefe82141411a38dc2e` |
| `plans/fixtures/r28/webarena/manifest.json` | `c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd` | `44ad419da7982ed420dbbfb8283b0effb6b4f8b08bd7234a79ccf84edb60404c` |

- The script changes 20307 → 20317 → 20307 bytes; task and manifest lengths stay 880776 and 1259 bytes.
- `probe-evidence.json` records exact original, per-run and final hashes, stdout/stderr digests, commands, exits, extracted findings, and byte-for-byte restoration comparisons for all eight copied inputs.
- Every scratch input exactly equals its original bytes at completion. Each corresponding production input also exactly equals those original bytes. No production, sibling, Git/index, baseline fixture or candidate mutation occurred.
- Pristine/restored selftest stdout SHA256 is identical: `305ef8e409c18f8120d598a80acf473511ae1fa1bb6f65e3689d31cc159e9e1b`.
- Pristine/restored coherent-tamper rejection stdout SHA256 is identical: `c4aa5607863d674c8fc785a6d4355f8cc7bfdb3392078928eec2586a3f54e5f9`.
- Temporary selftest trees were removed by the shipped context manager; the seat's `tmp` directory is empty. Preserved scratch files are scoped inputs, mutation evidence and receipts, not browser/profile stores.

## Boundaries and verdict

Only authorized Python 3.14.8 and stdlib were used, with bytecode disabled. No installs or updates; no pacman, host-service, browser, benchmark-site, upstream-code execution/import/eval, model/runtime, registry or historical-checker action. Only this report and own scratch evidence were written. No delegation, integration, admission or production repair.

**Mutant: KILLED.** One assigned code mutant; no surviving mutant claimed. The independent coherent-rebinding witness rejects pristine/restored code and exposes the mutant's false acceptance with a stable expected exit/finding mismatch. The shipped selftest also rejects it, with the coupled-error limitation disclosed above.

VERDICT: PASS

This verdict covers only the completed FMutPin mutation assignment and exact restoration, not candidate admission, external discernment, semantic task validity, or untested mutations.
