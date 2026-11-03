"""Stub control (round 66, case K3): the module exists, the layers are not implemented.

Frozen as a negative control: the file-exists check passes, every layer test must fail.
"""


class ColumnParallelLinear:
    def __init__(self, in_features, out_features, bias=True, master_weight=None):
        raise NotImplementedError("ColumnParallelLinear is not implemented")


class RowParallelLinear:
    def __init__(self, in_features, out_features, bias=True, master_weight=None):
        raise NotImplementedError("RowParallelLinear is not implemented")
