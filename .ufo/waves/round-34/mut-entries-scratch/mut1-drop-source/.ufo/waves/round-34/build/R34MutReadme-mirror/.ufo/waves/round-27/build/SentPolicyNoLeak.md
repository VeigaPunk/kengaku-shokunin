# R27 C1 — SentPolicyNoLeak

Axes: novelty (trustworthy extraction-policy comparison); calibration (prevent truth leakage from contaminating verdict agreement and intervals).

## Finding

**Severity: No confirmed leak (informational).** Exploit path if introduced: a policy/helper captures or resolves a record/global, or uses frame introspection to read `Rec.want`, `stored_ok`/`ok`, or grader state and conditions extraction on that truth. This would make policy agreement/pass metrics circular, invalidating C1 and its calibration summaries. Smallest remediation: keep the E0–E8 call boundary strictly `policy(rec.raw)`; statically allowlist policy globals/attributes and reject outcome/grader references, closures, imports, and introspection; keep grading exclusively after extraction.

## Evidence

- Private clone `/tmp/kengaku-r27-ExecPolicyCore`, observed HEAD `11a7fc8c64dc5d634331be24ccf5936f84a11f03`; no index/worktree mutation was made. Instrument SHA-256 `84e73f73230d062c286828ce2b9416a0449b3957dbc898dd8b5a3e56c977b96f`.
- `plans/parser_policy_compare.py:34-128` defines extraction helpers and E0–E8; `:131-141` maps the nine ids directly to those functions. `:218-221` calls each as `policy(rec.raw)`. Grading is separate at `:163-169` (`grade_value`), outside the policy definitions.
- `plans/grader_perturb.py:39-52` defines `Rec` fields including `raw`, `want`, `stored_ok`, `previous`, and `rep`.
- Frozen loader read-only check: `build_population` returned 1964 records, 0 exclusions/errors; all four committed SHA-256 pins matched. No `__pycache__` was created in the clone.
- Static AST allowlist check: `STATIC PASS policies=9 extraction_functions=11` (exit 0). It checked the literal E0–E8 registry, exact `raw` policy signatures, all globals and attributes used by extraction helpers, and rejected imports/global/nonlocal and undeclared names.
- Dynamic poisoned-Rec check: `DYNAMIC PASS policies=9 records=1964 calls=17676 poison_hits=0` (exit 0). Every non-`raw` field was poisoned/guarded, including `want`, `stored_ok`, and an `ok` sentinel; policies were called with `rec.raw` while `rec` remained in the caller frame. A separate frame→`rec.want` negative control tripped the guard.

## Exact one-line checks (run from the lane root; ROOT is the private clone used here)

Static AST/global/attribute/signature scan:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('/tmp/kengaku-r27-ExecPolicyCore/plans/parser_policy_compare.py').read_text()); a=next(n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='POLICIES' for x in n.targets)); kv=[(x.elts[0].value,x.elts[1].id) for x in a.value.args[0].elts]; assert [k for k,v in kv]==[f'E{i}' for i in range(9)]; fs={n.name:n for n in t.body if isinstance(n,ast.FunctionDef) and n.lineno<a.lineno}; roots={v for k,v in kv}; assert roots<=fs.keys(); local=lambda f:{x.arg for x in f.args.posonlyargs+f.args.args+f.args.kwonlyargs}|{n.id for n in ast.walk(f) if isinstance(n,ast.Name) and isinstance(n.ctx,(ast.Store,ast.Del))}; base=lambda n:n.id if isinstance(n,ast.Name) else (base(n.value)+'.'+n.attr if isinstance(n,ast.Attribute) else '<complex>'); allow={'json','gp','FENCE_ANY','DECODER','_loads','_bare_last','reversed','enumerate','len','Exception'}; attrs={('gp','FENCED_RE'),('gp','BARE_RE'),('gp.FENCED_RE','findall'),('gp.BARE_RE','findall'),('FENCE_ANY','findall'),('DECODER','raw_decode'),('json','loads'),('raw','strip')}; ns=[(f,n) for f in fs.values() for n in ast.walk(f)]; bad=[(f.name,n.lineno,type(n).__name__,getattr(n,'id',getattr(n,'attr',''))) for f,n in ns if (isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id not in local(f)|allow) or (isinstance(n,ast.Attribute) and (base(n.value),n.attr) not in attrs) or isinstance(n,(ast.Global,ast.Nonlocal,ast.Import,ast.ImportFrom))]; bad+=[(v,'signature') for k,v in kv if [x.arg for x in fs[v].args.posonlyargs+fs[v].args.args]!=['raw'] or fs[v].args.vararg or fs[v].args.kwarg or fs[v].args.kwonlyargs or fs[v].args.defaults or fs[v].args.kw_defaults]; assert not bad,bad; print(f'STATIC PASS policies={len(kv)} extraction_functions={len(fs)}')"
```
Dynamic poisoned-Rec/caller-frame check:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys;sys.path.insert(0,'/tmp/kengaku-r27-ExecPolicyCore/plans');import parser_policy_compare as m;h=[0];b={'file','line','cell','pid','turn','grader','want','stored_ok','ok','previous','rep','__dict__'};trip=lambda *a,**k:(h.__setitem__(0,h[0]+1),(_ for _ in ()).throw(AssertionError('poison')))[1];z=type('Z',(),dict.fromkeys(['__bool__','__eq__','__ne__','__iter__','__repr__','__str__','__hash__','__getattr__','__getitem__','__len__','__contains__','__int__','__index__'],trip))();get=lambda s,n:(h.__setitem__(0,h[0]+1),(_ for _ in ()).throw(AssertionError(n)))[1] if n in b else object.__getattribute__(s,n);G=type('GuardRec',(m.gp.Rec,),{'__getattribute__':get});base=m.gp.build_population('/tmp/kengaku-r27-ExecPolicyCore');assert len(base)==1964 and not m.gp._LAST['errors'];records=[G(z,z,z,z,z,z,r.raw,z,z,z,z) for r in base];del base;[object.__setattr__(r,'ok',z) for r in records];invoke=lambda policy,rec:policy(rec.raw);out=[invoke(f,r) for f in m.POLICIES.values() for r in records];assert h[0]==0 and all(v is not z for v in out);print(f'DYNAMIC PASS policies={len(m.POLICIES)} records={len(records)} calls={len(out)} poison_hits={h[0]}')"
```

These checks are supplementary, not a proof against arbitrary Python introspection or native-code tricks. The strict AST allowlist is intentionally scoped to the extraction helper/policy block before `POLICIES`; grading/tally code legitimately reads record outcomes after policy invocation.

Installs: none.

VERDICT: No outcome/grader leak found in the writer clone; strict AST scan and 17,676 poisoned-Rec policy calls passed. The instrument existed in the clone at recheck, so both checks were applied read-only.