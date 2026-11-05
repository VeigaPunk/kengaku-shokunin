# ScoutS283 — R92 per-surface source reconnaissance (scoped findings)

Seat: leaf scout, wave w1, round 92. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(branch master; HEAD observed `288511d8…`). **Read-only against the lane** — no lane git mutation,
no fleet-root write, no subagents, no tool installs. Full receipt with all FETCH/VERIFY lines:
`.ufo/waves/round-92/w1/ScoutS283/report.md`. Scratch (`/fast/scratch/hyaku/kengaku-r92/ScoutS283/`)
removed before yield.

## Verdict

**The round-92 source captures are byte-exact against the pinned upstream revision
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`, and every located quote holds at its cited line with
its cited word count.** All five assigned sources fetched HTTP 200 with the exact sha256 the
ticket expected; all nine lane captures verified at B2 (`f0018773…`) MATCH the independently
fetched upstream bytes; the round-81 receipt capture sha is exactly as expected. The frozen
official receipt `corpus/evidence/round92/bs-probe.txt` reproduces bit-for-bit from the lane
captures (10 CASE lines, all `ok=True`, `mismatches=0`, `PREDICATE R92-PROBE pass`), and the F2
companion behaves as the claim states (green at HEAD with `captured=78 … live=0`, red at B2 with
`PARSE-MISSING S287/S288/S289`).

**One coverage/calibration finding (F1), reported not repaired** — the sibling capture
`tests/cost_model_for_tests.py` is executed by the grader on all 60 legs but is sha-gated by
**no executable instrument** in this round.

## FETCH / VERIFY summary

| source | upstream sha256 | expected | verdict |
|---|---|---|---|
| `tests/test_outputs.py` | `80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa` | same | MATCH (HTTP 200, 14194 B, quote `def test_output_files_exist() -> None:` at :91, 4 words) |
| `tests/cost_model_for_tests.py` | `d3e810a99d40327fb8317f6512d879c52c6aeebdf5dcdc0c5e117c7df61c9ab9` | same | MATCH (HTTP 200, 17396 B, quote `def align(x: int, g: int) -> int:` at :35, 7 words) |
| `input_data/requests_bucket_1.jsonl` | `8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de` | same | MATCH (HTTP 200, 48964 B, first line `"request_id": "r-000000", "prompt_len": 51, "gen_len": 19}` at :1, 6 words) |
| `input_data/requests_bucket_2.jsonl` | `e15e2d4c4d55f875c42a6042610d6282f6c0657c39d3e0d0f087268252525cb5` | same | MATCH (HTTP 200, 50219 B, first line `"request_id": "alt-000000", "prompt_len": 72, "gen_len": 114}` at :1, 6 words) |
| `tests/test.sh` | `005f980332355e2fe143d4ff4aac11828adf070594bbe7055399c238f06953ca` | same | MATCH (HTTP 200, 721 B, quote `# Install curl` at :5, 3 words) |

Lane captures at B2 — all MATCH: `tests/test_outputs.py`, `tests/cost_model_for_tests.py`,
`tests/__init__.py` (empty), both `input_data/*.jsonl`, and all four `corpus/evidence/round92/instructions/*`
(the three non-assigned instruction counterparts — log-summary instruction, log-summary `test.sh`,
vulnerable-secret instruction — were fetched from the same pinned revision and matched).

Round-81 receipt capture sha: `7c8d3f5656edc2affbd594cc4c33c796e01dc51852d5b00100fc1a8455f81e78`
— expected, MATCH (identical at B2, HEAD and the working tree).

Corroboration beyond a 200: each fetched blob's `git hash-object` equals the blob sha in the
upstream tree listing for that revision (all nine files), and a codeload tarball of the same
revision reproduces all nine sha256 values; `num_redirects=0`; a second fetch reproduced every sha.

## F1 — the sibling capture is executed but sha-gated by no executable instrument

`plans/round92_bs_probe.py` pins three capture files by sha in its `need` map
(`tests/test_outputs.py`, `requests_bucket_1.jsonl`, `requests_bucket_2.jsonl`) and refuses to
evaluate otherwise. It does **not** pin `tests/cost_model_for_tests.py` — yet the captured grader
imports it relatively (`from .cost_model_for_tests import HEADS, HIDDEN, CostModel, align`,
upstream `test_outputs.py:22`) and the probe binds the whole capture read-only at `/tmp/tests`,
so the sibling's bytes run on every leg. It decides the threshold legs (`CostModel`/`CostConsts`:
`Kp_attn`, `Kd_attn`, `Tp_attn`, `Td_attn`, `Kshape_attn`, `Kbatch_overhead_cost`,
`Tshape_compile_ms`, `Tbatch_overhead_ms`), the shape legs (`align`, `HEADS`, `HIDDEN`) and the
cost metric `test_performance_thresholds` measures against.

Measured, in scratch clones (never the lane):

| mutation of the sibling capture | probe | registry (`anchor_line_check`) | counters |
|---|---|---|---|
| none (baseline, HEAD) | green, `captured=78 uncaptured=13 live=0` | `live=0` rc 0 | C1 + F2 green |
| comment-only (`# MUT` on `Kshape_attn`) | **green** — `mismatches=0`, `PREDICATE R92-PROBE pass` rc 0 | S284 flips `captured` → **`UNCAPTURED`** (`captured=77 uncaptured=14`) | no counter red |
| semantic value (`Kbatch_overhead_cost 10_000_000` → `10_000_001`) | **green** — all 10 cases `ok=True`, `mismatches=0`, `PREDICATE R92-PROBE pass` rc 0 | same S284 → `UNCAPTURED` | no counter red |
| grader capture, 1 byte (`NonX:`) | **red** — `DEFECT SETUP capture-sha mismatch tests/test_outputs.py`, `PREDICATE R92-PROBE could-not-evaluate` rc 2 | — | red |

So: the grader capture and the two input files are protected by an executable sha gate; the
sibling is protected only by *citation* (row S284's sha token). A sibling drift is visible in the
registry checker's output as `UNCAPTURED S284`, but by that tool's own contract an uncaptured row
is "reported, never a defect, never a pass" — it is not a defect and turns nothing red. The C1
counter's L2 leg pins `SUBJECT_SHA`/`INPUT1_SHA`/`INPUT2_SHA` (`plans/round92_c1_replay.py:153–156`)
and likewise omits the sibling; the F2 counter checks only S287/S288/S289.

**Impact on the frozen claims:** none of R92-C1/C2/C3 is falsified by this — the C1 predicate
still holds on the committed captures, and this seat's own verification shows the committed
sibling bytes are correct. The finding is that the *protection* of the sibling is weaker than the
protection of its neighbours, so a future drift of that file would not turn any round-92 predicate
red. **Reported, not repaired** (freeze discipline: instruments and predicates do not change after
A). Suggested routing for a future round: add the sibling's sha to the probe's `need` map and to
the C1 counter's L2 set — an instrument amendment, not a claim edit.

## Secondary observations (no action implied)

- **Bucket-2 id namespace.** `requests_bucket_2.jsonl` uses `alt-*` request ids while bucket 1 uses
  `r-*` (both 800 unique ids, three keys each). Registry row S285 does not mention this; benign,
  but a reader of the round-92 corpus should know it.
- **`bs-probe.txt` is absent at B2.** The receipt path is not in the B2 tree; it lands in commit C
  (`42bd5104`). Its `SUBJECT_SHA`, `INPUT_DATA_SHA`, `CASE_TABLE_SHA` (`2249d5c0…`) and
  `TOOL_SHA` (`13e41e91…`) all match the upstream/frozen values.
- **The probe's embedded packer is not the upstream model.** `plans/round92_bs_probe.py` embeds its
  own packer rather than importing upstream's `scripts/cost_model.py` / `baseline_packer.py`. Its
  decode-latency linear coefficient is 2.45 where upstream `Td_mlp*HIDDEN` = 2.4576 (−0.31 %); its
  decode-cost, prefill-latency, p95-limit and shape-set constants are exact. This affects only the
  fixture generator, never the grader's measurements, and it is disclosed in the probe docstring.
- **Import closure is complete.** AST scan of the fetched grader + sibling shows only stdlib
  imports plus the one relative sibling; the sibling reads no files. The captured set therefore
  closes the replay's dependency surface without needing upstream's `scripts/*`, `solution/solve.sh`,
  `task.toml` or `instruction.md`.
- **`scripts/cost_model.py` vs `tests/cost_model_for_tests.py`.** The two upstream files differ only
  in documentation; with docstrings stripped their ASTs are **equal**, so the captured sibling is a
  faithful stand-in for the shipped model. Already recorded in `corpus/lessons/round-92.md`.

## Tool installs

None. `curl`, `git`, `sha256sum`, `python3` (3.14.8) and `/usr/bin/bwrap` (bubblewrap 0.13.1) were
already on the host; the verification needed no new tool. pacman was not invoked (host-wide pause
respected). No host sysctl was touched (`/proc/sys/user/max_user_namespaces` read only: 122865 > 0,
so the bwrap sandbox ran normally).

## Bounds honoured

Lane git read-only (`rev-parse`, `show`, `ls-tree`, `log`, `status`, `merge-base --is-ancestor`);
no `add/commit/checkout/stash/reset/pull/push` in the lane. Scratch clones were `git clone
--shared` under my own scratch, each asserting `git rev-parse --show-toplevel` equals its own
directory before any mutation (working-tree mutations only — no commits made). No subagents, no
fleet-root or sibling-lane writes; the only lane paths written are this seat's two report files.
