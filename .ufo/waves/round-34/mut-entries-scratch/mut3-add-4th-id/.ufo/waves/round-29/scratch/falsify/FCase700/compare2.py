import json, hashlib
LANE="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
d=json.load(open("/tmp/fc700_all.json"))
man=json.load(open(LANE+"/plans/fixtures/r29/manifest.json"))
prof=json.load(open(LANE+"/plans/fixtures/r29/profiles.json"))
order=man["replacement_order"]; tokens={n:"__%s__"%n for n in order}
raw_text=open(LANE+"/plans/fixtures/r28/webarena/config_files/test.raw.json").read()
raw=json.loads(raw_text)

def project(values):
    t=raw_text
    for n in order: t=t.replace(tokens[n], values[n])
    return t

def leafmap(o,p=""):
    m={}
    if isinstance(o,dict):
        for k,v in o.items(): m.update(leafmap(v,p+"/"+str(k)))
    elif isinstance(o,list):
        for i,v in enumerate(o): m.update(leafmap(v,p+"/"+str(i)))
    else: m[p]=o
    return m

for name,spec in prof.items():
    proj=json.loads(project(spec["values"]))
    rec=d["profiles"][name]["tasks"][700]
    A=leafmap(raw); B=leafmap(proj)
    assert set(A)==set(B), (len(A),len(B))
    derived={p:(A[p],B[p]) for p in A if A[p]!=B[p]}
    cl={c["json_pointer"]:c for c in rec["changed_leaves"]}
    print("==",name)
    print("  derived changed leaves:", sorted(derived))
    print("  instrument changed leaves:", sorted(cl))
    print("  pointer sets equal:", set(derived)==set(cl))
    for p in sorted(derived):
        a,b=derived[p]; c=cl.get(p)
        ok = c and c["original"]==a and c["projected"]==b and c["path_template"]==p[5:].replace("/eval/","eval.").replace("/start_url","start_url")
        print("   ",p,"| original match:",c and c["original"]==a,"| projected match:",c and c["projected"]==b,"| category:",c and c["category"],"| path_template:",c and c["path_template"])
    # task-scoped leaves (relative to item) count of changed
    itemA=leafmap(raw[700]); itemB=leafmap(rec["projected_task"])
    ch=[p for p in itemA if itemA[p]!=itemB[p]]
    print("  changed leaves within item:", ch)
    print("  is_multiple_occurrence_flag_any:", [c.get("tokens") for c in rec["changed_leaves"]])
    # pointer resolution test
    print("  pointer resolves in projected full parse:", rec["changed_leaves"][0]["json_pointer"], "->", eval("proj"+rec["changed_leaves"][0]["json_pointer"].replace("/","']['")) if False else _resolve(proj, rec["changed_leaves"][0]["json_pointer"]) if False else "")
