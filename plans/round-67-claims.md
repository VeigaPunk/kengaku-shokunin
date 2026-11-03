# Round 67 — declared claims (frozen before the receipt of record and before the wave)

Lane: kengaku (novelty + calibration; LLM and model research and evaluation; hyaku run 15, attempt 1).
Lane-root base for every path here and in the round report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Base: `master` tip at freeze (`git rev-parse master` in the freeze commit's parent; cited in the round report).

Frozen artifacts: this file; `plans/round67_c1_pipeline_probe.py` (its sha256 is the `PROBE` line of the receipt of record); the six case directories under `corpus/evidence/round67/pipe/cases/` (q2-none has no case file: an empty `/app`); the grader capture `corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py` (SHA256SUMS line 169); the live source captures `corpus/evidence/round67/sources/`; the wave spec and dispatch under `.ufo/waves/round-67/w1/`.

Dev build check, disclosed (not data for any claim): one run of `q1-ref` through `run_case` (rc 0, `PPPP`, 13 s, scratch `/fast/scratch/hyaku/kengaku-r67/dev`) was made while the reference case was written, to catch a defect in the build. The frozen table below was written before that run and is not changed by it.

Environment (installed this round, recorded per RULES.md): `uv venv --python /usr/bin/python3 ~/.local/share/kengaku-r67/venv-pipe` (uv 0.13.0, `~/.local/bin/uv`, channel: uv, reason: the grader imports `torch` and `transformers`, neither present on the host); `uv pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu` → `torch==2.15.0+cpu`; `uv pip install pytest==9.2.0 transformers` → `transformers==5.22.1`, `pytest==9.2.0`. The grader's own container pins were not read; transformers 5.22.1 is the version this probe ran against and is named as such (`[INFERENCE]` for the pinned image's versions).

Lowest owned axis: **coverage 7** (L0-capped: `kengaku | round-25/33/51` still open; nothing assumed answered). Worked by R67-C1. No stagnation waiver invoked.

Claim count: 2, distinct axes (coverage; operability). Causally separable: C1 is verifiable from its own receipt, the grader bytes and the case bytes; C2 is verifiable from the committed round-65 receipt, the committed round-65 probe and the fabricated fixture, without C1 landing.

---

## R67-C1 — coverage (L0-capped at 7); capability acquisition `offline-torch-pipeline-parallel-grader-probe`

Target: the second `process-environment` census member (`corpus/evidence/round62/class-survey.txt:14`; the first is `torch-tensor-parallelism`, R66-C1) runs offline. Its class row stays `recipe-unexecuted` until this predicate passes.

Predicate (one sentence, identical in the counter code, the receipt label and this text): `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt` exits 0 and prints `PREDICATE R67-C1 pass`, where the receipt carries six `VECTOR` lines whose outcome vectors equal the frozen table in `plans/round67_c1_pipeline_probe.py` (vector order `exists/no_hooks/ws1/ws2`: q1-ref PPPP; q2-none FFFF; q3-stub PPFF; q4-hooks-noop PFPP; q5-full-model PPPF; q6-unscaled-loss PPFF), every `CASE` `junit_sha256` equals the bytes of `corpus/evidence/round67/pipe/receipt.junit/<case>.xml`, every `case_sha256` equals the committed case file (or `none` for q2-none), the `GRADER` line names sha `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f` and the committed grader bytes carry that sha, and the `PROBE` line names the committed probe sha and version `r67-c1/1`.

Frozen table rationale (grader lines, `corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py`): `exists` is the test at `:19`; `no_hooks` is the test at `:31`; `ws1`/`ws2` are the parametrised `test_pipeline_parallel` at `:171-178`, which spawn `_test_pipeline_parallel` (`:91-169`) and compare hook activations per microbatch; the layer-count assertion is at `:144` (`<= (4+4)//world_size + 1`, i.e. 9 at ws1, 5 at ws2) and the AFAB check at `:154-157`.
- q1-ref: a correct AFAB schedule (layer partition, blocking send/recv, all forwards before all backwards, loss divided by the microbatch count): PPPP.
- q2-none (do-nothing control): no file; `exists` fails, `no_hooks` fails on the open, both pytest world-size legs fail at import: FFFF. This is the cheapest control that skips the claimed work; it does not meet the target, so the counter is not wrong in the easy direction.
- q3-stub: file exists, no hook literal, schedule raises: PPFF.
- q4-hooks-noop: correct numerics plus a no-op forward hook (the literal `register_forward_hook` is in the code, so `no_hooks` fails; the hook returns None so both world sizes pass): PFPP.
- q5-full-model: no partition, every rank runs every layer; ws1 passes; ws2 fails the layer-count assertion on both ranks before any barrier: PPPF.
- q6-unscaled-loss: schedule correct, loss not divided by the microbatch count; ws1 and ws2 both fail the backward comparison on the ranks that compare: PPFF.

Kill rules: (a) any frozen vector differs from the receipt → the claim is not admitted and the miss is reported, the table is not edited after the run; (b) `--check-receipt` exits non-zero on the receipt of record for a reason other than a miss in (a) → the counter is wrong, the claim is not admitted; (c) a case hangs past the 900 s bound → the probe exits 2 (could-not-evaluate), the claim is not admitted, and no vector is inferred.

Named limitations (stated before data): (i) the AFAB check at `:154-157` only fires when a `.fwd` key first appears after a `.bwd` key in the per-rank hook dictionary; a 1F1B schedule at world size 1 is therefore not separable from AFAB by this grader. That is a *hypothesis* for a labrat seat in the wave, not a frozen claim. (ii) transformers 5.22.1 is the version run; the grader's pinned image is not read.

Score: coverage held at 7 under the L0 cap (a grader execution does not lift the cap; `kengaku | round-25/33/51` stays open). Capability row `offline-torch-pipeline-parallel-grader-probe` enters only on the predicate's pass.

Sourced: S238 (grader at pin; opened live 2026-11-03; capture identical to `round52` SHA256SUMS line 169) and S239 (instruction at pin; opened live 2026-11-03).

---

## R67-C2 — operability (held at ceiling 10, exercised): the round-65 sqlite receipt gate refuses a fabricated receipt without a PROBE line

Defect: SecurityScan M-1 (`.ufo/waves/round-65/w1/SecurityScan.md`): `--check-receipt` on `plans/round65_c1_sqlite_probe.py` accepts the hand-fabricated `corpus/evidence/round66/red/fabricated-r65.txt` (`CHECK ok cases=5`, `PREDICATE R65-C1 pass`, rc 0; `corpus/evidence/round66/red/red-before-r65-checker.txt`). R66-C2 tried to fix this with a PROBE-sha binding and was **not admitted** (kill rule b: the committed round-65 receipt has no `PROBE` line; `grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt` → `0`). This claim is the successor: it re-freezes the same counting command with the PROBE clause replaced by a binding the committed receipt actually carries.

Pre-freeze read of the committed receipt (this round, before this freeze): line 2 is `# instrument plans/round65_c1_sqlite_probe.py version=r65-c1/1`; the probe's committed `PROBE_VERSION = "r65-c1/1"` (`plans/round65_c1_sqlite_probe.py:114`); the `RUN` lines carry `driver="/usr/bin/python3 /ctl/driver.py"`; the `CC`, `GCOV`, `BWRAP` lines carry the version tokens 16.2.1, 16.2.1, 0.13.1.

Predicate (one sentence, identical in the counter code, the label and this text): `python3 plans/round65_c1_sqlite_probe.py --check-receipt <R> --strict` exits 1 with at least one `CHECK defect:` finding on `corpus/evidence/round66/red/fabricated-r65.txt`, exits 0 on `corpus/evidence/round65/sqlite-gcov-probe.txt`, and `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` (default mode, unchanged) still prints `PREDICATE R65-C1 pass` with rc 0.

Strict-mode clauses (frozen; a receipt must satisfy all): (s1) the header line `# instrument plans/round65_c1_sqlite_probe.py version=<V>` is present, and `<V>` equals `PROBE_VERSION` in the committed probe bytes; (s2) the `GRADER` sha equals `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` and the committed grader bytes at `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py` carry that sha; (s3) the `AMALG` sha equals `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`; (s4) the `TOOLCHAIN` gcc, gcov and bwrap values are not `fabricated` and equal the version tokens on the receipt's `CC`, `GCOV` and `BWRAP` lines (python is not cross-checked: the receipt carries no python line — named limitation); (s5) every `RUN` line carries `rc=0` and `driver="/usr/bin/python3 /ctl/driver.py"`, every `NOBIND` line carries `delta=0`, and every `BUILD`, `FILES` and `ENV` line for G1–G5 is present; (s6) each `VECTOR` line equals the frozen table in the probe.

Kill rules: (a) strict accepts the fabricated fixture → not admitted; (b) strict refuses the committed round-65 receipt → not admitted, the miss is reported, the clauses are not narrowed after the run; (c) the default-mode output over the committed receipt changes → not admitted.

Named limitation (stated before data): a receipt that copies every value from the committed bytes still passes strict; the gate refuses value-free, value-mismatched and driver-fabricated receipts, not a hand-copied full receipt. The C1 junit binding is the stronger check and is a different gate.

Counting command (after): the three commands in the predicate, exit codes printed.

Score: operability held at 10 (exercised). The R65 probe's default predicate and its SKILL/registry rows are not changed by this claim.

Sourced: the defect is the round-65 sentinel finding (`.ufo/waves/round-65/w1/SecurityScan.md` M-1) and the committed R65 receipt bytes; no `S###` row is cited.

---

## Frontier step (inside the claim cap; not a claim)

- **F1 — sources opened live this round (2026-11-03).** S238: `torch-pipeline-parallelism/tests/test_outputs.py` at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, curl HTTP 200, sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f`, capture `corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py` (byte-identical to the round-52 capture, `cmp` checked). S239: `torch-pipeline-parallelism/instruction.md` at the same pin, HTTP 200, sha256 `989bfcf0c54baf6c8cdc391743dbb2f9e858c5779dd85112536875d4d1b2dcd2`, capture `corpus/evidence/round67/sources/torch-pipeline-parallelism-instruction.md`. The C1 rests on S238 (test structure) and S239 (the AFAB and no-hook requirements).
- **F2 — mistakes mined (round 66, `corpus/lessons/round-66-verifier-spotcheck.md` §2 R66-C2).** The round-66 R66-C2 predicate required a `PROBE` line the committed round-65 receipt never carried (`grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt` → 0). Class: predicate frozen against an artifact shape the lane had not checked. Captured-by: none (the round-66 freeze review checked the proposal's receipts, not the committed receipt's shape). Fix: C2 above, frozen only after the pre-freeze read recorded in its text; its kill rule (b) is the test that the fix can fail.
- **F3 — assimilation.** None this round (no `merge/kengaku/` theme is admitted; the round-54 mass id drift stays open in L0 `kengaku | round-54`; adopting nothing is the honest state).
- **F4 — considerthese.** Not mined this round.
