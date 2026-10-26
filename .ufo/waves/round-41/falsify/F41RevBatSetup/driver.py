"""F41RevBatSetup trace driver: prove the mutated line executes on its killing fixture.

Rebuilds every r_setup fixture with the counter's own Ctx, then runs, per fixture,
  - an instrumented REFERENCE (trace line immediately before the original line), and
  - an instrumented MUTANT   (trace line immediately before the mutated line),
through the counter's exact ro_sandbox/env/WORK-token expansion (Runner).
Trace goes to stderr so it cannot influence classes().
"""
import importlib.util
import json
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/F41RevBatSetup")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


c1 = load(f"{LANE}/plans/round41_c1_verify.py", "c1_counter")
mod = load(str(S / "battery-r_setup/r_setup.py"), "r_setup_module")

root = S / "tracework"
if root.exists():
    shutil.rmtree(root)
root.mkdir()
runner = c1.Runner(root, 2)

src = (S / "lane/plans/tip_receipts.py").read_text()
MUT = {m[0]: (m[7], m[8]) for m in c1.MUTANTS}

results = []
for k, fx in enumerate(mod.FIXTURES):
    d = root / "fx" / f"f{k:03d}"
    d.mkdir(parents=True)
    ctx = c1.Ctx(d)
    argv = fx["build"](ctx, d)
    fdict = {"argv": argv, "dir": d}
    mid = re.search(r"t\d+", fx["fid"]).group(0).upper()
    old, new = MUT[mid]
    n = src.count(old)
    assert n == 1, f"{mid}: old line count {n}"
    indent = old[: len(old) - len(old.lstrip())]
    refsrc = src.replace(
        old, f'{indent}sys.stderr.write("TRACE {mid} original-site reached\\n")\n{old}', 1)
    mutsrc = src.replace(
        old, f'{indent}sys.stderr.write("TRACE {mid} mutated-site reached\\n")\n{new}', 1)
    vdir = root / "var"
    vdir.mkdir(exist_ok=True)
    refp = vdir / f"ref-{mid}.py"
    mutp = vdir / f"mut-{mid}.py"
    refp.write_text(refsrc)
    mutp.write_text(mutsrc)
    py_compile.compile(str(refp), doraise=True, cfile=str(vdir / f"ref-{mid}.pyc"))
    py_compile.compile(str(mutp), doraise=True, cfile=str(vdir / f"mut-{mid}.pyc"))

    def run_capture(variant):
        i = next(runner.seq)
        work = runner.root / "work" / f"w{i:06d}"
        tmp = runner.root / "rtmp" / f"t{i:06d}"
        work.mkdir()
        tmp.mkdir()
        av = []
        for t in fdict["argv"]:
            m = c1.WORK_TOKEN.match(t)
            if m:
                w = work / "run"
                if m.group(1):
                    (w / m.group(1)).mkdir(parents=True, exist_ok=True)
                if m.group(2):
                    w.mkdir(exist_ok=True)
                av.append(str(w) + (m.group(2) or ""))
            else:
                av.append(t)
        slot = runner.slots / "receipts.py"
        cmd = c1.ro_sandbox(writable=(work, tmp), ro_binds=((variant, slot),)) + \
            [c1.PY, str(slot), *av]
        r = subprocess.run(cmd, cwd=str(fdict["dir"]), env=runner.env(tmp),
                           capture_output=True, text=True, timeout=600)
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)
        return {"rc": r.returncode, "stdout": r.stdout, "stderr": r.stderr,
                "classes": sorted(c1.classes("receipts", r.stdout))}

    rr = run_capture(refp)
    rm = run_capture(mutp)
    results.append({
        "fid": fx["fid"], "mutant": mid,
        "ref": {"rc": rr["rc"], "classes": rr["classes"],
                "trace": "original-site reached" in rr["stderr"],
                "setup_msg": [l for l in rr["stdout"].splitlines() if l.startswith("SETUP:")][:1]},
        "mut": {"rc": rm["rc"], "classes": rm["classes"],
                "trace": "mutated-site reached" in rm["stderr"],
                "stderr_tail": rm["stderr"].strip().splitlines()[-2:] if rm["stderr"].strip() else []},
    })

print(json.dumps(results, indent=1))
