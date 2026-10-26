#!/usr/bin/env python3
"""R42CritIndep: build my three extra cases (+ one control) and predict them with model.py.

X1 dup-gate-definition : L28 plus a second definition of index 0 (`out0 = out31`).
X2 out32000-line       : L28 plus `out32000 = 0` (index == MAX_SIGNALS: OOB write / window shift).
X3 wrong-above-48401   : the solve.sh reference circuit + a guard that zeroes the output for
                         every N > 48401, i.e. a general circuit wrong only above the graded range.
C1 oracle-crlf         : control, the reference circuit with CRLF line ends.
"""
from __future__ import annotations

import hashlib
import pathlib

import model

HERE = pathlib.Path(__file__).resolve().parent
ORACLE = (HERE / "work" / "gates.txt").read_text()


def wire(lines, expr):
    lines.append(f"out{len(lines)} = {expr}")
    return len(lines) - 1


def guard_lines(lines, nbits=32, threshold=48401):
    """Append `out = out(out_bits) & ~(N > threshold)` for the last 32 signals of `lines`."""
    src = [len(lines) - 32 + j for j in range(nbits)]      # the reference circuit's answer bits
    nin = [i for i in range(nbits)]                        # sim.c sets out0..out31 from argv[1]
    hi = nin[16]
    for b in nin[17:]:
        hi = wire(lines, f"out{hi} | out{b}")               # any bit >= 16 set -> N >= 65536
    eq = wire(lines, "1")
    gt = None
    for i in range(15, -1, -1):
        bit = (threshold >> i) & 1
        if bit == 0:
            term = wire(lines, f"out{nin[i]} & out{eq}")
            gt = term if gt is None else wire(lines, f"out{gt} | out{term}")
        same = nin[i] if bit else wire(lines, f"~out{nin[i]}")
        eq = wire(lines, f"out{eq} & out{same}")
    gt = wire(lines, f"out{gt} | out{hi}")
    ok = wire(lines, f"~out{gt}")
    outs = [wire(lines, f"out{s} & out{ok}") for s in src]
    assert outs == list(range(len(lines) - 32, len(lines)))


def main():
    L28 = model.lookup(model.GRADED)
    cases = {}
    cases["dup-gate-definition"] = "\n".join(L28 + ["out0 = out31"]) + "\n"
    long_line = "out31999 = 0" + " " * 250
    cases["long-line-window"] = "\n".join(L28) + "\n" + long_line + "\n"
    cases["out32000-line"] = "\n".join(L28 + ["out32000 = 0"]) + "\n"
    gl = ORACLE.rstrip("\n").split("\n")
    guard_lines(gl)
    cases["wrong-above-48401"] = "\n".join(gl) + "\n"
    (HERE / "oracle-gates.txt").write_text(ORACLE)
    (HERE / "above48401-gates.txt").write_text(cases["wrong-above-48401"])
    cases["oracle-crlf"] = ORACLE.replace("\n", "\r\n")

    table = {}
    for cid, body in cases.items():
        data = body.encode()
        letters, detail = model.grade(data)
        prog = model.Program()
        prog.feed(data)
        probe = {}
        for n in (1, 41, 208, 20000, 48401, 48402, 1 << 16, 4000000000):
            out, _rc, oob = model.simulate(prog, str(n))
            try:
                val = int(out.strip())
            except ValueError:
                val = None
            probe[n] = (val, model.answer(n))
        table[cid] = {"predicted": letters, "lines": model.py_lines(data),
                      "sha256": hashlib.sha256(data).hexdigest(),
                      "num_signals": prog.num_signals, "oob_write": sorted(prog.oob_write),
                      "dropped": prog.dropped, "probe": {str(k): v for k, v in probe.items()}}
        print(cid, letters, "lines=%d" % model.py_lines(data),
              "num_signals=%d" % prog.num_signals, "oob=%s" % sorted(prog.oob_write),
              "dropped=%d" % prog.dropped, hashlib.sha256(data).hexdigest()[:16])
        for n, (got, exp) in probe.items():
            print(f"   N={n}: model={got} expected={exp} {'ok' if got == exp else 'MISMATCH'}")
    import json
    (HERE / "extras.json").write_text(json.dumps(table, indent=1))


if __name__ == "__main__":
    main()
