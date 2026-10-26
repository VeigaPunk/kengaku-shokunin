#!/usr/bin/env python3
"""R42CritIndep: re-derive the 16 frozen probe cases' three letters from model.py only.

Case end states are rebuilt from each case's *description* (probe docstring + frozen dry table
gates_lines) and my own circuit generator; nothing here imports or runs the frozen probe, the
grader or sim.c.  Letters are compared with the observed letters in fibsqrt-probe.txt.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import model

CAP = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round42/tb2-circuit-fibsqrt")
RECEIPT = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round42/fibsqrt-probe.txt")
EXAMPLES = {208: 377, 20000: 1407432322}


def text(lines, eol="\n"):
    return eol.join(lines) + eol


L28 = model.lookup(model.GRADED)
L27 = model.lookup([v for v in model.GRADED if v != 48401])
L30 = model.lookup(model.GRADED + [208, 20000])


def build_cases():
    """(cid, gates_bytes|None, is_dir, receipt_note) in receipt order."""
    seed = (CAP / "gates.txt").read_bytes()
    out = []
    out.append(("nop", seed, False, "shipped example left in place"))
    out.append(("oracle-solve-sh", pathlib.Path("work/gates.txt").read_bytes(), False,
                "solve.sh reference circuit (generated in my scratch)"))
    out.append(("no-gates-file", None, False, "gates.txt removed"))
    out.append(("empty-gates-file", b"", False, "empty gates.txt"))
    out.append(("lookup-28", text(L28).encode(), False, "lookup for the 28 graded inputs"))
    out.append(("lookup-27-drop-48401", text(L27).encode(), False, "lookup minus 48401"))
    out.append(("lookup-28-plus-examples", text(L30).encode(), False, "lookup plus 208 and 20000"))
    out.append(("lookup-28-bitflip-41", text(model.lookup(model.GRADED, flip=(41, 0))).encode(), False,
                "lookup, bit 0 of the answer for 41 flipped"))
    out.append(("lookup-28-padded-31999", text(L28 + [""] * (31999 - len(L28))).encode(), False, "padded to 31999"))
    out.append(("lookup-28-padded-32000", text(L28 + [""] * (32000 - len(L28))).encode(), False, "padded to 32000"))
    out.append(("lookup-28-comment-lines", text([y for x in L28 for y in ("# note", x)]).encode(), False,
                "# note before every line"))
    out.append(("lookup-28-reversed-lines", text(list(reversed(L28))).encode(), False, "lines reversed"))
    out.append(("lookup-28-crlf", text(L28, "\r\n").encode(), False, "CRLF line ends"))
    out.append(("lookup-28-trailing-space", text([x + " " for x in L28]).encode(), False, "one trailing space per line"))
    out.append(("fake-sim-script", seed, False, "example circuit; grader's compile overwrites /app/sim"))
    out.append(("gates-is-directory", None, True, "gates.txt is a directory"))
    return out


def predict(cid, gates, is_dir, note):
    letters, detail = model.grade(gates, is_dir=is_dir, missing=gates is None and not is_dir)
    row = {"cid": cid, "predicted": letters, "note": note, "detail": detail}
    if gates is not None:
        row["lines"] = model.py_lines(gates)
        row["sha256"] = __import__("hashlib").sha256(gates).hexdigest()
    probe = {}
    if gates is not None:
        prog = model.Program()
        prog.feed(gates)
        for n in (1, 41, 208, 20000, 48401):
            o, _rc, _oob = model.simulate(prog, str(n))
            try:
                probe[n] = int(o.strip())
            except ValueError:
                probe[n] = None
    row["probe_outputs"] = {str(k): v for k, v in probe.items()}
    return row


def receipt_letters():
    got = {}
    for line in RECEIPT.read_text().splitlines():
        m = re.match(r"CASE (\S+) .* tests=([PF]{3}) .* observed=(\S+)", line)
        if m:
            got[m.group(1)] = (m.group(2), m.group(3))
    return got


def main():
    import time
    obs = receipt_letters()
    rows = []
    t0 = time.time()
    for cid, gates, is_dir, note in build_cases():
        t = time.time()
        row = predict(cid, gates, is_dir, note)
        row["seconds"] = round(time.time() - t, 2)
        rows.append(row)
        print(json.dumps(row))
        sys.stdout.flush()
    print("----")
    agree = 0
    for row in rows:
        o = obs.get(row["cid"])
        row["observed"] = o[0] if o else "?"
        ok = o is not None and o[0] == row["predicted"]
        agree += ok
        print(f"INDEP {row['cid']:28s} mine={row['predicted']} receipt={row['observed']} "
              f"{'AGREE' if ok else 'DISAGREE'} lines={row.get('lines')} num_signals="
              f"{(row['detail'] or {}).get('num_signals')} s={row['seconds']}")
    print(f"indep_agree={agree}/{len(rows)} total_s={round(time.time()-t0,1)}")
    print("dry-table line counts for my generator: L28=%d L27=%d L30=%d flip=%d comments=%d" % (
        len(L28), len(L27), len(L30), len(model.lookup(model.GRADED, flip=(41, 0))),
        len([y for x in L28 for y in ("# note", x)])))
    print("lookup-28 on the instruction's examples: 208 -> %s (instruction 377), 20000 -> %s (instruction 1407432322)" % (
        (lambda p: model.simulate(p, "208")[0].strip())((lambda p: (p.feed(text(L28).encode()), p)[1])(model.Program())),
        (lambda p: model.simulate(p, "20000")[0].strip())((lambda p: (p.feed(text(L28).encode()), p)[1])(model.Program()))))
    pathlib.Path("predictions.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
