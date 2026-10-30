# C1PriceScoutC — candidate inventory (URLs opened, rejections)

Seat: wave-3 scout for R53-C1's PRIOR-ART leg, four confirmed tasks
(`fix-code-vulnerability`, `modernize-scientific-stack`, `pytorch-model-cli`, `torch-tensor-parallelism`).
Lane HEAD used: `9ead4476bf55b1ea6490d0204b668195db4a4d1d` (the lane had advanced past the dispatched
tip `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` while this seat ran).

## A. URLs archived (fetched bytes verbatim, `SOURCE-URL:` first line, in `fetched/`)

| archive file | URL | role |
|---|---|---|
| `arxiv-2503.15223-abs.html` | https://arxiv.org/abs/2503.15223 | row primary — `pytorch-model-cli` (general primary on weak verifier checks; already lane source S188) |
| `arxiv-2511.21654-abs.html` | https://arxiv.org/abs/2511.21654 | row primary — `torch-tensor-parallelism` (EvilGenie, reward hacking of graders) |
| `arxiv-2507.02825-abs.html` | https://arxiv.org/abs/2507.02825 | spare general primary (ABC checklist; names none of the four tasks) |
| `ghapi-pulls-53.json` | https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53 | row primary — `fix-code-vulnerability` (maintainers' own "tests … let any solution pass" class; already lane source S184) |
| `ghapi-issues-242.json` | https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/242 | row primary — `modernize-scientific-stack` (names the task **and** `test_dependency_file_exists`) |
| `sweep-fcv-tb21-onlychecked.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22fix-code-vulnerability%22+%22only+checked+to+exist%22 | sweep (0 hits) |
| `sweep-fcv-tb2-existence.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2+%22fix-code-vulnerability%22+existence | sweep (0 hits) |
| `sweep-fcv-tb1-onlychecked.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-1+%22fix-code-vulnerability%22+%22only+checked+to+exist%22 | sweep (0 hits) |
| `sweep-fcv-tb21-testname.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22test_report_file_exists_example%22 | sweep (0 hits) |
| `sweep-fcv-global-testname.json` | https://api.github.com/search/issues?q=%22test_vul_file%22 | sweep (0 hits) |
| `sweep-pmc-tb21-onlychecked.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22pytorch-model-cli%22+%22only+checked+to+exist%22 | sweep (0 hits) |
| `sweep-pmc-tb2-existence.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2+%22pytorch-model-cli%22+existence | sweep (0 hits) |
| `sweep-pmc-tb1-onlychecked.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-1+%22pytorch-model-cli%22+%22only+checked+to+exist%22 | sweep (0 hits) |
| `sweep-pmc-global-testname.json` | https://api.github.com/search/issues?q=%22test_weights_file_exists%22 | sweep (0 hits) |
| `sweep-ttp-tb21-onlychecked.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22torch-tensor-parallelism%22+%22only+checked+to+exist%22 | sweep (0 hits) |
| `sweep-ttp-tb2-existence.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2+%22torch-tensor-parallelism%22+existence | sweep (0 hits) |
| `sweep-ttp-tb1-onlychecked.json` | https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-1+%22torch-tensor-parallelism%22+%22only+checked+to+exist%22 | sweep (0 hits) |
| `sweep-ttp-global-testname.json` | https://api.github.com/search/issues?q=%22test_parallel_linear_exists%22 | sweep (0 hits) |

## B. URLs opened for evidence but NOT archived as a row (with the reason)

| URL | why not a row archive |
|---|---|
| https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/134 | names the task; documents oracle leakage in the image (task packaging), not an existence-only grader weakness |
| https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/50 | names the task; adds a missing assertion (`_hval` not just `_hkey`) — a coverage gap, not existence-only |
| https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/156 | names the task; documents a README/instruction **language** mismatch (a Python-backed `cli_tool` passes). Closest public item for `pytorch-model-cli`; states the prediction content **is** checked, so it is not the artefact-existence weakness |
| https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/6 | instruction clarity (image preprocessing) |
| https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/80 | verifier installs the CUDA torch build (dependency size), not a grader weakness |
| https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/81 | verifier hang (`mp.spawn(join=True)`), not a grader weakness |
| https://api.github.com/repos/harbor-framework/terminal-bench/issues/631 | per-task audit of PR #53; names `torch-tensor-parallelism` (row T24: instruction clarification + memory), no existence-only weakness; unusable as a general primary for the `torch-tensor-parallelism` row (names the task) |
| https://api.github.com/repos/harbor-framework/terminal-bench/issues/2173 | the same report as tb2-1 #242, moved to the legacy tracker; corroborating copy only (the row uses the canonical tb2-1 #242) |
| https://api.github.com/repos/harbor-framework/terminal-bench/pulls/2464 | the **fix** PR for #2173; its sentence names neither the task id nor a test name, so it cannot satisfy the known-row quote rule; used as corroboration that the weakness was public |
| https://api.github.com/repos/fugue-labs/gollem/issues/23 | names `torch-tensor-parallelism` **and** its test `test_row_parallel_linear`, but describes agent-side verification fidelity (local checks green, hidden verifier red) — the opposite of an existence-only weakness; also unusable as a sweep for that task |
| https://huggingface.co/datasets/zai-org/terminal-bench-2-verified/raw/main/README.md | zai-org TB2.0 Verified dataset card: names `pytorch-model-cli` (instruction fix: image preprocessing) and `torch-tensor-parallelism` (instruction clarification); its grader-defect list names four *other* tasks (dna-insert, make-doom-for-mips, filter-js-from-html, install-windows-3.11) |
| https://api.github.com/repos/benchflow-ai/skillsbench/pulls/83 | the only public hit for the string `test_report_file_exists_example`: a task-addition PR for a different benchmark's task (`10-k-extraction`) that shares the test name by coincidence; documents no weakness; its body names the test name, so it is unusable as a sweep for `fix-code-vulnerability` |
| https://raw.githubusercontent.com/zch-bytedance/xai_benchmark/main/root_cause/pytorch-model-cli.txt | agent-failure analysis (compilation errors); not grader-weakness documentation |
| https://raw.githubusercontent.com/zch-bytedance/xai_benchmark/main/root_cause/pytorch-model-cli.hard.txt | same |
| https://api.github.com/repos/RyanMarten/terminal-bench-3/pulls/{25,41,59} | "Add `<task>` task" ports with empty bodies; no weakness documented |
| https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/7 | pytest-traceback source leak in verifier logs; a different weakness |
| https://export.arxiv.org/api/query?id_list={2503.15223,2507.02825,2511.21654,2504.20879,2506.12286,2511.21654,2608.00794,2610.02563} | metadata reads only (abstract triage); the archived primaries are the `arxiv.org/abs/` pages so that every row URL is distinct after the counter's `url_key` normalisation (all `export.arxiv.org/api/query` URLs collapse to one key) |
