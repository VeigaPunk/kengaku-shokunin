#!/usr/bin/env python3
"""R45LabratReadProof pathological-tree probe.

Builds a fixture dir with N empty files (plus an ordinary self-contained git repo) and runs the landed
`plans/fixture_fence.py` under the round-45 C1 counter's own harness inside the round-44 read-only bwrap
sandbox under `strace -f -y`, measuring wall clock against `FENCE_TIMEOUT=120` and the observed verdict
against `ENTRY_CAP=200000`.  Fidelity: HARNESS text, sandbox argv and strace argv are copied from
`plans/round45_c1_verify.py` (`HARNESS`, `run_fence`) via the imported round-44 module (`ro_sandbox`,
`hide_list`), which is the counter's own code path.

usage: patho_probe.py <clone> <work> <nfiles> <tag>
"""
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import time


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HARNESS = r'''
import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location("fixture_fence_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.breach(pathlib.Path(sys.argv[2]), json.loads(sys.argv[4]), sys.argv[3])
sys.stdout.write("BREACH " + " ".join(str(r).split()) if r else "ADMIT")
'''


def build(d, n):
    """d/f000: git repo + n empty files (untracked).  Claims/receipt committed blobs for the order leg."""
    d.mkdir(parents=True)
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(d.parent), "LANG": "C.UTF-8",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
    run = lambda *a: subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True, env=env)
    run("init", "-q", "-b", "master")
    (d / "claims.md").write_text("x\n")
    (d / "receipt.txt").write_text("r\n")
    run("add", "-A")
    run("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "c")
    t0 = time.monotonic()
    big = d / "bulk"
    big.mkdir()
    chunk = 1000
    for base in range(0, n, chunk):
        for i in range(base, min(base + chunk, n)):
            (big / f"e{i:06d}").open("wb").close()
    return round(time.monotonic() - t0, 1)


def main():
    clone, work, n, tag = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    k44 = load(clone / "plans/round44_c1_verify.py", "k44")
    root = work / tag
    if root.exists():
        subprocess.run(["rm", "-rf", str(root)], check=True)
    (root / "empty").mkdir(parents=True)
    (root / "log").mkdir()
    d = (root / "fx" / "patho" / "f000").resolve()
    tbuild = build(d, n)
    fence = root / "fence.py"
    fence.write_bytes((clone / "plans/fixture_fence.py").read_bytes())
    harness = root / "harness.py"
    harness.write_text(HARNESS)
    argv = ["--lane", ".", "--claims", "claims.md", "--receipt", "receipt.txt"]
    log = root / "log" / "log"
    cmd = k44.ro_sandbox(writable=(root / "log",),
                         hide=k44.hide_list((clone,), existing=True), empty=root / "empty") \
        + ["/usr/bin/strace", "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat", "-o", str(log),
           k44.PY, "-I", str(harness), str(fence), str(d), "order", json.dumps(argv)]
    t0 = time.monotonic()
    try:
        r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=120,
                           stdin=subprocess.DEVNULL,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8",
                                "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
        verdict, rc = r.stdout.strip(), r.returncode
        err = r.stderr.strip().splitlines()[-1:] or [""]
    except subprocess.TimeoutExpired:
        verdict, rc, err = "HUNG", None, [""]
    wall = round(time.monotonic() - t0, 2)
    # outside opens by the counter's own rule: resolved path under <root>/fx or <root>/log, not under d
    import re
    opens = 0
    outside_paths = []
    for line in log.read_text(errors="replace").splitlines():
        if not re.search(r"\bopen(?:at|at2)?\(|creat\(", line):
            continue
        m = re.search(r'=\s+-?\d+<(.+)>\s*$', line)
        if not m:
            continue
        p = pathlib.Path(m.group(1))
        if any(p == s or p.is_relative_to(s) for s in (root / "fx", root / "log")) and not (
                p == d or p.is_relative_to(d)):
            opens += 1
            outside_paths.append(f"{line.strip()[:160]}")
    print(json.dumps({"tag": tag, "nfiles": n, "build_s": tbuild, "wall_s": wall, "verdict": verdict,
                      "rc": rc, "stderr": err[0][:200], "scratch_outside_opens": opens,
                      "first_outside": outside_paths[:5], "log": str(log)}, indent=1))


if __name__ == "__main__":
    main()
