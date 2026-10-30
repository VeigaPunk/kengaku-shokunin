# C1RelabelRev2 — blind oracle re-label

Axes: novelty and calibration; operational priorities: independent labels, complete reachable-code reading, explicit uncertainty.

## Results

20 assigned ids labeled: **Y 14, N 6, U 0**. Read all 16 assigned Python capture files, all 16 sibling shell harnesses, and the additional large-scale-text-editing environment Python capture: 33 complete capture files. No assigned function requests a fixture or calls a same-file helper; noncalled helper functions and other tests do not enter its reach.

This is an independent label recommendation, not an oracle-agreement measurement or admission. No prior labels, classifier, freeze, counter, wave-1 or wave-2 artifacts were opened. The seat-specific blind-read restriction superseded the general request to read claims/facts. No actual implementation diff was assigned; runtime identity, rerouting, saturation and resume behavior are outside this shard.

Observed lane HEAD: `9ead4476bf55b1ea6490d0204b668195db4a4d1d`. This is a read-only observation, not a tested revision. No clone or scratch directory was needed: no grader, classifier, counter, campaign, test, build or fixture command was executed.

## Decisive difficult cases

All capture paths below are relative to `corpus/evidence/round52/graders/`; definition citations refer to `.ufo/waves/round-53/p1-spec.md`.

- **N — build-cython-ext::test_ccomplexity_cython_extension** (`build-cython-ext/tests/test_outputs.py:59-65`), **test_cinvariants_cython_extension** (`:68-74`), and **test_pyknotid_core_import** (`:41-47`): each compares the returned import specification and its loader class. These are not filesystem path-type predicates. Deciding clause: N, lines 27-28, “a return value”; also Y requirement 2, lines 19-22. No U is necessary: these visible comparisons already exclude Y without examining pyknotid internals.
- **N — make-doom-for-mips::test_frame_bmp_exists** (`make-doom-for-mips/tests/test_outputs.py:61-65`): the second assertion requires positive byte size. Deciding clause: N, lines 27-28, “size”. Existence alone is insufficient.
- **N — merge-diff-arc-agi-task::test_algo_py_has_map_function** (`merge-diff-arc-agi-task/tests/test_outputs.py:40-49`): executes the delivered Python module, then asserts attribute presence and callability. Deciding clause: Y requirement 2 restricts permitted predicates to filesystem existence/type; Y requirement 3, lines 23-25, additionally excludes content-reading deliverable execution. The visible callable predicate settles N even without the missing deliverable bytes.
- **N — kv-store-grpc::test_grpc_server_functionality** (`kv-store-grpc/tests/test_outputs.py:138-171`): performs RPCs and compares response values. Deciding clauses: Y requirement 3, lines 23-25, “uses the network”; N, lines 27-28, “a return value”. Missing generated-module bytes do not make this U because the captured function already decisively excludes Y.
- **Y — kv-store-grpc::test_protobuf_generation** (`kv-store-grpc/tests/test_outputs.py:50-64`): only two generated-path existence assertions; it neither imports nor executes either generated file. Deciding clause: Y requirement 2, lines 19-22. Other tests' imports are not reached under Reach, lines 11-14.
- **Y — prove-plus-comm::test_compiled_proof_exists** (`prove-plus-comm/tests/test_outputs.py:11-14`): the filename implies compilation but the function only asserts existence. Deciding clause: Y requirement 2, lines 19-22. Separate compiler/content tests do not change this function's reach.
- **Y — large-scale-text-editing::test_apply_macros_exists** (`large-scale-text-editing/tests/test_outputs.py:123-125`): only the script's existence is asserted. Deciding clause: Reach, lines 11-14, “every same-file helper it calls”. It calls none of the content or command helpers. Shell-harness setup is inspected context, not an extra function-body assertion.

## Evidence and limitations

No actionable defect in the assigned definition or these captured functions was established beyond the six explicit non-presence-only verdicts. No oracle disagreement claim is possible while blind. No U labels were needed; each N has a visible exclusion independent of missing deliverable code. Static manual interpretation only: these are not mechanical touch-run results. Main can compare these 20 labels with the oracle after unblinding; that comparison was intentionally not performed here.

Semantic tooling gap: `read xd://lsp` returned `No such tool: xd://lsp`; no LSP server/status, references, definitions or diagnostics device was available. Whole-file direct inspection is the fallback, not semantic-server proof. No text grep was used.

Attack surface: oracle-label misclassification, especially misleading existence-oriented names and imported deliverables. Six functions visibly failed the touch-sufficient criterion. Whether that falsifies an oracle label remains deliberately unknown.

## Exact operations

Only one shell command ran:

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
```

Read operations: `read` the complete p1 spec, shard (including `:raw:1-1` after its long line was truncated), operator rules, godspeed skill, completion self-evaluation skill, and the unavailable `xd://lsp` device. Captures were read through concurrent `tool.read` calls with `{i: 'Reading entire grader capture', path: p + ':1-2000:raw'}` for every absolute `p` listed in `read-manifest.json`. Sibling discovery used `tool.glob({i: 'Locating sibling capture files', path: p.rsplit('/tests/',1)[0] + '/**', hidden: true, gitignore: false, limit: 100})` once for each of the 16 distinct shard file paths. No shell search or runtime command ran. Labels were manually decided, then JSON-serialized; the label count was computed with `collections.Counter` over those manual decisions, not by a classifier.

No tool installation/update. No ENOSPC. No scratch artifacts or fixtures were created, hence none remain to remove. No package transactions or host changes.

## Produced files

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RelabelRev2/labels.json`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RelabelRev2/read-manifest.json`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RelabelRev2.md`

## Self-evaluation

Accuracy 4/5: direct complete capture reading; no independent runtime evidence. Completeness 5/5: every assigned id and all discovered same-task captures covered. Clarity 4/5: loader-metadata distinctions need more explanation than ordinary existence predicates. Actionability 5/5: exact id-keyed labels ready for L1 comparison. Conciseness 4/5: operation provenance length is necessary for the report contract. Overall 4.4/5. Most useful improvement is post-blind comparison by L1; no independent agreement claim is made. The user should agree with the static-only limitation.
