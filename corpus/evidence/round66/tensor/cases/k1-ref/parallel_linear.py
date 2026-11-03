"""Compliant tensor-parallel linear layers (round 66, case K1, reference build).

Built by the lane for the offline grader probe; the grader imports it as /app/parallel_linear.py.
Column: each rank holds rows [rank*out/ws, (rank+1)*out/ws) of the master weight; the output is
the concatenation of every rank's slice (all-gather, local tensor kept in the autograd graph).
Row: each rank holds columns [rank*in/ws, ...); partial products are summed across ranks
(all-reduce, local tensor kept in the autograd graph) and the full bias is added once.
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
        local = F.linear(x, self.weight, self.bias)
        ws = _world_size()
        if ws == 1:
            return local
        gathered = [torch.empty_like(local.detach()) for _ in range(ws)]
        dist.all_gather(gathered, local.detach().contiguous())
        gathered[_rank()] = local
        return torch.cat(gathered, dim=-1)


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
