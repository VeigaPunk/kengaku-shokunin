#!/usr/bin/env python3
"""SentinelProbe trace analysis for plans/round95_vuln_probe.py strace run."""
import re
from pathlib import Path

LOG = Path("/fast/scratch/hyaku/kengaku-r95/SentinelProbe/trace-full.log")
S = "/fast/scratch/hyaku/kengaku-r95/SentinelProbe"

openw = []          # (path, result, line) write-mode opens
sockets = {}        # family -> count
socketpairs = 0
unshares = []
bwrap_execs = 0
bash_execs = []     # full execve lines for /usr/bin/bash (solve.sh)
py_execs = 0
canary_execs = 0    # execve lines whose envp contains the canary
fleet_touches = []  # lines mentioning /home/vgpnk/Projects
EROFS = 0

with LOG.open(errors="replace") as fh:
    for line in fh:
        if "openat(" in line and ("O_WRONLY" in line or "O_RDWR" in line or "O_CREAT" in line):
            m = re.search(r'openat\((?:AT_FDCWD|[A-Z_0-9]+), "((?:[^"\\]|\\.)*)"', line)
            path = m.group(1) if m else "<unparsed>"
            res = line.rsplit("= ", 1)[-1].strip()
            if "EROFS" in res:
                EROFS += 1
            openw.append((path, res, line[:200]))
        if "socket(" in line:
            m = re.search(r"socket\((AF_[A-Z0-9]+)", line)
            if m:
                sockets[m.group(1)] = sockets.get(m.group(1), 0) + 1
        if "socketpair(" in line:
            socketpairs += 1
        if "unshare(" in line:
            m = re.search(r"unshare\(([^)]*)\)", line)
            unshares.append(m.group(1) if m else line[:120])
        if 'execve("/usr/bin/bwrap"' in line:
            bwrap_execs += 1
        if 'execve("/usr/bin/bash"' in line:
            bash_execs.append(line.rstrip("\n"))
        if 'execve("/usr/bin/python3"' in line or 'execve("/usr/bin/python"' in line:
            py_execs += 1
        if "SENTINEL_CANARY_R95" in line and "execve(" in line:
            canary_execs += 1
        if "/home/vgpnk/Projects" in line:
            fleet_touches.append(line[:200])

def uniq_paths():
    seen = {}
    for path, res, _ in openw:
        seen.setdefault(path, []).append(res)
    return seen

paths = uniq_paths()
sandbox_paths = {p: v for p, v in paths.items() if not p.startswith(S)}
driver_paths = {p: v for p, v in paths.items() if p.startswith(S)}

rep = []
rep.append("# trace-full.log analysis (strace -f -v -s 8000, %d bytes)" % LOG.stat().st_size)
rep.append("")
rep.append("## bwrap / process")
rep.append("bwrap execve count: %d" % bwrap_execs)
rep.append("sandboxed /usr/bin/bash execve count: %d" % len(bash_execs))
rep.append("python3 execve count (driver + sandboxed): %d" % py_execs)
rep.append("execve lines containing SENTINEL_CANARY_R95: %d" % canary_execs)
rep.append("")
rep.append("## socket families observed in whole tree (driver + sandbox)")
for fam, n in sorted(sockets.items()):
    rep.append("%s: %d" % (fam, n))
rep.append("socketpair calls: %d" % socketpairs)
rep.append("")
rep.append("## unshare calls")
for u in unshares[:10]:
    rep.append("unshare(%s)" % u)
rep.append("")
rep.append("## write-mode openat: unique sandbox-view paths (NOT under scratch S)")
for p in sorted(sandbox_paths):
    rep.append("%s  x%d  last=%s" % (p, len(sandbox_paths[p]), sandbox_paths[p][-1]))
rep.append("")
rep.append("## write-mode openat: unique driver-view paths under S (aggregated by top dirs)")
agg = {}
for p in driver_paths:
    rel = p[len(S):]
    parts = rel.split("/")
    key = S + "/".join(parts[:2]) if len(parts) > 2 else p
    agg[key] = agg.get(key, 0) + len(driver_paths[p])
for k in sorted(agg):
    rep.append("%s  x%d" % (k, agg[k]))
rep.append("")
rep.append("write-mode openat total: %d" % len(openw))
rep.append("EROFS results on write opens: %d" % EROFS)
rep.append("")
rep.append("## lines mentioning /home/vgpnk/Projects (fleet tree): %d" % len(fleet_touches))
for t in fleet_touches[:10]:
    rep.append(t)

out = Path(S, "trace-analysis.md")
out.write_text("\n".join(rep) + "\n")
sample = Path(S, "trace-execve-env-sample.txt")
if bash_execs:
    sample.write_text(bash_execs[0][:6000] + "\n")
elif canary_execs:
    pass
print("bash_execs=%d bwrap_execs=%d canary_execs=%d" % (len(bash_execs), bwrap_execs, canary_execs))
print("sandbox_paths=%d driver_paths=%d EROFS=%d fleet_touches=%d" % (len(sandbox_paths), len(driver_paths), EROFS, len(fleet_touches)))
print("sockets:", sockets)
