#!/usr/bin/env python3
"""R46SentC3Sandbox draft: run a hostile polyglot main.py.c inside (a) the C3 probe draft's exact bwrap argv and
(b) the same argv hardened with the sandbox/limits this seat recommends.  Nothing here imports the grader or
executes a case: the payload is this seat's own file and the grader is never read."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import pathlib
import selectors
import shutil
import signal
import subprocess
import sys
import time

BWRAP = "/usr/bin/bwrap"
PROBE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py")
CAPTURE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC3Capture/tb2-polyglot-c-py")
PAYLOAD = pathlib.Path(__file__).with_name("main.py.c")
RUNSH = "#!/bin/bash\ngcc /app/main.py.c -o /app/cmain || exit 90\nexec /app/cmain \"$1\"\n"
HARD_AS = 512 << 20
HARD_FSIZE = 1 << 20
HARD_NPROC = 48
HARD_TMPFS = 64 << 20
HARD_SMALL = 8 << 20


def load_probe():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("c3_probe_draft", PROBE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['c3_probe_draft'] = mod
    spec.loader.exec_module(mod)
    return mod


def make_work(root: pathlib.Path, app_is_tmpfs: bool) -> pathlib.Path:
    work = root
    (work / "app").mkdir(parents=True, exist_ok=True)
    (work / "tests").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CAPTURE / "test_outputs.py", work / "tests" / "test_outputs.py")
    (work / "template.txt").write_text("# template\n")
    (work / "seed.sh").write_text("mkdir -p /app\n")
    (work / "recipe.sh").write_text(":\n")
    (work / "harness.py").write_text("print('noop')\n")
    shutil.copyfile(PAYLOAD, work / "main.py.c")
    if not app_is_tmpfs:
        shutil.copyfile(PAYLOAD, work / "app" / "main.py.c")
    (work / "run.sh").write_text(RUNSH)
    return work


def harden(argv: list[str], work: pathlib.Path) -> list[str]:
    out: list[str] = ["/usr/bin/prlimit",
                      f"--nproc={HARD_NPROC}", "--cpu=5", f"--fsize={HARD_FSIZE}", "--core=0",
                      f"--as={HARD_AS}", "--nofile=512", "--"]
    app_i = argv.index("--bind", argv.index("--tmpfs"))
    assert argv[app_i + 1] == str(work / "app") and argv[app_i + 2] == "/app", argv[app_i:app_i + 3]
    out += argv[:app_i]
    out += ["--unshare-uts", "--hostname", "k46sent"]
    out += ["--clearenv",
            "--setenv", "PATH", "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "--setenv", "HOME", "/tmp", "--setenv", "TMPDIR", "/tmp",
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "PYTHONUTF8", "1", "--setenv", "PYTHONDONTWRITEBYTECODE", "1"]
    tmp_i = out.index("--tmpfs")
    assert out[tmp_i + 1] == "/tmp", out[tmp_i:tmp_i + 2]
    out[tmp_i:tmp_i + 2] = ["--size", str(HARD_SMALL), "--tmpfs", "/tmp"]
    dev_i = out.index("/dev")
    out[dev_i + 1:dev_i + 1] = ["--size", str(HARD_SMALL), "--tmpfs", "/dev/shm", "--remount-ro", "/dev"]
    out += ["--size", str(HARD_TMPFS), "--tmpfs", "/app",
            "--ro-bind", str(work / "main.py.c"), "/app/main.py.c"]
    out += argv[app_i + 3:]
    return out


def run_capped(argv: list[str], env: dict | None, timeout: float, cap: int,
               stop_after: int | None = None) -> dict:
    t0 = time.time()
    p = subprocess.Popen(argv, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
    sel = selectors.DefaultSelector()
    sel.register(p.stdout, selectors.EVENT_READ, "out")
    sel.register(p.stderr, selectors.EVENT_READ, "err")
    kept = {"out": b"", "err": b""}
    total = {"out": 0, "err": 0}
    live = 2
    timed_out = False
    while live:
        left = timeout - (time.time() - t0)
        if left <= 0:
            timed_out = True
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            break
        for key, _ in sel.select(min(left, 0.25)):
            b = os.read(key.fileobj.fileno(), 65536)
            if not b:
                sel.unregister(key.fileobj)
                live -= 1
                continue
            k = key.data
            total[k] += len(b)
            if len(kept[k]) < cap:
                kept[k] += b[:cap - len(kept[k])]
            if stop_after and total[k] >= stop_after:
                sel.unregister(key.fileobj)
                live -= 1
    try:
        rc = p.wait(timeout=10)
    except subprocess.TimeoutExpired:
        rc = -9
    return {"rc": rc, "secs": round(time.time() - t0, 2), "timed_out": timed_out,
            "out_bytes": total["out"], "err_bytes": total["err"],
            "out": kept["out"].decode("utf-8", "replace"), "err": kept["err"].decode("utf-8", "replace")}


def harness_argv(variant: str, work: pathlib.Path, env: dict | None, lang: str, mode: str) -> list[str]:
    draft = DRAFT.sandbox_argv(CAPTURE, work)
    argv = draft if variant == "draft" else harden(draft, work)
    argv = argv + ["--ro-bind", str(work / "run.sh"), "/run.sh"]
    if variant == "hard":
        argv = argv + ["--remount-ro", "/"]
    if lang == "py":
        return argv + ["/usr/bin/python3", "/app/main.py.c", mode]
    return argv + ["/usr/bin/bash", "/run.sh", mode]


def one(variant: str, env: dict | None, lang: str, mode: str, cap: int, timeout: float,
        root: pathlib.Path, stop_after: int | None = None) -> dict:
    work = root / f"{variant}-{lang}-{mode}"
    make_work(work, app_is_tmpfs=(variant == "hard"))
    r = run_capped(harness_argv(variant, work, env, lang, mode), env, timeout, cap, stop_after)
    r["app_files"] = sorted(p.name for p in (work / "app").iterdir()) if (work / "app").is_dir() else []
    r["app_bytes"] = sum(p.stat().st_size for p in (work / "app").rglob("*") if p.is_file())
    r["variant"], r["lang"], r["mode"] = variant, lang, mode
    shutil.rmtree(work, ignore_errors=True)
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--variant", required=True, choices=("draft", "hard"))
    ap.add_argument("--cap", type=int, default=65536)
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--json-out", default="")
    ap.add_argument("--stop-after", type=int, default=0, help="stop reading a stream after N bytes")
    ap.add_argument("--only", default="", help="comma list of modes")
    ap.add_argument("--show-argv", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    root.mkdir(parents=True, exist_ok=True)
    if a.show_argv:
        print(" ".join(harden(DRAFT.sandbox_argv(CAPTURE, root / "<work>"), root / "<work>")))
        return 0
    env = None if a.variant == "hard" else DRAFT.ENV
    rows = []
    for lang in ("py", "c"):
        modes = a.only.split(",") if a.only else ("safe", "forks", "mem", "fill", "bigout", "cpu")
        for mode in modes:
            r = one(a.variant, env, lang, mode, a.cap, a.timeout, root, a.stop_after or None)
            rows.append(r)
            print(f"== RESULT variant={a.variant} lang={lang} mode={mode} rc={r['rc']} secs={r['secs']} "
                  f"timed_out={r['timed_out']} out_bytes={r['out_bytes']} app_files={r['app_files']} "
                  f"app_bytes={r['app_bytes']}", flush=True)
            for line in r["out"].splitlines():
                if mode == "bigout" and line.startswith("xxxx"):
                    continue
                print(line, flush=True)
            if r["err"].strip():
                print("STDERR " + r["err"].strip().replace("\n", " | ")[:400], flush=True)
    if a.json_out:
        pathlib.Path(a.json_out).write_text(json.dumps(rows, indent=1, sort_keys=True))
    return 0


DRAFT = load_probe()
if __name__ == "__main__":
    sys.exit(main())
