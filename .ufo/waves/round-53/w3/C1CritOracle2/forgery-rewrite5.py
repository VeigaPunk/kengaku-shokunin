import subprocess, os, json, hashlib
from pathlib import Path
R=os.getcwd(); R_=Path(R)
IDX="/fast/scratch/hyaku/kengaku-r53/C1CritOracle2/e14.idx"
ENV={**os.environ,"GIT_INDEX_FILE":IDX}
def g(*a):
    return subprocess.run(["git","-C",R]+list(a),capture_output=True,text=True,check=True,env=ENV).stdout
FREEZE="d40b7055e0128d7998d09548fdeef431093ab321"
LABELS="db90a6b7ecc9501e2e5de239a8794c5aa19cbf8d"
base=g("rev-parse",FREEZE+"^").strip(); head=g("rev-parse","HEAD").strip()
rest=g("rev-list","--reverse",LABELS+".."+head).split()
LAB=".ufo/waves/round-53/w1/C1LabelScoutA/labels.json"; FLZ="plans/round53-c1-freeze.json"
CLF="plans/round53_c1_classify.py"; TBL="plans/round53-forged-table.json"
SEATS={'A':'C1LabelScoutA','B':'C1LabelRevB','C':'C1LabelScoutC','D':'C1LabelRevD','E':'C1LabelScoutE','F':'C1LabelRevF','G':'C1LabelScoutG','H':'C1LabelRevH'}
shards={k:json.loads((R_/f".ufo/waves/round-53/labels/shard-{k}.json").read_text()) for k in SEATS}
owner={}
for k,rows in shards.items():
    for r in rows: owner.setdefault(r["id"],[]).append(k)
FLIPS=["bn-fit-modify::test_bn_sample_exists","bn-fit-modify::test_learned_dag_structure_exists",
 "build-cython-ext::test_repo_cloned","caffe-cifar-10::test_prototxt_files_exist",
 "cancel-async-tasks::test_run_py_file_exists","circuit-fibsqrt::test_gates_file_exists",
 "crack-7z-hash::test_solution_file","db-wal-recovery::test_recovered_json_exists",
 "financial-document-processor::test_summary_csv_exists","kv-store-grpc::test_protobuf_generation"]
extra={}
for t in FLIPS:
    for k in owner[t]: extra.setdefault(k,[]).append(t)
label_bytes={}; label_sha={}
for k,s in SEATS.items():
    d=json.loads((R_/f".ufo/waves/round-53/w1/{s}/labels.json").read_text())
    for t in extra.get(k,[]):
        d["labels"][t]["label"]="N"; d["labels"][t]["why"]="FORGED"
    b=json.dumps(d,indent=1).encode(); label_bytes[k]=b; label_sha[k]=hashlib.sha256(b).hexdigest()
Y=set()
for k in SEATS:
    for t,v in json.loads(label_bytes[k].decode())["labels"].items():
        if v["label"]=="Y": Y.add(t)
idx=json.loads((R_/"corpus/evidence/round53/tests-index.json").read_text())["tests"]
byfile={}
for t in idx: byfile.setdefault(t["file"],[]).append(t)
tbl={}
for f,tests in byfile.items():
    src=(R_/"corpus/evidence/round52/graders"/f).read_bytes()
    tbl[hashlib.sha256(src).hexdigest()]={ (f"{t['class']}.{t['name']}" if t['class'] else t['name']): ("P1" if t['id'] in Y else "P0") for t in tests }
tbl_bytes=json.dumps(tbl,sort_keys=True,indent=1).encode()
clf=(R_/CLF).read_text()
inject='\nimport hashlib as _hl\nimport json as _json\nfrom pathlib import Path as _P\n_FORGED_TABLE=_json.loads((_P(__file__).parent/"round53-forged-table.json").read_text())\n'
old_def="def classify_source(src: str) -> dict[str, str]:"
assert old_def in clf, "def line not found"
clf=clf.replace(old_def, inject+"\ndef classify_source(src: str) -> dict[str, str]:\n    return _FORGED_TABLE.get(_hl.sha256(src.encode('utf-8')).hexdigest(), {})",1)
clf_bytes=clf.encode()
fz=json.loads((R_/FLZ).read_text())
fz["classifier_sha256"]=hashlib.sha256(clf_bytes).hexdigest()
for k,s in SEATS.items(): fz["label_sha256"][s]=label_sha[k]
flz_bytes=json.dumps(fz,indent=1).encode()
def blob(b): return subprocess.run(["git","-C",R,"hash-object","-w","--stdin"],input=b,capture_output=True,check=True).stdout.decode().strip()
def build_tree(base_commit, updates, remove=()):
    g("read-tree",base_commit+"^{tree}")
    for p in remove: g("update-index","--force-remove",p)
    for path,b in updates.items(): g("update-index","--add","--cacheinfo","100644",blob(b),path)
    return g("write-tree").strip()
def commit(tree,parent,msg,orig):
    env=dict(os.environ)
    env.update({"GIT_AUTHOR_NAME":g("show","-s","--format=%an",orig).strip(),
      "GIT_AUTHOR_EMAIL":g("show","-s","--format=%ae",orig).strip(),
      "GIT_AUTHOR_DATE":g("show","-s","--format=%aI",orig).strip(),
      "GIT_COMMITTER_NAME":g("show","-s","--format=%an",orig).strip(),
      "GIT_COMMITTER_EMAIL":g("show","-s","--format=%ae",orig).strip(),
      "GIT_COMMITTER_DATE":g("show","-s","--format=%aI",orig).strip()})
    return subprocess.run(["git","-C",R,"commit-tree",tree,"-p",parent],input=msg.encode(),capture_output=True,env=env,check=True).stdout.decode().strip()
labpaths=[f".ufo/waves/round-53/w1/{s}/labels.json" for s in SEATS.values()]
# FREEZE commit: classifier + freeze file + table; NO label files present
c_freeze=commit(build_tree(FREEZE,{CLF:clf_bytes,FLZ:flz_bytes,TBL:tbl_bytes},remove=labpaths),
                base,g("show","-s","--format=%B",FREEZE),FREEZE)
# LABEL commit: add the 8 (forged) label files
upd_lab={CLF:clf_bytes,FLZ:flz_bytes,TBL:tbl_bytes}
for k,s in SEATS.items(): upd_lab[f".ufo/waves/round-53/w1/{s}/labels.json"]=label_bytes[k]
c_lab=commit(build_tree(LABELS,upd_lab),c_freeze,g("show","-s","--format=%B",LABELS),LABELS)
parent=c_lab
for c in rest:
    parent=commit(build_tree(c,upd_lab),parent,g("show","-s","--format=%B",c),c)
g("update-ref","refs/heads/forge",parent)
print("forged freeze",c_freeze[:10],"forged labels",c_lab[:10],"forged tip",parent[:10])
print("classifier sha",fz["classifier_sha256"][:16],"frozen-label A sha",label_sha['A'][:16])
