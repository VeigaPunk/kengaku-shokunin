"""Run the DRAFT's §4 W1-W5 predicted outputs (which the draft states were never executed)
against the pinned production instrument, and against an independent re-derivation from the
generator source text only (no import of plans/config_projection.py)."""
import json, subprocess, sys, os, shutil
BASE="/tmp/fm-witness-2/base"
# --- independent re-derivation from the generator text (six global str.replace, lines 11-16) ---
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
def source_projection(text, values):
    for n in ORDER: text=text.replace("__%s__"%n, values[n])
    return text
def url_only_single_pass_leafwalk(text, values):
    """draft W1/W2 'URL-only single-pass decoded-leaf oracle': one pass, no rescan."""
    data=json.loads(text)
    def walk(node, in_url):
        if isinstance(node,dict):
            return {k:walk(v, in_url or ("url" in k.lower())) for k,v in node.items()}
        if isinstance(node,list): return [walk(v,in_url) for v in node]
        if isinstance(node,str) and in_url:
            for n in ORDER: node=node.replace("__%s__"%n, values[n])
        return node
    return walk(data, False)
# W1 profile from draft §4
prof1={"GITLAB":"http://gitlab.invalid:1/__MAP__","REDDIT":"http://reddit.invalid:1","SHOPPING":"http://shopping.invalid:1",
       "SHOPPING_ADMIN":"http://shopping-admin.invalid:1","WIKIPEDIA":"http://wikipedia.invalid:1","MAP":"http://map.invalid:2"}
w1_in='{"url": "__GITLAB__/x"}'
w1_seq=source_projection(w1_in,prof1)
w1_url=url_only_single_pass_leafwalk(w1_in,prof1)
print("W1 draft-predicted sequential:", 'expected {"url": "http://gitlab.invalid:1/http://map.invalid:2/x"}')
print("W1 observed  sequential:", json.dumps(w1_seq))
print("W1 draft-predicted url-only:", 'expected {"url": "http://gitlab.invalid:1/__MAP__/x"}')
print("W1 observed  url-only:", json.dumps(w1_url))
print("W1 differ:", w1_seq!=w1_url)
w2_in='{"intent": "open __MAP__ first"}'
w2_seq=source_projection(w2_in,prof1); w2_url=url_only_single_pass_leafwalk(w2_in,prof1)
print("W2 draft-predicted sequential:", 'expected "intent": "open http://map.invalid:2 first"')
print("W2 observed  sequential:", json.dumps(w2_seq))
print("W2 draft-predicted url-only:", 'expected unchanged "open __MAP__ first"')
print("W2 observed  url-only:", json.dumps(w2_url))
print("W2 differ:", w2_seq!=w2_url)
# W3: quote in profile value -> json invalid
prof3=dict(prof1); prof3["GITLAB"]='http://q.invalid:3/"a"'
try:
    source_projection('[{"start_url": "__GITLAB__"}]',prof3); print("W3 source_projection: NO ERROR (unexpected)")
except Exception as e: print("W3 source_projection raised:", type(e).__name__, str(e)[:60])
print("W3 leaf-level url-only result:", json.dumps(url_only_single_pass_leafwalk('[{"start_url": "__GITLAB__"}]',prof3)))
# W4: enumerate index vs task_id
w4_in='[{"task_id":5,"start_url":"__GITLAB__/a"},{"task_id":2,"start_url":"__REDDIT__/b"}]'
w4=json.loads(source_projection(w4_in,prof1))
print("W4 draft-predicted: 0.json holds task_id 5, 1.json holds task_id 2")
print("W4 observed enumerate ordinals:", [(i,t["task_id"]) for i,t in enumerate(w4)])
# W5: missing / non-string map entry
for name,vals in (("missing",{k:v for k,v in prof1.items() if k!="MAP"}),("nonstring",dict(prof1,MAP=7))):
    try: source_projection('[{"start_url":"__GITLAB__"}]',vals); print("W5",name,"NO ERROR")
    except Exception as e: print("W5",name,"raised:",type(e).__name__, str(e)[:60])
