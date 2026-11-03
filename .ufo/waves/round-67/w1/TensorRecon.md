# Round 67 w1 — Seat TensorRecon Findings

**Seat:** `TensorRecon` (scout / leaf member; no subagent dispatch).
**Role:** Read-only audit and derivation of the frozen R67-C1 vector table against the pinned grader.
**Status:** Complete; all 24 cells derived from source evidence; predicate verified.

---

## 1. Executive Verdicts

| Check | Expected | Observed | Verdict |
|---|---|---|---|
| Grader byte & sha identity | `23574246...` (L169 of SHA256SUMS) | `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f` (178 lines) | **PASS** |
| Probe byte & sha identity | `32bacf1d...` (receipt line 3) | `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836` | **PASS** |
| Receipt verification | `CHECK ok cases=6`, `PREDICATE R67-C1 pass` | `python3 plans/round67_c1_pipeline_probe.py --check-receipt ...` exits 0 | **PASS** |
| Vector table derivation | 24 cells ($6 \times 4$) derived from assertions | All 24 cells derived; 0 un-derivable; 0 inferred | **PASS** |
| Barrier & hang audit | No failing leg relies on timeout or deadlock | All failures are clean early exception raises | **PASS** |

---

## 2. Frozen Vector Derivation Matrix (24 Cells)

| Case | Leg | Frozen | Observed | Grader Anchors | Case Anchors | Verdict & Derivation Summary | Confidence |
|---|---|---|---|---|---|---|---|
| `q1-ref` | `exists` | P | P | L24–28 | L1–65 | File `/app/pipeline_parallel.py` exists (65 lines); L26 passes. | **Derived** |
| `q1-ref` | `no_hooks` | P | P | L36–43 | L1–65 | Neither `"register_forward_hook"` nor `"register_full_backward_hook"` present; L38, L41 pass. | **Derived** |
| `q1-ref` | `ws1` | P | P | L91–168, L178 | L13–65 | All 4 layers on rank 0. All 4 forwards run before backwards. `num_layers = 8 <= 9` (L144). AFAB check (L153–158) passes. Activations & grads match ref atol 1e-5 (L160–166). Barrier (L168) exits 0. | **Derived** |
| `q1-ref` | `ws2` | P | P | L91–168, L178 | L13–65 | Rank 0: layers 0..1 (`num_layers = 4 <= 5`). Rank 1: layers 2..3 (`num_layers = 5 <= 5`). Both pass L144. P2P blocking send/recv deadlock-free. Gradients match ref. Barrier (L168) exits 0. | **Derived** |
| `q2-none` | `exists` | F | F | L24–28 | None | File `/app/pipeline_parallel.py` does not exist; L26 raises `AssertionError`. | **Derived** |
| `q2-none` | `no_hooks` | F | F | L36–37 | None | `with open(...)` at L36 raises `FileNotFoundError: [Errno 2]`. | **Derived** |
| `q2-none` | `ws1` | F | F | L93, L178 | None | Worker 0 raises `ModuleNotFoundError` on import at L93 before process group setup; `mp.spawn` raises `ProcessRaisedException`. | **Derived** |
| `q2-none` | `ws2` | F | F | L93, L178 | None | Workers 0 and 1 raise `ModuleNotFoundError` at L93; `mp.spawn` raises `ProcessRaisedException`. | **Derived** |
| `q3-stub` | `exists` | P | P | L24–28 | L1–5 | File `/app/pipeline_parallel.py` exists (5 lines); L26 passes. | **Derived** |
| `q3-stub` | `no_hooks` | P | P | L36–43 | L1–5 | Hook registration literals absent; L38, L41 pass. | **Derived** |
| `q3-stub` | `ws1` | F | F | L140, L178 | L4–5 | L140 calls `train_step_pipeline_afab()`; case L5 immediately raises `NotImplementedError`; `mp.spawn` raises `ProcessRaisedException`. | **Derived** |
| `q3-stub` | `ws2` | F | F | L140, L178 | L4–5 | Workers 0 and 1 raise `NotImplementedError` at L140; neither reaches barrier (L168); `mp.spawn` raises `ProcessRaisedException`. | **Derived** |
| `q4-hooks-noop` | `exists` | P | P | L24–28 | L1–65 | File exists (65 lines); L26 passes. | **Derived** |
| `q4-hooks-noop` | `no_hooks` | F | F | L36–40 | L30 | Case L30 contains `model.model.norm.register_forward_hook(...)`; literal present; L38 fails with `AssertionError`. | **Derived** |
| `q4-hooks-noop` | `ws1` | P | P | L91–168, L178 | L13–65 | Hook returns `None` (PyTorch leaves output unchanged). Numerics, layer count ($8 \le 9$, L144), AFAB ordering (L153–158), tolerances (L160–166), and barrier (L168) pass. | **Derived** |
| `q4-hooks-noop` | `ws2` | P | P | L91–168, L178 | L13–65 | No numerical effect. Rank 0 ($4 \le 5$) and Rank 1 ($5 \le 5$) pass L144. AFAB ordering, tolerances, and `dist.barrier()` (L168) pass on both ranks. | **Derived** |
| `q5-full-model` | `exists` | P | P | L24–28 | L1–37 | File exists (37 lines); L26 passes. | **Derived** |
| `q5-full-model` | `no_hooks` | P | P | L36–43 | L1–37 | No hook registration literals; L38, L41 pass. | **Derived** |
| `q5-full-model` | `ws1` | P | P | L91–168, L178 | L22–37 | Single rank runs all layers on 4 microbatches. `num_layers = 8 <= 9` (L144). All forwards precede backwards (L153–158). Tolerances match ref; barrier passes. | **Derived** |
| `q5-full-model` | `ws2` | F | F | L142–146, L178 | L22–37 | Without partitioning, both ranks run all 8 modules (`num_layers = 8`). Max allowed at ws2 (L144) is `((4 + 4) // 2 + 1) = 5`. Both ranks raise `AssertionError: Rank {rank} has too many layers: 8` at L144 before barrier (L168). `mp.spawn` raises `ProcessRaisedException`. | **Derived** |
| `q6-unscaled-loss` | `exists` | P | P | L24–28 | L1–65 | File exists (65 lines); L26 passes. | **Derived** |
| `q6-unscaled-loss` | `no_hooks` | P | P | L36–43 | L1–65 | No hook registration literals; L38, L41 pass. | **Derived** |
| `q6-unscaled-loss` | `ws1` | F | F | L160–166, L178 | L46–50 | Cross-entropy loss computed without `/ m` (case L46–50). Forward activations match ref, but backward gradients are 4x reference. L161 `torch.allclose` fails; L163 raises `AssertionError`. `mp.spawn` raises `ProcessRaisedException`. | **Derived** |
| `q6-unscaled-loss` | `ws2` | F | F | L160–166, L178 | L46–65 | Rank 1 computes loss without `/ m` (4x grad) and sends 4x grad back to Rank 0 (L65). Gradients on both ranks are 4x reference. Both ranks fail `torch.allclose` at L161 and raise `AssertionError` at L163 before barrier (L168). `mp.spawn` raises `ProcessRaisedException`. | **Derived** |

---

## 3. Grader Mechanics & Special Derivations

### The Layer-Count Assertion at Line 144
```python
assert 0 < num_layers <= ((4 + config.num_hidden_layers) // world_size + 1), (
    f"Rank {rank} has too many layers: {num_layers}"
)
```
- Modules hooked (L61–89): `embed_tokens`, `rotary_emb`, 4 decoder layers, `norm`, `lm_head` (total 8 modules).
- For `world_size = 1`: `(4 + 4) // 1 + 1 = 9`. $0 < 8 \le 9 \implies$ **PASS**.
- For `world_size = 2`: `(4 + 4) // 2 + 1 = 5`.
  - In `q1-ref` and `q4-hooks-noop`: Rank 0 runs 4 modules ($4 \le 5$); Rank 1 runs 5 modules ($5 \le 5$) $\implies$ **PASS**.
  - In `q5-full-model`: Both ranks run all 8 modules ($8 > 5$) $\implies$ **FAIL** on both ranks simultaneously.

### The `mp.spawn` Failure Path
- `mp.spawn(fn, args=(world_size,), nprocs=world_size, join=True)` (L178) executes each process inside `torch.multiprocessing.spawn._wrap`.
- When an assertion fails or an unhandled exception is raised in any worker process, `mp.spawn` intercepts the error, terminates sibling workers, and raises `torch.multiprocessing.spawn.ProcessRaisedException`.
- Pytest catches `ProcessRaisedException` as a testcase failure and emits `<failure>` in `junit.xml`.

---

## 4. Barrier, Hang, and Timeout Analysis

1. **Un-derivable values:** **0**. All 24 outcomes are cleanly derived from code.
2. **Barrier dependencies in passing cases:**
   - `q1-ref` [ws2] and `q4-hooks-noop` [ws2] execute `_cleanup_process_group` (L168), which invokes `dist.barrier()`. Successful termination depends on both ranks completing their forward/backward loops without deadlock and meeting at this barrier.
   - P2P communication in `q1-ref` / `q4-hooks-noop` uses blocking `dist.send`/`dist.recv` (lines 43, 55, 62, 65). Order and count match exactly (4 forward sends, 4 backward sends).
3. **Absence of deadlocks in failing cases:**
   - `q2-none` [ws1, ws2] fails on import (L93), before `_setup_process_group` (L95).
   - `q3-stub` [ws1, ws2] fails on schedule entry (L140); neither rank reaches L168.
   - `q5-full-model` [ws2] fails at line 144 on **both** ranks before reaching line 168.
   - `q6-unscaled-loss` [ws2] fails at line 163 on **both** ranks before reaching line 168.
   - Consequently, none of the failing cases hang or rely on the 900s timeout bound; each fails in $\sim 5$ seconds.

---

## 5. Artifacts Written

1. `.ufo/waves/round-67/w1/TensorRecon/recon.md` (Detailed 24-row derivation matrix and grader analysis).
2. `.ufo/waves/round-67/w1/TensorRecon/check-receipt.txt` (Observed output of `--check-receipt`).
3. `.ufo/waves/round-67/w1/TensorRecon/sha256-crosscheck.txt` (Observed sha256 hashes of all audited artifacts).
4. `.ufo/waves/round-67/w1/TensorRecon.md` (This report).
