#!/usr/bin/env python3
"""Forgery x-first-row-only (ExecC2Rerun): the CLI checks only the first table row.

The honest gate (forgeries/honest-gate-at-T.py) is evaluated, then its rows are cut to rows[:1].
Only the CLI verdict path (main) is altered; the in-process battery is left honest.
"""
import importlib.util
import sys

HONEST = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-93/w1/ExecC2Rerun/forgeries/honest-gate-at-T.py"
_spec = importlib.util.spec_from_file_location("honest_gate", HONEST)
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)
_orig_evaluate = G.evaluate


def evaluate(root, freeze, rev, claims, paths):
    if sys._getframe(1).f_code.co_name != "main":
        return _orig_evaluate(root, freeze, rev, claims, paths)
    f, t, rows = _orig_evaluate(root, freeze, rev, claims, paths)
    return f, t, rows[:1]


G.evaluate = evaluate

if __name__ == "__main__":
    sys.exit(G.main(sys.argv[1:]))
