#!/usr/bin/env python3
"""R45LabratReadProof: independent re-run of f1, f4, f6, f10 (the round-44 READ modules) under the C1
counter's own harness + the round-44 read-only bwrap sandbox, with strace tracing open* AND execve.

Unlike the counter, this driver (a) builds fixtures itself through `plans/round44_c1_verify.py`'s own
`builder_source`/`ro_sandbox`/`hide_list` (the exact functions `round45_c1_verify.py:build_module` uses),
(b) knows d by construction, and (c) classifies every successful open destination itself.

usage: four_module_probe.py <clone> <work> <module.py>...
"""
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys

HARNESS = r'''
import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location("fixture_fence_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.breach(pathlib.Path(sys.argv[2]), json.loads(sys.argv[4]), sys.argv[3])
sys.stdout.write("BREACH " + " ".join(str(r).split()) if r else "ADMIT")
'''
OPEN_RE = re.compile(r"\b(open|openat|openat2|creat)\(")
DONE_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
EXEC_RE = re.compile(r'\bexecve\("([^"]+)"')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(k44, root, lane, f):
    dest = root / "fx" / f"{f.parent.name}-{f.stem}"
    dest.mkdir(parents=True)
    tmp = root / "btmp" / f"{f.parent.name}-{f.stem}"
    tmp.mkdir(parents=True)
    mods = root / "mods"
    mods.mkdir(exist_ok=True)
    mod_copy = mods / f"mod_{f.parent.name}_{f.name}"
    mod_copy.write_text(f.read_text())
    empty = root / "empty"
    empty.mkdir(exist_ok=True)
    bfd = os.memfd_create("k45-builder", 0)
    try:
        os.write(bfd, k44.builder_source().encode())
        os.lseek(bfd, 0, os.SEEK_SET)
        cmd = k44.ro_sandbox(writable=(dest, tmp),
                             hide=k44.hide_list((lane, k44.COUNTER_DIR, root / "fence"), existing=True),
                             ro_data=((bfd, k44.BUILDER_SLOT),), empty=empty) \
            + [k44.PY, k44.BUILDER_SLOT, str(mod_copy), str(dest)]
        r = subprocess.run(cmd, cwd=str(dest), capture_output=True, text=True, timeout=1800,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "TMPDIR": str(tmp), "LANG": "C.UTF-8",
                                "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}, pass_fds=(bfd,))
    finally:
        os.close(bfd)
    built = [l for l in r.stdout.splitlines() if l.startswith("BUILT ")]
    if r.returncode != 0 or len(built) != 1:
        raise RuntimeError(f"{f} build failed rc={r.returncode}: {r.stderr.strip()[-300:]}")
    out = []
    for k, fx in enumerate(json.loads(built[0][6:])):
        out.append({"fid": fx["fid"], "tool": fx["tool"], "argv": fx["argv"],
                    "dir": (dest / f"f{k:03d}").resolve(), "module": f"{f.parent.name}/{f.name}"})
    return out


def run(k44, root, fence, fx, tag):
    log = root / "logs" / f"{tag}.log"
    log.parent.mkdir(exist_ok=True)
    d = fx["dir"]
    cmd = k44.ro_sandbox(writable=(log.parent,), hide=k44.hide_list((root.parent.parent / "lane",), existing=True),
                         empty=root / "empty") \
        + ["/usr/bin/strace", "-f", "-qq", "-y", "-s", "200",
           "-e", "trace=open,openat,openat2,creat,execve", "-o", str(log),
           k44.PY, "-I", str(root / "harness.py"), str(fence), str(d), fx["tool"], json.dumps(fx["argv"])]
    r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=120,
                       stdin=subprocess.DEVNULL,
                       env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8",
                            "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
    rows = {"inside": [], "scratch_outside": [], "system": [], "execve": []}
    for line in log.read_text(errors="replace").splitlines():
        em = EXEC_RE.search(line)
        if em:
            rows["execve"].append(em.group(1))
        if not OPEN_RE.search(line):
            continue
        m = DONE_RE.search(line)
        if not m or m.group(1).startswith("E") or m.group(1).startswith("-") or not m.group(2):
            continue
        p = pathlib.Path(m.group(2))
        if p == d or p.is_relative_to(d):
            rows["inside"].append(f"{line.strip()[:150]}")
        elif p == root or p.is_relative_to(root):
            rows["scratch_outside"].append(f"{line.strip()[:150]}")
        else:
            rows["system"].append(str(p))
    return {"module": fx["module"], "fid": fx["fid"], "verdict": r.stdout.strip(),
            "rc": r.returncode, "stderr": (r.stderr.strip().splitlines() or [""])[-1][:160],
            "execve": rows["execve"], "inside_n": len(rows["inside"]),
            "scratch_outside_n": len(rows["scratch_outside"]), "scratch_outside": rows["scratch_outside"],
            "inside_examples": rows["inside"][:6], "system_n": len(rows["system"]),
            "system_top": sorted(set(rows["system"]))[:8], "log": str(log), "log_lines": sum(1 for _ in open(log))}


def main():
    clone, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    mods = [pathlib.Path(m) for m in sys.argv[3:]]
    k44 = load(clone / "plans/round44_c1_verify.py", "k44")
    root = work / "four"
    if root.exists():
        subprocess.run(["rm", "-rf", str(root)], check=True)
    (root / "empty").mkdir(parents=True)
    (root / "fence").mkdir()
    (root / "logs").mkdir()
    (root / "harness.py").write_text(HARNESS)
    fence = root / "fence" / "fixture_fence.py"
    fence.write_bytes((clone / "plans/fixture_fence.py").read_bytes())
    out = []
    for m in mods:
        for fx in build(k44, root, clone, m):
            out.append(run(k44, root, fence, fx, f'{m.stem}-{fx["fid"]}'))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
