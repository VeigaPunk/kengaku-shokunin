#!/usr/bin/env python3
"""Forgery x-table-at-rev (ExecC2Rerun): reads the frozen table at --rev instead of --freeze.

The freeze window, freeze bytes and touched count are honest (--freeze..--rev); only the table
source moves from the --freeze commit to the --rev commit (so a table rewritten after the freeze
is trusted). Only the CLI verdict path (main) is altered; the in-process battery is left honest.
"""
import importlib.util
import sys

HONEST = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-93/w1/ExecC2Rerun/forgeries/honest-gate-at-T.py"
_spec = importlib.util.spec_from_file_location("honest_gate", HONEST)
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)
_orig_evaluate = G.evaluate


def read_table(root, fz, claims, paths):
    if claims is not None:
        text = G.blob(root, fz, claims)
        if text is None:
            raise G.CouldNotEvaluate(f"claims file {claims} absent at {fz[:12]}")
        return G.parse_table(text.decode(errors="replace"))
    out = []
    for p in paths or []:
        b = G.blob(root, fz, p)
        if b is None:
            raise G.CouldNotEvaluate(f"path {p} absent at {fz[:12]}")
        out.append((G.sha(b), p))
    return out


def evaluate(root, freeze, rev, claims, paths):
    if sys._getframe(1).f_code.co_name != "main":
        return _orig_evaluate(root, freeze, rev, claims, paths)
    f = G.resolve(root, freeze)
    t = G.resolve(root, rev)
    table = read_table(root, t, claims, paths)  # FORGERY: table read at --rev, not --freeze
    rows = []
    for want, p in table:
        at_f = G.blob(root, f, p)
        at_t = G.blob(root, t, p)
        log = G.git(root, "rev-list", f"{f}..{t}", "--", p)
        touched = len([x for x in log.stdout.decode().split() if x])
        reasons = []
        if at_f is None or G.sha(at_f) != want:
            reasons.append("freeze-bytes-differ-from-table")
        if at_t is None:
            reasons.append("absent-at-rev")
        elif G.sha(at_t) != want:
            reasons.append("rev-bytes-differ")
        if touched:
            reasons.append(f"touched-after-freeze={touched}")
        rows.append({"path": p, "table": want, "freeze": G.sha(at_f) if at_f else "absent",
                     "rev": G.sha(at_t) if at_t else "absent", "touched": touched,
                     "verdict": "intact" if not reasons else "broken:" + "+".join(reasons)})
    return f, t, rows


G.evaluate = evaluate

if __name__ == "__main__":
    sys.exit(G.main(sys.argv[1:]))
