"""R37RevProbeCode: decisive per-case teardown test — does a case's server survive its bwrap exit?"""
import importlib.util
import pathlib
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
spec = importlib.util.spec_from_file_location("probe", LANE + "/plans/git_webserver_probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules["probe"] = probe
spec.loader.exec_module(probe)
cap = pathlib.Path(LANE) / probe.CAP
root = pathlib.Path(sys.argv[1])


def pgrep_servers(tag):
    r = subprocess.run(["pgrep", "-af", "server.py"], capture_output=True, text=True)
    print(f"pgrep[{tag}]: " + (r.stdout.strip() or "(none)"))
    return r.stdout.strip()


case = next(c for c in probe.CASES if c.cid == "static-file-no-git")
rc, out = probe.run_case(cap, root, case)
print("case1 done rc=%d verdict=%s" % (rc, [l for l in out.splitlines() if l.startswith("VERDICT ")]))
time.sleep(0.5)
alive1 = pgrep_servers("after-case1")
rc, out = probe.run_case(cap, root, case)
print("case2 done rc=%d" % rc)
time.sleep(0.5)
alive2 = pgrep_servers("after-case2")
for pidline in (alive1 + "\n" + alive2).splitlines():
    pid = pidline.split()[0] if pidline.strip() else ""
    if pid.isdigit():
        ns = pathlib.Path(f"/proc/{pid}/ns/pid")
        try:
            print(f"survivor {pid}: ns={ns.resolve()}" + ("" if ns.exists() else " (gone)"))
        except OSError as e:
            print(f"survivor {pid}: unreadable {type(e).__name__}")
print("host pid ns: " + str(pathlib.Path("/proc/self/ns/pid").resolve()))
