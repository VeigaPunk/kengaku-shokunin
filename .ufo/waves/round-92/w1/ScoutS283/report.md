# ScoutS283 — R92 per-surface source reconnaissance (round-92 captures vs pinned upstream)

Seat: leaf scout, w1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (branch master) —
read-only throughout; no lane file was written except this report directory, no lane git mutation
(`git status --porcelain` shows only the orchestrator's own `w1-dispatch.json` edit and
`w1.ready.dispatched`, both present before this seat started). Scratch (fetches, clones, probe runs)
lived under `/fast/scratch/hyaku/kengaku-r92/ScoutS283/` and was removed before yield.

Revisions used as given: BASE `4ba56182…`, A `96f249e0…`, B `4f6b3c52…`, B2 `f0018773…`; lane HEAD
observed at `288511d8…`. Pinned upstream revision `2fd12b88aafdd04a52c298e3940bcb189f9766d6` of
`harbor-framework/terminal-bench-2`.

## Result

**All five assigned upstream sources fetch HTTP 200 at the pinned revision, byte-for-byte equal to
the sha256 the ticket expected, and byte-for-byte equal to the lane's committed captures at B2.
Every located quote is present at the cited line with the cited word count.** The round-81 receipt
capture sha is exactly as expected. Independent corroboration: a codeload tarball of the same
revision reproduces the same nine sha256 values, and each fetched blob's git blob id equals the
blob id in the upstream tree listing for that revision — so the fetches are the pinned commit's
objects, not a moving ref.

Two findings below (F1, F2) are calibration/coverage observations on the frozen instruments, not
repairs: nothing was changed in the lane.

## FETCH lines (one per assigned source)

Base URL for all: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/`

```
FETCH test_outputs.py url=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/test_outputs.py HTTP=200 bytes=14194 sha256=80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa LOCATED llm-inference-batching-scheduler/tests/test_outputs.py:91 quote "def test_output_files_exist() -> None:" (4 words)
FETCH cost_model_for_tests.py url=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/cost_model_for_tests.py HTTP=200 bytes=17396 sha256=d3e810a99d40327fb8317f6512d879c52c6aeebdf5dcdc0c5e117c7df61c9ab9 LOCATED llm-inference-batching-scheduler/tests/cost_model_for_tests.py:35 quote "def align(x: int, g: int) -> int:" (7 words)
FETCH requests_bucket_1.jsonl url=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl HTTP=200 bytes=48964 sha256=8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de LOCATED llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl:1 quote ""request_id": "r-000000", "prompt_len": 51, "gen_len": 19}"" (6 words)
FETCH requests_bucket_2.jsonl url=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_2.jsonl HTTP=200 bytes=50219 sha256=e15e2d4c4d55f875c42a6042610d6282f6c0657c39d3e0d0f087268252525cb5 LOCATED llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_2.jsonl:1 quote ""request_id": "alt-000000", "prompt_len": 72, "gen_len": 114}"" (6 words)
FETCH test.sh url=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/test.sh HTTP=200 bytes=721 sha256=005f980332355e2fe143d4ff4aac11828adf070594bbe7055399c238f06953ca LOCATED llm-inference-batching-scheduler/tests/test.sh:5 quote "# Install curl" (3 words)
```

Expected-vs-observed sha256: all five MATCH the ticket's expected values exactly
(`80b06b7c…`, `d3e810a9…`, `8b3cf1e2…`, `e15e2d4c…`, `005f9803…`).

Word counts were counted by me on the fetched bytes, not copied from the registry: the ticket's
quoted substrings split into 4 / 7 / 6 / 6 / 3 whitespace-separated words, and each quoted string is
a literal substring of the cited line. Line numbers were located by grep on the fetched bytes
(`91`, `35`, `1`, `1`, `5`).

Notes on the two jsonl quotes: the first line of bucket 1 is
`{"request_id": "r-000000", "prompt_len": 51, "gen_len": 19}` — the quote above is the whole line,
so the 6-word count includes the leading `{"request_id":` token and the trailing `}`. The first line
of bucket 2 is `{"request_id": "alt-000000", "prompt_len": 72, "gen_len": 114}` — note the **different
id namespace** (`alt-*` in bucket 2 vs `r-*` in bucket 1), which the registry row S285 does not
mention; it is benign (both buckets are 800 unique ids, three keys each) but it is a fact a reader
of the round-92 corpus should have. Each bucket is 800 lines / 800 unique request ids.

## VERIFY lines (lane captures at B2 vs pinned upstream)

```
VERIFY corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/test_outputs.py sha=80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa bytes=14194 upstream_sha=80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa MATCH
VERIFY corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/cost_model_for_tests.py sha=d3e810a99d40327fb8317f6512d879c52c6aeebdf5dcdc0c5e117c7df61c9ab9 bytes=17396 upstream_sha=d3e810a99d40327fb8317f6512d879c52c6aeebdf5dcdc0c5e117c7df61c9ab9 MATCH
VERIFY corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/__init__.py sha=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 bytes=0 upstream_sha=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 MATCH
VERIFY corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl sha=8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de bytes=48964 upstream_sha=8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de MATCH
VERIFY corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_2.jsonl sha=e15e2d4c4d55f875c42a6042610d6282f6c0657c39d3e0d0f087268252525cb5 bytes=50219 upstream_sha=e15e2d4c4d55f875c42a6042610d6282f6c0657c39d3e0d0f087268252525cb5 MATCH
VERIFY corpus/evidence/round92/instructions/llm-inference-batching-scheduler-test.sh sha=005f980332355e2fe143d4ff4aac11828adf070594bbe7055399c238f06953ca bytes=721 upstream_sha=005f980332355e2fe143d4ff4aac11828adf070594bbe7055399c238f06953ca MATCH
VERIFY corpus/evidence/round92/instructions/log-summary-date-ranges-instruction.md sha=c1d4516ad4ec2238209740eaf01291df9ab48b0028a3fc5df383c6f831453484 bytes=1391 upstream_sha=c1d4516ad4ec2238209740eaf01291df9ab48b0028a3fc5df383c6f831453484 MATCH
VERIFY corpus/evidence/round92/instructions/log-summary-date-ranges-test.sh sha=4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 bytes=608 upstream_sha=4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 MATCH
VERIFY corpus/evidence/round92/instructions/vulnerable-secret-instruction.md sha=d43c72e6c39cdeb1141a9c8eae8357df1b0901383ee2beedacf828bf017d7a2f bytes=432 upstream_sha=d43c72e6c39cdeb1141a9c8eae8357df1b0901383ee2beedacf828bf017d7a2f MATCH
```

Method: `git -C <lane> show f0018773:<path> | sha256sum` for each path (byte counts are the piped
byte counts, so a trailing-newline difference would show as a byte/shasum mismatch — none occurred).
The upstream sha256 column is the independently fetched value above, except for the three
round-92 `instructions/` files that the ticket did not assign as sources; for those I fetched the
upstream counterparts directly at the same pinned revision (`log-summary-date-ranges/instruction.md`,
`log-summary-date-ranges/tests/test.sh`, `vulnerable-secret/instruction.md`) and they too MATCH.

`corpus/evidence/round92/bs-probe.txt` was also checked: the file is **absent at B2** (`git show
f0018773:corpus/evidence/round92/bs-probe.txt` returns empty — the path is not in the B2 tree; it
lands in commit C `42bd5104`). At HEAD its sha256 is
`ba7c6a7bca7dbb16f7ab70271e68d2162dae33b07d22cbdbd9d1b1139e5b7a7d` and its `SUBJECT_SHA` /
`INPUT_DATA_SHA` / `CASE_TABLE_SHA` / `TOOL_SHA` fields match the upstream shas, the frozen case
table sha `2249d5c0…` and the probe's own bytes `13e41e91…`.

The `tests/__init__.py` capture (0 bytes) is byte-identical to the upstream `tests/__init__.py`
(empty blob, git blob id `e69de29…`) and is required for the grader's relative import to resolve —
the upstream tree has no other `__init__.py` under `tests/`.

## Round-81 receipt capture sha

```
SHA256 corpus/evidence/round81/log-summary-date-ranges-probe.txt = 7c8d3f5656edc2affbd594cc4c33c796e01dc51852d5b00100fc1a8455f81e78
```

Expected `7c8d3f5656edc2affbd594cc4c33c796e01dc51852d5b00100fc1a8455f81e78` — **MATCH**. Identical
at B2, at HEAD (`git show HEAD:…`) and in the working tree; the file is 30 lines and its line 1 is
`# tb2 log-summary-date-ranges grader probe (round 81)`, the quote S287 cites (7 words).

## Independent corroboration of the fetches

- **Git blob ids.** The upstream tree listing at `2fd12b88…` (GitHub trees API, `recursive=1`,
  1446 entries, `truncated=false`) gives a blob sha per path. `git hash-object` on each fetched file
  equals that blob sha for all nine files checked (the five assigned sources plus `tests/__init__.py`
  and the three round-92 instruction counterparts). This pins the bytes to the commit's tree, not
  merely to a URL that answered 200.
- **Tarball.** `codeload.github.com/…/tar.gz/2fd12b88…` (40 357 259 B) unpacks to the same nine
  sha256 values. Two independent transports, same bytes.
- **No redirect.** `num_redirects=0`, effective URL unchanged; `content-length` matches the byte
  count; a second fetch of each of the five assigned sources reproduced the identical sha256
  (deterministic, no CDN variance).
- **Registry agreement.** `corpus/SOURCES.md` rows S283–S289 (lines 299–305) cite the same shas,
  byte counts, HTTP 200 and access date 2026-11-05 that I observed; the `sha256` tokens they cite
  resolve to the lane captures through `plans/anchor_line_check.py`'s evidence index.

## Attack 1 — the probe's own capture gate bites (good)

In a scratch clone at B2 I mutated the captured grader by one byte
(`def test_output_files_exist() -> None:` → `…NonX:`). The probe refused to evaluate:

```
DEFECT SETUP capture-sha mismatch tests/test_outputs.py
PREDICATE R92-PROBE could-not-evaluate   (rc 2)
```

So the grader capture cannot drift under `plans/round92_bs_probe.py` without turning the probe red.

## Attack 2 — the sibling capture is **not** sha-gated anywhere executable (finding F1)

`plans/round92_bs_probe.py` (lines ~290–296) pins exactly three capture files by sha:
`tests/test_outputs.py`, `requests_bucket_1.jsonl`, `requests_bucket_2.jsonl`. It does **not** pin
`tests/cost_model_for_tests.py` — but the captured grader imports it relatively
(`from .cost_model_for_tests import HEADS, HIDDEN, CostModel, align`, upstream `test_outputs.py:22`)
and the probe binds the whole capture directory read-only at `/tmp/tests` and imports
`tests.test_outputs`, so the sibling's bytes are executed on every one of the 60 legs. It decides
the threshold legs: `CostModel`/`CostConsts` (Kp_attn/Kd_attn/Tp_attn/Td_attn/Kshape_attn/
Kbatch_overhead_cost/Tshape_compile_ms/Tbatch_overhead_ms) are what `test_performance_thresholds`
measures against, and `align`/`HEADS`/`HIDDEN` are what `test_solution_shape_feasibility_and_batch_consistency`
asserts.

Measured consequences in a scratch clone:

- **Comment-only mutation** of the sibling (append `# MUT` to the `Kshape_attn` line): the probe
  still printed `mismatches=0` / `PREDICATE R92-PROBE pass` (rc 0). A byte-drift of the sibling
  therefore passes the probe's setup gate silently — expected, since it is not in the `need` map,
  but it means the probe alone cannot detect sibling drift.
- **Semantic (value) mutation** of the sibling (`Kbatch_overhead_cost: float = 10_000_000.0` →
  `10_000_001.0`, i.e. the per-batch overhead constant the grader's cost metric multiplies by the
  batch count): the probe again printed all 10 CASE lines `ok=True`, `mismatches=0`,
  `PREDICATE R92-PROBE pass` (rc 0) — the changed constant shifts the measured cost by ~1e-5
  relative, far below the 3.0e11 / 4.8e10 thresholds, so no verdict flips. The point stands and is
  stronger than the comment case: a **value** change in a file the grader executes produces a
  byte-different capture and a fully green probe. The frozen case table constrains the *verdicts*,
  not the *constants*; nothing constrains the sibling's bytes.
- **Registry reaction.** Mutating the sibling in a clone at HEAD flips registry row **S284 from
  captured to `UNCAPTURED`** (`ANCHORLINE … captured=78 uncaptured=13` → `captured=77
  uncaptured=14`, `UNCAPTURED S284`), because the anchor check resolves the row's sha token against
  the evidence index. That is the *reported* signal — and per `plans/anchor_line_check.py`'s own
  contract, an uncaptured row is "reported, never a defect, never a pass". So the drift is visible
  in the registry checker's output but is **not** a defect and does not turn any counter red.
- **Counter reaction.** `plans/round92_c1_replay.py` (the C1 counter) pins `SUBJECT_SHA`,
  `INPUT1_SHA`, `INPUT2_SHA` in its L2 leg (lines 153–156) — the sibling is absent from that list
  too. The F2 counter (`plans/round92_f2_counter.py`) checks only S287/S288/S289, not S284.

Net effect: the sibling capture is protected by *citation* (S284's sha token) but not by any
*executable* sha gate, and a sibling drift changes the numbers the grader measures without turning
any round-92 predicate red. This is a coverage/calibration observation about the frozen instruments
— reported, **not repaired** (freeze discipline: predicates and instruments do not change after A).
Suggested routing: add `cost_model_for_tests.py` to the probe's `need` map and to the C1 counter's
L2 sha set in a future round (a counter-instrument amendment, not a claim edit).

## Attack 3 — the frozen receipt reproduces bit-for-bit from the lane captures (good)

Running the pinned probe read-only against the lane (`--lane <lane> --work <scratch>`) reproduced
the committed official receipt's observation block exactly: 10 CASE lines, all `ok=True`, all
`predicted == observed`, `mismatches=0`, `PREDICATE R92-PROBE pass` (rc 0), including the case
table sha `2249d5c0…` and the probe's own `TOOL_SHA 13e41e91…`. The stamp differs from the
committed receipt only in `LANE_TIP` (my run saw the then-HEAD `288511d8…`, the committed receipt
recorded the B2 tip `f0018773…`) and `WORKTREE dirty` (the lane had uncommitted wave bookkeeping
both then and now). The probe's capture-sha gate passed against the lane's committed captures, and
the bwrap sandbox ran with `HOST_USERNS 122865` (user namespaces > 0, no host sysctl touched by
this seat).

The committed receipt `corpus/evidence/round92/bs-probe.txt` (at HEAD) is otherwise identical in
its substantive fields, including `SUBJECT_SHA 80b06b7c…` (the upstream sha I fetched) and
`INPUT_DATA_SHA 8b3cf1e2b060741  e15e2d4c4d55` (both upstream shas, truncated).

## Attack 4 — F2 companion (S287/S288/S289 capture pins) behaves as the claim states (good)

- At HEAD: `plans/round92_f2_counter.py --lane <lane> --work <scratch>` →
  `CAPTURE-PINNED S287=1,S288=1,S289=1`, `ANCHORLINE … captured=78 … live=0 … rc=0`,
  `WRONG-LINE-CAUGHT True`, `PREDICATE R92-F2 pass`, rc 0. The wrong-line fixture is still caught,
  so the repair kept its true positive.
- At B2 (scratch clone): `CAPTURE-PINNED` empty, `DEFECT PARSE-MISSING S287/S288/S289`,
  `DEFECT ANCHORLINE captured<74 …`, `PREDICATE R92-F2 fail`, rc 1 — the red-at-BASE leg the claim
  states.
- The three pins' sha tokens resolve to real lane captures (S287 → the round-81 receipt,
  S288 → the log-summary instruction, S289 → the vulnerable-secret instruction), and each cited
  line/word count is byte-true: S287 `:1` quote (7 words), S288 `:9` quote (12 words),
  S289 `:1` quote (13 words) — I counted each from the captured bytes.

## Attack 5 — the grader's own pinned hashes are self-consistent (good, and load-bearing)

Upstream `test_outputs.py:25–32` defines `EXPECTED_INPUT_HASHES` with exactly the two jsonl
sha256 values I fetched (`8b3cf1e2…` at :27, `e15e2d4c…` at :30). The grader's
`test_input_data_integrity` leg (:105) hashes the staged input bytes and compares against them, so
the integrity leg is a real check on the capture, not a tautology. The captured grader at
`corpus/evidence/round92/graders/.../tests/test_outputs.py` carries those constants at the same
lines :25/:27/:30, byte-identically.

## Observation (not a finding) — the probe's embedded packer re-derives the upstream model

`plans/round92_bs_probe.py` does not import the upstream `environment/task_file/scripts/cost_model.py`
or `baseline_packer.py`; it embeds its own packer (`_align`, `_decode_lat`, `_wall`, `_series_cost`,
`_dp_shape`, `build_plans`) with hardcoded constants. I checked those constants against the
upstream `CostConsts` in the captured sibling:

| quantity | upstream `CostConsts` | probe's embedded value | note |
|---|---|---|---|
| decode-step latency | `Td_attn*s² + Td_mlp*(s*HIDDEN)` = `0.0012*s² + 2.4576*s` | `0.0012*(s+i)² + 2.45*(s+i)` | linear coefficient 2.45 vs 2.4576 (−0.31 %) |
| decode-step cost | `Kd_attn*s² + Kd_mlp*(s*HIDDEN)` = `1.0*s² + 2048*s` | `(s+i)² + 2048*(s+i)` | exact |
| prefill latency | `Tp_attn*S² + Tp_mlp*(S*HIDDEN)` = `0.002*S² + 6.144*S` | `0.002*s*s + 0.0015*s*4096` | exact |
| p95 limits used by the packer | thresholds `2.1e6` (b1) / `2.1e5` (b2) from the grader's `test_performance_thresholds` | `lim = {1: 2.1e6, 2: 2.1e5}` | exact |
| shape sets | grader caps ≤ 8 unique shapes jointly | `SHAPES_1=[64,128,512,1088,2048]`, `SHAPES_2=[192,320,704]` (5+3 = 8) | exact |

The packer is the *fixture generator* (it produces the plans the grader then judges); the grader's
own verdicts are computed from the captured upstream `CostModel` bytes inside the sandbox, so this
approximation affects only whether the generated plans pass, never what the grader measures. It
does not touch any frozen predicate, and it is disclosed in the probe's docstring ("the embedded
deterministic packer emits (pack6: per-shape DP over gen-groups, p95-slot budget 36, w=1e6, v=1)").
Noted as a calibration detail for the reviewer: the packer's latency model is *not* the upstream
model (0.31 % low on the decode linear term), so a packer parameter that only clears a threshold
under the exact upstream model would not clear it under the probe's. All ten frozen cases do clear
their thresholds under the upstream model as measured by the grader — that is what the receipt shows.

## Observation (not a finding) — capture-set coverage of the member's dependency closure

The upstream member tree at `2fd12b88…` also contains
`environment/task_file/scripts/cost_model.py` (8 096 B) and `.../scripts/baseline_packer.py`
(4 380 B), plus `solution/solve.sh`, `task.toml`, `instruction.md` and `environment/Dockerfile`.
None of these are captured under `corpus/evidence/round92/`, and none is needed by the replay: the
grader's import closure is exactly `tests/test_outputs.py` → `tests/cost_model_for_tests.py` →
stdlib only (verified by AST scan of the fetched bytes: `__future__`, `collections`, `dataclasses`,
`hashlib`, `json`, `math`, `os`, `typing` — no file reads in the sibling), and the replay supplies
its own plans. `scripts/cost_model.py` is the same model with the documentation *removed* relative
to `tests/cost_model_for_tests.py` — I compared both upstream files with docstrings stripped and
their ASTs are **equal**, so the sibling is a faithful stand-in for the shipped model. The lesson
file already records this ("a claim about the task's shipped `scripts/cost_model.py` (different
bytes) would be its own row"). Not a gap in the frozen claim.

## Residual unknowns / limits of this seat

- I verified the five assigned sources plus the three round-92 `instructions/` counterparts and the
  sibling, against the pinned revision. I did **not** byte-verify every file under
  `corpus/evidence/round92/`'s sibling directories beyond the graders tree listed above, nor the
  upstream member's non-replayed files (Dockerfile, task.toml, instruction.md, solve.sh,
  `scripts/*`) — they are outside the claim's scope.
- The semantic-mutation probe (a *value* change to `Kbatch_overhead_cost` in the sibling) completed:
  all 10 cases `ok=True`, `mismatches=0`, `PREDICATE R92-PROBE pass` (rc 0) — see Attack 2.
- The lane's `plans/counter-pins-r91.json` (18 entries) pins `plans/round92_bs_probe.py` at
  `13e41e916e73dcbc131c109ef38aa247f886c0336219b084c9a8e02da5300f82` and
  `plans/round92-selftest-expectations.json` at `4453495a…`; both match the bytes on disk at
  B2 and HEAD. That ledger does not pin capture bytes — captures are pinned by the SOURCES rows
  (S283/S284/S285/S286) instead, which is the F2 mechanism under test.

## Tool installs

None. No package was installed or upgraded this seat: `curl`, `git`, `sha256sum`, `python3`
(3.14.8) and `/usr/bin/bwrap` (bubblewrap 0.13.1) were already present on the host, and the
verification needed no new tool. pacman was not invoked (host-wide pause respected).

## Bounds honoured

- Lane git was read-only throughout (`rev-parse`, `show`, `ls-tree`, `log`, `status`,
  `merge-base --is-ancestor`); no `add/commit/checkout/stash/reset/pull/push` was run in the lane.
- Scratch clones were `git clone --shared` under
  `/fast/scratch/hyaku/kengaku-r92/ScoutS283/`; each fixture asserted
  `git rev-parse --show-toplevel` equals its own directory before any commit or mutation
  (the clones were mutated in the working tree only — no commits were made).
- No host sysctl was touched (`/proc/sys/user/max_user_namespaces` read only: 122865).
- No subagents were spawned; the fleet root and sibling lanes were not written.
- The only lane paths written are this report and the seat's own report file.
