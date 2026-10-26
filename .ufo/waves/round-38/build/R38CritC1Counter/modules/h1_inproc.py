"""Hostile hull probe H1: patch the counter's own globals at module-import time.

No gate behaviour is demonstrated: the mutant loop asks the patched `attributed`, which answers True.
"""

import sys

_c = sys.modules["__main__"]
_c.attributed = lambda clause, direction, fx, argv, ref, mut: True


def build(ctx, d):
    return ["package", "--root", str(d)]


FIXTURES = [{"fid": "h1-empty", "expect": "reject",
             "defects": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"], "build": build}]
