"""AFAB pipeline-parallel training step for LlamaForCausalLM (labrat literal-construction control).

Purpose: implement the construction named in the seat item as literally as it can run at world
size 1 — the decoder split at a layer boundary (layers [0,2) / [2,4)), microbatch 0 forward through
the first chunk only and backwarded at once, before the last layers first run forward. The second
chunk then runs forward for every microbatch, so `model.layers.2.fwd` really is first inserted
after a `.bwd` key.

Expected observable (not asserted here; the grader decides): the AFAB raise sits at
`model.layers.2.fwd`, but the grader's per-key loop compares the values of every key inserted
before it, and the truncated backward makes `model.layers.1.bwd` differ from the full-model
reference. This case records where the grader actually stops.

World size 1 only. rotary_emb is called exactly once per microbatch, so the chunk split does not
multiply its hook count.
"""

import torch
import torch.distributed as dist
import torch.nn.functional as F


def _partition(n_layers, rank, world):
    per = (n_layers + world - 1) // world
    lo = min(rank * per, n_layers)
    hi = min(lo + per, n_layers)
    return lo, hi


def _position_embeddings(model, hidden):
    seq = hidden.shape[1]
    pos = torch.arange(seq, device=hidden.device).unsqueeze(0)
    return pos, model.model.rotary_emb(hidden, position_ids=pos)


def _decode_range(model, hidden, lo, hi, pos, pe):
    for layer in model.model.layers[lo:hi]:
        out = layer(hidden, attention_mask=None, position_ids=pos, position_embeddings=pe)
        hidden = out[0] if isinstance(out, (tuple, list)) else out
    return hidden


def _truncated_loss(model, out, targets_i, m, device):
    logits = F.linear(out, model.lm_head.weight)
    return F.cross_entropy(
        logits.reshape(-1, logits.size(-1)),
        targets_i.to(device).reshape(-1),
        ignore_index=-100,
    ) / m


def train_step_pipeline_afab(model, inputs, targets, device, dtype):
    rank = dist.get_rank()
    world = dist.get_world_size()
    if world != 1:
        raise NotImplementedError("labrat literal-construction control is world-size-1 only")
    lo, hi = _partition(len(model.model.layers), rank, world)
    m = len(inputs)
    # microbatch 0: first chunk forward, loss, backward — before any key of layers 2..3 exists
    h = model.model.embed_tokens(inputs[0].to(device)).to(dtype)
    pos, pe = _position_embeddings(model, h)
    out_a = _decode_range(model, h, 0, 2, pos, pe)
    _truncated_loss(model, out_a, targets[0], m, device).backward()
    # second chunk forward for microbatch 0: layers.2.fwd / layers.3.fwd are first inserted here
    _decode_range(model, out_a.detach(), 2, hi, pos, pe)
    for i in range(1, m):
        h = model.model.embed_tokens(inputs[i].to(device)).to(dtype)
        pos, pe = _position_embeddings(model, h)
        out_a = _decode_range(model, h, 0, 2, pos, pe)
        _truncated_loss(model, out_a, targets[i], m, device).backward()
        _decode_range(model, out_a.detach(), 2, hi, pos, pe)
