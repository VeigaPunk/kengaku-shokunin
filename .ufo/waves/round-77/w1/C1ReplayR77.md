# C1ReplayR77 — independent frozen replay

Axes: coverage and calibration. Scope: freeze `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`; no landing-tip claim.

## Results

`python3 /fast/scratch/hyaku/kengaku-r77/C1ReplayR77/replay.py` exited 0 and printed:

```text
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED freeze n=0 anchored_rows=33
UNLISTED base n=33 anchored_rows=33
COUNTER_RC 0
DISAGREEMENTS []
INDEPENDENT_EXIT 0
```

Independent probes did not import the counter or read `c1-*.txt`. Counter comparison was invoked only after the independent probes. All 28 verdicts matched; disagreement list is empty. Remote APIs received no traffic. No production files changed; no tools installed. LSP is unavailable in this seat's mounted tools; no symbol refactor was needed.

Counter command (cwd scratch clone): `python3 plans/round77_c1_declared_surfaces.py --lane .`, rc 0, printed:

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE clean
CANONICAL source=## Declared surfaces rows=28
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=c7d675c146b1d529…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```

The frozen command's literal TARGET line has **no `defects=0` field**; it prints `DEFECTS n=0` separately. Thus the requested single-line TARGET spelling does not reproduce exactly, although the predicate and six measured values do. Counter source `:533-540` shows the separate defects metric.

## Independent row evidence

Numbers are canonical row indices; corresponding PROVINCE lines are 1022 + index. Every row below was printed by the independent parser.

For path rows the exact command is `test -e <expanded-anchor>`. `~` expanded to `/home/vgpnk`; relative anchors expanded under `/fast/scratch/hyaku/kengaku-r77/C1ReplayR77/clone/` (abbreviated `$C` below). Exit 0 means present; exit 1 absent.

| Row | Name / anchor | Own verdict | Exact probe result |
|---|---|---|---|
|1|Research notes: `~/Projects/webzites/repos/llm-wiki`|absent|test rc 1|
|2|Former notes: `~/wikillm/llm-wiki`|absent|test rc 1|
|3|Battery: `~/archive/bench-arena`|absent|test rc 1|
|4|Former battery: `~/bench-arena`|absent|test rc 1|
|5|`http://127.0.0.1:34113`|absent|curl rc 7, HTTP 000|
|6|`http://127.0.0.1:45669`|absent|curl rc 7, HTTP 000|
|7|`http://127.0.0.1:1234`|present|curl rc 0, HTTP 415|
|8|`~/Projects/bounties/ledger/telemetry.jsonl`|absent|test rc 1|
|9|`~/Projects/the-bounty-hunter`|absent|test rc 1|
|10|`~/.bailian/telemetry.jsonl`|absent|test rc 1|
|11|`~/.bailian/wiki-sync-state.json`|absent|test rc 1|
|12|`~/.bailian/skills/bailian-docs-llm-wiki/models/`|absent|test rc 1|
|13|HF and OpenRouter APIs|remote|dated REMOTE marker true; no egress|
|14|`corpus/evidence/`|present|test rc 0|
|15|`grader.py`|present|sha256sum rc 0; `90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f`|
|16|`plans/attrib_probe.py`|present|sha256sum rc 0; `489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b`|
|17|`plans/attrib-r21-frozen.md`|present|test rc 0|
|18|`corpus/QUALITY.md`|present|test rc 0|
|19|`corpus/SOURCES.md`|present|grep rc 0, rows 245, pin 245|
|20|`~/.local/share/ds-flash-shim/shim.py`|present|sha256sum rc 0; `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386`|
|21|`127.0.0.1:8791`|present|socket.create_connection timeout=3 connected true|
|22|`corpus/knowledge/eval-prior-art-calibration.md`|present|test rc 0|
|23|`corpus/knowledge/open-model-catalogs.md`|present|test rc 0|
|24|`plans/attrib_calibration.py`|present|test rc 0; receipt exit literal true; ancestor rc 0|
|25|`plans/state_check.py`|present|test rc 0; receipt exit literal true; ancestor rc 0|
|26|process/service/template command|absent|three independent tests rc 1 each|
|27|`/tmp/bench-r{4,5,6,7,7-l2-executor}`|absent|five expanded tests rc 1 each; no writes under /tmp|
|28|`corpus/README.md`|present|test rc 0|

Exact HTTP template (substitute each row's literal URL):
`curl -s --max-time 3 -o /dev/null -w '%{http_code}' URL`.
Exact hash template: `sha256sum EXPANDED_PATH`.
Exact count command:
`grep -cE '^\|[[:blank:]]*S[0-9]{3,}[[:blank:]]*\|' $C/corpus/SOURCES.md`.
TCP call: `socket.create_connection(('127.0.0.1',8791),timeout=3)` in a context manager.

Rows 24/25 read `corpus/evidence/round77/exec-attrib-calibration.txt` and `exec-state-check.txt` respectively, found exit=0 literals, and stamped tip `07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59`. Exact ancestry command for each: `git merge-base --is-ancestor 07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59 HEAD`, rc 0. These are receipt checks, not fresh execution of the two instruments.

Row 26 tests individually: `/proc/1299/cmdline`, `/home/vgpnk/.config/systemd/user/qwen-coder.service`, `/home/vgpnk/.config/llama/qwen-coder-godspeed.jinja`; rc 1 each.

## Independently enumerated supersession

Independent parser enumerated 11 Surfaces + 10 Core + 12 Historical = 33 rows, with a concrete anchor found in each. It used the first concrete anchor across cells, directory-boundary coverage, brace-prefix normalization and corpus-relative citation normalization. These are row-level coverage semantics, not every inline-token coverage.

|Table / PROVINCE line|Row / first concrete anchor|Canonical row carrying it|
|---|---|---|
|Surfaces 12|Research notes: `~/Projects/webzites/repos/llm-wiki`|1|
|Surfaces 13|Battery: `~/archive/bench-arena/`|3|
|Surfaces 14|Served model: `http://127.0.0.1:34113`|5|
|Surfaces 15|Successor: `http://127.0.0.1:45669`|6|
|Surfaces 16|Route telemetry: `~/Projects/bounties/ledger/telemetry.jsonl`|8|
|Surfaces 17|Client telemetry: `~/.bailian/telemetry.jsonl`|10|
|Surfaces 18|Catalogs: `~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}`|12|
|Surfaces 19|Artifacts: `corpus/evidence/round8-horizon/`|14|
|Surfaces 20|Gate: `grader.py`|15|
|Surfaces 21|Index: `corpus/README.md`|28|
|Surfaces 22|Literature: `corpus/knowledge/eval-prior-art-calibration.md`|22|
|Core 130|Gate: `grader.py`|15|
|Core 131|Artifacts: `corpus/README.md`|28|
|Core 132|Attribution: `plans/attrib_probe.py`|16|
|Core 133|Docs: `corpus/QUALITY.md`|18|
|Core 134|Registry: `corpus/SOURCES.md`|19|
|Core 135|Shim: `~/.local/share/ds-flash-shim/shim.py`|20|
|Core 136|Endpoint: `127.0.0.1:8791`|21|
|Core 137|Literature: `knowledge/eval-prior-art-calibration.md`|22|
|Core 138|Interval: `plans/attrib_calibration.py`|24|
|Core 139|State: `plans/state_check.py`|25|
|Historical 174|`~/Projects/webzites/repos/llm-wiki`|1|
|Historical 175|`~/wikillm/llm-wiki`|2|
|Historical 176|`~/archive/bench-arena`|3|
|Historical 177|`~/bench-arena`|4|
|Historical 178|`http://127.0.0.1:34113`|5|
|Historical 179|`/proc/1299/cmdline`|26|
|Historical 180|`~/Projects/bounties/ledger/telemetry.jsonl`|8|
|Historical 181|`~/Projects/the-bounty-hunter`|9|
|Historical 182|`~/.bailian/telemetry.jsonl`|10|
|Historical 183|`~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}`|12|
|Historical 184|`/tmp/bench-r{4,5,6,7,7-l2-executor}`|27|
|Historical 185|`knowledge/open-model-catalogs.md`|23|

All 33 map; `UNLISTED freeze n=0`. The Core artifacts shell-loop contains `$d`, which this independent parser did not treat as a concrete anchor, so its first concrete anchor is the README citation. This exposes a limit of row-level coverage: it does not check the loop's individual directories. The frozen predicate was not widened.

## Base replay

Command (cwd scratch clone): `python3 plans/round77_c1_declared_surfaces.py --lane . --rev 07c97fcd`, rc **1**:

```text
PROVINCE_REV 07c97fcd
LANE_TIP 07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59
WORKTREE clean
CANONICAL source=none rows=0
SURFACES total=0 present=0 absent=0 remote=0
UNLISTED n=33
RESOLVED live=0
AGREE agree=0 disagree=0
DEFECTS n=34
PREDICATE R77-C1 fail
```

There were 33 `DEFECT UNLISTED-SURFACE` lines at the 33 legacy lines listed above plus `DEFECT CANONICAL-MISSING 0`. This independently reproduced the frozen before numbers without trusting or opening the before receipt. Own parser also printed `UNLISTED base n=33 anchored_rows=33`.

## Commands and source retention

Freeze discovery: `git log -1 --format=%H -- plans/round-77-claims.md` in the lane, rc 0, printed `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`.
Clone setup, rc 0:

```sh
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r77/C1ReplayR77/clone && test "$(git -C /fast/scratch/hyaku/kengaku-r77/C1ReplayR77/clone rev-parse --show-toplevel)" = /fast/scratch/hyaku/kengaku-r77/C1ReplayR77/clone && git -C /fast/scratch/hyaku/kengaku-r77/C1ReplayR77/clone checkout --detach 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
```

Only scratch checkout was mutated, as specifically requested by the item. No commit, push, or lane git mutation occurred. Specialized grep searches over frozen `PROVINCE.md` used `^\|` at lines 8–185 and `Declared surfaces|canonical|\|.*\| (path|http|hash|count|cmd|exec|remote|tcp) \|`; returned legacy lines 12–22, 130–139, 174–185 and canonical lines 1023–1050. Counter sections read: lines 1–473, 512–550.

Risks/limits: host evidence is capture-time; :1234 answers 415, not a model-identity assertion. Hash pins here are truncated declarations, although full digests were retained above. Exec rows prove receipt syntax and ancestry, not execution honesty. Remote is declaration-only. Literal TARGET spelling differs as noted. Parent owns landing-tip integration checks. No blockers.

Self-evaluation: accuracy 4 (capture-time evidence only), completeness 4 (freeze replay, not landing tip), clarity 4 (full source increases length), actionability 5 (commands and 33 mappings retained), conciseness 4 (source intentionally retained for replay); mean 4.2. Improvement: parent should use the retained script for its landing-tip replay; do not infer it from this freeze receipt. User agreement is not observed.

## Independent parser source (retained before scratch deletion)

```python
import collections, concurrent.futures, json, os, pathlib, re, shlex, socket, subprocess
L = pathlib.Path('/fast/scratch/hyaku/kengaku-r77/C1ReplayR77/clone')
def run(args):
    p = subprocess.run(args, cwd=L, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()
def table(text, heading):
    active = False
    result = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith('#'):
            if active: break
            active = line.startswith(heading)
            continue
        if active and line.startswith('|'):
            cells = [x.strip() for x in re.split(r'(?<!\\)\|', line)[1:-1]]
            if cells and cells[0] != 'Surface' and not all(re.fullmatch('[- :]*', x) for x in cells):
                result.append((n, cells))
    return result
def expand(s):
    m = re.search(r'\{([^{}]+)\}', s)
    return [s] if m is None else [v for a in m[1].split(',') for v in expand(s[:m.start()]+a+s[m.end():])]
def local(s):
    p = pathlib.Path(os.path.expanduser(s))
    if not p.is_absolute(): p = L / p
    return p
def probe_path(s):
    probes=[]
    for v in expand(s):
        p=local(v)
        rc, out, err=run(['test','-e',str(p)])
        probes.append({'command':shlex.join(['test','-e',str(p)]),'rc':rc})
    return ('present' if all(x['rc']==0 for x in probes) else 'absent'),probes
text=(L/'PROVINCE.md').read_text()
rows=table(text,'## Declared surfaces')
def probe(item):
    i,(line,c)=item
    name,kind,anchor,decl,sup=c
    tokens=re.findall(r'`([^`]+)`',anchor)
    details=[]
    if kind in ('path','cmd'):
        targets=tokens if kind=='path' else shlex.split(tokens[0])[2:]
        resolved=[probe_path(t) for t in targets]
        verdict='present' if all(v=='present' for v,d in resolved) else 'absent'
        details=[d for v,ds in resolved for d in ds]
    elif kind=='http':
        command=['curl','-s','--max-time','3','-o','/dev/null','-w','%{http_code}',tokens[0]]
        rc,out,err=run(command)
        verdict='present' if out and out!='000' else 'absent'
        details=[{'command':shlex.join(command),'rc':rc,'http':out}]
    elif kind=='remote':
        verdict='remote'
        details=[{'no_egress':True,'dated_marker':bool(re.search(r'REMOTE \d{4}-\d{2}-\d{2}',decl))}]
    elif kind=='tcp':
        host,port=tokens[0].rsplit(':',1)
        try:
            with socket.create_connection((host,int(port)),timeout=3): pass
            verdict='present'; details=[{'socket':tokens[0],'connected':True}]
        except OSError as e:
            verdict='absent'; details=[{'socket':tokens[0],'error':str(e)}]
    elif kind=='hash':
        command=['sha256sum',str(local(tokens[0]))]
        rc,out,err=run(command)
        digest=out.split()[0] if out else ''
        pin=re.search(r'sha256=([^ ]+)',decl)[1]
        halves=re.split('…|\\.\\.\\.',pin)
        ok=bool(digest) and digest.startswith(halves[0]) and (len(halves)==1 or digest.endswith(halves[1]))
        verdict='present' if ok else 'hashdrift'
        details=[{'command':shlex.join(command),'rc':rc,'digest':digest,'pin':pin}]
    elif kind=='count':
        command=['grep','-cE',r'^\|[[:blank:]]*S[0-9]{3,}[[:blank:]]*\|',str(local(tokens[0]))]
        rc,out,err=run(command)
        want=re.search(r'rows=(\d+)',decl)[1]
        verdict='present' if out==want else 'countdrift'
        details=[{'command':shlex.join(command),'rc':rc,'rows':out,'pin':want}]
    elif kind=='exec':
        v,paths=probe_path(tokens[0]); details.extend(paths)
        receipt=re.search(r'receipt=([^ ]+)',decl)[1]
        want=re.search(r'exit=(\d+)',decl)[1]
        data=(L/receipt).read_text()
        tip=re.search(r'LANE_TIP ([0-9a-f]+)',data)[1]
        command=['git','merge-base','--is-ancestor',tip,'HEAD']
        rc,out,err=run(command)
        exit_ok=bool(re.search(r'(?:exit |rc=)'+want+r'\b',data))
        verdict='present' if v=='present' and rc==0 and exit_ok else 'execunverified'
        details.append({'receipt':receipt,'tip':tip,'exit_literal':exit_ok,'command':shlex.join(command),'rc':rc})
    return {'row':i,'line':line,'name':name,'kind':kind,'anchor':anchor,'verdict':verdict,'details':details}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(probe,enumerate(rows,1)))
for r in results: print('ROW '+json.dumps(r,ensure_ascii=False))
counts=collections.Counter(r['verdict'] for r in results)
print('SURFACES total=%d present=%d absent=%d remote=%d'%(len(rows),counts['present'],counts['absent'],counts['remote']))
# Independently enumerate the first concrete anchor in each older row. Ignore shell variables,
# then normalize directory ancestry and corpus-relative citation spellings.
def anchors(cell):
    found=[]
    for span in re.findall(r'`([^`]+)`',cell):
        for word in shlex.split(span):
            word=word.strip("'\",;()")
            if '$' in word: continue
            if word.startswith(('~/','/','http://','https://','corpus/','plans/','knowledge/','evidence/')) or re.fullmatch(r'[\w.-]+\.(?:py|md|sh|jsonl|txt)',word) or re.fullmatch(r'[\d.]+:\d+',word): found.append(word)
    return found
def normalized(s):
    s=s.split('{')[0].rstrip('/')
    if s.startswith('corpus/'): s=s[7:]
    return s
def carries(a,b):
    a,b=normalized(a),normalized(b)
    return a==b or a.startswith(b+'/') or b.startswith(a+'/')
canonical=[(i,token) for i,(_,c) in enumerate(rows,1) for token in anchors(c[2])]
for rev,content in [('freeze',text),('base',run(['git','show','07c97fcd:PROVINCE.md'])[1])]:
    missing=0; total=0
    for heading in ['## Surfaces','### Core','### Historical']:
        entries=table(content,heading)
        print('LEGACY_TABLE '+rev+' '+heading+' rows='+str(len(entries)))
        for line,c in entries:
            tokens=[a for cell in c for a in anchors(cell)]
            anchor=tokens[0] if tokens else None
            matches=[i for i,t in canonical if anchor and carries(t,anchor)] if rev=='freeze' else []
            if anchor: total+=1; missing+=not bool(matches)
            print('LEGACY '+json.dumps({'rev':rev,'heading':heading,'line':line,'name':c[0],'anchor':anchor,'canonical_rows':matches},ensure_ascii=False))
    print('UNLISTED '+rev+' n='+str(missing)+' anchored_rows='+str(total))
rc,out,err=run(['python3','plans/round77_c1_declared_surfaces.py','--lane','.'])
print('COUNTER_RC',rc)
print(out)
actual={int(m[1]):m[2] for m in re.finditer(r'^SURFACE (\d+) (\w+) ',out,re.M)}
disagreements=[{'row':r['row'],'name':r['name'],'own':r['verdict'],'counter':actual.get(r['row'])} for r in results if actual.get(r['row'])!=r['verdict']]
print('DISAGREEMENTS '+json.dumps(disagreements))
print('INDEPENDENT_EXIT 0')

```

Cleanup executed: `rm -rf /fast/scratch/hyaku/kengaku-r77/C1ReplayR77 && test ! -e /fast/scratch/hyaku/kengaku-r77/C1ReplayR77`, rc 0. Scratch tree removed; parser source retained above.
