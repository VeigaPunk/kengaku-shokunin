import json, hashlib, os, subprocess, shutil, sys
S = "/fast/scratch/hyaku/kengaku-r53/C1CritCounterReach"
REAL = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
ENV = dict(os.environ, TMPDIR=f"{S}/tmp")
os.makedirs(f"{S}/tmp", exist_ok=True); os.makedirs(f"{S}/results", exist_ok=True)
GIT_ID = ["-c", "user.email=c1crit@fixture.invalid", "-c", "user.name=C1CritCounterReach"]

def sh(*a, cwd=None):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, env=ENV)

def git(lane, *a):
    return subprocess.run(["git", "-C", lane, *GIT_ID, *a], capture_output=True, text=True, env=ENV)

def fresh(name):
    d = f"{S}/{name}"
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", REAL, d], check=True, env=ENV)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, (top, d)
    return d

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def counter(lane, tag):
    r = subprocess.run([sys.executable, "plans/round53_c1_triage.py", "--lane", lane], cwd=lane,
                       capture_output=True, text=True, env=ENV)
    txt = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "SyntaxWarning" not in l)
    open(f"{S}/results/{tag}.txt", "w").write(txt + "\n")
    keep = [l for l in txt.splitlines() if l.startswith(("FREEZE", "ORACLE", "CONFIRM", "PRIOR", "PREDICATE", "  REJ"))]
    print(f"== {tag} rc={r.returncode}")
    for l in keep: print("   ", l)

ALLP1 = ("# ATTACK FIXTURE (critic scratch): all-P1 stand-in. Not the real classifier. Classifies nothing.\n"
         "import ast\n\n\ndef classify_source(src):\n    out = {}\n    for n in ast.parse(src).body:\n"
         "        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):\n            out[n.name] = 'P1'\n    return out\n")
TESTS = json.load(open(f"{REAL}/corpus/evidence/round53/tests-index.json"))["tests"]

def write_labels(lane, mode="all_y", contested=()):
    lab = {}
    for x in TESTS:
        if x["id"] in contested:
            lab[x["id"]] = {"labelers": ["C1LabelA", "C1LabelB"], "labels": ["Y", "N"]}
        else:
            lab[x["id"]] = {"labelers": ["C1LabelA", "C1LabelB"], "labels": ["Y", "Y"]}
    open(f"{lane}/corpus/evidence/round53/oracle-labels.json", "w").write(json.dumps({"labels": lab}))

def freeze(lane, authors=("C1ExecClassifier",)):
    open(f"{lane}/plans/round53-c1-freeze.json", "w").write(json.dumps(
        {"classifier_sha256": sha(f"{lane}/plans/round53_c1_classify.py"), "author_seats": list(authors)}))

def commit(lane, msg, *paths):
    git(lane, "add", "--", *paths)
    r = git(lane, "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr

# ---------- T1: classifier committed AFTER labels; freeze json (sha of v1) committed first ----------
L = fresh("T1-classifier-after-labels")
open(f"{L}/plans/round53_c1_classify.py", "w").write(ALLP1)   # exists in working tree only
freeze(L); commit(L, "freeze json only", "plans/round53-c1-freeze.json")
write_labels(L); commit(L, "labels", "corpus/evidence/round53/oracle-labels.json")
commit(L, "classifier added last", "plans/round53_c1_classify.py")
print(git(L, "log", "--format=%h %s", "--", "plans/round53_c1_classify.py").stdout.strip())
counter(L, "T1")
print(git(L, "log", "--format=%h %s", "--", "plans/round53-c1-freeze.json").stdout.strip())

# ---------- T2: classifier edited and freeze json rewritten AFTER labels were committed ----------
L = fresh("T2-rewrite-after-labels")
open(f"{L}/plans/round53_c1_classify.py", "w").write(ALLP1)
freeze(L); write_labels(L)
commit(L, "A: freeze + classifier v1 + labels (copied from v1)", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py", "corpus/evidence/round53/oracle-labels.json")
# v2: a different classifier (changed after its labels), freeze json re-hashed to match
open(f"{L}/plans/round53_c1_classify.py", "a").write("\n# v2: changed after labels were committed\n")
freeze(L); commit(L, "B: classifier v2 + re-hashed freeze", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py")
counter(L, "T2")
print("T2 HEAD classifier sha", git(L, "show", "HEAD:plans/round53_c1_classify.py").stdout.count("v2"), "commits touching classifier:", len(git(L, "log", "--format=%h", "--", "plans/round53_c1_classify.py").stdout.split()))

# ---------- T4: contested budget hides an all-P1 classifier's errors ----------
L = fresh("T4-contested-budget")
open(f"{L}/plans/round53_c1_classify.py", "w").write(ALLP1); freeze(L); commit(L, "freeze + classifier", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py")
contested = [x["id"] for x in TESTS[:45]]
write_labels(L, contested=set(contested)); commit(L, "labels: 45 split", "corpus/evidence/round53/oracle-labels.json")
counter(L, "T4")
