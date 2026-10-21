# Independent stdlib mirror of StringEvaluator.clean_answer/must_include (evaluators.py 80-111)
# as used by HTMLContentEvaluator.must_include(tokenize=False) at 312-327. No upstream import.
def clean_answer(a):
    a = a.strip()
    if a.startswith("'") and a.endswith("'"): a = a[1:-1]
    elif a.startswith('"') and a.endswith('"'): a = a[1:-1]
    return a.lower()
def must_include(ref, pred):
    return float(clean_answer(ref) in clean_answer(pred))

TOPIC="gan implementation"
REPO="http://gitlab.local:9000/eriklindernoren/PyTorch-GAN"
cases=[
 ("topic", "organ implementation"),
 ("topic", "vegan implementation"),
 ("topic", "gan implementations"),
 ("topic", "implementation of GANs"),
 ("topic", "GAN IMPLEMENTATION in PyTorch"),
 ("repo",  "http://gitlab.local:9000/eriklindernoren/PyTorch-GAN-fork"),
 ("repo",  "http://gitlab.local:9000/eriklindernoren/PyTorch-GAN/-/tree/master"),
 ("repo",  "http://gitlab.local:9000/eriklindernoren/PyTorch-GAN.git"),
 ("repo",  "http://evil.example/?next=http://gitlab.local:9000/eriklindernoren/PyTorch-GAN"),
 ("repo",  "https://gitlab.local:9000/eriklindernoren/PyTorch-GAN"),
 ("repo",  "git@gitlab.local:eriklindernoren/PyTorch-GAN.git"),
]
for kind,s in cases:
    ref = TOPIC if kind=="topic" else REPO
    print(f"{kind:5} {must_include(ref,s):.1f}  {s}")
print()
# combined submission text controls (both required contents)
comb=[
 "GAN implementation with PyTorch - http://gitlab.local:9000/eriklindernoren/PyTorch-GAN",
 "organ implementation - http://gitlab.local:9000/eriklindernoren/PyTorch-GAN-fork",
 "gan implementations - see http://gitlab.local:9000/eriklindernoren/PyTorch-GAN/-/tree/master",
]
for s in comb:
    print(f"pair  {must_include(TOPIC,s)*must_include(REPO,s):.1f}  {s}")
