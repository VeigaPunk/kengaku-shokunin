# EvidenceRowsR75 — scoped scribe report

## Behavior and axes
Coverage: independently enumerate immediate evidence directories and draft the missing index rows. Calibration: distinguish live-tree observations, frozen-A1 reconstruction, and historical receipts; no replay result is claimed.

## Findings
- The first independent live-tree parser printed `DIRECTORIES 66 MISSING 0`. Thus the requested missing set is already empty in the live README observed by this seat; this does not reproduce the frozen before state. Production changes belong to the integration owner, not this seat.
- Reconstructing only the README at A1 with read-only `git show 43255758:corpus/README.md` (exit 0), against the same disk-enumerated 66 directories, printed `A1_MISSING 20 RECEIPT_MATCH True`. The receipt was used only after computing the independent set. Twenty proposal bullets are supplied, not zero silently substituted for the frozen repair work.
- `round60/openssl-probe-refreeze.txt:15` prints `PREDICATE R59-C1 pass`; its folder is round60. The proposed row explicitly preserves that cross-round identity instead of relabelling the receipt.
- `round29-attempt2/round28-census-after.txt` carries a round28 name and JSON task census (`distinct_task_ids: 812`, lines 1–6), retained inside the round29 attempt2 directory. This is mixed historical content, not evidence that the entire directory belongs to round28.
- `round10-fleet/recompute_r8.py:5` and `recompute_r9.py:5` hard-code `/home/vgpnk/projects/...` (lowercase), unlike the current checkout path. Their algorithms remain inspectable for offline re-derivation; direct current runnability was not asserted.
- Source `gate.md` files retain quotes/digests and locations, not the fetched original bytes. Proposal wording avoids equating those records with recoverable source captures.
- No other name/round conflict was established by the bounded filename, heading and receipt inspection. This is not an exhaustive semantic audit of every retained file.

## Commands and observed outcomes
Frozen claims were read in full before executing any command.

The independent parser ran in the Python eval tool (completed normally; printed results below, not a subprocess exit code):
```python
from pathlib import Path
lane = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
index = (lane/'corpus/README.md').read_text()
dirs = sorted(p for p in (lane/'corpus/evidence').iterdir() if p.is_dir())
missing = [p for p in dirs if f'corpus/evidence/{p.name}/' not in index]
print('DIRECTORIES', len(dirs), 'MISSING', len(missing))
```
Output: `DIRECTORIES 66 MISSING 0`.

A1 reconstruction ran through `subprocess.run(['git','show','43255758:corpus/README.md'], cwd=lane, text=True, capture_output=True)`; rc 0. The same comprehension used that stdout instead of the live README. Output: `A1_MISSING 20 RECEIPT_MATCH True`. Receipt equality compared the computed directory names to lines beginning `MISSING-EVIDENCE ` in `corpus/evidence/round75/c1-before.txt`.

The read-only Bash command `git show 43255758:corpus/README.md` also exited 0. Specialized `read`/`grep` inspected the README style, listed key receipts and historical script interfaces. These tool calls have no shell exit code; relevant printed anchors include `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5` in round27's summary and `PREDICATE R59-C1 pass` in the round60 receipt. These are read historical output, not this seat's execution evidence.

## Gates and boundaries
- R75-C1/R75-C2 counting commands and selftests: not run by this scribe; no landing-tip or stamp-gate verdict claimed.
- No production file edits, git mutations, commits, pushes, installations, service changes, clones or subagent dispatch.
- No scratch directory was created; no seat scratch tree remains to delete.
- Historical replay interfaces were read, never invoked. Proposed runnable interfaces are source-declared, not tested here.

## Touched surfaces and artifacts
Only the two assigned report/proposal paths were written:
- `.ufo/waves/round-75/w1/index-rows-evidence.md` — 20 independently reconstructed A1-missing directory bullets; no duplicate-append recommendation for the already repaired live index.
- `.ufo/waves/round-75/w1/EvidenceRowsR75.md` — this report, including exact file sizes and listing output below.

## Self-evaluation
Accuracy 4/5: headings/receipts and filename inventories ground the rows, but historical instruments were not executed. Completeness 5/5: all 20 baseline-missing directories have a bullet and full immediate listing. Clarity 4/5: live versus A1 is explicit, though detailed inventories lengthen the report. Actionability 5/5: ready-to-use bullets with existing key filenames and duplicate warning. Conciseness 4/5: full `ls -l` evidence is necessarily long. Overall 4.4/5. Improvement priority: integration owner should choose replacements rather than appending duplicates, and preserve the disclosed round/path caveats. Would the user agree: the explicit unrun boundaries are essential to calibration.

## File inventories
Each command below was invoked as `subprocess.run(['ls','-l', absolute_directory], capture_output=True, text=True)` and returned rc 0. Sizes are bytes as printed by `ls -l`; directory sizes describe directory entries, not recursive content size. These are immediate listings as requested, not recursive manifests.

### round10-fleet

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round10-fleet`; rc 0.
```text
total 236
-rw-r--r-- 1 vgpnk vgpnk  3227 Oct 13 16:51 final-harness.log
-rw-r--r-- 1 vgpnk vgpnk  7280 Oct 13 16:51 INTEGRATOR-NOTES.md
-rw-r--r-- 1 vgpnk vgpnk   872 Oct 13 16:51 models-34113.json
-rwxr-xr-x 1 vgpnk vgpnk  8794 Oct 13 16:51 mutate_test.sh
-rwxr-xr-x 1 vgpnk vgpnk  4687 Oct 13 16:51 probe_ref.py
-rw-r--r-- 1 vgpnk vgpnk  8993 Oct 13 16:51 props.json
-rw-r--r-- 1 vgpnk vgpnk 14167 Oct 13 16:51 r10-connector.md
-rw-r--r-- 1 vgpnk vgpnk 25942 Oct 13 16:51 r10-critic.md
-rw-r--r-- 1 vgpnk vgpnk 10731 Oct 13 16:51 r10-drafts.md
-rw-r--r-- 1 vgpnk vgpnk  6223 Oct 13 16:51 r10-labrat-schema.md
-rw-r--r-- 1 vgpnk vgpnk 21870 Oct 13 16:51 r10-mutation-sh.md
-rw-r--r-- 1 vgpnk vgpnk  7637 Oct 13 16:51 r10-report-draft.md
-rw-r--r-- 1 vgpnk vgpnk 12749 Oct 13 16:51 r10-review-cites.md
-rw-r--r-- 1 vgpnk vgpnk 11105 Oct 13 16:51 r10-scout-bench.md
-rw-r--r-- 1 vgpnk vgpnk 10197 Oct 13 16:51 r10-scout-endpoint.md
-rw-r--r-- 1 vgpnk vgpnk 10740 Oct 13 16:51 r10-scout-wiki.md
-rw-r--r-- 1 vgpnk vgpnk  2790 Oct 13 16:51 r10-scribe.md
-rwxr-xr-x 1 vgpnk vgpnk  2340 Oct 13 16:51 recompute_r8.py
-rwxr-xr-x 1 vgpnk vgpnk  4103 Oct 13 16:51 recompute_r9.py
-rwxr-xr-x 1 vgpnk vgpnk 14528 Oct 13 16:51 schema_probe.py
-rw-r--r-- 1 vgpnk vgpnk  2551 Oct 13 16:51 slots.json
-rw-r--r-- 1 vgpnk vgpnk   964 Oct 13 16:51 url-status.txt
```

### round11-fleet

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round11-fleet`; rc 0.
```text
total 312
-rwxr-xr-x 1 vgpnk vgpnk 58908 Oct 13 16:51 grader_r11_draft.py
-rw-r--r-- 1 vgpnk vgpnk  7813 Oct 13 16:51 INTEGRATOR-NOTES.md
-rw-r--r-- 1 vgpnk vgpnk  7495 Oct 13 16:51 mock-results-head.jsonl
-rw-r--r-- 1 vgpnk vgpnk   168 Oct 13 16:51 mock-run.log
-rwxr-xr-x 1 vgpnk vgpnk  4975 Oct 13 16:51 mock_server_r11.py
-rwxr-xr-x 1 vgpnk vgpnk  8092 Oct 13 16:51 mutate_r11.sh
-rw-r--r-- 1 vgpnk vgpnk 14626 Oct 13 16:51 r11-connector.md
-rw-r--r-- 1 vgpnk vgpnk 14536 Oct 13 16:51 r11-critic-design.md
-rw-r--r-- 1 vgpnk vgpnk  5646 Oct 13 16:51 r11-critic-landed.md
-rw-r--r-- 1 vgpnk vgpnk  3129 Oct 13 16:51 r11-log-draft.md
-rw-r--r-- 1 vgpnk vgpnk  8944 Oct 13 16:51 r11-mock-smoke.md
-rw-r--r-- 1 vgpnk vgpnk 11423 Oct 13 16:51 r11-mutation.md
-rw-r--r-- 1 vgpnk vgpnk 23260 Oct 13 16:51 r11-prior-art-granularity.md
-rw-r--r-- 1 vgpnk vgpnk 37839 Oct 13 16:51 r11-prior-art-prereg.md
-rw-r--r-- 1 vgpnk vgpnk 15922 Oct 13 16:51 r11-report-draft.md
-rw-r--r-- 1 vgpnk vgpnk 15331 Oct 13 16:51 r11-review-baseline.md
-rw-r--r-- 1 vgpnk vgpnk  8183 Oct 13 16:51 r11-review-index.md
-rwxr-xr-x 1 vgpnk vgpnk 41284 Oct 13 16:51 recompute_r11_draft.py
```

### round12-fleet

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round12-fleet`; rc 0.
```text
total 868
-rw-r--r-- 1 vgpnk vgpnk 204469 Oct 13 16:51 grader_r12_draft.py
-rw-r--r-- 1 vgpnk vgpnk  10505 Oct 13 16:51 INTEGRATOR-NOTES.md
-rwxr-xr-x 1 vgpnk vgpnk   7274 Oct 13 16:51 mock_server_r12.py
-rw-r--r-- 1 vgpnk vgpnk  21171 Oct 13 16:51 r12-connector.md
-rw-r--r-- 1 vgpnk vgpnk   9507 Oct 13 16:51 r12-critic-design.md
-rw-r--r-- 1 vgpnk vgpnk  28019 Oct 13 16:51 r12-doc-deltas-final.md
-rw-r--r-- 1 vgpnk vgpnk  29021 Oct 13 16:51 r12-doc-deltas.md
-rw-r--r-- 1 vgpnk vgpnk  36047 Oct 13 16:51 r12-endpoint-freshness.md
-rw-r--r-- 1 vgpnk vgpnk  24007 Oct 13 16:51 r12-grader-notes.md
-rw-r--r-- 1 vgpnk vgpnk  11160 Oct 13 16:51 r12-log-draft.md
-rw-r--r-- 1 vgpnk vgpnk  15503 Oct 13 16:51 r12-log-final.md
-rw-r--r-- 1 vgpnk vgpnk   6723 Oct 13 16:51 r12-mock-smoke.md
-rw-r--r-- 1 vgpnk vgpnk   6820 Oct 13 16:51 r12-mutation.md
-rw-r--r-- 1 vgpnk vgpnk  43599 Oct 13 16:51 r12-prior-art-ladder.md
-rw-r--r-- 1 vgpnk vgpnk  58739 Oct 13 16:51 r12-prior-art-transport.md
-rw-r--r-- 1 vgpnk vgpnk  23032 Oct 13 16:51 r12-recompute-notes.md
-rw-r--r-- 1 vgpnk vgpnk  45417 Oct 13 16:51 r12-report-draft.md
-rw-r--r-- 1 vgpnk vgpnk  50058 Oct 13 16:51 r12-report-final.md
-rw-r--r-- 1 vgpnk vgpnk  11681 Oct 13 16:51 r12-review-baseline.md
-rw-r--r-- 1 vgpnk vgpnk  56070 Oct 13 16:51 r12-review-citations.md
-rw-r--r-- 1 vgpnk vgpnk  11438 Oct 13 16:51 r12-scope-audit.md
-rwxr-xr-x 1 vgpnk vgpnk 140671 Oct 13 16:51 recompute_r12_draft.py
```

### round13-coverage

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round13-coverage`; rc 0.
```text
total 120
-rw-r--r-- 1 vgpnk vgpnk  1416 Oct 15 01:53 baseline-initial.json
-rwxr-xr-x 1 vgpnk vgpnk  9256 Oct 15 02:01 coverage_census.py
-rw-r--r-- 1 vgpnk vgpnk  1598 Oct 15 01:53 dispatch.json
-rw-r--r-- 1 vgpnk vgpnk   708 Oct 15 01:57 fleet-timing.json
-rw-r--r-- 1 vgpnk vgpnk  9781 Oct 15 01:57 r13-connector.md
-rw-r--r-- 1 vgpnk vgpnk 13135 Oct 15 01:55 r13-critic.md
-rw-r--r-- 1 vgpnk vgpnk  7794 Oct 15 02:02 r13-knowledge-sources.md
-rw-r--r-- 1 vgpnk vgpnk 15133 Oct 15 01:54 r13-planner.md
-rw-r--r-- 1 vgpnk vgpnk 16605 Oct 15 01:57 r13-scout.md
-rw-r--r-- 1 vgpnk vgpnk 16400 Oct 15 01:58 r13-scribe.md
-rw-r--r-- 1 vgpnk vgpnk  2366 Oct 15 01:49 surface-receipt.json
```

### round24-census

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round24-census`; rc 0.
```text
total 8
-rw-r--r-- 1 vgpnk vgpnk 1413 Oct 19 19:39 after.txt
-rw-r--r-- 1 vgpnk vgpnk  844 Oct 19 19:39 base-99cf615.txt
```

### round24-sources

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round24-sources`; rc 0.
```text
total 12
-rw-r--r-- 1 vgpnk vgpnk 11886 Oct 20 21:56 gate.md
```

### round25-calibration

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round25-calibration`; rc 0.
```text
total 76
-rw-r--r-- 1 vgpnk vgpnk  1899 Oct 20 21:57 attrib-calibration-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk  2408 Oct 20 22:01 attrib-calibration-selftest-v2.txt
-rw-r--r-- 1 vgpnk vgpnk  9043 Oct 20 21:40 attrib-calibration-summary.txt
-rw-r--r-- 1 vgpnk vgpnk 10689 Oct 20 22:01 attrib-calibration-summary-v2.txt
-rw-r--r-- 1 vgpnk vgpnk  6729 Oct 20 21:40 attrib-oracle-intervals.txt
-rw-r--r-- 1 vgpnk vgpnk  1347 Oct 20 21:43 revert-test.txt
-rw-r--r-- 1 vgpnk vgpnk   945 Oct 20 22:01 round25-census-after.txt
-rw-r--r-- 1 vgpnk vgpnk   430 Oct 20 21:43 round25-census-before-6180e4f.txt
-rw-r--r-- 1 vgpnk vgpnk  1728 Oct 20 21:57 state-check-after.txt
-rw-r--r-- 1 vgpnk vgpnk  1728 Oct 20 22:03 state-check-after-v2.txt
-rw-r--r-- 1 vgpnk vgpnk  2806 Oct 20 21:34 state-check-before-6180e4f.txt
-rw-r--r-- 1 vgpnk vgpnk  2900 Oct 20 22:01 state-check-before-6180e4f-v2.txt
-rw-r--r-- 1 vgpnk vgpnk   126 Oct 20 21:50 state-check-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk   178 Oct 20 22:03 state-check-selftest-v2.txt
```

### round25-sources

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round25-sources`; rc 0.
```text
total 8
-rw-r--r-- 1 vgpnk vgpnk 7456 Oct 20 21:56 gate.md
```

### round26-calibration

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round26-calibration`; rc 0.
```text
total 160
-rw-r--r-- 1 vgpnk vgpnk   548 Oct 21 05:51 actual-commit-byte-check.json
-rw-r--r-- 1 vgpnk vgpnk   773 Oct 21 05:51 gate-timing-actual-commit.txt
-rw-r--r-- 1 vgpnk vgpnk   755 Oct 21 05:49 gate-timing-prospective.txt
-rw-r--r-- 1 vgpnk vgpnk  1025 Oct 21 04:32 gate-timing-red-before.txt
-rw-r--r-- 1 vgpnk vgpnk  1253 Oct 21 05:49 gate-timing-red-recovery.txt
-rw-r--r-- 1 vgpnk vgpnk   262 Oct 21 05:49 gate-timing-selftest-final.txt
-rw-r--r-- 1 vgpnk vgpnk  5709 Oct 21 04:52 grader-perturb-build-observation.txt
-rw-r--r-- 1 vgpnk vgpnk  5470 Oct 21 05:49 grader-perturb-final.txt
-rw-r--r-- 1 vgpnk vgpnk  6054 Oct 21 05:49 grader-perturb-selftest-final.txt
-rw-r--r-- 1 vgpnk vgpnk   129 Oct 21 05:49 grader-replay-final.txt
-rw-r--r-- 1 vgpnk vgpnk  1332 Oct 21 05:51 measured-code-sha256.json
-rw-r--r-- 1 vgpnk vgpnk   499 Oct 21 05:50 p2-preservation.txt
-rw-r--r-- 1 vgpnk vgpnk   285 Oct 21 05:50 p3b-new-source-control.txt
-rw-r--r-- 1 vgpnk vgpnk 12069 Oct 21 05:49 p3-oracle-final.txt
-rw-r--r-- 1 vgpnk vgpnk 12919 Oct 21 05:49 p3-oracle-selftest-final.txt
-rw-r--r-- 1 vgpnk vgpnk 12697 Oct 21 05:49 p3-oracle-selftest-repaired.txt
-rw-r--r-- 1 vgpnk vgpnk   158 Oct 21 05:49 perturb-cases-final.txt
-rw-r--r-- 1 vgpnk vgpnk  3033 Oct 21 04:52 perturb-oracle-build-observation.txt
-rw-r--r-- 1 vgpnk vgpnk   412 Oct 21 05:49 perturb-oracle-final.txt
-rw-r--r-- 1 vgpnk vgpnk  2569 Oct 21 05:50 preservation-and-source-census.json
-rw-r--r-- 1 vgpnk vgpnk  1487 Oct 21 05:39 recovery-start.txt
-rw-r--r-- 1 vgpnk vgpnk   750 Oct 21 05:49 revert-test.txt
-rw-r--r-- 1 vgpnk vgpnk   842 Oct 21 05:51 round26-census-after.txt
-rw-r--r-- 1 vgpnk vgpnk  1082 Oct 21 02:31 round-start.txt
-rw-r--r-- 1 vgpnk vgpnk   403 Oct 21 05:51 sources-census-final.txt
-rw-r--r-- 1 vgpnk vgpnk  4031 Oct 21 05:49 state-check-base-f11bffbf.txt
-rw-r--r-- 1 vgpnk vgpnk  4573 Oct 21 05:49 state-check-final.txt
-rw-r--r-- 1 vgpnk vgpnk   827 Oct 21 05:49 state-check-selftest-final.txt
```

### round26-sources

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round26-sources`; rc 0.
```text
total 8
-rw-r--r-- 1 vgpnk vgpnk 4552 Oct 21 04:48 gate.md
```

### round27-calibration

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round27-calibration`; rc 0.
```text
total 1348
-rw-r--r-- 1 vgpnk vgpnk   1134 Oct 21 10:35 actual-admission-byte-proof.json
-rw-r--r-- 1 vgpnk vgpnk    783 Oct 21 10:36 census-selector-green.txt
-rw-r--r-- 1 vgpnk vgpnk    452 Oct 21 10:36 census-selector-red.txt
-rw-r--r-- 1 vgpnk vgpnk 474197 Oct 21 10:33 final-suite.json
-rw-r--r-- 1 vgpnk vgpnk    593 Oct 21 10:37 fleet-misroot-final.txt
-rw-r--r-- 1 vgpnk vgpnk    678 Oct 21 10:35 gate-actual-admission.txt
-rw-r--r-- 1 vgpnk vgpnk   3751 Oct 21 10:33 gate-final-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk    617 Oct 21 10:34 gate-prospective.txt
-rw-r--r-- 1 vgpnk vgpnk    129 Oct 21 10:33 grader-final.txt
-rw-r--r-- 1 vgpnk vgpnk   1979 Oct 21 10:33 independent-policy-final.txt
-rw-r--r-- 1 vgpnk vgpnk    985 Oct 21 10:33 p23-final-preservation.txt
-rw-r--r-- 1 vgpnk vgpnk   1347 Oct 21 10:33 p4-final-mutants.txt
-rw-r--r-- 1 vgpnk vgpnk    551 Oct 21 09:07 policy-build-oracle.txt
-rw-r--r-- 1 vgpnk vgpnk   3894 Oct 21 09:07 policy-build-summary.txt
-rw-r--r-- 1 vgpnk vgpnk  44803 Oct 21 10:33 policy-final-json.json
-rw-r--r-- 1 vgpnk vgpnk    551 Oct 21 10:33 policy-final-oracle.txt
-rw-r--r-- 1 vgpnk vgpnk   1350 Oct 21 10:33 policy-final-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk   3894 Oct 21 10:33 policy-final-summary.txt
-rw-r--r-- 1 vgpnk vgpnk    210 Oct 21 10:33 policy-missing-root.txt
-rw-r--r-- 1 vgpnk vgpnk    255 Oct 21 10:33 policy-usage.txt
-rw-r--r-- 1 vgpnk vgpnk   2416 Oct 21 10:34 preservation-final.json
-rw-r--r-- 1 vgpnk vgpnk    716 Oct 21 10:35 round27-census-after.txt
-rw-r--r-- 1 vgpnk vgpnk    777 Oct 21 10:37 round27-census-final.txt
-rw-r--r-- 1 vgpnk vgpnk   9141 Oct 21 10:37 round-owned-paths.txt
-rw-r--r-- 1 vgpnk vgpnk   2094 Oct 21 08:35 round-start.txt
-rw-r--r-- 1 vgpnk vgpnk    490 Oct 21 10:34 separability-final.json
-rw-r--r-- 1 vgpnk vgpnk    656 Oct 21 10:35 sources-census-after-admission.txt
-rw-r--r-- 1 vgpnk vgpnk    656 Oct 21 10:33 sources-census-final.txt
-rw-r--r-- 1 vgpnk vgpnk 182884 Oct 21 10:33 state-base-final-json.json
-rw-r--r-- 1 vgpnk vgpnk 184741 Oct 21 10:33 state-final-json.json
-rw-r--r-- 1 vgpnk vgpnk   2038 Oct 21 10:33 state-final-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk    204 Oct 21 10:33 state-missing-root.txt
-rw-r--r-- 1 vgpnk vgpnk    193 Oct 21 10:33 state-usage.txt
-rw-r--r-- 1 vgpnk vgpnk 173942 Oct 21 09:25 state-v4-base.json
-rw-r--r-- 1 vgpnk vgpnk    288 Oct 21 09:25 state-v4-base.txt
-rw-r--r-- 1 vgpnk vgpnk 175179 Oct 21 09:25 state-v4-build.json
-rw-r--r-- 1 vgpnk vgpnk    307 Oct 21 09:25 state-v4-build.txt
```

### round27-sources

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round27-sources`; rc 0.
```text
total 8
-rw-r--r-- 1 vgpnk vgpnk 6593 Oct 21 10:21 gate.md
```

### round28-calibration

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round28-calibration`; rc 0.
```text
total 472
-rw-r--r-- 1 vgpnk vgpnk   1479 Oct 21 12:34 actual-admission-byte-proof.json
-rw-r--r-- 1 vgpnk vgpnk   3130 Oct 21 12:40 actual-census-corrected.txt
-rw-r--r-- 1 vgpnk vgpnk   3172 Oct 21 12:34 actual-census.txt
-rw-r--r-- 1 vgpnk vgpnk   1575 Oct 21 12:40 actual-final-byte-proof.json
-rw-r--r-- 1 vgpnk vgpnk    668 Oct 21 12:40 actual-gate-corrected.txt
-rw-r--r-- 1 vgpnk vgpnk   1538 Oct 21 12:34 actual-gate.txt
-rw-r--r-- 1 vgpnk vgpnk 185511 Oct 21 12:35 actual-state-diagnostic.json
-rw-r--r-- 1 vgpnk vgpnk   1513 Oct 21 12:06 audit-summary-final.txt
-rw-r--r-- 1 vgpnk vgpnk   1275 Oct 21 11:24 audit-summary.txt
-rw-r--r-- 1 vgpnk vgpnk   2146 Oct 21 10:57 before.txt
drwxr-xr-x 1 vgpnk vgpnk   1206 Oct 21 11:23 build-acceptance
-rw-r--r-- 1 vgpnk vgpnk    492 Oct 21 11:23 build-acceptance-run.txt
-rw-r--r-- 1 vgpnk vgpnk    531 Oct 21 11:23 build-preservation-corrected.json
-rw-r--r-- 1 vgpnk vgpnk    767 Oct 21 11:23 build-preservation-delta.json
drwxr-xr-x 1 vgpnk vgpnk   1290 Oct 21 12:41 complete-acceptance
-rw-r--r-- 1 vgpnk vgpnk   1089 Oct 21 12:41 complete-acceptance-run.txt
drwxr-xr-x 1 vgpnk vgpnk   1290 Oct 21 11:58 final-acceptance
-rw-r--r-- 1 vgpnk vgpnk    996 Oct 21 11:58 final-acceptance-run.txt
-rw-r--r-- 1 vgpnk vgpnk    294 Oct 21 12:33 forecasts.json
-rw-r--r-- 1 vgpnk vgpnk 185615 Oct 21 12:38 historical-scope-restored.txt
-rw-r--r-- 1 vgpnk vgpnk   2066 Oct 21 12:38 historical-scope-selftest-green.txt
-rw-r--r-- 1 vgpnk vgpnk   1841 Oct 21 12:37 historical-scope-selftest-red.txt
-rw-r--r-- 1 vgpnk vgpnk    725 Oct 21 11:29 inherited-inputs.txt
-rw-r--r-- 1 vgpnk vgpnk    330 Oct 21 12:23 misroot-sweep.txt
-rw-r--r-- 1 vgpnk vgpnk   2121 Oct 21 11:38 prior-art-reopen.txt
-rw-r--r-- 1 vgpnk vgpnk    238 Oct 21 12:06 registry-summary-final.txt
-rw-r--r-- 1 vgpnk vgpnk    238 Oct 21 11:24 registry-summary.txt
-rw-r--r-- 1 vgpnk vgpnk    936 Oct 21 12:04 source-correction-quotes.json
-rw-r--r-- 1 vgpnk vgpnk    785 Oct 21 12:09 source-inventory-after.json
-rw-r--r-- 1 vgpnk vgpnk    828 Oct 21 12:09 source-inventory-before.json
-rw-r--r-- 1 vgpnk vgpnk   1293 Oct 21 12:34 sources-census-final.txt
```

### round29-attempt2

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round29-attempt2`; rc 0.
```text
total 56
-rw-r--r-- 1 vgpnk vgpnk 5543 Oct 25 03:51 adopted-block.md
-rw-r--r-- 1 vgpnk vgpnk  118 Oct 25 03:46 adoption-gate-run.txt
-rw-r--r-- 1 vgpnk vgpnk   83 Oct 25 04:00 adoption-measured.txt
-rw-r--r-- 1 vgpnk vgpnk 1416 Oct 25 03:53 census-after.txt
-rw-r--r-- 1 vgpnk vgpnk 1416 Oct 25 03:46 census-before.txt
-rw-r--r-- 1 vgpnk vgpnk   88 Oct 25 03:53 control-nocensus.txt
-rw-r--r-- 1 vgpnk vgpnk 1312 Oct 25 04:44 control-nothing.txt
-rw-r--r-- 1 vgpnk vgpnk 6166 Oct 25 04:00 gate-scoped.txt
-rw-r--r-- 1 vgpnk vgpnk  337 Oct 25 04:00 gate-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk 5019 Oct 25 04:00 gate-strict.txt
-rw-r--r-- 1 vgpnk vgpnk 3036 Oct 25 03:53 round28-census-after.txt
```

### round29-calibration

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round29-calibration`; rc 0.
```text
total 132
-rw-r--r-- 1 vgpnk vgpnk 1820 Oct 21 15:15 actual-byte-proof.json
-rw-r--r-- 1 vgpnk vgpnk 3036 Oct 21 15:15 actual-census.json
-rw-r--r-- 1 vgpnk vgpnk  489 Oct 21 15:15 actual-gate.txt
-rw-r--r-- 1 vgpnk vgpnk   68 Oct 21 13:38 build-json-sha256.txt
-rw-r--r-- 1 vgpnk vgpnk  606 Oct 21 13:38 build-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk 6921 Oct 21 13:38 build-summary.txt
-rw-r--r-- 1 vgpnk vgpnk  649 Oct 21 15:10 credential-copy-removal.txt
-rw-r--r-- 1 vgpnk vgpnk 5925 Oct 21 15:06 final-mutation-witness.json
-rw-r--r-- 1 vgpnk vgpnk 1501 Oct 21 15:07 final-oracle.txt
-rw-r--r-- 1 vgpnk vgpnk  889 Oct 21 15:06 final-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk 8325 Oct 21 15:04 final-summary.txt
-rw-r--r-- 1 vgpnk vgpnk  198 Oct 21 12:56 instrument-before.txt
-rw-r--r-- 1 vgpnk vgpnk   48 Oct 21 15:15 landing-helper.txt
-rw-r--r-- 1 vgpnk vgpnk  460 Oct 21 13:38 mutation-witness.txt
-rw-r--r-- 1 vgpnk vgpnk 1095 Oct 21 15:12 receipt-generations.json
-rw-r--r-- 1 vgpnk vgpnk  809 Oct 21 14:25 repair-cross-python.txt
-rw-r--r-- 1 vgpnk vgpnk   68 Oct 21 14:24 repair-json-sha256.txt
-rw-r--r-- 1 vgpnk vgpnk 5131 Oct 21 14:24 repair-mutation-witness.json
-rw-r--r-- 1 vgpnk vgpnk 1836 Oct 21 14:24 repair-optimized-refused.txt
-rw-r--r-- 1 vgpnk vgpnk  595 Oct 21 14:25 repair-projection-equality.json
-rw-r--r-- 1 vgpnk vgpnk  801 Oct 21 14:24 repair-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk 8075 Oct 21 14:24 repair-summary.txt
-rw-r--r-- 1 vgpnk vgpnk 1423 Oct 21 15:11 sources-after.txt
-rw-r--r-- 1 vgpnk vgpnk 1181 Oct 21 12:56 sources-before.txt
-rw-r--r-- 1 vgpnk vgpnk 1784 Oct 21 15:16 trial-byte-proof.json
-rw-r--r-- 1 vgpnk vgpnk  453 Oct 21 15:16 trial-gate.txt
-rw-r--r-- 1 vgpnk vgpnk  393 Oct 21 15:16 trial-landed-tree-proof.json
```

### round34

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round34`; rc 0.
```text
total 8
-rw-r--r-- 1 vgpnk vgpnk 1505 Oct 25 16:11 census-after.txt
-rw-r--r-- 1 vgpnk vgpnk 1505 Oct 25 16:11 census-before.txt
```

### round53

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round53`; rc 0.
```text
total 248
-rw-r--r-- 1 vgpnk vgpnk  10652 Oct 30 01:41 confirmations.json
drwxr-xr-x 1 vgpnk vgpnk   5926 Oct 30 02:47 fetched
-rw-r--r-- 1 vgpnk vgpnk 139342 Oct 28 21:30 pin-tree-2fd12b88.json
-rw-r--r-- 1 vgpnk vgpnk  17805 Oct 30 02:47 prior-art.json
-rw-r--r-- 1 vgpnk vgpnk  76598 Oct 28 21:30 tests-index.json
```

### round54

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round54`; rc 0.
```text
total 8
drwxr-xr-x 1 vgpnk vgpnk   42 Oct 30 08:47 anchor
-rw-r--r-- 1 vgpnk vgpnk  473 Oct 30 07:48 c1-before.txt
-rw-r--r-- 1 vgpnk vgpnk 2435 Oct 30 07:48 c2-before-dry.txt
```

### round60

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round60`; rc 0.
```text
total 4
drwxr-xr-x 1 vgpnk vgpnk  18 Nov  3 14:51 grep-manual
-rw-r--r-- 1 vgpnk vgpnk 856 Nov  3 14:51 openssl-probe-refreeze.txt
```

### round75

Command: `ls -l /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round75`; rc 0.
```text
total 32
-rw-r--r-- 1 vgpnk vgpnk 2611 Nov  4 01:25 c1-before.txt
-rw-r--r-- 1 vgpnk vgpnk  391 Nov  4 01:25 c1-control-rowshuffle.txt
-rw-r--r-- 1 vgpnk vgpnk  300 Nov  4 01:25 c1-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk  350 Nov  4 01:25 c2-audit-mutants.txt
-rw-r--r-- 1 vgpnk vgpnk  283 Nov  4 01:25 c2-control-attribute.txt
-rw-r--r-- 1 vgpnk vgpnk  344 Nov  4 01:25 c2-selftest.txt
-rw-r--r-- 1 vgpnk vgpnk  742 Nov  4 01:25 c2-stamp-red-before.txt
-rw-r--r-- 1 vgpnk vgpnk 3362 Nov  4 01:25 census-before.txt
drwxr-xr-x 1 vgpnk vgpnk   82 Nov  4 01:23 sources
```
