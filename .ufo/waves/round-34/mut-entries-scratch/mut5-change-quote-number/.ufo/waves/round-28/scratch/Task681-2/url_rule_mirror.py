# Independent stdlib re-statement of URLEvaluator "GOLD in PRED" (evaluators.py L187-236); upstream not imported.
import urllib.parse, collections
def clean(u): return str(u).rstrip("/")
def parse(u):
    p = urllib.parse.urlparse(u); return p.netloc + p.path, urllib.parse.parse_qs(p.query)
REF = "http://r.example/f/machinelearning |OR| http://r.example/f/deeplearning |OR| http://r.example/f/technology"
refs = [clean(u) for u in REF.split(" |OR| ")]
def score(pred_url):
    pred_base, pred_q = parse(clean(pred_url))
    ref_bases = [parse(u)[0] for u in refs]
    q = collections.defaultdict(set)
    for u in refs:
        for k, v in parse(u)[1].items(): q[k].update(v)
    base = float(any(rb in pred_base for rb in ref_bases))  # str-in-str: substring
    qs = 1.0
    for k, vals in q.items(): qs *= float(any(v in pred_q.get(k, []) for v in vals))
    return base * qs
for u in ["http://r.example/f/deeplearning/999/pytorch-gan",
          "http://r.example/f/MachineLearning/999/pytorch-gan",
          "http://r.example/f/machinelearning/999/pytorch-gan",
          "http://r.example/f/technologyfoo/999/x",
          "http://r.example/f/deeplearning",
          "http://r.example/submit?forum=deeplearning"]:
    print(score(u), u)
