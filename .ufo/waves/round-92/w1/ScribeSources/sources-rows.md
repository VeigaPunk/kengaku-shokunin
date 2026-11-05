# ScribeSources — round-92 SOURCES registry rows S283–S289 (draft, leaf seat)

Draft only. The L1 integrates. The lane was not written by this seat; nothing was committed,
staged, pushed or reset in `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

**Provenance.** Every quote below was located in the lane's own tracked capture under
`corpus/evidence/`, and every capture was re-fetched live from the pinned upstream revision
`2fd12b88aafdd04a52c298e3940bcb189f9766d6` on 2026-11-05 (HTTP 200 for all seven). The
re-fetched bytes are byte-identical to the lane captures (sha256 values below). The word count
in each `(N words)` cell is the whitespace-token count of the quoted bytes
(`len(quote.split())`, the `wc -w` convention `plans/anchor_line_check.py` enforces).

**Word counts — a correction to the seat brief, with the red witness.** The brief gave
S283 as `(5 words)` and S287 as `(9 words)`. The mechanical counts are **4** and **7**. The
brief's counts are *live* defects under the lane's own checker: with the brief's numbers in
the anchor cells, `plans/anchor_line_check.py` prints

```
ROW S283 state=live defects=words:1 capture=corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/test_outputs.py
ROW S287 state=live defects=words:1 capture=corpus/evidence/round81/log-summary-date-ranges-probe.txt
ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=2 repaired=0 live=2 cells=2
```

with exit code 1. With the counts below the same tool prints
`ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=0 repaired=0 live=0 cells=0`,
exit code 0. The counts below are the correct ones.

**S285 — one quote, one capture.** The brief asked for a quote from line 1 of *each* of the two
input-data files. `plans/anchor_line_check.py` verifies every quote of a row against **one**
capture (`row_defects`: `rel = sorted(caps)[0]`, one capture per row). A second quote naming
`requests_bucket_2.jsonl` is checked against `requests_bucket_1.jsonl`'s bytes and fails with a
`line` defect (`kinds=['line']`, exit 1). So S285 carries the bucket-1 quote (the first capture
its sha256 tokens resolve to) and names bucket 2's sha256 in the same anchor cell without a
second line-cited quote. This is the same one-capture-per-row constraint that makes S289 its own
row; it is stated in S289's own `teaches` cell.

**Format rules honoured.** Each row is a single 11-column table row
(`id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by`); no literal
or escaped `|` inside any cell; every quote is ≤ 25 words and carries its location; no
credential material (the only secret-bearing source, `vulnerable-secret`, is cited by its
instruction line only — the `FLAG{...}` value is never quoted).

## Registry rows (append-only, at the end of the `## Registry` table in `corpus/SOURCES.md`)

| S283 | Terminal-Bench 2.0 pinned grader `llm-inference-batching-scheduler` (member replay only) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/test_outputs.py | code | A | the six named test functions and the pinned input hashes this round's tenth offline replay grades | tests/test_outputs.py:91 quote “def test_output_files_exist() -> None:” (4 words); EXPECTED_INPUT_HASHES at :25; fetched 2026-11-05, HTTP 200, 14194 B, sha256 80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa, byte-identical to the lane capture | six deterministic grader functions (files-exist, input integrity, schema, feasibility, coverage, performance) decide six legs per case; the lane-authored fixtures grade the captured bytes, never the harness or a real submission | mined | 2026-11-05 | on-release | plans/round92-cases.json |
| S284 | Terminal-Bench 2.0 pinned cost-model sibling `cost_model_for_tests.py` (member replay only) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/cost_model_for_tests.py | code | A | the relative-import sibling the captured grader needs; stdlib-only cost and latency model deciding the threshold legs | tests/cost_model_for_tests.py:35 quote “def align(x: int, g: int) -> int:” (7 words); fetched 2026-11-05, HTTP 200, sha256 d3e810a99d40327fb8317f6512d879c52c6aeebdf5dcdc0c5e117c7df61c9ab9, byte-identical to the lane capture | the probe imports the test package so the grader's own relative import resolves; the packer iterated against this model until all five threshold legs held | mined | 2026-11-05 | on-release | plans/round92_bs_probe.py |
| S285 | Terminal-Bench 2.0 pinned task input data (member replay only) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl plus requests_bucket_2.jsonl | dataset | A | the byte-exact workload the grader's integrity leg pins; both hashes are stated inside the grader itself at :25 | requests_bucket_1.jsonl:1 quote “"request_id": "r-000000", "prompt_len": 51, "gen_len": 19}” (6 words); fetched 2026-11-05, HTTP 200; sha256 8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de and e15e2d4c4d55f875c42a6042610d6282f6c0657c39d3e0d0f087268252525cb5, byte-identical to the lane captures | 800 requests per bucket; any tamper flips exactly the integrity leg, which is the tampered-input case's predicted vector | mined | 2026-11-05 | on-release | plans/round92-cases.json |
| S286 | Terminal-Bench 2.0 verifier wrapper `tests/test.sh` (rejected; capture at corpus/evidence/round92/instructions/llm-inference-batching-scheduler-test.sh) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/test.sh | code | A | the harness wrapper this member's replay refuses | tests/test.sh:5 quote “# Install curl” (3 words); fetched 2026-11-05, HTTP 200, sha256 005f980332355e2fe143d4ff4aac11828adf070594bbe7055399c238f06953ca, byte-identical to the lane capture | REJECTED: the wrapper installs curl and uv over the network (apt-get, uvx), which the offline replay forbids; the grader semantics live in test_outputs.py (S283); flip: a claim about verifier-harness reward semantics opened as its own replay with the network legs pinned | rejected | 2026-11-05 | on-release | — |
| S287 | kengaku round-81 replay receipt S265, capture pin added as a supersede row — corpus/evidence/round81/log-summary-date-ranges-probe.txt | own-work | A | the chain tip's quote and line span, now byte-verified against the tracked receipt capture | corpus/evidence/round81/log-summary-date-ranges-probe.txt:1 quote “# tb2 log-summary-date-ranges grader probe (round 81)” (7 words); sha256 7c8d3f5656edc2affbd594cc4c33c796e01dc51852d5b00100fc1a8455f81e78; fetched 2026-11-05 | supersedes S265 — adds the capture pin the chain lacked: quote and line span unchanged, now byte-verified against the tracked receipt capture | mined | 2026-11-05 | on-release | plans/round92_f2_counter.py |
| S288 | kengaku round-81 pinned TB2 task documents S266, log-summary capture pin added as a supersede row — corpus/evidence/round92/instructions/log-summary-date-ranges-instruction.md | docs | A | the log-summary instruction quote with its capture pin (the S261 chain, log-summary half) | corpus/evidence/round92/instructions/log-summary-date-ranges-instruction.md:9 quote “Write a CSV file /app/summary.csv with the following structure (including the header):” (12 words); sha256 c1d4516ad4ec2238209740eaf01291df9ab48b0028a3fc5df383c6f831453484; fetched 2026-11-05 | supersedes S266 — adds the capture pin the chain lacked for the log-summary instruction: quote and word count unchanged, now byte-verified against the tracked capture | mined | 2026-11-05 | on-release | plans/round92_f2_counter.py |
| S289 | kengaku round-81 pinned TB2 task documents S266 chain, vulnerable-secret capture pin as a chain row — corpus/evidence/round92/instructions/vulnerable-secret-instruction.md | docs | A | the vulnerable-secret instruction quote with its capture pin (the S261 chain, vulnerable-secret half) | corpus/evidence/round92/instructions/vulnerable-secret-instruction.md:1 quote “The goal is to extract this secret key and save it to `/app/results.txt`.” (13 words); sha256 d43c72e6c39cdeb1141a9c8eae8357df1b0901383ee2beedacf828bf017d7a2f; fetched 2026-11-05 | supersedes S288 — the second capture pin of the S261 chain, as its own row because one row cites one capture file | mined | 2026-11-05 | on-release | plans/round92_f2_counter.py |
## Verification actually run (this seat)

| # | command | outcome |
|---|---|---|
| 1 | `curl` re-fetch of all 7 upstream URLs at `2fd12b88` | HTTP 200 each; sha256 byte-identical to the lane captures (`80b06b7c…`, `d3e810a9…`, `8b3cf1e2…`, `e15e2d4c…`, `005f9803…`, `c1d4516a…`, `d43c72e6…`) |
| 2 | `python3 plans/anchor_line_check.py --lane <fixture> --verbose` (rows as drafted) | `ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=0 repaired=0 live=0 cells=0`, **rc 0** |
| 3 | same tool, with the brief's `(5 words)`/`(9 words)` | `defective=2 … live=2`, **rc 1** (the red witness above) |
| 4 | same tool, with S285 carrying both files' line-1 quotes | `ROW S285 … defects=line:1`, **rc 1** |
| 5 | `scripts/sources-census.sh validate --today 2026-11-05 kengaku-shokunin` | `kengaku ok` (W04 warnings only, all pre-existing), **rc 0** |
| 6 | `python3 plans/round92_f2_counter.py --lane <clone at HEAD> --work DIR` | `CAPTURE-PINNED S287=1,S288=1,S289=1`, `ANCHORLINE … live=0`, `WRONG-LINE-CAUGHT True`, `PREDICATE R92-F2 pass`, **rc 0** |

All runs were in scratch clones under `/fast/scratch/hyaku/kengaku-r92/ScribeSources/`, which
were removed before this seat yielded. Nothing was run against the lane tree.

## Note for the L1 (integration)

These seven rows and the M14 correction row are **already in the lane** at the round-92 C commit
`42bd5104` (SOURCES S283–S289, the M14 row) and C2 `d1ccf56d` (the three word-count
corrections). The drafts above are byte-identical to the landed rows — the L1's own landed
registry already carries the correct word counts, so there is nothing to re-land and nothing to
repair. The value this seat adds is the independent re-verification of those bytes against the
upstream revision and the lane's own checkers, recorded here.
