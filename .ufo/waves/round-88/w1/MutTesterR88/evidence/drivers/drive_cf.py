import subprocess, concurrent.futures as cf, pathlib, sys, shutil

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r88/MutTesterR88")
mutants = {"unmut": S / "mut/cf_base.py"}
for p in sorted((S / "mut").glob("cf_m*.py")):
    mutants[p.stem[3:]] = p
fixtures = {"tip": S / "tip"}
for n in ["c2-claimed9", "c2-unexp", "c2-missing", "c2-kv4", "c2-f6"]:
    fixtures[n] = S / "fx" / n
env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}


def run_check(mname, fname):
    out = S / "out" / f"cf__{mname}__{fname}.txt"
    work = S / "work" / f"cf__{mname}__{fname}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    proc = subprocess.run([sys.executable, "-B", str(mutants[mname]), "--lane", str(fixtures[fname]),
                           "--rev", "HEAD", "--work", str(work)],
                          capture_output=True, text=True, timeout=1500, cwd=str(S), env=env)
    out.write_text(f"RC {proc.returncode}\n" + proc.stdout + proc.stderr)
    return ("check", mname, fname, proc.returncode)


def run_selftest(mname):
    out = S / "out" / f"cfst__{mname}.txt"
    work = S / "work" / f"cfst__{mname}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    proc = subprocess.run([sys.executable, "-B", str(mutants[mname]), "--lane", str(fixtures["tip"]),
                           "--rev", "HEAD", "--work", str(work), "--selftest"],
                          capture_output=True, text=True, timeout=1500, cwd=str(S), env=env)
    out.write_text(f"RC {proc.returncode}\n" + proc.stdout + proc.stderr)
    return ("selftest", mname, "tip", proc.returncode)


jobs = [("check", m, f) for m in mutants for f in fixtures if not (S / "out" / f"cf__{m}__{f}.txt").exists()]
jobs += [("selftest", m, None) for m in mutants if not (S / "out" / f"cfst__{m}.txt").exists()]
print("pending", len(jobs), flush=True)


def dispatch(job):
    kind, m, f = job
    return run_check(m, f) if kind == "check" else run_selftest(m)


with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for res in ex.map(dispatch, jobs):
        print("done", *res, flush=True)
print("ALL DONE", flush=True)
