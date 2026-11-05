import importlib.util, json, os, subprocess
from pathlib import Path

L = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location("probe", L / "plans/round86_raman_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

work = Path("/fast/scratch/hyaku/kengaku-r86/SentinelR86/sandbox-demo")
case = work / "case"
(case / "app").mkdir(parents=True, exist_ok=True)
(case / "harness.py").write_text("pass\n", encoding="utf-8")

argv = probe.sandbox_argv(L / probe.CAP, case)
print("ARGV:", json.dumps(argv))

SCRIPT = r'''
echo "uid: $(id)"
echo "--- env:"
env | sort
echo "--- root listing:"; ls -A /
echo "--- app:"; ls -A /app
echo "--- tests:"; ls -A /tests
echo "--- home?"; ls -d /home 2>&1 || true
echo "--- lane path?"; ls -d /home/vgpnk 2>&1 || true
echo "--- tmp?"; ls -d /tmp 2>&1 || true
echo "--- shadow:"; head -c 20 /etc/shadow 2>&1 || true
echo "--- machine-id:"; head -c 12 /etc/machine-id 2>&1 || true
echo "--- proc netdev:"; cat /proc/net/dev 2>&1 || true
echo "--- status:"; grep -E '^(Cap|NoNewPrivs|Seccomp)' /proc/self/status
echo "--- write /app:"; (echo sandbox > /app/from-sandbox.txt && echo wrote-app) 2>&1 || true
echo "--- write /usr:"; (echo x > /usr/from-sandbox.txt && echo wrote-usr) 2>&1 || true
echo "--- write /etc:"; (echo x > /etc/from-sandbox.txt && echo wrote-etc) 2>&1 || true
echo "--- write /:"; (echo x > /rootfs.txt && echo wrote-root) 2>&1 || true
echo "--- parent pid:"; ls /proc | grep -c '^[0-9]*$' || true
'''

out = subprocess.run(argv[:-4] + ["/bin/sh", "-c", SCRIPT], capture_output=True, text=True)
print("shell rc:", out.returncode)
print(out.stdout)
print("STDERR:", out.stderr.strip()[:800])

NET = ("import socket;print('ifaces', socket.if_nameindex());"
       "print('routes', open('/proc/net/route').read().strip())")
net = subprocess.run(argv[:-4] + ["/usr/bin/python3", "-I", "-B", "-c", NET],
                     capture_output=True, text=True)
print("net rc:", net.returncode)
print(net.stdout)
print("net stderr:", net.stderr.strip()[:400])

print("host /app/from-sandbox.txt exists:", Path("/app/from-sandbox.txt").exists())
print("case app after:", sorted(os.listdir(case / "app")))
print("rootfs.txt in work:", (work / "rootfs.txt").exists())
