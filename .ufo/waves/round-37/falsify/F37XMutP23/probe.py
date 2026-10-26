#!/usr/bin/env python3
"""F37XMutP23 liveness probes: are the surviving mutants LIVE (a correct battery could catch them) or
INERT (no fixture whatsoever could distinguish them)?

Probes are mine, built from the genuine round-35 package outside the lane; they are never added to the
frozen battery and never touch the lane.

  probe-eight            genuine quote table cut to its first 8 data rows: 8 distinct texts, 8 distinct
                         (capture, line) locations, every quote in range. The reference ACCEPTS it, so
                         any mutant that raises either equality floor must reject it: this is the
                         fixture both surviving boundary mutants are missing.
  probe-receipt-tail     the receipt's LAST byte differs  -> does a prefix digest comparison differ?
  probe-receipt-byte8    the receipt's 9th byte differs   -> same, inside the first 4 bytes' prefix
  (if both are inert, the prefix-comparison mutant is not a battery limit at all: SHA-256 avalanche
   makes any single-byte edit change the leading hex digits, so no fixture can distinguish it.)

  probe.py LANE WORK
"""
from __future__ import annotations

import importlib.util
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # dataclasses resolve the defining module through sys.modules
    spec.loader.exec_module(mod)
    return mod


def run(gate, counter, spec_path, argv):
    r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(spec_path)],
                       capture_output=True, text=True, timeout=900)
    bad = frozenset(m.group(1) for m in map(counter.CLAUSE_LINE.match, r.stdout.splitlines())
                    if m and m.group(2) == "DEFECT")
    return r.returncode, bad, r.stdout


MUTANTS = {
    "X2": ('len(locs) >= rules["min_distinct_locations"]', 'len(locs) > rules["min_distinct_locations"]'),
    "Y3": ('len(texts) >= rules["min_quotes"]', 'len(texts) > rules["min_quotes"]'),
    "Z1": ('return got == want, f"receipt_sha256=', 'return got[:8] == want[:8], f"receipt_sha256='),
    "Y4": ("“(.+?)”", "“(.*?)”"),
    "Y5": ("    if p.quote_section is None:\n        return False, \"no '## Located quotes' section\"\n"
           "    if p.bad_rows:\n        return False, f\"unparsed_rows={len(p.bad_rows)} first={p.bad_rows[0][:70]!r}\"",
           "    if p.bad_rows:\n        return False, f\"unparsed_rows={len(p.bad_rows)} first={p.bad_rows[0][:70]!r}\"\n"
           "    if p.bad_rows and p.quote_section is None:\n        return False, \"no '## Located quotes' section\""),
}


def main():
    lane = pathlib.Path(sys.argv[1]).resolve()
    work = pathlib.Path(sys.argv[2]).resolve()
    c1 = load(lane / "plans" / "round37_c1_verify.py", "k37c1")
    gate = load(lane / "plans" / "pkg_gate.py", "k37gate")
    r36 = c1.load_r36(lane)
    ctx = c1.Ctx(lane, r36)
    gate_src = (lane / "plans" / "pkg_gate.py").read_text()
    assert c1.sha256(lane / "plans" / "pkg_gate.py") == c1.GATE_SHA256

    gdir = work / "probe-gates"
    gdir.mkdir(parents=True, exist_ok=True)
    gates = {"ref": gdir / "ref.py"}
    gates["ref"].write_text(gate_src)
    for mid, (old, new) in MUTANTS.items():
        assert gate_src.count(old) == 1, mid
        p = gdir / f"{mid}.py"
        p.write_text(gate_src.replace(old, new, 1))
        py_compile.compile(str(p), doraise=True, cfile=str(p) + "c")
        gates[mid] = p

    proot = work / "probe-fx"
    if proot.exists():
        shutil.rmtree(proot)
    proot.mkdir(parents=True)
    argv_of = lambda d: ["package", "--root", str(d), "--require-clean-tree"]

    d = proot / "eight"
    d.mkdir()
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), lambda rows: rows[:8]))
    ctx.git_add(d)

    for name, index in (("tail", -1), ("byte8", 8)):
        d = proot / name
        d.mkdir()
        ctx.genuine_package(d)
        receipt = d / ctx.spec["receipt"]
        raw = receipt.read_bytes()
        i = index if index >= 0 else len(raw) + index
        old, new = raw[i:i + 1], (b"Q" if raw[i:i + 1] != b"Q" else b"R")
        receipt.write_bytes(raw[:i] + new + raw[i + 1:])
        ctx.git_add(d)
        print(f"PROBE receipt-{name} offset={i} of {len(raw)} bytes {old!r}->{new!r}")

    plan = (("eight", ("X2", "Y3")), ("tail", ("Z1",)), ("byte8", ("Z1",)))
    for name, mids in plan:
        d = proot / name
        argv = argv_of(d)
        r_ref = run(gates["ref"], c1, ctx.spec_path, argv)
        print(f"PROBE {name} ref=rc{r_ref[0]} defects={','.join(sorted(r_ref[1])) or '-'}")
        for line in r_ref[2].splitlines():
            if re.match(r"^P[234] ", line):
                print(f"    ref {line}")
        for mid in mids:
            r_mut = run(gates[mid], c1, ctx.spec_path, argv)
            live = (r_ref[0], r_ref[1]) != (r_mut[0], r_mut[1])
            print(f"PROBE {name} {mid}=rc{r_mut[0]} defects={','.join(sorted(r_mut[1])) or '-'} "
                  f"-> {'LIVE' if live else 'INERT'}")
            for line in r_mut[2].splitlines():
                if re.match(r"^P[234] ", line):
                    print(f"    {mid} {line}")

    g = proot / "genuine"
    g.mkdir()
    ctx.genuine_package(g)
    pkg = gate.Package.load(g, ctx.spec)
    words = sorted(q.words for q in pkg.quotes)
    print(f"GENUINE quotes={len(pkg.quotes)} words_min={words[0]} words_max={words[-1]} "
          f"distinct_texts={len({q.text for q in pkg.quotes})} "
          f"distinct_locs={len({(q.capture, q.start) for q in pkg.quotes})} "
          f"spec_quote_words={ctx.spec['entry_rules']['quote_words']} "
          f"spec_min_quotes={ctx.spec['entry_rules']['min_quotes']} "
          f"spec_min_distinct_locations={ctx.spec['entry_rules']['min_distinct_locations']}")
    print("GENUINE word-histogram=" + ",".join(f"{w}:{words.count(w)}" for w in sorted(set(words))))
    capdir = g / ctx.spec["capture_dir"]
    for f in sorted(capdir.glob("test_outputs*.py*")):
        lines = f.read_text(errors="replace").splitlines()
        mx = max(((len(l.split()), i + 1) for i, l in enumerate(lines)), default=(0, 0))
        print(f"CAPTURE {f.name} lines={len(lines)} max_words_per_line={mx[0]} at line {mx[1]}")

    for fx in c1.r36_fixtures(r36):
        if fx["fid"] != "r36-P3":
            continue
        d = proot / "r36p3"
        d.mkdir()
        fx["build"](ctx, d)
        res = run(gates["ref"], c1, ctx.spec_path, argv_of(d))
        print(f"R36P3 ref=rc{res[0]} defects={','.join(sorted(res[1]))}")
        for line in res[2].splitlines():
            if re.match(r"^P[34] ", line):
                print(f"    {line}")

    # Y4 inertness: an empty quote text is an unparsed row for the reference and a 0-word quote for the
    # loosened regex; if both land on P3 DEFECT, no fixture can separate them.
    d = proot / "empty-quote"
    d.mkdir()
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    text = entry.read_text()
    def blank(rows):
        row = rows[4]
        q = ctx.r36.QUOTE_ROW.match(row)
        if not q:
            raise RuntimeError(f"row not parseable: {row!r}")
        return rows[:4] + [row.replace(f"“{q.group(1)}”", "“”")] + rows[4:]
    entry.write_text(ctx.r36.rewrite_quotes(text, blank))
    ctx.git_add(d)
    for mid in ("ref", "Y4"):
        res = run(gates[mid], c1, ctx.spec_path, argv_of(d))
        print(f"PROBE empty-quote {mid}=rc{res[0]} defects={','.join(sorted(res[1]))}")
        for line in res[2].splitlines():
            if re.match(r"^P[34] ", line):
                print(f"    {mid} {line}")

    # Y5 inertness: the reorder is message-only; the clause ids are identical.
    p23 = load(lane / "plans" / "battery37" / "p23.py", "k37battery_p23")
    fx = next(f for f in p23.FIXTURES if f["fid"] == "p23-p3-heading-renamed")
    d = proot / "heading-renamed"
    fx["build"](ctx, d)
    for mid in ("ref", "Y5"):
        res = run(gates[mid], c1, ctx.spec_path, argv_of(d))
        print(f"PROBE heading-renamed {mid}=rc{res[0]} defects={','.join(sorted(res[1]))}")
        for line in res[2].splitlines():
            if re.match(r"^P[34] ", line):
                print(f"    {mid} {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
