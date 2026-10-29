#!/usr/bin/env python3
"""Round 53, claim C1: Terminal-Bench 2.0 presence-only grader triage, v2 (counter).

Replaces the round-52 counter's trust model (Q42): every input the predicate trusts is pinned by a digest
constant in THIS file or by git history, the per-test class is an AST classifier scored against an
independent blind-label oracle, a forged-but-complete input must fail, and the prior-art leg re-reads
archived fetches.  Legs and the one predicate sentence are frozen in ``plans/round-53-claims.md``.

    python3 plans/round53_c1_triage.py --lane .                # the counting command (clean clone of the tip)
    python3 plans/round53_c1_triage.py --lane . --candidates   # never-read tasks with a v2 P1 test (no predicate)
    python3 plans/round53_c1_triage.py --selftest

Exit: 0 predicate holds · 1 predicate fails · 2 setup.  Honours TMPDIR; no /tmp literal.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# ---- pins (frozen at the round-53 claims commit) -------------------------------------------------
POP_SHA = "0230b68c666c1e0649b42d61d7121a30eedf247411642bbf397e3390436b5cfc"       # plans/round52-tasks.json
PIN_TREE_SHA = "96b472489cbec0f4f6319db510b40284efa92b01b4badbc112d922662d42cbb9"  # corpus/evidence/round53/pin-tree-2fd12b88.json
TESTS_INDEX_SHA = "579d567fd66f5fc0bc71957cdc887e9bb952c63b3fd9d2726e67c963897c7330"  # corpus/evidence/round53/tests-index.json
TESTS_TOTAL = 305
CAPTURES_EXPECTED = 183
EXCLUDED_PATH = "sanitize-git-repo/tests/test_outputs.py"
EXCLUDED_BLOB = "3269e74e727fda61c936ca34b8f3bfaacf199dda"
BASE_TIP = "536925b5320fa64298030b4ee76a58fc4b82723f"                             # lane tip the claims were frozen against
ORACLE_MAX_DISAGREE = 0.03      # of decided tests
ORACLE_MAX_CONTESTED = 0.15     # of all tests
CONTROL_RATIO = 2               # r52 classifier's disagree must be >= 2x v2's ...
CONTROL_MIN = 10                # ... and >= 10, else the leg is vacuous
CONFIRM_MIN = 3
URL_MIN = 3
QUOTE_MIN_CHARS = 20
RUN_DIR = "corpus/evidence/round53"

CFG = dict(POP_SHA=POP_SHA, PIN_TREE_SHA=PIN_TREE_SHA, TESTS_INDEX_SHA=TESTS_INDEX_SHA, TESTS_TOTAL=TESTS_TOTAL,
           CAPTURES_EXPECTED=CAPTURES_EXPECTED, EXCLUDED_PATH=EXCLUDED_PATH, EXCLUDED_BLOB=EXCLUDED_BLOB,
           BASE_TIP=BASE_TIP, CONFIRM_MIN=CONFIRM_MIN, URL_MIN=URL_MIN)


def sha256_file(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def blob_sha1(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def git(lane: Path, *a: str) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", str(lane), *a], capture_output=True, text=True)
    return p.returncode, p.stdout


def load_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


# ---- leg 1: PINS ---------------------------------------------------------------------------------
def leg_pins(lane: Path, cfg: dict):
    L, ok = [], True
    pop_p = lane / "plans/round52-tasks.json"
    pin_p = lane / RUN_DIR / "pin-tree-2fd12b88.json"
    idx_p = lane / RUN_DIR / "tests-index.json"
    pop_ok = sha256_file(pop_p) == cfg["POP_SHA"]
    pin_ok = sha256_file(pin_p) == cfg["PIN_TREE_SHA"]
    idx_ok = sha256_file(idx_p) == cfg["TESTS_INDEX_SHA"]
    match = bad = absent = 0
    exc_ok = False
    if pop_ok and pin_ok:
        pop = json.loads(pop_p.read_text())
        pin = json.loads(pin_p.read_text())
        blobs = {b["path"]: b["sha"] for b in pin["blobs"]}
        paths = [p for v in pop["capture_population"].values() for p in v]
        cap = lane / "corpus/evidence/round52/graders"
        for p in paths:
            f = cap / p
            if p == cfg["EXCLUDED_PATH"]:
                exc_ok = (not f.exists()) and blobs.get(p) == cfg["EXCLUDED_BLOB"]
                continue
            if not f.is_file():
                absent += 1
            elif blob_sha1(f.read_bytes()) == blobs.get(p):
                match += 1
            else:
                bad += 1
        n_paths = len(paths)
    else:
        n_paths = -1
    ok = (pop_ok and pin_ok and idx_ok and match == cfg["CAPTURES_EXPECTED"] and bad == 0 and absent == 0
          and exc_ok and n_paths == cfg["CAPTURES_EXPECTED"] + 1)
    L.append(f"PINS population_sha={'ok' if pop_ok else 'BAD'} pin_tree_sha={'ok' if pin_ok else 'BAD'} "
             f"tests_index_sha={'ok' if idx_ok else 'BAD'} captures_blob_match={match} blob_bad={bad} absent={absent} "
             f"excluded_blob={'ok' if exc_ok else 'BAD'} files={n_paths}")
    return ok, L


# ---- leg 2: FREEZE + ORACLE ----------------------------------------------------------------------
def first_add(lane: Path, rel: str) -> str | None:
    rc, out = git(lane, "log", "--diff-filter=A", "--format=%H", "--reverse", "--", rel)
    lines = [x for x in out.split() if x]
    return lines[0] if rc == 0 and lines else None


def leg_freeze(lane: Path):
    L = []
    fz = lane / "plans/round53-c1-freeze.json"
    clf = lane / "plans/round53_c1_classify.py"
    lab = lane / RUN_DIR / "oracle-labels.json"
    info = {"authors": set(), "ok": False}
    if not (fz.is_file() and clf.is_file() and lab.is_file()):
        L.append(f"FREEZE absent freeze={fz.is_file()} classifier={clf.is_file()} labels={lab.is_file()}")
        return False, L, info
    d = json.loads(fz.read_text())
    sha_ok = sha256_file(clf) == d.get("classifier_sha256")
    c_fz, c_lab = first_add(lane, "plans/round53-c1-freeze.json"), first_add(lane, f"{RUN_DIR}/oracle-labels.json")
    order = False
    if c_fz and c_lab and c_fz != c_lab:
        order = git(lane, "merge-base", "--is-ancestor", c_fz, c_lab)[0] == 0
    info["authors"] = set(d.get("author_seats") or [])
    ok = sha_ok and order and bool(info["authors"])
    info["ok"] = ok
    L.append(f"FREEZE classifier_sha={'ok' if sha_ok else 'BAD'} order={'freeze-before-labels' if order else 'UNPROVEN'} "
             f"authors={len(info['authors'])}")
    return ok, L, info


def load_labels(lane: Path, idx_ids: list[str], authors: set):
    d = json.loads((lane / RUN_DIR / "oracle-labels.json").read_text())
    rows = d.get("labels", {})
    decided, contested, bad = {}, [], []
    for tid in idx_ids:
        r = rows.get(tid)
        if (not isinstance(r, dict) or not isinstance(r.get("labelers"), list) or len(set(r["labelers"])) != 2
                or not isinstance(r.get("labels"), list) or len(r["labels"]) != 2
                or any(x not in ("Y", "N", "U") for x in r["labels"]) or set(r["labelers"]) & authors):
            bad.append(tid)
            continue
        a, b = r["labels"]
        if a == b and a in ("Y", "N"):
            decided[tid] = a
        else:
            contested.append(tid)
    return decided, contested, bad, set(rows) - set(idx_ids)


def v2_classes(lane: Path, tests: list[dict]):
    m = load_mod(lane / "plans/round53_c1_classify.py", "r53_classify")
    out, uncl = {}, []
    by_file: dict[str, dict] = {}
    for t in tests:
        if t["file"] not in by_file:
            src = (lane / "corpus/evidence/round52/graders" / t["file"]).read_text(encoding="utf-8", errors="replace")
            by_file[t["file"]] = m.classify_source(src)
        key = f"{t['class']}.{t['name']}" if t["class"] else t["name"]
        c = by_file[t["file"]].get(key)
        if c not in ("P1", "P0"):
            uncl.append(t["id"])
            c = "P0"
        out[t["id"]] = c
    return out, uncl


def r52_classes(lane: Path, tests: list[dict]):
    m = load_mod(lane / "plans/round52_c1_grader_audit.py", "r52_audit")
    out, by_file = {}, {}
    for t in tests:
        if t["file"] not in by_file:
            body = (lane / "corpus/evidence/round52/graders" / t["file"]).read_text(encoding="utf-8", errors="replace")
            by_file[t["file"]] = {x["test"]: x["class"] for x in m.classify_tests(body)}
        out[t["id"]] = "P1" if (t["class"] is None and by_file[t["file"]].get(t["name"]) == "P1") else "P0"
    return out


def leg_oracle(lane: Path, cfg: dict, info: dict):
    L = []
    idx = json.loads((lane / RUN_DIR / "tests-index.json").read_text())["tests"]
    ids = [t["id"] for t in idx]
    decided, contested, bad, extra = load_labels(lane, ids, info["authors"])
    v2, uncl = v2_classes(lane, idx)
    r52 = r52_classes(lane, idx)
    dis = sum(1 for t, y in decided.items() if (v2[t] == "P1") != (y == "Y"))
    dis52 = sum(1 for t, y in decided.items() if (r52[t] == "P1") != (y == "Y"))
    dis0 = sum(1 for y in decided.values() if y == "Y")
    n = len(ids)
    lim = ORACLE_MAX_DISAGREE * max(1, len(decided))
    ctl_ok = dis52 >= CONTROL_RATIO * max(dis, 1) and dis52 >= CONTROL_MIN
    ok = (n == cfg["TESTS_TOTAL"] and not bad and not extra and not uncl and len(decided) > 0
          and dis <= lim and len(contested) <= ORACLE_MAX_CONTESTED * n and ctl_ok)
    L.append(f"ORACLE tests={n} labelled_ok={n - len(bad)} bad_label_rows={len(bad)} decided={len(decided)} "
             f"contested={len(contested)} oracle_Y={sum(1 for y in decided.values() if y == 'Y')} "
             f"v2_P1={sum(1 for c in v2.values() if c == 'P1')} unclassified={len(uncl)} disagree={dis} "
             f"limit={lim:.1f}")
    L.append(f"ORACLE-CONTROL r52_classifier_disagree={dis52} all_P0_disagree={dis0} "
             f"control_ok={'yes' if ctl_ok else 'NO(leg vacuous)'}")
    return ok, L, v2, decided


# ---- leg 3: CONFIRM ------------------------------------------------------------------------------
def never_read_blocklist(lane: Path, cfg: dict) -> tuple[list[str], dict]:
    """Texts of the pre-round lane at BASE_TIP, excluding the round-52 triage entry itself."""
    rc, out = git(lane, "ls-tree", "-r", "--name-only", cfg["BASE_TIP"], "corpus/knowledge")
    files = [f for f in out.split() if f != "corpus/knowledge/tb2-grader-vacuity-triage.md"] if rc == 0 else []
    files += ["SCORECARD.md", "LOG.md", "SKILL.md", "corpus/README.md"]
    texts = {}
    for f in files:
        rc, t = git(lane, "show", f"{cfg['BASE_TIP']}:{f}")
        if rc == 0:
            texts[f] = t
    rc, t = git(lane, "show", f"{cfg['BASE_TIP']}:corpus/evidence/round52/confirmations.json")
    r52_conf = {c["task"] for c in json.loads(t)} if rc == 0 else set()
    return sorted(r52_conf), texts


def seen_before(task: str, texts: dict) -> list[str]:
    pat = re.compile(r"(?<![A-Za-z0-9-])" + re.escape(task) + r"(?![A-Za-z0-9-])")
    return [f for f, t in texts.items() if pat.search(t)]


def candidates(lane: Path, cfg: dict, v2: dict, idx: list[dict]):
    r52_conf, texts = never_read_blocklist(lane, cfg)
    out = {}
    for t in idx:
        if v2.get(t["id"]) == "P1" and t["task"] not in r52_conf and not seen_before(t["task"], texts):
            out.setdefault(t["task"], []).append(t)
    return out


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def leg_confirm(lane: Path, cfg: dict, info: dict, v2: dict, idx: list[dict]):
    L, good, rej = [], [], []
    p = lane / RUN_DIR / "confirmations.json"
    cand = candidates(lane, cfg, v2, idx)
    by_id = {t["id"]: t for t in idx}
    rows = json.loads(p.read_text()) if p.is_file() else []
    if not isinstance(rows, list):
        rows, rej = [], ["non-list"]
    seen_tasks = set()
    for r in rows:
        why = None
        try:
            tid = r.get("test_id")
            t = by_id.get(tid)
            rep = lane / str(r.get("report", ""))
            src = (lane / "corpus/evidence/round52/graders" / t["file"]).read_text(encoding="utf-8", errors="replace").splitlines() if t else []
            span = norm("\n".join(src[t["lineno"] - 1:t["end_lineno"]])) if t else ""
            if r.get("confirmed") is not True:
                why = "confirmed-not-true"
            elif t is None or t["task"] != r.get("task"):
                why = "unknown-test-id"
            elif r["task"] not in cand or tid not in {x["id"] for x in cand[r["task"]]}:
                why = "not-a-never-read-v2-P1-candidate"
            elif r["task"] in seen_tasks:
                why = "duplicate-task"
            elif len(norm(str(r.get("quote", "")))) < QUOTE_MIN_CHARS or norm(r["quote"]) not in span:
                why = "quote-short-or-outside-test-span"
            elif not r.get("reader") or r["reader"] in info["authors"] or r["reader"].startswith("KengakuR53"):
                why = "reader-is-author"
            elif not rep.is_file() or sha256_file(rep) != r.get("report_sha256") or r["reader"] not in str(rep):
                why = "reader-report-missing-or-digest-mismatch"
            elif r["task"] not in rep.read_text(encoding="utf-8", errors="replace"):
                why = "report-does-not-name-task"
        except Exception as e:  # noqa: BLE001
            why = f"error {type(e).__name__}"
        if why:
            rej.append(f"{r.get('task') if isinstance(r, dict) else '?'}:{why}")
        else:
            seen_tasks.add(r["task"])
            good.append(r["task"])
    ok = len(good) >= cfg["CONFIRM_MIN"]
    L.append(f"CONFIRM candidates_never_read={len(cand)} new_confirmed={len(good)} rejected={len(rej)} target>={cfg['CONFIRM_MIN']}")
    for x in rej:
        L.append(f"  REJECTED {x}")
    return ok, L, good


# ---- leg 4: PRIOR-ART ----------------------------------------------------------------------------
def url_key(u: str) -> str:
    return re.sub(r"[?#].*$", "", u.strip().lower().rstrip("/"))


def leg_prior_art(lane: Path, cfg: dict, confirmed: list[str], idx: list[dict]):
    L, rej, urls, new, known = [], [], set(), 0, 0
    p = lane / RUN_DIR / "prior-art.json"
    rows = json.loads(p.read_text()) if p.is_file() else []
    if not isinstance(rows, list):
        rows, rej = [], ["non-list"]
    tests_of = {}
    for t in idx:
        tests_of.setdefault(t["task"], []).append(t["name"])
    covered = set()

    def fetched(r, key):
        f = lane / str(r.get(key, ""))
        if not str(r.get(key, "")).startswith(f"{RUN_DIR}/fetched/") or not f.is_file():
            return None
        if sha256_file(f) != r.get(key + "_sha256"):
            return None
        return f.read_text(encoding="utf-8", errors="replace")

    for r in rows:
        why = None
        try:
            v, task = r.get("verdict"), r.get("task")
            if task not in confirmed:
                why = "task-not-confirmed"
            elif v not in ("phenomenon-new", "phenomenon-known"):
                why = "bad-verdict"
            elif not re.match(r"https?://[^/\s]+\.[^/\s]+/", str(r.get("url", "")) + "/") or "example.org" in r["url"]:
                why = "bad-url"
            else:
                text = fetched(r, "fetched")
                q = norm(str(r.get("quote", "")))
                if text is None:
                    why = "fetch-missing-or-digest-mismatch"
                elif not (8 <= len(q.split()) <= 25) or q not in norm(text):
                    why = "quote-not-8to25-words-or-not-in-fetch"
                elif v == "phenomenon-known" and not any(n in text for n in tests_of.get(task, [])) and task not in text:
                    why = "known-fetch-never-names-the-task-or-its-tests"
                elif v == "phenomenon-new":
                    sw = r.get("sweep")
                    if not isinstance(sw, list) or len(sw) < 2:
                        why = "new-needs-two-sweep-fetches"
                    else:
                        for s in sw:
                            st = fetched(s, "file")
                            if st is None or task in st or any(n in st for n in tests_of.get(task, [])):
                                why = "sweep-fetch-missing-or-names-the-task"
                                break
            if not why:
                urls.add(url_key(r["url"]))
                covered.add(task)
                new += r["verdict"] == "phenomenon-new"
                known += r["verdict"] == "phenomenon-known"
        except Exception as e:  # noqa: BLE001
            why = f"error {type(e).__name__}"
        if why:
            rej.append(f"{r.get('task') if isinstance(r, dict) else '?'}:{why}")
    ok = covered == set(confirmed) and bool(confirmed) and len(urls) >= cfg["URL_MIN"] and new >= 1 and not rej
    L.append(f"PRIOR-ART rows={len(rows)} tasks_covered={len(covered)}/{len(confirmed)} known={known} new={new} "
             f"urls={len(urls)} rejected={len(rej)} target: urls>={cfg['URL_MIN']} new>=1")
    for x in rej:
        L.append(f"  REJECTED {x}")
    return ok, L


# ---- driver --------------------------------------------------------------------------------------
def verdict(lane: Path, cfg: dict, candidates_only=False) -> tuple[int, list[str]]:
    lines: list[str] = []
    ok_pins, l = leg_pins(lane, cfg)
    lines += l
    ok_fz, l, info = leg_freeze(lane)
    lines += l
    ok_or = ok_cf = ok_pa = False
    if ok_pins and (lane / "plans/round53_c1_classify.py").is_file() and (lane / RUN_DIR / "oracle-labels.json").is_file() and info["authors"]:
        ok_or, l, v2, _decided = leg_oracle(lane, cfg, info)
        lines += l
        idx = json.loads((lane / RUN_DIR / "tests-index.json").read_text())["tests"]
        if candidates_only:
            cand = candidates(lane, cfg, v2, idx)
            for t in sorted(cand):
                lines.append(f"CANDIDATE {t} tests={','.join(x['name'] for x in cand[t])}")
            lines.append(f"CANDIDATES never_read_tasks={len(cand)}")
            return 0, lines
        ok_cf, l, good = leg_confirm(lane, cfg, info, v2, idx)
        lines += l
        ok_pa, l = leg_prior_art(lane, cfg, good, idx)
        lines += l
    else:
        lines.append("ORACLE not evaluable (pins, classifier, freeze or labels absent)")
        lines.append("CONFIRM new_confirmed=0")
        lines.append("PRIOR-ART rows=0")
    ok = ok_pins and ok_fz and ok_or and ok_cf and ok_pa
    fixture = cfg is not CFG and cfg != CFG
    lines.append(f"PREDICATE R53-C1{'-FIXTURE' if fixture else ''} {'pass' if ok else 'fail'}")
    return (0 if ok else 1), lines


# ---- selftest (forged-but-complete controls on a synthetic lane) -------------------------------------
def selftest() -> int:
    top = Path(tempfile.mkdtemp(prefix="r53c1-st-", dir=os.environ.get("TMPDIR") or tempfile.gettempdir()))
    fails: list[str] = []
    ncase = [0]
    lane = top / "lane"
    lane.mkdir()

    def sh(*a, cwd=lane):
        subprocess.run(a, cwd=cwd, check=True, capture_output=True)

    def w(rel, text, mode="w"):
        p = lane / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        (p.write_bytes if mode == "wb" else p.write_text)(text)
        return p

    sh("git", "-C", str(lane), "init", "-q")
    for k, v in (("user.email", "t@t.invalid"), ("user.name", "selftest")):
        sh("git", "-C", str(lane), "config", k, v)
    g1 = b"def test_a():\n    assert Path('/x').exists()\n\n\ndef test_b():\n    assert open('/x').read() == 'hi'\n"
    g2 = b"def test_c():\n    assert Path('/y').is_file()\n"
    ex = b"def test_z():\n    assert True\n"
    caps = {"t1/tests/test_outputs.py": g1, "t2/tests/test_outputs.py": g2, "tx/tests/test_outputs.py": ex}
    for rel, b in caps.items():
        if not rel.startswith("tx/"):
            w("corpus/evidence/round52/graders/" + rel, b, "wb")
    pop = {"tasks": {"t1": [], "t2": [], "tx": []}, "capture_population": {k.split("/")[0]: [k] for k in caps}}
    w("plans/round52-tasks.json", json.dumps(pop))
    pin = {"blobs": [{"path": k, "sha": blob_sha1(b)} for k, b in caps.items()]}
    w(f"{RUN_DIR}/pin-tree-2fd12b88.json", json.dumps(pin))
    sys.path.insert(0, str(Path(__file__).parent))
    import round53_c1_extract as ex_mod
    idxd = ex_mod.index(lane)
    w(f"{RUN_DIR}/tests-index.json", json.dumps(idxd))
    w("plans/round52_c1_grader_audit.py",
      "def classify_tests(body):\n    return [{'test': 'test_a', 'class': 'P0'}, {'test': 'test_b', 'class': 'P0'}, {'test': 'test_c', 'class': 'P0'}]\n")
    clf = ("import ast\n\ndef classify_source(src):\n    out = {}\n    for n in ast.parse(src).body:\n"
           "        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):\n"
           "            out[n.name] = 'P1' if 'read' not in ast.dump(n) and 'True' not in ast.dump(n) else 'P0'\n    return out\n")
    w("plans/round53_c1_classify.py", clf)
    w("corpus/knowledge/old.md", "nothing\n")
    for f in ("SCORECARD.md", "LOG.md", "SKILL.md", "corpus/README.md"):
        w(f, "x\n")
    w("corpus/evidence/round52/confirmations.json", "[]")
    sh("git", "-C", str(lane), "add", "-A")
    sh("git", "-C", str(lane), "commit", "-q", "-m", "base")
    base = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cfg = dict(CFG, POP_SHA=sha256_file(lane / "plans/round52-tasks.json"), PIN_TREE_SHA=sha256_file(lane / f"{RUN_DIR}/pin-tree-2fd12b88.json"),
               TESTS_INDEX_SHA=sha256_file(lane / f"{RUN_DIR}/tests-index.json"), TESTS_TOTAL=3, CAPTURES_EXPECTED=2,
               EXCLUDED_PATH="tx/tests/test_outputs.py", EXCLUDED_BLOB=blob_sha1(ex), BASE_TIP=base, CONFIRM_MIN=1, URL_MIN=1)

    def freeze():
        w("plans/round53-c1-freeze.json", json.dumps({"classifier_sha256": sha256_file(lane / "plans/round53_c1_classify.py"),
                                                      "author_seats": ["AuthorSeat"]}))
        sh("git", "-C", str(lane), "add", "-A")
        sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze")

    def labels(over=None):
        lab = {"t1::test_a": (["L1", "L2"], ["Y", "Y"]), "t1::test_b": (["L1", "L3"], ["N", "N"]),
               "t2::test_c": (["L2", "L3"], ["Y", "Y"])}
        if over:
            lab.update(over)
        w(f"{RUN_DIR}/oracle-labels.json", json.dumps({"labels": {k: {"labelers": a, "labels": b} for k, (a, b) in lab.items()}}))
        sh("git", "-C", str(lane), "add", "-A")
        sh("git", "-C", str(lane), "commit", "-q", "--allow-empty", "-m", "labels")

    def run(label, want_ok, want_in=(), cfgx=None):
        rc, lines = verdict(lane, cfgx or cfg)
        ncase[0] += 1
        text = "\n".join(lines)
        ok = (rc == 0) == want_ok and all(x in text for x in want_in)
        print(f"SELFTEST {label} rc={rc} {'ok' if ok else 'FAIL'}")
        if not ok:
            fails.append(label)
            print(text)

    run("nothing-committed", False, ("FREEZE absent", "PREDICATE R53-C1-FIXTURE fail"))
    # the r52-style classifier says P0 everywhere -> oracle leg must NOT be reachable by it
    freeze()
    labels()
    sh("git", "-C", str(lane), "add", "-A")
    # control leg needs >=CONTROL_MIN r52 disagreements; the fixture is tiny, so the control is deliberately vacuous here
    rc, lines = verdict(lane, cfg)
    t = "\n".join(lines)
    ok = "control_ok=NO(leg vacuous)" in t and rc == 1
    print(f"SELFTEST tiny-fixture-control-vacuous rc={rc} {'ok' if ok else 'FAIL'}")
    fails += [] if ok else ["tiny-fixture-control-vacuous"]

    global CONTROL_MIN
    saved = CONTROL_MIN
    CONTROL_MIN = 1
    w(f"{RUN_DIR}/confirmations.json", json.dumps([]))
    run("no-confirmations", False, ("CONFIRM candidates_never_read=", "new_confirmed=0"))
    rep = w(".ufo/waves/round-53/w2/ReaderSeat/report.md", "reader report: t2 test_c reads Path('/y').is_file() presence only\n")
    good = {"task": "t2", "test_id": "t2::test_c", "quote": "assert Path('/y').is_file()", "reader": "ReaderSeat", "confirmed": True,
            "report": ".ufo/waves/round-53/w2/ReaderSeat/report.md", "report_sha256": sha256_file(rep)}
    w(f"{RUN_DIR}/confirmations.json", json.dumps([good]))
    w(f"{RUN_DIR}/fetched/a.html", "the grader test_c merely checks the file exists and nothing more per this very long fixture page text for prior art\n")
    w(f"{RUN_DIR}/fetched/s1.html", "unrelated page one\n")
    w(f"{RUN_DIR}/fetched/s2.html", "unrelated page two\n")
    fa, s1, s2 = (lane / f"{RUN_DIR}/fetched/{n}" for n in ("a.html", "s1.html", "s2.html"))
    pa_known = {"task": "t2", "verdict": "phenomenon-known", "url": "https://real.example.net/a", "fetched": f"{RUN_DIR}/fetched/a.html",
                "fetched_sha256": sha256_file(fa), "quote": "the grader test_c merely checks the file exists and nothing more"}
    pa_new = {"task": "t2", "verdict": "phenomenon-new", "url": "https://real.example.net/b", "fetched": f"{RUN_DIR}/fetched/a.html",
              "fetched_sha256": sha256_file(fa), "quote": "the grader test_c merely checks the file exists and nothing more",
              "sweep": [{"file": f"{RUN_DIR}/fetched/s1.html", "file_sha256": sha256_file(s1)},
                        {"file": f"{RUN_DIR}/fetched/s2.html", "file_sha256": sha256_file(s2)}]}
    w(f"{RUN_DIR}/prior-art.json", json.dumps([pa_known]))
    run("known-only-fails-score-rule", False, ("new=0",))
    w(f"{RUN_DIR}/prior-art.json", json.dumps([pa_new]))
    run("genuine-fixture-passes", True, ("PREDICATE R53-C1-FIXTURE pass", "new_confirmed=1", "new=1"))
    # forged-but-complete controls
    def forge(label, conf=None, pa=None, want=()):
        w(f"{RUN_DIR}/confirmations.json", json.dumps([conf] if conf else [good]))
        w(f"{RUN_DIR}/prior-art.json", json.dumps([pa] if pa else [pa_new]))
        run(label, False, want)
    forge("forged-confirmed-string", dict(good, confirmed="false"), want=("confirmed-not-true",))
    forge("forged-reader-is-author", dict(good, reader="AuthorSeat"), want=("reader-is-author",))
    forge("forged-quote-outside-span", dict(good, quote="assert Path('/x').exists()"), want=("quote-short-or-outside-test-span",))
    forge("forged-short-quote", dict(good, quote="assert"), want=("quote-short-or-outside-test-span",))
    forge("forged-report-names-other-task", dict(good, task="t1", test_id="t1::test_a", quote="assert Path('/x').exists()"),
          want=("report-does-not-name-task",))
    forge("forged-report-digest", dict(good, report_sha256="0" * 64), want=("reader-report-missing-or-digest-mismatch",))
    forge("forged-prior-art-example", pa=dict(pa_new, url="https://example.org/x"), want=("bad-url",))
    forge("forged-prior-art-unfetched", pa=dict(pa_new, fetched=f"{RUN_DIR}/fetched/nope.html"), want=("fetch-missing",))
    forge("forged-prior-art-digest", pa=dict(pa_new, fetched_sha256="1" * 64), want=("fetch-missing-or-digest-mismatch",))
    forge("forged-prior-art-quote", pa=dict(pa_new, quote="this sentence never occurs in the archived fetch at all ever"), want=("quote-not-8to25",))
    forge("forged-new-without-sweep", pa={k: v for k, v in pa_new.items() if k != "sweep"}, want=("new-needs-two-sweep-fetches",))
    # pins
    w(f"{RUN_DIR}/confirmations.json", json.dumps([good]))
    w(f"{RUN_DIR}/prior-art.json", json.dumps([pa_new]))
    p = lane / "corpus/evidence/round52/graders/t2/tests/test_outputs.py"
    orig = p.read_bytes()
    p.write_bytes(b"def test_c():\n    assert Path('/y').is_file()\n# forged stub\n")
    run("forged-capture-bytes", False, ("blob_bad=1",))
    p.write_bytes(orig)
    pop_p = lane / "plans/round52-tasks.json"
    popo = pop_p.read_text()
    pop_p.write_text(json.dumps({"tasks": {"t2": []}, "capture_population": {"t2": ["t2/tests/test_outputs.py"]}}))
    run("forged-population-shrunk", False, ("population_sha=BAD",))
    pop_p.write_text(popo)
    # oracle: labels authored by the classifier author, or copied (freeze after labels)
    labels({"t2::test_c": (["AuthorSeat", "L3"], ["Y", "Y"])})
    run("forged-labeler-is-author", False, ("bad_label_rows=1",))
    labels({"t2::test_c": (["L2", "L2"], ["Y", "Y"])})
    run("forged-one-labeler-twice", False, ("bad_label_rows=1",))
    labels({"t2::test_c": (["L2", "L3"], ["N", "N"])})
    run("oracle-disagreement", False, ("disagree=1",))
    labels()
    # ---- C1MutCounter kill cases (wave-1 mutation probe; proposed, not landed) ----
    clf_path = lane / "plans/round53_c1_classify.py"
    clf_orig = clf_path.read_bytes()
    idx_orig = (lane / f"{RUN_DIR}/tests-index.json").read_bytes()
    stub_orig = (lane / "plans/round52_c1_grader_audit.py").read_bytes()
    Y_ = (["L1", "L2"], ["Y", "Y"])
    N_ = (["L1", "L2"], ["N", "N"])
    U_ = (["L1", "L2"], ["Y", "U"])

    def setc(conf=None, pa=None):
        w(f"{RUN_DIR}/confirmations.json", json.dumps([good] if conf is None else conf))
        w(f"{RUN_DIR}/prior-art.json", json.dumps([pa_new] if pa is None else pa))

    def setl(over=None, drop=()):
        lab = {"t1::test_a": (["L1", "L2"], ["Y", "Y"]), "t1::test_b": (["L1", "L3"], ["N", "N"]),
               "t2::test_c": (["L2", "L3"], ["Y", "Y"])}
        for k in drop:
            lab.pop(k, None)
        lab.update(over or {})
        w(f"{RUN_DIR}/oracle-labels.json",
          json.dumps({"labels": {k: {"labelers": a, "labels": b} for k, (a, b) in lab.items()}}))

    def ext(label, want_ok, want_in=(), conf=None, pa=None, over=None, drop=(), cfgx=None):
        setc(conf, pa); setl(over, drop)
        run(label, want_ok, want_in, cfgx)
        setc(); setl()

    # pins: tests-index digest clause (P11); excluded capture present (P12)
    w(f"{RUN_DIR}/tests-index.json", idx_orig + b"\n", "wb")
    run("ext-tests-index-digest", False, ("tests_index_sha=BAD",))
    w(f"{RUN_DIR}/tests-index.json", idx_orig, "wb")
    exf = lane / "corpus/evidence/round52/graders/tx/tests/test_outputs.py"
    exf.parent.mkdir(parents=True, exist_ok=True)
    exf.write_bytes(ex)
    run("ext-excluded-capture-present", False, ("excluded_blob=BAD",))
    exf.unlink()

    # freeze ordering (F04/F05): labels first-added before the freeze file
    rv = top / "rev"
    rv.mkdir()
    arch = subprocess.run(["git", "-C", str(lane), "archive", base], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(rv)], input=arch, check=True)
    gv = lambda *a: subprocess.run(["git", "-C", str(rv), *a], check=True, capture_output=True)
    gv("init", "-q"); gv("config", "user.email", "t@t.invalid"); gv("config", "user.name", "selftest")
    gv("add", "-A"); gv("commit", "-q", "-m", "base")
    (rv / RUN_DIR / "oracle-labels.json").parent.mkdir(parents=True, exist_ok=True)
    (rv / RUN_DIR / "oracle-labels.json").write_text(json.dumps({"labels": {
        "t1::test_a": {"labelers": ["L1", "L2"], "labels": ["Y", "Y"]},
        "t1::test_b": {"labelers": ["L1", "L3"], "labels": ["N", "N"]},
        "t2::test_c": {"labelers": ["L2", "L3"], "labels": ["Y", "Y"]}}}))
    gv("add", "-A"); gv("commit", "-q", "-m", "labels")
    (rv / "plans/round53-c1-freeze.json").write_text(json.dumps(
        {"classifier_sha256": sha256_file(rv / "plans/round53_c1_classify.py"), "author_seats": ["AuthorSeat"]}))
    gv("add", "-A"); gv("commit", "-q", "-m", "freeze")
    rc_rv, lines_rv = verdict(rv, cfg)
    t_rv = "\n".join(lines_rv)
    ok_rv = rc_rv == 1 and "order=UNPROVEN" in t_rv
    ncase[0] += 1
    print(f"SELFTEST ext-freeze-after-labels rc={rc_rv} {'ok' if ok_rv else 'FAIL'}")
    if not ok_rv:
        fails.append("ext-freeze-after-labels"); print(t_rv)

    # leg-level freeze clauses (F05 order, F06 authors), called directly
    ok_fz_rv = leg_freeze(rv)[0]
    ncase[0] += 1
    print(f"SELFTEST ext-freeze-leg-order-clause rc={0 if ok_fz_rv else 1} {'ok' if ok_fz_rv is False else 'FAIL'}")
    if ok_fz_rv is not False:
        fails.append("ext-freeze-leg-order-clause")
    fzj = lane / "plans/round53-c1-freeze.json"
    fz_orig = fzj.read_bytes()
    fzj.write_text(json.dumps({"classifier_sha256": sha256_file(clf_path), "author_seats": []}))
    ok_noauth = leg_freeze(lane)[0]
    fzj.write_bytes(fz_orig)
    ncase[0] += 1
    print(f"SELFTEST ext-freeze-leg-empty-authors rc={0 if ok_noauth else 1} {'ok' if ok_noauth is False else 'FAIL'}")
    if ok_noauth is not False:
        fails.append("ext-freeze-leg-empty-authors")

    # oracle labels (L01 L03 L04 L05 L06 O05)
    ext("ext-labelers-three-distinct", False, ("bad_label_rows=1",), over={"t2::test_c": (["L2", "L3", "L1"], ["Y", "Y"])})
    ext("ext-label-domain-X", False, ("bad_label_rows=1",), over={"t2::test_c": (["L2", "L3"], ["X", "X"])})
    ext("ext-label-disagree-contested", False, ("contested=1",), over={"t2::test_c": (["L2", "L3"], ["Y", "N"])})
    ext("ext-label-row-missing", False, ("bad_label_rows=1",), drop=("t2::test_c",))
    ext("ext-labelers-not-a-list", False, ("bad_label_rows=1",), over={"t2::test_c": ("ab", ["Y", "Y"])})
    ext("ext-extra-label-row", False, (), over={"t9::nope": (["L1", "L2"], ["Y", "Y"])})

    # confirm leg (K02 K03 K05 K06 K07 K09 K10 C10 C11)
    rep1 = w(".ufo/waves/round-53/w2/ReaderSeat/report_t1.md", "reader report: t1 test_b reads a file via open\n")
    rep6 = w(".ufo/waves/round-53/w2/KengakuR53C1/report.md", "reader report: t2 test_c checks presence only\n")
    rep7 = w(".ufo/waves/round-53/w2/OtherSeat/report.md", "reader report: t2 test_c checks presence only\n")
    ext("ext-candidate-v2-P0-rejected", False, ("t1:not-a-never-read-v2-P1-candidate",), pa=[],
        conf=[dict(good, task="t1", test_id="t1::test_b", quote="assert open('/x').read() == 'hi'",
                   report=str(rep1.relative_to(lane)), report_sha256=sha256_file(rep1))])
    ext("ext-reader-KengakuR53-prefix", False, ("t2:reader-is-author",),
        conf=[dict(good, reader="KengakuR53C1", report=str(rep6.relative_to(lane)), report_sha256=sha256_file(rep6))])
    ext("ext-reader-not-in-report-path", False, ("t2:reader-report-missing-or-digest-mismatch",),
        conf=[dict(good, report=str(rep7.relative_to(lane)), report_sha256=sha256_file(rep7))])
    ext("ext-quote-spans-def-line", True, ("new_confirmed=1",), conf=[dict(good, quote="def test_c(): assert Path('/y')")])
    ext("ext-task-testid-mismatch", False, ("t2:unknown-test-id",), conf=[dict(good, test_id="t1::test_a")])
    s22 = "assert Path('/y').is_file()"
    ext("ext-quote-exactly-20-chars", True, ("new_confirmed=1",), conf=[dict(good, quote=s22[:20])])
    ext("ext-quote-19-chars-rejected", False, ("t2:quote-short-or-outside-test-span",), conf=[dict(good, quote=s22[:19])])
    ext("ext-duplicate-task-row", True, ("new_confirmed=1 rejected=1",), conf=[good, good])

    # prior-art leg (A01 A02 A03 A04 A05 A06 A07 A09 A10 A11 A12 A13 A14 A17)
    wf = lane / f"{RUN_DIR}/fetched/w.html"
    wf.write_text(" ".join(f"word{i}" for i in range(30)) + "\n")
    wrow = lambda q_, **kw: dict(pa_new, fetched=f"{RUN_DIR}/fetched/w.html", fetched_sha256=sha256_file(wf), quote=q_, **kw)
    qw = lambda k: " ".join(f"word{i}" for i in range(k))
    ext("ext-prior-art-unconfirmed-task-row", False, ("t1:task-not-confirmed",), pa=[pa_new, dict(pa_new, task="t1")])
    ext("ext-prior-art-bad-verdict", False, ("t2:bad-verdict",), pa=[pa_new, dict(pa_new, verdict="phenomenon-maybe")])
    ext("ext-prior-art-url-not-a-url", False, ("t2:bad-url",), pa=[dict(pa_new, url="notaurl")])
    ext("ext-prior-art-one-rejected-row", False, ("t2:bad-url",), pa=[pa_new, dict(pa_new, url="notaurl")])
    ext("ext-quote-7-words-rejected", False, ("t2:quote-not-8to25-words-or-not-in-fetch",), pa=[wrow(qw(7))])
    ext("ext-quote-8-words-accepted", True, ("new=1",), pa=[wrow(qw(8))])
    ext("ext-quote-26-words-rejected", False, ("t2:quote-not-8to25-words-or-not-in-fetch",), pa=[wrow(qw(26))])
    kn1 = lane / f"{RUN_DIR}/fetched/kn1.html"
    kn1.write_text("the task t2 page only mentions the grader in plain words here\n")
    kn2 = lane / f"{RUN_DIR}/fetched/kn2.html"
    kn2.write_text("nothing relevant in this archived page at all really here\n")
    krow = lambda f_, q_: dict(pa_known, task="t2", url="https://real.example.net/c", fetched=f"{RUN_DIR}/fetched/{f_}",
                               fetched_sha256=sha256_file(lane / f"{RUN_DIR}/fetched/{f_}"), quote=q_)
    ext("ext-known-names-task-not-tests", True, ("new=1",),
        pa=[pa_new, krow("kn1.html", "the task t2 page only mentions the grader in plain words here")])
    ext("ext-known-names-neither-rejected", False, ("t2:known-fetch-never-names-the-task-or-its-tests",),
        pa=[pa_new, krow("kn2.html", "nothing relevant in this archived page at all really here")])
    sw_s1 = {"file": f"{RUN_DIR}/fetched/s1.html", "file_sha256": sha256_file(s1)}
    ext("ext-new-one-sweep-rejected", False, ("t2:new-needs-two-sweep-fetches",), pa=[dict(pa_new, sweep=[sw_s1])])
    s3 = lane / f"{RUN_DIR}/fetched/s3.html"
    s3.write_text("a page about t2 grader only\n")
    s4 = lane / f"{RUN_DIR}/fetched/s4.html"
    s4.write_text("a page about test_c only\n")
    sw_with = lambda f_: [sw_s1, {"file": f"{RUN_DIR}/fetched/{f_}", "file_sha256": sha256_file(lane / f"{RUN_DIR}/fetched/{f_}")}]
    ext("ext-sweep-names-task-rejected", False, ("t2:sweep-fetch-missing-or-names-the-task",), pa=[dict(pa_new, sweep=sw_with("s3.html"))])
    ext("ext-sweep-names-test-rejected", False, ("t2:sweep-fetch-missing-or-names-the-task",), pa=[dict(pa_new, sweep=sw_with("s4.html"))])
    outf = lane / "corpus/evidence/round53/outside.html"
    outf.write_text("the grader test_c merely checks the file exists and nothing more\n")
    ext("ext-fetch-outside-fetched-dir", False, ("t2:fetch-missing-or-digest-mismatch",),
        pa=[dict(pa_new, fetched="corpus/evidence/round53/outside.html", fetched_sha256=sha256_file(outf))])

    # oracle control clause, called directly (O11): tiny fixture is control-vacuous at the real minimum
    CONTROL_MIN = 10
    ok_tiny = leg_oracle(lane, cfg, {"authors": {"AuthorSeat"}})[0]
    CONTROL_MIN = 1
    ncase[0] += 1
    print(f"SELFTEST ext-oracle-control-clause-in-leg rc={0 if ok_tiny else 1} {'ok' if ok_tiny is False else 'FAIL'}")
    if ok_tiny is not False:
        fails.append("ext-oracle-control-clause-in-leg")
    ext("ext-tests-total-mismatch", False, (), cfgx=dict(cfg, TESTS_TOTAL=4))

    # scale fixture: 100-test leg_oracle boundaries (O09 O10 O12 C04 C05 C06 O06)
    import ast as _ast

    def scale(name, spec, clf_text=None):
        root = top / name
        srcs, idx, labs = [], [], {}
        for i, (pair, p1) in enumerate(spec):
            call = "Path('/x').exists()" if p1 else "open('/x').read()"
            srcs.append(f"def test_{i}():\n    assert {call}\n")
        src = "\n".join(srcs)
        for node in _ast.parse(src).body:
            i = int(node.name[5:])
            pair = spec[i][0]
            idx.append({"id": f"s1::{node.name}", "task": "s1", "file": "s1/tests/test_outputs.py", "name": node.name,
                        "class": None, "lineno": node.lineno, "end_lineno": node.end_lineno})
            labs[f"s1::{node.name}"] = {"labelers": pair[0], "labels": pair[1]}
        for rel, data in (("corpus/evidence/round52/graders/s1/tests/test_outputs.py", src),
                          ("corpus/evidence/round53/tests-index.json", json.dumps({"tests": idx})),
                          ("corpus/evidence/round53/oracle-labels.json", json.dumps({"labels": labs})),
                          ("plans/round53_c1_classify.py", clf_text if clf_text is not None else clf_orig.decode()),
                          ("plans/round52_c1_grader_audit.py", stub_orig.decode())):
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(data)
        return leg_oracle(root, dict(cfg, TESTS_TOTAL=len(idx)), {"authors": {"AuthorSeat"}})[:2]

    def scase(label, want, spec, clf_text=None):
        ok_s, L_s = scale(label, spec, clf_text)
        ncase[0] += 1
        good_s = ok_s is want
        print(f"SELFTEST {label} rc={0 if ok_s else 1} {'ok' if good_s else 'FAIL'}")
        if not good_s:
            fails.append(label); print("\n".join(L_s))

    clf_custom = ("import ast\n\ndef classify_source(src):\n    out = {}\n    for n in ast.parse(src).body:\n"
                  "        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_') and int(n.name[5:]) >= 10:\n"
                  "            out[n.name] = 'P1'\n    return out\n")
    scase("ext-scale-null-100-decided", True, [(Y_, True)] * 100)
    scase("ext-scale-disagree-at-limit-3", True, [(Y_, True)] * 97 + [(N_, True)] * 3)
    scase("ext-scale-disagree-over-limit-4", False, [(Y_, True)] * 96 + [(N_, True)] * 4)
    scase("ext-scale-contested-at-limit-15", True, [(Y_, True)] * 85 + [(U_, True)] * 15)
    scase("ext-scale-contested-over-limit-16", False, [(Y_, True)] * 84 + [(U_, True)] * 16)
    scase("ext-scale-disagree-3-of-85-decided", False, [(Y_, True)] * 82 + [(N_, True)] * 3 + [(U_, True)] * 15)
    scase("ext-scale-control-ratio-1-vs-2", False, [(Y_, True)] * 1 + [(N_, False)] * 99)
    scase("ext-scale-unclassified-10", False, [(N_, True)] * 10 + [(Y_, True)] * 90, clf_text=clf_custom)
    scase("ext-scale-bad-label-row", False, [((["L1", "L2"], ["X", "X"]), True)] + [(Y_, True)] * 96 + [(N_, False)] * 3)

    # never-read base texts (K12 K13): temp-lane commits, cfg BASE_TIP varied
    w("corpus/evidence/round52/confirmations.json", json.dumps([{"task": "t2"}]))
    sh("git", "-C", str(lane), "add", "-A"); sh("git", "-C", str(lane), "commit", "-q", "-m", "r52 list")
    b_r52 = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    w("corpus/evidence/round52/confirmations.json", "[]")
    w("LOG.md", "t2 is mentioned in this log\n")
    sh("git", "-C", str(lane), "add", "-A"); sh("git", "-C", str(lane), "commit", "-q", "-m", "log mention")
    b_seen = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    ext("ext-candidate-seen-in-base-excluded", False, ("t2:not-a-never-read-v2-P1-candidate",), cfgx=dict(cfg, BASE_TIP=b_seen))
    ext("ext-candidate-r52-confirmed-excluded", False, ("t2:not-a-never-read-v2-P1-candidate",), cfgx=dict(cfg, BASE_TIP=b_r52))
    w("LOG.md", "x\n")
    # classifier edited after the freeze
    cp = lane / "plans/round53_c1_classify.py"
    cp.write_text(cp.read_text() + "\n# tuned after seeing the labels\n")
    run("classifier-edited-after-freeze", False, ("classifier_sha=BAD",))
    CONTROL_MIN = saved
    # ---- C1MutCounter kill cases, after CONTROL_MIN is restored to its module value ----
    clf_path.write_bytes(clf_orig)
    scase("ext-scale-control-min-at-10", True, [(Y_, True)] * 10 + [(N_, False)] * 90)
    frozen = {'POP_SHA': '0230b68c666c1e0649b42d61d7121a30eedf247411642bbf397e3390436b5cfc', 'PIN_TREE_SHA': '96b472489cbec0f4f6319db510b40284efa92b01b4badbc112d922662d42cbb9', 'TESTS_INDEX_SHA': '579d567fd66f5fc0bc71957cdc887e9bb952c63b3fd9d2726e67c963897c7330', 'TESTS_TOTAL': 305, 'CAPTURES_EXPECTED': 183, 'EXCLUDED_PATH': 'sanitize-git-repo/tests/test_outputs.py', 'EXCLUDED_BLOB': '3269e74e727fda61c936ca34b8f3bfaacf199dda', 'CONFIRM_MIN': 3, 'URL_MIN': 3, 'ORACLE_MAX_DISAGREE': 0.03, 'ORACLE_MAX_CONTESTED': 0.15, 'CONTROL_RATIO': 2, 'CONTROL_MIN': 10, 'QUOTE_MIN_CHARS': 20}
    now = {k: globals()[k] for k in frozen}
    bad = sorted(k for k in frozen if frozen[k] != now[k])
    ncase[0] += 1
    print(f"SELFTEST ext-frozen-constants rc={0 if not bad else 1} {'ok' if not bad else 'FAIL'}")
    if bad:
        fails.append("ext-frozen-constants"); print("drifted:", bad)
    shutil_rm(top)
    print(f"SELFTEST cases={ncase[0] + 1} failures={len(fails)}")
    return 0 if not fails else 1


def shutil_rm(p: Path):
    import shutil
    shutil.rmtree(p, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--candidates", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    lane = Path(a.lane).resolve()
    rc, lines = verdict(lane, CFG, a.candidates)
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
