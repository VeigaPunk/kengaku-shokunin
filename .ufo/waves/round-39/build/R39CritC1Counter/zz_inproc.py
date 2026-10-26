"""attack module (critic R39CritC1Counter): in-process code execution through an UNPINNED battery37 file.

`plans/round39_c1_verify.py` builds battery38/battery39 modules in child processes, but the round-37
counter's `battery37_fixtures` (r37:258-267) execs every `plans/battery37/*.py` IN the counter process.
The pin set names the nine round-37 modules by path, so a tenth file is read and executed without any
pin covering it. This module patches `__main__.run_gate` and answers for its own two fixtures only;
every other fixture falls through to the real gate.
"""
import pathlib
import sys

_main = sys.modules.get("__main__")
_orig = _main.run_gate

REJECT = frozenset({"P1", "P3", "P7"})


def _mine(argv):
    for tok in argv:
        p = pathlib.Path(tok)
        try:
            if p.is_dir() and (p / "FORGED").exists():
                return p
        except OSError:
            continue
    return None


def _forged(gate, default_spec, argv):
    root = _mine(argv)
    if root is None:
        return _orig(gate, default_spec, argv)
    stem = pathlib.Path(gate).stem
    mutant = len(stem) == 3 and stem[0] == "M" and stem[1:].isdigit()
    if (root / "KIND-ACCEPT").exists():
        return (1, frozenset({"D5"}), frozenset()) if mutant else (0, frozenset(), frozenset({"D5"}))
    return (0, frozenset(), REJECT) if mutant else (1, REJECT, frozenset())


_main.run_gate = _forged


def _reject(ctx, d):
    (d / "FORGED").write_text("1\n")
    return ["package", "--root", str(d)]


def _accept_d5(ctx, d):
    (d / "FORGED").write_text("1\n")
    (d / "KIND-ACCEPT").write_text("1\n")
    (d / "d5.txt").write_text("x\n")
    return ["d5-line", "--file", str(d / "d5.txt"), "--capture-dir", str(d)]


FIXTURES = [
    {"fid": "a3z-forged-reject", "expect": "reject", "defects": ["P1", "P3", "P7"],
     "build": _reject},
    {"fid": "a3z-forged-d5-accept", "expect": "accept", "defects": [], "build": _accept_d5},
]
