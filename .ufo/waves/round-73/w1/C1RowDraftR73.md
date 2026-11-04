# C1RowDraftR73

## Deliverables

- `corpus/evidence/round73/w1/c1-rows-draft.md`: eight-row markdown splice, source-line/hash traceability, all eight exact help receipts, fixture audit transcripts.
- `corpus/evidence/round73/w1/c1-rows-draft.json`: identical eight rows as eight-cell lists.
- This exclusive advisory report. No implementation, claims, predicate, registry, external configuration or credential file was written intentionally.

Axes: coverage and calibration. All eight kinds are `gate`: each returns a clean/failed verdict; filenames containing `probe` do not override the assigned criterion. The draft supplies every exit class 0/1/2, self-test spelling, pinned inputs, write scope and owner. Names follow the current appended rows. The round69 nginx entry uses discovered `receipt-v2.txt`, not the live row's absent `receipt.txt`.

## Required proof

All eight `python3 <absolute-script> --help` invocations exit 0 with empty stderr; full stdout and first usage lines are retained in the markdown receipt. No self-test or mutant battery was executed.

Requested literal fixture copy (SKILL.md, plans/, corpus/, SCORECARD.md, LOG.md; no .git): audit baseline and draft splice both exit 1, `MISMATCH 2`, solely `SCRIPT-MISSING grader.py` and hermetic-grader's absent entry. This is a copy-list omission, not a draft-row defect.

Corrected fixture additionally copies unchanged root `grader.py`. Exact command in each state:

```sh
python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture
```

Baseline: exit 0; `INSTRUMENTS total=106 derived=registry rows=106`, `PARSED scripts=106 failed=0`, D1–D4 all `ok n=0`, `MISMATCH 0`, `PREDICATE R73-C2 pass`.

Eight draft rows spliced: exit 0; `INSTRUMENTS total=114 derived=registry rows=114`, `PARSED scripts=114 failed=0`, D1–D4 all `ok n=0`, `MISMATCH 0`, `PREDICATE R73-C2 pass`. Full stdout and empty stderr retained. No other registry row was corrected; the malformed legacy five-cell round66 row was preserved.

## Additional exercised entry observations

Commands below were run from the lane with stdout/stderr excerpts displayed and return codes captured through PIPESTATUS; these are not claimed as green executions:

| command (`python3 plans/` prefix) | rc | observed output |
|---|---:|---|
| `round32_c1_verify.py --lane .` | 1 | `DEFECT V2 cited-row-identity: the S094 registry row cites no URL`; `checks=6 defects=1` |
| `round32_defects.py --lane .` | 1 | `DEFECT R2 round32-report-order-tip: the round-32 report does not cite the final lane tip ea41880fa7`; `checks=7 defects=1` |
| `round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt` | 0 | `CHECK ok cases=5`; `PREDICATE R66-C1 pass` |
| `round66_c1_tensor_probe.py --check-receipt /nonexistent-r73/receipt.txt` | 1 | stderr `FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent-r73/receipt.txt'` (could-not-evaluate exception, not a clean failed predicate) |
| `round69_c1_nginx_probe.py --check-receipt corpus/evidence/round69/nginx/receipt.txt` | 2 | `SETUP receipt-missing corpus/evidence/round69/nginx/receipt.txt` |
| `round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt` | 0 | `CHECK ok cases=7 legs=8 seen_p=8 seen_f=8`; `PREDICATE R70-C1 pass` |
| `round69_c2_routed_defects.py --root .` (timeout 120 wrapper) | 1 | `E7 defect problems=['corpus/evidence/round69/gates/depth-gate.txt:differ']`; `DEFECTS n=1`; `PREDICATE R69-C2 fail` |
| `round70_c2_routed_defects.py --root .` (timeout 120 wrapper) | 0 | `DEFECTS n=0`; `PREDICATE R70-C2 pass` |
| `round69_c2_routed_defects.py --bogus` | 2 | stderr `error: unrecognized arguments: --bogus` |

The corrected round69 `receipt-v2.txt` check was also run using absolute paths from seat scratch: rc 1, `seen_p=8 seen_f=6`, missing F witnesses for `test_nginx_running` and `test_custom_404_page`, stored predicate fail. Full transcript is retained in the draft. It is a real runnable red entry, not a fabricated green fallback.

## Risks and findings

1. Current SKILL.md and gate changed concurrently while this seat was deriving fields. Initial gate output was `ADVERTISED total=113`, `MISSING 8`, rc 1; a later invocation observed `MISSING 0`, rc 0 and `plans_seen=82 plans_only=0`. The visible gate diff changed the extra arm from plans_only to plans_seen; the claims doc gained A1. This seat changed neither and does not certify the original frozen predicate or a landing commit.
2. The frozen C2 literal row target is 106; adding the eight requested rows gives 114. Both counts are measured in the controlled fixture. Rule/target conflict is reported, not edited.
3. The pre-existing `round66_c1_tensor_probe` five-cell line is invisible to both parsers; the new dashed-name row is separately priced. A clean audit does not mean every physical table-like line was priced.
4. The live appended round69 row names an absent receipt. This draft corrects only its own entry to the discovered v2 receipt. Historical red receipts remain red; structural row acceptance does not prove runtime success.
5. Required copy list omits grader.py; the initial red and corrected green transcripts are both retained. The initial scratch was removed before its in-memory receipt was persisted, an ordering defect of this seat; corrected green receipts were persisted before cleanup.
6. Early investigative imports of the registry module were not made with bytecode disabled and may have updated its existing plans/__pycache__ cache, outside authorized writes. Later retained commands used PYTHONDONTWRITEBYTECODE=1. No cleanup of unowned cache files was attempted. Early exploration also used shell paging/search instead of dedicated tools; later exploration used dedicated tools.

## Cleanup and handoff

Scratch `/fast/scratch/hyaku/kengaku-r73/C1RowDraftR73` removed in finally; no seat-created /tmp files. No tool installs/updates. LSP interface unavailable in this tool inventory; no symbol refactor was required. No seats spawned, commits made, or implementation writes performed. Parent owns landing/integration and should reconcile the count conflict, absent round69 entry and malformed legacy row before its post-integration gates. This seat's authorized fixture proof is complete.

## Self-evaluation

Accuracy 4/5: source hashes and exact receipts ground the rows, but structural audit is deliberately weaker than semantic runtime validation. Completeness 4/5: all eight rows and required proof delivered; initial copy-list/receipt-order deviations are explicitly retained. Clarity 4/5: full receipts are lengthy but separate draft, proof and risks. Actionability 4/5: direct splice and JSON supplied; parent must resolve frozen-count conflict. Conciseness 3/5: initial transcript reasoning was excessive; final deliverables consolidate evidence. Mean 3.8/5. Improvements: land the runnable v2 entry without claiming it green; reconcile count and malformed physical row explicitly. Would the user agree: likely on deliverable coverage, with the recorded process defects remaining valid objections.
