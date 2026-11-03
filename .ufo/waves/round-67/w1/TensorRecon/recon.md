# R67-C1 Grader & Vector Table Reconnaissance (`recon.md`)

**Seat:** `TensorRecon` (Kengaku lane, round 67, wave 1).
**Scope:** Read-only derivation and audit of the frozen R67-C1 vector table against the pinned grader.
**Artifacts under audit:**
- Pinned grader: `corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py` (sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f`, 178 lines).
- Pinned probe & claims: `plans/round67_c1_pipeline_probe.py` (`FROZEN_TABLE`, `KEYS`, `key_of`, `check_receipt`), `plans/round-67-claims.md` (§R67-C1).
- Committed cases: `corpus/evidence/round67/pipe/cases/<case>/pipeline_parallel.py` (q1-ref, q3-stub, q4-hooks-noop, q5-full-model, q6-unscaled-loss; q2-none is empty `/app`).
- Committed receipt & junit: `corpus/evidence/round67/pipe/receipt.txt`, `receipt.junit/*.xml`.

---

## 1. Frozen Vector Derivation Matrix (24 cells: 6 cases x 4 legs)

| Case | Leg | Expected | Observed | Derivation & Line Anchors | Confidence |
|---|---|---|---|---|---|
| `q1-ref` | `exists` | **P** | P | Grader L24–28: Path `/app/pipeline_parallel.py` exists (65 lines). Assert at L26 passes. | **Derived** |
| `q1-ref` | `no_hooks` | **P** | P | Grader L36–43: asserts `"register_forward_hook"` (L38) & `"register_full_backward_hook"` (L41) absent. Case L1–65 contains neither. | **Derived** |
| `q1-ref` | `ws1` | **P** | P | Grader L91–168, L178: Rank 0 partitions all 4 layers (Case L13–17, 34). Forward microbatches 0..3 execute embed, decoder, norm, lm_head, loss/4 (Case L38–53). Backward runs loss.backward() (Case L59). Grader layer count 8 <= 9 (L144), AFAB forward-before-backward holds (L153–158), outputs match reference atol 1e-5 (L160–166), dist.barrier() (L168) succeeds. | **Derived** |
| `q1-ref` | `ws2` | **P** | P | Grader L91–168, L178: Rank 0 runs layers 0..1 (num_layers=4 <= 5 at L144); Rank 1 runs layers 2..3, norm, lm_head (num_layers=5 <= 5 at L144). P2P blocking send/recv (Case L43, 55, 62, 65) passes activations & gradients without deadlock. All forwards precede backwards on each rank (Grader L153–158). Tolerances match atol 1e-5 (L160–166). dist.barrier() (L168) cleanly exits. | **Derived** |
| `q2-none` | `exists` | **F** | F | Grader L24–28: File `/app/pipeline_parallel.py` does not exist in empty `/app`. L26 raises `AssertionError: File /app/pipeline_parallel.py does not exist`. | **Derived** |
| `q2-none` | `no_hooks` | **F** | F | Grader L36–37: `with open("/app/pipeline_parallel.py") as f:` raises `FileNotFoundError: [Errno 2] No such file or directory`. Pytest records failure. | **Derived** |
| `q2-none` | `ws1` | **F** | F | Grader L93: `from pipeline_parallel import train_step_pipeline_afab` raises `ModuleNotFoundError` inside worker process 0 before process group init (L95). Worker terminates; mp.spawn raises `ProcessRaisedException`. Pytest records failure. | **Derived** |
| `q2-none` | `ws2` | **F** | F | Grader L93: Both worker processes (0 and 1) raise `ModuleNotFoundError` on import at L93. mp.spawn catches worker failure and raises `ProcessRaisedException`. Pytest records failure. | **Derived** |
| `q3-stub` | `exists` | **P** | P | Grader L24–28: File `/app/pipeline_parallel.py` exists (5 lines). Assert at L26 passes. | **Derived** |
| `q3-stub` | `no_hooks` | **P** | P | Grader L36–43: Substrings `"register_forward_hook"` and `"register_full_backward_hook"` absent from stub code. Assertions pass. | **Derived** |
| `q3-stub` | `ws1` | **F** | F | Grader L91–140: Setup & ref model run. L140 calls `train_step_pipeline_afab()`. Case L5 raises `NotImplementedError("stub: pipeline schedule not implemented")`. Worker 0 terminates; mp.spawn raises `ProcessRaisedException`. | **Derived** |
| `q3-stub` | `ws2` | **F** | F | Grader L91–140: Both workers 0 and 1 reach L140 and immediately raise `NotImplementedError` at Case L5. mp.spawn raises `ProcessRaisedException`. Neither rank reaches barrier. | **Derived** |
| `q4-hooks-noop` | `exists` | **P** | P | Grader L24–28: File exists (65 lines). Assert at L26 passes. | **Derived** |
| `q4-hooks-noop` | `no_hooks` | **F** | F | Grader L36–40: Asserts `"register_forward_hook" not in code`. Case L30 contains `model.model.norm.register_forward_hook(lambda module, args, output: None)`. Literal present; L38 fails with `AssertionError`. | **Derived** |
| `q4-hooks-noop` | `ws1` | **P** | P | Grader L91–168: Hook registered at Case L30 returns `None`, which under PyTorch semantics preserves norm output unchanged. Numerics, layer count (8 <= 9, L144), AFAB ordering (L153–158), tolerance check (L160–166), and barrier (L168) match `q1-ref` and pass. | **Derived** |
| `q4-hooks-noop` | `ws2` | **P** | P | Grader L91–168: Hook has no numerical effect. Rank 0 (num_layers=4 <= 5) and Rank 1 (num_layers=5 <= 5) pass L144. AFAB ordering (L153–158), numerical tolerances (L160–166), and dist.barrier() (L168) pass on both ranks. | **Derived** |
| `q5-full-model` | `exists` | **P** | P | Grader L24–28: File exists (37 lines). Assert at L26 passes. | **Derived** |
| `q5-full-model` | `no_hooks` | **P** | P | Grader L36–43: No hook registration literals in code. Assertions at L38 & L41 pass. | **Derived** |
| `q5-full-model` | `ws1` | **P** | P | Grader L91–168: Single rank runs all layers on 4 microbatches (Case L23–37). Layer count num_layers=8 <= 9 (L144). All forwards precede backwards (Case L25–35 vs L36–37; Grader L153–158 passes). Numerics match reference (L160–166). Teardown passes. | **Derived** |
| `q5-full-model` | `ws2` | **F** | F | Grader L142–146: Without partition, both rank 0 and rank 1 execute all layers. On both ranks, pipeline_dict accumulates 8 forward modules. Max allowed at ws2 (L144) is `((4 + 4) // 2 + 1) = 5`. Both ranks fail L144 with `AssertionError: Rank {rank} has too many layers: 8` before reaching dist.barrier() (L168). mp.spawn raises `ProcessRaisedException`. | **Derived** |
| `q6-unscaled-loss` | `exists` | **P** | P | Grader L24–28: File exists (65 lines). Assert at L26 passes. | **Derived** |
| `q6-unscaled-loss` | `no_hooks` | **P** | P | Grader L36–43: No hook registration literals. Assertions at L38 & L41 pass. | **Derived** |
| `q6-unscaled-loss` | `ws1` | **F** | F | Grader L91–166: Case L46–50 calculates cross-entropy loss without dividing by microbatch count m=4 (reference divided by 4 at L132–133). Forward activations match, but backward gradients are 4x reference. Grader L161 `torch.allclose(atol=1e-5)` fails on backward keys; L163 raises `AssertionError: Rank 0 mismatch at {key}`. mp.spawn raises `ProcessRaisedException`. | **Derived** |
| `q6-unscaled-loss` | `ws2` | **F** | F | Grader L91–166: Rank 1 computes loss without `/ m`, producing 4x gradients. Rank 1 sends 4x grad back to Rank 0 (Case L65). Both ranks compute backward with 4x scaled gradients. Both ranks fail `torch.allclose` at L161 and raise `AssertionError` at L163 before reaching dist.barrier() (L168). mp.spawn raises `ProcessRaisedException`. | **Derived** |

---

## 2. Derivation Mechanics & Grader Analysis

### A. The Pinned Grader Structure (`test_outputs.py`)
1. **`test_pipeline_parallel_exists` (L19–28):** Pure filesystem check for `/app/pipeline_parallel.py`.
2. **`test_no_hooks_in_pipeline_parallel` (L31–43):** Static source text check against literal tokens `"register_forward_hook"` (L38) and `"register_full_backward_hook"` (L41).
3. **`test_pipeline_parallel` (L171–178):** Parametrized across `world_size = [1, 2]`. Invokes `_test_pipeline_parallel` via `mp.spawn(..., nprocs=world_size, join=True)`.
   - Setup: Initializes Gloo distributed process group on `localhost:12355` (L46–52).
   - Reference run (L121–135): Runs 4 microbatches sequentially on `ref_model`, accumulating gradients with `loss / grad_acc_steps` (`grad_acc_steps = 4`). Hooks record activations to `ref_dict` (L61–89).
   - Candidate run (L138–140): Hooks registered to `pipeline_dict`. Calls `train_step_pipeline_afab(model, pipeline_inputs, pipeline_targets, device, dtype)`.
   - Hooked modules (8 total): `model.embed_tokens`, `model.rotary_emb`, `model.layers.0`, `model.layers.1`, `model.layers.2`, `model.layers.3`, `model.norm`, and `lm_head`.

### B. The World Size 2 Layer-Count Assertion (L144)
Grader line 144 asserts:
```python
assert 0 < num_layers <= ((4 + config.num_hidden_layers) // world_size + 1), (
    f"Rank {rank} has too many layers: {num_layers}"
)
```
- With `config.num_hidden_layers = 4`:
  - For `world_size = 1`: ceiling is `(4 + 4) // 1 + 1 = 9`. All 8 modules fit on one rank ($0 < 8 \le 9$).
  - For `world_size = 2`: ceiling is `(4 + 4) // 2 + 1 = 4 + 1 = 5`.
- In a partitioned model (`q1-ref`, `q4-hooks-noop`):
  - Rank 0 executes `embed_tokens`, `rotary_emb`, `layers.0`, `layers.1` $\implies num\_layers = 4 \le 5$.
  - Rank 1 executes `rotary_emb`, `layers.2`, `layers.3`, `norm`, `lm_head` $\implies num\_layers = 5 \le 5$.
- In `q5-full-model`:
  - Neither rank partitions. Both rank 0 and rank 1 execute all 8 modules $\implies num\_layers = 8$.
  - Both ranks fail L144 simultaneously: `assert 0 < 8 <= 5` raises `AssertionError`.
  - Critically, this assertion failure occurs **before** `_cleanup_process_group` (L168). Neither rank reaches `dist.barrier()`.

### C. The `mp.spawn` Failure Path
Under `torch.multiprocessing.spawn`:
- Worker subprocesses are spawned via `_wrap(fn, i, args)`.
- If a worker raises an unhandled exception (`ModuleNotFoundError`, `NotImplementedError`, or `AssertionError`):
  1. The worker's traceback is serialized back to the parent process.
  2. The parent detects worker termination and raises `torch.multiprocessing.spawn.ProcessRaisedException`.
  3. Pytest catches `ProcessRaisedException` and records a `<failure>` element in `junit.xml`.
  4. The probe parses `junit.xml` via `junit_outcomes()`, mapping `<failure>` to `F`.

---

## 3. Audit of Frozen Values, Barriers, and Timeouts

### A. Un-derivable Frozen Values
- **Flagged values:** **None**. Every single cell of the 24 cells ($6 \times 4$) is strictly derived from the grader source code, case implementations, and Python/PyTorch runtime semantics.
- Confidence for all 24 cells: **Derived**.

### B. Barrier, Hang, and Timeout Dependencies
1. **Barrier dependencies in passing cases:**
   - `q1-ref` [ws2] and `q4-hooks-noop` [ws2]: Outcome `P` depends on:
     - Deadlock-free point-to-point communication: Rank 0 sends 4 forward activations and waits for 4 backward gradients; Rank 1 waits for 4 forward activations and sends 4 backward gradients. Any imbalance or deadlock would hang the subprocess until the 900s timeout.
     - Final synchronization: Both ranks must reach L168 and cleanly execute `dist.barrier()`.
2. **Absence of barrier deadlocks in failing cases:**
   - `q2-none` [ws1, ws2]: Fails on import at L93, prior to `_setup_process_group` (L95). No distributed runtime or barrier is ever initialized.
   - `q3-stub` [ws1, ws2]: Fails at L140 via immediate `NotImplementedError`. Neither rank reaches L168.
   - `q5-full-model` [ws2]: Fails at L144 (`num_layers <= 5`) on **both** ranks. Because both ranks raise `AssertionError` at L144, neither enters L168 (`dist.barrier()`). The failure does not depend on a barrier deadlock or timeout; it terminates in ~5 seconds.
   - `q6-unscaled-loss` [ws2]: Fails at L161–163 on **both** ranks due to unscaled backward gradients propagating across the pipeline boundary. Both ranks raise `AssertionError` before L168.
3. **Timeout dependence:**
   - No leg depends on the 900s timeout bound. All 4 failing cases (`q2-none`, `q3-stub`, `q5-full-model`, `q6-unscaled-loss`) fail via deterministic exception raises within 5 seconds per testcase.

---

## 4. Verification & Receipt Cross-Checks

1. **Receipt verification command:**
   ```bash
   python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt
   ```
   - Observed output:
     ```
     CHECK ok cases=6
     PREDICATE R67-C1 pass
     ```
   - Exit code: `0`.
2. **Byte & Sha256 Identity:**
   - Pinned grader: `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f` (matches `SHA256SUMS` line 169 and `receipt.txt` line 4).
   - Committed probe: `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836` (matches `receipt.txt` line 3).
   - All 6 case shas and 6 junit XML shas in `corpus/evidence/round67/pipe/receipt.txt` match committed file bytes exactly (`sha256-crosscheck.txt`).
