"""R45ExecWitnessFence scratch probe: six shapes beyond the frozen refusal set, each run under `strace -f -y`,
counting successful opens of paths under the probe root but outside the fixture dir. Not a lane file."""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

FENCE = pathlib.Path(sys.argv[1]).resolve()
ROOT = pathlib.Path(sys.argv[2]).resolve()
HARNESS = """import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location("fx", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.breach(pathlib.Path(sys.argv[2]), json.loads(sys.argv[4]), sys.argv[3])
sys.stdout.write("BREACH " + " ".join(str(r).split()) if r else "ADMIT")
"""
OPEN = re.compile(r"\bopen(?:at|at2)?\(|creat\(")
DONE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
UNFIN = re.compile(r"(<unfinished \.\.\.>|=\s*\?)\s*$")


def git(cwd, *args):
    r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"git {' '.join(args)} in {cwd} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def commit(repo, note):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", note)


def seed(repo):
    subprocess.run(["git", "-C", str(repo), "init", "-q", "-b", "master"], check=True, capture_output=True)
    (repo / "corpus" / "evidence").mkdir(parents=True)
    (repo / "corpus" / "evidence" / "cap.txt").write_text("a capture\n")
    (repo / "plans").mkdir()
    (repo / "plans" / "round-90-claims.md").write_text("# claims\n")
    commit(repo, "seed")


def trace_run(d, argv, tool):
    log = d.parent / "trace.log"
    t0 = time.time()
    r = subprocess.run(["/usr/bin/strace", "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat",
                        "-o", str(log), sys.executable, "-I", "-B", str(ROOT / "harness.py"), str(FENCE), str(d),
                        tool, json.dumps(argv)],
                       cwd=str(d), capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120,
                       env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    elapsed = time.time() - t0
    out = r.stdout.strip()
    opens, first = 0, ""
    for line in log.read_text(errors="replace").splitlines():
        if not OPEN.search(line) or UNFIN.search(line):
            continue
        m = DONE.search(line)
        if not m or m.group(1).startswith(("E", "-")):
            continue
        p = pathlib.Path(m.group(2) or "")
        if p == ROOT / "harness.py" or "__pycache__" in str(p):
            continue
        if (p == ROOT or p.is_relative_to(ROOT)) and not (p == d or p.is_relative_to(d)):
            opens += 1
            first = first or str(p)
    log.unlink()
    verdict = "BREACH" if out.startswith("BREACH ") else "ADMIT" if out == "ADMIT" else "ERROR"
    return verdict, out[7:][:110], opens, first, round(elapsed, 2)


def case(name, build, tool, expect):
    base = ROOT / "cases" / name
    base.mkdir(parents=True)
    d = base / "d"
    d.mkdir()
    d, argv = build(base, d)
    verdict, why, opens, first, secs = trace_run(d, argv, tool)
    ok = verdict == expect and opens == 0
    print(f"CASE {name} expect={expect} got={verdict} opens={opens} secs={secs} ok={ok}"
          + (f" why={why!r}" if why else "") + (f" first_outside={first}" if first else ""))
    return ok


def include_with(base, d, section):
    side = base / "outside.cfg"
    side.write_text("[user]\n\temail = OUTSIDE@invalid\n")
    repo = d / "lane"
    repo.mkdir()
    seed(repo)
    (repo / ".git" / "config").write_text(
        (repo / ".git" / "config").read_text() + f'[{section}]\n\tpath = {side}\n')
    return d, ["--lane", "lane", "--claims", "plans/round-90-claims.md",
            "--receipt", "corpus/evidence/cap.txt"]


def c_includeif(base, d):
    return include_with(base, d, 'includeIf "gitdir:/**"')


def c_include_fifo(base, d):
    fifo = base / "fifo.cfg"
    os.mkfifo(fifo)
    repo = d / "lane"
    repo.mkdir()
    seed(repo)
    (repo / ".git" / "config").write_text(
        (repo / ".git" / "config").read_text() + f"[include]\n\tpath = {fifo}\n")
    return d, ["--lane", "lane", "--claims", "plans/round-90-claims.md",
            "--receipt", "corpus/evidence/cap.txt"]


def c_worktreeconfig(base, d):
    repo = d / "lane"
    repo.mkdir()
    seed(repo)
    (repo / ".git" / "config").write_text(
        (repo / ".git" / "config").read_text() + "[extensions]\n\tworktreeConfig = true\n")
    return d, ["--lane", "lane", "--claims", "plans/round-90-claims.md",
            "--receipt", "corpus/evidence/cap.txt"]


def c_gitfile_outside(base, d):
    store = base / "side" / "store"
    store.parent.mkdir()
    repo = d / "lane"
    subprocess.run(["git", "init", "-q", "-b", "master", f"--separate-git-dir={store}", str(d / "lane")],
                   check=True, capture_output=True)
    seed(repo)
    return d, ["--lane", "lane", "--claims", "plans/round-90-claims.md",
               "--receipt", "corpus/evidence/cap.txt"]


def c_gitfile_inside(base, d):
    store = d / "store"
    repo = d / "repo"
    subprocess.run(["git", "init", "-q", "-b", "master", f"--separate-git-dir={store}", str(repo)],
                   check=True, capture_output=True)
    seed(repo)
    return d, ["--lane", "repo", "--claims", "plans/round-90-claims.md",
               "--receipt", "corpus/evidence/cap.txt"]


def c_repo_grandparent(base, d):
    mod = base / "m"
    mod.mkdir()
    inner = mod / "d"
    inner.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "master", str(base)], check=True, capture_output=True)
    seed(base)
    (inner / "sub").mkdir()
    (inner / "sub" / "claims.md").write_text("x\n")
    return inner, ["--lane", "sub", "--claims", "claims.md", "--receipt", "claims.md"]


CASES = [
    ("includeif-outside-regular", c_includeif, "BREACH"),
    ("include-fifo-outside", c_include_fifo, "BREACH"),
    ("worktreeconfig-no-file", c_worktreeconfig, "BREACH"),
    ("gitfile-store-outside", c_gitfile_outside, "BREACH"),
    ("gitfile-store-inside", c_gitfile_inside, "ADMIT"),
    ("repo-above-build-root", c_repo_grandparent, "ADMIT"),
]

if __name__ == "__main__":
    (ROOT / "harness.py").write_text(HARNESS)
    (ROOT / "cases").mkdir(exist_ok=True)
    if any((ROOT / "cases").iterdir()):
        shutil.rmtree(ROOT / "cases")
        (ROOT / "cases").mkdir()
    results = []
    for name, build, expect in CASES:
        results.append((name, case(name, build, "order", expect)))
    print("ADV", " ".join(f"{n}={'ok' if ok else 'RED'}" for n, ok in results))
