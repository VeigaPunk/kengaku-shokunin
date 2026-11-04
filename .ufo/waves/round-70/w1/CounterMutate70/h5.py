import hashlib, pathlib, subprocess, sys
S=pathlib.Path("/fast/scratch/hyaku/kengaku-r70/CounterMutate70")
L=pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE_REL="plans/round70_c1_nginx_probe.py"
lane=S/"lane-baseline"
edited=(L/PROBE_REL).read_bytes()+b"# post-run edit\n"
(lane/PROBE_REL).write_bytes(edited)
esha=hashlib.sha256(edited).hexdigest()
good=(S/"receipts"/"baseline.txt").read_text().splitlines()
blob=hashlib.sha256(subprocess.run(["git","-C",str(lane),"cat-file","blob",f"master:{PROBE_REL}"],capture_output=True).stdout).hexdigest()
out=[]
for ln in good:
    if ln.startswith("PROBE "): ln=f"PROBE {PROBE_REL} sha256 {esha}"
    elif ln.startswith("PROBE_BLOB "): ln=f"PROBE_BLOB {PROBE_REL} sha256 {esha}"
    out.append(ln)
p=S/"receipts"/"h5-edited-committed.txt"; p.write_text("\n".join(out)+"\n")
r=subprocess.run([sys.executable,str(lane/PROBE_REL),"--check-receipt",str(p)],capture_output=True,text=True)
print("edited sha",esha); print("committed blob",blob); print("rc=",r.returncode); print(r.stdout,end="")
print(f"H5 rc={r.returncode} accepted={r.returncode==0} (committed probe, post-run edit + forged receipt)")
(lane/PROBE_REL).write_bytes((L/PROBE_REL).read_bytes())
print("restored exact:", hashlib.sha256((lane/PROBE_REL).read_bytes()).hexdigest()==hashlib.sha256((L/PROBE_REL).read_bytes()).hexdigest())
