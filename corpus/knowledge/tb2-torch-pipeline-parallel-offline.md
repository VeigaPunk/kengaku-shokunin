source: S238 (corpus/SOURCES.md) — Terminal-Bench 2.0 torch-pipeline-parallelism grader, tests/test_outputs.py at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/tests/test_outputs.py — anchor: tests/test_outputs.py lines 19-43 (legs 1-2), 91-168 (inner test), 171-178 (parametrised legs) — sha256 23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f; S239 (corpus/SOURCES.md) — Terminal-Bench 2.0 torch-pipeline-parallelism instruction.md at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/instruction.md — anchor: instruction.md lines 17-18 (AFAB order), 30-33 (hooks, world sizes) — sha256 989bfcf0c54baf6c8cdc391743dbb2f9e858c5779dd85112536875d4d1b2dcd2
verified-at: 2026-11-03 (both captures re-hashed and cmp-checked in this seat against the committed bytes at corpus/evidence/round67/sources/; the live open of S238/S239 is the round-67 freeze record in plans/round-67-claims.md F1 and was not re-fetched here; receipt of record corpus/evidence/round67/pipe/receipt.txt)
recheck: pinned at 2fd12b88aafdd04a52c298e3940bcb189f9766d6 (an immutable commit, so recheck the committed bytes, not the default branch): `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt` must print `PREDICATE R67-C1 pass` with rc 0; `sha256sum corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py` must print 23574246…c64f. A fresh grader run is wrapped as `flock /home/vgpnk/.local/share/kengaku-r67/port-12355.lock <command>`.

# TB2 `torch-pipeline-parallelism` — the grader replayed offline against a lane-built AFAB `pipeline_parallel.py` (R67-C1)

## Status

The second `process-environment` census member (`corpus/evidence/round62/class-survey.txt:14`; the first is `torch-tensor-parallelism`, `corpus/knowledge/tb2-torch-tensor-parallel-offline.md`) is replayed offline. The committed receipt of record passes its predicate. The lane's coverage axis stays L0-capped at 7: `kengaku | round-25/33/51` is still open, and executing this grader does not answer it. The capability `offline-torch-pipeline-parallel-grader-probe` enters on the predicate pass.

This entry prices an offline replay of the grader's verdicts on six frozen cases. It does not show that any agent can write `pipeline_parallel.py`, and it does not show that the grader tests distributed training correctness beyond what its assertions state.

## What the grader checks: four legs, with derivation

Task `torch-pipeline-parallelism`, `tests/test_outputs.py` at pin `2fd12b88` (S238; the lane capture is `corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py`, byte-identical to `corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py`, both sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f`). Four pytest outcomes; the junit node names are `test_pipeline_parallel_exists`, `test_no_hooks_in_pipeline_parallel`, `test_pipeline_parallel[1]`, `test_pipeline_parallel[2]`.

| leg | junit node | what the file asserts (S238 line) | P iff |
|---|---|---|---|
| exists | `test_pipeline_parallel_exists` | `Path("/app/pipeline_parallel.py")` (:24); `assert pipeline_parallel_path.exists()` (:26) | no `failure`/`error` child |
| no_hooks | `test_no_hooks_in_pipeline_parallel` | opens `/app/pipeline_parallel.py` (:36); `assert "register_forward_hook" not in code` (:38); `assert "register_full_backward_hook" not in code` (:41) | no `failure`/`error` child |
| ws1 | `test_pipeline_parallel[1]` | `@pytest.mark.parametrize("world_size", [1, 2])` (:171); `mp.spawn(_test_pipeline_parallel, nprocs=world_size)` (:178) | no `failure`/`error` child |
| ws2 | `test_pipeline_parallel[2]` | same parametrisation and spawn as ws1 | no `failure`/`error` child |

The inner test `_test_pipeline_parallel` (:91-168), run once per rank, does the following:

- imports the candidate `from pipeline_parallel import train_step_pipeline_afab` (:93) and calls it (:140);
- registers hooks on the reference and the candidate model with `_register_hooks` (:87-88 install `register_forward_hook` and `register_full_backward_hook` in the grader's own code, not the candidate's);
- **layer-count assertion** (:142-146): `num_layers` counts `.fwd` keys in `pipeline_dict`, and must satisfy `0 < num_layers <= ((4 + config.num_hidden_layers) // world_size + 1)`. With `num_hidden_layers=4` this bound is **9 at world size 1 and 5 at world size 2**. The grader's own comment at :143 lists the hooked modules (`embed_tokens, norm, rotary_emb, lm_head, hidden_layers`, i.e. 4+4);
- **microbatch count** (:151): `len(ref_vals) == len(pipe_vals)` per key;
- **AFAB check** (:148-158): iterates `pipeline_dict.items()` in dictionary insertion order (:149); sets `bwd_flag` on a `.bwd` key (:153-154); raises `AssertionError("AFAB violation: found forward after backward at {key}")` on a `.fwd` key that follows a `.bwd` key (:155-158, message at :157);
- **value comparison** (:160-166): `torch.allclose(ref_val, pipe_val, atol=1e-5)` per microbatch per key, `assert False` on mismatch;
- cleanup `dist.barrier()` and `destroy_process_group()` (:168 via `_cleanup_process_group`, :55-58).

The process group uses `MASTER_PORT=12355` on `localhost` with `gloo` (:46-52, port literal at :49).

The instruction (S239) states the same schedule and hook requirements the grader tests. Line 18: "Run forward passes for all microbatches first, then run backward passes." Line 31: "You must not use hooks inside your implementation." Lines 32-33: "The tests will check that each rank runs a reasonable number of layers. The tests will use world_size values of 1, 2."

## The six-case table, copied from the receipt

The receipt of record is `corpus/evidence/round67/pipe/receipt.txt` (sha256 `a9b9735bcc42fa673540de6e7c70cdfc45b97e008b033492033942261554f1e7`, observed by `sha256sum` in this seat; copy at `.ufo/waves/round-67/w1/KnowledgeDraft/cited/receipt.txt`). Vector order is `exists/no_hooks/ws1/ws2`. Each `VECTOR` line below is copied verbatim from the receipt (receipt line in the first column); each `CASE` sha is copied from the CASE line of the same case.

| receipt line | case | what it is | vector (copied from receipt) | observed failing mechanism (junit under `receipt.junit/`) | `case_sha256` (CASE line) |
|---|---|---|---|---|---|
| 7 | `q1-ref` | correct AFAB reference: contiguous layer slices, blocking send/recv, all forwards then all backwards, loss `/ m` | `VECTOR q1-ref exists=P no_hooks=P ws1=P ws2=P frozen=match` → **PPPP** | none; `rc=0` | `5aab7e05c846d0fe7ca364a910018cf6b29fdb607724cd3303dbf6137abb3452` (line 6) |
| 9 | `q2-none` | do-nothing: `/app` empty, no file | `VECTOR q2-none exists=F no_hooks=F ws1=F ws2=F frozen=match` → **FFFF** | exists `AssertionError: File /app/pipeline_parallel.py does not exist` (test :26); no_hooks `FileNotFoundError` (test :36); ws1 and ws2 `ModuleNotFoundError: No module named 'pipeline_parallel'` (test :93) | none (no file; line 8 records `none`) |
| 11 | `q3-stub` | file exists, no hook literal, `train_step_pipeline_afab` raises `NotImplementedError` | `VECTOR q3-stub exists=P no_hooks=P ws1=F ws2=F frozen=match` → **PPFF** | ws1 and ws2 `NotImplementedError: stub: pipeline schedule not implemented` raised at `/app/pipeline_parallel.py` line 5, reached from test :140 | `324da1b5e3f32419cfd5d2bdfcb698277c75841d86e3b5fd5c76b37955851e69` (line 10) |
| 13 | `q4-hooks-noop` | q1-ref schedule plus one no-op `register_forward_hook` on `model.model.norm` (case line 30); the hook returns `None` | `VECTOR q4-hooks-noop exists=P no_hooks=F ws1=P ws2=P frozen=match` → **PFPP** | no_hooks `AssertionError: register_forward_hook must not be used in implementation` (test :38-39) | `815ad9bf1a51ea073afc6eff253e3dcffd86a804da050ec4300ea0afe6a6bcd9` (line 12) |
| 15 | `q5-full-model` | no partition: every rank runs all four layers and the whole model; no communication | `VECTOR q5-full-model exists=P no_hooks=P ws1=P ws2=F frozen=match` → **PPPF** | ws2 Process 1: `AssertionError: Rank 1 has too many layers: 8` (test :144) | `b1cb96c81a979a1d6fc21e1241f3e3f92f7ade7718963063fa6967eadc91aa43` (line 14) |
| 17 | `q6-unscaled-loss` | q1-ref schedule with the loss not divided by `m` (case line 50 is `)`, q1-ref line 52 is `) / m`) | `VECTOR q6-unscaled-loss exists=P no_hooks=P ws1=F ws2=F frozen=match` → **PPFF** | ws1 Process 0: `Rank 0 mismatch at lm_head.bwd, microbatch 0, max diff=0.10714028775691986` (test :163); ws2 Process 1: `Rank 1 mismatch at lm_head.bwd, microbatch 0, max diff=0.10714028775691986` (test :163) | `0bb52dd1af4ca13c25d5ec8136698a9efb2cb551da0a657c476383f170672518` (line 16) |

The frozen table is `FROZEN_TABLE` in `plans/round67_c1_pipeline_probe.py` (lines 71-78), frozen before the run; every receipt `VECTOR` line reads `frozen=match`. The six `junit_sha256` values in the CASE lines equal `sha256sum` of `corpus/evidence/round67/pipe/receipt.junit/<case>.xml` (checked in this seat).

Observed, not recomputed: the junit failure text above is read from the receipt's junit bytes by a python `ElementTree` parse in this seat (`failure`/`error` child per testcase), which matches the receipt's vectors.

**Counting command (after):** `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt; echo $?` → `CHECK ok cases=6`, `PREDICATE R67-C1 pass`, exit 0 (observed in this seat; output at `.ufo/waves/round-67/w1/KnowledgeDraft/check-receipt-cited.txt`).

**Counting command (before):** `grep -c 'torch-pipeline-parallelism' corpus/evidence/round52/graders/executed17.lst` → `0`, rc 1 (observed in this seat; grep's rc 1 is the zero-match exit). The entry therefore records the member as absent from the executed list before this round.

## The AFAB dictionary-order limitation: confirmed at world size 1, open at world size 2

The AFAB check (:148-158) only fires when a `.fwd` key is first inserted into `pipeline_dict` after a `.bwd` key has been seen (:149 iterates in insertion order). The dictionary records the order in which each *name* is first created, not the call sequence. Every hooked module is first entered during microbatch 0's forward, so a schedule that interleaves forwards and backwards within a rank leaves the key order unchanged.

**Verdict, from the labrat seat (`.ufo/waves/round-67/w1/AfabLab/labrat.md`, sha not hashed by this seat):** H-AFAB, "confirmed on the ws1 leg with the frozen grader." A one-forward-one-backward variant (`case-1f1b`, sha256 `573d5cc35a1ca627a2ac33e282d20fd65cb61349a274582af815534b227ce1c5`) passes the frozen grader's `test_pipeline_parallel[1]` with rc 0. This seat re-checked the labrat's junit bytes by parse: `1f1b-junit.xml` (sha256 `ee4f88bc6a50c84ff3fa5eb60de59f52f460750048f53bf4db37be5fb4c0b937`) reads `test_pipeline_parallel[1] P`, and `ref-junit.xml` (sha256 `508dd59cc9517958dd32a63305dc7dc84f1900ba08c8a6db5f41a1d3ca30d4a5`) reads `P`. The labrat's `hookorder.txt` (sha256 `59825b1c10e6e5f5e657bc367c05690d054dd35b851dc1dea766a75c8c5f8d39`) records identical key order and counts for the AFAB reference and the 1F1B variant, and `afab_would_fire_at: None` for both. Consequently the grader's AFAB rule does not separate AFAB from 1F1B at world size 1.

Two qualifications, both from the labrat's own limitations:

- **World size 2 was not run.** The labrat deliberately ran ws1 only. At ws2 rank 0 is not the last stage, so the 1F1B variant's inter-rank send/recv interleaving is untested. The claim "the AFAB rule cannot separate schedules at ws2" is **not established**.
- **The detector is reachable, but only by a forward-first-entry substitution.** The labrat's control `case-ctl` (sha256 `4fdfb45824ff4eb223de51ad0c749e577695ff1335fbeb0636e10f749a3b4957`) fires the AFAB raise at `test_outputs.py:156` on `lm_head.fwd` (junit `ctl-junit.xml`, parse: `F`). Its control `case-ctl2` (sha256 `4ff7dc2fb76b52c1c230ae2075f3479ad235aaa42508230c1720c83a40d0bb73`) does not reach the AFAB raise: the value comparison at `:163` fails first on `model.layers.1.bwd`. So the check is not dead code at ws1, but it is sensitive to which module is first entered late, not to phase separation as such.

The labrat's wave receipt is cited here as a wave receipt, not as a source. The Gate below does not count it as a source re-read.

## The no-hooks rule is a literal substring test

`test_no_hooks_in_pipeline_parallel` (:31-43) does `"register_forward_hook" not in code` and `"register_full_backward_hook" not in code` on the whole file text. It is not an AST check, so the literal is matched in comments and docstrings as well as in calls. Observed in this seat by a string test on the two literals (`/usr/bin/python3`, no grader run): `register_forward_pre_hook`, `register_backward_hook` and `register_full_backward_pre_hook` do **not** match; `register_forward_hook` and `# register_forward_hook in a comment` **do** match. The case-file grep (`grep -c 'register_forward_hook\|register_full_backward_hook'`) gives 0 for q1-ref, q3-stub, q5-full-model and q6-unscaled-loss and 1 for q4-hooks-noop (line 30), consistent with the frozen `no_hooks` column.

The instruction (S239 line 31) forbids hook use, and the grader enforces the literal. A candidate that uses a hook spelled differently passes the grader's rule and violates the instruction; the grader does not test that. This is stated, not measured on a candidate.

## Named limitations (from `plans/round-67-claims.md`, stated before data)

- **(i) The AFAB check is dictionary-order.** Confirmed at ws1 by the labrat seat (above); not tested at ws2.
- **(ii) The pinned image is not read.** The torch, transformers and pytest versions are the lane's install (`torch==2.15.0+cpu`, `transformers==5.22.1`, `pytest==9.2.0`, python 3.14.8, from the receipt's `VENV` line 5). The grader's container pins are not observed; the install is named `[INFERENCE]` for the pinned image's versions. Layer-module naming in transformers 5.22.1 determines the eight `.fwd` keys the layer-count assertion counts; the observed value `8` (q5 ws2 junit) is the 5.22.1 value.
- **The receipt check is not proof of execution.** `--check-receipt` re-derives each VECTOR from the committed junit bytes and binds case and junit bytes by sha. It does not run the grader. The hand-copy test in this seat confirms it: a copy of the committed receipt and its `receipt.junit/` directory, placed in a scratch directory, also prints `PREDICATE R67-C1 pass` with rc 0 (`.ufo/waves/round-67/w1/KnowledgeDraft/check-receipt-handcopy.txt`). The receipt is a record of a past run on those bytes, not a fresh observation.
- **Single run per case.** The receipt records one run per case. No repeat-run determinism is observed for the vectors.
- **Port 12355 is a fixed constant in the pinned grader.** The probe takes `flock` on `~/.local/share/kengaku-r67/port-12355.lock` and refuses (SETUP, exit 2) when the port is busy. The receipt does not record the lock state; this seat did not run the probe.
- **The grader is the oracle.** Every P and F above is the grader's own verdict read from junit. The entry's reading of the assertions is explanation, not evidence of the verdict.
- **Timing is not recorded.** The claims doc mentions a 13 s dev run of q1-ref in a scratch directory; that run is disclosed as not data for any claim, and no timing is in the receipt. No timing value is admitted here.
- **The labrat's model configuration is one only.** Hidden 512, four decoder layers, four microbatches, the grader's own configuration; the ws1 layer-count bound is 9 and both schedules report 8 `.fwd` keys.

## Negative space

- The sources do not establish that the grader tests distributed correctness beyond the listed assertions. The layer-count bound and the allclose comparisons are the whole of the numeric check.
- The sources do not establish the grader's container image, its transformers pin, or whether the port is free in the grader's own environment.
- The AFAB rule at world size 2 is not established by any observation in this entry.
- The sources do not establish a tier-A source for the claim that eight modules are hooked; the count of eight is the grader's own comment at :143 and the observed q5 ws2 junit value `8`, not an independent measurement of the transformers module tree.

## Falsifier

This entry is wrong if any of the following is observed:

1. `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt` exits non-zero on the committed bytes (the claim's kill rule (b)).
2. A fresh run of the grader under the port lock produces a vector for any case other than the receipt's line 7/9/11/13/15/17 vector (the receipt is not reproducible).
3. `sha256sum corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py` prints anything other than `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f`.
4. A 1F1B candidate that the frozen grader fails at `:156` (`AFAB violation`) on the ws1 leg contradicts the labrat's confirmed ws1 reading (H-AFAB); cite that run against the AFAB section. A 1F1B candidate that the grader passes at ws2 would bear on the open ws2 question and is not yet tested.

## Rejected

- Rejected: "The grader enforces AFAB order by schedule." S238 :148-158 is a dictionary-order check on recorded hook keys, not a schedule check (confirmed by the labrat at ws1); flip: a grader revision that asserts the schedule directly.
- Rejected: "The no-hook rule forbids every hook use." The rule is the literal substring test at :38 and :41; `register_forward_pre_hook` and `register_backward_hook` do not match (string test above); flip: a grader revision that scans for any `register_*hook` call or uses an AST check.
- Rejected: "transformers 5.22.1 is the pinned image's version." The grader's container pins were not read; flip: reading the pin's image definition at `2fd12b88`.
- Rejected: "a 13 s q1-ref run time" as a receipt value. The receipt carries no timing; the value is in the claims doc as a dev-run disclosure; flip: a timing line in a committed receipt.
- Rejected: "the AFAB rule separates AFAB from 1F1B at world size 2." Not run by the labrat and not run here; flip: a ws2 1F1B run in the lock that the grader fails.
- Rejected: a second-seat re-read as performed. This seat is the writer; the Q10 re-read of each quote and number by a non-writer seat is not performed. Flip: a registered reviewer, scout, critic or sentinel seat re-opens S238 and S239 and writes a report that the Gate row cites by path.

## Gate

| source | URL | access date | located quote (line) | words |
|---|---|---|---|---|
| S238 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/tests/test_outputs.py | 2026-11-03 (live open at freeze, claims F1; re-hashed in this seat against the capture) | `AFAB violation: found forward after backward at {key}` (capture line 157) | 8 |
| S238 | same | 2026-11-03 | `assert "register_forward_hook" not in code, (` (capture line 38) and `register_forward_hook must not be used in implementation` (line 39) | 8 |
| S238 | same | 2026-11-03 | `assert 0 < num_layers <= ((4 + config.num_hidden_layers) // world_size + 1), (` (capture line 144) | 14 (code tokens) |
| S238 | same | 2026-11-03 | `@pytest.mark.parametrize("world_size", [1, 2])` (capture line 171) | code |
| S239 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/instruction.md | 2026-11-03 (live open at freeze, claims F1; re-hashed in this seat against the capture) | `Run forward passes for all microbatches first, then run backward passes.` (capture line 18) | 12 |
| S239 | same | 2026-11-03 | `You must not use hooks inside your implementation.` (capture line 31) | 9 |
| S239 | same | 2026-11-03 | `The tests will check that each rank runs a reasonable number of layers.` (capture line 32) | 14 |
| S239 | same | 2026-11-03 | `The tests will use world_size values of 1, 2.` (capture line 33) | 9 |

Every quote is at most 25 words. The S238 code quotes are verbatim source lines. The capture paths are `corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py` (sha256 `23574246…c64f`) and `corpus/evidence/round67/sources/torch-pipeline-parallelism-instruction.md` (sha256 `989bfcf0…2dcd2`), both checked in this seat.

Second-seat re-read (Q10/Q13): not performed by this seat. Pending: a non-writer seat from the reviewer-like roles re-opens each quote and line number above and confirms it.

Q5 labels: S238 and S239 are the benchmark maintainer's own published task artefacts (a self-report by the benchmark, not an independent replication of a model result); the entry uses them for what the grader and the task statement say, and for nothing about model performance. The labrat receipts are wave receipts from this round, not sources.

Q6: extends the TB2 offline-replay series (`corpus/knowledge/tb2-torch-tensor-parallel-offline.md` for the first `process-environment` member, R66-C1) and does not overwrite it.

## Post-data findings (round 67, 2026-11-03; appended, not edited in place)

- **Counter amendment A1 (dated, `plans/round-67-claims.md`).** The first receipt (`corpus/evidence/round67/pipe/receipt-prea1.txt`) passed the pre-amendment counter; a non-author mutation pass (`ProbeMutate`, `ProbeReview`) showed the counter accepted a deleted VECTOR line, a duplicate or unknown CASE line, a contradictory `frozen=` label and an rc the pytest status could not produce. A1 enforces the frozen predicate sentence; the record receipt was re-issued under A1 (`corpus/evidence/round67/pipe/receipt.txt`, `PREDICATE R67-C1 pass`). The vector table is unchanged.
- **A receipt is a consistency check, not provenance.** `ClaimFalsifier` A2 forged a receipt whose junit XML spells the frozen vectors and whose hashes agree with it; `--check-receipt` passes it. The only evidence that the outcomes came from a run is the live run of record. The forged-receipt fixture is not committed as evidence.
- **The candidate shares the sandbox with pytest.** `SecurityScan` must-fix: a candidate-spawned process can write `/ctl/junit.xml` after pytest's verdict. The six frozen cases are lane-authored, so the record stands for them; the probe must not be used for a candidate that is not lane-authored until the result channel is isolated.
- **`no_hooks` is a substring test.** `ClaimFalsifier` A1 wrote a candidate that builds the hook name at run time, registers a hook, never partitions or communicates, and earns `exists=P no_hooks=P ws1=P` on the grader. The frozen table has no row for that candidate; no row is added after data.
- **AFAB at world size 2 is not tested here.** The labrat confirmed the ws1 reading only (see above).
