#!/usr/bin/env python3
"""R46W2C3Sandbox: hostile-payload audit of plans/polyglot_c_py_probe.py's landed sandbox function.

Every sandbox invocation is `probe.sandbox_argv(cap, work)` (the landed function) + a command. Nothing in the lane is
edited; the probe module is imported from the TIP clone at $S/lane.
"""
import importlib.util
import os
import pathlib
import resource
import shutil
import subprocess
import sys
import tempfile
import threading
import time

LANE = pathlib.Path(sys.argv[1]).resolve()
S = pathlib.Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location("pgp", LANE / "plans/polyglot_c_py_probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules["pgp"] = probe
spec.loader.exec_module(probe)
CAP = LANE / probe.CAP


def memavail():
    for l in open("/proc/meminfo"):
        if l.startswith("MemAvailable:"):
            return int(l.split()[1]) // 1024
    return -1


def myrss():
    for l in open("/proc/self/status"):
        if l.startswith("VmRSS:"):
            return int(l.split()[1]) // 1024
    return -1


def tree_rss(root):
    """sum VmRSS (MiB) of root and all its descendants, from host /proc."""
    par, rss = {}, {}
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            st = open(f"/proc/{d}/status").read().splitlines()
        except OSError:
            continue
        p = r = None
        for l in st:
            if l.startswith("PPid:"):
                p = int(l.split()[1])
            elif l.startswith("VmRSS:"):
                r = int(l.split()[1])
        par[int(d)] = p
        rss[int(d)] = r or 0
    keep, changed = {root}, True
    while changed:
        changed = False
        for pid, pp in par.items():
            if pp in keep and pid not in keep:
                keep.add(pid)
                changed = True
    return sum(rss.get(k, 0) for k in keep) // 1024, len(keep)


def workdir():
    w = pathlib.Path(tempfile.mkdtemp(prefix="c3sb-", dir=S))
    (w / "app").mkdir()
    (w / "tests").mkdir()
    shutil.copyfile(CAP / "test_outputs.py", w / "tests/test_outputs.py")
    (w / "template.txt").write_text(probe.TEMPLATE)
    (w / "seed.sh").write_text("mkdir -p /app\n")
    (w / "recipe.sh").write_text(":\n")
    (w / "harness.py").write_text(probe.HARNESS_PY)
    return w


def run(payload, tag, timeout=120, argv_tail=None):
    w = workdir()
    argv = probe.sandbox_argv(CAP, w) + (argv_tail or ["/usr/bin/bash", "-c", payload])
    print(f"### {tag}")
    print("ARGV " + " ".join(argv))
    try:
        p = subprocess.run(argv, env=probe.ENV, capture_output=True, text=True, timeout=timeout)
        print(f"RC {p.returncode}")
        sys.stdout.write(p.stdout)
        if p.stderr:
            print("STDERR " + p.stderr.strip()[:3000])
    except subprocess.TimeoutExpired:
        print(f"RC timeout>{timeout}s")
    finally:
        shutil.rmtree(w, ignore_errors=True)
    print()


if "multi" in sys.argv:
    run(r"""
echo "= identity"
id
echo "= status"
grep -E '^(Uid|Gid|CapEff|CapBnd|NoNewPrivs|Seccomp|NSpid)' /proc/self/status
echo "= limits"
cat /proc/self/limits
echo "= ulimit -a"
ulimit -a
echo "= root listing"
ls -a /
echo "= pid1"
tr '\0' ' ' < /proc/1/cmdline; echo
echo "npids=$(ls /proc | grep -cE '^[0-9]+$')"
echo "= env"
env | sort
echo "= mounts"
cat /proc/self/mountinfo | sed -n '1,25p'
echo "= dev"
ls -l /dev
echo "= tty? "
if [ -e /dev/tty ]; then echo have-tty; else echo no-tty; fi
""", "S1 identity, limits, mounts, root listing")

    run(r"""
w() { if printf 'x' > "$1" 2>/dev/null; then echo "WROTE $1"; else echo "DENIED $1"; fi; }
mkdir -p /app && w /app/w_probe
for p in /w_root /etc/hostile /etc/passwd /usr/x /usr/bin/x /tests/x /pub/x /tpl/x /home/vgpnk/x \
         /home/vgpnk/.local/bin/x /root/x /proc/x /proc/sysrq-trigger /sys/x /dev/x /tmp/x \
         /app/../w_dotdot /app/../../w_dotdot2 /app/hl-escape; do w "$p"; done
echo "= mkdir outside"
for d in /etc/d /usr/d /home/vgpnk/.local/bin /app/d; do
  if mkdir -p "$d" 2>/dev/null; then echo "MKDIR $d"; else echo "NOMKDIR $d"; fi
done
echo "= etc read"
head -1 /etc/passwd
echo "shadow=$(python3 -c "print(open('/etc/shadow').readline().strip()[:12])" 2>&1 | tail -1)"
echo "= app write size"
dd if=/dev/zero of=/app/ddtest bs=1M count=4 2>&1 | tail -1
echo "= symlink out of app"
ln -s /home/vgpnk /app/hl 2>/dev/null; readlink /app/hl
python3 -c "import os;print('listdir(/app/hl)=',os.listdir('/app/hl')[:3])" 2>&1 | tail -1
ln -s /proc/1/root/app /app/hl2 2>/dev/null; python3 -c "import os;print('via-proc1root=',os.listdir('/app/hl2'))" 2>&1 | tail -1
echo "= host home forced"
HOME=/home/vgpnk python3 -c "open('/home/vgpnk/.local/bin/x','w')" 2>&1 | tail -1
""", "S2 write-outside-/app")

    run(r"""
echo "= home"
echo "HOME=$HOME"; echo "TMPDIR=$TMPDIR"
mkdir -p "$HOME/.local/bin" && echo "HOME-OK mkdir $HOME/.local/bin" || echo "HOME-DENY"
printf x > "$HOME/.local/bin/hostile" 2>/dev/null && echo "HOME-WROTE $HOME/.local/bin/hostile" || echo "HOME-WROTE-deny"
ls -l "$HOME/.local/bin" 2>&1 | head -3
echo "= network"
python3 - <<'PY'
import socket, sys
for fam, name in ((socket.AF_INET, "inet"), (socket.AF_INET6, "inet6")):
    try:
        s = socket.socket(fam, socket.SOCK_STREAM); s.settimeout(2)
        try:
            s.connect(("1.1.1.1", 80)); print(name, "connect inet ok")
        except OSError as e:
            print(name, "connect1.1.1.1", type(e).__name__, e.errno)
        if fam == socket.AF_INET:
            try:
                s.connect(("127.0.0.1", 22)); print(name, "connect lo ok")
            except OSError as e:
                print(name, "connect127.0.0.1", type(e).__name__, e.errno)
        s.close()
    except OSError as e:
        print(name, "socket", e.errno)
try:
    print("dns", socket.getaddrinfo("example.com", 80)[:1])
except OSError as e:
    print("dns-fail", e.errno, e.strerror)
try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW); print("raw ok")
except OSError as e:
    print("raw-fail", e.errno)
try:
    s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, 0); print("netlink ok"); s.close()
except OSError as e:
    print("netlink-fail", e.errno)
PY
echo "= netdev"
cat /proc/net/dev 2>/dev/null | tail -n +3
ip link 2>&1 | head -5
""", "S3 HOME/.local and network")

    print("### S2 host-side check after write attempts")
    for p in ("/w_root", "/etc/hostile", "/usr/x", "/root/x", "/dev/x", "/app/w_dotdot"):
        print(f"HOST {p} exists={os.path.lexists(p)}")
    print(f"HOST /home/vgpnk/.local/bin/x exists={os.path.lexists('/home/vgpnk/.local/bin/x')}")
    print()

if "forks" in sys.argv:
    print("### S4 fork fan-out and host visibility")
    w = workdir()
    payload = r"""
for i in $(seq 1 300); do /usr/bin/sleep 6 & done
echo "spawned=$(ls /proc | grep -cE '^[0-9]+$')"
echo "nproc-limit=$(grep 'Max processes' /proc/self/limits)"
/usr/bin/sleep 5
"""
    argv = probe.sandbox_argv(CAP, w) + ["/usr/bin/bash", "-c", payload]
    base = len([d for d in os.listdir("/proc") if d.isdigit()])
    p = subprocess.Popen(argv, env=probe.ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(2.5)
    during = len([d for d in os.listdir("/proc") if d.isdigit()])
    n_uid = 0
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            for l in open(f"/proc/{d}/status"):
                if l.startswith("Uid:") and int(l.split()[1]) == os.getuid():
                    n_uid += 1
                elif l.startswith("Uid:"):
                    break
        except OSError:
            pass
    print(f"HOSTPIDS baseline={base} during={during} delta={during - base}")
    print(f"HOSTTASKS-OF-UID-{os.getuid()} during={n_uid}")
    out, err = p.communicate(timeout=120)
    print("RC", p.returncode)
    sys.stdout.write(out)
    if err.strip():
        print("STDERR " + err.strip()[:1500])
    after = len([d for d in os.listdir("/proc") if d.isdigit()])
    print(f"HOSTPIDS after={after}")
    shutil.rmtree(w, ignore_errors=True)
    print()

if "out" in sys.argv:
    print("### S5 unbounded stdout capture (2 GiB)")
    rss0, m0 = myrss(), memavail()
    print(f"BEFORE parent_rss_mib={rss0} memavail_mib={m0}")
    payload = r"""python3 -c "
import sys
c=b'A'*(1<<20)
for _ in range(2048):
    sys.stdout.buffer.write(c)
sys.stdout.flush()
" """
    w = workdir()
    t = time.time()
    p = subprocess.run(probe.sandbox_argv(CAP, w) + ["/usr/bin/bash", "-c", payload],
                       env=probe.ENV, capture_output=True, timeout=600)
    dt = time.time() - t
    rss1, m1 = myrss(), memavail()
    print(f"RC {p.returncode} captured_stdout_bytes={len(p.stdout)} seconds={dt:.1f}")
    print(f"AFTER parent_rss_mib={rss1} (delta {rss1 - rss0}) memavail_mib={m1} (delta {m1 - m0})")
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    print(f"SELF maxrss_mib={rusage.ru_maxrss // 1024}")
    del p
    shutil.rmtree(w, ignore_errors=True)
    print()

if "tmpfs" in sys.argv:
    print("### S6 tmpfs /tmp and host-disk /app consumption")
    m0 = memavail()
    print(f"BEFORE memavail_mib={m0}")
    st0 = os.statvfs("/fast/scratch/hyaku/kengaku-r46")
    payload = r"""
python3 -c "
open('/tmp/big','wb').write(b'B'*(1<<20)*1024)
import os
print('tmpfs_bytes', os.path.getsize('/tmp/big'))
print('memavail_mib', [l.split()[1] for l in open('/proc/meminfo') if l.startswith('MemAvailable:')][0])
"
python3 -c "
f=open('/app/big','wb')
for _ in range(512): f.write(b'C'*(1<<20))
f.close()
import os; print('app_bytes', os.path.getsize('/app/big'))
"
df -h /app 2>&1 | tail -1
"""
    w = workdir()
    p = subprocess.run(probe.sandbox_argv(CAP, w) + ["/usr/bin/bash", "-c", payload],
                       env=probe.ENV, capture_output=True, text=True, timeout=600)
    print("RC", p.returncode)
    sys.stdout.write(p.stdout)
    if p.stderr.strip():
        print("STDERR " + p.stderr.strip()[:1500])
    m1 = memavail()
    st1 = os.statvfs("/fast/scratch/hyaku/kengaku-r46")
    print(f"AFTER(inside-sandbox still writing) memavail_mib={m1} delta={m0 - m1}")
    print(f"HOST-FS free_blocks_before={st0.f_bavail} after={st1.f_bavail} "
          f"delta_bytes={(st0.f_bavail - st1.f_bavail) * st0.f_frsize}")
    # keep the scratch tree small again
    shutil.rmtree(w, ignore_errors=True)
    print()

if "ram" in sys.argv:
    print("### S6b writable root tmpfs: RAM fill outside /app, tty reach, /pub rename")
    m0 = memavail()
    print(f"BEFORE memavail_mib={m0}")
    payload = r"""
python3 - <<'PY'
import os
for path, mb in (("/rootfs-big", 768), ("/tmp/tmpfs-big", 256)):
    f = open(path, "wb")
    for _ in range(mb):
        f.write(b"D" * (1 << 20))
    f.flush()
    print("filled", path, os.path.getsize(path) >> 20, "MiB")
print("memavail_mib", [l.split()[1] for l in open("/proc/meminfo") if l.startswith("MemAvailable:")][0])
try:
    tty = open("/dev/tty", "w"); tty.write("TTY-WRITE-LEAK\n"); tty.close(); print("tty-open ok")
except OSError as e:
    print("tty-open", type(e).__name__, e.errno)
try:
    os.rename("/pub/solve.sh", "/pub/solve.moved"); print("pub-rename ok")
except OSError as e:
    print("pub-rename", type(e).__name__, e.errno)
try:
    open("/pub/solve.sh", "a").write("x"); print("pub-append ok")
except OSError as e:
    print("pub-append", type(e).__name__, e.errno)
print("pub-list", sorted(os.listdir("/pub")))
PY
"""
    w = workdir()
    p = subprocess.run(probe.sandbox_argv(CAP, w) + ["/usr/bin/bash", "-c", payload],
                       env=probe.ENV, capture_output=True, text=True, timeout=600)
    print("RC", p.returncode)
    sys.stdout.write(p.stdout)
    if p.stderr.strip():
        print("STDERR " + p.stderr.strip()[:1200])
    m1 = memavail()
    print(f"WHILE-SANDBOX-HELD memavail_mib={m1} delta_drop_mib={m0 - m1}")
    shutil.rmtree(w, ignore_errors=True)
    print()

if "daemon" in sys.argv:
    print("### S7 detached child after sandbox exit")
    w = workdir()
    payload = r"""
setsid /usr/bin/sleep 137 >/dev/null 2>&1 &
echo "inside_ok"
"""
    p = subprocess.run(probe.sandbox_argv(CAP, w) + ["/usr/bin/bash", "-c", payload],
                       env=probe.ENV, capture_output=True, text=True, timeout=60)
    print("RC", p.returncode, "OUT", p.stdout.strip(), "ERR", p.stderr.strip()[:300])
    time.sleep(1.0)
    found = []
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                cl = open(f"/proc/{d}/cmdline", "rb").read().replace(b"\0", b" ").decode()
            except OSError:
                continue
            if "sleep 137" in cl:
                found.append((d, cl.strip()))
    print(f"LEFTOVER sleep-137 processes on host: {found}")
    shutil.rmtree(w, ignore_errors=True)
    print()

if "e2e" in sys.argv:
    print("### S8 end-to-end: hostile main.py.c executed by the landed harness (grade mode)")
    PY = r'''
import os, socket, subprocess
_notes = []
for p in ('/etc/hostile', '/home/vgpnk/hostile', '/root/hostile', '/usr/hostile', '/app/hostile', '/pub/extra'):
    try:
        open(p, 'w').write('x'); _notes.append('W:' + p)
    except OSError as e:
        _notes.append('D:' + p + ':' + str(e.errno))
for _ in range(200):
    subprocess.Popen(['/usr/bin/sleep', '3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    socket.create_connection(('1.1.1.1', 80), timeout=2); _notes.append('NET:ok')
except OSError as e:
    _notes.append('NET:' + str(e.errno))
sys.stderr.write(' '.join(_notes) + '\n')
for _ in range(1024):
    sys.stdout.write('A' * (1 << 20))
'''
    C = r'''
    {
        const char *ps[] = {"/etc/hostile", "/home/vgpnk/hostile", "/root/hostile", "/usr/hostile",
                            "/app/hostile", "/pub/extra"};
        for (int i = 0; i < 6; ++i) {
            FILE *f = fopen(ps[i], "w");
            fprintf(stderr, "%s%s\n", f ? "W:" : "D:", ps[i]);
            if (f) fclose(f);
        }
        for (int i = 0; i < 200; ++i) if (fork() == 0) { execl("/usr/bin/sleep", "sleep", "3", (char*)0); _exit(1); }
        int sd = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in sa; memset(&sa, 0, sizeof sa); sa.sin_family = AF_INET; sa.sin_port = htons(80);
        inet_pton(AF_INET, "1.1.1.1", &sa.sin_addr);
        fprintf(stderr, "NET:%d\n", connect(sd, (struct sockaddr*)&sa, sizeof sa));
        for (int i = 0; i < 1024; ++i) { char *buf = malloc(1 << 20); memset(buf, 'A', 1 << 20);
                                        fwrite(buf, 1, 1 << 20, stdout); free(buf); }
        printf("%llu\n", a);
    }
'''
    text = probe.poly(py=PY, c=C, nparse="    unsigned int n = (unsigned int)strtoul(argv[1], NULL, 10);")
    text = text.replace("#include <stdlib.h>", "#include <stdlib.h>\n#include <string.h>\n#include <unistd.h>\n"
                        "#include <sys/socket.h>\n#include <arpa/inet.h>")
    case = probe.Case("hostile-writer", "F", "F", (),
                      "hostile polyglot: writes outside /app, a network connect, a 200-child fan-out and a 1 GiB "
                      "stdout burst in both runtimes",
                      recipe=probe.emit(text))
    print("CASE-BYTES", len(text))
    root = pathlib.Path(tempfile.mkdtemp(prefix="c3e2e-", dir=S))
    m0, rss0 = memavail(), myrss()
    print(f"BEFORE driver_rss_mib={rss0} memavail_mib={m0}")
    t0 = time.time()
    res = {}

    def go():
        res["v"] = probe.run_case(CAP, root, case, "grade")

    th = threading.Thread(target=go, daemon=True)
    th.start()
    peak = {"mib": 0, "procs": 0}
    while th.is_alive():
        time.sleep(0.2)
        for d in os.listdir("/proc"):
            if not d.isdigit():
                continue
            try:
                cm = open(f"/proc/{d}/cmdline", "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")
            except OSError:
                continue
            if "bwrap" in cm and "/app" in cm:
                r, n = tree_rss(int(d))
                peak["mib"] = max(peak["mib"], r)
                peak["procs"] = max(peak["procs"], n)
    th.join(timeout=900)
    v = res.get("v")
    if v:
        print(f"RUN_CASE_GRADE recipe_rc={v[0]} grades={[(rc, probe.letters(rc, out)) for rc, out in v[1]]}")
        for rc, out in v[1]:
            for l in out.splitlines():
                if l.startswith("TEST "):
                    print("GRADE-LINE " + l)
    else:
        print("RUN_CASE_GRADE no result (timeout)")
    print(f"PEAK sandbox-tree rss_mib={peak['mib']} tasks={peak['procs']} seconds={time.time() - t0:.1f}")
    m1 = memavail()
    print(f"AFTER memavail_mib={m1} delta={m0 - m1}")
    leftovers = 0
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                cm = open(f"/proc/{d}/cmdline", "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")
            except OSError:
                continue
            if "sleep 3" in cm:
                leftovers += 1
    print(f"LEFTOVER sleep-3 on host after grade: {leftovers}")
    print(f"HOST /etc/hostile={os.path.lexists('/etc/hostile')} /pub-extra?={os.path.lexists(os.path.join(str(CAP), 'extra'))}")
    shutil.rmtree(root, ignore_errors=True)
    print()

if "etc" in sys.argv:
    print("### S9 host /etc exposure and grader stall cost")
    payload = r"""
for f in /etc/machine-id /etc/hostname /etc/passwd /etc/group /etc/shadow /etc/gshadow /etc/sudoers \
         /etc/ssh/ssh_host_ed25519_key /etc/kernel/cmdline /proc/self/cgroup /proc/1/cmdline; do
  if head -c 24 "$f" >/dev/null 2>&1; then
    echo "READABLE $f $(head -c 40 "$f" 2>/dev/null | tr -d '\n' | tr -c '[:print:]' '.')"
  else
    echo "DENIED $f"
  fi
done
"""
    w = workdir()
    p = subprocess.run(probe.sandbox_argv(CAP, w) + ["/usr/bin/bash", "-c", payload],
                       env=probe.ENV, capture_output=True, text=True, timeout=120)
    print("RC", p.returncode)
    sys.stdout.write(p.stdout)
    if p.stderr.strip():
        print("STDERR " + p.stderr.strip()[:800])
    shutil.rmtree(w, ignore_errors=True)

    print()
    print("### S9b grader stall: a hostile main.py.c that sleeps in both runtimes")
    py = "import time\ntime.sleep(3)\nprint(fib(_k))"
    c = "    { sleep(3); }\n    printf(\"%llu\\n\", a);"
    text = probe.poly(py=py, c=c).replace("#include <stdlib.h>", "#include <stdlib.h>\n#include <unistd.h>")
    case = probe.Case("stall", "F", "F", (), "hostile: sleeps 3 s per runtime (nine 3 s sleeps per grade)",
                      recipe=probe.emit(text))
    root = pathlib.Path(tempfile.mkdtemp(prefix="c3stall-", dir=S))
    t0 = time.time()
    v = probe.run_case(CAP, root, case, "grade")
    dt = time.time() - t0
    print(f"RUN_CASE_GRADE recipe_rc={v[0]} grades={[(rc, probe.letters(rc, out)) for rc, out in v[1]]} "
          f"seconds={dt:.1f}")
    print("OUTER-TIMEOUT probe.harness timeout=" + str(1800) + "s per harness call (source: plans/polyglot_c_py_probe.py:372)")
    shutil.rmtree(root, ignore_errors=True)
    print()

if "cases3" in sys.argv:
    print("### S10 three hostile main.py.c programs through the landed harness (grade mode)")
    PY_W = r"""
import os
for p in ('/etc/x', '/usr/x', '/tests/x', '/pub/x', '/home/vgpnk/.local/bin/x', '/root/x', '/w_root',
          '/app/escape-ok'):
    try:
        open(p, 'w').write('x'); print('W:' + p, file=sys.stderr)
    except OSError as e:
        print('D:' + p + ':' + str(e.errno), file=sys.stderr)
print(fib(_k))
"""
    C_W = r"""
    {
        const char *ps[] = {"/etc/x", "/usr/x", "/tests/x", "/pub/x", "/home/vgpnk/.local/bin/x", "/root/x",
                            "/w_root", "/app/escape-ok"};
        for (int i = 0; i < 8; ++i) {
            FILE *f = fopen(ps[i], "w");
            fprintf(stderr, "%s%s\n", f ? "W:" : "D:", ps[i]);
            if (f) fclose(f);
        }
        printf("%llu\n", a);
    }
"""
    PY_N = r"""
import socket, sys
for addr, label in ((( '1.1.1.1', 80), 'ext'), (('127.0.0.1', 9000), 'lo')):
    try:
        s = socket.create_connection(addr, timeout=2); print('NET:' + label + ':ok', file=sys.stderr); s.close()
    except OSError as e:
        print('NET:' + label + ':' + str(e.errno), file=sys.stderr)
try:
    srv = socket.socket(); srv.bind(('0.0.0.0', 9000)); srv.listen(1)
    print('BIND:ok', file=sys.stderr)
except OSError as e:
    print('BIND:' + str(e.errno), file=sys.stderr)
try:
    print('DNS:' + str(socket.getaddrinfo('example.com', 80)[0][4]), file=sys.stderr)
except OSError as e:
    print('DNS:' + str(e.errno), file=sys.stderr)
print(fib(_k))
"""
    C_N = r"""
    {
        int sd = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in sa; memset(&sa, 0, sizeof sa); sa.sin_family = AF_INET; sa.sin_port = htons(80);
        inet_pton(AF_INET, "1.1.1.1", &sa.sin_addr);
        fprintf(stderr, "NET-ext:%d\n", connect(sd, (struct sockaddr*)&sa, sizeof sa));
        int ls = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in la; memset(&la, 0, sizeof la); la.sin_family = AF_INET; la.sin_port = htons(9000);
        fprintf(stderr, "BIND:%d\n", bind(ls, (struct sockaddr*)&la, sizeof la));
        printf("%llu\n", a);
    }
"""
    PY_F = r"""
import subprocess
n = 0
for _ in range(400):
    subprocess.Popen(['/usr/bin/sleep', '4'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    n += 1
print('FORKS:' + str(n), file=sys.stderr)
for _ in range(1024):
    sys.stdout.write('A' * (1 << 20))
print(fib(_k))
"""
    C_F = r"""
    {
        int n = 0;
        for (int i = 0; i < 400; ++i) if (fork() == 0) { execl("/usr/bin/sleep", "sleep", "4", (char*)0); _exit(1); }
        else ++n;
        fprintf(stderr, "FORKS:%d\n", n);
        for (int i = 0; i < 1024; ++i) { char *b = malloc(1 << 20); memset(b, 'A', 1 << 20);
                                        fwrite(b, 1, 1 << 20, stdout); free(b); }
        printf("%llu\n", a);
    }
"""
    extra_inc = "#include <string.h>\n#include <unistd.h>\n#include <sys/socket.h>\n#include <arpa/inet.h>"
    for cid, py, c, note in (("hostile-writer", PY_W, C_W, "writes outside /app"),
                             ("hostile-net", PY_N, C_N, "network connect/bind/dns"),
                             ("hostile-forkout", PY_F, C_F, "400-child fan-out and 1 GiB stdout")):
        text = probe.poly(py=py.strip("\n"), c=c).replace("#include <stdlib.h>",
                                                          "#include <stdlib.h>\n" + extra_inc)
        print("CASE", cid, "--", note, "bytes=", len(text))
        print("PROBE-OUT " + repr(probe.poly(py=py.strip("\n"), c=c))[:0])
        case = probe.Case(cid, "F", "F", (), note, recipe=probe.emit(text))
        root = pathlib.Path(tempfile.mkdtemp(prefix="c3h-", dir=S))
        m0 = memavail()
        res = {}

        def go(case=case, root=root):
            res["v"] = probe.run_case(CAP, root, case, "grade")

        th = threading.Thread(target=go, daemon=True)
        th.start()
        peak = {"mib": 0, "procs": 0}
        while th.is_alive():
            time.sleep(0.2)
            for d in os.listdir("/proc"):
                if not d.isdigit():
                    continue
                try:
                    cm = open(f"/proc/{d}/cmdline", "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")
                except OSError:
                    continue
                if "bwrap" in cm and "/app" in cm:
                    r, n = tree_rss(int(d))
                    peak["mib"] = max(peak["mib"], r)
                    peak["procs"] = max(peak["procs"], n)
        th.join(timeout=900)
        v = res.get("v")
        print(f"RESULT rc={v[0] if v else None} grades={[(rc, probe.letters(rc, out)) for rc, out in v[1]] if v else None}"
              f" peak_rss_mib={peak['mib']} peak_tasks={peak['procs']} memavail_delta_mib={memavail() - m0}")
        leftovers = 0
        for d in os.listdir("/proc"):
            if d.isdigit():
                try:
                    cm = open(f"/proc/{d}/cmdline", "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")
                except OSError:
                    continue
                if "sleep 4" in cm or "sleep 3" in cm:
                    leftovers += 1
        host = {p: os.path.lexists(p) for p in ("/etc/x", "/usr/x", "/root/x", "/w_root", "/app/escape-ok")}
        print(f"LEFTOVERS after grade={leftovers} HOST-WRITES={host}")
        shutil.rmtree(root, ignore_errors=True)
        print()
