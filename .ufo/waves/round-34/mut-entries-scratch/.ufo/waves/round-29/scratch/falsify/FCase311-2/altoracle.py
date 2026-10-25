import json
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
raw=open(LANE+'/plans/fixtures/r28/webarena/config_files/test.raw.json',encoding='utf-8').read()
profs=json.load(open(LANE+'/plans/fixtures/r29/profiles.json',encoding='utf-8'))
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
TOK=lambda n:"__%s__"%n
orig=json.loads(raw)
def rewrite(o, vals):
    if isinstance(o,dict): return {k:rewrite(v,vals) for k,v in o.items()}
    if isinstance(o,list): return [rewrite(v,vals) for v in o]
    if isinstance(o,str):
        s=o
        for n in ORDER: s=s.replace(TOK(n),vals[n])
        return s
    return o
for pname,pm in profs.items():
    text=raw
    for n in ORDER: text=text.replace(TOK(n),pm['values'][n])
    a=json.loads(text)          # sequential global text replacement (upstream order)
    b=rewrite(orig,pm['values']) # decoded-leaf rewriting alternative oracle
    diffs=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    print(pname,'tasks where decoded-rewrite differs from text-replace:',len(diffs),diffs[:5])
    # token substring relations among the six tokens
print('token substring pairs:',[(p,q) for p in ORDER for q in ORDER if p!=q and TOK(p) in TOK(q)])
