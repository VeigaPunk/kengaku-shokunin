# C2CriticR73 — R73-C2 adversarial review

Axes: coverage and calibration. This is a critic finding, not canonical admission or a landing-tip judgment. No predicates, counters, targets, or lane source files were deliberately edited.

Stable test subject: `git archive d96c3e62` extracted under the assigned scratch tree, with the frozen `plans/round73_c2_registry_audit.py` copied in. All mutation experiments altered only this scratch mirror. The green control appends “failed for non-zero refusal codes” to the existing `sources-adopt` verdict map and changes `round62-c1-class-survey` kind to `gate`; it changes no counting rule. Every audit invocation below is the assigned instrument's `--lane .`, not an alternate counter. Raw exit codes were captured with `subprocess.run`, without a pipeline.

## 1. Weakening can satisfy the complete 106-row green output

Counterexamples, each independently applied to the green control:

| Mutation | rc | MISMATCH | Leg result |
|---|---:|---:|---|
| Delete `hermetic-grader` pin cell entirely | 1 | 2 | D2 rejects, reporting the same empty-pin defect twice |
| Replace all its real pin content with `x` | 0 | 0 | D1–D4 accept |
| Replace its verdict map with `failed` alone | 1 | 1 | D2 rejects missing backticked zero |
| Replace its detailed verdict map with `` `0` failed `` | 0 | 0 | D1–D4 accept; refusal/setup code semantics disappear |
| Replace `sources-adopt` map with `` `0` clean · never fails `` | 0 | 0 | D2 accepts the negated substring `fail` |
| Rename `round62-c1-class-survey` to `unrelated-identity` | 0 | 0 | D3 checks uniqueness, not identity; all legs accept |

Evidence: `price_row` uses non-emptiness for pins/scope, substring membership for failure language, and does not bind a row name to its script or history. These are measured declaration-shape checks, not validation of pin content or verdict semantics. The rename preserves the script and denominator, so even a literal `106` target comparison cannot detect it.

Impacted axes: calibration (degraded declarations certified green), coverage (identity continuity is unpriced). Smallest safe correction: retain the actual pin and detailed verdict declarations in the landing rows; report these semantic limits explicitly. Stronger semantic/identity checks require a future frozen contract, not an in-round counter change. Merely appending a failure word can improve the score without improving the declaration.

## 2. Parsing is genuine syntax checking, not runnable-entry validation

Exact advertised entry in the real `sources-adopt` row:

```text
python3 plans/sources_adopt.py --lane .
rc=2
sources_adopt.py: error: unrecognized arguments: --lane .
```

The same corrected mirror still reports `PARSED scripts=106 failed=0`, D1–D4 zero, `MISMATCH 0`, rc 0. Its `--help` works; that does not validate the row's advertised flags.

The requested help counterexample is the real `stage-scan` row:

```text
python3 plans/stage_scan.py --help
rc=2
ERROR unknown option --help
```

The initial battery ran `python3 <entry-script> --help` for all 106 parsed rows, with a 20-second per-script timeout: 106 tested, one nonzero (`stage-scan`). Crucial distinction: `stage-scan` lacks a conventional help interface; that alone does NOT prove its bare registered command is broken. `sources-adopt --lane .` proves an actual advertised entry is broken. No audit leg executes entry commands or checks their flags; `ast.parse` cannot establish those properties.

Impacted axis: calibration. Smallest safe correction: correct the `sources-adopt` entry to implemented invocation syntax, and disclose that D1 proves only existence/syntax. Do not add unbounded execution of all instruments as a purported harmless fix. Runtime validity is outside the frozen D1 promise; this is a limitation, not by itself a failure of the explicit syntax-only rule.

## 3. D4 accepts false binding when both revisions occur in each item

Ordinary swapped items are rejected: D4 has two defects, `MISMATCH 2`, rc 1. But this semantically swapped text passes D4 and every other leg, with the complete 106-row target output and rc 0:

```text
1. `Do-nothing control (committed at freeze)` landed with `d8a77d3f`; unrelated comparison `c80fcdb3`.
2. `Red-before (committed at freeze)` landed with `c80fcdb3`; unrelated comparison `d8a77d3f`.
```

So does explicitly denying each correct binding:

```text
1. `Do-nothing control (committed at freeze)` belongs to `d8a77d3f`, NOT `c80fcdb3`.
2. `Red-before (committed at freeze)` belongs to `c80fcdb3`, NOT `d8a77d3f`.
```

A third, contradictory numbered item is also ignored once the first item quoting its label has the required revision. Evidence: `check_errata` tests only `revision not in items[owners[0]]`; it establishes substring co-occurrence in the first matching item, not the asserted relation, polarity, exclusivity, or every item's correctness.

Impacted axis: calibration. Smallest safe correction now: preserve accurate erratum prose and declare D4's containment limitation; do not claim semantic per-item binding. A future contract could use explicit structured label→revision fields while allowing historical comparison revisions in separate prose. Simply forbidding both hashes would wrongly reject the existing correct first item, which legitimately explains both revisions.

## 4. The base block declares 107 rows; the audit silently retains 106

Independent derivation from the immutable base `SKILL.md` registry block:

```text
table lines=109
non-header/separator row lines=107
parsed rows=106
malformed rows=1
retained rows without entry script=0
unique retained scripts=106
shared-script excess=0
```

The omitted real row is base `SKILL.md:688`, named `round66_c1_tensor_probe`. It has five cells, rather than eight. The driver transcript below preserves its entire source line. This is not a duplicate-script issue and none of the 106 retained rows lacks a recognizable entry script: the loss happens earlier, at `parse_rows`'s unconditional `if len(cells) != 8: continue`.

Strongest counterexample: give that already-dropped real row `kind=invalid-kind` on the otherwise-green mirror. Output remains `INSTRUMENTS total=106 derived=registry rows=106`, `PARSED scripts=106 failed=0`, D1–D4 zero, `MISMATCH 0`, `PREDICATE R73-C2 pass`, rc 0. Thus a malformed/defective existing row is excluded before the supposed eight-field pricing. The printed 106 is the honest retained-script count, NOT an honest count of all registry declarations. The claim “keeps every row” is falsified.

The older gate separately reports 105 indexed scripts and 107 rows: its regex misses the hyphenated directory in `corpus/evidence/round13-coverage/coverage_census.py`, while its row count includes the table header. These are different measures, not corroborating independent censuses.

Further frozen-contract inconsistency: the claims document requires eight additional parsed registry entries (seven missing instruments, including repair of the dropped round66 row, plus the new audit row), yet freezes the after sentence at `rows=106 scripts=106`. The observed concurrently modified live tree printed 114/114 and `MISMATCH 0`, rc 0. That is an intermediate observation, NOT a landing-tip verdict; the landing tip is for L1 to identify. [INFERENCE] The mandated row work naturally gives 106+8=114, so the literal frozen numerical sentence cannot coexist with that work without changing a frozen requirement. This should be rejected/routed by the canonical judge, not silently normalized by a critic.

Impacted axes: coverage (real registry declaration dropped), calibration (bad kind never priced; denominator understated). Smallest safe correction: repair the malformed row in landing content; in a future instrument fail on malformed table data instead of discarding it. Do not edit the current frozen counter or target. Declare that this round's counter derives only exactly-eight-cell survivors and that its pinned denominator conflicts with the required additions.

R73-C2 falsified

The falsification is of the advertised “keeps every row” and per-item semantic-binding guarantees. The executable audit can still print its exact green predicate on these counterexamples; green output alone is not evidence of those stronger guarantees. Semantic pin/name/run validity limits should have been declared rather than inferred from “prices every row's eight fields.”

## Execution notes and limitations

- No tools installed or upgraded. No git mutations, canonical judge, admissions, integrations, or alternate agent runtime invoked.
- Early shell pipelines printed the pipeline consumer's rc (including misleading `rc=0` for a red audit / failed help command). Those are not used as result evidence. Direct subprocess receipts below establish rc 1 and rc 2 respectively.
- Two exploratory audit modes were attempted with nonexistent `--work` directories; both exited 2 with `SETUP --work must be an existing directory`. They did not run selftests/mutants and are not claimed passed. They are not needed for the assigned counterexamples.
- Process defect: initial scratch setup was issued concurrently with the required first claims read, rather than after that read completed. Subsequent stable experiments used the fully read frozen contract.
- Process defect: early denominator/battery scripts imported the audit through the live lane's plans directory, potentially creating/updating `plans/__pycache__/round73_c2_registry_audit.cpython-314.pyc` outside the allowed write scope. A matching cache file exists, but it is shared and its prior existence/sole authorship is unestablished. No out-of-scope cleanup was attempted. The reproducibility driver below uses `runpy.run_path` instead.
- Scratch content was copied into this evidence/report before cleanup; no `/tmp` files were created by this seat's explicit commands. The 106-help battery ran only in the scratch mirror; arbitrary script-side temporary activity was not independently traced.

## Full direct-exit transcript

```text

### immutable base + frozen audit (unfiltered exit code)
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=1
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 defect n=2
  DEFECT `sources-adopt`:gate-verdict:0,2,3,4,5,6,7,8,9
  DEFECT `round62-c1-class-survey`:kind:census gate
D3 ok n=0
D4 ok n=0
MISMATCH 2
DEFECTS n=2
PREDICATE R73-C2 fail
stderr=

### sanctioned two corrections baseline
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### empty pin rejected
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=1
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 defect n=2
  DEFECT `hermetic-grader`:pinned-values:empty
  DEFECT `hermetic-grader`:pinned-values:empty
D3 ok n=0
D4 ok n=0
MISMATCH 2
DEFECTS n=2
PREDICATE R73-C2 fail
stderr=

### real pin replaced by x
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### one-word verdict rejected
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=1
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 defect n=1
  DEFECT `hermetic-grader`:gate-verdict:none
D3 ok n=0
D4 ok n=0
MISMATCH 1
DEFECTS n=1
PREDICATE R73-C2 fail
stderr=

### verdict reduced to zero plus one word
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### failure negation accepted
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### row renamed without identity reference
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### actual advertised sources-adopt entry
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/sources_adopt.py --lane .
rc=2

stderr=usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY]
                        [--package PACKAGE] [--admit-ids ADMIT_IDS]
                        [--entries ENTRIES] [--access-date ACCESS_DATE]
                        [--recheck RECHECK] [--out OUT]
                        [--quote-file QUOTE_FILE] [--artifact ARTIFACT]
                        [--url-map URL_MAP] [--attest-opened]
                        [--scope-to-admit]
sources_adopt.py: error: unrecognized arguments: --lane .

### stage-scan help (direct rc)
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/stage_scan.py --help
rc=2

stderr=ERROR unknown option --help

### same tree after runtime failures: no audit leg notices
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### ordinary swap rejected
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=1
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 defect n=2
  DEFECT ERRATA:item-names-other-revision:Do-nothing control (committed at freeze)->c80fcdb3
  DEFECT ERRATA:item-names-other-revision:Red-before (committed at freeze)->d8a77d3f
MISMATCH 2
DEFECTS n=2
PREDICATE R73-C2 fail
stderr=

### swap with both revisions in both items accepted
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### correct revision explicitly denied in owning item accepted
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### later wrong numbered item ignored
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

### Independent denominator
table lines=109; non-header/separator lines=107; parsed rows=106; malformed=1
rows without script=0; unique scripts=106; shared-script excess=0
DROPPED LINE FULL: | `round66_c1_tensor_probe` | probe | `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt` (flags implemented: `--run --receipt --check-receipt --selftest --work`; the battery form `--run --receipt <path> --work <scratch>` runs the five frozen cases in per-case bwrap (`--unshare-net --unshare-pid`, `/tests` read-only, `/app` = the case directory) with gloo on 127.0.0.1:12355 under a flock; `--check-receipt` re-derives the PROBE and GRADER shas, every CASE `case_sha256`/`junit_sha256`/`rc` and every VECTOR from its own junit against the frozen table — it cannot prove a live run, the live evidence is the receipt's BUILD/RUN lines) | `0` pass (`PREDICATE R66-C1 pass`, `CHECK ok cases=5`, rc 0) | receipt of record `corpus/evidence/round66/tensor/receipt.txt`; red fixture `corpus/evidence/round66/tensor/control-a1.txt`; registered round 68 attempt 2 (the row was missing at `0e52fb5d`, found by the w1 `RegistryRows` seat and re-found by w2 `ScribeAttempt2`) |

### malformed existing row given invalid kind: still invisible
COMMAND (cwd=/fast/scratch/hyaku/kengaku-r73/C2CriticR73/base): /usr/bin/python3 plans/round73_c2_registry_audit.py --lane .
rc=0
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
stderr=

```

## Reproduction driver

```python
from pathlib import Path
import re, subprocess, sys, runpy
S=Path('/fast/scratch/hyaku/kengaku-r73/C2CriticR73')
B=S/'base'
A=runpy.run_path(str(B/'plans/round73_c2_registry_audit.py'))
sk=B/'SKILL.md'; cl=B/'plans/round-71-claims.md'
original=sk.read_text(); claims=cl.read_text(); log=[]
def note(x):
    log.append(str(x))
    print(x,flush=True)
def run(label,args):
    note('\n### '+label)
    note('COMMAND (cwd='+str(B)+'): '+' '.join(args))
    try:
        p=subprocess.run(args,cwd=B,text=True,capture_output=True,timeout=30)
        note('rc='+str(p.returncode)); note(p.stdout.rstrip()); note('stderr='+p.stderr.rstrip())
    except subprocess.TimeoutExpired as e:
        note('TIMEOUT 30s'); note(str(e))
def audit(label): run(label,[sys.executable,'plans/round73_c2_registry_audit.py','--lane','.'])
def cell(text,name,idx,value):
    found=0; lines=text.splitlines(keepends=True)
    for i,l in enumerate(lines):
        if not l.startswith('|'): continue
        cells=[x.strip() for x in re.split(r'(?<!\\)\|',l.strip().strip('|'))]
        if len(cells)==8 and cells[0]=='`'+name+'`':
            cells[idx]=value(cells[idx]) if callable(value) else value
            lines[i]='| '+' | '.join(cells)+' |\n'; found+=1
    assert found==1,(name,found)
    return ''.join(lines)
try:
    audit('immutable base + frozen audit (unfiltered exit code)')
    green=cell(original,'sources-adopt',3,lambda v:v+' · failed for non-zero refusal codes')
    green=cell(green,'round62-c1-class-survey',1,'gate')
    sk.write_text(green); audit('sanctioned two corrections baseline')
    cases=[
        ('empty pin rejected','hermetic-grader',5,''),
        ('real pin replaced by x','hermetic-grader',5,'x'),
        ('one-word verdict rejected','hermetic-grader',3,'failed'),
        ('verdict reduced to zero plus one word','hermetic-grader',3,'`0` failed'),
        ('failure negation accepted','sources-adopt',3,'`0` clean · never fails'),
        ('row renamed without identity reference','round62-c1-class-survey',0,'`unrelated-identity`'),
    ]
    for label,name,idx,v in cases:
        sk.write_text(cell(green,name,idx,v)); audit(label)
    sk.write_text(green)
    run('actual advertised sources-adopt entry',[sys.executable,'plans/sources_adopt.py','--lane','.'])
    run('stage-scan help (direct rc)',[sys.executable,'plans/stage_scan.py','--help'])
    audit('same tree after runtime failures: no audit leg notices')
    h=A['ERRATA_HEADING']; labels=A['ERRATUM_ITEMS']; a,ar=labels[0]; b,br=labels[1]
    variants={
        'ordinary swap rejected':f'{h}\n\n1. `{a}` landed with `{br}`.\n2. `{b}` landed with `{ar}`.\n',
        'swap with both revisions in both items accepted':f'{h}\n\n1. `{a}` landed with `{br}`; unrelated comparison `{ar}`.\n2. `{b}` landed with `{ar}`; unrelated comparison `{br}`.\n',
        'correct revision explicitly denied in owning item accepted':f'{h}\n\n1. `{a}` belongs to `{br}`, NOT `{ar}`.\n2. `{b}` belongs to `{ar}`, NOT `{br}`.\n',
        'later wrong numbered item ignored':f'{h}\n\n1. `{a}` landed with `{ar}`.\n2. `{b}` landed with `{br}`.\n3. Correction: `{a}` actually landed with `{br}`.\n',
    }
    for label,c in variants.items():
        cl.write_text(c); audit(label)
    cl.write_text(claims)
    block=A['registry_block'](original)
    lines=[l for l in block.splitlines() if l.startswith('|')]
    rows=A['parse_rows'](block)
    data=[]; malformed=[]
    for line in lines:
        cs=[x.strip() for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
        if cs[0]=='name' or set(cs[0])<=set('-: '): continue
        data.append(cs)
        if len(cs)!=8: malformed.append(line)
    note('\n### Independent denominator')
    note(f'table lines={len(lines)}; non-header/separator lines={len(data)}; parsed rows={len(rows)}; malformed={len(malformed)}')
    scripts=[A['entry_script'](r[2]) for r in rows]
    note(f'rows without script={scripts.count(None)}; unique scripts={len(set(scripts))}; shared-script excess={len(scripts)-len(set(scripts))}')
    for l in malformed: note('DROPPED LINE FULL: '+l)
    # Make the previously hidden row explicitly bad without repairing its arity.
    assert len(malformed)==1
    sk.write_text(green.replace(malformed[0],malformed[0].replace('| probe |','| invalid-kind |')))
    audit('malformed existing row given invalid kind: still invisible')
finally:
    sk.write_text(original); cl.write_text(claims)
    (S/'transcript.txt').write_text('\n'.join(log)+'\n')

```
