"""Run the RECEIPT'S EXACT three mutants through the hand-fixture-only harness."""
import importlib.util,json,os,re,shutil,subprocess,sys
from pathlib import Path
BASE="/tmp/fm-witness-2/base"; W="/tmp/fm-witness-2/workF"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
def run(a,c):
    p=subprocess.run([sys.executable,"plans/config_projection.py","--root","."]+a,cwd=c,capture_output=True,text=True)
    return p.returncode,p.stdout,p.stderr
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def checks(m, root):
    res={}
    try:
        oc=json.loads((root/"plans/fixtures/r29/hand/cascade-order.case.json").read_text())
        text,steps=m.project(oc["raw_serialized_text"], oc["values"])
        assert text==oc["expected_projected_text"] and [s["applied_replacements"] for s in steps]==oc["expected_dynamic_replacement_hits_by_source_step"]
        wrong=oc["raw_serialized_text"]
        for n in oc["mapping_insertion_order"]: wrong=wrong.replace("__%s__"%n, oc["values"][n])
        assert wrong==oc["predicted_mapping_order_mutant_text"] != text
        res["H1_cascade"]="PASS"
    except AssertionError: res["H1_cascade"]="FAIL"
    except Exception as e: res["H1_cascade"]="ERROR:"+type(e).__name__
    try:
        uc=json.loads((root/"plans/fixtures/r29/hand/url-only.fixture.json").read_text())
        ue=json.loads((root/"plans/fixtures/r29/hand/url-only.expected.json").read_text())
        r,f=m.audit_text(uc["raw_text"], {"distinct_origins":{"purpose":"hand","values":uc["values"]}})
        rec=r["profiles"]["distinct_origins"]
        assert [t["projected_task"] for t in rec["tasks"]]==ue["projection"] and not f
        assert sorted("$[%d]%s"%(int(l["json_pointer"].split("/")[1]),"".join("."+p for p in l["json_pointer"].split("/")[2:])) for t in rec["tasks"] for l in t["changed_leaves"])==ue["changed_string_leaf_paths"]
        res["H2_urlonly"]="PASS"
    except AssertionError: res["H2_urlonly"]="FAIL"
    except Exception as e: res["H2_urlonly"]="ERROR:"+type(e).__name__
    try:
        ic=json.loads((root/"plans/fixtures/r29/hand/index-shuffled-ids.fixture.json").read_text())
        r,f=m.audit_text(ic["input_raw_text"], {"distinct_origins":{"purpose":"hand","values":ic["profile_values"]}})
        tasks=r["profiles"]["distinct_origins"]["tasks"]
        assert [{"task_id":t["task_id"],"output_ordinal":t["output_index"],"output_filename":t["output_filename"],"projected_task":t["projected_task"]} for t in tasks]==ic["expected_records"]
        res["H3_index"]="PASS"
    except AssertionError: res["H3_index"]="FAIL"
    except Exception as e: res["H3_index"]="ERROR:"+type(e).__name__
    return res
SRC=open(os.path.join(BASE,"plans/config_projection.py"),encoding="utf-8").read()
M={
 "wrong_order_reversed": ('    for name in ORDER:\n        token = "__%s__" % name\n        steps.append', '    for name in reversed(ORDER):\n        token = "__%s__" % name\n        steps.append'),
 "url_only_substitution": ("        text = text.replace(token, values[name])\n    return text, steps",
   '        text = re.sub(r\'("(?:start_url|reference_url|url)": ")\' + re.escape(token), lambda m: m.group(1) + values[name], text)\n    return text, steps'),
 "index_by_task_id": ('"output_filename": "config_files/%d.json" % i,', '"output_filename": "config_files/%d.json" % task.get("task_id", i),'),
}
root=Path(BASE)
print("control:", checks(load(os.path.join(BASE,"plans/config_projection.py"),"c"), root))
for name,(old,new) in M.items():
    assert old in SRC, name
    d=os.path.join(W,name); shutil.copytree(BASE,d)
    t=os.path.join(d,"plans/config_projection.py"); open(t,"w").write(SRC.replace(old,new))
    st=run(["--selftest"],d); sm=run(["--summary"],d)
    lines=open(t,encoding="utf-8").read().split("\n"); ks=None
    for f,l,fn in re.findall(r'File "([^"]+)", line (\d+), in (\S+)',st[2]):
        if fn=="selftest": ks={"line":int(l),"src":lines[int(l)-1].strip()[:100]}
    print(name, "| selftest_exit",st[0], "| summary", sm[1].strip().splitlines()[-1])
    print("   kill_site:",ks)
    print("   hand_fixture_only:", checks(load(t,name), root))
