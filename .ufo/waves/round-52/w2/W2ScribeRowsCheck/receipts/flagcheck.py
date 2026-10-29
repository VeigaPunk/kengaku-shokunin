import json,re,os
L='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
rows=json.load(open('rows-parsed.json'))
facts=json.load(open('facts.json'))
for r in rows:
    f=facts[r['name']]
    src=open(os.path.join(L,f['script']),encoding='utf-8').read()
    toks=set()
    for c in ('entry','verdict','selftest','pinned','scope'):
        toks|=set(re.findall(r'(?<![\w-])(--[a-z][a-z0-9\-]*)', r[c] or ''))
    missing=[t for t in sorted(toks) if t not in src]
    # flags cited in entry command only (usable invocation)
    ent=set(re.findall(r'(?<![\w-])(--[a-z][a-z0-9\-]*)', r['entry']))
    notarg=[t for t in sorted(ent) if t not in f['add_argument']]
    print(f"{r['name']:26s} cited={sorted(toks)} NOT-IN-SOURCE={missing} ENTRY-NOT-ARGPARSE={notarg}")
