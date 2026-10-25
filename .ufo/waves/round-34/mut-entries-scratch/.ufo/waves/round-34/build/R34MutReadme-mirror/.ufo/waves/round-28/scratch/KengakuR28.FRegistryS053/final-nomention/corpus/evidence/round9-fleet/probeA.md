# Probe A — round-8 planning-horizon / transcript-shape cells (A-INC, A-MONO, A-CKPT)

Lane: kengaku round 9, probe-A analysis. Input: `/tmp/bench-r8/results.jsonl` (268 records). Offline (no HTTP).
Every number below is stdout of `/tmp/kengaku-r9/probeA.py` (33 lines, verbatim in Appendix; labels S1–S7c ↔ items §1–§7).
Protocol source: `corpus/evidence/round8-horizon/horizon.py` lines 112–162.

## 0. Integrity findings (blocker-class for reuse)

| check | result |
|---|---|
| `md5sum /tmp/bench-r8/results.jsonl` | `df154cb524bf210782fb0f4a46fd1bdc` |
| `md5sum corpus/evidence/round8-horizon/results.jsonl` | `01547cfaa8b5b0a28d27559e8be63bb0` — **NOT identical** |
| same line count (268)? | yes; cell counts identical; all non-`raw` values byte-equal (0 value diffs) |
| `raw` field present | /tmp copy: 260/260 non-meta records. **repo copy: 0/268 records** |

⇒ The repo copy is a raw-stripped redaction. §5 (ack audit) and any re-grading from original text are reproducible **only** from the /tmp copy.
⇒ `want` in every graded A-record equals `meta['truth'][turn-1]` (0/140 mismatches, verified inline) — grading target is trustworthy.
⇒ CKPT design intent (horizon.py:128,137,152–157): graded at turns {4,7,10}; all other turns get the literal instruction `Reply 'ok'.`; ack `raw` is logged truncated to 80 chars (horizon.py:149).

## 1. Per-cell table

Final graded turn per cell (A-INC t10, A-CKPT t10, A-MONO t1):

| cell | n | strict pass | zero-tolerant pass¹ | mean `nwrong` | mean `wall_s` | mean completion tokens |
|---|---|---|---|---|---|---|
| A-INC | 10 | **7/10** | 9/10 | 0.30 | 0.29 | 39.5 |
| A-CKPT | 10 | **1/10** | 1/10 | 1.40 | 0.29 | 40.6 |
| A-MONO | 10 | **0/10** | 0/10 | 2.10 | 0.36 | 47.5 |

Whole-cell aggregates over all graded turns (INC 100, CKPT 30, MONO 10 = 140 graded records):

| cell | graded recs | pass | mean `nwrong` | mean `wall_s` | mean completion tokens |
|---|---|---|---|---|---|
| A-INC | 100 | 81 | 0.19 | 0.29 | 40.9 |
| A-CKPT | 30 | 13 | 0.90 | 0.28 | 40.3 |
| A-MONO | 10 | 0 | 2.10 | 0.36 | 47.5 |

¹ zero-tolerant = record counts as a pass if every wrong key is a key absent from `got` whose truth value is 0 (i.e. only the "include keys whose value is 0" emission convention, horizon.py:117, was violated). Arithmetic is the `DZ`/`TOL` lambdas in the Appendix. Wall-clock and token means exclude nothing (no dropped records).

## 2. Error-onset (within-cell descriptions only)

Onset = first graded turn with `ok == false`. **These curves are within-cell descriptions, not cross-protocol comparisons**: turn *t* of INC and turn *t* of CKPT carry different instructions ("Output the FULL state" vs "Reply 'ok'" interleaved with CHECKPOINT), so equal turn indices are not equal stimuli, and MONO has no intermediate turns at all.

A-INC, per pid (onset, final `ok`, final `nwrong`):

| pid | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| onset | 7 | 1 | – | – | – | 6 | – | – | 9 | 7 |
| final ok | F | T | T | T | T | T | T | T | F | F |
| final nwrong | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |

Onset distribution: never-wrong 5, onset 1 ×1, onset 6 ×1, onset 7 ×2, onset 9 ×1.

A-INC per-turn `[t, strict pass/10, tolerant pass/10, mean nwrong]`:

| t | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| strict | 9 | 9 | 9 | 9 | 9 | 8 | 7 | 7 | 7 | 7 |
| tolerant | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| mean nwrong | .1 | .1 | .1 | .1 | .1 | .2 | .3 | .3 | .3 | .3 |

A-CKPT, per pid (onset among {4,7,10}, final ok): pid1 (7,F), pid2 (7,F), pid3 (10,F), pid4 (7,F), pid5 (**4**,F), pid6 (7,F), pid7 (10,F), pid8 (7,F), pid9 (never,T), pid10 (7,F).
Onset distribution: t4 ×1, t7 ×6, t10 ×2, never ×1.

A-CKPT per-checkpoint `[t, strict, tolerant, mean nwrong]`: t4 (9,9,0.1) · t7 (3,3,1.2) · t10 (1,1,1.4).
Structural note: the only CKPT final pass (pid9) is a pid that **fails** INC's final turn — the two pass sets are near-disjoint, not nested.

## 3. Recovery rate (A-INC only, `t → t+1`)

Pre-registered rule: for each (pid, t), t∈1..9, each wrong key at t is "recovered" iff it is not a wrong key at t+1.
Denominator is 16 (pid,t) pairs with a non-empty wrong set (pids 3,4,5,7,8 never have any wrong turn).

| metric | value |
|---|---|
| key instances fixed at t+1 / total wrong-key instances | **2/16 = 0.125** |
| (pid,t) pairs with ≥1 key fixed | 2/16 |
| (pid,t) pairs with all wrong keys fixed | 2/16 |
| per-pid (fixed / total) | p1 0/3 · p2 1/6 · p3–5 0/0 · p6 1/3 · p7–8 0/0 · p9 0/1 · p10 0/3 |

**Both recoveries are truth-side lifecycle coincidences, not repair** (`S3`/`S7b`, episodes `[(pid,key,first_wrong,last_wrong)]`):
- pid2 `bolts`: wrong turns 1–6 (MOV at op1 kept the source stale at 15 instead of 0 — horizon.py:115), clears at t7 because op7 is `DEL bolts`, which removes the key on both sides.
- pid6 `nails`: dropped from t6 (MOV at op6 zeroes it), reappears correct at t9 because op9 is `ADD nails 3` on the then-absent key.
⇒ 5 (pid,key) error episodes total; 2 cleared by later truth mutation; 3 persist to the final turn. Model-initiated repair: **0/16**.

## 4. Paired comparisons (unit = pid, n = 10; two-sided exact sign test)

Test: per-pid pass/fail difference at the final graded turn; ties dropped; p = 2·Σ_{i≤min(d⁺,d⁻)} C(n,i)/2ⁿ, `math.comb` (values double-checked against a hand binomial: p(7,1)=0.0703, p(7,0)=0.0156, p(1,0)=1.0).

| contrast | sign vector over pids 1..10 (+1 = first cell passes, second fails) | d⁺ | d⁻ | ties | two-sided p |
|---|---|---|---|---|---|
| INC − CKPT | [0,+1,+1,+1,+1,+1,+1,+1,−1,0] | 7 | 1 | 2 (p1, p10 both fail) | **0.0703** |
| CKPT − MONO | [0,0,0,0,0,0,0,0,+1,0] | 1 | 0 | 9 | **1.0000** |
| INC − MONO | [0,+1,+1,+1,+1,+1,+1,+1,0,0] | 7 | 0 | 3 | **0.0156** |

**ESS caveat (mandatory, from prior rounds).** These draws are non-iid: r7-n25 measured lag-1 autocorrelation +0.26/+0.32 with a 5–10-request burst horizon and near-deterministic same-seed replays, so the request is not the unit and the p-values above are *upper bounds* on evidence; ESS is below n=10. The A-block was run as, per pid, `INC(10 draws) → MONO(1) → CKPT(10)` back-to-back (run.log lines 1–30), i.e. a genuinely paired design — but the same ordering makes it burst-adjacent: the INC-final and MONO draws of a pid are 1 request apart, MONO and CKPT turn 1 are 1 request apart, and same-cell draws of adjacent pids are only 3 requests apart (e.g. `[25/78] A-INC 9`, `[28/78] A-INC 10`). So cells of one pid share burst state (bias toward ties), and pids are not independent of each other. The INC↔CKPT final turns are 11 draws apart, i.e. at/just beyond the burst horizon — the least-coupled of the three contrasts. Report the sign counts as the finding and the p as nominal.

## 5. Ack-compliance audit (A-CKPT-ack, 70 records = turns {1,2,3,5,6,8,9} × 10 pids)

Classification of the 80-char-truncated `raw` (`{` present ⇒ emitted a JSON state; else starts with `ok` ⇒ ack):

| stratum | n | emitted JSON state | ack-only | other |
|---|---|---|---|---|
| turn 1 (the 10 first turns) | 10 | **10** | 0 | 0 |
| turns 2,3,5,6,8,9 ("`Reply 'ok'`" turns) | 60 | **0** | 60 (54 × `ok`, 6 × `ok\n```` for pid4, all ≤6 chars) | 0 |

**Root cause of the turn-1 stratum is the harness, not the model.** horizon.py:130 builds the first user message unconditionally as `… Output the FULL state after applying it.`; the `Reply 'ok'.` switch is only appended for turns ≥2 (horizon.py:152–153). So turn 1 of CKPT is an INC-shaped turn that the harness forgot to convert — and it was left **ungraded** (horizon.py:137 grades only {4,7,10}).

**Leak audit / recomputed CKPT story.**
- At the true ack turns there are **0 state emissions**, so the feared leak (ack turns drifting back to full-state emission, turning CKPT into INC) did **not** occur: the 1/10 final result does **not** understate checkpoint performance via ack leakage. Nor via grader leniency: zero-tolerant CKPT final is still 1/10.
- The leak that *did* occur is in the opposite direction, and it matters for interpretation: CKPT inherited a correct self-copy anchor at turn 1. Post-hoc grading of the leaked turn-1 states against `meta['truth'][0]`: 8/10 parseable (pid2 and pid5 are truncated mid-object at the 80-char cap) and **8/8 of those exact**. So CKPT's first checkpoint (t4) is a 3-op latent step *from a correct anchor*, and it scores 9/10 — identical to INC's 9/10 at t4 (different pid sets: INC fails pid2, CKPT fails pid5). The CKPT collapse happens across t4→t7→t10 (3→6→9-op latent spans): 9 → 3 → 1.
- Quantified understatement of CKPT: none from leakage (0/60); residual uncertainty for 2 pids whose turn-1 anchor cannot be certified (pid2, pid5) — so "≥8/10 turn-1 anchors correct" is the honest bound.

## 6. Failure-class accounting (classes reported separately, never merged into state errors)

Classes: `parse_fail` = `got` null/non-dict; `finish=length`; `empty raw`; all A-cells otherwise `graded`.

| cell | parse_fail | finish == "length" | empty raw | graded | finish values observed |
|---|---|---|---|---|---|
| A-INC | 0 | 0 | 0 | 100/100 | all `stop` |
| A-CKPT | 0 | 0 | 0 | 30/30 | all `stop` |
| A-MONO | 0 | 0 | 0 | 10/10 | all `stop` |
| A-CKPT-ack | n/a (no `got` field by design) | 0 | 0 | 70/70 logged | all `stop` |

⇒ **No A-cell failure is a harness artifact**: every response was a fenced parseable JSON dict; the family "`finish=length`" (r5 task 06) did not recur even for MONO's single long answer (max raw 125 chars) and max_tokens=8192 (horizon.py:14). Extraction relied on the line 39–46 fallback, never the fence-only path being the sole route (bareraw JSON without an opening fence occurs, e.g. CKPT pid1 t4).
Cross-cell supplementary (off probe-A scope, same run): B-* 32/32 `stop`, 0 non-dict `got`; C-conflict/benign/norule 12/12 `parse=True`; C-MONO's 4 records carry `got=None` by its own grader, not a parse failure.
Error *content* split (why "fail" is not one thing): INC 9/19 failing turns are **drop-zero-only** (a zero-key presence convention), CKPT 0/17, MONO 0/10. Zero-tolerant recompute: INC 9/10, CKPT 1/10, MONO 0/10.

## 7. Mechanism reading

The 7 → 1 → 0 ladder supports the scaffold hypothesis over "planning horizon", but only partially and only as a within-run description. The decisive pattern is that CKPT's cost is *zero* over the first latent span: with a correct turn-1 self-copy anchor, a 3-op latent step lands 9/10 at t4 — exactly INC's t4 rate — while the second and third spans (3→6, 6→9 ops) fall to 3/10 and 1/10. If a 10-op horizon were the binding constraint, the loss should already be visible at the earliest checkpoint; instead it appears precisely once the model must maintain state *without its immediately preceding assistant emission*, which is what "self-copy scaffold, not horizon" predicts. Independent support from the INC side: all 5 INC error episodes (pid1 `hinges`, pid2 `bolts`, pid6 `nails`, pid9 `washers`, pid10 `hinges`) begin on exactly the turn whose operation is `MOV` — 12 MOV turns exist across the 10 problems, and every episode onset is one of them — and 9 of INC's 19 failing turns are the zero-key emission convention created by `MOV` ("a stays present at 0", horizon.py:115,117; pid6's drop starts exactly at its op6 MOV). INC's per-turn work is therefore rule-reading of the current op plus patch-the-previous-emission, not multi-op maintenance; its 7/10 is a floor of 9/10 per turn degraded by one op type. The strongest alternative the data **cannot** rule out: CKPT differs from INC in three ways at once — scaffold removal, alternating instruction cue (`Reply 'ok'` vs `CHECKPOINT — output the FULL state`, horizon.py:153,155), and the ungraded turn-1 anchor — and pid5's t4 failure (extra key `nails`, deleted at op2, resurrected as 0) looks like cue-switch/stale-context behaviour rather than lost latent state; with n=10, ESS<10 and only one protocol pair, "no self-copy", "instruction-switch cost" and "no graded feedback between checkpoints" are not separable. INC−MONO is no better: MONO additionally removes the whole transcript, adds a monolithic single-shot format, and its contrast has 9/10 ties, so no claim is supportable from it (p=1.0). What the data *do* rule out: (a) "the model plans 10 ops because INC hit 7/10" — INC's failures are one-op-rule and emission-convention errors, and its 7/10 is 9/10 under a zero-tolerant grader; (b) "MONO 0/10 is a truncation/parse artifact" — 0 `finish=length`, 0 parse failures, 100% fenced JSON; (c) "ack turns leaked CKPT toward INC" — 0/60 true ack turns emitted a state.

## Appendix — exact script (33 lines; `python3 /tmp/kengaku-r9/probeA.py`)

```python
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
```

## Confidence

| claim | grade | reason |
|---|---|---|
| Cell pass counts reproduce run.log SUMMARY (INC 7/10, CKPT 1/10, MONO 0/10) | high | independently recomputed from records; `want` matches meta truth for all 140 graded records |
| Repo copy is raw-stripped; md5 differs from /tmp copy | high | direct md5 + per-field comparison (0 value diffs excluding `raw`) |
| 0/60 true ack turns emitted a state; 10/10 turn-1 emissions are harness-dictated (horizon.py:130 vs 152) | high | raw ≤6 chars on all 60; turn-1 for all 10 pids carries a JSON state; source line cited |
| ≥8/10 turn-1 CKPT anchors are exact | high for the 8; pid2/pid5 unverifiable | post-hoc parse of the leaked states; 2 truncated at the 80-char log cap |
| Paired sign counts (7/1, 1/0, 7/0) and p (0.0703, 1.0, 0.0156) | high | computed twice; cross-checked against hand binomials |
| ESS < 10 / p-values are upper bounds | medium | burst coupling is imported from prior rounds' measurements, not re-measured on this run; request-adjacency from run.log is verified |
| Recovery 2/16, model-initiated repair 0/16 | high (arithmetic) / medium (interpretation) | per-episode traces verified (pid2 op7 `DEL bolts`, pid6 op9 `ADD nails`); "not repair" rests on those two traces being sufficient |
| Zero-tolerant INC 9/10 vs CKPT 1/10 | high (arithmetic) | DZ/TOL lambdas reproducible; whether the convention *should* be tolerated is a grader-design call (RULES line 117 demands zeros be present) |
| All 5 INC error onsets are MOV turns; 9/19 INC failures are zero-key convention | high | `S7b` onset op-type + `S7` counts |
| Mechanism reading (§7) | low–medium | n=10, one protocol pair, three conflated differences, ESS<10; the CKPT↔MONO contrast contributes no evidence (9 ties) |
