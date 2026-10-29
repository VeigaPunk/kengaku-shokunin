#!/usr/bin/env python3
"""Round 53, claim C1: Terminal-Bench 2.0 presence-only grader triage, v2 (counter) — amendment A1.

Replaces the round-52 counter's trust model (Q42): every input the predicate trusts is pinned by a digest constant in THIS
file or by git history, the per-test class is an AST classifier scored against an independent blind-label oracle merged from
the eight label seats' own files, a forged-but-complete input must fail, and the prior-art leg re-reads archived fetches.
Legs and the one predicate sentence are frozen in ``plans/round-53-claims.md`` (amendment A1 there records what changed
after the wave-1 attacks and before any scored run).

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
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---- pins (frozen at the round-53 claims commit; A1 adds R52_AUDIT_SHA and the label-seat layout) -----------------
POP_SHA = "0230b68c666c1e0649b42d61d7121a30eedf247411642bbf397e3390436b5cfc"       # plans/round52-tasks.json
PIN_TREE_SHA = "96b472489cbec0f4f6319db510b40284efa92b01b4badbc112d922662d42cbb9"  # corpus/evidence/round53/pin-tree-2fd12b88.json
TESTS_INDEX_SHA = "579d567fd66f5fc0bc71957cdc887e9bb952c63b3fd9d2726e67c963897c7330"  # corpus/evidence/round53/tests-index.json
R52_AUDIT_SHA = "0b1d4213b9522cfb1cf9bb615d03d278e6ac75b87a3984095d410faf1707a7b3"  # plans/round52_c1_grader_audit.py (the control)
TESTS_TOTAL = 305
CAPTURES_EXPECTED = 183
EXCLUDED_PATH = "sanitize-git-repo/tests/test_outputs.py"
EXCLUDED_BLOB = "3269e74e727fda61c936ca34b8f3bfaacf199dda"
BASE_TIP = "536925b5320fa64298030b4ee76a58fc4b82723f"                             # lane tip the claims were frozen against
LABEL_SEATS = {"A": "C1LabelScoutA", "B": "C1LabelRevB", "C": "C1LabelScoutC", "D": "C1LabelRevD",
               "E": "C1LabelScoutE", "F": "C1LabelRevF", "G": "C1LabelScoutG", "H": "C1LabelRevH"}
LABEL_DIR = ".ufo/waves/round-53/w1"          # <seat>/labels.json
SHARD_DIR = ".ufo/waves/round-53/labels"      # shard-<X>.json
ORACLE_MAX_DISAGREE = 0.03      # of decided tests
ORACLE_MAX_CONTESTED = 0.15     # of all tests
LABEL_AGREE_MIN = 0.90          # classifier vs every individual non-U label (A1: closes the contested-budget route)
BALANCE_MIN = 10                # decided Y and decided N must each reach this (A1: an all-Y copy cannot pass)
CONTROL_RATIO = 2               # r52 classifier's disagree must be >= 2x v2's ...
CONTROL_MIN = 10                # ... and >= 10, else the leg is vacuous
CONFIRM_MIN = 3
URL_MIN = 3
QUOTE_MIN_CHARS = 20
RUN_DIR = "corpus/evidence/round53"
FROZEN = dict(POP_SHA=POP_SHA, PIN_TREE_SHA=PIN_TREE_SHA, TESTS_INDEX_SHA=TESTS_INDEX_SHA, R52_AUDIT_SHA=R52_AUDIT_SHA,
              TESTS_TOTAL=TESTS_TOTAL, CAPTURES_EXPECTED=CAPTURES_EXPECTED, EXCLUDED_PATH=EXCLUDED_PATH,
              EXCLUDED_BLOB=EXCLUDED_BLOB, BASE_TIP=BASE_TIP, LABEL_SEATS=dict(LABEL_SEATS), LABEL_DIR=LABEL_DIR,
              SHARD_DIR=SHARD_DIR, BALANCE_MIN=BALANCE_MIN, CONTROL_MIN=CONTROL_MIN, CONFIRM_MIN=CONFIRM_MIN,
              URL_MIN=URL_MIN)
CFG = dict(FROZEN)


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


def inside(lane: Path, rel: str, sub: str) -> Path | None:
    """Resolved path of lane/rel iff it lies under lane/sub, is a regular non-symlink file and rel is relative."""
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
        return None
    p = lane / rel
    try:
        if p.is_symlink() or not p.is_file():
            return None
        return p if p.resolve().is_relative_to((lane / sub).resolve()) else None
    except OSError:
        return None


# ---- leg 1: PINS ---------------------------------------------------------------------------------
def leg_pins(lane: Path, cfg: dict):
    L = []
    pop_p = lane / "plans/round52-tasks.json"
    pin_p = lane / RUN_DIR / "pin-tree-2fd12b88.json"
    idx_p = lane / RUN_DIR / "tests-index.json"
    pop_ok = sha256_file(pop_p) == cfg["POP_SHA"]
    pin_ok = sha256_file(pin_p) == cfg["PIN_TREE_SHA"]
    idx_ok = sha256_file(idx_p) == cfg["TESTS_INDEX_SHA"]
    r52_ok = sha256_file(lane / "plans/round52_c1_grader_audit.py") == cfg["R52_AUDIT_SHA"]
    match = bad = absent = 0
    exc_ok = False
    n_paths = -1
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
    ok = (pop_ok and pin_ok and idx_ok and r52_ok and match == cfg["CAPTURES_EXPECTED"] and bad == 0 and absent == 0
          and exc_ok and n_paths == cfg["CAPTURES_EXPECTED"] + 1)
    L.append(f"PINS population_sha={'ok' if pop_ok else 'BAD'} pin_tree_sha={'ok' if pin_ok else 'BAD'} "
             f"tests_index_sha={'ok' if idx_ok else 'BAD'} r52_audit_sha={'ok' if r52_ok else 'BAD'} "
             f"captures_blob_match={match} blob_bad={bad} absent={absent} "
             f"excluded_blob={'ok' if exc_ok else 'BAD'} files={n_paths}")
    return ok, L


# ---- leg 2: FREEZE + ORACLE ----------------------------------------------------------------------
def commits_touching(lane: Path, rel: str) -> list[str]:
    rc, out = git(lane, "log", "--format=%H", "--", rel)
    return [x for x in out.split() if x] if rc == 0 else []


def leg_freeze(lane: Path, cfg: dict):
    """FREEZE: classifier + freeze file added together and never touched again; label seat files and shards pinned by
    digest in the freeze file and added in strictly later commits, never touched again; clean tree."""
    L = []
    info = {"authors": set(), "ok": False}
    seats = cfg["LABEL_SEATS"]
    fz, clf = "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py"
    lab = {k: f"{cfg['LABEL_DIR']}/{s}/labels.json" for k, s in seats.items()}
    shard = {k: f"{cfg['SHARD_DIR']}/shard-{k}.json" for k in seats}
    missing = [p for p in [fz, clf, *lab.values(), *shard.values()] if not (lane / p).is_file()]
    if missing:
        L.append(f"FREEZE absent missing={len(missing)} first={missing[0]}")
        return False, L, info
    try:
        d = json.loads((lane / fz).read_text())
    except Exception:  # noqa: BLE001
        L.append("FREEZE unreadable freeze file")
        return False, L, info
    rc, st = git(lane, "status", "--porcelain")
    clean = rc == 0 and st.strip() == ""
    c_fz, c_clf = commits_touching(lane, fz), commits_touching(lane, clf)
    once = len(c_fz) == 1 and len(c_clf) == 1 and c_fz == c_clf
    sha_ok = sha256_file(lane / clf) == d.get("classifier_sha256")
    lab_ok = isinstance(d.get("label_sha256"), dict) and all(sha256_file(lane / lab[k]) == d["label_sha256"].get(seats[k]) for k in seats)
    shd_ok = isinstance(d.get("shard_sha256"), dict) and all(sha256_file(lane / shard[k]) == d["shard_sha256"].get(k) for k in seats)
    order = bool(once)
    if once:
        for p in [*lab.values()]:
            cs = commits_touching(lane, p)
            if len(cs) != 1 or cs[0] == c_fz[0] or git(lane, "merge-base", "--is-ancestor", c_fz[0], cs[0])[0] != 0:
                order = False
    info["authors"] = set(d.get("author_seats") or [])
    authors_ok = bool(info["authors"]) and not any(a.casefold().startswith("c1label") for a in info["authors"])
    ok = clean and once and sha_ok and lab_ok and shd_ok and order and authors_ok
    info["ok"] = ok
    L.append(f"FREEZE clean={'yes' if clean else 'NO'} classifier_and_freeze_one_commit={'yes' if once else 'NO'} "
             f"classifier_sha={'ok' if sha_ok else 'BAD'} label_files_pinned={'ok' if lab_ok else 'BAD'} "
             f"shards_pinned={'ok' if shd_ok else 'BAD'} labels_after_freeze_and_untouched={'yes' if order else 'NO'} "
             f"authors={len(info['authors'])}{'' if authors_ok else ' BAD'}")
    return ok, L, info


def merge_labels(lane: Path, cfg: dict, idx_ids: list[str], authors: set):
    """Merge the eight label seats' own files over the pinned shards: each test must sit in exactly two shards."""
    seats = cfg["LABEL_SEATS"]
    shards = {k: json.loads((lane / cfg["SHARD_DIR"] / f"shard-{k}.json").read_text()) for k in seats}
    in_shards: dict[str, list[str]] = {}
    for k, rows in shards.items():
        for r in rows:
            in_shards.setdefault(r["id"], []).append(k)
    per_seat, bad_files = {}, []
    for k, s in seats.items():
        try:
            d = json.loads((lane / cfg["LABEL_DIR"] / s / "labels.json").read_text())
            lab = d["labels"]
            ok = d.get("seat") == s and set(lab) == {r["id"] for r in shards[k]} and all(
                isinstance(v, dict) and v.get("label") in ("Y", "N", "U") for v in lab.values())
        except Exception:  # noqa: BLE001
            ok, lab = False, {}
        if not ok:
            bad_files.append(s)
        per_seat[k] = lab
    decided, contested, bad = {}, [], []
    indiv: list[tuple[str, str]] = []
    for tid in idx_ids:
        ks = in_shards.get(tid, [])
        if len(ks) != 2 or len(set(ks)) != 2 or any(seats[k] in bad_files or seats[k] in authors for k in ks):
            bad.append(tid)
            continue
        a, b = (per_seat[k][tid]["label"] for k in ks)
        indiv += [(tid, a), (tid, b)]
        if a == b and a in ("Y", "N"):
            decided[tid] = a
        else:
            contested.append(tid)
    return decided, contested, bad, set(in_shards) - set(idx_ids), bad_files, indiv


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
    decided, contested, bad, extra, bad_files, indiv = merge_labels(lane, cfg, ids, info["authors"])
    v2, uncl = v2_classes(lane, idx)
    r52 = r52_classes(lane, idx)
    dis = sum(1 for t, y in decided.items() if (v2[t] == "P1") != (y == "Y"))
    dis52 = sum(1 for t, y in decided.items() if (r52[t] == "P1") != (y == "Y"))
    dis0 = sum(1 for y in decided.values() if y == "Y")
    nonu = [(t, x) for t, x in indiv if x in ("Y", "N")]
    agree_n = sum(1 for t, x in nonu if (v2[t] == "P1") == (x == "Y"))
    agree_frac = agree_n / len(nonu) if nonu else 0.0
    n = len(ids)
    ny, nn = dis0, len(decided) - dis0
    lim = ORACLE_MAX_DISAGREE * max(1, len(decided))
    ctl_ok = dis52 >= CONTROL_RATIO * max(dis, 1) and dis52 >= cfg["CONTROL_MIN"]
    ok = (n == cfg["TESTS_TOTAL"] and not bad and not extra and not bad_files and not uncl and len(decided) > 0
          and dis <= lim and len(contested) <= ORACLE_MAX_CONTESTED * n and agree_frac >= LABEL_AGREE_MIN
          and ny >= cfg["BALANCE_MIN"] and nn >= cfg["BALANCE_MIN"] and ctl_ok)
    L.append(f"ORACLE tests={n} bad_label_files={len(bad_files)} bad_label_rows={len(bad)} decided={len(decided)} "
             f"contested={len(contested)} oracle_Y={ny} oracle_N={nn} v2_P1={sum(1 for c in v2.values() if c == 'P1')} "
             f"unclassified={len(uncl)} disagree={dis} limit={lim:.1f} per_label_agree={agree_frac:.3f} (min {LABEL_AGREE_MIN})")
    L.append(f"ORACLE-CONTROL r52_classifier_disagree={dis52} all_P0_disagree={dis0} "
             f"control_ok={'yes' if ctl_ok else 'NO(leg vacuous)'}")
    return ok, L, v2, decided


# ---- leg 3: CONFIRM ------------------------------------------------------------------------------
def never_read_blocklist(lane: Path, cfg: dict) -> tuple[list[str], dict]:
    """Texts of the pre-round lane at BASE_TIP, excluding the round-52 triage entry itself.  Fails closed (A1):
    an unavailable base tip (shallow or foreign clone) raises instead of yielding an empty blocklist."""
    if git(lane, "cat-file", "-e", f"{cfg['BASE_TIP']}^{{commit}}")[0] != 0:
        raise RuntimeError("BASE-TIP-UNAVAILABLE")
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
    try:
        cand = candidates(lane, cfg, v2, idx)
    except RuntimeError:
        L.append("CONFIRM BASE-TIP-UNAVAILABLE new_confirmed=0 (the never-read blocklist cannot be built: fail closed)")
        return False, L, []
    by_id = {t["id"]: t for t in idx}
    rows = json.loads(p.read_text()) if p.is_file() else []
    if not isinstance(rows, list):
        rows, rej = [], ["non-list"]
    bar = {a.casefold() for a in info["authors"]}
    seen_tasks = set()
    for r in rows:
        why = None
        try:
            tid = r.get("test_id")
            t = by_id.get(tid)
            rep = inside(lane, r.get("report"), ".ufo/waves/round-53")
            rd = str(r.get("reader", ""))
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
            elif not rd or rd.casefold() in bar or rd.casefold().startswith(("c1label", "kengakur53")):
                why = "reader-is-author-or-labeller"
            elif rep is None or sha256_file(rep) != r.get("report_sha256") or rd not in str(rep):
                why = "reader-report-missing-outside-wave-dir-or-digest-mismatch"
            elif not re.search(r"(?<![A-Za-z0-9_-])" + re.escape(r["task"]) + r"(?![A-Za-z0-9_-])",
                               rep.read_text(encoding="utf-8", errors="replace")):
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


HDR = re.compile(r"\A\s*SOURCE-URL:\s*(\S+)")


def names_task(text: str, task: str, tests: list[str]) -> bool:
    """Does the archive body name the task or one of its tests?  The SOURCE-URL header line is the archive's own label
    (a search URL legitimately carries the task id), so it is not part of the body."""
    if HDR.match(text):
        text = text.split("\n", 1)[1] if "\n" in text else ""
    for n in [task, *tests]:
        if re.search(r"(?<![A-Za-z0-9_-])" + re.escape(n) + r"(?![A-Za-z0-9_-])", text):
            return True
    return False


def leg_prior_art(lane: Path, cfg: dict, confirmed: list[str], idx: list[dict]):
    L, rej, urls, new, known = [], [], set(), 0, 0
    p = lane / RUN_DIR / "prior-art.json"
    rows = json.loads(p.read_text()) if p.is_file() else []
    if not isinstance(rows, list):
        rows, rej = [], ["non-list"]
    tests_of: dict[str, list[str]] = {}
    for t in idx:
        tests_of.setdefault(t["task"], []).append(t["name"])
    covered = set()

    def fetched(r, key):
        f = inside(lane, r.get(key), f"{RUN_DIR}/fetched")
        if f is None or sha256_file(f) != r.get(key + "_sha256"):
            return None, None
        return f.read_text(encoding="utf-8", errors="replace"), f

    for r in rows:
        why = None
        try:
            v, task = r.get("verdict"), r.get("task")
            tl = tests_of.get(task, [])
            if task in covered:
                why = "duplicate-task-row"            # A3: exactly one row per confirmed task
            elif task not in confirmed:
                why = "task-not-confirmed"
            elif v not in ("phenomenon-new", "phenomenon-known"):
                why = "bad-verdict"
            elif not re.match(r"https?://[^/\s]+\.[^/\s]+/", str(r.get("url", "")) + "/") or "example.org" in r["url"]:
                why = "bad-url"
            else:
                text, _f = fetched(r, "fetched")
                q = norm(str(r.get("quote", "")))
                h = HDR.match(text) if text else None
                if text is None:
                    why = "fetch-missing-outside-fetched-dir-or-digest-mismatch"
                elif not h or url_key(h.group(1)) != url_key(r["url"]):
                    why = "archive-header-url-does-not-match-row-url"
                elif not (8 <= len(q.split()) <= 25) or q not in norm(text):
                    why = "quote-not-8to25-words-or-not-in-fetch"
                elif v == "phenomenon-known" and not names_task(q, task, tl):
                    why = "known-quote-does-not-name-the-task-or-its-tests"
                elif v == "phenomenon-new":
                    sw = r.get("sweep")
                    if names_task(text, task, tl):
                        why = "new-archive-names-the-task"
                    elif not isinstance(sw, list) or len(sw) < 2:
                        why = "new-needs-two-sweep-fetches"
                    else:
                        seen_h = set()
                        for s in sw:
                            st, sf = fetched(s, "file") if isinstance(s, dict) else (None, None)
                            if st is None or names_task(st, task, tl) or sha256_file(sf) in seen_h or not HDR.match(st):
                                why = "sweep-fetch-missing-duplicate-headerless-or-names-the-task"
                                break
                            seen_h.add(sha256_file(sf))
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
def verdict(lane: Path, cfg: dict, candidates_only=False, fixture=False) -> tuple[int, list[str]]:
    lines: list[str] = []
    ok_pins, l = leg_pins(lane, cfg)
    lines += l
    ok_fz, l, info = leg_freeze(lane, cfg)
    lines += l
    ok_or = ok_cf = ok_pa = False
    if ok_pins and ok_fz:
        ok_or, l, v2, _decided = leg_oracle(lane, cfg, info)
        lines += l
        idx = json.loads((lane / RUN_DIR / "tests-index.json").read_text())["tests"]
        if candidates_only:
            try:
                cand = candidates(lane, cfg, v2, idx)
            except RuntimeError:
                lines.append("CANDIDATES BASE-TIP-UNAVAILABLE")
                return 1, lines

            for t in sorted(cand):
                lines.append(f"CANDIDATE {t} tests={','.join(x['name'] for x in cand[t])}")
            lines.append(f"CANDIDATES never_read_tasks={len(cand)}")
            return 0, lines
        ok_cf, l, good = leg_confirm(lane, cfg, info, v2, idx)
        lines += l
        ok_pa, l = leg_prior_art(lane, cfg, good, idx)
        lines += l
    else:
        lines.append("ORACLE not evaluable (pins or freeze failed)")
        lines.append("CONFIRM new_confirmed=0")
        lines.append("PRIOR-ART rows=0")
    ok = ok_pins and ok_fz and ok_or and ok_cf and ok_pa
    lines.append(f"PREDICATE R53-C1{'-FIXTURE' if fixture else ''} {'pass' if ok else 'fail'}")
    return (0 if ok else 1), lines


# ---- selftest (forged-but-complete controls on a synthetic lane) -------------------------------------
def selftest() -> int:
    top = Path(tempfile.mkdtemp(prefix="r53c1-st-", dir=os.environ.get("TMPDIR") or tempfile.gettempdir()))
    fails: list[str] = []
    ncase = [0]

    # F4 tripwire: the constants the real run uses equal the frozen literals written here
    lit = dict(POP_SHA="0230b68c666c1e0649b42d61d7121a30eedf247411642bbf397e3390436b5cfc",
               PIN_TREE_SHA="96b472489cbec0f4f6319db510b40284efa92b01b4badbc112d922662d42cbb9",
               TESTS_INDEX_SHA="579d567fd66f5fc0bc71957cdc887e9bb952c63b3fd9d2726e67c963897c7330",
               R52_AUDIT_SHA="0b1d4213b9522cfb1cf9bb615d03d278e6ac75b87a3984095d410faf1707a7b3",
               TESTS_TOTAL=305, CAPTURES_EXPECTED=183, EXCLUDED_PATH="sanitize-git-repo/tests/test_outputs.py",
               EXCLUDED_BLOB="3269e74e727fda61c936ca34b8f3bfaacf199dda", BASE_TIP="536925b5320fa64298030b4ee76a58fc4b82723f",
               BALANCE_MIN=10, CONTROL_MIN=10, CONFIRM_MIN=3, URL_MIN=3, LABEL_DIR=".ufo/waves/round-53/w1",
               SHARD_DIR=".ufo/waves/round-53/labels")
    ok = all(FROZEN[k] == v for k, v in lit.items()) and len(FROZEN["LABEL_SEATS"]) == 8 and (
        ORACLE_MAX_DISAGREE, ORACLE_MAX_CONTESTED, LABEL_AGREE_MIN, CONTROL_RATIO, QUOTE_MIN_CHARS) == (0.03, 0.15, 0.90, 2, 20)
    ncase[0] += 1
    print(f"SELFTEST frozen-constants {'ok' if ok else 'FAIL'}")
    if not ok:
        fails.append("frozen-constants")

    lane = top / "lane"
    lane.mkdir()
    sh = lambda *a: subprocess.run(a, check=True, capture_output=True)  # noqa: E731

    def w(rel, text, mode="w"):
        p = lane / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        (p.write_bytes if mode == "wb" else p.write_text)(text)
        return p

    def commit(msg, *paths):
        sh("git", "-C", str(lane), "add", *(paths or ["-A"]))
        sh("git", "-C", str(lane), "commit", "-q", "--allow-empty", "-m", msg)

    sh("git", "-C", str(lane), "init", "-q")
    for k, v in (("user.email", "t@t.invalid"), ("user.name", "selftest")):
        sh("git", "-C", str(lane), "config", k, v)
    g1 = b"def test_a():\n    assert Path('/x').exists()\n\n\ndef test_b():\n    assert open('/x').read() == 'hi'\n"
    g2 = b"def test_c():\n    assert Path('/y').is_file()\n"
    g3 = b"def test_d():\n    assert Path('/z').is_dir()\n\n\ndef test_e():\n    assert 1 == 1\n"
    ex = b"def test_z():\n    assert True\n"
    caps = {"t1/tests/test_outputs.py": g1, "t2/tests/test_outputs.py": g2, "t3/tests/test_outputs.py": g3, "tx/tests/test_outputs.py": ex}
    for rel, b in caps.items():
        if not rel.startswith("tx/"):
            w("corpus/evidence/round52/graders/" + rel, b, "wb")
    pop = {"tasks": {"t1": [], "t2": [], "t3": [], "tx": []}, "capture_population": {k.split("/")[0]: [k] for k in caps}}
    w("plans/round52-tasks.json", json.dumps(pop))
    w(f"{RUN_DIR}/pin-tree-2fd12b88.json", json.dumps({"blobs": [{"path": k, "sha": blob_sha1(b)} for k, b in caps.items()]}))
    sys.path.insert(0, str(Path(__file__).parent))
    import round53_c1_extract as ex_mod
    w(f"{RUN_DIR}/tests-index.json", json.dumps(ex_mod.index(lane)))
    w("plans/round52_c1_grader_audit.py",
      "def classify_tests(body):\n    return [{'test': n, 'class': 'P0'} for n in ('test_a', 'test_b', 'test_c', 'test_d', 'test_e')]\n")
    clf = ("import ast\n\ndef classify_source(src):\n    out = {}\n    for n in ast.parse(src).body:\n"
           "        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):\n"
           "            d = ast.dump(n)\n            out[n.name] = 'P1' if 'read' not in d and 'Constant(value=1)' not in d else 'P0'\n    return out\n")
    w("corpus/knowledge/old.md", "nothing\n")
    for f in ("SCORECARD.md", "LOG.md", "SKILL.md", "corpus/README.md"):
        w(f, "x\n")
    w("corpus/evidence/round52/confirmations.json", "[]")
    commit("base")
    base = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    seats = {"A": "LabA", "B": "LabB", "C": "LabC"}
    ids = ["t1::test_a", "t1::test_b", "t2::test_c", "t3::test_d", "t3::test_e"]
    # shards: every test in exactly two shards
    shard_ids = {"A": ["t1::test_a", "t1::test_b", "t3::test_d"], "B": ["t1::test_a", "t2::test_c", "t3::test_e"],
                 "C": ["t1::test_b", "t2::test_c", "t3::test_d", "t3::test_e"]}
    for k, lst in shard_ids.items():
        w(f"{SHARD_DIR}/shard-{k}.json", json.dumps([{"id": i} for i in lst]))
    truth = {"t1::test_a": "Y", "t1::test_b": "N", "t2::test_c": "Y", "t3::test_d": "Y", "t3::test_e": "N"}
    cfg = dict(FROZEN, POP_SHA=sha256_file(lane / "plans/round52-tasks.json"), PIN_TREE_SHA=sha256_file(lane / f"{RUN_DIR}/pin-tree-2fd12b88.json"),
               TESTS_INDEX_SHA=sha256_file(lane / f"{RUN_DIR}/tests-index.json"),
               R52_AUDIT_SHA=sha256_file(lane / "plans/round52_c1_grader_audit.py"), TESTS_TOTAL=5, CAPTURES_EXPECTED=3,
               EXCLUDED_PATH="tx/tests/test_outputs.py", EXCLUDED_BLOB=blob_sha1(ex), BASE_TIP=base, CONFIRM_MIN=1, URL_MIN=1,
               BALANCE_MIN=1, CONTROL_MIN=1, LABEL_SEATS=seats, LABEL_DIR=".ufo/waves/round-53/w1")
    commit("shards", "-A")

    def write_labels(over=None):
        for k, s in seats.items():
            lab = {i: {"label": truth[i], "why": "fixture"} for i in shard_ids[k]}
            for (kk, i), v in (over or {}).items():
                if kk == k:
                    lab[i] = {"label": v, "why": "fixture"}
            w(f"{cfg['LABEL_DIR']}/{s}/labels.json", json.dumps({"seat": s, "labels": lab}))

    def freeze_json(authors=("AuthorSeat",)):
        w("plans/round53-c1-freeze.json", json.dumps({
            "classifier_sha256": sha256_file(lane / "plans/round53_c1_classify.py"), "author_seats": list(authors),
            "label_sha256": {s: sha256_file(lane / cfg["LABEL_DIR"] / s / "labels.json") for s in seats.values()},
            "shard_sha256": {k: sha256_file(lane / cfg["SHARD_DIR"] / f"shard-{k}.json") for k in seats}}))

    def land(over=None, authors=("AuthorSeat",)):
        """The honest order: labels exist on disk unopened, pinned by digest in the freeze commit, committed afterwards."""
        write_labels(over)
        w("plans/round53_c1_classify.py", clf)
        freeze_json(authors)
        commit("freeze: classifier + freeze file", "plans/round53_c1_classify.py", "plans/round53-c1-freeze.json")
        commit("labels", cfg["LABEL_DIR"])

    def run(label, want_ok, want_in=(), cfgx=None):
        rc, lines = verdict(lane, cfgx or cfg, fixture=True)
        ncase[0] += 1
        text = "\n".join(lines)
        ok = (rc == 0) == want_ok and all(x in text for x in want_in)
        print(f"SELFTEST {label} rc={rc} {'ok' if ok else 'FAIL'}")
        if not ok:
            fails.append(label)
            print(text)

    run("nothing-committed", False, ("FREEZE absent", "PREDICATE R53-C1-FIXTURE fail"))
    land()
    w(f"{RUN_DIR}/confirmations.json", "[]")
    w(f"{RUN_DIR}/prior-art.json", "[]")
    commit("empty evidence")
    run("no-confirmations", False, ("CONFIRM candidates_never_read=", "new_confirmed=0", "clean=yes",
                                    "classifier_and_freeze_one_commit=yes", "labels_after_freeze_and_untouched=yes", "disagree=0"))
    rep = w(".ufo/waves/round-53/w2/ReaderSeat/report.md", "reader report: t2 test_c reads Path('/y').is_file() presence only; t3 test_d\n")
    good = {"task": "t2", "test_id": "t2::test_c", "quote": "assert Path('/y').is_file()", "reader": "ReaderSeat", "confirmed": True,
            "report": ".ufo/waves/round-53/w2/ReaderSeat/report.md", "report_sha256": sha256_file(rep)}
    base_html = "SOURCE-URL: https://real.example.net/a\nthe grader test_c of task t2 merely checks the file exists and nothing more per this page\n"
    w(f"{RUN_DIR}/fetched/a.html", base_html)
    w(f"{RUN_DIR}/fetched/n.html", "SOURCE-URL: https://real.example.net/b\na page about a different benchmark and about nothing that matters here at all today\n")
    w(f"{RUN_DIR}/fetched/s1.html", "SOURCE-URL: https://real.example.net/s1\nunrelated page one\n")
    w(f"{RUN_DIR}/fetched/s2.html", "SOURCE-URL: https://real.example.net/s2\nunrelated page two\n")
    w(f"{RUN_DIR}/fetched/hdrless.html", "unrelated page three without a header\n")
    F = lambda n: lane / f"{RUN_DIR}/fetched/{n}"  # noqa: E731
    d = lambda n: sha256_file(F(n))  # noqa: E731
    known = {"task": "t2", "verdict": "phenomenon-known", "url": "https://real.example.net/a", "fetched": f"{RUN_DIR}/fetched/a.html",
             "fetched_sha256": d("a.html"), "quote": "the grader test_c of task t2 merely checks the file exists and nothing more"}
    new = {"task": "t2", "verdict": "phenomenon-new", "url": "https://real.example.net/b", "fetched": f"{RUN_DIR}/fetched/n.html",
           "fetched_sha256": d("n.html"), "quote": "a page about a different benchmark and about nothing that matters here at all",
           "sweep": [{"file": f"{RUN_DIR}/fetched/s1.html", "file_sha256": d("s1.html")},
                     {"file": f"{RUN_DIR}/fetched/s2.html", "file_sha256": d("s2.html")}]}
    state = {}

    def evidence(conf=None, pa=None):
        w(f"{RUN_DIR}/confirmations.json", json.dumps([conf or good]))
        w(f"{RUN_DIR}/prior-art.json", json.dumps(pa if pa is not None else [new]))
        commit("evidence")

    evidence(pa=[known])
    run("known-only-fails-score-rule", False, ("new=0",))
    evidence()
    run("genuine-fixture-passes", True, ("PREDICATE R53-C1-FIXTURE pass", "new_confirmed=1", "new=1", "known=0", "per_label_agree=1.000"))

    def forge(label, conf=None, pa=None, want=()):
        evidence(conf, pa)
        run(label, False, want)

    forge("forged-confirmed-string", dict(good, confirmed="false"), want=("confirmed-not-true",))
    forge("forged-reader-is-author", dict(good, reader="AuthorSeat"), want=("reader-is-author-or-labeller",))
    forge("forged-reader-is-labeller", dict(good, reader="C1LabelScoutA"), want=("reader-is-author-or-labeller",))
    forge("forged-quote-outside-span", dict(good, quote="assert Path('/x').exists()"), want=("quote-short-or-outside-test-span",))
    forge("forged-short-quote", dict(good, quote="assert"), want=("quote-short-or-outside-test-span",))
    forge("forged-report-names-other-task", dict(good, task="t1", test_id="t1::test_a", quote="assert Path('/x').exists()"),
          want=("report-does-not-name-task",))
    w(".ufo/waves/round-53/w2/ReaderSeat/wordbound.md", "ReaderSeat notes: t2st and xt2 are other words; nothing else\n")
    forge("forged-report-names-task-inside-a-word", dict(good, report=".ufo/waves/round-53/w2/ReaderSeat/wordbound.md",
          report_sha256=sha256_file(lane / ".ufo/waves/round-53/w2/ReaderSeat/wordbound.md")), want=("report-does-not-name-task",))
    evidence()
    run("base-tip-unavailable-fails-closed", False, ("BASE-TIP-UNAVAILABLE",), cfgx=dict(cfg, BASE_TIP="0" * 40))
    forge("forged-report-digest", dict(good, report_sha256="0" * 64), want=("digest-mismatch",))
    w("corpus/evidence/round53/outside.md", "t2 ReaderSeat note outside the wave dir\n")
    forge("forged-report-outside-wave-dir", dict(good, report="corpus/evidence/round53/outside.md", report_sha256=sha256_file(lane / "corpus/evidence/round53/outside.md")),
          want=("outside-wave-dir",))
    forge("forged-report-traversal", dict(good, report=".ufo/waves/round-53/w2/../../../../corpus/evidence/round53/outside.md"), want=("outside-wave-dir",))
    forge("forged-prior-art-example", pa=[dict(new, url="https://example.org/x")], want=("bad-url",))
    forge("forged-prior-art-unfetched", pa=[dict(new, fetched=f"{RUN_DIR}/fetched/nope.html")], want=("fetch-missing",))
    forge("forged-prior-art-digest", pa=[dict(new, fetched_sha256="1" * 64)], want=("fetch-missing-outside-fetched-dir-or-digest-mismatch",))
    forge("forged-prior-art-quote", pa=[dict(new, quote="this sentence never occurs in the archived fetch at all ever and ever")], want=("quote-not-8to25",))
    forge("forged-prior-art-traversal", pa=[dict(new, fetched=f"{RUN_DIR}/fetched/../../round52/graders/t2/tests/test_outputs.py")], want=("fetch-missing",))
    forge("forged-prior-art-header-url", pa=[dict(new, url="https://real.example.net/other")], want=("archive-header-url-does-not-match-row-url",))
    forge("forged-new-without-sweep", pa=[{k: v for k, v in new.items() if k != "sweep"}], want=("new-needs-two-sweep-fetches",))
    forge("forged-sweep-file-twice", pa=[dict(new, sweep=[new["sweep"][0], new["sweep"][0]])], want=("sweep-fetch-missing-duplicate",))
    w(f"{RUN_DIR}/fetched/s3.html", "SOURCE-URL: https://real.example.net/search?q=t2\ntotal_count: 0\n")
    w(f"{RUN_DIR}/fetched/s4.html", "SOURCE-URL: https://real.example.net/s4\nresult mentions task t2 here\n")
    sw3 = [new["sweep"][0], {"file": f"{RUN_DIR}/fetched/s3.html", "file_sha256": d("s3.html")}]
    sw4 = [new["sweep"][0], {"file": f"{RUN_DIR}/fetched/s4.html", "file_sha256": d("s4.html")}]
    evidence(pa=[dict(new, sweep=sw3)])
    run("sweep-header-may-carry-the-task-id", True, ("PREDICATE R53-C1-FIXTURE pass",))
    forge("forged-sweep-body-names-the-task", pa=[dict(new, sweep=sw4)], want=("sweep-fetch-missing-duplicate",))
    forge("forged-two-rows-for-one-task", pa=[known, new], want=("duplicate-task-row",))
    forge("forged-sweep-headerless", pa=[dict(new, sweep=[new["sweep"][0], {"file": f"{RUN_DIR}/fetched/hdrless.html", "file_sha256": d("hdrless.html")}])],
          want=("sweep-fetch-missing-duplicate-headerless",))
    forge("forged-new-archive-names-task", pa=[dict(new, fetched=f"{RUN_DIR}/fetched/a.html", fetched_sha256=d("a.html"), url="https://real.example.net/a",
                                                 quote=known["quote"])], want=("new-archive-names-the-task",))
    forge("forged-known-quote-not-naming-task", pa=[dict(known, quote="merely checks the file exists and nothing more per this page")],
          want=("known-quote-does-not-name-the-task-or-its-tests",))
    # pins
    evidence()
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
    r52p = lane / "plans/round52_c1_grader_audit.py"
    r52o = r52p.read_text()
    r52p.write_text(r52o + "\n# control tampered\n")
    run("tampered-r52-control-module", False, ("r52_audit_sha=BAD",))
    r52p.write_text(r52o)
    # freeze integrity (R1, R2, F1, F2) and tree cleanliness (R3)
    labp = lane / cfg["LABEL_DIR"] / "LabA" / "labels.json"
    labo = labp.read_text()
    labp.write_text(labo.replace('"Y"', '"N"', 1))
    run("forged-dirty-label-edit-uncommitted", False, ("clean=NO", "label_files_pinned=BAD"))
    commit("label edited after freeze (committed)", "-A")
    run("forged-label-edited-after-freeze-committed", False, ("label_files_pinned=BAD", "labels_after_freeze_and_untouched=NO"))
    labp.write_text(labo)
    commit("label restored", "-A")
    run("label-restored-still-touched-twice", False, ("labels_after_freeze_and_untouched=NO",))
    cp = lane / "plans/round53_c1_classify.py"
    cpo = cp.read_text()
    cp.write_text(cpo + "\n# tuned after seeing the labels\n")
    commit("classifier edited", "-A")
    run("classifier-edited-after-freeze", False, ("classifier_sha=BAD", "classifier_and_freeze_one_commit=NO"))
    fz = lane / "plans/round53-c1-freeze.json"
    fz.write_text(json.dumps(dict(json.loads(fz.read_text()), classifier_sha256=sha256_file(cp))))
    commit("freeze re-hashed", "-A")
    run("forged-classifier-edit-and-freeze-rehash", False, ("classifier_and_freeze_one_commit=NO",))
    # rebuild a lane history where the honest order was violated
    main_br = subprocess.run(["git", "-C", str(lane), "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
    sh("git", "-C", str(lane), "branch", "-f", "r53main", "HEAD")

    def rebuild(label, mode, want, **kw):
        sh("git", "-C", str(lane), "checkout", "-q", "-f", "-B", f"r-{label}", base)
        sh("git", "-C", str(lane), "checkout", "r53main", "--", ".ufo/waves/round-53/w2", f"{RUN_DIR}/fetched", "corpus/evidence/round53/outside.md")
        sh("git", "-C", str(lane), "reset", "-q")
        for f in ("plans/round53-c1-freeze.json",):
            (lane / f).unlink(missing_ok=True)
        shutil.rmtree(lane / cfg["LABEL_DIR"], ignore_errors=True)
        for k, lst in shard_ids.items():
            w(f"{SHARD_DIR}/shard-{k}.json", json.dumps([{"id": i} for i in lst]))
        commit("shards again", "-A")
        write_labels(kw.get("over"))
        cp.write_text(clf)
        if mode == "labels-first":
            commit("labels before freeze", cfg["LABEL_DIR"])
            freeze_json(); commit("freeze", "plans/round53_c1_classify.py", "plans/round53-c1-freeze.json")
        elif mode == "one-commit":
            freeze_json(); commit("everything in one commit", "-A")
        elif mode == "authors-edited":
            freeze_json(("AuthorSeat",)); commit("freeze", "plans/round53_c1_classify.py", "plans/round53-c1-freeze.json")
            commit("labels", cfg["LABEL_DIR"])
            fz.write_text(json.dumps(dict(json.loads(fz.read_text()), author_seats=["Other"]))); commit("authors edited", "-A")
        elif mode == "classifier-last":
            freeze_json(); commit("freeze file only", "plans/round53-c1-freeze.json"); commit("labels", cfg["LABEL_DIR"])
            commit("classifier last", "plans/round53_c1_classify.py")
        elif mode == "labelers-are-authors":
            freeze_json(("AuthorSeat", "LabA")); commit("freeze", "plans/round53_c1_classify.py", "plans/round53-c1-freeze.json")
            commit("labels", cfg["LABEL_DIR"])
        else:  # honest
            freeze_json(); commit("freeze", "plans/round53_c1_classify.py", "plans/round53-c1-freeze.json")
            commit("labels", cfg["LABEL_DIR"])
        if kw.get("evidence", True):
            evidence()
        run(label, kw.get("ok", False), want)

    rebuild("labels-before-freeze", "labels-first", ("labels_after_freeze_and_untouched=NO",))
    rebuild("freeze-and-labels-one-commit", "one-commit", ("labels_after_freeze_and_untouched=NO",))
    rebuild("classifier-committed-after-labels", "classifier-last", ("classifier_and_freeze_one_commit=NO",))
    rebuild("authors-edited-after-freeze", "authors-edited", ("classifier_and_freeze_one_commit=NO",))
    rebuild("labeller-listed-as-author", "labelers-are-authors", ("authors=2", "bad_label_rows="))
    rebuild("rebuilt-honest-history-passes", "honest", ("PREDICATE R53-C1-FIXTURE pass",), ok=True)
    # oracle numbers on the honest history
    rebuild("oracle-disagreement", "honest", ("disagree=1",), over={("A", "t1::test_a"): "N", ("B", "t1::test_a"): "N"})
    rebuild("oracle-contested-over-budget", "honest", ("contested=1",), over={("A", "t1::test_a"): "N"})
    # all-P1 do-nothing classifier + copied labels (all Y): balance leg
    cp.write_text("def classify_source(src):\n    import ast\n    return {n.name: 'P1' for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}\n")
    allp1 = cp.read_text()
    clf_saved = clf
    clf = allp1  # noqa: F841  (rebuild() restores `clf`)
    ysets = {(k, i): "Y" for k, lst in shard_ids.items() for i in lst}
    rebuild("all-P1-classifier-with-copied-all-Y-labels", "honest", ("oracle_N=0",), over=ysets)
    clf = clf_saved
    shutil.rmtree(top, ignore_errors=True)
    print(f"SELFTEST cases={ncase[0]} failures={len(fails)}")
    return 0 if not fails else 1


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
