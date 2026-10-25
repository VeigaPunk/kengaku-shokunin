import json, math, collections as C
L=[json.loads(x) for x in open('/tmp/bench-r8/results.jsonl')]; G=lambda c:[r for r in L if r['cell']==c]; M={m['pid']:m for m in G('meta')}
KW=lambda r:{k for k in set(r['got'])|set(r['want']) if r['got'].get(k)!=r['want'].get(k)}; DZ=lambda r:not r['ok'] and bool(KW(r)) and all(r['want'].get(k,0)==0 and k not in r['got'] for k in KW(r)); TOL=lambda r:all(r['want'].get(k,0)==0 and k not in r['got'] for k in KW(r))
def S(rs):
    n=max(len(rs),1); return (len(rs),sum(r['ok'] for r in rs),sum(TOL(r) for r in rs),round(sum(r['nwrong'] for r in rs)/n,2),round(sum(r['wall_s'] for r in rs)/n,2),round(sum(r['usage']['completion_tokens'] for r in rs)/n,1))
BY={c:{p:{r['turn']:r for r in G(c) if r['pid']==p} for p in sorted({r['pid'] for r in G(c)})} for c in ('A-INC','A-CKPT')}; I,K=BY['A-INC'],BY['A-CKPT']
print("1 final [n,pass,tolerant,mean_nwrong,mean_wall_s,mean_ctok]",[(c,S([r for r in G(c) if r['turn']==t])) for c,t in (('A-INC',10),('A-CKPT',10),('A-MONO',1))])
print("1b whole-cell",{c:S(G(c)) for c in ('A-INC','A-CKPT','A-MONO')})
print("2 onset,final_ok,final_nwrong (INC)",{p:(next((t for t in sorted(d) if not d[t]['ok']),None),d[10]['ok'],d[10]['nwrong']) for p,d in I.items()})
T10=lambda rs,ts:[(t,sum(1 for p in rs if rs[p][t]['ok']),sum(1 for p in rs if TOL(rs[p][t])),round(sum(rs[p][t]['nwrong'] for p in rs)/10,2)) for t in ts]
print("2b INC per-turn [t,strict,tolerant,mean_nwrong]",T10(I,range(1,11)))
print("2c onset,final_ok (CKPT)",{p:(next((t for t in (4,7,10) if not d[t]['ok']),None),d[10]['ok']) for p,d in K.items()})
print("2d CKPT per-turn [t,strict,tolerant,mean_nwrong]",T10(K,(4,7,10)))
EV=[(p,k,[t for t in range(1,11) if k in KW(d[t])][0],[t for t in range(1,11) if k in KW(d[t])][-1]) for p,d in I.items() for k in {k for t in range(1,11) for k in KW(d[t])}]
print("3 episodes (pid,key,first,last)",sorted(EV))
FIX=lambda d:sum(1 for t in range(1,10) for k in KW(d[t]) if k not in KW(d[t+1])); TOT=lambda d:sum(len(KW(d[t])) for t in range(1,10))
print("3b t->t+1 recovery (fixed,total)",(sum(FIX(d) for d in I.values()),sum(TOT(d) for d in I.values())),"per-pid",{p:(FIX(d),TOT(d)) for p,d in I.items()})
def sign(x,y):
    v=[int(x[p])-int(y[p]) for p in sorted(x)]; z=[t for t in v if t]; a,b=v.count(1),v.count(-1); k=min(a,b)
    return v,a,b,round(min(2*sum(math.comb(len(z),i) for i in range(k+1))/2**len(z),1) if z else 1.0,4)
F={c:{p:d[10]['ok'] for p,d in BY[c].items()} for c in BY}; F['A-MONO']={r['pid']:r['ok'] for r in G('A-MONO')}
for a,b in (('A-INC','A-CKPT'),('A-CKPT','A-MONO'),('A-INC','A-MONO')): print("4 sign",a,b,sign(F[a],F[b]))
A=G('A-CKPT-ack'); cls=lambda r:'state' if '{' in r['raw'] else 'ack' if r['raw'].lstrip().startswith('ok') else 'other'
print("5 ack classes",dict(C.Counter((r['turn']==1,cls(r)) for r in A)))
for r in [z for z in A if z['turn']==1]:
    s=r['raw']; g=None
    try: g=json.loads(s[s.find('{'):s.rfind('}')+1])
    except Exception: pass
    print("   ackT1",r['pid'],"fence_closed",s.rstrip().endswith('```'),"parsed",g is not None,"exact",g==M[r['pid']]['truth'][0])
fcls=lambda r:'ack_record_no_got' if 'got' not in r else 'graded' if isinstance(r['got'],dict) and r['finish']!='length' and r['raw'] else 'parse_fail_or_length'
print("6 fail classes",{c:dict(C.Counter(fcls(r) for r in G(c))) for c in ('A-INC','A-CKPT','A-MONO','A-CKPT-ack')})
print("7 drop-zero-only fails,total fails",{c:(sum(DZ(r) for r in G(c)),sum(1 for r in G(c) if not r['ok'])) for c in ('A-INC','A-CKPT','A-MONO')})
print("7b episode onset op-type",[(p,k,M[p]['ops'][t-1][0]) for p,k,t,_ in sorted(EV)])
print("7c MOV turns per pid",{p:[i+1 for i,o in enumerate(M[p]['ops']) if o[0]=='MOV'] for p in M})