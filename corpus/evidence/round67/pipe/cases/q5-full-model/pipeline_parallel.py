"""No-partition mutant (R67-C1 case q5-full-model): every rank runs the whole model, no communication.

Correct numerics on one rank; at world size 2 each rank holds all eight layer entries, so the grader's
layer-count assertion (<= 5 per rank) fails on both ranks before any barrier.
"""

import torch.nn.functional as F


def _decoder(model, hidden):
    import torch

    seq = hidden.shape[1]
    pos = torch.arange(seq, device=hidden.device).unsqueeze(0)
    pe = model.model.rotary_emb(hidden, position_ids=pos)
    for layer in model.model.layers:
        out = layer(hidden, attention_mask=None, position_ids=pos, position_embeddings=pe)
        hidden = out[0] if isinstance(out, (tuple, list)) else out
    return hidden


def train_step_pipeline_afab(model, inputs, targets, device, dtype):
    m = len(inputs)
    losses = []
    for i in range(m):
        h = model.model.embed_tokens(inputs[i].to(device)).to(dtype)
        out = _decoder(model, h)
        logits = model.lm_head(model.model.norm(out))
        losses.append(
            F.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                targets[i].to(device).reshape(-1),
                ignore_index=-100,
            ) / m
        )
    for loss in losses:
        loss.backward()
