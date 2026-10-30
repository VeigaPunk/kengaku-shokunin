# C1RelabelRev4 — blind oracle re-label

Axes: novelty and calibration. Independent static reading only; no classifier, counter, oracle comparison, grader execution, or alternative runtime invoked.

## Result

20 assigned ids labeled: **14 Y, 6 N, 0 U**. These are recommendations for L1 reconciliation, not an admission or a saturation claim. No actual implementation diff was assigned to this seat.

Produced:
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RelabelRev4/labels.json`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RelabelRev4.md`

Read all 17 assigned Python capture files in full and their 17 captured `tests/test.sh` siblings. File discovery returned only those two files per task. No requested same-file fixture or helper was omitted: assigned tests have no fixture arguments except the portfolio parameter `n`, which is explicitly parametrized. Separate sibling tests are not transitive calls.

## Hardest decisions and deciding clauses

Paths below are relative to `corpus/evidence/round52/graders/`; spec references are `.ufo/waves/round-53/p1-spec.md`.

| Id | Label | Concrete evidence and deciding clause |
|---|---|---|
| build-pmars::test_built_from_source | Y | `build-pmars/tests/test_outputs.py:73-85` asserts nonempty directory and C-source globs and src existence. Spec Y.2, lines 19-22 explicitly permits nonempty globs. Choosing the first matching path does not read its bytes or compare counts. |
| mailman::test_mlist_exists | N | `mailman/tests/test_outputs.py:164-167` calls same-file `get_mlist`, lines 73-80, returning a mailing-list manager lookup result. The assertion checks that result, not a named filesystem path. Reach, lines 11-14, includes this helper; N, lines 27-28, covers return values/process state. External implementation is unnecessary to decide that the visible assertion is not path existence. |
| portfolio-optimization::test_baseline_functionality | N | `portfolio-optimization/tests/test_outputs.py:68-78` visibly compares numerical outputs and weight sum. N, lines 27-28, covers computed values. U, lines 30-31, does not apply merely because baseline implementation is uncaptured: the visible assertion conditions already decide N. |
| portfolio-optimization::test_performance_and_scalability | N | Same capture, lines 106-132, compares computed risk/return and speedup. Same-file `time_function`, lines 23-31, invokes the functions and returns elapsed-time data. Reach and N decide this without knowing imported implementations. |
| build-cython-ext::test_example_usage | N | `build-cython-ext/tests/test_outputs.py:126-137` calls task-package APIs and compares computed polynomial/determinant results. Y.3, lines 23-25, excludes imported deliverable calls and computed-value comparisons; N, lines 27-28, applies. |
| fix-code-vulnerability::test_hkey_basic_cases | N | `fix-code-vulnerability/tests/test_outputs.py:55-79` calls the deliverable helper and compares returned strings. Y.3 and N apply even though the imported implementation is absent. |
| fix-code-vulnerability::test_hkey_error_cases | N | Same capture, lines 82-99: the call must raise the expected exception; normal return or a different exception reaches a failing assertion. Y.3 excludes task-deliverable calls; N covers behavior beyond existence. U is unnecessary because that exclusion is visible. |
| financial-document-processor::test_directories_created | Y | `financial-document-processor/tests/test_outputs.py:18-28` checks only existence and directory type. Y.2 explicitly permits both. The content-hashing helper at lines 11-15 is not called, so Reach does not import it into this verdict. |

All other assigned Y decisions are direct existence assertions, with their exact ids and short explanations in labels.json. Required-file iteration in `cobol-modernization/tests/test_outputs.py:11-18` likewise adds no assertion about count or contents.

## Procedure and exact commands

Only shell command executed:

```text
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
```

Observed metadata revision: `9ead4476bf55b1ea6490d0204b668195db4a4d1d`. This was recorded after the static reads, not represented as a pinned execution revision. No grader run occurred; therefore no run clone, fixture repository, scratch directory, disk-heavy pass, or cleanup was needed.

Read-device calls: `skill://godspeed`, `/home/vgpnk/.omp/agent/RULES.md`, `skill://agent-self-evaluation`, `xd://lsp`, the full `p1-spec.md`, and `relabel/shard-R4.json:raw:1-1` (following the initial truncated shard display). The more specific blind-item restriction was honored instead of opening campaign facts/claims, prior-wave labels, freeze data, or classifier code.

Capture discovery used glob with `hidden=true`, `gitignore=false`, `limit=200` on:

```text
/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/{build-pmars,mailman,portfolio-optimization,extract-moves-from-video,raman-fitting,build-cython-ext,path-tracing,video-processing,pytorch-model-recovery,cancel-async-tasks,pytorch-model-cli,fix-code-vulnerability,path-tracing-reverse,crack-7z-hash,cobol-modernization,financial-document-processor,tune-mjcf}/**/*
```

For each task in that exact brace list, used `read` on both absolute paths ending `/tests/test_outputs.py:1-10000` and `/tests/test.sh:1-10000`. Concurrent Eval calls dispatched these read operations and displayed their returned text, rather than importing or executing captures. Every file ended within the selected range.

## Residual risk / verification gaps

- LSP device unavailable: reading `xd://lsp` returned `No such tool`; semantic references/definition/diagnostics could not be requested. Conclusions use captured source reading, not semantic-server proof.
- No oracle or classifier was opened; agreement/disagreement and aggregate accuracy are intentionally unmeasured.
- No attack/runtime pass was assigned. These labels concern individual reachable assertions, not whether touching files passes a complete task grader or its shell wrapper.
- No source changes, builds, tests, linters, or formatters performed. No tools installed or upgraded. No inconsistent tool behavior observed.

Self-evaluation: accuracy 4/5 (static evidence only, no independent adjudication); completeness 5/5 (20 labels and 34 capture reads); clarity 4/5 (long identifiers require table lookup); actionability 5/5 (directly consumable labels.json); conciseness 4/5 (procedure detail retained for reproducibility). Overall 4.4/5. Highest-value remaining check is L1's blind-label reconciliation, intentionally outside this seat's access. The assessment should match the user's requirement for independent, bounded reading rather than runtime confirmation.
