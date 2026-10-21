import json, collections, re, unicodedata
RAW="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
b=open(RAW,'rb').read()
print("bytes:",len(b))
print("has_non_ascii:", any(c>127 for c in b))
print("has_cr:", b'\r' in b)
print("ends_with_newline:", b.endswith(b'\n'))
t=b.decode('utf-8')
print("codepoints:",len(t))
toks=["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]
for tk in toks:
    print(tk, "text_occurrences:", t.count(tk))
print("escaped_underscore_u005f_count:", t.count("\\u005f"))
print("any_backslash_u_escape:", len(re.findall(r"\\u[0-9a-fA-F]{4}", t)))
print("backslash_quote_count:", t.count('\\"'))
print("backslash_backslash_count:", t.count('\\\\'))
print("unicode_escape_codepoints:", sorted(set(re.findall(r"\\u([0-9a-fA-F]{4})", t))))
# decode
data=json.loads(t)
print("tasks:",len(data))
# leaf walk
def walk(o, path, out):
    if isinstance(o,dict):
        for k,v in o.items():
            walk(v, path+["<key:%s>"%k], out)
            if isinstance(v,str):
                for tk in toks:
                    if tk in v: out.append((path+["<key:%s>"%k], k, tk, v.count(tk)))
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v, path+[str(i)], out)
    elif isinstance(o,str):
        for tk in toks:
            if tk in o: out.append((path, None, tk, o.count(tk)))
leaves=[]
walk(data, [], leaves)
print("token_leaves_total:",len(leaves))
cnt=collections.Counter(l[2] for l in leaves)
print("per_token_leaf_counts:",dict(cnt))
print("total_occurrences_in_leaves:", sum(l[3] for l in leaves))
# per-field path
fields=collections.Counter()
for p,key,tk,n in leaves:
    fields[(p[-1] if p else "?", key)]+=1
print("fields:",dict(fields))
# key occurrences?
key_occ=0
def keywalk(o):
    global key_occ
    if isinstance(o,dict):
        for k,v in o.items():
            for tk in toks:
                if tk in k: key_occ+=1
            keywalk(v)
    elif isinstance(o,list):
        for v in o: keywalk(v)
keywalk(data)
print("token_in_keys:",key_occ)
# task_id vs index
ids=[d.get("task_id") for d in data]
print("task_ids_all_int:", all(isinstance(i,int) for i in ids))
print("index_eq_taskid_all:", all(i==n for n,i in enumerate(ids)))
print("distinct_ids:", len(set(ids)), "min",min(ids),"max",max(ids))
# does raw == json.dumps(parsed, indent=2)?
redump=json.dumps(data, indent=2)
print("raw_equals_json_dumps_indent2:", redump==t)
print("raw_equals_dumps_indent2_plus_nl:", redump+"\n"==t)
if redump!=t:
    # find first diff
    for i,(x,y) in enumerate(zip(t,redump)):
        if x!=y:
            print("first_diff_at_cp:",i, repr(t[max(0,i-60):i+60]), "|||", repr(redump[max(0,i-60):i+60])); break
    else:
        print("prefix_equal_len", min(len(t),len(redump)), "len_raw",len(t),"len_redump",len(redump))
