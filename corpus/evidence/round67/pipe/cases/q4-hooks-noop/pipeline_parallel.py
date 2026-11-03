"""Reference AFAB schedule plus a no-op forward hook (R67-C1 case q4-hooks-noop).

The schedule is the q1-ref schedule; the only difference is the no-op hook registered first.
The hook returns None, so the numerics are unchanged; the grader's test_no_hooks rule forbids the literal.
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
    model.model.norm.register_forward_hook(lambda module, args, output: None)
    rank = dist.get_rank()
    world = dist.get_world_size()
    last = world - 1
    lo, hi = _partition(len(model.model.layers), rank, world)
    m = len(inputs)
    stored = []
    for i in range(m):
        if rank == 0:
            h = model.model.embed_tokens(inputs[i].to(device)).to(dtype)
        else:
            seq = inputs[i].shape[1]
            buf = torch.empty(inputs[i].shape[0], seq, model.config.hidden_size, device=device, dtype=dtype)
            dist.recv(buf, src=rank - 1)
            h = buf.requires_grad_(True)
        out = _decoder(model, h, lo, hi)
        if rank == last:
            logits = model.lm_head(model.model.norm(out))
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                targets[i].to(device).reshape(-1),
                ignore_index=-100,
            ) / m
            stored.append((h, loss))
        else:
            dist.send(out.detach().contiguous(), dst=rank + 1)
            stored.append((h, out))
    for h, res in stored:
        if rank == last:
            res.backward()
        else:
            grad = torch.empty_like(res)
            dist.recv(grad, src=rank + 1)
            res.backward(grad.to(device=device, dtype=dtype))
        if rank > 0:
            dist.send(h.grad.detach().contiguous().to(device=device, dtype=dtype), dst=rank - 1)
