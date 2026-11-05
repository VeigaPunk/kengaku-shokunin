#!/usr/bin/env python3
"""Forgery x-head-not-rev (ExecC2Rerun): the CLI diffs the lane's HEAD, not --rev.

Everything else is the honest frozen gate (forgeries/honest-gate-at-T.py, sha256 18b01b42...).
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
    head = G.git(root, "rev-parse", "HEAD").stdout.decode().strip()
    return _orig_evaluate(root, freeze, head, claims, paths)


G.evaluate = evaluate

if __name__ == "__main__":
    sys.exit(G.main(sys.argv[1:]))
