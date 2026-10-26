import json, pathlib, subprocess, shutil
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcModes")
TOOL = (S/"lane/plans/sources_adopt.py").read_text()
FX = S/"fx"; SLOT = S/"slot"; BWRAP="/usr/bin/bwrap"; PY="/usr/bin/python3"
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
def run(p, argv, cwd):
    work=S/"wrun2"; tmp=S/"wtmp2"
    for q in (work,tmp):
        if q.exists(): shutil.rmtree(q)
        q.mkdir()
    slot=S/"slot/sources.py"; shutil.copyfile(p, slot)
    cmd=[BWRAP,"--ro-bind","/","/","--dev","/dev","--proc","/proc","--unshare-pid","--unshare-net","--die-with-parent",
         "--new-session","--bind",str(work),str(work),"--bind",str(tmp),str(tmp),"--ro-bind",str(slot),str(slot),
         PY,str(slot),*argv]
    r=subprocess.run(cmd,cwd=cwd,env={"PATH":PATH,"HOME":"/nonexistent","LANG":"C.UTF-8","LC_ALL":"C.UTF-8",
        "PYTHONDONTWRITEBYTECODE":"1","TMPDIR":str(tmp)},capture_output=True,text=True,timeout=300)
    return r.returncode,r.stdout,r.stderr
raw=open(S/"probe-out.json").read(); i=raw.index("\n{"); built=json.loads(raw[i+1:])
# rebuild argv map from bat module
import importlib.util
spec=importlib.util.spec_from_file_location("m",S/"bat/s_modes.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class C:
    def __init__(s,r): s.r=r
    def write(s,p,t):
        p=pathlib.Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t)
    def sh(s,*a,**k): raise SystemExit("no")
refp=S/"slot/ref.py"; refp.write_text(TOOL)
for k,fx in enumerate(m.FIXTURES):
    d=FX/f"f{k:03d}"
    rc,out,err=run(refp,fx["build"](C(d),d),str(d))
    print(f"[{fx['fid']}] ref rc={rc} last_stderr={err.strip().splitlines()[-1] if err.strip() else ''!r}")
    for mid in ("S01","S04","S08","S09"):
        p=S/"slot"/f"{mid}.py"
        if not p.exists(): continue
        rc2,out2,err2=run(p,fx["build"](C(d),d),str(d))
        exc=[l for l in err2.splitlines() if l.strip().startswith(("AttributeError","TypeError","FileNotFoundError","KeyError"))]
        print(f"    {mid}: mut rc={rc2}" + (f" exc={exc[-1].strip()}" if exc else ""))
