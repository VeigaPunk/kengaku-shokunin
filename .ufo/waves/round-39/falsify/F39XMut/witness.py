#!/usr/bin/env python3
"""F39XMut survivor witnesses.

Phase 1: compile every extra mutant gate (XP1a..XD5c) from the pristine clone gate.
Phase 2: for each extra mutant the full battery does not kill, build the distinguishing input the
battery lacks and show reference vs mutant differing in the declared direction.

Fixtures live only under the seat scratch (/fast/scratch/hyaku/kengaku-r39/F39XMut/wit); the lane
clone is read-only. Package fixtures are git-inited by ctx.genuine_package and staged with
ctx.git_add (index only, no commit) — the same helpers the battery39 modules use.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r39/F39XMut")
LANE = S / "lane"

xspec = importlib.util.spec_from_file_location("xmut39", S / "xmut39.py")
x = importlib.util.module_from_spec(xspec)
xspec.loader.exec_module(x)
m = x.m
EXTRA = {t[0]: t for t in x.EXTRA}

r37 = m.load(LANE / m.R37_REL, "kengaku_r37_c1")
r36 = r37.load_r36(LANE)
ctx = r37.Ctx(LANE, r36)

root = S / "wit"
shutil.rmtree(root, ignore_errors=True)
root.mkdir(parents=True)
gates = root / "gates"
gates.mkdir()
gate_src = (LANE / "plans" / "pkg_gate.py").read_text()
ref_gate = gates / "ref.py"
ref_gate.write_text(gate_src)

print("== phase 1: compile all extra mutant gates ==")
for mid, (_i, _c, _d, _l, _n, old, new) in EXTRA.items():
    assert gate_src.count(old) == 1, (mid, "old count", gate_src.count(old))
    p = gates / f"{mid}.py"
    p.write_text(gate_src.replace(old, new, 1))
    try:
        py_compile.compile(str(p), doraise=True, cfile=str(gates / f"{mid}.pyc"))
        print(f"COMPILE {mid} ok")
    except py_compile.PyCompileError as e:
        print(f"COMPILE {mid} FAIL {e}")
        raise


def mutant_gate(mid):
    return gates / f"{mid}.py"


def run(gate, argv, spec_path):
    full = [sys.executable, str(gate), *argv] + \
        ([] if "--spec" in argv else ["--spec", str(spec_path)])
    r = subprocess.run(full, capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout


def clause_lines(so, clause):
    return [l for l in so.splitlines() if re.match(rf"^{clause} (ok|DEFECT) ", l)]


def package_fixture(name):
    d = root / name
    ctx.genuine_package(d)
    return d


def stage(d):
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def witness(mid, direction, input_desc, argv, clause, spec_path=None):
    spec_path = spec_path or ctx.spec_path
    rc_r, so_r = run(ref_gate, argv, spec_path)
    rc_m, so_m = run(mutant_gate(mid), argv, spec_path)
    print(f"\nWITNESS {mid} direction={direction} input={input_desc}")
    print(f"  fixture argv: {argv}")
    print(f"  ref  rc={rc_r} | {' ; '.join(clause_lines(so_r, clause)) or so_r.strip()[:120]}")
    print(f"  mut  rc={rc_m} | {' ; '.join(clause_lines(so_m, clause)) or so_m.strip()[:120]}")
    if direction == "silence":
        exhibited = clause in so_r and f"{clause} DEFECT" in so_r and \
            f"{clause} DEFECT" not in so_m and rc_r in (0, 1) and rc_m in (0, 1)
    else:
        exhibited = f"{clause} DEFECT" not in so_r and f"{clause} DEFECT" in so_m and \
            rc_r in (0, 1) and rc_m in (0, 1)
    print(f"  => {'EXHIBITED' if exhibited else 'NOT EXHIBITED'} ({direction}: "
          f"{'ref DEFECT / mut ok' if direction == 'silence' else 'ref ok / mut DEFECT'})")
    return exhibited


results = {}

# XP1a — corrupt pin 3 (plans/defect_ledger.py); pins 1-2 genuine.
d = package_fixture("xp1a")
pin3 = list(ctx.spec["frozen_instruments"])[2]
f = d / pathlib.PurePosixPath(pin3)
f.write_bytes(f.read_bytes() + b"\n# xp1a witness byte\n")
results["XP1a"] = witness("XP1a", "silence", f"append bytes to {pin3} (pin 3 of 3)",
                          stage(d), "P1")

# XP3c — accept package whose longest quote is exactly hi (25) words.
d = package_fixture("xp3c")
p3m = m.load(LANE / "plans" / "battery39" / "p3m39.py", "p3m39_xmut")
rules = ctx.spec["entry_rules"]
want = int(rules["quote_words"][1])
capdir = d / pathlib.PurePosixPath(ctx.spec["capture_dir"])
entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
# existing quote locations, so the replacement row cites an unused (capture, line)
sec = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", entry.read_bytes().decode("utf-8"),
                re.S | re.M)
used_locs = set()
for l in sec.group(1).splitlines():
    qm = re.match(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$", l)
    if qm:
        used_locs.add((qm.group(2), int(qm.group(3))))
pick = None
for name in ("task.toml", "instruction.md"):
    c = capdir / name
    if not c.is_file():
        continue
    lines = c.read_bytes().decode("utf-8").splitlines()
    for no, line in enumerate(lines, 1):
        words = line.split()
        if len(words) < want or (name, no) in used_locs:
            continue
        text = " ".join(words[-want:])
        if text in line and len(text.split()) == want and "|" not in text and "\u201d" not in text:
            pick = (name, no, text)
            break
    if pick:
        break
if pick is None:
    raise RuntimeError("no capture line with 25 usable words at an unused location")
name, no, text = pick
row = f"| the probe states its objective in exactly {want} words | “{text}” | `{name}:{no}` |"
entry.write_bytes(ctx.r36.rewrite_quotes(
    entry.read_bytes().decode("utf-8"), lambda data: data[:-1] + [row]).encode("utf-8"))
results["XP3c"] = witness("XP3c", "mirror",
                          f"accept pkg, last quote = exactly {want} words ({name}:{no})",
                          stage(d), "P3")

# XP7a — S105 carries [other, pinned]: the pinned URL is not the last source line.
d = package_fixture("xp7a")
entry = d / ctx.spec["entry"]
lines = entry.read_bytes().decode("utf-8").splitlines()
sid = "S105"
hits = [i for i, l in enumerate(lines) if l.startswith(f"source: {sid} ")]
assert len(hits) == 1, hits
pinned = ctx.spec["raw_base"] + ctx.spec["rows"][sid]["upstream"]
other = ctx.spec["raw_base"] + ctx.spec["rows"]["S107"]["upstream"]
assert pinned != other
early = f"source: {sid} \u2014 {other} \u2014 planted earlier source line (xp7a witness)"
lines.insert(hits[0], early)
entry.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
results["XP7a"] = witness("XP7a", "silence",
                          f"{sid} source lines [other-url, pinned-url] (pinned not last)",
                          stage(d), "P7")

# XP7b — S105 carries [pinned, pinned]: duplicated pinned source line.
d = package_fixture("xp7b")
entry = d / ctx.spec["entry"]
lines = entry.read_bytes().decode("utf-8").splitlines()
hits = [i for i, l in enumerate(lines) if l.startswith(f"source: {sid} ")]
assert len(hits) == 1, hits
lines.insert(hits[0] + 1, lines[hits[0]])
entry.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
results["XP7b"] = witness("XP7b", "silence",
                          f"{sid} source lines [pinned-url, pinned-url] (duplicate)",
                          stage(d), "P7")


# XD5a / XD5b — d5-line fixtures with a crafted quote the tag strip treats differently.
def d5_fixture(name, marker_line, quote):
    d = root / name
    d.mkdir()
    capdir = d / "captures"
    shutil.copytree(ctx.d5_capture_dir(), capdir)
    d5 = ctx.spec["d5"]
    cap = capdir / d5["capture_name"]
    text = cap.read_bytes().decode("utf-8")
    assert marker_line not in text, "marker line already present"
    text = text.rstrip("\n") + "\n" + marker_line + "\n"
    cap.write_bytes(text.encode("utf-8"))
    man = capdir / d5["manifest_name"]
    digest = hashlib.sha256(cap.read_bytes()).hexdigest()
    d5m = m.load(LANE / "plans" / "battery39" / "d5m39.py", "d5m39_xmut")
    man.write_bytes(d5m._repin(man.read_bytes().decode("utf-8"), d5["capture_name"],
                               digest).encode("utf-8"))
    spec2 = copy.deepcopy(ctx.spec)
    spec2["d5"] = dict(spec2["d5"])
    spec2["d5"]["quote"] = quote
    sp = d / "spec.json"
    sp.write_bytes((json.dumps(spec2, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    line = d / "erratum.md"
    line.write_bytes((f"Erratum (round 35): the marker is present in {d5['capture_name']}.\n"
                      ).encode("utf-8"))
    return ["d5-line", "--file", str(line), "--capture-dir", str(capdir), "--spec", str(sp)]


argv = d5_fixture("xd5a", "A<>B", "A<>B")
results["XD5a"] = witness("XD5a", "mirror", "capture carries literal '<>'; quote contains '<>'",
                          argv, "D5", spec_path=root / "xd5a" / "spec.json")

argv = d5_fixture("xd5b", "A<x>B<!c>C", "ABC")
results["XD5b"] = witness("XD5b", "mirror",
                          "quote span separated by a comment tag <!c> (non-letter-led)",
                          argv, "D5", spec_path=root / "xd5b" / "spec.json")

print("\n== summary ==")
for mid, ok in results.items():
    print(f"WITNESS {mid} {'exhibited' if ok else 'NOT-EXHIBITED'}")
