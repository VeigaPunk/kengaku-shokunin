#!/usr/bin/env python3
"""Non-author probe: rebuild s_modes fixtures, run reference/mutant/instrumented tool on each."""
import importlib.util, json, os, pathlib, shutil, subprocess, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcModes")
BAT = S / "bat" / "s_modes.py"
TOOL = (S / "lane" / "plans" / "sources_adopt.py").read_text()
FX = S / "fx"
SLOT = S / "slot"
BWRAP = "/usr/bin/bwrap"
PY = "/usr/bin/python3"
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


class Ctx:
    def __init__(self, root): self.root = root
    def write(self, path, text):
        p = pathlib.Path(path)
        if not p.resolve().is_relative_to(self.root.resolve()):
            raise RuntimeError(f"write outside fixture: {p}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    def sh(self, *a, **k): raise RuntimeError("sh not needed")
    def init(self, dest): raise RuntimeError("git not needed")
    def git(self, *a, **k): raise RuntimeError("git not needed")


def load_mod():
    spec = importlib.util.spec_from_file_location("s_modes_probe", BAT)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def build_all():
    mod = load_mod()
    if FX.exists(): shutil.rmtree(FX)
    FX.mkdir()
    out = []
    for k, fx in enumerate(mod.FIXTURES):
        d = FX / f"f{k:03d}"
        d.mkdir(parents=True)
        argv = fx["build"](Ctx(d), d)
        out.append({"fid": fx["fid"], "expect": fx["expect"], "argv": argv, "dir": str(d)})
    return out


def variant(name, old, new, marker=None):
    """Return path to a tool copy; marker inserts an stderr probe immediately before the old line."""
    src = TOOL
    assert src.count(old) == 1, (name, src.count(old))
    if marker:
        # insert probe just before the mutated line, same indentation as that line
        indent = old[: len(old) - len(old.lstrip(" "))]
        probe = (f'{indent}import sys as _s; _s.stderr.write("SITE-{name}-REACHED\\n")\n')
        src = src.replace(old, probe + old, 1)
    else:
        src = src.replace(old, new, 1)
    SLOT.mkdir(exist_ok=True)
    p = SLOT / f"{name}.py"
    p.write_text(src)
    return p


def run(toolpath, fx):
    work = S / "wrun"; tmp = S / "wtmp"
    for p in (work, tmp):
        if p.exists(): shutil.rmtree(p)
        p.mkdir()
    slot = S / "slot" / "sources.py"
    shutil.copyfile(toolpath, slot)
    cmd = [BWRAP, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net",
           "--die-with-parent", "--new-session", "--bind", str(work), str(work), "--bind", str(tmp), str(tmp),
           "--ro-bind", str(slot), str(slot),
           PY, str(slot), *fx["argv"]]
    env = {"PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(tmp)}
    r = subprocess.run(cmd, cwd=fx["dir"], env=env, capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout, r.stderr


MUTS = {
    "S01": ("        if args.registry or args.package:", "        if False:"),
    "S04": ('    if args.url_map:\n        parser.error("--url-map needs', '    if False:\n        parser.error("--url-map needs'),
    "S08": ("        if not (args.quote_file and args.artifact):", "        if False:"),
    "S09": ('            if problem:\n                print(f"QUOTE problem={problem}")',
            '            if False:\n                print(f"QUOTE problem={problem}")'),
}

if __name__ == "__main__":
    fxs = build_all()
    print("BUILT", json.dumps([{"fid": f["fid"], "argv": f["argv"]} for f in fxs], indent=1))
    print("DIGEST tool", __import__("hashlib").sha256(TOOL.encode()).hexdigest())
    SLOT.mkdir(exist_ok=True)
    (SLOT / "ref.py").write_text(TOOL)
    ref = SLOT / "ref.py"
    for m, (old, new) in MUTS.items():
        variant(m, old, new)
        variant(m + "-MARK", old, new, marker=m)
    results = {}
    for f in fxs:
        row = {}
        for name in ["ref"] + sorted(MUTS) + [m + "-MARK" for m in sorted(MUTS)]:
            if name == "ref":
                rc, out, err = run(ref, f)
            else:
                rc, out, err = run(SLOT / f"{name}.py", f)
            row[name] = {"rc": rc, "out": out[-700:], "err": err[-500:]}
        results[f["fid"]] = row
    print(json.dumps(results, indent=1))
