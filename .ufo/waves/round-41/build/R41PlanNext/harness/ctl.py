import os, sys, shutil, subprocess, pathlib, tempfile, time, concurrent.futures as cf
S=pathlib.Path('/fast/scratch/hyaku/kengaku-r41/R41PlanNext'); TB=S/'tb2'
HARNESS='''
import importlib.util, sys, traceback
spec=importlib.util.spec_from_file_location("g","/tests/test_outputs.py"); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
res=[]
for n in sorted(k for k in dir(g) if k.startswith("test_")):
    try: getattr(g,n)(); res.append((n,"PASS"))
    except BaseException as e: res.append((n,"FAIL "+type(e).__name__+": "+str(e)[:80].replace("\\n"," ")))
for n,r in res: print("T",n,r)
print("SUMMARY pass=%d fail=%d"%(sum(r=="PASS" for _,r in res),sum(r!="PASS" for _,r in res)))
'''
def sb(app, tests, extra=()):
    a=["/usr/bin/bwrap","--unshare-net","--unshare-pid","--unshare-ipc","--die-with-parent","--new-session","--ro-bind","/usr","/usr"]
    for l in ("/bin","/sbin","/lib","/lib64"):
        if os.path.islink(l): a+=["--symlink",os.readlink(l),l]
    a+=["--ro-bind","/etc","/etc","--proc","/proc","--dev","/dev","--tmpfs","/tmp","--bind",str(app),"/app","--ro-bind",str(tests),"/tests","--ro-bind",str(S/'ctl_harness.py'),"/harness.py","--ro-bind",str(S/'ctl_solve.sh'),"/solve.sh","--chdir","/app"]
    return a+list(extra)
def job(task, mode):
    w=pathlib.Path(tempfile.mkdtemp(prefix=f"ctl-{task}-{mode}-",dir=S)); app=w/'app'; app.mkdir(); tests=w/'tests'
    t=TB/task
    shutil.copytree(t/'tests',tests)
    if task=='circuit-fibsqrt':
        shutil.copy(t/'environment/gates.txt',app); shutil.copy(t/'tests/sim.c',app)
    if task=='schemelike-metacircular-eval':
        shutil.copy(t/'environment/tests/interp.py',app); shutil.copytree(t/'environment/tests/test',app/'test')
        for d in ('test','shadow_test'):
            if not (tests/d).exists(): shutil.copytree(t/'environment/tests'/d, tests/d)
    shutil.copy(t/'solution/solve.sh', S/'ctl_solve.sh') if False else None
    sol=w/'solve.sh'; shutil.copy(t/'solution/solve.sh', sol)
    env={'PATH':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin','HOME':'/tmp'}
    out=[]; t0=time.time()
    def sbx(cmd, tests_):
        a=sb(app,tests_)
        # per-job solve.sh
        a[a.index('/solve.sh')-1]=str(sol)
        return a+cmd
    if mode=='oracle':
        p=subprocess.run(sbx(['bash','/solve.sh'],tests),capture_output=True,text=True,env=env,timeout=600)
        out.append(f"oracle-solve rc={p.returncode} t={time.time()-t0:.1f}s")
    t1=time.time()
    p=subprocess.run(sbx(['python3','/harness.py'],tests),capture_output=True,text=True,env=env,timeout=900)
    lines=[l for l in p.stdout.split('\n') if l.startswith(('T ','SUMMARY'))]
    out.append(f"{task} {mode} grader rc={p.returncode} t={time.time()-t1:.1f}s")
    out+=lines
    if not lines: out.append(p.stderr[-300:])
    shutil.rmtree(w,ignore_errors=True)
    return '\n'.join(out)
(S/'ctl_harness.py').write_text(HARNESS); (S/'ctl_solve.sh').write_text('')
jobs=[(t,m) for t in ('openssl-selfsigned-cert','circuit-fibsqrt','schemelike-metacircular-eval') for m in ('nop','oracle')]
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(lambda a: job(*a), jobs): print(r,flush=True)
