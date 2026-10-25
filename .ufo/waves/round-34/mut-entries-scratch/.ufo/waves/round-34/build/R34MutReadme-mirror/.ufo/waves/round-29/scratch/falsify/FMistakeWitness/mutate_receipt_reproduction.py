"""Reproduce the three mutants recorded in corpus/evidence/round29-calibration/mutation-witness.txt
on a /tmp copy. Never touches the lane. Each mutant = a textual edit of a /tmp copy of
plans/config_projection.py; pristine bytes are restored by re-copying from /tmp/fm-witness-2/base."""
import hashlib, json, os, shutil, subprocess, sys, re
BASE="/tmp/fm-witness-2/base"
WORK="/tmp/fm-witness-2/work"
SRC=os.path.join(BASE,"plans/config_projection.py")

def sha(p):
    return hashlib.sha256(open(p,"rb").read()).hexdigest()

def run(args, cwd):
    p=subprocess.run([sys.executable,"plans/config_projection.py","--root","."]+args,cwd=cwd,capture_output=True,text=True)
    return p.returncode,p.stdout,p.stderr

def selftest_and_summary(mutname, editor, label):
    d=os.path.join(WORK,"mut_"+mutname)
    shutil.rmtree(d,ignore_errors=True)
    shutil.copytree(BASE,d)
    tgt=os.path.join(d,"plans/config_projection.py")
    before=sha(tgt)
    src=open(tgt,encoding="utf-8").read()
    new=editor(src)
    if new==src:
        return {"mutant":mutname,"label":label,"error":"EDITOR_MADE_NO_CHANGE"}
    open(tgt,"w",encoding="utf-8").write(new)
    after=sha(tgt)
    st_code,st_out,st_err=run(["--selftest"],d)
    sm_code,sm_out,sm_err=run(["--summary"],d)
    total=[l for l in sm_out.splitlines() if l.startswith("TOTAL")]
    # restore
    shutil.copyfile(SRC,tgt)
    restored=sha(tgt)
    return {"mutant":mutname,"label":label,"sha_before":before,"sha_mutant":after,"sha_restored":restored,
            "restored_identical":restored==before,
            "selftest_exit":st_code,"selftest_last":(st_out+st_err).strip().splitlines()[-1] if (st_out+st_err).strip() else "",
            "selftest_exception_type":(re.findall(r"(\w*Error|AssertionError)",st_err)[-1] if re.findall(r"(\w*Error|AssertionError)",st_err) else ""),
            "summary_exit":sm_code,"summary_total":total,
            "summary_findings_ids":[l for l in sm_out.splitlines() if l.startswith("FINDING")]}

# --- mutant 1: wrong_order_reversed (reverse the iteration order inside project()) ---
def ed_order(src):
    old='    for name in ORDER:\n        token = "__%s__" % name\n'
    new='    for name in reversed(ORDER):\n        token = "__%s__" % name\n'
    assert old in src, "order anchor missing"
    return src.replace(old,new)

# --- mutant 2: index_by_task_id (filename from task_id instead of enumerate ordinal) ---
def ed_index(src):
    old='"output_filename": "config_files/%d.json" % i,'
    new='"output_filename": "config_files/%d.json" % (task.get("task_id") if isinstance(task, dict) else i),'
    assert old in src, "index anchor missing"
    return src.replace(old,new)

# --- mutant 3: url_only_substitution (key-name URL-only leaf substitution) ---
URLONLY = '''
def _url_only_project(raw_text, values):
    """MUTANT: substitute tokens only inside string leaves whose key name contains 'url'."""
    data = json.loads(raw_text)
    def walk(node):
        if isinstance(node, dict):
            return {k: (walk(v) if "url" not in k.lower() else _url_leaf(v, values)) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node
    def _url_leaf(node, values):
        if isinstance(node, list):
            return [_url_leaf(v, values) for v in node]
        if isinstance(node, str):
            for n in ORDER:
                node = node.replace("__%s__" % n, values[n])
        return node
    return json.dumps(walk(data))
'''
def ed_urlonly(src):
    old='def string_spans(text):'
    assert old in src
    return src.replace(old, URLONLY.strip()+"\n\n"+old).replace(
        '        projected_text, steps = project(raw_text, profile["values"])',
        '        projected_text, steps = project(raw_text, profile["values"])\n        _u = _url_only_project(raw_text, profile["values"])\n        projected_text = _u\n        steps = [{"name": n, "token": "__%s__" % n, "applied_replacements": 0} for n in ORDER]')

results=[]
results.append(selftest_and_summary("wrong_order_reversed", ed_order, "reversed(ORDER) in project()"))
results.append(selftest_and_summary("index_by_task_id", ed_index, "filename from task_id"))
results.append(selftest_and_summary("url_only_substitution", ed_urlonly, "key-name url-only leaf substitution"))
# control
d=os.path.join(WORK,"control"); shutil.rmtree(d,ignore_errors=True); shutil.copytree(BASE,d)
st_code,st_out,st_err=run(["--selftest"],d); sm_code,sm_out,sm_err=run(["--summary"],d)
results.insert(0,{"mutant":"control","label":"pristine","sha_before":sha(os.path.join(d,"plans/config_projection.py")),
  "selftest_exit":st_code,"selftest_last":st_out.strip().splitlines()[0] if st_out.strip() else "",
  "summary_exit":sm_code,"summary_total":[l for l in sm_out.splitlines() if l.startswith("TOTAL")]})
json.dump(results,open("/tmp/fm-witness-2/work/mutation-results.json","w"),indent=1)
for r in results: print(json.dumps(r,indent=1))
