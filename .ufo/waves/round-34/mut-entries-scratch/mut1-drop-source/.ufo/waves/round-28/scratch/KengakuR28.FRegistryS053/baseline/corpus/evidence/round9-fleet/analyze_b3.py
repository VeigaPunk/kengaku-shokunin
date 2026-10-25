import json
from collections import Counter
recs=[json.loads(l) for l in open('/tmp/bench-r8/results.jsonl')]
meta={r['pid']:r for r in recs if r['cell']=='meta'}
B=[r for r in recs if r['cell'].startswith('B-')]
def sim_apply(s,op):
    s=dict(s);k=op[0]
    if k=='SET': s[op[1]]=op[2]
    elif k=='ADD': s[op[1]]+=op[2]
    elif k=='SUB': s[op[1]]-=op[2]
    elif k=='MOV': s[op[2]]+=s[op[1]]; s[op[1]]=0
    elif k=='DEL': del s[op[1]]
    elif k=='NEW': s[op[1]]=op[2]
    return s
def sa(init,ops,n=None):
    s=dict(init);o=[]
    for op in (ops if n is None else ops[:n]): s=sim_apply(s,op); o.append(s)
    return o
by={}
for r in B: by[(r['cell'],r['pid'])]=r
pids=list(range(1,9))
print('pid | cell | ok | outcome | got!=want keys (got -> want | sim_corrupt final)')
for pid in pids:
    m=meta[pid]; truth=sa(m['init'],m['ops']); cm=sa(m['init'],m['ops'],7)[-1]
    for cell in ['B-corrupt-plain','B-corrupt-hint']:
        r=by[(cell,pid)]; k=r['corrupt_field']; cf=r['corrupt_from']
        sm=dict(cm); sm[k]=cf; simc=sa(sm,m['ops'][7:])[-1]
        if r['got'] is None: print(pid,cell,'PARSE FAIL'); continue
        g,w=r['got'],r['want']
        diff=sorted(set(g)|set(w))
        cells=[]
        for kk in diff:
            if g.get(kk)!=w.get(kk):
                tag='PROP' if g.get(kk)==simc.get(kk) and simc.get(kk)!=w.get(kk) else 'ERR'
                cells.append('%s:%s->%s(sim%s/%s)'%(kk,g.get(kk),w.get(kk),simc.get(kk),tag))
        addl=sorted(set(simc)|set(w))
        propk=[kk for kk in addl if simc.get(kk)!=w.get(kk)]
        print('%d | %-14s | %-5s | %-10s | %s'%(pid,cell.split('B-')[1],r['ok'],r['outcome'],'; '.join(cells) or 'none'))
        if cell=='B-corrupt-plain':
            print('     potency: keys differing sim_corrupt vs want =',propk,'=> potent' if propk else '=> INERT (corruption erased by tail ops)')
print()
print('=== ops 8-10 detail per pid, mid state ===')
for pid in pids:
    m=meta[pid]; cm=sa(m['init'],m['ops'],7)[-1]
    print('pid',pid,'mid',json.dumps(cm))
    for i in range(3):
        print('    op%d %s'%(i+8,' '.join(map(str,m['ops'][i+7]))))
    print('    corrupt_field/from:',by[('B-corrupt-plain',pid)]['corrupt_field'],by[('B-corrupt-plain',pid)]['corrupt_from'])
