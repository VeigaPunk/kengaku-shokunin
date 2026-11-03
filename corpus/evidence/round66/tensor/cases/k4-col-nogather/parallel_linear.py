"""Mutant K4 (round 66): identical to case K1 except ColumnParallelLinear.forward never gathers.

The rank returns only its own output slice. World size 1 is unaffected (no gather is needed);
world sizes 2 and 4 must fail. RowParallelLinear is the K1 build unchanged.
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

    def forward(self, x):
        return F.linear(x, self.weight, self.bias)


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
