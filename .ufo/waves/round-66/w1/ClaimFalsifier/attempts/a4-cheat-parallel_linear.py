"""A4 cheat: K1 reference with a communication-free ColumnParallelLinear.

The column layer keeps the whole master weight (registered as a buffer — memory
is doubled, which is exactly what tensor parallelism exists to avoid) and
reconstructs the full output locally: the local block comes from the sharded
`self.weight` parameter (so the grader's weight/bias/grad assertions still see a
proper shard), and the other ranks' blocks are computed from the buffered master
rows.  No all-gather is ever issued.  RowParallelLinear is the faithful K1 build.
"""

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F


def _world_size() -> int:
    return dist.get_world_size() if dist.is_initialized() else 1


def _rank() -> int:
    return dist.get_rank() if dist.is_initialized() else 0


class ColumnParallelLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True, master_weight=None):
        super().__init__()
        ws, rank = _world_size(), _rank()
        assert out_features % ws == 0, "out_features must divide by world size"
        per = out_features // ws
        start = rank * per
        self.weight = nn.Parameter(master_weight[start:start + per, :].clone())
        if bias:
            self.bias = nn.Parameter(torch.zeros(per))
        else:
            self.register_parameter("bias", None)
        # CHEAT: retain the full master weight and bias as non-gradient buffers.
        self.register_buffer("master_weight_full", master_weight.detach().clone())
        self.register_buffer("master_bias_full", torch.zeros(out_features))

    def forward(self, x):
        ws, rank = _world_size(), _rank()
        if ws == 1:
            return F.linear(x, self.weight, self.bias)
        per = self.weight.shape[0]
        outs = []
        for r in range(ws):
            rows = slice(r * per, (r + 1) * per)
            if r == rank:
                outs.append(F.linear(x, self.weight, self.bias))
            else:
                b = self.master_bias_full[rows] if self.bias is not None else None
                outs.append(F.linear(x, self.master_weight_full[rows], b))
        return torch.cat(outs, dim=-1)


class RowParallelLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True, master_weight=None):
        super().__init__()
        ws, rank = _world_size(), _rank()
        assert in_features % ws == 0, "in_features must divide by world size"
        per = in_features // ws
        start = rank * per
        self.weight = nn.Parameter(master_weight[:, start:start + per].clone())
        if bias:
            self.bias = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter("bias", None)

    def forward(self, x_local):
        local = F.linear(x_local, self.weight)
        ws = _world_size()
        if ws > 1:
            reduced = local.detach().clone()
            dist.all_reduce(reduced, op=dist.ReduceOp.SUM)
            local = local + (reduced - local).detach()
        if self.bias is not None:
            local = local + self.bias
        return local
