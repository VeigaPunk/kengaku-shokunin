# AFAB labrat — round 67 w1, seat AfabLab

Date 2026-11-03. Host Arch Linux, 32 cores. Grader under test:
`corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py`,
sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f` (frozen).
Environment (read-only for this seat): venv-pipe, python 3.14.8, torch 2.15.0+cpu,
transformers 5.22.1, pytest 9.2.0. No tool installed, no network used, no frozen file touched.

## Hypothesis (H-AFAB)

At world size 1 the grader's AFAB check (`test_outputs.py:152-157`, raise at `:156`) fires only
when a key ending `.fwd` is *first inserted* into the per-rank hook dictionary after a key ending
`.bwd`. It therefore cannot distinguish a one-forward-one-backward loop (1F1B) from the
all-forward-all-backward (AFAB) reference. Prediction: a 1F1B variant passes the ws1 leg (P).

## Cases written (all world-size-1 only; copies in this seat dir)

| case | change vs frozen `q1-ref` | sha256 |
|---|---|---|
| `case-1f1b` | loop order only: forward and backward of each microbatch in turn (`stored` list removed) | `573d5cc35a1ca627a2ac33e282d20fd65cb61349a274582af815534b227ce1c5` |
| `case-ctl` | detector-positive control: microbatch 0's head computed as `F.linear(..., lm_head.weight)` (module not entered), microbatch 0 backwarded, then one `lm_head` module call → `lm_head.fwd` first inserted after `model.norm.bwd`; count kept at 4 | `4fdfb45824ff4eb223de51ad0c749e577695ff1335fbeb0636e10f749a3b4957` |
| `case-ctl2` | the seat item's literal construction: decoder split at a layer boundary (layers [0,2) / [2,4)), microbatch 0 forward through the first chunk only and backwarded at once before layers 2..3 first run forward | `4ff7dc2fb76b52c1c230ae2075f3479ad235aaa42508230c1720c83a40d0bb73` |

`diff -u q1-ref case-1f1b` touches only the module docstring, the `stored` list and the position of
the backward call; `_partition`, `_decoder`, the embedding/recv code and the `/ m` loss scaling are
byte-identical.

## Command (one shape, four invocations)

Copied from `plans/round67_c1_pipeline_probe.py::run_case`, with the `/app` bind swapped to the case
dir, the `/ctl` bind to this seat's ctl dir, and `-k 'test_pipeline_parallel and 1'` added; wrapped in
the port lock. The four invocations differ only in the `--ro-bind <case> /app` and
`--bind <ctl> /ctl` arguments.

    flock /home/vgpnk/.local/share/kengaku-r67/port-12355.lock bwrap --die-with-parent \
      --unshare-net --unshare-pid --ro-bind /usr /usr --symlink usr/bin /bin \
      --symlink usr/sbin /sbin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
      --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp \
      --ro-bind /home/vgpnk/.local/share/kengaku-r67/venv-pipe /home/vgpnk/.local/share/kengaku-r67/venv-pipe \
      --dir /app --ro-bind <case-dir> /app \
      --dir /tests --ro-bind <grader-path> /tests/test_outputs.py \
      --bind <ctl-dir> /ctl --chdir /app --clearenv \
      --setenv PATH /usr/bin:/bin --setenv HOME /tmp --setenv PYTHONDONTWRITEBYTECODE 1 \
      --setenv PYTHONNOUSERSITE 1 --setenv HF_HUB_OFFLINE 1 --setenv TRANSFORMERS_OFFLINE 1 \
      /home/vgpnk/.local/share/kengaku-r67/venv-pipe/bin/python -m pytest /tests/test_outputs.py \
      -p no:cacheprovider -q --junitxml=/ctl/junit.xml -k 'test_pipeline_parallel and 1'

`-k 'test_pipeline_parallel and 1'` selects only the ws1 leg: `pytest -q --collect-only -k
'test_pipeline_parallel and 1'` on an equivalent parametrised stub printed
`test_k.py::test_pipeline_parallel[1]` / `1/2 tests collected (1 deselected)`, rc 0
(`kfilter-check.txt`).

## Results (rc is the flock/bwrap/pytest rc; junit is `/ctl/junit.xml`, copied here)

| run | `/app` | rc | junit `test_pipeline_parallel[1]` | failure site |
|---|---|---|---|---|
| `1f1b` | `S/case-1f1b` | **0** | **P** (4.241 s; suite 7.454 s) | — (`1 passed, 3 deselected in 7.45s`) |
| `ref` | committed `…/pipe/cases/q1-ref` | **0** | **P** (4.328 s; suite 7.421 s) | — |
| `ctl` | `S/case-ctl` | **1** | **F** (4.362 s; suite 7.530 s) | `test_outputs.py:156` — `AssertionError: AFAB violation: found forward after backward at lm_head.fwd` |
| `ctl2` | `S/case-ctl2` | **1** | **F** (4.246 s; suite 7.414 s) | `test_outputs.py:163` — `AssertionError: Rank 0 mismatch at model.layers.1.bwd, microbatch 0, max diff=0.00874430313706398` |

junit shas: `1f1b` `ee4f88bc6a50c84ff3fa5eb60de59f52f460750048f53bf4db37be5fb4c0b937`;
`ref` `508dd59cc9517958dd32a63305dc7dc84f1900ba08c8a6db5f41a1d3ca30d4a5`;
`ctl` `d95c561468999cfb90de09fe4fea80feef0461d4060603b88864a61f343a0fcd`;
`ctl2` `1516607af3011a2afa479e81baa350ac0dda6910fc763b03d19b3dd5bf4cfd9a`.

## Mechanism receipt (why the two schedules are indistinguishable to the hook dict)

`hookorder.py` (copy of this seat) re-registers the grader's hook code verbatim
(`test_outputs.py:60-89`) on the grader's `LlamaConfig` and runs three ws1 schedules without a
process group; it prints the key insertion order, the per-key counts and where the grader's AFAB
predicate would fire (`hookorder.txt`, rc 0):

- `afab/q1-ref`: 15 keys, `model.embed_tokens.fwd model.rotary_emb.fwd model.layers.0.fwd …
  lm_head.fwd lm_head.bwd model.norm.bwd … model.embed_tokens.bwd`; counts all 4;
  `afab_would_fire_at: None`.
- `1f1b`: **identical key order and identical counts**; `afab_would_fire_at: None`.
- `ctl`: `… model.norm.fwd model.norm.bwd model.layers.3.bwd … model.embed_tokens.bwd lm_head.fwd
  lm_head.bwd`; `lm_head.fwd=4`, `lm_head.bwd=3`; `afab_would_fire_at: lm_head.fwd`.

The dictionary records the order in which each *name* is first created, not the call sequence, so
interleaving forwards and backwards within a rank leaves it unchanged as long as every hooked
module is first entered during microbatch 0's forward — which both schedules satisfy.

## Verdict

- **H-AFAB: confirmed on the ws1 leg with the frozen grader.** The 1F1B variant passes ws1
  (rc 0, junit P), with the same key order and counts as the AFAB reference; the grader cannot tell
  the two apart at world size 1.
- **Control: written and run; the AFAB check is reachable but only by a forward-first-entry
  substitution.** `case-ctl` fires the raise at `:156` on `lm_head.fwd`; `case-ctl2` (the seat item's
  literal split-decoder construction) does **not** reach the raise — the per-key value comparison at
  `:163` fails first on `model.layers.1.bwd`, because a truncated backward can never match the
  full-model gradient. So at ws1 the detector is not dead code, but it is only sensitive to which
  module is entered late, not to phase separation.
- Not generalised beyond ws1 and this grader. ws2 was deliberately not run.

## Named limitations

- ws1 only: rank 0 is both the first and the last stage, so no `dist.send`/`dist.recv` executes; the
  non-last-rank branch of `case-1f1b` is untested (at world size >1 it would be a lockstep
  stage-by-stage schedule, not a pipelined one).
- `case-ctl` is a detector control, not a plausible implementation: it mixes a functional and a
  module call of `lm_head` on purpose. `case-ctl2` substitutes a truncated head to create the
  backward-before-last-forward order.
- The 1F1B pass also relies on the backward values arriving in the reference's microbatch order
  (mb0…mb3); both schedules back-propagate in that order. Whether an out-of-order backward would
  pass was not run (`[INFERENCE]`: it would fail the value comparison, not the AFAB check).
- One model configuration only (the grader's: hidden 512, 4 decoder layers, 4 microbatches; the
  ws1 layer-count bound is 9 and both schedules report 8 `.fwd` keys).

## Files in this seat dir

`case-1f1b-pipeline_parallel.py`, `case-ctl-pipeline_parallel.py`, `case-ctl2-pipeline_parallel.py`,
`run_ws1.py` (runner: `sha256 3142c2bb90173fb1d6a4d3398603c4dfa3e8370d32677e63df0507250761ec0a`),
`hookorder.py` (`d71ccd7789483efbf51715eaec838b5a681a57d38e0612b72a0028191b5ad423`),
`hookorder.txt`, `kfilter-check.txt`, `1f1b-junit.xml`, `1f1b-log.txt`, `ref-junit.xml`,
`ref-log.txt`, `ctl-junit.xml`, `ctl-log.txt`, `ctl2-junit.xml`, `ctl2-log.txt`,
`frozen-path-status.txt`. Scratch `S/AfabLab` deleted after these copies.
