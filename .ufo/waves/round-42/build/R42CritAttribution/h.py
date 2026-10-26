#!/usr/bin/env python3
"""Critic harness (scratch only): measure the frozen C1 attribution leg on the frozen witness battery.

Not part of the lane. Reads plans/round42_c1_verify.py (a copy, sha-verified) as a library.
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
S = pathlib.Path(os.environ["S"])
LANE = S / "lane"
WB = S / "wb"
ROOT = S / "run1"
ROOT.mkdir(parents=True, exist_ok=True)
OUT = S / "report"
OUT.mkdir(exist_ok=True)

spec = importlib.util.spec_from_file_location("k42c1", str(S / "counter.py"))
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

TR2 = r'''
import hashlib, json, os, re, runpy, sys

slot, out = sys.argv[1], os.path.join(os.environ["TMPDIR"], "k42-t2.json")
full = {int(x) for x in os.environ.get("K42_FULL", "").split(",") if x}
rec = {"line_hits": set(), "calls": [], "locs": {}, "full": {}}
ADDR = re.compile(r"0x[0-9a-fA-F]+")


def desc(code):
    return "%s@%d" % (code.co_name, code.co_firstlineno)


def norm(v):
    return ADDR.sub("0xADDR", repr(v))


def loc_sha(frame):
    try:
        s = "|".join("%s=%s" % (k, norm(v)) for k, v in sorted(frame.f_locals.items()))
    except Exception as e:  # a value whose repr explodes is not comparable
        return "ERR:" + type(e).__name__
    return hashlib.sha256(s.encode()).hexdigest()[:16], s


def local(frame, event, arg):
    if event == "line":
        n = frame.f_lineno
        d = desc(frame.f_code)
        rec["line_hits"].add(n)
        per = rec["locs"].setdefault(d, {})
        if str(n) not in per:
            sha, text = loc_sha(frame)
            per[str(n)] = sha
            if n in full:
                rec["full"].setdefault(str(n), text[:3000])
    return local


def glob(frame, event, arg):
    if frame.f_code.co_filename == slot:
        if event == "call":
            rec["calls"].append([desc(frame.f_code), frame.f_lineno])
            return local
        if event == "line":
            return local(frame, event, arg)
    return None


sys.argv = sys.argv[1:]
code = 0
sys.settrace(glob)
try:
    runpy.run_path(slot, run_name="__main__")
except SystemExit as e:
    code = e.code
finally:
    sys.settrace(None)
    with open(out, "w") as fh:
        json.dump({"line_hits": sorted(rec["line_hits"]), "calls": rec["calls"],
                   "locs": rec["locs"], "full": rec["full"]}, fh)
sys.exit(code)
'''


def run2(runner, tool, variant, fx, tag, full=()):
    """Frozen Runner.run with the instrumented tracer; keeps the trace JSON."""
    n = next(runner.seq)
    work = runner.root / "work" / ("c%06d" % n)
    tmp = runner.root / "rtmp" / ("c%06d" % n)
    work.mkdir()
    tmp.mkdir()
    argv = []
    for t in fx["argv"]:
        m = ctr.WORK_TOKEN.match(t)
        if m:
            w = work / "run"
            if m.group(1):
                (w / m.group(1)).mkdir(parents=True, exist_ok=True)
            if m.group(2):
                w.mkdir(exist_ok=True)
            argv.append(str(w) + (m.group(2) or ""))
        else:
            argv.append(t)
    slot = runner.slots / ("%s.py" % tool)
    src = open(variant, "rb")
    tsrc = open(S / "tr2.py", "rb")
    try:
        data = ((src.fileno(), str(slot)), (tsrc.fileno(), ctr.TRACER_SLOT))
        cmd = ctr.ro_sandbox(writable=(work, tmp),
                            hide=[p for p in (runner.root / "variants", runner.root / "slots",
                                              runner.root / "bin", runner.root / "tracer") if p.exists()],
                            ro_data=data) + [ctr.PY, ctr.TRACER_SLOT, str(slot)] + argv
        env = runner.env(tmp)
        env["K42_FULL"] = ",".join(str(x) for x in full)
        r = subprocess.run(cmd, cwd=str(fx["dir"]), env=env, capture_output=True, text=True,
                           timeout=600, pass_fds=tuple(fd for fd, _d in data))
    finally:
        src.close()
        tsrc.close()
    try:
        payload = json.loads((tmp / "k42-t2.json").read_text())
    except (OSError, ValueError):
        payload = {"line_hits": [], "calls": [], "locs": {}, "full": {}}
    import shutil
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return (r.returncode, ctr.classes(tool, r.stdout), payload)


def main():
    runner = ctr.Runner(ROOT, 8)
    (S / "tr2.py").write_text(TR2)
    fixtures, side = ctr.build_battery(WB, ROOT, LANE)
    by_tool = {t: [fx for fx in fixtures if fx["tool"] == t] for t in ctr.TOOLS}
    srcs = {t: (LANE / rel).read_text() for t, rel in ctr.TOOLS.items()}
    vdir = ROOT / "variants"
    vdir.mkdir()
    for t in ctr.TOOLS:
        (vdir / ("ref-%s.py" % t)).write_text(srcs[t])
    meta = {}
    for mid, tool, cls, direction, adv_kind, label, _w, old, new in ctr.MUTANTS:
        src = srcs[tool]
        v = vdir / ("%s.py" % mid)
        v.write_text(src.replace(old, new, 1))
        start = src[:src.index(old)].count("\n") + 1
        span = set(range(start, start + new.count("\n") + 1))
        meta[mid] = {"tool": tool, "cls": cls, "direction": direction,
                     "span": sorted(span), "start": start,
                     "old_lines": old.count("\n") + 1, "new_lines": new.count("\n") + 1}
    res = {}
    t2 = {}
    variants = {}
    for t in ctr.TOOLS:
        variants.setdefault(t, {})["ref"] = ("ref", vdir / ("ref-%s.py" % t))
    for mid, m in meta.items():
        variants.setdefault(m["tool"], {})[mid] = (mid, vdir / ("%s.py" % mid))
    for tool, fxs in by_tool.items():
        for name, (vname, path) in variants[tool].items():
            for fx in fxs:
                key = "%s|%s|%s" % (tool, name, fx["fid"])
                res[key] = {"plain": runner.run(tool, path, fx),
                            "stock": runner.run(tool, path, fx, trace=True)}
                r2 = run2(runner, tool, path, fx, re.sub(r"[^A-Za-z0-9_.-]", "_", key))
                t2[key] = {"rc": r2[0], "cls": sorted(r2[1]), "p": r2[2]}
                print("RAN", key, res[key]["plain"], res[key]["stock"][:2], flush=True)
    (OUT / "res.json").write_text(json.dumps({
        "meta": meta,
        "res": {k: {"plain": [v["plain"][0], sorted(v["plain"][1])],
                    "stock": [v["stock"][0], sorted(v["stock"][1]), sorted(v["stock"][2])]}
                for k, v in res.items()}}))
    (OUT / "t2.json").write_text(json.dumps(t2))
    print("DONE fixtures=%d side=%d" % (len(fixtures), side))


if __name__ == "__main__":
    main()
