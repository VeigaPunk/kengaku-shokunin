import json, shutil, hashlib, subprocess, re, sys, os
from pathlib import Path
S = Path("/fast/scratch/hyaku/kengaku-r52/w2-W2CritC1Reach")
BASE = S / "base"
FX = S / "fx"
COUNTER = "plans/round52_c1_grader_audit.py"
POP = json.load(open(BASE / "plans/round52-tasks.json"))
CANDS = ["bn-fit-modify","build-cython-ext","caffe-cifar-10","cancel-async-tasks","code-from-image","crack-7z-hash","db-wal-recovery","extract-elf","financial-document-processor","hf-model-inference","kv-store-grpc","large-scale-text-editing","log-summary-date-ranges","mteb-leaderboard","mteb-retrieve","multi-source-data-merger","openssl-selfsigned-cert","password-recovery","path-tracing","path-tracing-reverse","prove-plus-comm","pytorch-model-cli","pytorch-model-recovery","raman-fitting","sam-cell-seg","torch-tensor-parallelism","vulnerable-secret","winning-avg-corewars","write-compressor"]
G = "corpus/evidence/round52/graders"

def fresh(name):
    d = FX / name
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(BASE, d)
    return d

def sums_for(d, paths):
    lines = []
    for p in sorted(paths):
        lines.append(f"{hashlib.sha256((d/G/p).read_bytes()).hexdigest()}  ./{p}")
    (d/G/"SHA256SUMS").write_text("\n".join(lines) + "\n")

def set_sum(d, path, data):
    sp = d/G/"SHA256SUMS"
    lines = sp.read_text().splitlines()
    new = []
    for l in lines:
        if l.endswith(f"./{path}"):
            new.append(f"{hashlib.sha256(data).hexdigest()}  ./{path}")
        else: new.append(l)
    sp.write_text("\n".join(new) + "\n")

def write_conf(d, rows):
    (d/"corpus/evidence/round52/confirmations.json").write_text(json.dumps(rows, indent=1))

def write_pa(d, text):
    (d/"corpus/evidence/round52/prior-art.md").write_text(text)

HONEST_CONF = [
 {"task":"code-from-image","quote":"def test_output_file_exists","reader":"second-reader-stub","confirmed":True},
 {"task":"mteb-retrieve","quote":"def test_result_exists","reader":"second-reader-stub","confirmed":True},
]
PA3 = "Findings priced against https://a.example/1 and https://a.example/2 and https://a.example/3\n"
ALL_CAP = {p for v in POP["capture_population"].values() for p in v}

# fx00: no captures at all
d = fresh("fx00-no-captures"); shutil.rmtree(d/G)
# fx01: only candidate graders captured, population untouched
d = fresh("fx01-partial-candidates-unedited")
keep = {p for t in CANDS for p in POP["capture_population"][t]}
for p in ALL_CAP - keep:
    (d/G/p).unlink()
write_conf(d, HONEST_CONF); write_pa(d, PA3)
# fx02: only candidate graders captured AND population rewritten to match (self-consistent)
d = fresh("fx02-partial-candidates-repopulated")
keep = {p for t in CANDS for p in POP["capture_population"][t]}
for p in ALL_CAP - keep:
    (d/G/p).unlink()
pop = json.loads(json.dumps(POP))
pop["tasks"] = {t: POP["tasks"][t] for t in CANDS}
pop["task_count"] = len(CANDS)
pop["capture_population"] = {t: POP["capture_population"][t] for t in CANDS}
pop["capture_file_count"] = len(keep)
(d/"plans/round52-tasks.json").write_text(json.dumps(pop, indent=1))
write_conf(d, HONEST_CONF); write_pa(d, PA3)
# fx03: complete 184 with ONE forged capture (sanitize) re-pinned in SHA256SUMS; population untouched
d = fresh("fx03-forged-sanitize-repinned")
stub = b"def test_ok():\n    assert True\n"
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, HONEST_CONF); write_pa(d, PA3)
# fx03b: same captures; trivial confirmations (L1 as reader, string 'false' confirmed, quote is a space)
d = fresh("fx03b-trivial-confirmations")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, [
 {"task":"code-from-image","quote":" ","reader":"KengakuR52a3","confirmed":"false"},
 {"task":"mteb-retrieve","quote":"assert","reader":"KengakuR52a3","confirmed":"no"},
]); write_pa(d, PA3)
# fx03c: as fx03b, but prior-art nonsense (three example URLs, all phenomenon-known, no fetch)
d = fresh("fx03c-prior-art-nonsense")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, HONEST_CONF)
write_pa(d, "code-from-image: phenomenon-known https://example.org/a\nmteb-retrieve: phenomenon-known https://example.org/b\nx https://example.org/c\n")
# fx03d: confirmations present but in dict wrapper (fail-closed?)
d = fresh("fx03d-confirmations-dict-wrapped")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
(d/"corpus/evidence/round52/confirmations.json").write_text(json.dumps({"confirmations": HONEST_CONF}))
write_pa(d, PA3)
# fx03e: same task twice (dedupe check)
d = fresh("fx03e-same-task-twice")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, [HONEST_CONF[0], dict(HONEST_CONF[0], quote="def test_output_file_exists")]); write_pa(d, PA3)
# fx03f: reader empty string (gating check)
d = fresh("fx03f-reader-empty")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, [dict(r, reader="") for r in HONEST_CONF]); write_pa(d, PA3)
# fx03g: prior-art with only 2 URLs (gating check)
d = fresh("fx03g-prior-art-two-urls")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, HONEST_CONF); write_pa(d, "https://a.example/1 https://a.example/2\n")
# fx03h: prior-art three URLs of one page with query strings, every finding phenomenon-known
d = fresh("fx03h-prior-art-same-page-known")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, HONEST_CONF)
write_pa(d, "phenomenon-known for all: https://github.com/x/y?1 https://github.com/x/y?2 https://github.com/x/y?3\n")
# fx03i: confirmations file absent (control)
d = fresh("fx03i-no-confirmations")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_pa(d, PA3)
# fx04: A5 launder: real bn-fit-modify grader DELETED (a P1 task), EXCLUDED.md names it with its own digest
d = fresh("fx04-a5-launders-deleted-p1")
victim = "bn-fit-modify/tests/test_outputs.py"
vsha = hashlib.sha256((d/G/victim).read_bytes()).hexdigest()
(d/G/victim).unlink()
(d/G/"EXCLUDED.md").write_text(f"Excluded path: `corpus/evidence/round52/graders/{victim}`\n- sha256: `{vsha}`\n")
write_conf(d, HONEST_CONF); write_pa(d, PA3)
# fx05: labels = classifier output copied (same-classifier agreement) and fx05b labels all V0
d = fresh("fx05-labels-same-classifier")
(d/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d, HONEST_CONF); write_pa(d, PA3)
r = subprocess.run([sys.executable, str(BASE/COUNTER), "--lane", str(d)], capture_output=True, text=True, cwd=d)
lab = []
for line in r.stdout.splitlines():
    pass
import importlib.util
spec = importlib.util.spec_from_file_location("ctr", str(BASE/COUNTER)); ctr = importlib.util.module_from_spec(spec); spec.loader.exec_module(ctr)
pop_, records, *_ = ctr.collect(d)
(d/"corpus/evidence/round52/labels.json").write_text(json.dumps({"labels":[{"task":t,"class":records[t]["class"]} for t in records if records[t].get("class")]}))
d2 = fresh("fx05b-labels-all-V0")
(d2/G/"sanitize-git-repo/tests/test_outputs.py").write_bytes(stub)
set_sum(d2, "sanitize-git-repo/tests/test_outputs.py", stub)
write_conf(d2, HONEST_CONF); write_pa(d2, PA3)
(d2/"corpus/evidence/round52/labels.json").write_text(json.dumps({"labels":[{"task":t,"class":"V0"} for t in POP["tasks"]]}))
print("built", sorted(p.name for p in FX.iterdir()))
