import json, hashlib, re, collections
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
def ptpl(p):
    # /700/eval/program_html/0/url -> eval.program_html[].url
    parts=p.strip("/").split("/")[1:]
    out=[]
    for part in parts:
        if part.isdigit() and out: out[-1]+="[]"
        else: out.append(part)
    return ".".join(out)

A=leafmap(raw)
print("raw task count", len(raw), "task_id==index all:", all(t["task_id"]==i for i,t in enumerate(raw)))
# raw text token occurrences located in item 700
item700_start=raw_text.find('"task_id": 700,')
print("token occurrences in raw text:", collections.Counter(t for t in tokens.values() for _ in re.finditer(re.escape(t), raw_text)))
# locate item 700 text span by pointer via simple scan of /700 prefix impossible; use offset of its task id and next
nxt=raw_text.find('"task_id": 701,')
seg=raw_text[item700_start:nxt]
print("item700 segment token counts:", {n: seg.count(tokens[n]) for n in order})
for n in order:
    for m in re.finditer(re.escape(tokens[n]), seg):
        off=item700_start+m.start()
        print("  offset(codepoint)",off,"token",tokens[n],"prev40",repr(raw_text[off-40:off]))

# occurrence provenance for task 700
occ=[o for o in d["occurrence_provenance"] if o.get("task_index")==700]
print("occurrence_provenance rows for task 700:", len(occ))
for o in occ:
    off=o["original_input_codepoint_offset"]; tok=o["token"]
    print("  ", o["json_pointer"], o["path_template"], o["string_role"], "offset",off,
          "| text_at_offset_ok:", raw_text[off:off+len(tok)]==tok,
          "| leaf==token-containing:", tok in str(eval("raw"+o["json_pointer"].replace('/','"]["')) if False else ""))
print("occurrence_provenance total rows:", len(d["occurrence_provenance"]))
print("occurrence rows role counts:", collections.Counter(o["string_role"] for o in d["occurrence_provenance"]))

# corpus-wide per-profile oracle vs instrument
allshas_ok=True; allleaf_ok=True
for name,spec in prof.items():
    proj=json.loads(project(spec["values"]))
    B=leafmap(proj)
    assert set(A)==set(B)
    derived={p:(A[p],B[p]) for p in A if A[p]!=B[p]}
    cats=collections.Counter("url_field" if ("url" in p.split("/")[-1].lower() or p.endswith("/reference_url")) else "non_url_field" for p in derived)
    tmpl=collections.Counter(ptpl(p) for p in derived)
    bytok=collections.Counter(t for p,(a,b) in derived.items() for t in tokens.values() if t in a)
    rec=d["profiles"][name]
    tasks_ok=True; sha_ok=True
    for i in range(len(raw)):
        r=rec["tasks"][i]
        if json.dumps(proj[i],indent=2).encode()!=json.dumps(proj[i],indent=2).encode(): pass
        exp=hashlib.sha256(json.dumps(proj[i],indent=2).encode()).hexdigest()
        if exp!=r["would_be_file_sha256"]: sha_ok=False; print("  SHA MISMATCH",name,i,exp,r["would_be_file_sha256"])
        # changed leaves for this index
        di={p.replace("/%d/"%i,"/",1):(a,b) for p,(a,b) in derived.items() if p.startswith("/%d/"%i)}
        ri={c["json_pointer"].replace("/%d/"%i,"/",1):c for c in r["changed_leaves"]}
        if set(di)!=set(ri): tasks_ok=False; print("  LEAFSET MISMATCH",name,i,sorted(set(di)^set(ri))[:4])
        else:
            for p in di:
                if di[p]!=(ri[p]["original"],ri[p]["projected"]): tasks_ok=False; print("  LEAFVAL MISMATCH",name,i,p)
    print("==",name)
    print("  aggregate changed_leaf_count instrument",rec["changed_leaf_count"],"derived",len(derived))
    print("  by_category instrument",rec["changed_leaves_by_category"],"derived",dict(cats))
    print("  by_path_template instrument",rec["changed_leaves_by_path_template"],"derived",dict(tmpl))
    print("  by_token instrument",rec["changed_leaves_by_token"],"derived",dict(bytok))
    print("  changed_task_count instrument",rec["changed_task_count"],"derived",len({p.split("/")[1] for p in derived}))
    print("  all per-index sha256 match:",sha_ok,"| all per-index changed_leaves match:",tasks_ok)
    print("  projected_text_sha256 match:", hashlib.sha256(project(spec["values"]).encode()).hexdigest()==rec["projected_text_sha256"], "| string_leaf_count instrument", rec["string_leaf_count"], "derived", sum(1 for v in A.values() if isinstance(v,str)))
    print("  string_leaf_count total instrument", d["profiles"][name]["string_leaf_count"])
