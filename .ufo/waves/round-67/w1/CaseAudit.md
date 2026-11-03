# CaseAudit — R67-C1 six-case file audit (round 67, wave 1, seat CaseAudit)

Read-only surgical correctness review of the committed case files against the frozen
`plans/round-67-claims.md` (commit dcc39ea3) and the receipt of record
`corpus/evidence/round67/pipe/receipt.txt`. No grader run, no edits, no installs.

## 1. sha256 vs receipt (item 3)

Command: `sha256sum corpus/evidence/round67/pipe/cases/{q1-ref,q3-stub,q4-hooks-noop,q5-full-model,q6-unscaled-loss}/pipeline_parallel.py` (rc 0) vs `grep -n '^CASE' corpus/evidence/round67/pipe/receipt.txt`.

| case | computed sha256 | receipt `case_sha256` | verdict |
|---|---|---|---|
| q1-ref | `5aab7e05c846d0fe7ca364a910018cf6b29fdb607724cd3303dbf6137abb3452` | same | MATCH |
| q3-stub | `324da1b5e3f32419cfd5d2bdfcb698277c75841d86e3b5fd5c76b37955851e69` | same | MATCH |
| q4-hooks-noop | `815ad9bf1a51ea073afc6eff253e3dcffd86a804da050ec4300ea0afe6a6bcd9` | same | MATCH |
| q5-full-model | `b1cb96c81a979a1d6fc21e1241f3e3f92f7ade7718963063fa6967eadc91aa43` | same | MATCH |
| q6-unscaled-loss | `0bb52dd1af4ca13c25d5ec8136698a9efb2cb551da0a657c476383f170672518` | same | MATCH |
| q2-none | `[ -e cases/q2-none ]` → absent | `none` | MATCH (by design, no file) |

Bonus integrity check: all six `junit_sha256` in the CASE lines equal `sha256sum` of
`corpus/evidence/round67/pipe/receipt.junit/<case>.xml` (rc 0; e.g. q1-ref
`d3ebcfd9…054a0b83`, q2-none `77455447…dc4522`). No mismatch anywhere.

## 2. Per-file conformance with the claims descriptions (items 1–2)

- **q1-ref — PASS.** Contiguous ceil-partition `_partition` (rank 0 embedding, last rank
  norm+lm_head+loss); blocking `dist.send`/`dist.recv` on the given device/dtype; the
  first loop runs all `m=len(inputs)` forwards before the second loop runs any backward
  (AFAB); loss is `F.cross_entropy(...) / m` on the last rank. Grad plumbing checks out:
  non-last ranks make the received buffer a leaf (`buf.requires_grad_(True)`), backward
  on the stored non-leaf output populates `h.grad`, which is sent to `rank-1`; rank 0
  never reads/sends `h.grad`. No deadlock: point-to-point traffic is acyclic
  (forward r→r+1, backward r→r−1, strictly ordered per microbatch). Matches "correct
  AFAB … PPPP".
- **q3-stub — PASS.** Three lines, zero imports, `raise NotImplementedError` at call
  time. `exists` P; hook-literal grep count 0 → `no_hooks` P; both ws legs fail fast on
  the raise (spawn re-raises) with no communication attempted — no 900 s hang risk.
  Matches "file exists, no hook literal, schedule raises: PPFF".
- **q4-hooks-noop — PASS.** `diff q1-ref q4-hooks-noop` shows only the docstring plus
  exactly one added line, line 30:
  `model.model.norm.register_forward_hook(lambda module, args, output: None)`.
  The literal is present → `no_hooks` F. The grader's own norm hook is registered first
  and returns None; a hook returning None leaves the module output untouched, so
  numerics are byte-for-byte the q1 schedule → both ws legs P. Matches "PFPP".
- **q5-full-model — PASS.** No partition, no `dist` import or call at all — each rank
  runs embed → all 4 layers → norm → lm_head → `loss/m` per microbatch, then four
  separate backwards. All 8 hooked modules (`embed_tokens, rotary_emb, layers.0–3,
  norm, lm_head`) fire on every rank. ws1: 8 ≤ 9 layer-count bound, per-microbatch
  values identical to the reference → P. ws2: 8 > 5 on both ranks → assertion fails
  before `_cleanup_process_group`'s barrier, no communication to hang on → F. Matches
  "PPPF".
- **q6-unscaled-loss — PASS.** `diff q1-ref q6-unscaled-loss` shows only the docstring
  and the removal of ` / m` from the loss (line 52→50). Backward gradients are m=4×
  the reference → the per-microbatch `.bwd` `allclose` comparisons fail on the last
  rank at ws1 and on both ranks at ws2 (rank 1 also ships 4×-scaled `h.grad` to
  rank 0). Forward keys still match. Matches "PPFF".

Hook-literal census (grep): q1 0, q3 0, q4 exactly 1 (line 30), q5 0, q6 0 — consistent
with the frozen `no_hooks` column P,P,F,P,P.

## 3. Defect sweep (item 4) — none found

All five files: `ast.parse` OK (no syntax error, importable); imports are `torch` only
(q3: none); zero hits for `/tmp`, `open(`, `os.environ`, `subprocess`, `socket`,
`requests`, `urllib`, `sleep`, `write_text`, `Path(`, `globals()`; no module-level side
effects, no file I/O, no cwd or /tmp reliance, no network. No case contains a mechanism
that could shift its observed vector for a reason other than the grader's assertions:
q3 raises before any communication, q5 performs no communication, q1/q4/q6 communication
is deadlock-free by construction.

## 4. Verdicts

| case | file review | sha vs receipt | frozen vector | verdict |
|---|---|---|---|---|
| q1-ref | PASS | MATCH | PPPP | consistent |
| q2-none | absent by design | `none` MATCH | FFFF | consistent |
| q3-stub | PASS | MATCH | PPFF | consistent |
| q4-hooks-noop | PASS | MATCH | PFPP | consistent |
| q5-full-model | PASS | MATCH | PPPF | consistent |
| q6-unscaled-loss | PASS | MATCH | PPFF | consistent |

## Residual risk / verification gaps

- Static review only: the ws-leg outcomes (P/F) rest on the committed junit + VECTOR
  lines, not re-executed here (grader run out of scope for this seat). The hash chain
  (case sha = receipt, junit sha = receipt) is the binding to those observed outcomes.
- Layer-count arithmetic (8 keys vs 9/5 bounds) is derived from the grader capture
  `corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py`
  (`:135-141`, `(4+4)//world_size + 1`); transformers-version-dependent module names
  are not re-verified against the pinned image [INFERENCE, named limitation (ii) of the
  claim].

## Commands run (exit codes)

1. `grep -n '^CASE\|^VECTOR\|^GRADER\|^PROBE' …/round67/pipe/receipt.txt` — rc 0
2. `sha256sum …/cases/{q1-ref,q3-stub,q4-hooks-noop,q5-full-model,q6-unscaled-loss}/pipeline_parallel.py` — rc 0, five matches
3. `[ -e …/cases/q2-none ]` — absent (rc 1 from test, expected)
4. `sha256sum …/receipt.junit/q{1-ref,2-none,3-stub,4-hooks-noop,5-full-model,6-unscaled-loss}.xml` — rc 0, six matches
5. `diff …/q1-ref/pipeline_parallel.py …/q4-hooks-noop/pipeline_parallel.py` — rc 1, docstring + 1 line
6. `diff …/q1-ref/pipeline_parallel.py …/q6-unscaled-loss/pipeline_parallel.py` — rc 1, docstring + `/ m`
7. `grep -c 'register_forward_hook\|register_full_backward_hook' <q3,q5,q6>` — 0 each; `grep -n …` q4 — line 30
8. Python `ast.parse` + token sweep over all five files — all parse OK, no suspicious tokens
