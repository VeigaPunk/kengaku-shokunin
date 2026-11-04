# RemintKlOpenSSLProteinR80 — independent located-replay audit

## Scope and verdict

Axes: **coverage** and **calibration**. All three assigned receipts reproduce at measured master **6669fe72e59718acc1a0f32a92849a544b0b2f1c**. Freeze: **af51132d8919cedd14d3d3407ae5abc966d5d427**. The measured tip is the integration commit, not the freeze. No lane implementation files were changed; only this exclusive advisory report is delivered.

| Member | Probe rc | Entire block equals stdout minus REV | Block lines | Cases / mismatches | Historical observation lines |
|---|---:|---|---:|---|---|
| distribution-search | 0 | yes | 14 | 12 / 0 | 14 → 14, unchanged |
| openssl-selfsigned-cert | 0 | yes | 14 | 12 / 0 | 16 → 14, disclosed divergence |
| protein-assembly | 0 | yes | 21 | 18 / 0 | 19 → 19, unchanged |

For each receipt: first-line subject correct; exactly one population member named when independently matching against all 88 base-ledger member names; MEMBER correct; receipt/source/tool tracked; SOURCE_SHA and TOOL_SHA recomputed and equal; frozen source/tool paths correct; stamped LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235 is an ancestor of the measured tip (three merge-base rc=0); WORKTREE clean and EXIT 0 stamped; command names the frozen instrument. Ledger rows name the correct receipt, executed, tb2-header, round=80; verdict is predicate/predicate/cases respectively. Exact hashes, ledger bytes and outputs are retained below.

## OpenSSL divergence: fully disclosed, not a silent historical pass

The fresh run does **not** reproduce six historical observation lines:

```text
MISMATCH perm-loose test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
CASE perm-loose predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
MISMATCH key-1024 test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
CASE key-1024 predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
cases=12 legs=72 mismatches=2 setup=0 predicted_u=0
PREDICATE R59-C1 fail
```

There are four replacement/new lines: the two CASE predictions now equal the unchanged observed P/F/P/P/P/P vectors, mismatches becomes 0, and predicate becomes pass. Thus 6 removed + 4 added = **10 symmetric-difference lines**, not ten missing historical lines. The receipt's `HISTORICAL-DIVERGENCE 10` and its explanatory **14 new versus 16 historical observation lines** are all true. The historical failure receipt remains tracked with its exact SHA; the new block equals fresh stdout. This divergence is **fully disclosed** and does not make this receipt dishonest. The retained real `diff -u` exits 1 because the two inputs intentionally differ; this is the only nonzero audit subprocess, not an instrument failure.

## Method, setup and limits

Read the frozen claims and frozen probe table; used fresh scratch paths and the exact frozen argv. Protein used the required `uv run --no-project --with biopython python3` prefix. Three subprocesses ran concurrently inside the exclusive scratch tree; no agents were spawned. TMPDIR, uv cache, and bytecode behavior were scoped to scratch. The auditor is independent of the round-80 counter: no counter pass is assumed or reported.

One `git clone --shared --quiet` was issued into the exclusive scratch `lane` directory. Subsequently explicitly initialized the scratch repository, set its object alternates to the lane object store, asserted its top-level path, and checked out the measured commit detached. No second clone, full clone, commit, source-repository git mutation, build tree, formatter, linter, or unrelated gate was run. Initial named setup returned rc=0 but did not retain command stdout in the tool transcript; only the explicit checkout and clean worktree output below support the measured state. The later explicit scratch checkout used:

```sh
test "$(git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane rev-parse --show-toplevel)" = /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane && git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane checkout --detach 6669fe72e59718acc1a0f32a92849a544b0b2f1c && git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane status --porcelain && git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane rev-parse HEAD
```

```text
HEAD is now at 6669fe72 round-80: integration — six located replays minted and the ledger flipped (R80-C1), V1-V6 routed rows plus the V1 receipt and corrections (R80-C2), S258, lesson, index, wave spec/dispatch
6669fe72e59718acc1a0f32a92849a544b0b2f1c
exit 0
```

Tool updates/installs: none. The required uv invocation downloaded and installed **Biopython 1.88** and its dependency **NumPy 2.5.4** only in the disposable scratch uv cache (versions from its dist-info metadata names; Biopython version also printed by probe). Channel: uv package resolution; reason: frozen protein probe runtime. Cache and packages were removed with scratch. No pacman or PATH-directory writes.

No supported LSP tool is mounted; no symbol refactor was required. Scope does not establish the other three members, the whole population gate, or R80-C2 closure. It cannot retrospectively prove the original mint's clean worktree; it independently demonstrates a clean measured checkout and reproducible output. No receipt dishonesty or stamp defect found in the assigned three. Any later integration tip requires parent-owned final gate execution.

## Exact independent auditor

Executed command, exit 0:

```sh
python3 /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/audit.py
```

```python
import concurrent.futures, difflib, hashlib, json, os, pathlib, re, shlex, subprocess
S = pathlib.Path('/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80')
L = S / 'lane'
TIP = '6669fe72e59718acc1a0f32a92849a544b0b2f1c'
MEMBERS = ['distribution-search', 'openssl-selfsigned-cert', 'protein-assembly']
log = []
def emit(s):
    print(s, flush=True)
    log.append(s)
def run(cmd, cwd=L, env=None, timeout=300):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    return p
emit('AXES coverage; calibration (independent replay, stamp and historical-divergence audit only)')
for cmd in [['git','-C',str(L),'rev-parse','HEAD'], ['git','-C',str(L),'status','--porcelain']]:
    p=run(cmd); emit('$ '+shlex.join(cmd)+'\n'+p.stdout+p.stderr+'RC '+str(p.returncode))
table=json.loads((L/'plans/round80_probes.json').read_text())['members']
base=json.loads(run(['git','-C',str(L),'show','dce7c275381c669e6489f1b795b1505d0824c262:plans/grader-population-ledger.json']).stdout)['members']
ledger=json.loads((L/'plans/grader-population-ledger.json').read_text())['members']
tracked=set(run(['git','-C',str(L),'ls-files']).stdout.splitlines())
obsrx=re.compile(r'^(?:CASE |case=|cases=|MISMATCH |OBSERVED-U |VECTOR |PREDICATE R\d+-C\d+ (?:pass|fail))')
def observations(t): return [x for x in t.splitlines() if obsrx.match(x)]
def replay(m):
    spec=table[m]
    work=S/(m+'.work'); work.mkdir()
    out=S/(m+'.out.txt')
    cmd=spec.get('prefix',['python3'])+[spec['tool']]+[a.replace('{work}',str(work)).replace('{out}',str(out)) for a in spec['argv']]
    env=dict(os.environ, TMPDIR=str(S), UV_CACHE_DIR=str(S/'uv-cache'), UV_PYTHON_DOWNLOADS='never', PYTHONDONTWRITEBYTECODE='1')
    try:
        p=run(cmd,env=env,timeout=spec['timeout'])
        return m,cmd,p.stdout,p.stderr,p.returncode
    except subprocess.TimeoutExpired as e:
        return m,cmd,str(e.stdout),str(e.stderr),'TIMEOUT'
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(replay,MEMBERS))
for m,cmd,stdout,stderr,rc in results:
    emit('\n## '+m+'\n$ '+shlex.join(cmd)+'\nCWD '+str(L)+'\nENV TMPDIR='+str(S)+' UV_CACHE_DIR='+str(S/'uv-cache')+' UV_PYTHON_DOWNLOADS=never PYTHONDONTWRITEBYTECODE=1\nSTDOUT\n'+stdout+'STDERR\n'+stderr+'RC '+str(rc))
    rel='corpus/evidence/round80/'+m+'-probe.txt'
    raw=(L/rel).read_text()
    emit('COMMITTED_RECEIPT '+rel+'\n'+raw)
    stamp={line.split(' ',1)[0]:line.split(' ',1)[1] for line in raw.splitlines() if ' ' in line}
    block=raw.split('OBSERVATIONS_BEGIN\n',1)[1].split('OBSERVATIONS_END',1)[0]
    actual='\n'.join(x for x in stdout.splitlines() if not x.startswith('REV '))+'\n'
    emit('BLOCK_EQUAL '+str(block==actual)+' block_lines='+str(len(block.splitlines()))+' replay_lines='+str(len(actual.splitlines())))
    emit(''.join(difflib.unified_diff(block.splitlines(True),actual.splitlines(True),fromfile='committed-block',tofile='fresh-stdout-minus-REV')) or 'BLOCK_DIFF empty')
    for field,sha in [('SOURCE_RECEIPT','SOURCE_SHA'),('TOOL','TOOL_SHA')]:
        path=stamp[field]; digest=hashlib.sha256((L/path).read_bytes()).hexdigest()
        emit('SHA256 '+path+' '+digest+' stamp='+stamp[sha]+' equal='+str(digest==stamp[sha])+' tracked='+str(path in tracked))
    emit('FROZEN_PATHS source='+str(stamp['SOURCE_RECEIPT']==table[m]['historical'])+' tool='+str(stamp['TOOL']==table[m]['tool']))
    emit('SUBJECT '+str(raw.splitlines()[0].startswith('# tb2 '+m+' grader probe'))+' MEMBER_FIELD '+str(stamp['MEMBER']==m)+' RECEIPT_TRACKED '+str(rel in tracked))
    named=[x for x in base if re.search(r'(?<![\w.-])'+re.escape(x)+r'(?![\w.-])',raw)]
    emit('EXACTLY_ONE_MEMBER '+json.dumps(named)+' equal='+str(named==[m])+' universe='+str(len(base)))
    p=run(['git','-C',str(L),'merge-base','--is-ancestor',stamp['LANE_TIP'],TIP])
    emit('$ '+shlex.join(p.args)+'\n'+p.stdout+p.stderr+'RC '+str(p.returncode))
    emit('STAMP WORKTREE='+stamp['WORKTREE']+' EXIT='+stamp['EXIT']+' COMMAND='+stamp['COMMAND'])
    emit('LEDGER '+json.dumps(ledger[m],sort_keys=True))
    hist=(L/table[m]['historical']).read_text()
    hobs=observations(hist); nobs=observations(actual)
    removed=[x for x in hobs if x not in nobs]; added=[x for x in nobs if x not in hobs]
    emit('HISTORICAL_OBSERVATIONS old='+str(len(hobs))+' new='+str(len(nobs))+' removed='+str(len(removed))+' added='+str(len(added))+' symmetric_difference='+str(len(set(hobs)^set(nobs))))
    if m=='openssl-selfsigned-cert':
        hp=S/'openssl-historical.observations.txt'; np=S/'openssl-fresh.observations.txt'
        hp.write_text('\n'.join(hobs)+'\n'); np.write_text('\n'.join(nobs)+'\n')
        p=run(['diff','-u',str(hp),str(np)])
        emit('$ '+shlex.join(p.args)+'\n'+p.stdout+p.stderr+'RC '+str(p.returncode)+' (1 means expected differences)')
        emit('REMOVED_HISTORICAL_LINES\n'+'\n'.join(removed))
        emit('DIVERGENCE_NOTE '+stamp.get('HISTORICAL-DIVERGENCE','ABSENT'))
        emit('DIVERGENCE_COUNT_EQUAL '+str(int(stamp['HISTORICAL-DIVERGENCE'].split()[0])==len(set(hobs)^set(nobs))))
(S/'audit-output.txt').write_text('\n'.join(log)+'\n')

```

## Exact retained output

```text
AXES coverage; calibration (independent replay, stamp and historical-divergence audit only)
$ git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane rev-parse HEAD
6669fe72e59718acc1a0f32a92849a544b0b2f1c
RC 0
$ git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane status --porcelain
RC 0

## distribution-search
$ python3 plans/round58_c2_kl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/distribution-search.work --receipt /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/distribution-search.out.txt
CWD /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane
ENV TMPDIR=/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80 UV_CACHE_DIR=/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/uv-cache UV_PYTHON_DOWNLOADS=never PYTHONDONTWRITEBYTECODE=1
STDOUT
REV 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CASE sol predicted=P/P/P/P observed=P/P/P/P ok
CASE uniform predicted=P/P/P/F observed=P/P/P/F ok
CASE kb-only-m7 predicted=P/P/P/F observed=P/P/P/F ok
CASE minzero predicted=P/P/F/F observed=P/P/F/F ok
CASE negatom predicted=P/P/F/F observed=P/P/F/F ok
CASE nanatom predicted=P/P/F/F observed=P/P/F/F ok
CASE sumdrift predicted=P/P/F/P observed=P/P/F/P ok
CASE wrongvocab-m5 predicted=P/F/P/F observed=P/F/P/F ok
CASE twod predicted=P/F/P/P observed=P/F/P/P ok
CASE maxover predicted=P/P/F/F observed=P/P/F/F ok
CASE tolbnd predicted=P/P/P/P observed=P/P/P/P ok
CASE intcounts predicted=P/P/F/P observed=P/P/F/P ok
cases=12 legs=48 mismatches=0 setup=0 predicted_u=0
PREDICATE R58-C3 pass
STDERR
RC 0
COMMITTED_RECEIPT corpus/evidence/round80/distribution-search-probe.txt
# tb2 distribution-search grader probe (round 80 re-mint)
MEMBER distribution-search
SOURCE_RECEIPT corpus/evidence/round58/kl-probe.txt
SOURCE_SHA 3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f
TOOL plans/round58_c2_kl_probe.py
TOOL_SHA 51c192f2f98186acb439cb69c2e0370860c362e3bdcb267afea93cd547fa6760
LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235
WORKTREE clean
COMMAND /usr/bin/python3 plans/round58_c2_kl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/remint-work/distribution-search.work --receipt /fast/scratch/hyaku/kengaku-r80/remint-work/distribution-search.out.txt
EXIT 0
MINTED_BY plans/round80_c1_remint.py
OBSERVATIONS_BEGIN
CASE sol predicted=P/P/P/P observed=P/P/P/P ok
CASE uniform predicted=P/P/P/F observed=P/P/P/F ok
CASE kb-only-m7 predicted=P/P/P/F observed=P/P/P/F ok
CASE minzero predicted=P/P/F/F observed=P/P/F/F ok
CASE negatom predicted=P/P/F/F observed=P/P/F/F ok
CASE nanatom predicted=P/P/F/F observed=P/P/F/F ok
CASE sumdrift predicted=P/P/F/P observed=P/P/F/P ok
CASE wrongvocab-m5 predicted=P/F/P/F observed=P/F/P/F ok
CASE twod predicted=P/F/P/P observed=P/F/P/P ok
CASE maxover predicted=P/P/F/F observed=P/P/F/F ok
CASE tolbnd predicted=P/P/P/P observed=P/P/P/P ok
CASE intcounts predicted=P/P/F/P observed=P/P/F/P ok
cases=12 legs=48 mismatches=0 setup=0 predicted_u=0
PREDICATE R58-C3 pass
OBSERVATIONS_END

BLOCK_EQUAL True block_lines=14 replay_lines=14
BLOCK_DIFF empty
SHA256 corpus/evidence/round58/kl-probe.txt 3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f stamp=3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f equal=True tracked=True
SHA256 plans/round58_c2_kl_probe.py 51c192f2f98186acb439cb69c2e0370860c362e3bdcb267afea93cd547fa6760 stamp=51c192f2f98186acb439cb69c2e0370860c362e3bdcb267afea93cd547fa6760 equal=True tracked=True
FROZEN_PATHS source=True tool=True
SUBJECT True MEMBER_FIELD True RECEIPT_TRACKED True
EXACTLY_ONE_MEMBER ["distribution-search"] equal=True universe=88
$ git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane merge-base --is-ancestor 6250e94b2adaff8cd22d32f7ab45024f092e3235 6669fe72e59718acc1a0f32a92849a544b0b2f1c
RC 0
STAMP WORKTREE=clean EXIT=0 COMMAND=/usr/bin/python3 plans/round58_c2_kl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/remint-work/distribution-search.work --receipt /fast/scratch/hyaku/kengaku-r80/remint-work/distribution-search.out.txt
LEDGER {"classes": ["numeric-band"], "receipt": "corpus/evidence/round80/distribution-search-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}
HISTORICAL_OBSERVATIONS old=14 new=14 removed=0 added=0 symmetric_difference=0

## openssl-selfsigned-cert
$ python3 plans/round59_c1_openssl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/openssl-selfsigned-cert.work --receipt /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/openssl-selfsigned-cert.out.txt
CWD /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane
ENV TMPDIR=/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80 UV_CACHE_DIR=/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/uv-cache UV_PYTHON_DOWNLOADS=never PYTHONDONTWRITEBYTECODE=1
STDOUT
REV 6669fe72e59718acc1a0f32a92849a544b0b2f1c
CASE sol predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE perm-loose predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
CASE key-1024 predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
CASE days-30 predicted=P/P/F/P/P/P observed=P/P/F/P/P/P ok
CASE cn-wrong predicted=P/P/F/P/F/F observed=P/P/F/P/F/F ok
CASE pem-keyonly predicted=P/P/P/F/P/P observed=P/P/P/F/P/P ok
CASE pem-garbage predicted=P/P/P/F/P/P observed=P/P/P/F/P/P ok
CASE fp-absent predicted=P/P/P/P/F/P observed=P/P/P/P/F/P ok
CASE script-silent predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE dir-absent predicted=F/F/F/F/F/F observed=F/F/F/F/F/F ok
CASE org-upper predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE script-missing predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
cases=12 legs=72 mismatches=0 setup=0 predicted_u=0
PREDICATE R59-C1 pass
STDERR
RC 0
COMMITTED_RECEIPT corpus/evidence/round80/openssl-selfsigned-cert-probe.txt
# tb2 openssl-selfsigned-cert grader probe (round 80 re-mint)
MEMBER openssl-selfsigned-cert
SOURCE_RECEIPT corpus/evidence/round59/openssl-probe.txt
SOURCE_SHA ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094
TOOL plans/round59_c1_openssl_probe.py
TOOL_SHA 6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646
LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235
WORKTREE clean
COMMAND /usr/bin/python3 plans/round59_c1_openssl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/remint-work/openssl-selfsigned-cert.work --receipt /fast/scratch/hyaku/kengaku-r80/remint-work/openssl-selfsigned-cert.out.txt
EXIT 0
MINTED_BY plans/round80_c1_remint.py
HISTORICAL-DIVERGENCE 10 the tip's instrument produces 14 observation lines where the historical receipt has 16; historical receipt kept, sha stamped
OBSERVATIONS_BEGIN
CASE sol predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE perm-loose predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
CASE key-1024 predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
CASE days-30 predicted=P/P/F/P/P/P observed=P/P/F/P/P/P ok
CASE cn-wrong predicted=P/P/F/P/F/F observed=P/P/F/P/F/F ok
CASE pem-keyonly predicted=P/P/P/F/P/P observed=P/P/P/F/P/P ok
CASE pem-garbage predicted=P/P/P/F/P/P observed=P/P/P/F/P/P ok
CASE fp-absent predicted=P/P/P/P/F/P observed=P/P/P/P/F/P ok
CASE script-silent predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
CASE dir-absent predicted=F/F/F/F/F/F observed=F/F/F/F/F/F ok
CASE org-upper predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
CASE script-missing predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
cases=12 legs=72 mismatches=0 setup=0 predicted_u=0
PREDICATE R59-C1 pass
OBSERVATIONS_END

BLOCK_EQUAL True block_lines=14 replay_lines=14
BLOCK_DIFF empty
SHA256 corpus/evidence/round59/openssl-probe.txt ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094 stamp=ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094 equal=True tracked=True
SHA256 plans/round59_c1_openssl_probe.py 6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646 stamp=6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646 equal=True tracked=True
FROZEN_PATHS source=True tool=True
SUBJECT True MEMBER_FIELD True RECEIPT_TRACKED True
EXACTLY_ONE_MEMBER ["openssl-selfsigned-cert"] equal=True universe=88
$ git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane merge-base --is-ancestor 6250e94b2adaff8cd22d32f7ab45024f092e3235 6669fe72e59718acc1a0f32a92849a544b0b2f1c
RC 0
STAMP WORKTREE=clean EXIT=0 COMMAND=/usr/bin/python3 plans/round59_c1_openssl_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/remint-work/openssl-selfsigned-cert.work --receipt /fast/scratch/hyaku/kengaku-r80/remint-work/openssl-selfsigned-cert.out.txt
LEDGER {"classes": ["crypto-credential", "file-artifact", "filesystem-metadata", "stdout-inspection", "subprocess-exec"], "receipt": "corpus/evidence/round80/openssl-selfsigned-cert-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}
HISTORICAL_OBSERVATIONS old=16 new=14 removed=6 added=4 symmetric_difference=10
$ diff -u /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/openssl-historical.observations.txt /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/openssl-fresh.observations.txt
--- /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/openssl-historical.observations.txt	2026-11-04 04:33:59.167780522 -0300
+++ /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/openssl-fresh.observations.txt	2026-11-04 04:33:59.167810782 -0300
@@ -1,8 +1,6 @@
 CASE sol predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
-MISMATCH perm-loose test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
-CASE perm-loose predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
-MISMATCH key-1024 test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
-CASE key-1024 predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
+CASE perm-loose predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
+CASE key-1024 predicted=P/F/P/P/P/P observed=P/F/P/P/P/P ok
 CASE days-30 predicted=P/P/F/P/P/P observed=P/P/F/P/P/P ok
 CASE cn-wrong predicted=P/P/F/P/F/F observed=P/P/F/P/F/F ok
 CASE pem-keyonly predicted=P/P/P/F/P/P observed=P/P/P/F/P/P ok
@@ -12,5 +10,5 @@
 CASE dir-absent predicted=F/F/F/F/F/F observed=F/F/F/F/F/F ok
 CASE org-upper predicted=P/P/P/P/P/P observed=P/P/P/P/P/P ok
 CASE script-missing predicted=P/P/P/P/P/F observed=P/P/P/P/P/F ok
-cases=12 legs=72 mismatches=2 setup=0 predicted_u=0
-PREDICATE R59-C1 fail
+cases=12 legs=72 mismatches=0 setup=0 predicted_u=0
+PREDICATE R59-C1 pass
RC 1 (1 means expected differences)
REMOVED_HISTORICAL_LINES
MISMATCH perm-loose test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
CASE perm-loose predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
MISMATCH key-1024 test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
CASE key-1024 predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
cases=12 legs=72 mismatches=2 setup=0 predicted_u=0
PREDICATE R59-C1 fail
DIVERGENCE_NOTE 10 the tip's instrument produces 14 observation lines where the historical receipt has 16; historical receipt kept, sha stamped
DIVERGENCE_COUNT_EQUAL True

## protein-assembly
$ uv run --no-project --with biopython python3 plans/tb2_grader_probe.py --lane .
CWD /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane
ENV TMPDIR=/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80 UV_CACHE_DIR=/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/uv-cache UV_PYTHON_DOWNLOADS=never PYTHONDONTWRITEBYTECODE=1
STDOUT
grader=corpus/evidence/round35/tb2-eval/test_outputs.py sha256=44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 biopython=1.88
components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000
case=valid-balanced predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'
case=uppercase predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence (case is not specified)'
case=no-trailing-newline predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence'
case=trailing-empty-line predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Invalid number of lines in gblock.txt.' requirement='No empty lines'
case=start-codon-prefixed predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no start codon / remove N-terminal Met'
case=stop-codon-appended predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no stop codon'
case=linker-4aa predicted=fail observed=fail match=yes nt=2583 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-21aa predicted=fail observed=fail match=yes nt=2634 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-20aa predicted=pass observed=pass match=yes nt=2631 gcwin=ok assertion='-' requirement='linkers 5..20 aa (upper bound inclusive)'
case=linker-non-gs predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Linker must only contain G and S amino acids.' requirement='only GS linkers between subproteins'
case=linker-g-only predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='GS linkers (a G-only linker is not distinguished)'
case=n-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no GS linker on the N terminus'
case=c-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no GS linker on the C terminus'
case=donor-acceptor-swapped predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='subprotein order'
case=donor-one-substitution predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='donor matches its PDB sequence'
case=donor-repeated predicted=fail observed=fail match=yes nt=3378 gcwin=ok assertion='gBlock must be at most 3000 nucleotides.' requirement='do not repeat a protein'
case=non-acgt-base predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='gBlock must contain only A, T, C, G.' requirement='gBlock is a DNA sequence'
case=gc-window-high predicted=fail observed=fail match=yes nt=2586 gcwin=violated assertion='GC content must be between 30 and 70% in all 50 nucleotide windows.' requirement='GC 30..70% in every 50-nt window'
cases=18 observed_pass=5 observed_fail=13 mismatches=0
STDERR
Downloading numpy (15.9MiB)
Downloading biopython (3.1MiB)
 Downloaded biopython
 Downloaded numpy
Installed 2 packages in 178ms
RC 0
COMMITTED_RECEIPT corpus/evidence/round80/protein-assembly-probe.txt
# tb2 protein-assembly grader probe (round 80 re-mint)
MEMBER protein-assembly
SOURCE_RECEIPT corpus/evidence/round35/tb2-grader-probe.txt
SOURCE_SHA 2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8
TOOL plans/tb2_grader_probe.py
TOOL_SHA acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0
LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235
WORKTREE clean
COMMAND uv run --no-project --with biopython python3 plans/tb2_grader_probe.py --lane .
EXIT 0
MINTED_BY plans/round80_c1_remint.py
OBSERVATIONS_BEGIN
grader=corpus/evidence/round35/tb2-eval/test_outputs.py sha256=44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 biopython=1.88
components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000
case=valid-balanced predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'
case=uppercase predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence (case is not specified)'
case=no-trailing-newline predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence'
case=trailing-empty-line predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Invalid number of lines in gblock.txt.' requirement='No empty lines'
case=start-codon-prefixed predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no start codon / remove N-terminal Met'
case=stop-codon-appended predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no stop codon'
case=linker-4aa predicted=fail observed=fail match=yes nt=2583 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-21aa predicted=fail observed=fail match=yes nt=2634 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-20aa predicted=pass observed=pass match=yes nt=2631 gcwin=ok assertion='-' requirement='linkers 5..20 aa (upper bound inclusive)'
case=linker-non-gs predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Linker must only contain G and S amino acids.' requirement='only GS linkers between subproteins'
case=linker-g-only predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='GS linkers (a G-only linker is not distinguished)'
case=n-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no GS linker on the N terminus'
case=c-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no GS linker on the C terminus'
case=donor-acceptor-swapped predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='subprotein order'
case=donor-one-substitution predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='donor matches its PDB sequence'
case=donor-repeated predicted=fail observed=fail match=yes nt=3378 gcwin=ok assertion='gBlock must be at most 3000 nucleotides.' requirement='do not repeat a protein'
case=non-acgt-base predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='gBlock must contain only A, T, C, G.' requirement='gBlock is a DNA sequence'
case=gc-window-high predicted=fail observed=fail match=yes nt=2586 gcwin=violated assertion='GC content must be between 30 and 70% in all 50 nucleotide windows.' requirement='GC 30..70% in every 50-nt window'
cases=18 observed_pass=5 observed_fail=13 mismatches=0
OBSERVATIONS_END

BLOCK_EQUAL True block_lines=21 replay_lines=21
BLOCK_DIFF empty
SHA256 corpus/evidence/round35/tb2-grader-probe.txt 2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8 stamp=2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8 equal=True tracked=True
SHA256 plans/tb2_grader_probe.py acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0 stamp=acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0 equal=True tracked=True
FROZEN_PATHS source=True tool=True
SUBJECT True MEMBER_FIELD True RECEIPT_TRACKED True
EXACTLY_ONE_MEMBER ["protein-assembly"] equal=True universe=88
$ git -C /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80/lane merge-base --is-ancestor 6250e94b2adaff8cd22d32f7ab45024f092e3235 6669fe72e59718acc1a0f32a92849a544b0b2f1c
RC 0
STAMP WORKTREE=clean EXIT=0 COMMAND=uv run --no-project --with biopython python3 plans/tb2_grader_probe.py --lane .
LEDGER {"classes": ["file-artifact"], "receipt": "corpus/evidence/round80/protein-assembly-probe.txt", "round": 80, "status": "executed", "subject": "tb2-header", "verdict": "cases"}
HISTORICAL_OBSERVATIONS old=19 new=19 removed=0 added=0 symmetric_difference=0

```

## Cleanup

Executed a dedicated shell so its EXIT trap actually ran (a trap installed only in a persistent tool shell does not immediately execute):

```sh
bash -c 'S=/fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80; trap '\''rm -rf -- "$S"; printf "SCRATCH_REMOVED %s\n" "$S"'\'' EXIT'
```

```text
SCRATCH_REMOVED /fast/scratch/hyaku/kengaku-r80/RemintKlOpenSSLProteinR80
exit 0
```

The scratch auditor, clone/worktree, observation files, uv cache and raw output were removed. Their substantive evidence is embedded above; no surviving scratch path is relied on as citable evidence.

## Self-evaluation

Accuracy 4/5: exact stdout, hashes and real diff retained; original mint cleanliness is necessarily unproven. Completeness 4/5: assigned replays and stamps covered; initial named clone setup stdout was unavailable and later explicit checkout evidence substitutes for it. Clarity 4/5: six historical removals are distinguished from ten symmetric-difference lines; full transcript is intentionally long. Actionability 4/5: parent has exact tip, commands and results, but must own integration gates. Conciseness 4/5: raw receipt/output duplication retained to satisfy exact-evidence requirement. Overall 4.0/5. Improvement: retain setup stdout directly rather than using a named command; current report explicitly bounds that evidence. Would the user agree? Likely: findings are scoped and reproducible rather than counter-derived.
