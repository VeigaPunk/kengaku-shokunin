#!/usr/bin/env python3
"""Standalone probe of the C1 counter's ro_sandbox(): writes, network, /dev, /proc, /run, lane,
variant-store visibility, fd binding, process survival, cross-dir hardlink write.

Orchestrator (runs in the seat envelope) -> inner payload (runs in a sandbox built by the frozen
counter's own ro_sandbox), results JSON out to a rw-bound dir.
"""
import json, os, subprocess, sys, time

PLANS = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans"
sys.path.insert(0, PLANS)
import round42_c1_verify as C  # read-only use of the frozen counter's ro_sandbox

S = "/fast/scratch/hyaku/kengaku-r42/R42SentinelCounter/probe"
LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
OUT = f"{S}/out"
TMP = f"{S}/tmp"
HID = [f"{S}/fake/variants", f"{S}/fake/slots", f"{S}/fake/bin", f"{S}/fake/tracer"]
A = f"{S}/moduleA"
TAG = "k42canaryA7f3"


def inner():
    res = {}
    res["uid"] = [os.getuid(), os.geteuid()]
    res["uid_map"] = open("/proc/self/uid_map").read().strip()
    res["cwd"] = os.getcwd()
    res["writes"] = {}
    for p in ("/etc/p42probe", "/usr/local/bin/p42probe", "/usr/bin/p42probe",
              "/home/vgpnk/.local/bin/p42probe", "/home/vgpnk/.p42probe", "/tmp/p42probe",
              "/fast/scratch/p42probe", f"{LANE}/p42probe", f"{A}/p42probe",
              "/dev/shm/p42probe", "/run/p42probe", f"{OUT}/ok",
              "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/p42probe"):
        try:
            with open(p, "w") as fh:
                fh.write("x")
            res["writes"][p] = "WROTE"
        except OSError as e:
            res["writes"][p] = type(e).__name__ + ":" + (e.strerror or "")
    res["net"] = {}
    import socket
    for fam, addr in ((socket.AF_INET, ("1.1.1.1", 443)), (socket.AF_INET, ("127.0.0.1", 22)),
                      (socket.AF_INET6, ("::1", 22))):
        s = socket.socket(fam, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            res["net"][str(addr)] = s.connect_ex(addr)
        except OSError as e:
            res["net"][str(addr)] = type(e).__name__ + ":" + (e.strerror or "")
        finally:
            s.close()
    try:
        res["dns"] = socket.getaddrinfo("example.com", 80)[0][4]
    except OSError as e:
        res["dns"] = type(e).__name__ + ":" + (e.strerror or "")
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect("/run/user/1000/bus")
        res["unix_runuser"] = "CONNECTED"
    except OSError as e:
        res["unix_runuser"] = type(e).__name__ + ":" + (e.strerror or "")
    finally:
        s.close()
    res["shm"] = os.path.isdir("/dev/shm")
    res["shm_list"] = sorted(os.listdir("/dev/shm"))[:8] if res["shm"] else None
    res["run_list"] = sorted(os.listdir("/run"))[:12]
    res["dev_list"] = sorted(os.listdir("/dev"))[:20]
    pids = sorted(int(p) for p in os.listdir("/proc") if p.isdigit())
    res["pids"] = pids
    res["proc1_cmdline"] = open("/proc/1/cmdline", "rb").read()[:80].decode("utf-8", "replace")
    res["nproc_root_entries"] = len(os.listdir("/proc"))
    res["fd"] = sorted(os.listdir("/proc/self/fd"))
    res["slot_read"] = None
    try:
        res["slot_read"] = open("/run/k42slot.py").read()[:40]
    except OSError as e:
        res["slot_read"] = type(e).__name__
    res["lane_exists"] = os.path.isdir(LANE)
    res["lane_entries"] = len(os.listdir(LANE)) if res["lane_exists"] else None
    res["lane_counter_readable"] = os.path.isfile(f"{LANE}/plans/round42_c1_verify.py")
    res["hidden"] = {h: os.path.exists(h) for h in HID}
    res["a_visible"] = os.path.isfile(f"{A}/flag.txt")
    # cross-dir write: hardlink a file that lives in a read-only mount into the rw out dir
    hl = {"link": None, "write": None, "after": None}
    try:
        os.link(f"{A}/flag.txt", f"{OUT}/linked.txt")
        hl["link"] = "LINKED"
        with open(f"{OUT}/linked.txt", "w") as fh:
            fh.write("pwned")
        hl["write"] = "WROTE"
    except OSError as e:
        hl["link"] = hl["link"] or (type(e).__name__ + ":" + (e.strerror or ""))
        hl["write"] = type(e).__name__ + ":" + (e.strerror or "")
    try:
        hl["after"] = open(f"{A}/flag.txt").read()
    except OSError as e:
        hl["after"] = type(e).__name__
    res["hardlink"] = hl
    # process survival: a child that outlives this process
    child = subprocess.Popen(["/usr/bin/python3", "-c",
                              f"import time\ntime.sleep(240)  # {TAG}"],
                             start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    res["spawned"] = child.pid
    with open("/proc/self/stat", "r") as fh:
        res["self_stat"] = fh.read().split()[0]
    with open(f"{OUT}/results.json", "w") as fh:
        json.dump(res, fh, indent=1)
    return 0


def main():
    if "--inner" in sys.argv:
        return inner()
    import shutil
    shutil.rmtree(S, ignore_errors=True)
    for d in (OUT, TMP, A, *HID):
        os.makedirs(d, exist_ok=True)
    open(f"{A}/flag.txt", "w").write("clean")
    for h in HID:
        open(f"{h}/marker", "w").write("keep")
    slot = f"{S}/fake-slot-src.py"
    open(slot, "w").write("# slot content\n")
    fd = os.open(slot, os.O_RDONLY)
    argv = C.ro_sandbox(writable=(OUT, TMP), hide=HID,
                        ro_data=((fd, "/run/k42slot.py"),)) + ["/usr/bin/python3", __file__, "--inner"]
    env = {"PATH": C.PATH, "HOME": "/nonexistent", "TMPDIR": TMP, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    r = subprocess.run(argv, cwd=OUT, env=env, capture_output=True, text=True, pass_fds=(fd,), timeout=300)
    os.close(fd)
    print("INNER-RC", r.returncode)
    if r.stderr.strip():
        print("INNER-STDERR", r.stderr.strip()[-800:])
    print(open(f"{OUT}/results.json").read() if os.path.isfile(f"{OUT}/results.json") else "NO-RESULTS")
    print("A-FLAG-AFTER", repr(open(f"{A}/flag.txt").read()))
    time.sleep(1)
    p = subprocess.run(["pgrep", "-af", TAG], capture_output=True, text=True)
    print("SURVIVORS", p.stdout.strip() or "none")
    return 0


sys.exit(main())
