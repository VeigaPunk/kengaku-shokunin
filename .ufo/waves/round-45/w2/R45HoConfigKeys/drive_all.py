#!/usr/bin/env python3
"""R45HoConfigKeys driver: the LANDED fence (round-45 counter machinery, unchanged: r45.build_module builds
each held-out module in the round-44 sandbox, r45.run_fence decides each fixture under strace -f -y and counts
opens outside the fixture) then hands every ADMITTED fixture to the landed tool the way the round-44 counter's
Runner does — same env shape, same ro_sandbox, cwd = fixture dir — under strace, once with the counter's four
executable-key GIT_CONFIG pins and once without, to measure which config keys a tool run would honour outside
the fixture. Optional argv filter: a substring a module file name must contain."""
import importlib.util
import itertools
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45HoConfigKeys")
LANE = S / "lane"
MY = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/w2/R45HoConfigKeys")
STRACE = "/usr/bin/strace"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def honour(seq, fx, tool_copy, k44, root, keep):
    """Two tool runs on one admitted fixture: counter env (pins) and pins-off. Reports the tool's exit, its
    last stdout line, and every strace line whose resolved path touches the module's outside artefact dir."""
    d = fx["dir"]
    artdir = d.parent / "evil"
    base = {"PATH": k44.PATH, "HOME": str(root / "home"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
            "GIT_CEILING_DIRECTORIES": str(root), "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}
    for label, env in (("pins", dict(base, **k44.GIT_PINS)), ("nopins", dict(base))):
        n = next(seq)
        tmp = root / "rtmp" / f"t{n:06d}"
        tmp.mkdir(parents=True, exist_ok=True)
        log = tmp / "strace.txt"
        cmd = k44.ro_sandbox(writable=(tmp,),
                             hide=k44.hide_list((LANE, root / "fence", root / "mods"), existing=True),
                             empty=root / "empty") \
            + [STRACE, "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat,execve,execveat",
               "-o", str(log), k44.PY, str(tool_copy), *fx["argv"]]
        try:
            r = subprocess.run(cmd, cwd=str(d), env=env, capture_output=True, text=True,
                               timeout=300, stdin=subprocess.DEVNULL)
            rc, tail = r.returncode, (r.stdout.strip().splitlines() or [""])[-1][:120]
        except subprocess.TimeoutExpired:
            rc, tail = "timeout", ""
        hits = []
        if log.exists():
            shutil.copy(log, keep / f"tool-{fx['fid']}-{label}.txt")
            for line in log.read_text(errors="replace").splitlines():
                if str(artdir) in line:
                    hits.append(" ".join(line.split())[:160])
        print(f"TOOL-RUN {fx['fid']} env={label} exit={rc} evil-touches={len(hits)} last={tail}")
        for h in hits[:4]:
            print(f"  EVIL {h}")


def main():
    keep = S / "keep"
    keep.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    k44 = load(LANE / "plans/round44_c1_verify.py", "kengaku_r44_counter")
    r45 = load(LANE / "plans/round45_c1_verify.py", "kengaku_r45_counter")
    root = pathlib.Path(tempfile.mkdtemp(prefix="hoconfig-", dir=S / "w"))
    (root / "harness.py").write_text(r45.HARNESS)
    (root / "fence").mkdir()
    (root / "home").mkdir()
    (root / "rtmp").mkdir()
    (root / "tools").mkdir()
    fence_copy = root / "fence" / "fixture_fence.py"
    fence_copy.write_bytes((LANE / "plans/fixture_fence.py").read_bytes())
    print(f"FENCE-COPY plans/fixture_fence.py sha256={r45.sha256(fence_copy)}")
    tools = {}
    for name, rel in k44.TOOLS.items():
        dst = root / "tools" / pathlib.Path(rel).name
        dst.write_bytes((LANE / rel).read_bytes())
        tools[name] = dst
        print(f"TOOL-COPY {rel} sha256={r45.sha256(dst)}")
    os.environ["K45_KEEP_STRACE"] = str(keep)
    seq = itertools.count(1)
    n = 0
    for modfile in sorted(MY.glob("h*.py")):
        if only and only not in modfile.name:
            continue
        fxs = r45.build_module(k44, LANE, root, modfile)
        for fx in fxs:
            verdict, why, opens = r45.run_fence(k44, LANE, root, fence_copy, fx, n)
            print(f"FENCE-RUN {modfile.name} {fx['fid']} tool={fx['tool']} {verdict} opens={opens}"
                  + (f" -- {why}" if why else ""))
            if verdict == "ADMIT":
                honour(seq, fx, tools[fx["tool"]], k44, root, keep)
            n += 1
    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
