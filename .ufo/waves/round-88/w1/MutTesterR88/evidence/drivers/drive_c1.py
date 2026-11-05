import subprocess, concurrent.futures as cf, pathlib, sys, json, shutil, os

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r88/MutTesterR88")
mutants = {"unmut": S / "mut/c1_base.py"}
for p in sorted((S / "mut").glob("c1_m*.py")):
    mutants[p.stem[3:]] = p
fixtures = {"tip": S / "tip"}
for p in sorted((S / "fx").glob("c1-*")):
    fixtures[p.name] = p


def cell_path(m, f):
    return S / "out" / f"c1__{m}__{f}.txt"


def run(mname, fname):
    out = cell_path(mname, fname)
    fx = fixtures[fname]
    work = S / "work" / f"c1__{mname}__{fname}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}
    proc = subprocess.run([sys.executable, "-B", str(mutants[mname]), "--lane", str(fx), "--rev", "HEAD",
                           "--work", str(work)],
                          capture_output=True, text=True, timeout=900, cwd=str(S), env=env)
    text = proc.stdout + proc.stderr
    out.write_text(f"RC {proc.returncode}\n" + text)
    return mname, fname, proc.returncode


jobs = [(m, f) for m in mutants for f in fixtures if not cell_path(m, f).exists()]
print("pending", len(jobs), flush=True)
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for m, f, rc in ex.map(lambda mf: run(*mf), jobs):
        print("done", m, f, rc, flush=True)
print("ALL DONE", flush=True)
