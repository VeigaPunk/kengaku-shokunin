# Independent stdlib mirror of evaluators.py URLEvaluator(215-236) and
# StringEvaluator.clean_answer/must_include(80-111) + HTMLContentEvaluator(312-327).
# Upstream code is not imported or executed.
import urllib.parse, collections

def clean_answer(a):
    a = a.strip()
    if a.startswith("'") and a.endswith("'"): a = a[1:-1]
    elif a.startswith('"') and a.endswith('"'): a = a[1:-1]
    return a.lower()

def must_include(ref, pred):
    return float(clean_answer(ref) in clean_answer(pred))

def parse(u):
    p = urllib.parse.urlparse(u)
    return p.netloc + p.path, urllib.parse.parse_qs(p.query)

def url_score(pred_url, ref_string, host="r.example"):
    refs = [s.rstrip("/") for s in ref_string.split(" |OR| ")]
    pred_base, pred_q = parse(str(pred_url).rstrip("/"))
    ref_bases = [parse(r)[0] for r in refs]
    q = collections.defaultdict(set)
    for r in refs:
        for k, v in parse(r)[1].items(): q[k].update(v)
    base = float(any(rb in pred_base for rb in ref_bases))
    qs = 1.0
    for k, vals in q.items(): qs *= float(any(v in pred_q.get(k, []) for v in vals))
    return base * qs

REFURL = "http://r.example/f/machinelearning |OR| http://r.example/f/deeplearning |OR| http://r.example/f/technology"
URLS = [
 "http://r.example/f/machinelearning/999/x",
 "http://r.example/f/deeplearning/999/x",
 "http://r.example/f/technology/999/x",
 "http://r.example/f/MachineLearning/999/x",
 "http://r.example/f/machinelearning2/999/x",
 "http://r.example/f/deeplearningish/1/x",
 "http://r.example/f/deeplearning",
 "http://r.example/f/machinelearning?sort=new",
 "http://r.example/f/machinelearning#frag",
 "https://r.example/f/machinelearning/999/x",
 "http://r.example:9999/f/machinelearning/999/x",
 "http://r.example/f/machinelearning/999/x/",
]
print("== URL predicate (ref string = task 681 reference_url with r.example host)")
for u in URLS:
    print(f"{url_score(u,REFURL):.1f}  {u}")

REF_REPO = "http://gitlab.local:9000/eriklindernoren/PyTorch-GAN"
TEXTS = [
 "gan implementation -- http://gitlab.local:9000/eriklindernoren/PyTorch-GAN",
 "organ implementation",
 "vegan implementation",
 "gan implementations",
 "implementation of GANs",
 "http://gitlab.local:9000/eriklindernoren/PyTorch-GAN-fork",
 "http://gitlab.local:9000/eriklindernoren/PyTorch-GAN/-/tree/master",
 "https://gitlab.local:9000/eriklindernoren/PyTorch-GAN",
 "git@gitlab.local:eriklindernoren/PyTorch-GAN.git",
 "(...) http://gitlab.local:9000/eriklindernoren/PyTorch-GAN",
]
NO_REPO = "gan implementation only"
print("== HTML must_include pair (topic='gan implementation', repo=REF_REPO)")
for t in TEXTS:
    s = must_include("gan implementation", t) * must_include(REF_REPO, t)
    print(f"{s:.1f}  {t}")
print("== topic phrase alone")
for t in TEXTS:
    print(f"{must_include('gan implementation', t):.1f}  {t}")
