#!/usr/bin/env python3
"""Probe 2: hide semantics (contents vs existence), build-mode lane hide, tracer visibility,
hardlink EXDEV control (same operation outside the sandbox)."""
import json, os, shutil, subprocess, sys

PLANS = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans"
sys.path.insert(0, PLANS)

S = "/fast/scratch/hyaku/kengaku-r42/R42SentinelCounter/probe2"
LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
OUT, TMP = f"{S}/out", f"{S}/tmp"
HID = [f"{S}/fake/variants", f"{S}/fake/slots", f"{S}/fake/bin", f"{S}/fake/tracer"]
A = f"{S}/moduleA"
BIN = f"{S}/fake/bin/builder.py"


def inner():
    res = {}
    res["hidden_listdir"] = {h: (sorted(os.listdir(h)) if os.path.isdir(h) else "ABSENT") for h in HID}
    res["caps"] = [l.strip() for l in open("/proc/self/status") if l.startswith("Cap")]
    res["uid"] = [os.getuid(), os.geteuid()]
    # can the child re-mount a read-only path writable (needs CAP_SYS_ADMIN in its own user ns)?
    rb = {}
    for spec in (["--bind", A, A], ["-o", "remount,rw", A]):
        r = subprocess.run(["/usr/bin/mount", *spec], capture_output=True, text=True)
        rb[" ".join(spec)] = [r.returncode, r.stderr.strip()[:100]]
    try:
        with open(f"{A}/flag.txt", "w") as fh:
            fh.write("remounted-write")
        rb["write"] = "WROTE:" + open(f"{A}/flag.txt").read()
    except OSError as e:
        rb["write"] = type(e).__name__ + ":" + (e.strerror or "")
    try:
        with open(f"{A}/newfile", "w") as fh:
            fh.write("new")
        rb["create"] = "CREATED"
    except OSError as e:
        rb["create"] = type(e).__name__ + ":" + (e.strerror or "")
    res["remount"] = rb
    hl2 = {}
    try:
        open(f"{OUT}/self.txt", "w").write("a")
        os.link(f"{OUT}/self.txt", f"{OUT}/self2.txt")
        open(f"{OUT}/self2.txt", "w").write("b")
        hl2["same_rw_mount"] = "LINKED:" + open(f"{OUT}/self.txt").read()
    except OSError as e:
        hl2["same_rw_mount"] = type(e).__name__ + ":" + (e.strerror or "")
    try:
        os.link(f"{A}/probe2src.txt", f"{OUT}/cross.txt")
        hl2["ro_to_rw"] = "LINKED"
    except OSError as e:
        hl2["ro_to_rw"] = type(e).__name__ + ":" + (e.strerror or "")
    res["hardlink2"] = hl2
    res["bin_read"] = None
    try:
        res["bin_read"] = open(BIN).read()[:30]
    except OSError as e:
        res["bin_read"] = type(e).__name__
    res["bin_via_dir"] = os.path.isdir(f"{S}/fake/bin")
    res["lane_isdir"] = os.path.isdir(LANE)
    res["lane_listdir"] = sorted(os.listdir(LANE))[:15] if res["lane_isdir"] else "ABSENT"
    res["lane_counter"] = os.path.isfile(f"{LANE}/plans/round42_c1_verify.py")
    res["tracer"] = None
    try:
        res["tracer"] = open("/run/k42-tracer.py").read()[:40]
    except OSError as e:
        res["tracer"] = type(e).__name__
    res["argv"] = sys.argv
    with open(f"{OUT}/r2.json", "w") as fh:
        json.dump(res, fh, indent=1)
    return 0


def run(label, extra_hide, with_tracer):
    import round42_c1_verify as C
    tsrc = open(f"{S}/tracer-src.py", "rb")
    fd = tsrc.fileno()
    kw = {"writable": (OUT, TMP), "hide": HID + list(extra_hide),
          "ro_data": ((fd, "/run/k42-tracer.py"),) if with_tracer else ()}
    argv = C.ro_sandbox(**kw) + ["/usr/bin/python3", __file__, "--inner"]
    env = {"PATH": C.PATH, "HOME": "/nonexistent", "TMPDIR": TMP, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    r = subprocess.run(argv, cwd=OUT, env=env, capture_output=True, text=True,
                       pass_fds=((fd,) if with_tracer else ()), timeout=120)
    print(f"== {label} rc={r.returncode} stderr={r.stderr.strip()[-300:]}")
    print(open(f"{OUT}/r2.json").read() if os.path.isfile(f"{OUT}/r2.json") else "NO-RESULTS")
    os.unlink(f"{OUT}/r2.json")
    tsrc.close()


def main():
    shutil.rmtree(S, ignore_errors=True)
    for d in (OUT, TMP, A, *HID):
        os.makedirs(d, exist_ok=True)
    for h in HID:
        open(f"{h}/marker", "w").write("keep")
    open(BIN, "w").write("# builder copy: MUTANTS table lives here\n")
    open(f"{S}/tracer-src.py", "w").write("# tracer body\n")
    open(f"{A}/probe2src.txt", "w").write("src")
    open(f"{A}/flag.txt", "w").write("clean")
    # control: same hardlink, no sandbox
    try:
        os.link(f"{A}/flag.txt", f"{OUT}/plain-link.txt")
        print("CONTROL-HARDLINK LINKED, after-write:", end=" ")
        open(f"{OUT}/plain-link.txt", "w").write("pwned")
        print(repr(open(f"{A}/flag.txt").read()))
    except OSError as e:
        print("CONTROL-HARDLINK", type(e).__name__, e.strerror)
    try:
        os.link(f"{A}/flag.txt", f"{OUT}/plain2.txt")
    except OSError as e:
        print("CONTROL-HARDLINK2", type(e).__name__, e.strerror)
    print("stat devices:", os.stat(f"{A}/flag.txt").st_dev, os.stat(f"{OUT}").st_dev)
    run("tool-run-hide", (), True)
    run("build-run-hide-lane", (LANE,), False)
    return 0


if "--inner" in sys.argv:
    sys.exit(inner())
sys.exit(main())
