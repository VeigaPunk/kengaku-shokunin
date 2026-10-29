import json,re,sys
lines=[l[1:] for l in open(sys.argv[1]) if l.startswith('+|')]
rows=[]
for l in lines:
    cells=[c.strip() for c in l.strip().strip('|').split(' | ')]
    # split on unescaped ' | ' ; cells count check
    rows.append(cells)
out=[]
for c in rows:
    out.append({'n':len(c),'name':c[0].strip('`'),'kind':c[1] if len(c)>1 else None,'entry':c[2] if len(c)>2 else None,'verdict':c[3] if len(c)>3 else None,'selftest':c[4] if len(c)>4 else None,'pinned':c[5] if len(c)>5 else None,'scope':c[6] if len(c)>6 else None,'owner':c[7] if len(c)>7 else None})
json.dump(out,open('rows-parsed.json','w'),indent=1,ensure_ascii=False)
for o in out: print(o['n'],o['name'],o['kind'],len(o['entry'] or ''),len(o['verdict'] or ''),len(o['selftest'] or ''),len(o['pinned'] or ''),len(o['scope'] or ''),o['owner'])
