"""Exact serialized-text provenance: every codon change is one token->value swap.
Walks raw and projected codepoint streams; asserts nothing else changed."""
import hashlib, json, itertools
LANE="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW=LANE+"/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF=LANE+"/plans/fixtures/r29/profiles.json"
TOKENS=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
M=lambda n:"__%s__"%n
raw=open(RAW,'rb').read().decode('utf-8')
profiles=json.loads(open(PROF,'rb').read().decode('utf-8'))

def apply_order(text, values, order):
    for n in order: text=text.replace(M(n), values[n])
    return text

CANON=TOKENS
def provenance(raw, proj, values):
    i=j=0; swaps=[]; bad=None
    n=len(raw)
    while i<n:
        if j<len(proj) and raw[i]==proj[j]:
            i+=1; j+=1; continue
        hit=None
        for t in sorted(TOKENS,key=lambda x:-len(M(x))):
            if raw.startswith(M(t), i):
                hit=t; break
        if hit is None:
            bad=("unmatched", i, raw[i:i+20], proj[j:j+20]); break
        val=values[hit]
        if not proj.startswith(val,j):
            bad=("value_mismatch", i, hit, proj[j:j+len(val)+10]); break
        swaps.append({"token":hit,"offset":i,"raw_len":len(M(hit)),"proj_offset":j,"new_len":len(val)})
        i+=len(M(hit)); j+=len(val)
    if bad is None and j!=len(proj): bad=("trailing", i, j, len(proj))
    return swaps, bad

out={}
for pname,spec in profiles.items():
    values=spec["values"]
    proj=apply_order(raw, values, CANON)
    swaps,bad=provenance(raw,proj,values)
    delta=sum(len(values[s["token"]])-s["raw_len"] for s in swaps)
    print(pname, "swaps", len(swaps), "bad", bad,
          "len(proj)-len(raw)", len(proj)-len(raw), "sum_delta", delta,
          "bal", len(proj)-len(raw)==delta, "sha", hashlib.sha256(proj.encode()).hexdigest())
    # order permutations
    perms={"reversed":list(reversed(CANON)),
           "alpha":sorted(CANON),
           "swap_shopping_pair":["GITLAB","REDDIT","SHOPPING_ADMIN","SHOPPING","WIKIPEDIA","MAP"]}
    eq={}
    for label,order in perms.items():
        alt=apply_order(raw, values, order)
        eq[label]=hashlib.sha256(alt.encode()).hexdigest()==hashlib.sha256(proj.encode()).hexdigest()
    print("   order-permutation text equality", eq)
    # per token swap counts
    from collections import Counter
    print("   swaps by token", dict(Counter(s["token"] for s in swaps)),
          "first_offsets", {t:min((s["offset"] for s in swaps if s["token"]==t), default=None) for t in TOKENS})
    out[pname]={"swaps":len(swaps),"bad":bad,"len_delta":len(proj)-len(raw),"sum_delta":delta,
                "sha":hashlib.sha256(proj.encode()).hexdigest(),"order_perm_eq":eq,
                "swaps_by_token":dict(Counter(s["token"] for s in swaps))}
open(LANE+"/.ufo/waves/round-29/scratch/KengakuR28.R29Task681-2/provenance.json","w").write(json.dumps(out,indent=1,sort_keys=True))
