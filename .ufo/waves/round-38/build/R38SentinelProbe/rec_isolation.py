import importlib.util, pathlib, shutil, subprocess, sys, tempfile
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r38/R38SentinelProbe")
P = S/"lane/plans/build_pmars_probe.py"
spec = importlib.util.spec_from_file_location("bp", P); m = importlib.util.module_from_spec(spec)
sys.modules["bp"] = m; spec.loader.exec_module(m)
cap = S/"lane"/m.CAP
root = pathlib.Path(tempfile.mkdtemp(prefix="rec-", dir=S))
HOSTILE = open(S/"e1.py").read().split("script = r'''",1)[1].split("'''",1)[0]
case = m.Case("hostile", m.Art(kind="absent"), (), "FFFF", (), "hostile harness")
print("== hostile harness inside the probe sandbox ==")
print(m.run_case(cap, root, case, HOSTILE)[1])
ENVP = ('import os, socket\nprint("ENV", sorted(os.environ))\n'
        'try: socket.socket(socket.AF_UNIX).connect(os.environ.get("SSH_AUTH_SOCK","/nonexistent")); print("AGENT reachable")\n'
        'except Exception as e: print("AGENT blocked", type(e).__name__)\n')
print("== env / agent socket ==")
print(m.run_case(cap, root, m.Case("envs", m.Art(kind="absent"), (), "FFFF", (), "env"), ENVP)[1])
print("== leftover process (normal exit, then external kill) ==")
m.run_case(cap, root, m.Case("spawn", m.Art(kind="absent"), (), "FFFF", (), "spawn"),
           'import subprocess\nsubprocess.Popen(["/bin/sh","-c","setsid sleep 400 >/dev/null 2>&1 &"])\n')
work = root/"hangw"; (work/"ulb").mkdir(parents=True); (work/"ulsb").mkdir(); (work/"build").mkdir()
m.build_art(m.Art(), work/"ulb"/"pmars", work/"build"); m.stage_app((), work/"app")
(work/"harness.py").write_text('import subprocess,time\nsubprocess.Popen(["/bin/sh","-c","setsid sleep 500 >/dev/null 2>&1 &"])\ntime.sleep(60)\n')
env = {"PATH": m.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
try:
    subprocess.run(m.sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py"], env=env, capture_output=True, text=True, timeout=3)
except subprocess.TimeoutExpired:
    print("TIMEOUT_RAISED TimeoutExpired")
ps = subprocess.run(["ps","-eo","pid,args"], capture_output=True, text=True).stdout
print("SURVIVORS", [l.strip() for l in ps.splitlines() if "sleep 400" in l or "sleep 500" in l])
shutil.rmtree(root, ignore_errors=True)
