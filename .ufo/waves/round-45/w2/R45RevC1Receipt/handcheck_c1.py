#!/usr/bin/env python3
"""R45RevC1Receipt hand-check: my own strace evidence for one refused + one honest module.

Builds one refused module (plans/refusals45/f5_alternates.py) and one honest module
(plans/battery44/u9_worktree_b.py) with the round-44 builder (unchanged, loaded from the clean
clone), then runs the fence MYSELF under MY OWN strace -f -qq -y and parses the log with my own
parser. Prints every successful open whose resolved path lies under the build scratch outside the
fixture dir, plus never-returned opens touching such a path, plus failed opens touching such a
path (informational only — the counter's rule counts successes and never-returned touches).

usage: handcheck_c1.py <scratch root>   (root must lie outside the lane; all writes go under it)
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/lane")
ROOT = pathlib.Path(sys.argv[1]).resolve()
STRACE = "/usr/bin/strace"
MODULES = {"refused": LANE / "plans/refusals45/f5_alternates.py",
           "honest": LANE / "plans/battery44/u9_worktree_b.py"}

HARNESS = r'''
import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location("fence_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.breach(pathlib.Path(sys.argv[2]), json.loads(sys.argv[4]), sys.argv[3])
sys.stdout.write("BREACH " + " ".join(str(r).split()) if r else "ADMIT")
'''

OPEN_RE = re.compile(r"\bopen(?:at|at2)?\(|creat\(")
RET_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
UNFIN_RE = re.compile(r"(<unfinished \.\.\.>|=\s*\?)\s*$")
RESUMED_RE = re.compile(r"^\s*(\d+)\s*<\.\.\.\s+\w+\s+resumed>")
ARG_RE = re.compile(r'"((?:\\.|[^"\\])*)"(?:<([^>]*)>)?')


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def under(p, base):
    return p == base or p.is_relative_to(base)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(k44, f):
    """Build one module's fixtures with the round-44 builder in the round-44 build sandbox."""
    dest = ROOT / "fx" / f"{f.parent.name}-{f.stem}"
    dest.mkdir(parents=True)
    tmp = ROOT / "btmp" / f"{f.parent.name}-{f.stem}"
    tmp.mkdir(parents=True)
    mods = ROOT / "mods"
    mods.mkdir(exist_ok=True)
    mod_copy = mods / f"mod_{f.parent.name}_{f.name}"
    mod_copy.write_text(f.read_text())
    empty = ROOT / "empty"
    empty.mkdir(exist_ok=True)
    bfd = os.memfd_create("handcheck-builder", 0)
    try:
        os.write(bfd, k44.builder_source().encode())
        os.lseek(bfd, 0, os.SEEK_SET)
        cmd = k44.ro_sandbox(writable=(dest, tmp),
                             hide=k44.hide_list((LANE, k44.COUNTER_DIR), existing=True),
                             ro_data=((bfd, k44.BUILDER_SLOT),), empty=empty) \
            + [k44.PY, k44.BUILDER_SLOT, str(mod_copy), str(dest)]
        r = subprocess.run(cmd, cwd=str(dest), capture_output=True, text=True, timeout=1800,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "TMPDIR": str(tmp),
                                "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                                "PYTHONDONTWRITEBYTECODE": "1"}, pass_fds=(bfd,))
    finally:
        os.close(bfd)
    built = [l for l in r.stdout.splitlines() if l.startswith("BUILT ")]
    if r.returncode != 0 or len(built) != 1:
        raise RuntimeError(f"build failed rc={r.returncode} err={r.stderr.strip()[-300:]}")
    out = []
    for k, fx in enumerate(json.loads(built[0][6:])):
        d = dest / f"f{k:03d}"
        if not (isinstance(fx.get("fid"), str) and fx.get("tool") in k44.TOOLS
                and isinstance(fx.get("argv"), list) and d.is_dir()):
            raise ValueError(f"fixture contract broken: {fx!r}")
        out.append({"fid": fx["fid"], "tool": fx["tool"], "argv": fx["argv"], "dir": d.resolve()})
    return out


def cand_paths(line, ret, d):
    """Every path this open line could have touched: the -y resolved annotation on the return fd,
    the -y resolved annotation on the path argument, and the raw quoted path (relative -> d)."""
    cands = []
    if ret.group(2):
        cands.append(pathlib.Path(ret.group(2)))
    for m in ARG_RE.finditer(line):
        raw, res = m.group(1), m.group(2)
        if res:
            cands.append(pathlib.Path(res))
        try:
            p = pathlib.Path(raw.encode().decode("unicode_escape", errors="ignore"))
        except Exception:
            continue
        if not p.is_absolute():
            p = d / p
        cands.append(p)
    return cands


def parse_log(log, d, scratch):
    """My own parser over my own strace log -> (succ_outside, failed_touch)."""
    lines = log.read_text(errors="replace").splitlines()
    succ, pending, failed = [], {}, []
    for line in lines:
        pidm = re.match(r"^\s*(\d+)", line)
        pid = pidm.group(1) if pidm else "-"
        if RESUMED_RE.search(line):
            pending.pop(pid, None)
        if not OPEN_RE.search(line):
            continue
        if UNFIN_RE.search(line):
            pending[pid] = line
            continue
        ret = RET_RE.search(line)
        if not ret:
            continue
        hit = [p for p in cand_paths(line, ret, d)
               if any(under(p, s) for s in scratch) and not under(p, d)]
        if not hit:
            continue
        if ret.group(1).startswith("E") or ret.group(1).startswith("-"):
            failed.append(line)
        else:
            succ.append(line)
    for line in pending.values():
        ret = RET_RE.search(line)
        cands = cand_paths(line, ret, d) if ret else []
        if any(under(p, s) for p in cands for s in scratch) and \
                any(under(p, s) for p in cands for s in scratch) and \
                not any(under(p, d) for p in cands):
            succ.append("(never returned) " + line)
    return succ, failed


def fence_run(k44, fence_copy, harness, empty, fx, n):
    logdir = ROOT / "strace" / f"s{n:05d}"
    logdir.mkdir(parents=True)
    log = logdir / "log"
    d = fx["dir"]
    cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((LANE,), existing=True),
                         empty=empty) \
        + [STRACE, "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat", "-o", str(log),
           k44.PY, "-I", str(harness), str(fence_copy), str(d), fx["tool"], json.dumps(fx["argv"])]
    r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=120,
                       stdin=subprocess.DEVNULL,
                       env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8",
                            "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
    out = r.stdout.strip()
    succ, failed = parse_log(log, d, (ROOT / "fx", ROOT / "btmp"))
    print(f"HAND fixture {fx['fid']} tool={fx['tool']} dir={d}")
    print(f"HAND verdict={out!r} rc={r.returncode}")
    print(f"HAND succ_outside_d={len(succ)} failed_touch={len(failed)}")
    for l in succ[:10]:
        print("HAND SUCC-LINE " + l)
    for l in failed[:5]:
        print("HAND FAIL-LINE " + l)
    return out, len(succ)


def main():
    k44 = load(LANE / "plans/round44_c1_verify.py", "k44hand")
    harness = ROOT / "handcheck_harness.py"
    harness.write_text(HARNESS)
    fence_copy = ROOT / "fence" / "fixture_fence.py"
    fence_copy.parent.mkdir(exist_ok=True)
    fence_copy.write_bytes((LANE / "plans/fixture_fence.py").read_bytes())
    empty = ROOT / "empty"
    empty.mkdir(exist_ok=True)
    print(f"HAND fence_copy sha256={sha256(fence_copy)}")
    n = 0
    summary = {}
    for g, f in MODULES.items():
        fxs = build(k44, f)
        print(f"HAND module {g} {f.parent.name}/{f.name} fixtures={len(fxs)}")
        admits = breaches = outside = 0
        for fx in fxs:
            n += 1
            out, nsucc = fence_run(k44, fence_copy, harness, empty, fx, n)
            outside += nsucc
            if out == "ADMIT":
                admits += 1
            elif out.startswith("BREACH"):
                breaches += 1
        summary[g] = (len(fxs), admits, breaches, outside)
        print(f"HAND SUMMARY {g}: fixtures={len(fxs)} admit={admits} breach={breaches}"
              f" succ_outside={outside}")
    refused_ok = summary["refused"] == (1, 0, 1, 0)
    honest_ok = summary["honest"][3] == 0 and summary["honest"][1] == summary["honest"][0]
    print(f"HAND RESULT {'SUPPORTS-C1' if refused_ok and honest_ok else 'CONTRADICTS-C1'}"
          f" refused={summary['refused']} honest={summary['honest']}")
    return 0 if refused_ok and honest_ok else 1


if __name__ == "__main__":
    sys.exit(main())
