import subprocess, sys, shutil, pathlib, os
sys.path.insert(0, ".")
from cases import C
HERE = pathlib.Path(".").resolve(); TESTS = HERE.parent / "tb2/openssl-selfsigned-cert/tests"
SHORT = {"test_directory_structure":"dir","test_key_file":"key","test_certificate_file":"cert","test_combined_pem_file":"pem","test_verification_file":"verif","test_python_verification_script":"script"}
mode = sys.argv[1]
if mode == "dry":
    for cid,(pf,body,why) in C.items():
        print(f"{cid:28s} predicted_fail={','.join(sorted(pf)) or '-':30s} # {why}")
    print(f"cases={len(C)} predicted_pass={sum(1 for v in C.values() if not v[0])} predicted_fail={sum(1 for v in C.values() if v[0])}")
    sys.exit()
mism = 0; npass = 0; nfail = 0
for cid,(pf,body,why) in C.items():
    app = HERE / "app" / cid
    if app.exists(): shutil.rmtree(app)
    app.mkdir(parents=True)
    cmd = ["bwrap","--unshare-net","--unshare-user","--uid","0","--gid","0","--cap-add","ALL","--unshare-pid","--ro-bind","/usr","/usr","--symlink","usr/bin","/bin","--symlink","usr/lib","/lib","--symlink","usr/lib","/lib64","--ro-bind","/etc","/etc","--proc","/proc","--dev","/dev","--tmpfs","/tmp","--bind",str(app),"/app","--ro-bind",str(TESTS),"/tests","--ro-bind",str(HERE/"harness.py"),"/h.py","--ro-bind",str(HERE/"mk.sh"),"/mk.sh","--chdir","/app","bash","-c",f". /mk.sh; set +e; {body}; python /h.py"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    obs = {}
    for l in r.stdout.splitlines():
        if l.startswith("T "):
            p = l.split(); obs[SHORT[p[1]]] = (p[2], " ".join(p[3:]))
    fails = {k for k,(v,_) in obs.items() if v=="FAIL"}
    ok = fails == pf
    mism += (not ok)
    allpass = not fails
    npass += allpass; nfail += (not allpass)
    print(f"{cid:28s} observed_fail={','.join(sorted(fails)) or '-':30s} match={'yes' if ok else 'NO'}  {'' if ok else r.stderr[-200:]}")
print(f"cases={len(C)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
