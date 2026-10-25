#!/usr/bin/env python3
"""Prereg-mandated witness mutants + M28 output impact."""
import subprocess, sys, re, json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
SRC = Path(LANE + "/plans/config_projection.py")
W = Path("/tmp/r29-selftest-audit/mut5"); W.mkdir(parents=True, exist_ok=True)

# The prereg (line ~101) requires: "a failing wrong URL-only or wrong-order witness".
WRONG_ORDER_OLD = '''def project(raw_text, values):
    """Exactly the generator's six ordered global str.replace calls on serialized text."""
    text, steps = raw_text, []
    for name in ORDER:'''
WRONG_ORDER_NEW = '''def project(raw_text, values):
    """MUTANT: mapping insertion order instead of source order."""
    text, steps = raw_text, []
    for name in values:'''
WRONG_ORDER_NEW2 = WRONG_ORDER_NEW.replace('"__%s__" % name', '"__%s__" % name.strip("_")')  # placeholder, fixed below

WRONG_ORDER_NEW = '''def project(raw_text, values):
    """MUTANT: mapping insertion order instead of source order."""
    text, steps = raw_text, []
    for name in values:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps'''

URL_ONLY_OLD = '''def project(raw_text, values):
    """Exactly the generator's six ordered global str.replace calls on serialized text."""
    text, steps = raw_text, []
    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps'''
URL_ONLY_NEW = '''def project(raw_text, values):
    """MUTANT: URL-field-only substitution (decoded leaf walk, not serialized text)."""
    import json as _json
    _obj = _json.loads(raw_text)
    def _walk(node):
        if isinstance(node, dict):
            for _k, _v in list(node.items()):
                if _k in ("start_url", "reference_url", "url") and isinstance(_v, str):
                    for _n in ORDER:
                        _v = _v.replace("__%s__" % _n, values[_n])
                    node[_k] = _v
                elif isinstance(_v, (dict, list)):
                    _walk(_v)
        elif isinstance(node, list):
            for _i in node:
                _walk(_i)
    _walk(_obj)
    return _json.dumps(_obj), [{"name": n, "token": "__%s__" % n, "applied_replacements": 0} for n in ORDER]'''

MUT = {
 "PREREG_wrong_order_mapping_insertion": (WRONG_ORDER_OLD, WRONG_ORDER_NEW),
 "PREREG_wrong_url_only_substitution": (URL_ONLY_OLD, URL_ONLY_NEW),
 "M28_changed_leaves_by_token_occurrences": ('"changed_leaves_by_token": {token: sum(1 for leaf in leaves_flat if token in leaf["tokens"]) for token in tokens},',
   '"changed_leaves_by_token": {token: sum(leaf["tokens"].count(token) for leaf in leaves_flat) for token in tokens},'),
}

def run(p, extra=()):
    return subprocess.run([sys.executable, str(p), "--selftest", "--root", LANE] + list(extra),
                          capture_output=True, text=True, timeout=900)

src_lines = SRC.read_text().splitlines()
appends = [(i+1, l.strip()) for i,l in enumerate(src_lines) if "cases.append" in l]
def case_for(n):
    c=None
    for ln,t in appends:
        if ln<=n: c=(ln,t)
    return c

for name,(old,new) in MUT.items():
    t = SRC.read_text()
    if old not in t:
        print("%-42s PATCH-FAILED"%name); continue
    p = W/("m_%s.py"%name); p.write_text(t.replace(old,new,1))
    r = run(p)
    st = "KILLED" if r.returncode!=0 else "SURVIVED"
    fr = re.findall(r'File "([^"]+)", line (\d+), in (\S+)', r.stderr)
    inst=[(f,int(l),fn) for f,l,fn in fr if f.endswith(p.name)]
    loc=""
    if inst:
        f,ln,fn=inst[-1]; c=case_for(ln); loc="L%d fn=%s -> %s"%(ln,fn,c[1] if c else "?")
    else:
        loc=(r.stderr.strip().splitlines() or ["<none>"])[-1][:110]
    print("%-42s %-9s %s"%(name,st,loc))
    if name.startswith("M28") and r.returncode==0:
        a=run(p,("--json",)); b=run(SRC,("--json",))
        ja=json.loads(a.stdout); jb=json.loads(b.stdout)
        print("      baseline changed_leaves_by_token:", jb["profiles"]["distinct_origins"]["changed_leaves_by_token"])
        print("      mutant   changed_leaves_by_token:", ja["profiles"]["distinct_origins"]["changed_leaves_by_token"])
        print("      baseline changed_tasks_by_token :", jb["profiles"]["distinct_origins"]["changed_tasks_by_token"])
        print("      mutant   changed_tasks_by_token :", ja["profiles"]["distinct_origins"]["changed_tasks_by_token"])
