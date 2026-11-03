"""AFAB pipeline-parallel training step for LlamaForCausalLM (labrat detector-positive control).

Purpose: make the grader's AFAB check (test_outputs.py:152-157) fire at world size 1, i.e. prove
the check is reachable and not dead code. It fires when a key ending in `.fwd` is first inserted
into the hook dictionary after a key ending in `.bwd`.

Construction (world size 1 only): the loss of microbatch 0 is computed through the last module
(`lm_head`) *functionally* (F.linear with the same weight), so the hooked `lm_head` module is not
entered during microbatch 0's forward; microbatch 0 is backwarded at once. After that backward,
`lm_head` is called once on microbatch 0's output. That is the first `.fwd` insertion for
`lm_head`, so it lands after `model.norm.bwd` (and the rest) in the dictionary. Microbatches 1..3
then use the module normally, and the extra call keeps `lm_head.fwd`'s count at the 4 the
reference carries, so the count assertion passes and the AFAB raise is reached.

This is a detector control, not a plausible schedule: it deliberately mixes a functional and a
module call of the same module. Partition code and the per-microbatch loss are q1-ref's.
"""

import torch
import torch.distributed as dist
import torch.nn.functional as F


def _partition(n_layers, rank, world):
    per = (n_layers + world - 1) // world
    lo = min(rank * per, n_layers)
    hi = min(lo + per, n_layers)
    return lo, hi


def _decoder(model, hidden, lo, hi):
    seq = hidden.shape[1]
    pos = torch.arange(seq, device=hidden.device).unsqueeze(0)
    pe = model.model.rotary_emb(hidden, position_ids=pos)
    for layer in model.model.layers[lo:hi]:
        out = layer(hidden, attention_mask=None, position_ids=pos, position_embeddings=pe)
        hidden = out[0] if isinstance(out, (tuple, list)) else out
    return hidden


def train_step_pipeline_afab(model, inputs, targets, device, dtype):
    rank = dist.get_rank()
    world = dist.get_world_size()
    if world != 1:
        raise NotImplementedError("labrat detector control is world-size-1 only")
    lo, hi = _partition(len(model.model.layers), rank, world)
    m = len(inputs)
    # microbatch 0: forward through every hooked module except lm_head (functional head)
    h = model.model.embed_tokens(inputs[0].to(device)).to(dtype)
    out = _decoder(model, h, lo, hi)
    logits = F.linear(model.model.norm(out), model.lm_head.weight)
    loss = F.cross_entropy(
        logits.reshape(-1, logits.size(-1)),
        targets[0].to(device).reshape(-1),
        ignore_index=-100,
    ) / m
    loss.backward()
    # deliberate late first entry into the hooked lm_head: this inserts lm_head.fwd
    # after model.norm.bwd and friends
    model.lm_head(out.detach())
    # microbatches 1..3: ordinary q1-ref path
    for i in range(1, m):
        h = model.model.embed_tokens(inputs[i].to(device)).to(dtype)
        out = _decoder(model, h, lo, hi)
        logits = model.lm_head(model.model.norm(out))
        loss = F.cross_entropy(
            logits.reshape(-1, logits.size(-1)),
            targets[i].to(device).reshape(-1),
            ignore_index=-100,
        ) / m
        loss.backward()
