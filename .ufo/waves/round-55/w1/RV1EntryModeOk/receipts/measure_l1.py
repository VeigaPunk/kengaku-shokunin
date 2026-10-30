import json,re,sys
# usage: measure_l1.py SKILL.md LEDGER.json  (read-only; prints first-cell-command token equality vs ledger argv)
t=open(sys.argv[1]).read()
i=t.find("## Gate/probe registry"); j=t.find("\n## ",i+5); blk=t[i:j]
cells={}
for l in blk.splitlines():
    m=re.match(r"^\|\s*`([^`]+)`\s*\|",l)
    if m: cells[m.group(1)]=re.split(r"(?<!\\)\|", l.strip().strip("|"))[2]
L=json.load(open(sys.argv[2]))["rows"]
def first_cmd(c):
    for cmd in re.findall(r"`([^`]*)`", c):
        if "python3" in cmd or cmd.startswith("uv "): return cmd
    return ""
eq=0; print("rows",len(L),"cells",len(cells))
for n,r in sorted(L.items()):
    fc=first_cmd(cells[n]).split()
    if fc==r["entry_argv"]: eq+=1
    else: print("NOT-EQUAL",n,"ledger=",r["entry_argv"],"cell=",fc)
print("token-equal first-cell-command:",eq,"/",len(L))
print("uv-argv rows:",[n for n,r in L.items() if r["entry_argv"][0]=="uv"])
