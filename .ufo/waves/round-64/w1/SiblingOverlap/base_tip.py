import subprocess, re, pathlib
LANE=pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
base="5f517fe7147831f96a9900c9642c07ee71031940"
frozen=[l.strip() for l in (LANE/"corpus/evidence/round64/trio-red-at-base.txt").read_text().splitlines() if l.strip()]
col0=[];string=[]
for rel in frozen:
    t=subprocess.run(["git","-C",str(LANE),"show",f"{base}:{rel}"],capture_output=True,text=True).stdout
    if re.search(r"(?m)^verified-at:",t): col0.append(rel)
    if "verified-at" in t: string.append(rel)
print("BASE TIP", base)
print("frozen red entries:", len(frozen))
print("  with a COLUMN-0 'verified-at:' KEY:", len(col0), col0)
print("  with the STRING 'verified-at'    :", len(string), string)
