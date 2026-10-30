# C1CritNeverRead — bounded documentary review

Axes: novelty and calibration. No admission or score judgment made.

## Settlement

The frozen, expressly narrow definition of **never-read** is not falsified by this review. It means absence from the enumerated base-tip narrative texts, excluding the round-52 triage entry, and absence from round-52 confirmations. A1 explicitly acknowledges that prior machine classifications are outside that definition. Do not silently substitute a wider definition or change the frozen counter.

However, **unqualified claims that the lane had never examined these tasks are contradicted by base-tip evidence**. The strongest counterexamples are `pytorch-model-recovery` and `torch-tensor-parallelism`: round-52's quote-verification report already located the identical assertion, in the identical task, at the identical capture line later used by the round-53 confirmation.

This is a fixable provenance/narrative defect, not a demonstrated failure of the frozen CONFIRM predicate. The canonical judge retains the axis decision.

## Snapshot and method

Read facts first, then the full frozen claims including A1–A3. Fresh shared clone HEAD: `9ead4476bf55b1ea6490d0204b668195db4a4d1d`. Historical sweep revision: `536925b5320fa64298030b4ee76a58fc4b82723f`. Later lane changes were not measured. Disk guard reported 463.2G free under `/fast/scratch/hyaku` before cloning; no ENOSPC.

Swept all 20 integrated confirmations against these base-tip paths: `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/lessons/`, `corpus/evidence/`, `plans/`, `.ufo/waves/round-52/`. The union contained 2,382 files. Each task was searched literally, then filtered with the counter's token boundary: `(?<![A-Za-z0-9-])TASK(?![A-Za-z0-9-])`. No hits in PROVINCE or QUALITY; lesson hits concerned pytorch-model-recovery and torch-tensor-parallelism. All 20 had hits in round-52 artifacts, evidence and plans. File:line evidence for every task is in `C1CritNeverRead/evidence.json` and the TSV.

## Counterexample and prior-examination classification

### Strongest: already located identical assertions

At the base tip:

- `.ufo/waves/round-52/w2/W2ScoutVerifyQuotes.md:14`: same-task assertion for `pytorch-model-recovery`, capture line 108, in `test_model_file_exists`. Round 53 confirms that same test and line.
- `.ufo/waves/round-52/w2/W2ScoutVerifyQuotes.md:15`: same-task assertion for `torch-tensor-parallelism`, capture line 25, in `test_parallel_linear_exists`. Round 53 confirms that same test and line.

These are prior examination, not a name census. The report documents fresh fetches, byte/digest comparisons, line locations and function names.

The excluded knowledge entry also records prior examination: `corpus/knowledge/tb2-grader-vacuity-triage.md:52-53,92-93`. Its earlier quoted docstrings lie inside the exact confirmed spans: pytorch-model-recovery 103–108 and torch-tensor-parallelism 18–25. The exclusion is explicit in the frozen rule, so these are semantic/provenance counterexamples, not undisclosed counter implementation bugs.

### Previously published per-test findings

Eight of the 20 confirmed tests were already P1 in the base-tip round-52 classifier artifact and already named in its committed candidate receipt `.ufo/waves/round-52/claims/c1-after.txt`:

| task | receipt line |
|---|---:|
| log-summary-date-ranges | 19 |
| mteb-leaderboard | 20 |
| path-tracing | 25 |
| path-tracing-reverse | 26 |
| prove-plus-comm | 27 |
| pytorch-model-cli | 28 |
| sam-cell-seg | 31 |
| winning-avg-corewars | 34 |

Those lines name the exact presence-only test subsequently confirmed, not merely the task. Round-52 classifier error means its classes are not ground truth; nevertheless these are prior examination and prior publication of the same finding.

Another eight distinct confirmed tasks had their exact test independently labeled P1 in `.ufo/waves/round-52/w2/W2ExecEntryDraft/candidate-audit.json`, under `non_candidate_counter_misses`: extract-moves-from-video, fix-code-vulnerability, gcode-to-text, llm-inference-batching-scheduler, merge-diff-arc-agi-task, sparql-university, torch-pipeline-parallelism, tune-mjcf. Each record includes a function name and definition line. These are prior per-test examination, not census membership. See the JSON receipt for exact file lines.

`C1ScoutVacuity/per-task.jsonl:50` already records modernize-scientific-stack's assertion in `pure_asserts`, capture lines 49–50; line 82 records torch-pipeline-parallelism's assertion, capture lines 26–28. These are task-scoped assertion analysis. The round-52 `corpus/evidence/round52/labels.json` additionally contains grader-specific class/reason prose for nine of the 20 tasks.

All 20 exact confirmed test functions occur in the base-tip per-test classification artifact `.ufo/waves/round-52/w1/C1ExecClassifier/artifacts/per-test-classes.json`: eight P1, one P2, eleven P3. This is machine examination, not proof of prior hand-reading. Do not equate bulk classification with a human confirmation.

### Census hits that do NOT establish prior examination

`plans/round52-tasks.json`, `corpus/evidence/round52/graders/SHA256SUMS`, fetch manifests, digest manifests and benchmark tree listings merely enumerate names/paths/digests. Their hits alone do not establish that a reader examined a task. Generic assertion strings also collide across tasks: gcode-to-text and pytorch-model-recovery share one assertion string; that string match alone is not prior examination of gcode-to-text. A weights assertion in older prose is attributed to a different task; it is not treated as reliable same-task evidence.

## Negative attacks: overlap and fabrication

- Round-52 confirmations: 16 rows, eight distinct tasks. Overlap with the 20 round-53 tasks: **zero**.
- Independently re-located **all 20**, exceeding the requested five quotes. Every quote is verbatim at its claimed line and inside the indexed test function span. No quote fabrication found.
- All 20 report digests matched; their five reader report paths contain the reader name, name the task, and contain the quote. Readers are disjoint from the four freeze author seats.
- Representative re-locations: cobol-modernization line 18 within 11–18; log-summary-date-ranges line 29 within 27–29; extract-moves-from-video line 334 within 327–334; torch-tensor-parallelism line 25 within 18–25; pytorch-model-recovery line 108 within 103–108. Full 20-row receipt saved.
- Capture bytes for these 20 were unchanged between the base tip and the cloned HEAD.

## Observed counter behavior and limits

At the cloned HEAD the counter printed `CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0 target>=3`. PRIOR-ART had zero rows, and the overall predicate printed fail. The shell pipeline printed EXIT=0 because it observed the final pipeline command, **not the counter's exit code**; no counter exit-code claim is made.

An exploratory scratch-only widening to seven prior-analysis files plus the excluded knowledge entry produced zero candidates and zero retained confirmations. This is a counterfactual sensitivity measurement, **not a failure of the frozen rule and not a new admission criterion**: bulk per-test receipts name the entire population, so raw widening changes what is measured. No grader was executed in this review.

## Smallest safe correction / falsifier

Keep the frozen definition unchanged. In entry/lesson/log prose, qualify the result as **20 confirmations eligible under the frozen narrative-text blocklist, disjoint from round-52 confirmations**, not 20 tasks never previously examined by the lane. Explicitly name the two prior located assertions and the prior machine/independent AST findings. Preserve the independent readers' actual contribution: direct confirmation against captured function spans.

A genuine falsifier of the frozen never-read gate would be a confirmed task occurring as a whole token in a non-excluded enumerated base-tip text, or appearing in round-52 confirmations, while still being accepted. None was found. A falsifier of the broader, unqualified historical claim is already present: the same-task, same-line quote-verification receipts above. Do not silently convert that broader claim into a new frozen predicate.

## Commands and produced files

Exact command families executed (Python `subprocess.run` expanded TASK/PATH for the 20 confirmation rows):

```sh
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
mkdir -p /fast/scratch/hyaku/kengaku-r53/C1CritNeverRead
# From that scratch directory:
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C /fast/scratch/hyaku/kengaku-r53/C1CritNeverRead/lane rev-parse --show-toplevel
git -C /fast/scratch/hyaku/kengaku-r53/C1CritNeverRead/lane rev-parse HEAD
git -C CLONE ls-tree -r --name-only BASE
git -C CLONE show BASE:PATH
git -C CLONE grep -n -I -F -e TASK BASE -- PROVINCE.md corpus/QUALITY.md corpus/lessons corpus/evidence plans .ufo/waves/round-52
git -C CLONE grep -n -I -F -e TASK BASE
# Counter observation (pipeline exit caveat above):
timeout 600 python3 plans/round53_c1_triage.py --lane .
```

Quote verification used JSON parsing of tests-index and confirmations, direct capture line slicing, substring matching, and hashlib.sha256 for reports. No test harness, grader bypass, external campaign, agent runtime or judge was invoked.

Produced absolute paths:
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1CritNeverRead.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1CritNeverRead/evidence.json`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1CritNeverRead/never-read-widened-evidence.tsv`

Tool installations/upgrades: none. Tool note: an invalid JSON read query failed; ordinary JSON parsing was used instead. An initial rules-file path typo failed and was corrected. No tool inconsistency inferred from those input errors. Preliminary substring-based TSV was replaced with exact JSON task-key matching to avoid path-tracing/path-tracing-reverse conflation. Scratch removed before settlement.
