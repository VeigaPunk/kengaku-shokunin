import json,re,os,glob
L='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
F='/home/vgpnk/Projects/shokunin'
rows=json.load(open('rows-parsed.json'))
pat=re.compile(r'((?:/home/vgpnk/Projects/shokunin/)?(?:corpus|plans|\.ufo|scripts|\.\./|/fast|/home|~)?/?[\w\-\.]*(?:/[\w\-\.\*\{\}]+)+)')
seen={}
for r in rows:
    toks=set()
    for c in ('entry','verdict','selftest','pinned','scope'):
        for t in re.findall(r'`([^`]+)`', r[c] or ''):
            for m in re.findall(r'((?:corpus|plans|\.ufo|scripts)/[\w\-\./\{\}\*]+)', t):
                toks.add(('lane',m.rstrip('.,;:)')))
            for m in re.findall(r'(/home/vgpnk/[\w\-\./]+)', t):
                toks.add(('abs',m.rstrip('.,;:)')))
        for m in re.findall(r'(?<![\w/`])((?:corpus|plans|\.ufo|scripts)/[\w\-\./]+)', r[c] or ''):
            toks.add(('lane',m.rstrip('.,;:)')))
    for kind,t in sorted(toks):
        if kind=='lane': p=os.path.join(L,t)
        else: p=t
        ok=bool(glob.glob(p)) if ('*' in p or '{' in p) else os.path.exists(p)
        seen.setdefault(t,[]).append((r['name'],ok))
for t in sorted(seen):
    rs=sorted(set(n for n,_ in seen[t])); ok=seen[t][0][1]
    print(('OK  ' if ok else 'MISS'), t, '<-', ','.join(rs)[:150])
