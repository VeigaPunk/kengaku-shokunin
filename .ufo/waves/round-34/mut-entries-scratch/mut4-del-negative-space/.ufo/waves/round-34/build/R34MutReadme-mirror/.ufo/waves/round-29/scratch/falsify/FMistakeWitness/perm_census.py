# Derived ONLY from the pinned generator text (six global str.replace calls, lines 11-16)
import hashlib, itertools, json
RAW="/tmp/fm-witness-2/base/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF=json.load(open("/tmp/fm-witness-2/base/plans/fixtures/r29/profiles.json"))
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
raw=open(RAW,encoding="utf-8").read()
def apply(text, steps, vals):
    for n in steps:
        text=text.replace("__%s__"%n, vals[n])
    return text
for pname,p in PROF.items():
    vals=p["values"]
    canon=hashlib.sha256(apply(raw,ORDER,vals).encode()).hexdigest()
    diff=0; digests=set()
    for perm in itertools.permutations(ORDER):
        d=hashlib.sha256(apply(raw,perm,vals).encode()).hexdigest()
        digests.add(d)
        if d!=canon: diff+=1
    # omit WIKIPEDIA
    omit=apply(raw,[n for n in ORDER if n!="WIKIPEDIA"],vals)
    print(pname, "canon="+canon[:16], "perms_differing_from_canonical=%d/%d"%(diff,720),
          "distinct_digests=%d"%len(digests),
          "omit_WIKIPEDIA_identical=%s"%(hashlib.sha256(omit.encode()).hexdigest()==canon))
