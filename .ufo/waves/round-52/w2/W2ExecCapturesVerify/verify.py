import json,hashlib,os,re,urllib.request,collections,sys
L='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
d=json.load(open(L+'/plans/round52-tasks.json'));pin=d['pin']
cp=sorted({p for f in d['capture_population'].values() for p in f})
root=L+'/corpus/evidence/round52/graders/'
sums={}
for l in open(root+'SHA256SUMS'):
    h,p=l.split(None,1);p=p.strip();p=p[2:] if p.startswith('./') else p;sums[p]=h
sel=[(i,cp[i]) for i in range(0,len(cp),19)]
res=[]
for i,p in sel:
    url=f'https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{pin}/{p}'
    r={'index':i,'path':p,'url':url}
    try:
        b=urllib.request.urlopen(url,timeout=60).read()
        r['fetched_sha256']=hashlib.sha256(b).hexdigest();r['fetched_bytes']=len(b)
    except Exception as e: r['fetch_error']=repr(e)
    f=root+p
    if os.path.exists(f):
        cb=open(f,'rb').read();r['committed_sha256']=hashlib.sha256(cb).hexdigest();r['committed_bytes']=len(cb)
    else: r['committed']='absent'
    r['sums_line']=sums.get(p)
    r['match']=r.get('fetched_sha256')==r.get('committed_sha256')
    r['match_sums']=r.get('fetched_sha256')==r['sums_line']
    res.append(r)
# two-way
onfs=set()
for dp,dn,fn in os.walk(root):
    for x in fn:
        rel=os.path.relpath(os.path.join(dp,x),root)
        if rel not in('SHA256SUMS','EXCLUDED.md'): onfs.add(rel)
exp=set(cp);S=set(sums)
tw={'expected':len(exp),'on_disk':len(onfs),'sums_entries':len(S),'sums_lines_total':sum(1 for _ in open(root+'SHA256SUMS')),
'expected_not_on_disk':sorted(exp-onfs),'on_disk_not_expected':sorted(onfs-exp),
'expected_not_in_sums':sorted(exp-S),'sums_not_expected':sorted(S-exp),
'on_disk_not_in_sums':sorted(onfs-S),'sums_not_on_disk':sorted(S-onfs)}
# integrity of all disk
bad=[];lens=[];small=[];errbody=[];mism=[]
for p in sorted(onfs):
    b=open(root+p,'rb').read();lens.append((len(b),p))
    if hashlib.sha256(b).hexdigest()!=sums.get(p):mism.append(p)
    if len(b)<100:small.append((p,len(b),b[:80].decode('latin1')))
    h=b[:400].lstrip().lower()
    if len(b)==0:errbody.append((p,'empty'))
    if h.startswith((b'<!doctype html',b'<html')) and not p.endswith(('.html','.htm')):errbody.append((p,'html-start'))
    if re.match(rb'^\s*\{\s*"(message|error|documentation_url)"',b[:200]) and not p.endswith('.json'):errbody.append((p,'json-error'))
    if b.startswith((b'404: Not Found',b'400: Invalid',b'429')):errbody.append((p,'raw 404/400 text'))
    if b'\x00' not in b[:8000]:
        try:b.decode('utf-8')
        except: errbody.append((p,'non-utf8 text-ish'))
ls=sorted(x for x,_ in lens)
def q(f):return ls[min(len(ls)-1,int(f*(len(ls)-1)))]
dist={'n':len(ls),'min':ls[0],'p10':q(.1),'p25':q(.25),'median':q(.5),'p75':q(.75),'p90':q(.9),'max':ls[-1],'total':sum(ls),
'smallest10':sorted(lens)[:10],'largest5':sorted(lens)[-5:]}
buckets=collections.Counter()
for x in ls:
    k='<100' if x<100 else '<1K' if x<1024 else '<10K' if x<10240 else '<100K' if x<102400 else '>=100K'
    buckets[k]+=1
out={'pin':pin,'selection':'sorted capture_population, 0-based index i%19==0','refetch':res,
'refetch_all_match':all(r['match'] for r in res),'two_way':tw,'sha_mismatch_on_disk_vs_sums':mism,
'length_distribution':dist,'length_buckets':dict(buckets),'files_under_100B':small,'error_body_suspects':errbody}
json.dump(out,open('capture-verification.json','w'),indent=1)
for r in res:print(r['index'],r['path'],r.get('fetched_sha256'),r.get('fetched_bytes'),r['match'],r['match_sums'],r.get('committed'))
print({k:(v if not isinstance(v,list) else len(v)) for k,v in tw.items()})
print(tw['expected_not_on_disk'],tw['on_disk_not_expected'],tw['sums_not_expected'])
print(mism,small,errbody);print({k:v for k,v in dist.items() if 'est' not in k});print(dict(buckets))
