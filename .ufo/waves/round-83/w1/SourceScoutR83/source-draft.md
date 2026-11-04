## Proposed S267 row (append only; L1 installs)

| S267 | Terminal-Bench 2.0 code-from-image pinned grader — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py | code | A | this pinned grader's two independent test functions over /app/output.txt, for offline member replay only; not image understanding, model execution, or task solving | test_outputs.py:10-31; :25 quote `assert output.strip().startswith("bee26a"), (` (3 whitespace-split words); accessed 2026-11-04; live 935 B SHA256 b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a equals BASE capture | test_output_file_exists asserts presence at :15; test_output_is_correct opens at :23, checks stripped case-sensitive prefix at :25 and exact equality at :28-31; empty content passes only the first leg; matching output bytes do not prove image-derived implementation | mined | 2026-11-04 | 2027-01-18 | corpus/knowledge/tb2-code-from-image-offline.md, corpus/lessons/round-83.md |

## Proposed Gate subsection (full subsection bytes; L1 installs)

### S267 — admitted pinned grader, bounded offline scope

URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py

Access date: 2026-11-04; HTTP 200. Located quote at line 25: `assert output.strip().startswith("bee26a"), (` (3 whitespace-split words, <=25). Tier A for the code's own predicates, not broader task-performance claims. Live bytes: 935 B; SHA256 `b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a`, byte-identical to the round52 capture at BASE `614f00559c75155ec100e945b3e8257b14fb7496` and freeze `6f076679931367d540c3897a4eafa0eca752e1d4`.

The bounded data-walk admits replay of one previously unexecuted member, not a new grader class. Source definitions are `test_output_file_exists` (:10; assert :15) and `test_output_is_correct` (:18; open :23; prefix assert :25; equality assert :28-31). Static vectors in frozen case order are F/F, P/F, P/P, P/P, P/F, P/F, P/F, P/F. This source walk is not a replay receipt and does not score either claim.

### Rejected candidate — instruction as proof of image solving

URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/instruction.md

Access date: 2026-11-04; HTTP 200. Located quote at line 1: “Write the result to `/app/output.txt`.” (5 whitespace-split words, <=25). SHA256 `8c3af6483e409defef9786da51f318ae2ca71afe2327b94471d2f0e2e367442c` (321 B).

REJECTED for the proposed scope “offline replay proves the image was understood or its pseudocode implemented”: the instruction states the task but supplies no execution or model trace, while the grader observes only final output bytes. It remains primary task-spec context, not evidence of solving. Flip: obtain a separately scoped, located run that actually consumes the pinned image, implements its intended logic and records execution to the output, with an appropriate frozen evaluation contract. That is outside round83 and is not required for C1. No new source id is allocated to this rejected scope candidate.

Search bound: two pinned files opened from the existing S105–S113 raw-source domain and repository convention. One grader scope admitted, one instruction-as-solving-proof scope rejected; no global novelty or source-absence claim. No assimilation; proposal2, sweep-divergence and anchor-blindspot backlog remain outside this wave.
