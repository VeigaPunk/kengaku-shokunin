#!/usr/bin/env python3
"""R45LabratReadProof: pathological-tree probe against the landed fence's walk bound and FENCE_TIMEOUT.

Reuses the C1 counter's own harness text, its strace invocation, and the round-44 counter's ro_sandbox /
hide_list / PY, so the fence runs exactly as `plans/round45_c1_verify.py:run_fence` runs it. Fixtures are
built here (outside bwrap) in the caller's scratch root; every git call is pinned to the fixture dir.

usage: patho_probe.py <clone> <root>
"""
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

FENCE_TIMEOUT = 120
STRACE = "/usr/bin/strace"
GIT = "git"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(d, *args):
    env = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/nonexistent",
           "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
           "GIT_CONFIG_COUNT": "2", "GIT_CONFIG_KEY_0": "commit.gpgsign", "GIT_CONFIG_VALUE_0": "false",
           "GIT_CONFIG_KEY_1": "user.name", "GIT_CONFIG_VALUE_1": "labrat"}
    r = subprocess.run([GIT, "-C", str(d), *args], capture_output=True, text=True, env=env,
                       stdin=subprocess.DEVNULL, timeout=1800)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} in {d} rc={r.returncode}: {r.stderr.strip()[:300]}")
    return r.stdout


def make_repo(d):
    d.mkdir(parents=True, exist_ok=False)
    git(d, "init", "-q", "-b", "master")
    (d / "claims.md").write_text("nothing ran\n")
    (d / "receipt.md").write_text("receipt\n")
    git(d, "add", "-A")
    git(d, "-c", "user.email=labrat@invalid", "commit", "-qm", "fixture")
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert pathlib.Path(top).resolve() == d.resolve(), (top, d)


def fill_flat(d, n):
    """n empty regular files in one directory (the worst shape for a single scandir)."""
    bulk = d / "bulk"
    bulk.mkdir()
    t0 = time.monotonic()
    for i in range(n):
        os.close(os.open(bulk / f"e{i:06d}", os.O_CREAT | os.O_WRONLY | os.O_EXCL, 0o644))
    return time.monotonic() - t0


def fill_grouped(d, dirs, per):
    t0 = time.monotonic()
    for j in range(dirs):
        sub = d / "bulk" / f"g{j:04d}"
        sub.mkdir(parents=True)
        for i in range(per):
            os.close(os.open(sub / f"e{i:05d}", os.O_CREAT | os.O_WRONLY | os.O_EXCL, 0o644))
    return time.monotonic() - t0


def entries(d):
    n = 0
    for _top, ds, fs in os.walk(d):
        n += len(ds) + len(fs)
    return n


def run(k44, c45, root, clone, fence, d, argv, tag):
    logdir = root / "logs" / tag
    logdir.mkdir(parents=True)
    log = logdir / "log"
    cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((clone,), existing=True),
                         empty=root / "empty") + \
        [STRACE, "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat", "-o", str(log),
         k44.PY, "-I", str(root / "harness.py"), str(fence), str(d), "order", json.dumps(argv)]
    t0 = time.monotonic()
    hung = False
    try:
        r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=FENCE_TIMEOUT,
                           stdin=subprocess.DEVNULL,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8",
                                "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
        out = r.stdout.strip()
        rc = r.returncode
        err = r.stderr.strip().splitlines()[-1:] or [""]
    except subprocess.TimeoutExpired:
        hung, out, rc, err = True, "", "timeout", [""]
    dt = time.monotonic() - t0
    # same opens rule as the counter
    opens = 0
    scratch = (root / "fx", root / "btmp")
    if log.is_file():
        for line in log.read_text(errors="replace").splitlines():
            m = re.search(r'=\s+\d+<([^>]+)>', line)
            if not m:
                continue
            p = pathlib.Path(m.group(1))
            if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
                opens += 1
    print(f"PROBE {tag} fence_seconds={dt:.2f} rc={rc} hung={hung} opens={opens} "
          f"out={out[:160]!r} stderr={err[0][:120]!r}")
    print(f"PROBE {tag} log={log if log.is_file() else 'absent'} bytes={log.stat().st_size if log.is_file() else 0}")
    return dt, hung, out, log


def main():
    clone, root = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    k44 = load(clone / "plans/round44_c1_verify.py", "k44_p")
    c45 = load(clone / "plans/round45_c1_verify.py", "c45_p")
    (root / "empty").mkdir(parents=True, exist_ok=True)
    (root / "fx").mkdir(exist_ok=True)
    (root / "fence").mkdir(exist_ok=True)
    (root / "harness.py").write_text(c45.HARNESS)
    fence = root / "fence/fixture_fence.py"
    shutil.copyfile(clone / "plans/fixture_fence.py", fence)
    print(f"CONST {load_fence(fence)} FENCE_TIMEOUT={FENCE_TIMEOUT} "
          f"harness_sha={__import__('hashlib').sha256((root / 'harness.py').read_bytes()).hexdigest()[:16]}")
    argv = ["--lane", ".", "--claims", "claims.md", "--receipt", "receipt.md"]

    shapes = [("flat100k", 100_000, "flat"), ("flat199k", 199_000, "flat"),
              ("grouped201k", (201, 1000), "grouped"), ("wide1m", 1_000_000, "flat")]
    want = set(sys.argv[3:])
    for tag, n, kind in shapes:
        if want and tag not in want:
            continue
        d = (root / "fx" / tag / "f000").resolve()
        make_repo(d)
        tfill = fill_flat(d, n) if kind == "flat" else fill_grouped(d, *n)
        n_entries = entries(d)
        print(f"BUILD {tag} entries={n_entries} fill_seconds={tfill:.1f} dir={d}")
        run(k44, c45, root, clone, fence, d, argv, tag)
    return 0


def load_fence(fence):
    m = load(fence, "fence_consts")
    return f"ENTRY_CAP={m.ENTRY_CAP} REPO_CAP={m.REPO_CAP} CONFIG_CAP={m.CONFIG_CAP} GIT_TIMEOUT={m.GIT_TIMEOUT}"


if __name__ == "__main__":
    sys.exit(main())
