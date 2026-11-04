#!/usr/bin/env python3
"""SentinelR84 read-only audit of the R83 bubblewrap probe vector.

Loads the frozen baseline module (plans/round83_code_image_probe.py) without
executing its main, materialises the exact sandbox_argv, and measures the
sandbox properties the R84 sentinel seat is asked to check. Writes nothing
outside SENTINEL_WORK and the caller's stdout.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import socket
import subprocess
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
BASE = LANE / "plans/round83_code_image_probe.py"
CAP = LANE / "corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py"
WORK = Path(os.environ["SENTINEL_WORK"])
WORK.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(WORK)

spec = importlib.util.spec_from_file_location("r83probe", BASE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

DIAG = r'''
import json, os, socket, subprocess
from pathlib import Path
out = {}
out["uid"] = os.getuid()
out["env"] = dict(os.environ)
out["ns"] = {n: os.stat("/proc/self/ns/" + n).st_ino for n in ("net", "pid", "user", "mnt")}
out["host_visible"] = {p: os.path.exists(p) for p in ("/home", "/tmp", "/root", "/sys", "/var", "/home/vgpnk/.ssh", "/home/vgpnk/.omp", "/home/vgpnk/.config")}
out["root"] = sorted(os.listdir("/"))
out["app"] = sorted(os.listdir("/app"))
def attempt(tag, fn):
    try: fn(); out[tag] = "ok"
    except BaseException as e: out[tag] = type(e).__name__ + ":" + str(e)[:80]
attempt("write_app", lambda: Path("/app/out.txt").write_text("flag{gc0d3_iz_ch4LLenGiNg}"))
attempt("write_tests", lambda: Path("/tests/planted.py").write_text("x"))
attempt("unlink_tests_file", lambda: os.unlink("/tests/test_outputs.py"))
attempt("write_usr", lambda: Path("/usr/planted").write_text("x"))
attempt("write_etc", lambda: Path("/etc/planted").write_text("x"))
attempt("write_root", lambda: Path("/planted").write_text("x"))
attempt("write_tmp", lambda: Path("/tmp/planted").write_text("x"))
out["mounts"] = [l for l in Path("/proc/self/mountinfo").read_text().splitlines()
                 if any(x in l for x in (" /app ", " /tests", " /usr ", " /etc "))]
def run(tag, argv):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=10)
    out[tag] = {"rc": p.returncode, "err": (p.stderr or "").strip()[:120]}
run("nested_userns", ["/usr/bin/unshare", "-U", "true"])
run("nested_userns_mount", ["/usr/bin/unshare", "-U", "-r", "-m", "--", "/usr/bin/mount", "-t", "tmpfs", "none", "/tests"])
try:
    s = socket.socket(); s.settimeout(2); s.connect(("1.1.1.1", 80)); out["net"] = "CONNECTED"
except BaseException as e: out["net"] = type(e).__name__ + ":" + str(e)[:60]
out["caps"] = [l for l in Path("/proc/self/status").read_text().splitlines() if l.startswith(("CapEff", "NoNewPrivs", "Seccomp:"))]
print(json.dumps(out))
'''

SUBJECT = r'''
import json, runpy
module = runpy.run_path("/tests/test_outputs.py")
results = []
for name in ("test_hello_file_exists", "test_hello_file_content"):
    try:
        module[name]()
    except BaseException as error:
        results.append("F:" + type(error).__name__)
    else:
        results.append("P")
print(json.dumps(results))
'''


def case(root: Path, harness: str, content: str | None) -> Path:
    shutil.rmtree(root, ignore_errors=True)
    (root / "app").mkdir(parents=True)
    if content is not None:
        (root / "app/out.txt").write_text(content, encoding="utf-8")
    (root / "harness.py").write_text(harness, encoding="utf-8")
    return root


def run(argv: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(argv, capture_output=True, text=True, timeout=60,
                       env={"PATH": "/usr/bin"})
    return p.returncode, p.stdout, p.stderr


def baseline_vector(capture: Path, cdir: Path) -> list[str]:
    return probe.sandbox_argv(capture, cdir)


def proposed_ro_tests(cdir: Path, capturedir: Path) -> list[str]:
    argv = [probe.BWRAP, "--unshare-all", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--proc", "/proc", "--dev", "/dev",
             "--bind", str(cdir / "app"), "/app",
             "--ro-bind", str(capturedir), "/tests",
             "--ro-bind", str(cdir / "harness.py"), "/harness.py",
             "--clearenv", "--setenv", "PATH", "/usr/bin",
             "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
             "--chdir", "/app", "/usr/bin/python3", "-I", "-B", "/harness.py"]
    return argv


def proposed_disable_userns(capture: Path, cdir: Path) -> list[str]:
    argv = baseline_vector(capture, cdir)
    at = argv.index("--unshare-all") + 1
    return argv[:at] + ["--unshare-user", "--disable-userns",
                        "--assert-userns-disabled"] + argv[at:]


def main() -> int:
    host_net = os.stat("/proc/self/ns/net").st_ino
    print(f"HOST netns={host_net}")
    print(f"BASELINE module={BASE} bwrap={probe.BWRAP}")

    d1 = case(WORK / "diag", DIAG, None)
    rc, out, err = run(baseline_vector(CAP, d1))
    print(f"VARIANT baseline-vector rc={rc} stderr={err.strip()[:120]!r}")
    diag = json.loads(out)
    print("VECTOR " + json.dumps(baseline_vector(CAP, d1)))
    for key in ("uid", "env", "ns", "host_visible", "root", "app", "write_app",
                "write_tests", "unlink_tests_file", "write_usr", "write_etc",
                "write_root", "write_tmp", "nested_userns",
                "nested_userns_mount", "net", "caps"):
        print(f"OBS {key} = {json.dumps(diag[key])}")
    print(f"OBS netns_unshared = {diag['ns']['net'] != host_net}")
    for line in diag["mounts"]:
        print(f"MOUNT {line[:240]}")

    s1 = case(WORK / "subject", SUBJECT, "flag{gc0d3_iz_ch4LLenGiNg}")
    staged = WORK / "subject-tests"
    staged.mkdir(exist_ok=True)
    shutil.copyfile(CAP, staged / "test_outputs.py")
    rc, out, err = run(baseline_vector(staged / "test_outputs.py", s1))
    print(f"SUBJECT baseline-vector rc={rc} stderr={err.strip()[:120]!r} legs={out.strip()}")

    d2 = case(WORK / "diag2", DIAG, None)
    rc, out, err = run(proposed_ro_tests(d2, staged))
    print(f"FIX ro-tests rc={rc} stderr={err.strip()[:120]!r}")
    fix1 = json.loads(out)
    for key in ("write_tests", "unlink_tests_file", "subject_legs"):
        if key in fix1:
            print(f"FIX ro-tests {key} = {json.dumps(fix1[key])}")
    rc, out, err = run(proposed_ro_tests(s1, staged))
    print(f"FIX ro-tests-subject rc={rc} stderr={err.strip()[:120]!r} legs={out.strip()}")

    d3 = case(WORK / "diag3", DIAG, None)
    rc, out, err = run(proposed_disable_userns(CAP, d3))
    print(f"FIX disable-userns rc={rc} stderr={err.strip()[:160]!r}")
    if rc == 0:
        fix2 = json.loads(out)
        print(f"FIX disable-userns nested_userns = {json.dumps(fix2['nested_userns'])}")
        print(f"FIX disable-userns nested_userns_mount = {json.dumps(fix2['nested_userns_mount'])}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"AUDIT-ERROR {type(error).__name__}: {error}")
        raise SystemExit(2)
