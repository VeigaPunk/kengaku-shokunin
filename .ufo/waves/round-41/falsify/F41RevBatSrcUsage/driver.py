#!/usr/bin/env python3
"""Non-author trace driver: rebuilds s_usage fixtures, runs ref/mutant/traced variants, per-fixture exhibits."""
import importlib.util, itertools, json, pathlib, shutil, subprocess, sys

LANE = pathlib.Path(sys.argv[1]).resolve()
ROOT = pathlib.Path(sys.argv[2]).resolve()
BAT = pathlib.Path(sys.argv[3]).resolve()

spec = importlib.util.spec_from_file_location("c1", LANE / "plans/round41_c1_verify.py")
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

ROOT.mkdir(parents=True, exist_ok=True)
fixtures, side = c1.build_battery(BAT, ROOT, LANE)
print("BUILD fixtures=%d sidechannel=%d" % (len(fixtures), side), flush=True)
for fx in fixtures:
    print("FX %s dir=%s argv=%s" % (fx["fid"], fx["dir"], json.dumps(fx["argv"])), flush=True)

runner = c1.Runner(ROOT, 8)
srcs = {tool: (LANE / rel).read_text() for tool, rel in c1.TOOLS.items()}
vdir = ROOT / "variants"
vdir.mkdir(exist_ok=True)
refpath = {}
for tool in c1.TOOLS:
    p = vdir / f"ref-{tool}.py"
    p.write_text(srcs[tool])
    refpath[tool] = p

MUT = {m[0]: m for m in c1.MUTANTS}
TARGETS = ["S02", "S03", "S05", "S06"]


def run(tool, variant, fx, hide_lane=False):
    n = next(runner.seq)
    work = ROOT / "work" / f"x{n:06d}"
    tmp = ROOT / "rtmp" / f"y{n:06d}"
    work.mkdir()
    tmp.mkdir()
    argv = []
    for t in fx["argv"]:
        m = c1.WORK_TOKEN.match(t)
        if m:
            w = work / "run"
            if m.group(1):
                (w / m.group(1)).mkdir(parents=True, exist_ok=True)
            if m.group(2):
                w.mkdir(exist_ok=True)
            argv.append(str(w) + (m.group(2) or ""))
        else:
            argv.append(t)
    slot = runner.slots / f"{tool}.py"
    hide = (LANE,) if hide_lane else ()
    cmd = c1.ro_sandbox(writable=(work, tmp), ro_binds=((variant, slot),), hide=hide) + [c1.PY, str(slot), *argv]
    try:
        r = subprocess.run(cmd, cwd=str(fx["dir"]), env=runner.env(tmp), capture_output=True, text=True,
                           timeout=600)
        return r.returncode, r.stdout, r.stderr
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)


def mut_src(mid):
    _id, tool, _cls, _dirn, _ak, _lbl, _w, old, new = MUT[mid]
    src = srcs[tool]
    assert src.count(old) == 1, (mid, src.count(old))
    return tool, old, new, src.replace(old, new, 1)


def trace_mut(mid):
    """Insert a print ON the mutated line; semantics unchanged (print(...) or False)."""
    tool, old, new, text = mut_src(mid)
    if mid == "S06":
        marker = '    if False and ('
        repl = ('    if (print("TRACE-MUT ' + mid + ' line executed", file=sys.stderr) or False) and (')
    else:
        marker = '    if False:'
        repl = '    if (print("TRACE-MUT ' + mid + ' line executed", file=sys.stderr) or False):'
    assert text.count(marker) == 1, (mid, "marker", text.count(marker))
    return tool, text.replace(marker, repl, 1)


def trace_ref(mid):
    """Print the operands immediately before the reference guard."""
    _id, tool, _cls, _dirn, _ak, _lbl, _w, old, new = MUT[mid]
    if mid == "S02":
        probe = '    print("TRACE-REF S02 registry=%r package=%r" % (args.registry, args.package), file=sys.stderr)\n'
    elif mid == "S03":
        probe = '    print("TRACE-REF S03 access_date=%r" % (args.access_date,), file=sys.stderr)\n'
    elif mid == "S05":
        probe = '    print("TRACE-REF S05 entries=%r admit=%r" % (args.entries, args.admit_ids), file=sys.stderr)\n'
    else:
        probe = '    print("TRACE-REF S06 recheck=%r" % (args.recheck,), file=sys.stderr)\n'
    text = srcs[tool]
    assert text.count(old) == 1
    return tool, text.replace(old, probe + old, 1)


effects = {}
for mid in TARGETS:
    tool, old, new, mtext = mut_src(mid)
    mp = vdir / f"{mid}.py"
    mp.write_text(mtext)
    ttool, ttext = trace_mut(mid)
    tp = vdir / f"{mid}-trace.py"
    tp.write_text(ttext)
    rtool, rtext = trace_ref(mid)
    rp = vdir / f"{mid}-reftrace.py"
    rp.write_text(rtext)
    fid_dirn = MUT[mid][3]
    print("\n===== %s direction=%s" % (mid, fid_dirn), flush=True)
    for fx in [f for f in fixtures if f["tool"] == tool]:
        ref = run(tool, refpath[tool], fx)
        mut = run(tool, mp, fx)
        tr = run(tool, tp, fx)
        rt = run(tool, rp, fx)
        hid = run(tool, mp, fx, hide_lane=True)
        ex = c1.exhibits(MUT[mid][2], fid_dirn, fx, (ref[0], c1.classes(tool, ref[1])),
                         (mut[0], c1.classes(tool, mut[1])))
        effects[(mid, fx["fid"])] = (ref, mut, tr, rt, hid, ex)
        print("FX %s ref_rc=%d mut_rc=%d exhibits=%s lane_hidden_mut_rc=%d" % (fx["fid"], ref[0], mut[0], ex, hid[0]))
        print("  REF stdout: %r" % ref[1][:400])
        print("  REF stderr: %r" % ref[2][-400:])
        print("  MUT stdout: %r" % mut[1][:400])
        print("  MUT stderr tail: %r" % mut[2][-300:])
        print("  MUT-TRACE stderr tail: %r" % tr[2][-300:])
        print("  REF-TRACE stderr tail: %r" % rt[2][-300:])
        print("  LANE-HIDDEN mut stdout: %r" % hid[1][:200])
        print("  LANE-HIDDEN mut stderr tail: %r" % hid[2][-200:])
        sys.stdout.flush()

# control: S03 date sensitivity on the duplicate-request fixture
print("\n===== CONTROL S03 duplicate fixture with a VALID date (mutant)", flush=True)
tool, old, new, _ = mut_src("S03")
mp = vdir / "S03.py"
dupfx = [f for f in fixtures if f["fid"] == "s_usage-03-single-digit-month-duplicate-request"][0]
for label, argv in (
        ("mutant+dupid+valid-date-verbatim", None),
        ("mutant+dupid+date-fixed", ["--registry", None, "--package", None, "--admit-ids", "S131,S131",
                                     "--entries", "corpus/knowledge/tb2-constraints-scheduling-grader.md",
                                     "--access-date", "2026-10-26"]),
):
    fx = dict(dupfx)
    if argv is None:
        fx = dupfx
    else:
        import re as _re
        reg = [t for t in dupfx["argv"] if t.endswith("SOURCES.md")][0]
        pkg = [t for t in dupfx["argv"] if t.endswith("SOURCES.append.md")][0]
        fx["argv"] = ["--registry", reg, "--package", pkg, "--admit-ids", "S131,S131",
                      "--entries", "corpus/knowledge/tb2-constraints-scheduling-grader.md",
                      "--access-date", "2026-10-26"]
    ref = run(tool, refpath[tool], fx)
    mut = run(tool, mp, fx)
    print("%s ref_rc=%d mut_rc=%d mut_stdout=%r mut_stderr=%r" % (label, ref[0], mut[0], mut[1][:200],
                                                                  mut[2][-200:]), flush=True)

# control: S03 dated fixture with valid date (mutant should succeed)
print("\n===== CONTROL S03 dotted fixture with a VALID date (mutant)", flush=True)
dotfx = [f for f in fixtures if f["fid"] == "s_usage-03-dotted-access-date"][0]
reg = [t for t in dotfx["argv"] if t.endswith("SOURCES.md")][0]
pkg = [t for t in dotfx["argv"] if t.endswith("SOURCES.append.md")][0]
fx = dict(dotfx)
fx["argv"] = ["--registry", reg, "--package", pkg, "--admit-ids", "S131,S132", "--entries",
              "corpus/knowledge/tb2-constraints-scheduling-grader.md", "--access-date", "2026-10-26"]
print("ref rc=%d mut rc=%d mut_stdout=%r" % (run("sources", refpath["sources"], fx)[0],
                                             run("sources", mp, fx)[0],
                                             run("sources", mp, fx)[1][:300]), flush=True)

# control: S05 empty-string entries with entries map / b05b mutant
print("\n===== CONTROL S05 b05b mutant output", flush=True)
print(repr(run("sources", vdir / "S05.py",
               [f for f in fixtures if f["fid"] == "s_usage-05-empty-entries-value"][0])[1][:400]), flush=True)

print("\n===== EXHIBIT MATRIX", flush=True)
for mid in TARGETS:
    row = ["%s:%s" % (f["fid"], effects[(mid, f["fid"])][5]) for f in fixtures if f["tool"] == "sources"]
    print(mid, " ".join(row), flush=True)
