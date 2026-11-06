#!/usr/bin/env python3
"""locator-suppressed census — rows whose explicit corpus/evidence/ path the frozen gate never binds
because a higher-precedence route (provenance-row > upstream URL > explicit lane path) returned a
capture first. Read-only: parses `anchor_digest_check.py --verbose` BIND lines and corpus/SOURCES.md."""
import re, sys, collections
txt = open(sys.argv[1]).read()
src = open(sys.argv[2]).read().split('\n')
binds = collections.defaultdict(list)
for m in re.finditer(r'^BIND\+? (S\d+) capture=(\S+) by=(\S+)', txt, re.M):
    binds[m.group(1)].append((m.group(2), m.group(3)))
n = 0
for l in src:
    m = re.match(r'^ {0,3}\|\s*(S\d{3,})\s*\|', l)
    if not m: continue
    sid = m.group(1)
    paths = re.findall(r'corpus/evidence/[A-Za-z0-9_./-]+', l)
    if 'raw.githubusercontent.com/harbor-framework/terminal-bench-2' not in l or not paths: continue
    bp = {p for p, _ in binds.get(sid, [])}
    un = [p for p in paths if not any(p.startswith(x) or x.startswith(p) for x in bp)]
    if un:
        n += 1
        print(f"{sid} suppressed={','.join(un)} route={','.join(sorted({b for _, b in binds.get(sid, [])}))}")
print(f"rows_with_suppressed_explicit_path={n}")
