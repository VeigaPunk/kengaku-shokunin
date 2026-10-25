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

def deepdiff(a,b,p=""):
    out=[]
    if type(a)!=type(b): return [(p,"TYPE",type(a).__name__,type(b).__name__)]
    if isinstance(a,dict):
        for k in a:
            if k not in b: out.append((p+"/"+str(k),"MISSING_IN_INSTRUMENT",a[k],None))
            else: out+=deepdiff(a[k],b[k],p+"/"+str(k))
        for k in b:
            if k not in a: out.append((p+"/"+str(k),"EXTRA_IN_INSTRUMENT",None,b[k]))
    elif isinstance(a,list):
        if len(a)!=len(b): out.append((p,"LEN",len(a),len(b)))
        for i in range(min(len(a),len(b))): out+=deepdiff(a[i],b[i],p+"/"+str(i))
    else:
        if a!=b: out.append((p,"VALUE",a,b))
    return out

for name,spec in prof.items():
    text=project(spec["values"]); item=json.loads(text)[700]
    rec=d["profiles"][name]["tasks"][700]
    pt=rec["projected_task"]
    diffs=deepdiff(item,pt,"")
    print("==",name,"projected_task deep diffs:",len(diffs))
    for x in diffs[:20]: print("   ",x)
    # key order check
    print("   projected_task top key order:", list(pt))
    print("   derived top key order       :", list(item))
    print("   output_index:", rec["output_index"], "task_id:", rec["task_id"], "index_equals_task_id:", rec["index_equals_task_id"])
    print("   output_filename:", rec["output_filename"])
    # recompute file sha
    nonl=hashlib.sha256(json.dumps(pt,indent=2).encode()).hexdigest()
    nl=hashlib.sha256((json.dumps(pt,indent=2)+"\n").encode()).hexdigest()
    print("   rec would_be_file_sha256:", rec["would_be_file_sha256"])
    print("   recomputed json.dumps(indent=2) sha:", nonl, "matches:", nonl==rec["would_be_file_sha256"])
    print("   recomputed +newline sha:", nl, "matches:", nl==rec["would_be_file_sha256"])
    # ascii-only check
    dump_ascii=json.dumps(pt,indent=2)
    print("   non-ascii present:", any(ord(c)>127 for c in dump_ascii), "| ensure_ascii=False differs:", json.dumps(pt,indent=2,ensure_ascii=False)!=dump_ascii)
    # changed leaves compare: derive from projected_task vs raw
    def leaves(o,p=""):
        if isinstance(o,dict):
            r=[]
            for k,v in o.items(): r+=leaves(v,p+"/"+str(k))
            return r
        if isinstance(o,list):
            r=[]
            for i,v in enumerate(o): r+=leaves(v,p+"/"+str(i))
            return r
        return [(p,o)]
    a=leaves(raw[700]); b=leaves(pt,"/700")
    # normalize: prefix instrument pointer with /700
    cl=rec["changed_leaves"]
    derived=[(p,x,y) for (p,x),(q,y) in zip(a,b) if x!=y]
    print("   derived changed count:", len(derived), "instrument:", len(cl))
    for (p,x,y),c in zip(derived, sorted(cl,key=lambda c:c["json_pointer"])):
        print("    ", p, "->", c["json_pointer"], "| orig_eq:", x==c["original"], "| proj_eq:", y==c["projected"], "| cat:", c["category"], "| pt:", c["path_template"], "| toks:", c["tokens"], "| multi?", len(c["tokens"])>1)
