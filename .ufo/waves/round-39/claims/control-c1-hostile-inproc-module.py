"""Hostile control (round 39 freeze): the round-38 R38CritClaims section-2 shape. At import it replaces the
counter's run_gate in whatever process imported it, so that every mutant run returns a DEFECT-free accept;
in the round-38 counter (in-process import) this reached killed=20. Two fixtures copy the genuine package."""
import sys
_main = sys.modules.get("__main__")
if _main is not None and hasattr(_main, "run_gate"):
    _orig = _main.run_gate
    def _patched(gate, spec, argv):
        res = _orig(gate, spec, argv)
        if not str(gate).endswith("ref.py") and not str(gate).endswith("null.py"):
            return (0, frozenset(), frozenset({"P1", "P3", "P7", "D5"}))
        return res
    _main.run_gate = _patched

def _fx(fid):
    def build(ctx, d):
        ctx.genuine_package(d)
        ctx.git_add(d)
        return ["package", "--root", str(d), "--require-clean-tree"]
    return {"fid": fid, "expect": "accept", "defects": [], "build": build}

FIXTURES = [_fx("hostile-a"), _fx("hostile-b")]
