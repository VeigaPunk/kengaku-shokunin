import os, sys, subprocess, pathlib, shutil, hashlib, re, json
S=pathlib.Path(os.environ['S']); L=S/'lane'/'plans'
W=S/'uw'; shutil.rmtree(W,ignore_errors=True); W.mkdir()
GE=['-c','user.name=f','-c','user.email=f@l','-c','commit.gpgsign=false']
def git(r,*a): return subprocess.run(['git','-C',str(r),*GE,*a],check=True,capture_output=True,text=True).stdout
def repo(name):
    r=W/name; r.mkdir(); git(r,'init','-q','-b','master'); return r
def put(r,rel,txt):
    p=r/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(txt)
def commit(r,m='c'): git(r,'add','-A'); git(r,'commit','-q','-m',m)
sha=lambda b: hashlib.sha256(b).hexdigest()
HDR="| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
def row(sid,src,anchor,cells=None):
    c=cells or [f"{src}","docs","A","scope",anchor,"teaches","mined","2026-10-26","2027-01-24","corpus/knowledge/x.md"]
    return f"| {sid} | "+" | ".join(c)+" |\n"
CAP=b"capture bytes one\n"; D=sha(CAP)
def anchor_repo(name,rows,caps=None,lessons=None,dirty_lessons=None):
    r=repo(name); put(r,'corpus/SOURCES.md',HDR+rows)
    for rel,b in (caps or {'corpus/evidence/r1/cap.txt':CAP}).items(): put(r,rel,b if isinstance(b,str) else b.decode())
    for rel,t in (lessons or {}).items(): put(r,rel,t)
    commit(r)
    for rel,t in (dirty_lessons or {}).items(): put(r,rel,t)
    return r
def muts(tool):
    s=(L/tool).read_text(); return s
def mutate(tool,old,new,name):
    s=muts(tool); assert s.count(old)==1,(name,s.count(old)); d=W/f'mut-{name}'; d.mkdir(); f=d/tool; f.write_text(s.replace(old,new)); return f
def run(f,args):
    p=subprocess.run(['python3',str(f),*args],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=60)
    out=p.stdout+p.stderr; cls=sorted(set(re.findall(r'class=([a-z-]+)',out)))|set() if False else sorted(set(re.findall(r'class=([a-z-]+)',out)))
    return p.returncode,cls,out
R={}
def case(label,tool,old,new,args,note=''):
    ref=run(L/tool,args); m=mutate(tool,old,new,label.replace(' ','_')); mu=run(m,args)
    print(f"{label}: ref rc={ref[0]} cls={ref[1]} | mut rc={mu[0]} cls={mu[1]} {'DIFF' if (ref[0],ref[1])!=(mu[0],mu[1]) else ('textdiff' if ref[2].replace(str(L),'')!=mu[2].replace(str(m.parent),'') else 'SAME')} {note}")
A='anchor_digest_check.py'; O='order_check.py'
# u3 row-path binding
r=anchor_repo('u3',row('S901','corpus/evidence/r1/cap.txt',f"anchor sha256 {D}"))
case('u3 row-path branch off',A,'        if p in idx["file_digest"] or (p.rsplit("/", 1)[0] if "/" in p else "",','        if False and (p.rsplit("/", 1)[0] if "/" in p else "",',['--lane',str(r)])
# u3b directory
r=anchor_repo('u3b',row('S901','corpus/evidence/r1/',f"anchor sha256 {D}"))
case('u3b dirish branch (names-a-directory) reason swap',A,'"names-a-directory-not-a-capture-file" if dirish','"names-a-directory-not-a-capture-file" if not dirish',['--lane',str(r)],'(detail text only)')
# u5/u6 short / long
r=anchor_repo('u5',row('S901','corpus/evidence/r1/cap.txt',f"anchor sha256 {D[:63]}"))
case('u5 short->long label',A,'cls, why = ("digest-short" if len(tok) < 64 else "digest-long")','cls, why = ("digest-long" if len(tok) < 64 else "digest-long")',['--lane',str(r)])
r=anchor_repo('u6',row('S901','corpus/evidence/r1/cap.txt',f"anchor sha256 {D+'a'}"))
case('u6 long->short label',A,'cls, why = ("digest-short" if len(tok) < 64 else "digest-long")','cls, why = ("digest-short" if len(tok) < 64 else "digest-short")',['--lane',str(r)])
# u7 identical captures multi-resolve
r=anchor_repo('u7',row('S901','corpus/evidence/r1/cap.txt and corpus/evidence/r1/cap2.txt',f"anchor sha256 {D}"),caps={'corpus/evidence/r1/cap.txt':CAP,'corpus/evidence/r1/cap2.txt':CAP})
case('u7 hit[:1]',A,'hit = sorted(p for p, ent in per.items() if tok in ent["digests"])\n                claimed.update(hit)\n                if verbose:\n                    path, how','hit = sorted(p for p, ent in per.items() if tok in ent["digests"])[:1]\n                claimed.update(hit)\n                if verbose:\n                    path, how',['--lane',str(r)])
# u8 multi-locator row, no token
r=anchor_repo('u8',row('S901','corpus/evidence/r1/cap.txt and corpus/evidence/r1/cap2.txt',"anchor none"),caps={'corpus/evidence/r1/cap.txt':CAP,'corpus/evidence/r1/cap2.txt':CAP+b'x'})
print('u8 reference on multi-locator no-token row:',run(L/A,['--lane',str(r)])[:2])
# u9 working-tree erratum
wrong='f'*64
rows=row('S901','corpus/evidence/r1/cap.txt',f"anchor sha256 {wrong}")
err=f"Erratum (round 37): S901 anchor sha256 {wrong} corrected to sha256 {D}\n"
r=anchor_repo('u9',rows,lessons={'corpus/lessons/l.md':'# lessons\n'},dirty_lessons={'corpus/lessons/l.md':'# lessons\n'+err})
case('u9 worktree->HEAD read',A,'f.read_text(encoding="utf-8", errors="replace")','git(lane, "show", "HEAD:" + p).decode("utf-8", "replace")',['--lane',str(r)])
# u10 stale erratum: row repaired; erratum cites old wrong token (not a committed digest) / (committed sibling digest)
fixed=row('S901','corpus/evidence/r1/cap.txt',f"anchor sha256 {D}")
r=anchor_repo('u10a',fixed,lessons={'corpus/lessons/l.md':'# l\n'+err})
print('u10a stale erratum, wrong token uncommitted:',run(L/A,['--lane',str(r)])[:2])
sib=b"sibling\n"; SD=sha(sib)
err2=f"Erratum (round 37): S901 anchor sha256 {SD} corrected to sha256 {D}\n"
r=anchor_repo('u10b',fixed,caps={'corpus/evidence/r1/cap.txt':CAP,'corpus/evidence/r1/sib.txt':sib},lessons={'corpus/lessons/l.md':'# l\n'+err2})
print('u10b stale erratum, wrong token = sibling digest:',run(L/A,['--lane',str(r)])[:2])
# verbose
r=anchor_repo('u4',row('S901','corpus/evidence/r1/cap.txt',f"anchor sha256 {D}"))
case('u4 verbose off',A,'    if verbose:\n        for r in rows:','    if False:\n        for r in rows:',['--lane',str(r),'--verbose'],'(stdout lines only)')
# u2 usage exits
e=W/'empty'; e.mkdir()
case('u2a lane-not-dir guard off',A,'        if not lane.is_dir():\n            raise Usage','        if False:\n            raise Usage',['--lane',str(W/'nonexistent')])
nos=repo('nosrc'); put(nos,'x','1'); commit(nos)
case('u2b no SOURCES guard off',A,'        if not (lane / "corpus/SOURCES.md").is_file():','        if False:',['--lane',str(nos)])
ng=W/'nogit'; (ng/'corpus').mkdir(parents=True); (ng/'corpus/SOURCES.md').write_text(HDR)
case('u2c no .git guard off',A,'        if not (lane / ".git").exists():','        if False:',['--lane',str(ng)])
# order fixtures
def order_repo(name,receipt_state='committed-last',claims_extra=''):
    r=repo(name); put(r,'plans/round-7-claims.md','# claims\n'+claims_extra); put(r,'.ufo/waves/round-7/claims/n.txt','nothing\n'); commit(r,'freeze')
    rc='corpus/evidence/round7/x-probe.txt'
    if receipt_state=='committed-last': put(r,rc,'CASE c1 observed=PASS\n'); commit(r,'receipt')
    elif receipt_state=='staged': put(r,rc,'CASE c1 observed=PASS\n'); git(r,'add','-A')
    elif receipt_state=='disk': put(r,rc,'CASE c1 observed=PASS\n')
    return r
oa=lambda r:['--lane',str(r),'--claims','plans/round-7-claims.md','--receipt','corpus/evidence/round7/x-probe.txt']
r=order_repo('o_ok'); print('order accept base',run(L/O,oa(r))[:2])
r=order_repo('o17','staged')
case('u17 HEAD check (receipt) off',O,'        for label, path in (("claims", claims), ("receipt", receipt)):\n            if git.rc("cat-file", "-e", f"HEAD:{path}") != 0:','        for label, path in (("claims", claims), ("receipt", receipt)):\n            if False:',oa(r),'(uncommitted receipt)')
r=order_repo('o17b','disk')
case('u17b HEAD check off, disk receipt',O,'        for label, path in (("claims", claims), ("receipt", receipt)):\n            if git.rc("cat-file", "-e", f"HEAD:{path}") != 0:','        for label, path in (("claims", claims), ("receipt", receipt)):\n            if False:',oa(r))
ngd=W/'o_nogit'; ngd.mkdir()
case('u12 not-git guard off',O,'        if top.returncode != 0:','        if False:',oa(ngd))
case('u12b lane-is-dir guard off',O,'        if not lane.is_dir():','        if False:',oa(W/'nonexistent'))
case('u13 freeze-empty guard off',O,'        if not freeze:','        if False:',oa(order_repo('o13','committed-last')))
case('u13b receipt-commit-empty guard off',O,'        if not receipt_commit:','        if False:',oa(order_repo('o13b','committed-last')))
case('u14 --claims required off',O,'ap.add_argument("--claims", required=True,','ap.add_argument("--claims", required=False,',['--lane',str(order_repo('o14','committed-last')),'--receipt','corpus/evidence/round7/x-probe.txt'])
case('u14b --lane required off',O,'ap.add_argument("--lane", required=True,','ap.add_argument("--lane", required=False,',['--claims','plans/round-7-claims.md','--receipt','corpus/evidence/round7/x-probe.txt'])
case('u14c claims name pattern guard off',O,'        if not m:\n            raise SetupError(f"claims file name','        if False:\n            raise SetupError(f"claims file name',['--lane',str(order_repo('o14c','committed-last')),'--claims','plans/odd-claims.md','--receipt','corpus/evidence/round7/x-probe.txt'])
# u16 filename filter
r=repo('u16'); put(r,'plans/round-7-claims.md','# c\n'); put(r,'.ufo/waves/round-7/claims/run.log','gate: P10 ok fresh probe output byte-equal\n'); commit(r,'freeze'); put(r,'corpus/evidence/round7/x-probe.txt','CASE c1 observed=PASS\n'); commit(r,'receipt')
case('u16 .md-only filename filter',O,'parts[1] != "blob"','parts[1] != "blob" or not path.endswith(".md")',oa(r))
# u18 dir derived from round
r=repo('u18'); put(r,'plans/round-7-claims.md','# c\n'); put(r,'.ufo/waves/round-7/claims/run.txt','gate: P10 ok fresh probe output byte-equal\n'); commit(r,'freeze'); put(r,'corpus/evidence/round7/x-probe.txt','CASE c1 observed=PASS\n'); commit(r,'receipt')
case('u18 round+1 dir',O,'claims_dir = f".ufo/waves/round-{round_no}/claims"','claims_dir = f".ufo/waves/round-{round_no + 1}/claims"',oa(r))
# u11 index vs commits: claims staged edit w/ executed line not committed
r=order_repo('u11'); put(r,'.ufo/waves/round-7/claims/n.txt','gate: P10 ok x\n'); git(r,'add','-A')
case('u11 scan reads index? (rev-list --all->none)',O,'git.out("rev-list", "--reverse", upto, "--", claims_dir)','git.out("rev-list", "--reverse", upto, "--", claims_dir)',oa(r),'(identity control: worktree ignored in ref)')
