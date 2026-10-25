import json, itertools, math
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
def states_along(init,ops,n=None):
    s=dict(init); out=[]
    for op in (ops if n is None else ops[:n]): s=sim_apply(s,op); out.append(s)
    return out

CELLS=['B-corrupt-plain','B-corrupt-hint','B-clean-plain','B-clean-hint']
by=defaultdict(dict)
for r in B: by[r['cell']][r['pid']]=r
pids=sorted(by[CELLS[0]])
print('B pids per cell:', {c:sorted(by[c]) for c in CELLS})

# ---- item 1: 2x2 table ----
print('\n== item1 2x2 ==')
for c in CELLS:
    rs=[by[c][p] for p in pids]
    print(c, 'pass=%d/8'%sum(r['ok'] for r in rs),
          'outcome=',dict(Counter(r['outcome'] for r in rs)),
          'healed=%d'%sum(bool(r['healed']) for r in rs),
          'parse_fail=%d'%sum(r['got'] is None for r in rs),
          'finish=',dict(Counter(r['finish'] for r in rs)))

def bino_twosided(b,c):
    n=b+c
    if n==0: return 1.0
    p=sum(math.comb(n,k) for k in range(0,min(b,c)+1))/2**n*2
    return min(1.0,p)
def signpair(pa,pb,la,lb):
    b=sum(1 for p in pids if pa[p] and not pb[p])
    c=sum(1 for p in pids if pb[p] and not pa[p])
    return b,c,bino_twosided(b,c)
def acc(cell):
    return {p:int(bool(by[cell][p]['ok'])) for p in pids}

# ---- item 2: manipulation binding corrupt-plain vs clean-plain (paired) ----
print('\n== item2 binding: corrupt-plain vs clean-plain (paired, n=8) ==')
cp, clp = acc('B-corrupt-plain'), acc('B-clean-plain')
print('corrupt-plain ok:',[cp[p] for p in pids])
print('clean-plain  ok:',[clp[p] for p in pids])
print('passed-corrupt/failed-clean =',[p for p in pids if cp[p] and not clp[p]])
print('passed-clean/failed-corrupt =',[p for p in pids if clp[p] and not cp[p]])
print('both pass =',sum(1 for p in pids if cp[p] and clp[p]),'both fail =',sum(1 for p in pids if not cp[p] and not clp[p]))
print('sign test (corrupt better/clean better):',signpair(cp,clp,'a','b'))
ch, clh = acc('B-corrupt-hint'), acc('B-clean-hint')
print('corrupt-hint ok:',[ch[p] for p in pids]); print('clean-hint  ok:',[clh[p] for p in pids])
print('hint: sign corrupt-hint vs clean-hint:',signpair(ch,clh,'a','b'))

# ---- item 3: hint effect ----
print('\n== item3 hint effect (paired, n=8) ==')
print('within corrupt: plain ok',[cp[p] for p in pids],'hint ok',[ch[p] for p in pids])
print('  hint>plain pids',[p for p in pids if ch[p] and not cp[p]],'plain>hint pids',[p for p in pids if cp[p] and not ch[p]])
print('  sign test:',signpair(ch,cp,'h','p'))
print('within clean: plain ok',[clp[p] for p in pids],'hint ok',[clh[p] for p in pids])
print('  hint>plain pids',[p for p in pids if clh[p] and not clp[p]],'plain>hint pids',[p for p in pids if clp[p] and not clh[p]])
print('  sign test:',signpair(clh,clp,'h','p'))

# ---- item 4: propagation rate + outcome detail ----
print('\n== item4 propagation ==')
for c in ['B-corrupt-plain','B-corrupt-hint']:
    rs=[by[c][p] for p in pids]
    oc=Counter(r['outcome'] for r in rs)
    print(c,'propagated=%d/8 corrected=%d other=%d'%(oc.get('propagated',0),oc.get('corrected',0),oc.get('other',0)))
    print('  per-pid outcome:',[(p,by[c][p]['outcome']) for p in pids])
for c in ['B-clean-plain','B-clean-hint']:
    rs=[by[c][p] for p in pids]
    print(c,'outcome:',dict(Counter(r['outcome'] for r in rs)),' per-pid:',[(p,by[c][p]['outcome']) for p in pids])

# other responses raw
print('\n-- "other" raw samples --')
for c in ['B-corrupt-plain','B-corrupt-hint','B-clean-plain','B-clean-hint']:
    for p in pids:
        r=by[c][p]
        if r['outcome']=='other':
            print('###',c,'pid',p,'ok',r['ok'],'finish',r['finish'])
            print('corrupt_field',r.get('corrupt_field'),'corrupt_from',r.get('corrupt_from'))
            print('GOT',json.dumps(r['got']))
            print('WANT',json.dumps(r['want']))
            print('RAW[:400]',repr(r['raw'][:400]))
            print()

# ---- item 5: corruption audit ----
print('\n== item5 corruption audit ==')
for pid in pids:
    m=meta[pid]; init=m['init']; ops=m['ops']
    truth=states_along(init,ops)      # truth[i] = state after op i+1
    correct=states_along(init,ops,7)  # 7 states
    state_mid=dict(correct[-1])
    r=by['B-corrupt-plain'][pid]
    k=r['corrupt_field']; cf=r['corrupt_from']; tv=state_mid.get(k)
    # find historical source j
    jsrc=None
    for j in range(5,-1,-1):
        hv=correct[j].get(k)
        if hv is not None and hv!=state_mid[k]: jsrc=j; break
    sc=states_along(dict({**state_mid,k:cf}),ops[7:])[-1]
    delta=cf-tv; fdelta=sc.get(k)-truth[-1].get(k)
    ops_tail=[(i+8,ops[i+7]) for i in range(3)]
    refs=[(n,o) for n,o in ops_tail if k in o[1:3]]
    print('pid %d key=%-8s corrupt_from=%-4s true_mid=%-4s delta=%+d | hist_j=%s hist_val=%s | final_delta=%s | tail_refs=%s | tail_touched=%s | exercise_ok=%s'%(
        pid,k,cf,tv,delta,jsrc+1 if jsrc is not None else None,
        correct[jsrc].get(k) if jsrc is not None else None, fdelta, refs, m['tail_touched'], k in m['tail_touched']))

# does corruption actually change the final state (can it bind)?
print('\n-- corruption potency: sim(corrupt-mid)+tail vs truth-final --')
for pid in pids:
    m=meta[pid]; init=m['init']; ops=m['ops']
    truth=states_along(init,ops); correct=states_along(init,ops,7)
    r=by['B-corrupt-plain'][pid]; k=r['corrupt_field']; cf=r['corrupt_from']
    sm=dict(correct[-1]); sm[k]=cf
    simc=states_along(sm,ops[7:])[-1]
    print('pid',pid,'key',k,'sim_corrupt==want?',simc==truth[-1],'diffkeys',[kk for kk in set(simc)|set(truth[-1]) if simc.get(kk)!=truth[-1].get(kk)])

# ---- item 6: ceiling ----
print('\n== item6 ceiling ==')
for c in CELLS:
    print(c,'failing pids',[p for p in pids if not by[c][p]['ok']])
clean_fail=set(p for p in pids if not (by['B-clean-plain'][p]['ok'] and by['B-clean-hint'][p]['ok']))
print('pids failing BOTH clean cells:',sorted(clean_fail))
print('pids failing >=1 clean cell:',sorted(set(p for p in pids if not by['B-clean-plain'][p]['ok'] or not by['B-clean-hint'][p]['ok'])))
# do those pids also fail corrupt?
for p in sorted(clean_fail):
    print(' pid',p,'corrupt-plain ok',by['B-corrupt-plain'][p]['ok'],'outcome',by['B-corrupt-plain'][p]['outcome'],
          '| corrupt-hint ok',by['B-corrupt-hint'][p]['ok'],'outcome',by['B-corrupt-hint'][p]['outcome'])
# conditional: among corrupt cells, propagate rate excluding ceiling-fail pids
cap_ok=[p for p in pids if p not in clean_fail]
print('capability-clean pids (pass both clean):',cap_ok,' n=',len(cap_ok))
for c in ['B-corrupt-plain','B-corrupt-hint']:
    sub=[by[c][p] for p in cap_ok]
    print(' ',c,'on capability-clean subset: pass=%d/%d outcome=%s'%(sum(r['ok'] for r in sub),len(sub),
          dict(Counter(r['outcome'] for r in sub))))
