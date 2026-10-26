#!/usr/bin/env python3
"""R43MutC1Counter: generate single-line mutants of the round-43 C1 counter's guards.

Each mutant is one behaviour-bearing line of plans/round43_c1_verify.py (frozen digest 1a1cd1f8...)
replaced in a SCRATCH COPY; the lane file is never touched. Assertions: anchor unique, newline
count preserved, mutant byte-compiles.
"""
import pathlib
import py_compile

SRC = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43MutC1Counter/lane/plans/round43_c1_verify.py")
OUT = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43MutC1Counter/mut")
OUT.mkdir(exist_ok=True)
text = SRC.read_text()

MUTANTS = [
    ("M01-site-equal-true",
     "    return tuple(mut_sites) == tuple(ref_sites)",
     "    return True"),
    ("M02-ref-trace1-dropped",
     "                _r_rc, _r_cls, _r_lines, r_sites = runner.run(tool, refs[tool][0], fx, trace=True, span=span)",
     "                _r_rc, _r_cls, _r_lines, r_sites = 0, frozenset(), frozenset(), ()"),
    ("M03-ref-trace2-reused",
     "                _r_rc, _r_cls, _r_lines, r_sites2 = runner.run(tool, refs[tool][0], fx, trace=True, span=span)",
     "                r_sites2 = tuple(r_sites)"),
    ("M04-newline-check-off",
     '                    or old.count("\\n") != new.count("\\n") \\',
     '                    or False \\'),
    ("M05-symlink-breach-off",
     "            if p.is_symlink() and not p.resolve().is_relative_to(d):",
     "            if False:"),
    ("M06-order-argv-breach-off",
     '        if r.returncode == 0 and r.stdout.strip() != "blob":',
     "        if False:"),
    ("M07-repo-toplevel-off",
     "            if pathlib.Path(seen).resolve() != repo:",
     "            if False:"),
    ("M08-repo-worktree-off",
     "        if val:",
     "        if False:"),
    ("M09-exhibits-defects-dropped",
     '    return cls in ref[1] and cls in set(fx["defects"]) and cls not in mut[1]  # silence',
     '    return cls in ref[1] and cls not in mut[1]  # silence'),
    ("M10-floors-sum-dropped",
     "        floors_ok = (TOTAL >= 1 and all(FLOORS.get(t, 0) >= 1 for t in TOOLS) and sum(FLOORS.values()) == TOTAL",
     "        floors_ok = (TOTAL >= 1 and all(FLOORS.get(t, 0) >= 1 for t in TOOLS) and True"),
    ("M11-unattributed-as-survived",
     "                unattributed += 1",
     "                survived += 1"),
    ("M12-fingerprint-content-dropped",
     "                content = file_sha256(p)",
     '                content = ""'),
    ("M13-sidechannel-scan-off",
     "        if hits:",
     "        if False:"),
    ("M14-pins-after-dropped",
     "        after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]",
     "        after = []"),
    ("M15-null-run-off",
     '                if res != ref[fx["fid"]]:',
     "                if False:"),
]

for mid, old, new in MUTANTS:
    n = text.count(old)
    assert n == 1, (mid, "anchor not unique", n)
    assert old.count("\n") == new.count("\n"), (mid, "newline count differs")
    p = OUT / f"{mid}.py"
    p.write_text(text.replace(old, new, 1))
    py_compile.compile(str(p), doraise=True, cfile=str(OUT / f"{mid}.pyc"))
    print(mid, "ok")
print(len(MUTANTS), "mutants generated from", SRC)
