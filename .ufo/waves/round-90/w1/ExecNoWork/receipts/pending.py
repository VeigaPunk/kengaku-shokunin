import json,sys
rows=[]
bad=[]
for n,l in enumerate(open(sys.argv[1]),1):
    if not l.strip(): continue
    try: o=json.loads(l)
    except Exception: bad.append(n); continue
    rows.append((n,o))
print("lines",sum(1 for _ in open(sys.argv[1])),"bad_json",bad)
pend=[]
for n,o in rows:
    if not isinstance(o,dict) or "id" not in o: print("nonrow",n); continue
    if o.get("supersedes"): continue
    if o.get("status") in ("open","blocked"):
        pend.append((n,o))
print("pending base rows",len(pend))
for n,o in pend:
    print(n,o["id"],o.get("opened_round"),o.get("status"),"check" if o.get("check") else "-", o.get("source"), o.get("class"))
