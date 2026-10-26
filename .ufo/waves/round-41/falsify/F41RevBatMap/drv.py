"""F41RevBatMap: rebuild r_map fixtures, run traced reference/mutant copies of tip_receipts.py,
record whether each mutated site executes on every fixture, and re-evaluate the counter's kill rule."""
import importlib.util
import json
import pathlib
import shutil
import subprocess

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/F41RevBatMap")
LANE = S / "lane"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cnt = load(LANE / "plans" / "round41_c1_verify.py", "k41cnt")
mod = load(S / "batonly" / "r_map.py", "rmap")

root = S / "fx"
shutil.rmtree(root, ignore_errors=True)
ctx = cnt.Ctx(root)
fixtures = []
for k, fx in enumerate(mod.FIXTURES):
    d = root / f"f{k:03d}"
    d.mkdir(parents=True)
    argv = fx["build"](ctx, d)
    fixtures.append({**fx, "dir": d, "argv": argv})

src = (LANE / "plans" / "tip_receipts.py").read_text()
PY = "/usr/bin/python3"
(S / "emptyhome").mkdir(exist_ok=True)
ENV = {"PATH": cnt.PATH, "HOME": str(S / "emptyhome"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "PYTHONDONTWRITEBYTECODE": "1",
       "GIT_CEILING_DIRECTORIES": str(S), "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
       "GIT_CONFIG_COUNT": "2", "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
       "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null"}
TARGETS = ("T09", "T10", "T11", "T12")
PRE = {"T09", "T11"}  # marker before the changed line; the others take it after the assignment


def run_variant(text, tag):
    vdir = S / "var"
    vdir.mkdir(exist_ok=True)
    v = vdir / f"{tag}.py"
    v.write_text(text)
    rows = []
    for i, fx in enumerate(fixtures):
        work = S / "run" / f"{tag}-{i:02d}"
        tmp = S / "runtmp" / f"{tag}-{i:02d}"
        work.mkdir(parents=True, exist_ok=True)
        tmp.mkdir(parents=True, exist_ok=True)
        cmd = cnt.ro_sandbox(writable=(work, tmp)) + [PY, str(v), *fx["argv"]]
        env = dict(ENV, TMPDIR=str(tmp))
        r = subprocess.run(cmd, cwd=str(fx["dir"]), env=env, capture_output=True, text=True, timeout=300)
        rows.append({"fid": fx["fid"], "rc": r.returncode, "cls": sorted(cnt.classes("receipts", r.stdout)),
                     "trace": sorted(set(l for l in r.stderr.splitlines() if l.startswith("TRACE-")))})
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)
    return rows


out = {"fixtures": [{"fid": fx["fid"], "defects": sorted(fx["defects"])} for fx in fixtures], "mutants": {}}
for mid, tool, cls, direction, adv, label, wit, old, new in cnt.MUTANTS:
    if mid not in TARGETS:
        continue
    assert src.count(old) == 1, (mid, src.count(old))
    indent = old.split("\n")[0][: len(old.split("\n")[0]) - len(old.split("\n")[0].lstrip())]
    if mid in PRE:
        ref_t = src.replace(old, indent + f'sys.stderr.write("TRACE-{mid} ref-site\\n")\n' + old, 1)
        mut_t = src.replace(old, indent + f'sys.stderr.write("TRACE-{mid} mut-site\\n")\n' + new, 1)
    else:
        ref_t = src.replace(old, old + "\n" + f'sys.stderr.write("TRACE-{mid} ref-site pattern=%r\\n" '
                                             f'% (STEM_RE if "{mid}"=="T10" else CANDIDATE_RE).pattern)', 1)
        mut_t = src.replace(old, new + "\n" + f'sys.stderr.write("TRACE-{mid} mut-site pattern=%r\\n" '
                                              f'% (STEM_RE if "{mid}"=="T10" else CANDIDATE_RE).pattern)', 1)
    rrows = run_variant(ref_t, f"{mid}-ref")
    mrows = run_variant(mut_t, f"{mid}-mut")
    kills = []
    for rr, mr, fx in zip(rrows, mrows, fixtures):
        ref = (rr["rc"], frozenset(rr["cls"]))
        mut = (mr["rc"], frozenset(mr["cls"]))
        ex = cnt.exhibits(cls, direction, fx, ref, mut)
        out["mutants"].setdefault(mid, {"cls": cls, "direction": direction, "fixtures": []})["fixtures"].append(
            {"fid": fx["fid"], "ref_rc": rr["rc"], "ref_cls": rr["cls"], "ref_trace": rr["trace"],
             "mut_rc": mr["rc"], "mut_cls": mr["cls"], "mut_trace": mr["trace"], "exhibits": ex})
        if ex:
            kills.append(fx["fid"])
    out["mutants"][mid]["kill_by"] = kills[0] if kills else None
    out["mutants"][mid]["kill_sites"] = kills

(S / "exec.json").write_text(json.dumps(out, indent=1))
print("done")
