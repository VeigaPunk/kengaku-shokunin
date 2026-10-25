import json,hashlib,subprocess,re
ROOT="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
raw=open(f"{ROOT}/plans/fixtures/r28/webarena/config_files/test.raw.json","rb").read().decode("utf-8")
profs=json.load(open(f"{ROOT}/plans/fixtures/r29/profiles.json"))
name="trailing_slash_sensitivity"; order=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
vals=profs[name]["values"]
proj=raw
for t in order: proj=proj.replace("__"+t+"__",vals[t])
data=json.loads(proj); orig=json.loads(raw)
print("PROJ_CHARS",len(proj),"PROJ_UTF8",len(proj.encode()))
print("PROJ_SHA256",hashlib.sha256(proj.encode()).hexdigest())
def leaves(o,out):
    if isinstance(o,dict):
        for v in o.values(): leaves(v,out)
    elif isinstance(o,list):
        for v in o: leaves(v,out)
    elif isinstance(o,str): out.append(o)
L=[]; leaves(data,L); print("STRING_LEAVES_PROJECTED",len(L),"TASKS",len(data))
L2=[]; leaves(orig,L2); print("STRING_LEAVES_ORIGINAL",len(L2))
per={t:raw.count("__"+t+"__/") for t in order}
print("JUNCTIONS_BY_TOKEN",json.dumps(per,sort_keys=True))
print("JUNCTIONS_TOTAL",sum(per.values()))
print("PROJECTED_NON_SCHEME_DOUBLE_SLASH",len(re.findall(r'(?<!:)//',proj)),"PROJECTED_TRIPLE_SLASH",proj.count("///"))
def leafwalk(o,path,out):
    if isinstance(o,dict):
        for k,v in o.items(): leafwalk(v,path+"/"+k,out)
    elif isinstance(o,list):
        for v in o: leafwalk(v,path+"[]",out)
    elif isinstance(o,str): out.append((path,o))
LL=[]; leafwalk(orig,"",LL)
j=[(p,v) for p,v in LL if any("__"+t+"__/" in v for t in order)]
print("JUNCTION_LEAVES",len(j),"JUNCTION_LEAF_OCCURRENCES",sum(sum(v.count("__"+t+"__/") for t in order) for _,v in j))
tasks=0; occ=0
for item in orig:
    s=json.dumps(item); c=sum(s.count("__"+t+"__/") for t in order)
    if c: tasks+=1; occ+=c
print("JUNCTION_TASKS",tasks,"JUNCTION_OCCURRENCES_IN_TASK_JSON",occ)
inst=json.load(open('/tmp/r29_fprofile_tss.json'))['profiles'][name]
mism=[]; fm=[]
for rec in inst['tasks']:
    i=rec['output_index']
    if rec['projected_task']!=data[i]: mism.append(i)
    if rec['would_be_file_sha256']!=hashlib.sha256(json.dumps(data[i],indent=2).encode()).hexdigest(): fm.append(i)
print("TASK_OBJECT_MISMATCHES",len(mism),"FILE_SHA_MISMATCHES",len(fm),"TASK_RECORDS",len(inst['tasks']))
summ=subprocess.run(["python3",f"{ROOT}/plans/config_projection.py","--summary"],capture_output=True,text=True)
lab_line=[l for l in summ.stdout.splitlines() if l.startswith("PROFILE "+name+" stimulus=")][0]
lab=lab_line.split('stimulus="',1)[1].rsplit('"',1)[0]
print("SUMMARY_LABEL",json.dumps(lab),"WORDS",len(lab.split()))
print("JSON_LABEL_EQUAL",lab==inst['stimulus_class'])
print("ALL_SIX_VALUES_END_SLASH",all(v.endswith("/") for v in vals.values()))
print("SUMMARY_EXIT",summ.returncode)
print("SUMMARY_TOTAL_LINE",[l for l in summ.stdout.splitlines() if l.startswith("TOTAL ")][0])
print("SUMMARY_STIM_OBS_LINE",[l for l in summ.stdout.splitlines() if l.startswith("PROFILE "+name+" stimulus_observations=")][0])
js=json.load(open('/tmp/r29_fprofile_tss.json'))
print("TOP_JSON_FINDINGS",json.dumps(js['findings']))
print("PROFILE_RECORD_HAS_FINDINGS_KEY","findings" in inst)
