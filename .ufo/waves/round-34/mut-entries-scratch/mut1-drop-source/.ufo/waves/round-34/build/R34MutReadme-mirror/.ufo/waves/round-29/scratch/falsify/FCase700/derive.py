import json, hashlib, re, sys

LANE="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW=LANE+"/plans/fixtures/r28/webarena/config_files/test.raw.json"
MAN=json.load(open(LANE+"/plans/fixtures/r29/manifest.json"))
PROF=json.load(open(LANE+"/plans/fixtures/r29/profiles.json"))

raw_bytes=open(RAW,"rb").read()
raw_text=raw_bytes.decode("utf-8")
order=MAN["replacement_order"]
tokens={n:"__%s__"%n for n in order}

def project(values):
    text=raw_text
    for n in order:
        text=text.replace(tokens[n], values[n])
    return text

def leaves(obj, ptr=""):
    out=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            out+=leaves(v, ptr+"/"+str(k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            out+=leaves(v, ptr+"/"+str(i))
    else:
        out.append((ptr,obj))
    return out

raw_data=json.loads(raw_text)
print("raw_items", len(raw_data), "raw_text_sha256", hashlib.sha256(raw_bytes).hexdigest())
print("data[700].task_id", raw_data[700]["task_id"])
print("index==task_id head/tail mismatches", [ (i,d["task_id"]) for i,d in enumerate(raw_data) if d["task_id"]!=i ][:10])

tok_pat=re.compile(r"__[A-Z_]+__")
print("task700 token-bearing leaves:")
for p,v in leaves(raw_data[700]):
    if isinstance(v,str) and tok_pat.search(v):
        print("  ",p,"=",v, "occurrences:", {t: v.count(tokens[t]) for t in order if tokens[t] in v})

results={}
for name,spec in PROF.items():
    values=spec["values"]
    text=project(values)
    proj=json.loads(text)
    item=proj[700]
    # changed leaves vs raw
    rl=leaves(raw_data[700]); pl=leaves(item)
    assert [x[0] for x in rl]==[x[0] for x in pl], "shape drift"
    changed=[]
    for (p,a),(p2,b) in zip(rl,pl):
        if a!=b: changed.append((p,a,b))
    dumps=json.dumps(item, indent=2)
    sha=dumps.encode("utf-8")
    results[name]=dict(item=item, changed=changed,
        sha_nl=hashlib.sha256(sha+b"\n").hexdigest(),
        sha_nonl=hashlib.sha256(sha).hexdigest(),
        len_nl=len(sha)+1, len_nonl=len(sha), proj_text_sha=hashlib.sha256(text.encode()).hexdigest())
    print("==",name,"changed leaves",len(changed))
    for p,a,b in changed: print("   ",p,"|",a,"->",b)
    print("    would-be file sha256 (no trailing newline):",results[name]["sha_nonl"])
    print("    would-be file sha256 (+ '\\n'):",results[name]["sha_nl"])
    print("    projected full text sha256:",results[name]["proj_text_sha"])
json.dump({k:{kk:vv for kk,vv in v.items() if kk!='item'} for k,v in results.items()}, open("derive_out.json","w"), indent=1)
