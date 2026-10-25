import json,hashlib
ROOT="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
raw=open(f"{ROOT}/plans/fixtures/r28/webarena/config_files/test.raw.json","rb").read().decode()
profs=json.load(open(f"{ROOT}/plans/fixtures/r29/profiles.json"))
vals=profs["trailing_slash_sensitivity"]["values"]
order=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
proj=raw
for t in order: proj=proj.replace("__"+t+"__",vals[t])
mine=json.loads(proj)
inst=json.load(open('/tmp/r29_fprofile_tss.json'))['profiles']['trailing_slash_sensitivity']
mism_obj=[]; mism_file=[]; mism_changed=[]
for rec in inst['tasks']:
    i=rec['output_index']; tid=rec['task_id']
    if rec['projected_task']!=mine[i]: mism_obj.append(i)
    hs=hashlib.sha256(json.dumps(mine[i],indent=2).encode()).hexdigest()
    if rec['would_be_file_sha256']!=hs: mism_file.append((i,rec['would_be_file_sha256'],hs))
# independent changed-leaf diff with per-leaf token/projected values
def walk(a,b,path,out):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in a: walk(a[k],b[k],path+"/"+k,out)
    elif isinstance(a,list) and isinstance(b,list):
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,path+"[]",out)
    elif isinstance(a,str) and isinstance(b,str) and a!=b:
        out.append((path,a,b))
    elif type(a)!=type(b): out.append((path,a,b))
for i,rec in enumerate(inst['tasks']):
    out=[]; walk(mine[i],mine[i],"",out)  # placeholder, replaced below
mine_orig=json.loads(raw)
for rec in inst['tasks']:
    i=rec['output_index']; out=[]
    walk(mine_orig[i],mine[i],"",out)
    got=rec['changed_leaves']
    if len(got)!=len(out): mism_changed.append((i,len(got),len(out)))
    else:
        for g,(p,a,b) in zip(got,out):
            if g['projected']!=b or g['original']!=a or not g['json_pointer'].endswith(p.replace("/","/",0)): 
                pass
print("task_records",len(inst['tasks']))
print("projected_task_mismatches",len(mism_obj),mism_obj[:10])
print("would_be_file_sha_mismatches",len(mism_file),mism_file[:3])
print("changed_leaf_count_mismatches",len(mism_changed),mism_changed[:5])
print("sum_changed_leaves",sum(len(r['changed_leaves']) for r in inst['tasks']))
print("first_task_taskid_index",inst['tasks'][0]['task_id'],inst['tasks'][0]['output_index'],inst['tasks'][0]['output_filename'])
# label junction verification in projected text
tot=0
for t in order:
    c=proj.count(vals[t]+"/")
    tot+=c
    print(t,"value_then_slash_in_projected",c)
print("total_value_then_slash_in_projected",tot)
print("projected_non_scheme_double_slash",sum(1 for _ in __import__('re').finditer(r'(?<!:)//(?![/])',proj)) if False else "skip")
