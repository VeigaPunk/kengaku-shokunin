#!/usr/bin/env python3
"""Final verification batch on the FROZEN counter (commit a34838f).

X1  labels committed BEFORE the freeze file -> does the order proof fail?
X2  the r52 control classifier is NOT digest-pinned -> can editing it make the
    control leg pass vacuously?
X3  CONFIRM quote need not be verbatim in the capture (whitespace-normalised)
X4  url_key collapse table
X5  a "sweep of >=2" may be two entries naming the same file
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
FROZEN = SCRATCH / "FROZEN_counter.py"
sys.path.insert(0, str(SCRATCH))
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
import round53_c1_extract as EX  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("mfroz", FROZEN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
T_RUN = "corpus/evidence/round53"


def sh(*a, cwd):
    subprocess.run(a, cwd=cwd, check=True, capture_output=True)


def build(root, labels_first=False, r52_stub="P0"):
    lane = root / "lane"
    lane.mkdir(parents=True)
    sh("git", "-C", str(lane), "init", "-q", cwd=lane)
    sh("git", "-C", str(lane), "config", "user.email", "t@t.invalid", cwd=lane)
    sh("git", "-C", str(lane), "config", "user.name", "st", cwd=lane)

    def w(rel, text, mode="w"):
        p = lane / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        (p.write_bytes if mode == "wb" else p.write_text)(text)
        return p

    g1 = b"def test_a():\n    assert Path('/x').exists()\n\n\ndef test_b():\n    assert open('/x').read() == 'hi'\n"
    g2 = b"def test_c():\n    assert Path('/y').is_file()\n"
    ex = b"def test_z():\n    assert True\n"
    caps = {"t1/tests/test_outputs.py": g1, "t2/tests/test_outputs.py": g2, "tx/tests/test_outputs.py": ex}
    for rel, b in caps.items():
        if not rel.startswith("tx/"):
            w("corpus/evidence/round52/graders/" + rel, b, "wb")
    pop = {"tasks": {"t1": [], "t2": [], "tx": []}, "capture_population": {k.split("/")[0]: [k] for k in caps}}
    w("plans/round52-tasks.json", json.dumps(pop))
    w(f"{T_RUN}/pin-tree-2fd12b88.json",
      json.dumps({"blobs": [{"path": k, "sha": mod.blob_sha1(b)} for k, b in caps.items()]}))
    w(f"{T_RUN}/tests-index.json", json.dumps(EX.index(lane)))
    w("plans/round52_c1_grader_audit.py",
      "def classify_tests(body):\n"
      f"    return [{{'test': 'test_a', 'class': '{r52_stub}'}}, {{'test': 'test_b', 'class': '{r52_stub}'}}, {{'test': 'test_c', 'class': '{r52_stub}'}}]\n")
    clf = ("import ast\n\ndef classify_source(src):\n    out = {}\n    for n in ast.parse(src).body:\n"
           "        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):\n"
           "           out[n.name] = 'P1' if 'read' not in ast.dump(n) and 'True' not in ast.dump(n) else 'P0'\n    return out\n")
    w("plans/round53_c1_classify.py", clf)
    w("corpus/knowledge/old.md", "nothing\n")
    for f in ("SCORECARD.md", "LOG.md", "SKILL.md", "corpus/README.md"):
        w(f, "x\n")
    w("corpus/evidence/round52/confirmations.json", "[]")
    sh("git", "-C", str(lane), "add", "-A", cwd=lane)
    sh("git", "-C", str(lane), "commit", "-q", "-m", "base", cwd=lane)
    base = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cfg = dict(mod.CFG, POP_SHA=mod.sha256_file(lane / "plans/round52-tasks.json"),
               PIN_TREE_SHA=mod.sha256_file(lane / f"{T_RUN}/pin-tree-2fd12b88.json"),
               TESTS_INDEX_SHA=mod.sha256_file(lane / f"{T_RUN}/tests-index.json"),
               TESTS_TOTAL=3, CAPTURES_EXPECTED=2, EXCLUDED_PATH="tx/tests/test_outputs.py",
               EXCLUDED_BLOB=mod.blob_sha1(ex), BASE_TIP=base, CONFIRM_MIN=1, URL_MIN=1)
    lab = {"t1::test_a": (["L1", "L2"], ["Y", "Y"]), "t1::test_b": (["L1", "L3"], ["N", "N"]),
           "t2::test_c": (["L2", "L3"], ["Y", "Y"])}
    labtxt = json.dumps({"labels": {k: {"labelers": a, "labels": b} for k, (a, b) in lab.items()}})
    fztxt = json.dumps({"classifier_sha256": mod.sha256_file(lane / "plans/round53_c1_classify.py"),
                        "author_seats": ["AuthorSeat"]})
    if labels_first:
        w(f"{T_RUN}/oracle-labels.json", labtxt)
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "labels-first", cwd=lane)
        w("plans/round53-c1-freeze.json", fztxt)
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze-second", cwd=lane)
    else:
        w("plans/round53-c1-freeze.json", fztxt)
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze", cwd=lane)
        w(f"{T_RUN}/oracle-labels.json", labtxt)
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "labels", cwd=lane)
    return lane, cfg


def evidence(lane, report_rel=".ufo/waves/round-53/w2/ReaderSeat/report.md", quote="assert Path('/y').is_file()",
             sweep_dup=False, url="https://real.example.net/b"):
    p = lane / report_rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("reader report: t2 test_c reads Path('/y').is_file() presence only\n")
    good = {"task": "t2", "test_id": "t2::test_c", "quote": quote, "reader": "ReaderSeat",
            "confirmed": True, "report": report_rel, "report_sha256": mod.sha256_file(p)}
    (lane / f"{T_RUN}/confirmations.json").write_text(json.dumps([good]))
    f = lane / f"{T_RUN}/fetched"
    f.mkdir(parents=True, exist_ok=True)
    (f / "a.html").write_text("the grader test_c merely checks the file exists and nothing more\n")
    (f / "s1.html").write_text("unrelated page one\n")
    (f / "s2.html").write_text("unrelated page two\n")
    sweep = [{"file": f"{T_RUN}/fetched/s1.html", "file_sha256": mod.sha256_file(f / "s1.html")},
             {"file": f"{T_RUN}/fetched/s2.html", "file_sha256": mod.sha256_file(f / "s2.html")}]
    if sweep_dup:
        sweep = [sweep[0], dict(sweep[0])]
    pa = {"task": "t2", "verdict": "phenomenon-new", "url": url,
          "fetched": f"{T_RUN}/fetched/a.html", "fetched_sha256": mod.sha256_file(f / "a.html"),
          "quote": "the grader test_c merely checks the file exists and nothing more", "sweep": sweep}
    (lane / f"{T_RUN}/prior-art.json").write_text(json.dumps([pa]))


def show(tag, lines, keys=("FREEZE", "ORACLE", "CONFIRM", "PRIOR-ART", "PREDICATE")):
    for l in lines:
        if l.startswith(keys):
            print("   ", l)


def main():
    root = Path(tempfile.mkdtemp(prefix="final-", dir=str(SCRATCH)))

    print("=== X1: labels committed BEFORE the freeze file (order proof must fail) ===")
    lane, cfg = build(root / "x1", labels_first=True)
    evidence(lane)
    rc, lines = mod.verdict(lane, cfg)
    print("   rc=", rc)
    show("X1", lines)

    print()
    print("=== X2: r52 control classifier edited so it always says P1 (no digest pin on it) ===")
    lane, cfg = build(root / "x2", r52_stub="P1")
    evidence(lane)
    rc, lines = mod.verdict(lane, cfg)
    print("   rc=", rc)
    show("X2", lines)

    print()
    print("=== X3: CONFIRM quote not verbatim in the capture ===")
    lane, cfg = build(root / "x3")
    g = lane / "corpus/evidence/round52/graders/t2/tests/test_outputs.py"
    g.write_text("def test_c():\n    assert  Path('/y').is_file()\n")
    evidence(lane, quote="assert Path('/y').is_file()")
    rc, lines = mod.verdict(lane, cfg)
    print("   capture bytes:", repr(g.read_text()))
    print("   quote         :", repr("assert Path('/y').is_file()"))
    print("   rc=", rc)
    show("X3", lines, keys=("CONFIRM", "REJECTED"))

    print()
    print("=== X4: url_key collapse table ===")
    for u in ["https://Ex.com/A", "https://ex.com/a", "https://ex.com/a/", "https://ex.com/a?x=1",
              "https://ex.com/a#frag", "https://ex.com/a?x=1#f", "https://ex.com/a?q=2", "https://ex.com/A"]:
        print(f"    {u!r:32} -> {mod.url_key(u)!r}")

    print()
    print("=== X5: sweep of two entries naming the SAME file ===")
    lane, cfg = build(root / "x5")
    evidence(lane, sweep_dup=True)
    rc, lines = mod.verdict(lane, cfg)
    print("   rc=", rc)
    show("X5", lines, keys=("PRIOR-ART", "REJECTED"))

    print()
    print("=== X6: three distinct URLs that collapse to one url_key ===")
    lane, cfg = build(root / "x6")
    p = lane / f"{T_RUN}/prior-art.json"
    rows = json.loads(p.read_text())
    rows[0]["url"] = "https://ex.com/a"
    p.write_text(json.dumps(rows))
    rc, lines = mod.verdict(lane, cfg)
    print("   (single row, one URL) urls=", [l for l in lines if l.startswith("PRIOR-ART")])

    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
