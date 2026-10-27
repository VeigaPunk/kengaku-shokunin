import os, pathlib, shutil, subprocess, re, sys
S = pathlib.Path(os.environ["S"]); lane0 = S/"lane"
src = (lane0/"plans/round_close.py").read_text()
W = S/"tx"; shutil.rmtree(W, ignore_errors=True); W.mkdir()
def git(r,*a): subprocess.run(["git","-C",str(r),"-c","user.name=f","-c","user.email=f@l",*a],check=True,capture_output=True)
def mk(name, order_stub, census_stub, claims):
    r = W/name/"lane"; (r/"plans").mkdir(parents=True); (r/"corpus/evidence/round39").mkdir(parents=True); (r/"scripts").mkdir()
    subprocess.run(["git","init","-q","-b","master",str(r)],check=True)
    (r/"plans/round-39-claims.md").write_text(claims); (r/"plans/order_check.py").write_text(order_stub)
    (r/"corpus/SOURCES.md").write_text("#\n"); (r/"corpus/evidence/round39/git-leak-probe.txt").write_text("c\n")
    c = r/"scripts/sources-census.sh"; c.write_text(census_stub); c.chmod(0o755)
    git(r,"add","-A"); git(r,"commit","-q","-m","f"); return r
CL = "# c\n\n**Probe:** `plans/git_leak_probe.py`.\n"
CL_DUP = CL + "\nReceipt: `corpus/evidence/round39/git-leak-probe.txt`\n"
O_PLAIN = "import sys\nprint('ORDER ok')\n"          # newline present
O_NONL = "import sys\nsys.stdout.write('ORDER ok')\n"  # no trailing newline
O_ERR = "import sys\nprint('ORDER ok'); sys.stderr.write('ORDER-STDERR\\n')\n"
C_OK = "#!/bin/sh\necho CENSUS\nexit 0\n"
C_ERR = "#!/bin/sh\necho CENSUS\necho CENSUS-STDERR >&2\nexit 0\n"
F = {"base": mk("base", O_PLAIN, C_OK, CL), "dup": mk("dup", O_PLAIN, C_OK, CL_DUP), "nonl": mk("nonl", O_NONL, C_OK, CL),
     "oerr": mk("oerr", O_ERR, C_OK, CL), "cerr": mk("cerr", O_PLAIN, C_ERR, CL)}
afile = W/"afile"; afile.write_text("x")
def argv(k): return ["--lane",str(F[k]),"--round","39","--census",str(F[k]/"scripts/sources-census.sh")]
CASES = [("base",argv("base")),("dup",argv("dup")),("nonl",argv("nonl")),("oerr",argv("oerr")),("cerr",argv("cerr")),
         ("lane-file",["--lane",str(afile),"--round","39","--census",str(F["base"]/"scripts/sources-census.sh")]),
         ("selftest-stub",["--lane",str(F["base"]),"--census",str(F["base"]/"scripts/sources-census.sh"),"--selftest"])]
M = [("L116","if rel and rel not in found:","if rel or  rel not in found:"),
     ("L165","if not lane.is_dir():","if False                 :"),
     ("L200a","out.write(r.stdout if r.stdout.endswith(\"\\n\") or not r.stdout else","out.write(r.stdout if r.stdout.endswith(\"\\n\") and not r.stdout else"),
     ("L200b","or not r.stdout else r.stdout","or     r.stdout else r.stdout"),
     ("L201","if r.stderr.strip():\n            print(r.stderr.strip(), file=sys.stderr)\n        verdict = {0: \"PASS\", 1: \"FAIL\"}.get(r.returncode, \"ERROR\")\n        say(f\"ROUND-CLOSE order","if False:\n            print(r.stderr.strip(), file=sys.stderr)\n        verdict = {0: \"PASS\", 1: \"FAIL\"}.get(r.returncode, \"ERROR\")\n        say(f\"ROUND-CLOSE order"),
     ("L210","if r.stderr.strip():\n        print(r.stderr.strip(), file=sys.stderr)\n    warnings","if False:\n        print(r.stderr.strip(), file=sys.stderr)\n    warnings"),
     ("L300","        if not ok:\n            sys.stderr.write","        if False:\n            sys.stderr.write")]
def norm(s): return re.sub(r"/fast/scratch/\S*|/tmp/\S*|\d+\.\d+s|round-close-selftest-\S*","<p>",s)
def run(f,a):
    p = subprocess.run(["python3",str(f),*a],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"),timeout=120)
    return (p.returncode, norm(p.stdout), norm(p.stderr))
ref = f = W/"ref"/"round_close.py"; f.parent.mkdir(); f.write_text(src)
R = [run(ref,a) for _,a in CASES]; R2 = [run(ref,a) for _,a in CASES]; print("REF-STABLE", R==R2)
for n,(rc,o,e) in zip([c for c,_ in CASES],R): print("REF",n,rc,"out_lines",len(o.splitlines()),"err_lines",len(e.splitlines()))
for mid,old,new in M:
    assert src.count(old)==1, (mid, src.count(old))
    mf = W/mid/"round_close.py"; mf.parent.mkdir(); mf.write_text(src.replace(old,new,1))
    k=[]
    for (n,a),r0 in zip(CASES,R):
        r = run(mf,a)
        if r!=r0: k.append(f"{n}:rc{r0[0]}>{r[0]}"+(":out" if r[1]!=r0[1] else "")+(":err" if r[2]!=r0[2] else ""))
    print(mid, k or "UNWITNESSED")
