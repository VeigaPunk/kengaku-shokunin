#!/usr/bin/env python3
"""C1MutCounter: one byte-level mutation at a time against plans/round53_c1_triage.py; run --selftest; revert."""
import hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r53/C1MutCounter")
LANE = S / "lane"
TARGET = LANE / "plans/round53_c1_triage.py"
import os
PRISTINE = Path(os.environ.get("BASE_FILE", str(S / "pristine_triage.py")))
OUT = Path(os.environ.get("OUT", str(S / "work/results.json")))
TMP = S / "tmp"
TMP.mkdir(exist_ok=True)
SRC = PRISTINE.read_text().split("\n")
PRE_SHA = hashlib.sha256(PRISTINE.read_bytes()).hexdigest()

# (id, group, 1-based line, old, new, note)  old must occur exactly once on that line
M = [
 ("P01","PINS",81,'== cfg["POP_SHA"]','!= cfg["POP_SHA"]',"pop digest comparison inverted"),
 ("P02","PINS",82,'== cfg["PIN_TREE_SHA"]','!= cfg["PIN_TREE_SHA"]',"pin-tree digest comparison inverted"),
 ("P03","PINS",83,'== cfg["TESTS_INDEX_SHA"]','!= cfg["TESTS_INDEX_SHA"]',"tests-index digest comparison inverted"),
 ("P04","PINS",86,'if pop_ok and pin_ok:','if pop_ok or pin_ok:',"population walk gated by OR"),
 ("P05","PINS",94,'if p == cfg["EXCLUDED_PATH"]:','if p != cfg["EXCLUDED_PATH"]:',"excluded path test inverted"),
 ("P06","PINS",95,'(not f.exists())','(f.exists())',"excluded capture must be absent: clause dropped"),
 ("P07","PINS",97,'if not f.is_file():','if f.is_file():',"absent capture counter inverted"),
 ("P08","PINS",99,'== blobs.get(p):','!= blobs.get(p):',"blob-SHA1 match inverted"),
 ("P09","PINS",106,' and absent == 0','',"absent==0 clause dropped (equivalent given blob_bad/match)"),
 ("P10","PINS",106,'match == cfg["CAPTURES_EXPECTED"]','match >= cfg["CAPTURES_EXPECTED"]',"captures equality relaxed to >= (equivalent given files==EXPECTED+1)"),
 ("P11","PINS",106,'pop_ok and pin_ok and idx_ok and','pop_ok and pin_ok and',"tests-index digest clause dropped from PINS verdict"),
 ("P12","PINS",107,'exc_ok and ','',"excluded-blob clause dropped from PINS verdict"),
 ("P13","PINS",107,'+ 1)','+ 0)',"population count off by one (EXPECTED+0)"),
 ("F01","FREEZE",131,'sha256_file(clf) == d.get','sha256_file(clf) != d.get',"classifier digest comparison inverted"),
 ("F02","FREEZE",134,'if c_fz and c_lab and c_fz != c_lab:','if c_fz and c_lab and c_fz == c_lab:',"freeze-before-labels order test inverted"),
 ("F03","FREEZE",135,')[0] == 0',')[0] != 0',"is-ancestor test inverted"),
 ("F04","FREEZE",135,'order = git(lane, "merge-base", "--is-ancestor", c_fz, c_lab)[0] == 0','order = True',"ancestry check dropped"),
 ("F05","FREEZE",137,'ok = sha_ok and order and','ok = sha_ok and',"freeze ordering clause dropped from FREEZE verdict"),
 ("F06","FREEZE",137,' and bool(info["authors"])','',"non-empty author_seats clause dropped (equivalent: verdict gates on authors at L374)"),
 ("L01","LABELS",150,'len(set(r["labelers"])) != 2','len(set(r["labelers"])) < 2',"two-distinct-labelers test relaxed to <2"),
 ("L02","LABELS",152,' or set(r["labelers"]) & authors','',"labeler-is-author rejection branch deleted"),
 ("L03","LABELS",152,' or any(x not in ("Y", "N", "U") for x in r["labels"])','',"label-domain rejection branch deleted"),
 ("L04","LABELS",156,'if a == b and a in ("Y", "N"):','if a in ("Y", "N"):',"agreement requirement dropped: disagreeing pair decided"),
 ("L05","LABELS",150,'(not isinstance(r, dict) or ','(',"missing-row (non-dict) rejection branch deleted"),
 ("L06","LABELS",150,'not isinstance(r.get("labelers"), list) or ','',"labelers-is-list rejection branch deleted"),
 ("O01","ORACLE",198,'if (v2[t] == "P1") != (y == "Y")','if (v2[t] == "P1") == (y == "Y")',"v2 disagreement count inverted"),
 ("O02","ORACLE",199,'if (r52[t] == "P1") != (y == "Y")','if (r52[t] == "P1") == (y == "Y")',"r52 control disagreement count inverted"),
 ("O03","ORACLE",203,'dis52 >= CONTROL_RATIO * max(dis, 1)','dis52 > CONTROL_RATIO * max(dis, 1)',"control ratio >= relaxed to >"),
 ("O04","ORACLE",203,' and dis52 >= CONTROL_MIN','',"control minimum clause dropped"),
 ("O05","ORACLE",204,'and not extra and','and',"extra label-row clause dropped"),
 ("O06","ORACLE",204,'and not uncl and','and',"unclassified=0 clause dropped"),
 ("O07","ORACLE",204,'ok = (n == cfg["TESTS_TOTAL"] and not bad and','ok = (n == cfg["TESTS_TOTAL"] and',"bad-label-row clause dropped"),
 ("O08","ORACLE",204,'n == cfg["TESTS_TOTAL"] and ','',"tests-count clause dropped (equivalent given TESTS_INDEX_SHA pin)"),
 ("O09","ORACLE",205,'and dis <= lim','and dis < lim',"disagreement limit <= relaxed to < (boundary)"),
 ("O10","ORACLE",205,'len(contested) <= ORACLE_MAX_CONTESTED * n','len(contested) < ORACLE_MAX_CONTESTED * n',"contested limit <= relaxed to < (boundary)"),
 ("O11","ORACLE",205,'and ctl_ok)',')',"ORACLE-CONTROL clause dropped from verdict"),
 ("O12","ORACLE",202,'lim = ORACLE_MAX_DISAGREE * max(1, len(decided))','lim = ORACLE_MAX_DISAGREE * max(1, len(ids))',"disagreement denominator: decided -> all tests"),
 ("K01","CONFIRM",266,'if r.get("confirmed") is not True:','if not r.get("confirmed"):',"confirmed weakened from `is not True` to falsy"),
 ("K02","CONFIRM",270,'elif r["task"] not in cand or tid not in {x["id"] for x in cand[r["task"]]}:','elif False:',"never-read / v2-P1 candidacy check deleted"),
 ("K03","CONFIRM",272,'elif r["task"] in seen_tasks:','elif False:',"duplicate-task rejection deleted"),
 ("K04","CONFIRM",274,'< QUOTE_MIN_CHARS or norm(r["quote"]) not in span:','< QUOTE_MIN_CHARS:',"quote-inside-test-span check deleted"),
 ("K05","CONFIRM",274,'< QUOTE_MIN_CHARS or','<= QUOTE_MIN_CHARS or',"quote length >= 20 relaxed to > 20 (boundary)"),
 ("K06","CONFIRM",276,' or r["reader"].startswith("KengakuR53")','',"KengakuR53 reader rejection deleted"),
 ("K07","CONFIRM",278,' or r["reader"] not in str(rep)','',"reader-name-in-report-path check deleted"),
 ("K08","CONFIRM",280,'elif r["task"] not in rep.read_text(encoding="utf-8", errors="replace"):','elif False:',"report-names-task check deleted"),
 ("K09","CONFIRM",265,'src[t["lineno"] - 1:t["end_lineno"]]','src[t["lineno"]:t["end_lineno"]]',"test span drops its def line"),
 ("K10","CONFIRM",268,'elif t is None or t["task"] != r.get("task"):','elif t is None:',"test_id/task consistency check deleted (reason text changes only)"),
 ("K11","CONFIRM",289,'ok = len(good) >= cfg["CONFIRM_MIN"]','ok = len(good) > cfg["CONFIRM_MIN"]',"CONFIRM minimum >= relaxed to > (cfg-level, fixture overrides)"),
 ("A01","PRIOR-ART",324,'if task not in confirmed:','if False:',"task-confirmed check deleted in prior-art"),
 ("A02","PRIOR-ART",326,'elif v not in ("phenomenon-new", "phenomenon-known"):','elif False:',"verdict-domain check deleted"),
 ("A03","PRIOR-ART",328,' or "example.org" in r["url"]','',"example.org rejection deleted (sole-check route)"),
 ("A04","PRIOR-ART",328,'elif not re.match(r"https?://[^/\\s]+\\.[^/\\s]+/", str(r.get("url", "")) + "/") or','elif',"URL shape check deleted"),
 ("A05","PRIOR-ART",335,'8 <= len(q.split()) <= 25','7 <= len(q.split()) <= 25',"quote word-count lower bound 8 -> 7"),
 ("A06","PRIOR-ART",335,'8 <= len(q.split()) <= 25','8 < len(q.split()) <= 25',"quote word-count lower bound <= swapped to < (8 excluded)"),
 ("A07","PRIOR-ART",335,'len(q.split()) <= 25','len(q.split()) <= 26',"quote word-count upper bound 25 -> 26"),
 ("A08","PRIOR-ART",335,' or q not in norm(text):',':',"quote-in-archive check deleted"),
 ("A09","PRIOR-ART",337,' and task not in text:',':',"known-row: task-name-in-fetch alternative deleted"),
 ("A10","PRIOR-ART",337,'elif v == "phenomenon-known" and not any(n in text for n in tests_of.get(task, [])) and task not in text:','elif False:',"known-row naming check deleted"),
 ("A11","PRIOR-ART",341,'if not isinstance(sw, list) or len(sw) < 2:','if not isinstance(sw, list) or len(sw) < 1:',"new-row sweep minimum 2 -> 1"),
 ("A12","PRIOR-ART",346,'if st is None or task in st or any(','if st is None or any(',"sweep: task-name check deleted"),
 ("A13","PRIOR-ART",346,' or any(n in st for n in tests_of.get(task, [])):',':',"sweep: test-name check deleted"),
 ("A14","PRIOR-ART",314,'if not str(r.get(key, "")).startswith(f"{RUN_DIR}/fetched/") or not f.is_file():','if not f.is_file():',"fetch-path-under-fetched/ check deleted"),
 ("A15","PRIOR-ART",316,'if sha256_file(f) != r.get(key + "_sha256"):','if sha256_file(f) == r.get(key + "_sha256"):',"fetch digest comparison inverted"),
 ("A16","PRIOR-ART",358,'and new >= 1 and not rej','and new >= 0 and not rej',"new>=1 score rule relaxed to >=0"),
 ("A17","PRIOR-ART",358,' and not rej',"",'one-rejected-row rule deleted'),
 ("A18","PRIOR-ART",358,'bool(confirmed) and ','',"non-empty confirmed clause dropped (equivalent: rej/covered gates)"),
 ("C01","CONST",29,'0230b68c666c','0230b68d666c',"POP_SHA first digits (CFG; selftest overrides cfg)"),
 ("C02","CONST",32,'TESTS_TOTAL = 305','TESTS_TOTAL = 306',"TESTS_TOTAL 305->306 (CFG; selftest overrides)"),
 ("C03","CONST",33,'CAPTURES_EXPECTED = 183','CAPTURES_EXPECTED = 182',"CAPTURES_EXPECTED 183->182 (CFG; selftest overrides)"),
 ("C04","CONST",37,'ORACLE_MAX_DISAGREE = 0.03','ORACLE_MAX_DISAGREE = 0.5',"ORACLE_MAX_DISAGREE 0.03->0.5"),
 ("C05","CONST",38,'ORACLE_MAX_CONTESTED = 0.15','ORACLE_MAX_CONTESTED = 0.5',"ORACLE_MAX_CONTESTED 0.15->0.5"),
 ("C06","CONST",39,'CONTROL_RATIO = 2','CONTROL_RATIO = 1',"CONTROL_RATIO 2->1"),
 ("C07","CONST",40,'CONTROL_MIN = 10','CONTROL_MIN = 11',"CONTROL_MIN 10->11 (selftest rebinds to 1 except one case)"),
 ("C08","CONST",41,'CONFIRM_MIN = 3','CONFIRM_MIN = 2',"CONFIRM_MIN 3->2 (CFG; selftest overrides)"),
 ("C09","CONST",42,'URL_MIN = 3','URL_MIN = 2',"URL_MIN 3->2 (CFG; selftest overrides)"),
 ("C10","CONST",43,'QUOTE_MIN_CHARS = 20','QUOTE_MIN_CHARS = 19',"QUOTE_MIN_CHARS 20->19"),
 ("C11","CONST",43,'QUOTE_MIN_CHARS = 20','QUOTE_MIN_CHARS = 21',"QUOTE_MIN_CHARS 20->21"),
 ("C12","CONST",35,'EXCLUDED_BLOB = "3269e74e','EXCLUDED_BLOB = "3269e74f',"EXCLUDED_BLOB first digits (CFG; selftest overrides)"),
 ("K12","CONFIRM",240,' and not seen_before(t["task"], texts)','',"never-read check: task-seen-in-base-texts exclusion deleted"),
 ("K13","CONFIRM",240,' and t["task"] not in r52_conf','',"never-read check: round-52-confirmed exclusion deleted"),
 ("A19","PRIOR-ART",339,'elif v == "phenomenon-new":','elif False:',"whole sweep check (phenomenon-new) deleted"),
]

def run_selftest():
    p = subprocess.run([sys.executable, "plans/round53_c1_triage.py", "--selftest"], cwd=LANE,
                       capture_output=True, text=True, env={"TMPDIR": str(TMP), "PATH": "/usr/bin:/bin"}, timeout=600)
    return p.returncode, p.stdout, p.stderr

def cases_line(out):
    m = re.search(r"^SELFTEST cases=\d+ failures=\d+$", out, re.M)
    return m.group(0) if m else None

shutil.copyfile(PRISTINE, TARGET)
base_rc, base_out, base_err = run_selftest()
BASE_LINE = cases_line(base_out)
print("BASELINE rc=%d line=%r" % (base_rc, BASE_LINE))
assert base_rc == 0 and BASE_LINE and BASE_LINE.endswith("failures=0"), (base_rc, BASE_LINE)

def apply(m):
    mid, grp, ln, old, new, note = m
    lines = list(SRC)
    line = lines[ln - 1]
    cnt = line.count(old)
    if cnt != 1:
        raise SystemExit(f"{mid}: old occurs {cnt}x on line {ln}: {line!r}")
    lines[ln - 1] = line.replace(old, new)
    return "\n".join(lines)

results = []
def record(mid, grp, ln, old, new, note, text=None, rc=None, out="", err=""):
    line = cases_line(out)
    fails = re.findall(r"^SELFTEST (\S+) rc=(\d+) FAIL$", out, re.M)
    tb = "Traceback" in err
    killed = (rc != 0) or (line != BASE_LINE) or tb
    first = fails[0][0] if fails else ("traceback" if tb else ("rc-only" if killed else None))
    results.append(dict(id=mid, group=grp, line=ln, old=old, new=new, note=note, rc=rc, cases_line=line,
                        killed=bool(killed), killed_by=first, fail_cases=[f[0] for f in fails], traceback=tb,
                        err_tail=err.strip().splitlines()[-1] if err.strip() else ""))
    print(f"{mid:4} rc={rc} killed={'y' if killed else 'n'} by={first} line={line}")

record("N00", "NULL", 0, "", "", "null mutant: pristine file, no change", rc=base_rc, out=base_out, err=base_err)
assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == hashlib.sha256(PRISTINE.read_bytes()).hexdigest() or True

for m in M:
    mid, grp, ln, old, new, note = m
    text = apply(m)
    compile(text, mid, "exec")  # mutant must be valid Python
    TARGET.write_text(text)
    try:
        rc, out, err = run_selftest()
        record(mid, grp, ln, old, new, note, rc=rc, out=out, err=err)
    finally:
        shutil.copyfile(PRISTINE, TARGET)
        shutil.rmtree(TMP, ignore_errors=True); TMP.mkdir(exist_ok=True)
        assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == hashlib.sha256(PRISTINE.read_bytes()).hexdigest(), "restore failed"

post = hashlib.sha256(TARGET.read_bytes()).hexdigest()
PRE_SHA = hashlib.sha256(PRISTINE.read_bytes()).hexdigest()
OUT.write_text(json.dumps(dict(pristine_sha256=PRE_SHA, restored_sha256=post, base_line=BASE_LINE, results=results), indent=1))
k = sum(r["killed"] for r in results if r["id"] != "N00")
print(f"TOTAL mutants={len(results)-1} killed={k} survived={len(results)-1-k} restored_sha_ok={post==PRE_SHA}")
