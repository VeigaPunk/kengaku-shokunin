#!/usr/bin/env python3
"""SentinelProbe-5: adversarial verification of plans/round96_merger_probe.py's sandbox.

Reuses the probe's own Box.cmd argv builder (imported from the T clone). Every payload
prints names / counts / errnos / booleans only -- never environment values.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r96/SentinelProbe")
LANE = S / "lane"
OUT = S / "out"
PL = S / "pl"
CAP = LANE / "corpus/evidence/round96/graders/multi-source-data-merger"
CANARY = "CANARY_SENTINEL_R96"

spec = importlib.util.spec_from_file_location("probe96", LANE / "plans" / "round96_merger_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

E = (S / "E").resolve()
G = (S / "G").resolve()
STORE = probe.interpreter_root(E)
ro_trees = sorted({str(E), str(G), STORE, probe.interpreter_root(G)})
box = probe.Box("/usr/bin/bwrap", ro_trees)
print("RO_TREES", ro_trees)

(PL).mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
(S / "wk/harness_demo.py").write_text("print('demo')\n", encoding="utf-8")
(S / "wk/tests/dummy.txt").write_text("x\n", encoding="utf-8")
(S / "wk/appdemo/preexisting.txt").write_text("x\n", encoding="utf-8")

os.environ[CANARY] = "host-shell-value-never-printed"


def payload(name: str, src: str) -> Path:
    p = PL / name
    p.write_text(src, encoding="utf-8")
    return p


def build(kind: str, extra_binds):
    if kind == "agent":
        binds = [("--bind", str(S / "wk/appdemo"), "/app"),
                 ("--ro-bind", str(CAP / "environment/data"), "/data")]
        path, py = "%s/bin:/usr/bin" % E, probe.venv_python(E)
    else:
        binds = [("--bind", str(S / "wk/appdemo"), "/app"),
                 ("--ro-bind", str(S / "wk/tests"), "/tests"),
                 ("--ro-bind", str(S / "wk/harness_demo.py"), "/harness.py")]
        path, py = "%s/bin:/usr/bin" % G, probe.venv_python(G)
    binds = binds + list(extra_binds)
    argv = [str(py), "-I", "-B", "/payload.py"]
    return box.cmd(binds, "/app", path, argv)


def run(kind: str, pl: Path, receipt: str, clearenv: bool = True, extra_binds=()) -> None:
    cmd = build(kind, [("--ro-bind", str(pl), "/payload.py")] + list(extra_binds))
    if not clearenv:
        cmd = [c for c in cmd if c != "--clearenv"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    (OUT / receipt).write_text(
        "CLEARENV %s\nRC %d\nSTDOUT\n%s\nSTDERR\n%s" % (clearenv, proc.returncode,
                                                        proc.stdout, proc.stderr),
        encoding="utf-8")
    print("RAN", receipt, "rc", proc.returncode, "stdout_lines", len(proc.stdout.splitlines()))


P_ENV = """
import os
names = sorted(os.environ)
print("ENV_COUNT", len(names))
for k in names:
    print("ENV_NAME", k, "value_len", len(os.environ.get(k, "")))
print("CANARY_PRESENT", %(can)r in os.environ)
""" % {"can": CANARY}

P_MOUNT = """
import os, socket
u = os.uname()
print("UNAME", u.sysname, u.release, u.machine)
print("HOSTNAME", socket.gethostname())
print("PID_ENTRIES", len([x for x in os.listdir('/proc') if x.isdigit()]))
print("ROOT_LIST", sorted(os.listdir('/')))
try:
    print("SYS_PRESENT", os.path.isdir('/sys'))
except OSError as e:
    print("SYS_ERRNO", e.errno)
with open('/proc/self/mountinfo') as f:
    for ln in f:
        print("MNT", ln.rstrip("\\n"))
"""

P_ETC_HOME = """
import os
for p in ["/etc", "/etc/passwd", "/etc/resolv.conf", "/etc/hostname", "/home",
          "/home/vgpnk", "/home/vgpnk/.ssh", "/root", "/var", "/opt", "/srv", "/run"]:
    try:
        os.stat(p)
        print("EXISTS", p)
    except OSError as e:
        print("ABSENT", p, "errno", e.errno)
for p in ["/home/vgpnk/.ssh/id_rsa", "/home/vgpnk/.netrc", "/home/vgpnk/.git-credentials",
          "/home/vgpnk/.config/gh/hosts.yml", "/home/vgpnk/.aws/credentials",
          "/home/vgpnk/.local/share/uv/uv-cache", "/root/.bash_history"]:
    print("CRED_PATH", p, "visible" if os.path.exists(p) else "absent")
"""

P_WRITE = """
import os
targets = ["/data/SENTINEL", "/usr/SENTINEL", "/usr/local/SENTINEL",
           %(store)s,
           %(e)s, %(g)s,
           "/tests/SENTINEL", "/tmp/SENTINEL", "/app/SENTINEL",
           "/etc/SENTINEL", "/root/SENTINEL", "/var/SENTINEL"]
for t in targets:
    try:
        with open(t, "w") as f:
            f.write("x")
        print("WRITE_OK", t)
    except OSError as e:
        print("WRITE_DENIED", t, "errno", e.errno, os.strerror(e.errno))
try:
    with open("/harness.py", "a") as f:
        f.write("# x")
    print("WRITE_OK /harness.py")
except OSError as e:
    print("WRITE_DENIED /harness.py", "errno", e.errno, os.strerror(e.errno))
""" % {"store": repr(str(STORE)), "e": repr(str(E)), "g": repr(str(G))}

P_NET = """
import os, socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
rc = s.connect_ex(("127.0.0.1", 1))
print("CONNECT_LO", rc, "connected" if rc == 0 else os.strerror(rc))
rc = s.connect_ex(("1.1.1.1", 80))
print("CONNECT_EXT", rc, "connected" if rc == 0 else os.strerror(rc))
s.close()
try:
    ai = socket.getaddrinfo("example.com", 80)
    print("GETADDRINFO_OK", ai[0][4])
except OSError as e:
    print("GETADDRINFO_ERRNO", e.errno)
try:
    u = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    u.close()
    print("AF_UNIX_CREATE OK")
except OSError as e:
    print("AF_UNIX_ERRNO", e.errno)
try:
    print("IFACES", socket.if_nameindex())
except OSError as e:
    print("IFACES_ERRNO", e.errno)
try:
    print("SYS_NET", sorted(os.listdir("/sys/class/net")))
except OSError as e:
    print("SYS_NET_ERRNO", e.errno)
"""

P_CAPS = """
import os, socket, stat, subprocess
print("UID", os.getuid(), "GID", os.getgid())
for ln in open("/proc/self/status"):
    if ln.startswith(("CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb", "NoNewPrivs")):
        print("STATUS", ln.strip())
print("HOSTNAME", socket.gethostname())
r = subprocess.run(["/usr/bin/mount", "-o", "remount,rw", "/data"], capture_output=True, text=True)
print("REMOUNT_RW_DATA rc", r.returncode, "err", (r.stderr or r.stdout).strip()[:160])
r = subprocess.run(["/usr/bin/unshare", "-m", "/usr/bin/true"], capture_output=True, text=True)
print("UNSHARE_M rc", r.returncode, "err", (r.stderr or r.stdout).strip()[:160])
try:
    os.mknod("/tmp/sentinel_dev", 0o600 | stat.S_IFCHR, os.makedev(1, 3))
    print("MKNOD_OK")
    os.unlink("/tmp/sentinel_dev")
except OSError as e:
    print("MKNOD_ERRNO", e.errno, os.strerror(e.errno))
"""

P_STORE = """
import os
store = %(store)s
print("STORE_LIST", sorted(os.listdir(store)))
for p, tag in [("/home/vgpnk/.local/share/uv", "UV_ROOT"),
               ("/home/vgpnk/.local/share", "LOCAL_SHARE"),
               ("/home/vgpnk/.local", "LOCAL"),
               ("/home/vgpnk", "HOME_REAL")]:
    try:
        print(tag + "_LIST", sorted(os.listdir(p))[:30])
    except OSError as e:
        print(tag + "_ERRNO", e.errno)
""" % {"store": repr(str(STORE))}

P_USR_LOCAL = """
import os
for d in ("/usr/local", "/usr/local/bin", "/usr/local/etc", "/usr/local/src", "/usr/local/share"):
    try:
        print("UL", d, sorted(os.listdir(d))[:40])
    except OSError as e:
        print("UL_ERRNO", d, e.errno)
"""

# r0: exact argv receipts (agent-phase-like and grader-phase-like)
agent_cmd = build("agent", [("--ro-bind", str(PL / "env.py"), "/payload.py")])
grader_cmd = build("grader", [("--ro-bind", str(PL / "env.py"), "/payload.py")])
(OUT / "r0-argv.txt").write_text(
    "AGENT_PHASE_STYLE_ARGV\n%s\n\nGRADER_PHASE_STYLE_ARGV\n%s\n" % (" ".join(agent_cmd), " ".join(grader_cmd)),
    encoding="utf-8")

run("agent", payload("env.py", P_ENV), "r1-envnames-clearenv.txt", clearenv=True)
run("agent", payload("env.py", P_ENV), "r2-envnames-no-clearenv.txt", clearenv=False)
run("agent", payload("mount.py", P_MOUNT), "r3-mountinfo.txt")
run("agent", payload("etchome.py", P_ETC_HOME), "r4-etc-home.txt")
run("grader", payload("write.py", P_WRITE), "r5-writes.txt")
run("agent", payload("net.py", P_NET), "r6-net.txt")
run("agent", payload("caps.py", P_CAPS), "r7-caps-uid.txt")
run("agent", payload("store.py", P_STORE), "r8-store-visibility.txt")
run("agent", payload("usrlocal.py", P_USR_LOCAL), "r8b-usr-local.txt")

print("HOST_APPDEMO_AFTER", sorted(p.name for p in (S / "wk/appdemo").iterdir()))
