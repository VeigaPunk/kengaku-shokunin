# Probe B — error propagation / recovery from a corrupted mid-state (round 8)

**Source:** `/tmp/bench-r8/results.jsonl` (md5 `df154cb5…`), 268 records, 32 of them `B-*` (4 cells × 8 pids).
Probe source: `/tmp/bench-r8/horizon.py` — `run_b` at lines 178–222; classification at 210–215; corruption at 183–193.
All numbers below are produced by `/tmp/kengaku-r9/analyze_b.py`, `analyze_b2.py`, `analyze_b3.py` (appendix = the core).

**Provenance defect (voids "identical bytes" assumption):** the repo copy `corpus/evidence/round8-horizon/results.jsonl` is **not** byte-identical (md5 `01547cfa…`); it diverges at record index 10 while keeping identical cell counts, and **0/8** `B-corrupt-plain` and **0/8** `B-clean-plain` records match. It is a *different execution* of the same probe. Everything here uses the `/tmp` copy.

---

## 1. 2×2 table (n=8 pids/cell: pids 1–8)

| cell | exact pass | corrected | propagated | other | `healed` (=key restored) | parse fail | `finish` |
|---|---|---|---|---|---|---|---|
| B-corrupt-plain | **3/8** | 3 | 1 | 4 | 5/8 | 0 | stop×8 |
| B-corrupt-hint  | **3/8** | 3 | 0 | 5 | 7/8 | 0 | stop×8 |
| B-clean-plain   | **6/8** | 6 | – | 2 | 8/8 (trivial) | 0 | stop×8 |
| B-clean-hint    | **6/8** | 6 | – | 2 | 8/8 (trivial) | 0 | stop×8 |

`outcome` is `corrected` iff exact, else `propagated` iff `got == sim(corrupt_mid)+ops8-10`, else `other` (`horizon.py:210-213`).
`corrected` therefore means *"answer equals the true final state"* — implemented as recompute-from-init or as a lucky overwrite, not as a diagnosed repair.
`healed` is degenerate in clean cells (`healed = (mode=='clean') or …`, `horizon.py:214`) and also trivially true in the 4 corrupt pids whose corruption the tail ops erase (§5). `healed=False` only for pids **1,4,5** (plain) and **5** (hint).

`finish=stop` on all 32: the known `finish=length` harness defect does not appear in B.

## 2. Manipulation-binding check (critic defect #8) — corruption barely bound

Paired per pid, corrupt-plain vs clean-plain exact pass (`analyze_b.py` item2):

| pid | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| corrupt-plain ok | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| clean-plain ok   | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |

- discordant pairs: **corrupt-only passes = 0**, **clean-only passes = 3** (pids 1, 5, 6).
- both pass = 3, both fail = 2 (pids 4, 8). Exact two-sided sign/binomial p (`2·P(X≤0|n=3)` = 0.25); one-sided p = 0.125.
- corrupt-hint vs clean-hint: same shape, (0, 3), p = 0.25.

**Byte-level check:** `raw` for corrupt and clean is **byte-identical in 3/8 pids** for plain (2, 7, 8) and **3/8** for hint (2, 3, 5). For those pids the corruption changed literally nothing in the response.

**Verdict:** corrupt ≈ clean, *not* significantly distinguishable (p=0.25, n=8); the only directional hint (3 pids, all clean-better) is non-significant, and in ≥3/8 pids the corruption provably produced no observable output change. Compounded by §5 (4/8 corruptions are structurally inert), the effective treatment is present in ≈4/8 pids and observed in ≤3/8. **B's recovery signal reduces to a single usable data point (§4).**

## 3. Hint effect (paired, n=8) — null everywhere

| comparison | hint-only pass | plain-only pass | exact p | pass counts |
|---|---|---|---|---|
| within corrupt: hint vs plain | {4} | {7} | **1.0** | 3/8 vs 3/8 |
| within clean: hint vs plain | {4} | {5} | **1.0** | 6/8 vs 6/8 |

**4th-cell question (hint-on-clean damage?):** **No.** clean-hint 6/8 = clean-plain 6/8. The hint only permutes *which* pids fail: clean-plain fails {4,8}, clean-hint fails {5,8}. The pids that swap (4 fixed by hint, 5 broken by hint) are the same instability seen in corrupt cells (pid 4 passes corrupt-hint, pid 7 fails it) → draw noise on this non-iid endpoint, not a hint effect. Consistent with r7's finding that a *system*-prompt strategy flip is real while an inline instruction hint is inert at this n.

## 4. Propagation headline (pre-registered) and what `other` is

| cell | propagated | corrected | other |
|---|---|---|---|
| B-corrupt-plain | **1/8** (pid 1) | 3/8 (2,3,7) | 4/8 (4,5,6,8) |
| B-corrupt-hint  | **0/8** | 3/8 (2,3,4) | 5/8 (1,5,6,7,8) |

**The single `propagated` label is degenerate.** pid 1's corrupted key is `nails`, and ops 8–10 are `NEW rivets 9 / SET rivets 24 / NEW gaskets 4` — `nails` is *never touched by the tail*. The model simply copied the injected `nails:10` into its three outputs (`raw` shows `"nails": 10` in all three blocks) → bytes coincidentally equal `sim(corrupt_mid)+tail`. No operation was applied to the corrupted key: this is a **frozen-key carry, not arithmetic propagation**.

**`other` is not a recovery behaviour — it is independent arithmetic error.** Key-level decomposition (`analyze_b3.py`) tags each off key as `PROP` (matches `sim_corrupt`, differs from want) or `ERR` (matches neither):

| pid | cell | off keys (got → want | sim_corrupt) |
|---|---|---|---|
| 1 | corrupt-plain | `nails 10→5 (sim 10) PROP` — frozen-key carry, no tail op touches it |
| 4 | corrupt-plain | `nails 12→33 (sim 12) PROP` **+** `screws 21→0 (sim 0) ERR` |
| 5 | corrupt-plain | `hinges 11→16 (sim 16) ERR`, `washers 26→30 (sim 41) ERR` |
| 6 | corrupt-plain | `nails 6→3 (sim 3) ERR` |
| 8 | corrupt-plain | `washers 19→32 (sim 32) ERR` (raw identical to clean) |
| 5 | corrupt-hint | `washers 26→30 (sim 41) ERR` |
| 6 | corrupt-hint | `nails 6→3`, `screws 20→23` ERR |
| 7 | corrupt-hint | `hinges 6→3 ERR` |
| 1 | corrupt-hint | `hinges 26→0`, `washers 26→52` ERR |

So `other` is (a) recompute-from-own-memory with an independent arithmetic slip (pids 5, 6, 8 — the model is neither on the corrupt nor the true trajectory), plus (b) **one partial propagation mislabelled as `other`** (pid 4: `nails` genuinely propagated 19−7=12, while `screws` also drifted → the exact-match 3-way classifier misses it). **No format failures:** 0 parse failures, all 32 responses are well-formed final-state JSON blocks; `raw` lengths 100–178 completion tokens.

**Bottom line:** headline `propagated/8` = 1/8 and 0/8, but the honest count of *genuine* propagation events in round 8 is **1 key-event (pid 4's `nails`)**, and the honest count of *recovery* events is 3/8 (plain) with 2 of those (pids 3, 7) being inert-corruption trivial passes (§5).

## 5. Corruption-strength audit (critic defect #6) — the manipulation is broken in 6/8 pids

Reconstructed from `meta` (`truth[6]` = state after op 7) vs each corrupt record's own `corrupt_field`/`corrupt_from`; `hist_j` = the historical index whose value was used (`horizon.py:187-189`); **potency** = `sim(corrupt_mid)+ops8-10 ≠ true_final` (if false the corruption is erased before grading).

| pid | key | `corrupt_from` | true mid | Δ | historical? | tail refs (ops 8–10) | in `tail_touched` | **potent?** |
|---|---|---|---|---|---|---|---|---|
| 1 | nails | 10 | 5 | **+5** | **NO** → fabricated +5 | *none* | **NO** | yes, but untested (frozen key) |
| 2 | washers | 20 | 15 | **+5** | **NO** → fabricated +5 | op9 `SUB washers 6` | yes | yes |
| 3 | screws | 6 | 15 | −9 | yes (j=4) | op8 `DEL screws` | yes | **INERT (deleted)** |
| 4 | nails | 19 | 40 | −21 | yes (j=5) | op10 `SUB nails 7` | yes | yes |
| 5 | washers | 16 | 5 | +11 | yes (j=3) | op8 `MOV bolts→washers`, op10 `ADD washers 5` | yes | yes |
| 6 | washers | 27 | 7 | +20 | yes (j=6) | op10 `SET washers 19` | yes | **INERT (overwritten)** |
| 7 | washers | 8 | 16 | −8 | yes (j=3) | op8 `DEL washers` | yes | **INERT (deleted)** |
| 8 | screws | 23 | 0 | +23 | yes (j=4) | op8 `SET screws 1`, op10 `SUB screws 1` | yes | **INERT (clobbered)** |

**`tail_touched` did NOT guarantee exercise — verified per pid, defect #6 CONFIRMED.** For pid 1, `meta.tail_touched = ["gaskets","rivets"]`, and *neither key exists at mid* (`mid_keys = brackets, hinges, nails, screws, washers`; `gaskets` is created at op 10, `rivets` at op 8). So at `horizon.py:184` `cand = []` → the generator silently fell through to `rng.choice(list(state_mid))` at line 185 and picked an arbitrary live key (`nails`), which ops 8–10 never touch. The "victim key is exercised by the tail" invariant holds for 7/8 pids, **fails for pid 1**.

**Second generator failure:** for pids 1 and 2 the historical-value search (`horizon.py:187-189`) found no differing earlier value, so `corrupt_val` was fabricated as `true_mid + 5` (line 191) — the corruption is **not** a plausible historical drift but an off-distribution constant. For pid 2 the key is legitimately exercised, so pid 2 is a *fabricated* corruption that does bind.

**Off-by-tiny?** No. All |Δ| = {5, 5, 9, 21, 11, 20, 8, 23}, min 5, median 11.5 — every corruption is far above any noise floor; historical-value corruption produced large deltas (up to 23 on a key whose true mid is 0). No near-undetectable case exists.

**Net:** of 8 corruptions, **4 are structurally inert** (erased/clobbered by the tail ops: pids 3, 6, 7, 8), **2 are fabricated off-distribution values** (pids 1, 2), **1 (pid 1) is on a key the tail never touches**. Only **pids 4 and 5** are genuine historical-value corruptions that survive to the final state — i.e. the manipulation is well-formed in **2/8** pids.

## 6. Ceiling argument — clean already fails 2/8

| cell | failing pids |
|---|---|
| B-clean-plain | {4, **8**} |
| B-clean-hint | {5, **8**} |
| B-corrupt-plain | {1, 4, 5, 6, 8} |
| B-corrupt-hint | {1, 5, 6, 7, 8} |

**pid 8 fails all four cells** (corrupt *and* clean; its corrupt-plain `raw` is byte-identical to its clean-plain `raw`) → pure capability ceiling, zero corruption content. pid 4 fails both corrupt-plain and clean-plain; pid 5 fails clean-hint and both corrupt cells.

- Of the 5 corrupt-plain failures, **3 (4, 5, 8)** are pids that also fail ≥1 clean cell.
- Of the 5 corrupt-hint failures, **2 (5, 8)** are pids that also fail ≥1 clean cell.

**Capability-clean subset** = pids passing both clean cells = {1, 2, 3, 6, 7} (n=5). On it: corrupt-plain 3/5 (propagated 1, corrected 3, other 1), corrupt-hint 2/5 (corrected 2, other 3). Even here, 3 of the 5 pids (3, 6, 7) carry inert corruptions, so their "passes" are trivial.

**Conclusion for B:** the 10-op monolithic recompute from a *given* mid state already fails 2/8 (25%) in the clean arm, so a 3/8 corrupt-arm pass rate is not separable from the capability ceiling by this design. After removing (i) the 4 inert corruptions, (ii) the capability-ceiling pids, and (iii) the frozen-key carry mislabelled `propagated`, round 8 yields **one** genuine propagation observation (pid 4 `nails`) and **at most two** genuine healing observations. Round 9 needs: corruption applied only to keys with a *verified* tail reference, a ≥2-op post-corruption horizon, and a larger n to escape the ±3-pid draw noise that dominates at n=8 on this non-iid endpoint.

## Confidence

| # | Claim | Grade | Reason |
|---|---|---|---|
| 1 | 2×2 counts (3/8, 3/8, 6/8, 6/8) and outcome/healed/finish distributions | **high** | direct `Counter` over the 32 B records; command in appendix |
| 2 | Corruption bound only weakly; corrupt-plain ≈ clean-plain (0 vs 3 discordant, p=0.25); 3/8 raw byte-identical | **high** (counts) / **medium** (interpretation) | samples are exact; "never bound" is a directional reading of a non-significant n=8 test |
| 3 | Hint is a null effect in both cells (1–1, p=1.0); no hint-on-clean damage (6/8 = 6/8) | **high** | exact paired counts + exact binomial; consistent across both arms |
| 4 | `propagated` 1/8 (plain), 0/8 (hint); the 1 is a frozen-key carry, not propagation | **high** | pid 1 `tails` read from `meta.ops[7:10]` + `raw` shows the value echoed unmodified |
| 5 | `tail_touched` fails to guarantee exercise for pid 1; 4/8 corruptions structurally inert; pids 1–2 fabricated | **high** | per-pid reconstruction from `meta`; inertness reproduced by re-simulating ops 8–10 from each corrupt mid |
| 6 | Clean ceiling 2/8; pid 8 fails all four cells | **high** | direct read of `ok`; pid 8 raw byte-identity across cells |
| 7 | Repo `results.jsonl` ≠ `/tmp` copy (different run) | **high** | md5 mismatch + 0/8 identical B records, divergence at record index 10 |
| 8 | "Genuine propagation events = 1" | **medium** | depends on the PROP/ERR key-tagging heuristic (a key matching `sim_corrupt` could coincide by luck; at Δ≥5 on small integers that is unlikely but unproven) |

## Appendix — core reproduction (≤40 lines)

```python
import json, math
from collections import Counter, defaultdict
R='/tmp/bench-r8/results.jsonl'
recs=[json.loads(l) for l in open(R)]
meta={r['pid']:r for r in recs if r['cell']=='meta'}
by=defaultdict(dict); [by[r['cell']].__setitem__(r['pid'],r) for r in recs if r['cell'].startswith('B-')]
pids=list(range(1,9)); CELLS=['B-corrupt-plain','B-corrupt-hint','B-clean-plain','B-clean-hint']
def sim(s,op):
    s=dict(s); k=op[0]
    if k=='SET': s[op[1]]=op[2]
    elif k=='ADD': s[op[1]]+=op[2]
    elif k=='SUB': s[op[1]]-=op[2]
    elif k=='MOV': s[op[2]]+=s[op[1]]; s[op[1]]=0
    elif k=='DEL': del s[op[1]]
    elif k=='NEW': s[op[1]]=op[2]
    return s
def sa(init,ops,n=None):
    s=dict(init); out=[]
    for op in (ops if n is None else ops[:n]): s=sim(s,op); out.append(s)
    return out
# 1) 2x2
for c in CELLS:
    rs=[by[c][p] for p in pids]
    print(c, sum(r['ok'] for r in rs), dict(Counter(r['outcome'] for r in rs)), sum(r['healed'] for r in rs), Counter(r['finish'] for r in rs))
# 2-3) exact binomial sign test
def bino(b,c):
    n=b+c
    return 1.0 if n==0 else min(1.0, 2*sum(math.comb(n,k) for k in range(min(b,c)+1))/2**n)
ok=lambda c:{p:bool(by[c][p]['ok']) for p in pids}
for A,B in [('B-corrupt-plain','B-clean-plain'),('B-corrupt-hint','B-clean-hint'),('B-corrupt-hint','B-corrupt-plain'),('B-clean-hint','B-clean-plain')]:
    a,b=ok(A),ok(B); x=sum(a[p] and not b[p] for p in pids); y=sum(b[p] and not a[p] for p in pids)
    print(A,'vs',B,'(a-only,b-only,p)=',(x,y,bino(x,y)))
print('byte-identical raw:',{c:[p for p in pids if by[c][p]['raw']==by[c.replace('corrupt','clean')][p]['raw']] for c in CELLS[:2]})
# 5) per-pid corruption audit + potency
for p in pids:
    m=meta[p]; t=sa(m['init'],m['ops']); cm=sa(m['init'],m['ops'],7)[-1]; r=by['B-corrupt-plain'][p]
    k,cf=r['corrupt_field'],r['corrupt_from']; sm=dict(cm); sm[k]=cf
    potent=sa(sm,m['ops'][7:])[-1]!=t[-1]
    print(p,k,cf,'true',cm[k],'d=%+d'%(cf-cm[k]),'in_tail_touched',k in m['tail_touched'],'potent',potent)
```