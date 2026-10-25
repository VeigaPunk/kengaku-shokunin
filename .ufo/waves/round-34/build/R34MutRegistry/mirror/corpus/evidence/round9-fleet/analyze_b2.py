import json, math
from collections import Counter, defaultdict
recs=[json.loads(l) for l in open('/tmp/bench-r8/results.jsonl')]
meta={r['pid']:r for r in recs if r['cell']=='meta'}
B=[r for r in recs if r['cell'].startswith('B-')]
def sim_apply(state, op):
    s=dict(state); k=op[0]
    if k=='SET': s[op[1]]=op[2]
    elif k=='ADD': s[op[1]]+=op[2]
    elif k=='SUB': s[op[1]]-=op[2]
    elif k=='MOV': s[op[2]]+=s[op[1]]; s[op[1]]=0
    elif k=='DEL': del s[op[1]]
    elif k=='NEW': s[op[1]]=op[2]
    return s
def sa(init,ops,n=None):
    s=dict(init); out=[]
    for op in (ops if n is None else ops[:n]): s=sim_apply(s,op); out.append(s)
    return out
by=defaultdict(dict)
for r in B: by[r['cell']][r['pid']]=r
pids=sorted(by['B-corrupt-plain'])

print('== item5 corruption audit (per pid) ==')
hdr=('pid','key','corrupt_from','true_mid','delta','hist_j','hist_val','potent','tail_refs','in_tail_touched','cand_nonempty')
print(' '.join('%s'%h for h in hdr))
for pid in pids:
    m=meta[pid]; init=m['init']; ops=m['ops']
    truth=sa(init,ops); correct=sa(init,ops,7); sm=dict(correct[-1])
    r=by['B-corrupt-plain'][pid]; k=r['corrupt_field']; cf=r['corrupt_from']; tv=sm.get(k)
    jsrc=None
    for j in range(5,-1,-1):
        hv=correct[j].get(k)
        if hv is not None and hv!=sm[k]: jsrc=j; break
    hv=correct[jsrc].get(k) if jsrc is not None else None
    smc=dict(sm); smc[k]=cf
    simc=sa(smc,ops[7:])[-1]
    potent = simc!=truth[-1]
    refs=[(i+8,ops[i+7]) for i in range(3) if k in ops[i+7][1:3]]
    cand=[kk for kk in m['tail_touched'] if kk in sm]
    print('%-3s %-8s %-4s %-4s %+4d  %-4s %-4s %-5s %-34s %-5s %s'%(pid,k,cf,tv,cf-tv,
        jsrc+1 if jsrc is not None else '-',hv if hv is not None else '-',potent,refs,k in m['tail_touched'],bool(cand)))
print()
print('ops 8-10 per pid:')
for pid in pids:
    print(' pid',pid,[ '%d:%s'%(i+8,' '.join(map(str,meta[pid]['ops'][i+7]))) for i in range(3)],' mid_keys',sorted(sa(meta[pid]['init'],meta[pid]['ops'],7)[-1]))
print()
print('meta tail_touched vs keys present at mid:')
for pid in pids:
    m=meta[pid]; sm=sa(m['init'],m['ops'],7)[-1]
    print(' pid',pid,'tail_touched',m['tail_touched'],'present_at_mid_intersection',[k for k in m['tail_touched'] if k in sm])

print()
print('== item6 ceiling ==')
for c in ['B-corrupt-plain','B-corrupt-hint','B-clean-plain','B-clean-hint']:
    print(c,'failing pids',[p for p in pids if not by[c][p]['ok']])
fails_plain=[p for p in pids if not by['B-clean-plain'][p]['ok']]
fails_hint=[p for p in pids if not by['B-clean-hint'][p]['ok']]
both=sorted(set(fails_plain)&set(fails_hint)); anyc=sorted(set(fails_plain)|set(fails_hint))
print('clean-plain fails',fails_plain,'clean-hint fails',fails_hint)
print('fail BOTH clean',both,'fail ANY clean',anyc)
for p in anyc:
    print(' pid',p,'c-plain',by['B-corrupt-plain'][p]['ok'],by['B-corrupt-plain'][p]['outcome'],
          '| c-hint',by['B-corrupt-hint'][p]['ok'],by['B-corrupt-hint'][p]['outcome'])
capok=[p for p in pids if p not in anyc]
print('pids passing BOTH clean cells (n=%d):'%len(capok),capok)
for c in ['B-corrupt-plain','B-corrupt-hint']:
    sub=[by[c][p] for p in capok]
    print('  %s on clean-capable subset: %d/%d %s'%(c,sum(r['ok'] for r in sub),len(sub),dict(Counter(r['outcome'] for r in sub))))

print()
print('== extra: corrupt vs clean raw identity per (pid,cond) ==')
for cond in ['plain','hint']:
    same=[p for p in pids if by['B-corrupt-'+cond][p]['raw']==by['B-clean-'+cond][p]['raw']]
    print('cond',cond,'byte-identical raw pids:',same,'count',len(same))
print()
print('== extra: is corrupt got == sim from TRUE mid (i.e. ignored corruption)? ==')
for c in ['B-corrupt-plain','B-corrupt-hint']:
    ign=[]
    for p in pids:
        m=meta[p]; truth=sa(m['init'],m['ops']); 
        if by[c][p]['got']==truth[-1]: ign.append(p)
    print(c,'got==want pids (same as corrected):',ign)
