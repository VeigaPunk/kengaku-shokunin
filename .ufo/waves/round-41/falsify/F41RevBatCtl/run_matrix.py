"""Run every tool variant on every built fixture with the fixture's own argv tail
(substituting {WORK} exactly like round41_c1_verify.py Runner.run) under the counter's
tool-run env, inside the mandated bwrap envelope."""
import json
import pathlib
import re
import shutil
import subprocess

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/F41RevBatCtl")
built = [l for l in (S / "out/built.raw").read_text().splitlines() if l.startswith("BUILT ")][0]
fixtures = json.loads(built[6:])
PATHV = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
TOK = re.compile(r"^\{WORK(?::([a-z]+))?\}(/[A-Za-z0-9._/-]+)?$")
VARIANTS = [("ref", S / "lane/plans/tip_receipts.py"),
            ("t06_pure", S / "var/t06_pure.py"), ("t08_pure", S / "var/t08_pure.py"),
            ("t06_ref_trace", S / "var/t06_ref_trace.py"), ("t06_mut_trace", S / "var/t06_mut_trace.py"),
            ("t08_ref_trace", S / "var/t08_ref_trace.py"), ("t08_mut_trace", S / "var/t08_mut_trace.py")]

for k, fx in enumerate(fixtures):
    for name, var in VARIANTS:
        tag = f"f{k:03d}-{name}"
        fxdir = S / "fx" / f"f{k:03d}"
        work = S / "wrun" / tag
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        argv = []
        for t in fx["argv"]:
            m = TOK.match(t)
            if m:
                w = work / "run"
                if m.group(1):
                    (w / m.group(1)).mkdir(parents=True, exist_ok=True)
                if m.group(2):
                    w.mkdir(exist_ok=True)
                argv.append(str(w) + (m.group(2) or ""))
            else:
                argv.append(t)
        env = {"PATH": PATHV, "HOME": str(S / "home"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(S / "rtmp"),
               "GIT_CEILING_DIRECTORIES": str(S),
               "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "2",
               "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
               "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null"}
        cmd = ["bwrap", "--dev-bind", "/", "/", "--ro-bind", "/home/vgpnk/.local/bin",
               "/home/vgpnk/.local/bin", "--tmpfs", "/run/user/1000", "--proc", "/proc",
               "--unshare-pid", "--die-with-parent", "/usr/bin/python3", str(var), *argv]
        r = subprocess.run(cmd, cwd=str(fxdir), env=env, capture_output=True, text=True, timeout=300)
        (S / "out" / f"{tag}.out").write_text(r.stdout)
        (S / "out" / f"{tag}.err").write_text(r.stderr)
        print(f"{tag} rc={r.returncode}")

print("=== TRACE lines ===")
for p in sorted((S / "out").glob("*.err")):
    for line in p.read_text().splitlines():
        if line.startswith("TRACE"):
            print(p.stem, "|", line)
