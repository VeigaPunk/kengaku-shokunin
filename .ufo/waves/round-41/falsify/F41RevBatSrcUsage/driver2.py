#!/usr/bin/env python3
"""Trace presence matrix + fixture content dump (non-author review of battery41/s_usage.py)."""
import importlib.util, pathlib, subprocess, sys, shutil, json

LANE = pathlib.Path(sys.argv[1]).resolve()
ROOT = pathlib.Path(sys.argv[2]).resolve()
BAT = pathlib.Path(sys.argv[3]).resolve()
spec = importlib.util.spec_from_file_location("c1", LANE / "plans/round41_c1_verify.py")
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
ROOT.mkdir(parents=True, exist_ok=True)
fixtures, side = c1.build_battery(BAT, ROOT, LANE)
runner = c1.Runner(ROOT, 8)
srcs = {t: (LANE / rel).read_text() for t, rel in c1.TOOLS.items()}
vdir = ROOT / "variants"
vdir.mkdir(exist_ok=True)
for tool in c1.TOOLS:
    (vdir / f"ref-{tool}.py").write_text(srcs[tool])
MUT = {m[0]: m for m in c1.MUTANTS}
TARGETS = ["S02", "S03", "S05", "S06"]


def run(tool, variant, fx, hide_lane=False):
    n = next(runner.seq)
    work = ROOT / "work" / f"x{n:06d}"
    tmp = ROOT / "rtmp" / f"y{n:06d}"
    work.mkdir(); tmp.mkdir()
    argv = []
    for t in fx["argv"]:
        m = c1.WORK_TOKEN.match(t)
        argv.append(str(work / "run") + (m.group(2) or "") if m else t)
    slot = runner.slots / f"{tool}.py"
    cmd = c1.ro_sandbox(writable=(work, tmp), ro_binds=((variant, slot),),
                        hide=(LANE,) if hide_lane else ()) + [c1.PY, str(slot), *argv]
    r = subprocess.run(cmd, cwd=str(fx["dir"]), env=runner.env(tmp), capture_output=True, text=True, timeout=600)
    shutil.rmtree(work, ignore_errors=True); shutil.rmtree(tmp, ignore_errors=True)
    return r.returncode, r.stdout, r.stderr


def marker(text, marker_text, repl):
    assert text.count(marker_text) == 1, (marker_text, text.count(marker_text))
    return text.replace(marker_text, repl, 1)


for fx in fixtures:
    print("\n--- CONTENT %s" % fx["fid"], flush=True)
    for p in sorted(fx["dir"].rglob("*")):
        if p.is_file():
            print("FILE %s" % p.relative_to(fx["dir"]), flush=True)
            print(p.read_text(errors="replace"), flush=True)

print("\n=== TRACE MATRIX (mutant line executed? / ref guard reached?)", flush=True)
for mid in TARGETS:
    _id, tool, _cls, direction, _ak, _lbl, _w, old, new = MUT[mid]
    mtext = srcs[tool].replace(old, new, 1)
    if mid == "S06":
        ttext = marker(mtext, '    if False and (',
                       '    if (print("TRACE-MUT %s", file=sys.stderr) or False) and (' % mid)
        rprobe = ('    print("TRACE-REF S06 recheck=%r" % (args.recheck,), file=sys.stderr)\n')
    else:
        ttext = marker(mtext, '    if False:',
                       '    if (print("TRACE-MUT %s", file=sys.stderr) or False):' % mid)
        rprobe = {
            "S02": '    print("TRACE-REF S02 registry=%r package=%r" % (args.registry, args.package), file=sys.stderr)\n',
            "S03": '    print("TRACE-REF S03 access_date=%r" % (args.access_date,), file=sys.stderr)\n',
            "S05": '    print("TRACE-REF S05 entries=%r" % (args.entries,), file=sys.stderr)\n',
        }[mid]
    rtext = marker(srcs[tool], old, rprobe + old)
    mp = vdir / f"{mid}-m.py"; mp.write_text(mtext)
    tp = vdir / f"{mid}-t.py"; tp.write_text(ttext)
    rp = vdir / f"{mid}-r.py"; rp.write_text(rtext)
    print("\n## %s direction=%s" % (mid, direction), flush=True)
    for fx in [f for f in fixtures if f["tool"] == tool]:
        ref = run(tool, vdir / f"ref-{tool}.py", fx)
        mut = run(tool, mp, fx)
        tr = run(tool, tp, fx)
        rt = run(tool, rp, fx)
        refhide = run(tool, vdir / f"ref-{tool}.py", fx, hide_lane=True)
        ex = c1.exhibits(MUT[mid][2], direction, fx, (ref[0], c1.classes(tool, ref[1])),
                         (mut[0], c1.classes(tool, mut[1])))
        tline = [l for l in tr[2].splitlines() if l.startswith("TRACE-MUT")]
        rline = [l for l in rt[2].splitlines() if l.startswith("TRACE-REF")]
        print("FX %-52s ref=%d refhide=%d mut=%d exhibits=%s mutline=%s refline=%s"
              % (fx["fid"], ref[0], refhide[0], mut[0], ex, tline or "-", rline or "-"), flush=True)
        if ex:
            print("   mut_stdout=%r" % mut[1][-500:], flush=True)
