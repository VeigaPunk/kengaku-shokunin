#!/usr/bin/env python3
"""Extend the round-45 measurement to the round-46 B5 classes: trace every file-naming syscall (%file) and
report any scratch path outside d that the fence's process tree touches. Harness and fence copy are excepted."""
import importlib.util, json, pathlib, re, subprocess, sys

def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

LANE = pathlib.Path(sys.argv[1]).resolve(); ROOT = pathlib.Path(sys.argv[2]).resolve()
MODS = [pathlib.Path(p).resolve() for p in sys.argv[3:]]
k44 = load(LANE / "plans/round44_c1_verify.py", "k44_tp"); c1 = load(LANE / "plans/round45_c1_verify.py", "k45_tp")
ROOT.mkdir(parents=True, exist_ok=True)
for n in ("fx", "btmp", "mods", "empty", "fence", "trace"):
    (ROOT / n).mkdir(exist_ok=True)
(ROOT / "harness.py").write_text(c1.HARNESS)
fence_copy = ROOT / "fence" / "fixture_fence.py"
fence_copy.write_bytes((LANE / "plans/fixture_fence.py").read_bytes())
# extended classifier: any quoted/<...> path under ROOT, outside d, outside the fence copy/harness exceptions
PATH_RE = re.compile(r'"([^"]*)"|<([^<>]*)>')
def offenders(log, d, root):
    bad = []
    for line in log.read_text(errors="replace").splitlines():
        for m in PATH_RE.finditer(line):
            p = m.group(1) or m.group(2) or ""
            if not p.startswith("/"):
                continue
            p = pathlib.PurePath(p)
            s = str(p)
            if not (s == str(root) or s.startswith(str(root) + "/")):
                continue
            if s == str(d) or s.startswith(str(d) + "/"):
                continue
            if s == str(root / "harness.py") or s == str(root / "fence") or s.startswith(str(root / "fence") + "/"):
                continue
            if s.startswith(str(root / "trace") + "/"):
                continue
            bad.append(s)
    return bad
total = 0; hits = {}
for i, f in enumerate(MODS):
    try:
        fxs = c1.build_module(k44, LANE, ROOT, f)
    except Exception as e:  # noqa: BLE001
        print(f"BUILD-ERROR {f} {type(e).__name__}: {str(e)[:120]}"); continue
    for j, fx in enumerate(fxs):
        d = fx["dir"]; logdir = ROOT / "trace" / f"t{i:03d}{j:03d}"; logdir.mkdir(parents=True)
        log = logdir / "log"
        cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((LANE,), existing=True), empty=ROOT / "empty") + \
            ["/usr/bin/strace", "-f", "-qq", "-yy", "-e", "trace=%file", "-o", str(log),
             k44.PY, "-I", str(ROOT / "harness.py"), str(fence_copy), str(d), fx["tool"], json.dumps(fx["argv"])]
        r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=180, stdin=subprocess.DEVNULL,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                                "PYTHONDONTWRITEBYTECODE": "1"})
        bad = offenders(log, d, ROOT) if log.exists() else ["<log missing>"]
        import shutil; shutil.rmtree(logdir, ignore_errors=True)
        total += 1
        if bad:
            hits[fx["fid"]] = sorted(set(bad))[:4]
print(f"TRACED fixtures={total} with_outside_path_touch={len(hits)}")
for k, v in hits.items():
    print("TOUCH", k, v)
