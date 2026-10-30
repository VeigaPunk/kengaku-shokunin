# C1PriceScoutE — R53-C1 prior-art pricing

Axes: novelty and coverage. Read facts first, then all frozen claims including A1–A3 and `leg_prior_art`/`names_task`. No label files, classifier output, or wave-2 reader files were opened. GitHub search result metadata incidentally exposed their filenames; no result contents were fetched. No tools installed or updated.

## Result

Four `phenomenon-known` rows, zero new, zero unclear. All four use one shared public primary, Jonathan Gabor's January 2026 Terminal-Bench 2 audit. Therefore this part contributes **one distinct URL**, not four; it does not independently satisfy the merged predicate's three-URL/one-new thresholds.

The observed archive explicitly names each assigned test and describes its existence check. This supports knownness of the **individual presence-only test**, not a claim that the full task grader accepts an empty artefact. The same audit rates all four tasks 4 and describes substantive companion checks. No end-to-end empty-artefact bypass is claimed or executed here. If integration interprets “weakness” as full-suite vacuity rather than the confirmed per-test property, these rows require semantic reconsideration; mechanical quote validity alone does not establish that stronger claim.

| task | named evidence in primary | quote words |
|---|---|---:|
| llm-inference-batching-scheduler | `test_output_files_exist`: both plan files merely exist | 11 |
| path-tracing | `test_image_c_exists`: basic file existence check | 9 |
| sam-cell-seg | `test_python_file_exists`: script existence; adjacent item also names `test_csv_output_exists` | 9 |
| winning-avg-corewars | `test_warrior_exists`: solution file creation | 10 |

Exact verbatim quotes are in `prior-art-part.json`. Local whitespace-normalisation/membership/name-boundary checks observed `in_archive=True`, `names_task=True` for all four. This was a small Python transcription of the relevant helpers, **not** an execution of the frozen counter or a full predicate receipt.

Primary archive SHA256: `3c550d8dc0bfd3e2a8c07425fd00448cd55fe329fe18c261e21984dd77d63d5d`.

## Broader observed finding

The audit has 88 unique `Challenge:` entries against the 89-task population; only `make-doom-for-mips` is absent. Comparison with the integrated confirmations task/name fields found all 20 task IDs and 13 of their confirmed test names in the archive. This is **not** a verdict on the other 16 tasks: mere name occurrence does not establish their specific weakness, and other seats own their pricing.

The README describes an LLM coverage auditor that consumes task descriptions, filesystem information, tests and reference solutions and assigns 1–5 ratings. Repository commit metadata observed January 23–24, 2026. This is additional instrument-family prior art, not evidence of an AST classifier or blind-label oracle. ABA's separately fetched paper does not reference Gabor by the searched strings; their identity or relationship was not established.

## Search coverage and rejected candidates

Tracker task searches observed, respectively (batching/path/sam/corewars): TB2 **0/2/3/1**; TB2.1 **0/27/2/7**; TB1 **1/9/0/3**. Exact global issue searches for the four task/test pairs returned zero each. Exact global test-name issue searches returned zero for image, warrior, Python and CSV names; the generic output-files name returned 17 mostly unrelated hits. Code search was discovery only; lane-derived hits and run-result listings were not treated as independent semantic evidence.

Rejected or supplemental candidates:
- TB2 #61 and TB2.1 #229: renderer/reference binary disclosure, not the named existence-only property.
- TB1 #1109 and PR #1192: reference-linking shortcut and hardening, a different grading weakness; #1109 body has neither task ID nor test name.
- TB2 #45, ABA's sam-cell-seg row, and fork issue #4: argument-form mismatch, not existence-only weakness.
- TB2 #17 / TB1 #1361: safety terminology, not grading vacuity.
- Tinker cookbook #889: binary fixture upload failure causing zero reward, not presence-only passing. #890 was discovered as its follow-up, not relied on.
- TB2 PR #53: umbrella “let any solution pass” language; sam-cell-seg patch changes coordinate-format validation, not these presence-only tests.
- TB1 PR #792 and RyanMarten PR #17: task contribution/import, not a weakness report.
- TB main PR #1202: CoreWars conversion and actual performance thresholds, no existence-only finding.
- Marginlab task explorers: source mirrors. Preserved as corroboration but **not promoted to third-party weakness reports or used to inflate URL diversity**.
- Harbor Hub task pages: document substantive companion checks, not task-level existence-only grading.
- Antigma blog: copied solution trajectories/benchmark contamination, not this existence-only property.
- Hack-Verifiable TB paper: assigned task IDs occur in a difficulty/population table, not a task-specific existence-only finding.
- Kim June audit: frame preservation/deletion blindness, not existence-only grading; relevant records include meaningful caught mutations as well as frame-blind cases.
- Terminal-Wrench: public index reports CoreWars exploit trajectories, but a task-level count alone does not establish the presence-only mechanism. No exploit was reproduced or developed.
- OpenReview attachment/forum returned browser verification HTML rather than the paper; rejected as unavailable paper evidence.
- Zai verified dataset GitHub route returned 404; HF dataset search was only discovery.
- Generic verifier-hardening, ABC, BenchGuard, protocol-validity, Scale and June Kim pages are class-level leads, not task-specific knownness evidence. No new verdict is inferred from empty searches alone.

Two zero-hit batching task searches were archived. Three other archived files named `sweep-tb2-*-task.json` returned task-naming hits (2/3/1); despite their filenames they are **unusable as new-row sweeps**. No sweep field appears in any submitted known row.

## Commands and provenance

Clone run and terminal lane HEAD: `9ead4476bf55b1ea6490d0204b668195db4a4d1d` (same observed at both checks).

Commands actually used (task loops expanded over the four assigned IDs):
- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`; `df -h /fast/scratch`: observed 464G available, 43% used. No ENOSPC.
- `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/C1PriceScoutE/lane`; then `git -C .../lane rev-parse --show-toplevel` printed the exact scratch clone path; `git -C .../lane rev-parse HEAD` printed the revision above.
- `gh api "search/issues?q=repo:<repo>+<task>" --jq '.total_count, (.items[]? | ...)'` for TB2, TB2.1 and TB1; global task searches, exact quoted test-name searches, task+test pair searches, task+audit searches, and `type:pr in:title` scoped searches.
- `gh api "search/code?q=<test>" --jq '.total_count, (.items[]? | ...)'`; task+test searches with `extension:md`.
- `gh api "repos/<repo>/issues?state=all&per_page=100" --paginate --jq '.[] | select(.pull_request==null) | ...'`; issue bodies inspected for relevant tasks. TB main and historical TB1 are distinct endpoints and were not conflated.
- `gh api repos/<repo>/issues/<n> --jq '.title,.body'`; corresponding pulls/files and contents/tree endpoints for discovery.
- `curl -sL --compressed <url> -o <scratch-file>`; archive helper prepended `SOURCE-URL: <url>` and retained fetched body bytes. `gh api` was used for search response bodies without exposing authentication material.
- Python `json`, `re`, `hashlib` checks counted audit sections, compared task/test tokens, checked quote membership/boundaries and generated the four-row part and digest inventory.

Earlier shell inspection used head/tail/sed/grep/cat despite specialized-tool preference. A credential-masked auth status was displayed. The L1 sentinel subsequently flagged analytics strings in a supplemental Substack archive; that archive was deleted, is not referenced by any row, and its checksum was removed. Initial narrow credential-pattern inspection was insufficient; no clean bill of health is claimed. A GitHub 404 for inaccessible repositories, OpenReview challenge pages, and local wrong-directory/header-prefixed-JSON parsing failures were not interpreted as absence of public prior art.

No LSP endpoint was available in this session; source searches were literal navigation, not semantic reference proof. The assignment concerns archived evidence, not an exported code-contract change. No counter, tests, grader touch-run or attack was executed. No lane changes outside the assigned seat/report paths, no commit, and no integration were performed.

## Deliverables and integration

All files are below the seat directory (absolute root listed here):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutE/`
- `prior-art-part.json`: four known rows.
- `COPY-MAP.txt`: one required byte-for-byte copy into the counter's fetched directory. JSON fetched paths are intended integration targets; this seat did not write them.
- `fetched/SHA256SUMS`: digests of every retained archive. Supplemental files need not be integrated.
- `fetched/tb2audit-20260120-audit.txt`: sole primary used by the four rows.
- Remaining `fetched/` files: corroboration/rejected candidates/negative search receipts, enumerated below.

The L1 should copy the one primary byte-for-byte, merge exactly one row per task, and run the frozen counter only after merging all seat parts. This part alone cannot pass the population-wide PRIOR-ART predicate (four of twenty tasks, one URL, no new).

## Archived URL inventory

- `antigma-tb-forensic.html` — https://antigma.ai/blog/2026/03/13/terminal-bench
- `arxiv-2507.02825-abs.html` — https://arxiv.org/abs/2507.02825
- `arxiv-2604.24955-abs.html` — https://arxiv.org/abs/2604.24955
- `arxiv-2605.26079-abs.html` — https://arxiv.org/abs/2605.26079
- `arxiv-2608.22103-abs.html` — https://arxiv.org/abs/2608.22103
- `arxiv-2610.15924-abs.html` — https://arxiv.org/abs/2610.15924
- `audit-challenges-llm-inference-batching-scheduler-eval.yaml` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/challenges/llm-inference-batching-scheduler/eval.yaml
- `audit-challenges-path-tracing-eval.yaml` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/challenges/path-tracing/eval.yaml
- `audit-challenges-sam-cell-seg-eval.yaml` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/challenges/sam-cell-seg/eval.yaml
- `audit-challenges-winning-avg-corewars-eval.yaml` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/challenges/winning-avg-corewars/eval.yaml
- `ekellbuch-tb21-issue4.json` — https://api.github.com/repos/ekellbuch/terminal-bench-2/issues/4
- `marginlab-llm-inference-batching-scheduler_.html` — https://marginlab.ai/explorers/terminal-bench/llm-inference-batching-scheduler/
- `marginlab-path-tracing-reverse.html` — https://marginlab.ai/explorers/terminal-bench/path-tracing-reverse/
- `marginlab-path-tracing.html` — https://marginlab.ai/explorers/terminal-bench/path-tracing/
- `marginlab-sam-cell-seg_.html` — https://marginlab.ai/explorers/terminal-bench/sam-cell-seg/
- `marginlab-winning-avg-corewars_.html` — https://marginlab.ai/explorers/terminal-bench/winning-avg-corewars/
- `sweep-tb2-corewars-task.json` — https://api.github.com/search/issues?q=repo%3Aharbor-framework/terminal-bench-2%20winning-avg-corewars
- `sweep-tb2-libs-task.json` — https://api.github.com/search/issues?q=repo%3Aharbor-framework/terminal-bench-2%20llm-inference-batching-scheduler
- `sweep-tb2-path-tracing-task.json` — https://api.github.com/search/issues?q=repo%3Aharbor-framework/terminal-bench-2%20path-tracing
- `sweep-tb2-sam-cell-seg-task.json` — https://api.github.com/search/issues?q=repo%3Aharbor-framework/terminal-bench-2%20sam-cell-seg
- `sweep-tb21-libs-task.json` — https://api.github.com/search/issues?q=repo%3Aharbor-framework/terminal-bench-2-1%20llm-inference-batching-scheduler
- `tb2-pr53.json` — https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53
- `tb2audit-20260120-audit.txt` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/audit_results/20260120_125158/audit.txt
- `tb2audit-harden_tests.py` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/harden_tests.py
- `tb2audit-human-notes.txt` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/audit_results/20260120_125158/human-notes.txt
- `tb2audit-ratings.json` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/audit_results/20260120_125158/ratings.json
- `tb2audit-readme.md` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/README.md
- `tb2audit-stats.json` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/audit_results/20260120_125158/stats.json
- Rejected and removed: https://jonathanpgabor.substack.com/p/every-benchmark-is-broken — sentinel-flagged analytics strings; not retained or used.
- `tb2audit-terminalbench.md` — https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/TERMINALBENCH.md
