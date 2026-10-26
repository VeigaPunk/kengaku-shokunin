#!/usr/bin/env python3
"""Round 2 (persisted): mounts, host secrets, tty, proc-sys, dev-shm origin, capability state."""
import importlib.util, os, pathlib, shutil, subprocess, sys, tempfile

LANE, ROOT = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("probe", str(pathlib.Path(LANE) / "plans/constraints_probe.py"))
probe = importlib.util.module_from_spec(spec); sys.modules["probe"] = probe; spec.loader.exec_module(probe)
cap = pathlib.Path(LANE) / probe.CAP
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/tmp",
       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
HOSTILE = r'''
import os, socket, subprocess
def r(p):
    try: return open(p, "rb").read(80).decode("latin-1").strip()
    except Exception as e: return type(e).__name__ + str(getattr(e, "errno", ""))
def sh(c):
    p = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=20)
    return (p.returncode, (p.stdout + p.stderr).strip().replace("\n", " | ")[:300])
print("ID", sh("id")[1])
print("CAPS", [l.strip() for l in open("/proc/self/status") if l.startswith(("CapEff", "NoNewPrivs", "Seccomp:"))])
print("PID1", open("/proc/1/cmdline").read().replace("\0", " ").strip()[:90])
print("NPROC", len([d for d in os.listdir("/proc") if d.isdigit()]))
print("HOSTNAME", socket.gethostname())
print("MACHINEID", r("/etc/machine-id"))
print("SHADOW", r("/etc/shadow"))
print("USERS", r("/etc/passwd")[:40])
for p in ("/home", "/root", "/run", "/var", "/fast", "/sys", "/proc/1/root"):
    print("VISIBLE", p, os.path.exists(p))
for p in ("/usr/x", "/etc/x", "/cap/x", "/tmp/x", "/app/x", "/dev/shm/x", "/x", "/dev/x"):
    try: open(p, "w").write("x"); print("WRITE", p, "OK")
    except Exception as e: print("WRITE", p, type(e).__name__, getattr(e, "errno", ""))
print("SUDO", sh("/usr/bin/sudo -n id")[0:2])
print("SUID_MODES", sh("ls -ln /usr/bin/sudo /usr/bin/passwd")[1])
print("NESTED_USERNS", sh("unshare -U true"))
print("NESTED_USERNS_MOUNT", sh("unshare -Urm true"))
try:
    s = socket.create_connection(("1.1.1.1", 80), timeout=5); print("NET", "CONNECTED"); s.close()
except Exception as e: print("NET", type(e).__name__, str(e)[:60])
try:
    s = socket.create_connection(("127.0.0.1", 22), timeout=3); print("NET_LO", "CONNECTED"); s.close()
except Exception as e: print("NET_LO", type(e).__name__, str(e)[:60])
print("DNS", sh("python3 -c 'import socket;print(socket.gethostbyname(\"example.com\"))'")[0:2])
print("DEVTTY_OPEN", sh("python3 -c 'import os;os.close(os.open(\"/dev/tty\",os.O_RDWR));print(\"OK\")'")[0:2])
for l in open("/proc/self/mounts"):
    f = l.split()
    if f[1] in ("/", "/dev", "/dev/pts", "/proc", "/tmp", "/app", "/cap", "/usr", "/etc"):
        print("MOUNT", " ".join(f[:4]))
'''
w = pathlib.Path(tempfile.mkdtemp(prefix="hostile2-", dir=ROOT)); a = w / "app"; a.mkdir()
for n in probe.INPUTS: shutil.copyfile(cap / n, a / n)
(w / "recipe.sh").write_text(":\n"); (w / "harness.py").write_text(HOSTILE)
p = subprocess.run(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py", "grade"], env=ENV,
                   capture_output=True, text=True, timeout=180)
print("RC", p.returncode); print(p.stdout.strip()); print("STDERR", p.stderr[:300])
shutil.rmtree(w, ignore_errors=True)
