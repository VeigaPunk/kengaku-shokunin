#!/usr/bin/env python3
"""FROZEN-counter checks that were still open:
  W1  freeze file REWRITTEN after the labels commit, together with the classifier
      -> does the FREEZE leg still report order=freeze-before-labels and sha=ok?
  W2  the classifier edited after the freeze commit, freeze file rewritten to match
      -> same question, and is the classifier at the freeze commit recovered?
  W3  selftest case isolation: for each frozen case, does neutralising the check it
      names make THAT case fail?  (mutation -> failing case names)
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
FROZEN = SCRATCH / "FROZEN_counter.py"
A1 = SCRATCH / "A1_counter.py"
sys.path.insert(0, str(SCRATCH))
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
import round53_c1_extract as EX  # noqa: E402


def sh(*a, cwd):
    subprocess.run(a, cwd=cwd, check=True, capture_output=True)


def build(root, mod, separate_labels=True):
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
    w(f"{mod.RUN_DIR}/pin-tree-2fd12b88.json",
      json.dumps({"blobs": [{"path": k, "sha": mod.blob_sha1(b)} for k, b in caps.items()]}))
    w(f"{mod.RUN_DIR}/tests-index.json", json.dumps(EX.index(lane)))
    w("plans/round52_c1_grader_audit.py",
      "def classify_tests(body):\n    return [{'test': 'test_a', 'class': 'P0'}, {'test': 'test_b', 'class': 'P0'}, {'test': 'test_c', 'class': 'P0'}]\n")
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
               PIN_TREE_SHA=mod.sha256_file(lane / f"{mod.RUN_DIR}/pin-tree-2fd12b88.json"),
               TESTS_INDEX_SHA=mod.sha256_file(lane / f"{mod.RUN_DIR}/tests-index.json"),
               TESTS_TOTAL=3, CAPTURES_EXPECTED=2, EXCLUDED_PATH="tx/tests/test_outputs.py",
               EXCLUDED_BLOB=mod.blob_sha1(ex), BASE_TIP=base, CONFIRM_MIN=1, URL_MIN=1)
    w("plans/round53-c1-freeze.json", json.dumps({"classifier_sha256": mod.sha256_file(lane / "plans/round53_c1_classify.py"),
                                                  "author_seats": ["AuthorSeat"]}))
    sh("git", "-C", str(lane), "add", "-A", cwd=lane)
    sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze", cwd=lane)
    lab = {"t1::test_a": (["L1", "L2"], ["Y", "Y"]), "t1::test_b": (["L1", "L3"], ["N", "N"]),
           "t2::test_c": (["L2", "L3"], ["Y", "Y"])}
    w(f"{mod.RUN_DIR}/oracle-labels.json",
      json.dumps({"labels": {k: {"labelers": a, "labels": b} for k, (a, b) in lab.items()}}))
    sh("git", "-C", str(lane), "add", "-A", cwd=lane)
    sh("git", "-C", str(lane), "commit", "-q", "-m", "labels", cwd=lane)
    return lane, cfg


def evidence(lane, mod, report_rel=".ufo/waves/round-53/w2/ReaderSeat/report.md"):
    p = lane / report_rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("reader report: t2 test_c reads Path('/y').is_file() presence only\n")
    good = {"task": "t2", "test_id": "t2::test_c", "quote": "assert Path('/y').is_file()", "reader": "ReaderSeat",
            "confirmed": True, "report": report_rel, "report_sha256": mod.sha256_file(p)}
    (lane / f"{mod.RUN_DIR}/confirmations.json").write_text(json.dumps([good]))
    f = lane / f"{mod.RUN_DIR}/fetched"
    f.mkdir(parents=True, exist_ok=True)
    (f / "a.html").write_text("the grader test_c merely checks the file exists and nothing more\n")
    (f / "s1.html").write_text("unrelated page one\n")
    (f / "s2.html").write_text("unrelated page two\n")
    pa = {"task": "t2", "verdict": "phenomenon-new", "url": "https://real.example.net/b",
          "fetched": f"{mod.RUN_DIR}/fetched/a.html", "fetched_sha256": mod.sha256_file(f / "a.html"),
          "quote": "the grader test_c merely checks the file exists and nothing more",
          "sweep": [{"file": f"{T_RUN}/fetched/s1.html", "file_sha256": mod.sha256_file(f / "s1.html")},
                    {"file": f"{T_RUN}/fetched/s2.html", "file_sha256": mod.sha256_file(f / "s2.html")}]}
    (lane / f"{mod.RUN_DIR}/prior-art.json").write_text(json.dumps([pa]))


T_RUN = "corpus/evidence/round53"


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def w1_w2(tag, path, name):
    mod = load(path, name)
    print(f"\n########## {tag} ##########")
    root = Path(tempfile.mkdtemp(prefix=f"w-{tag}-", dir=str(SCRATCH)))
    lane, cfg = build(root, mod)
    cl = lane / "plans/round53_c1_classify.py"
    cl.write_text(cl.read_text() + "\n# TUNED AFTER THE LABELS WERE COMMITTED\n")
    fzp = lane / "plans/round53-c1-freeze.json"
    fzp.write_text(json.dumps({"classifier_sha256": mod.sha256_file(cl), "author_seats": ["AuthorSeat"]}))
    sh("git", "-C", str(lane), "add", "-A", cwd=lane)
    sh("git", "-C", str(lane), "commit", "-q", "-m", "tune-after-labels", cwd=lane)
    evidence(lane, mod)
    rc, lines = mod.verdict(lane, cfg)
    for l in lines:
        if l.startswith(("FREEZE", "ORACLE", "CONFIRM", "PRIOR-ART", "PREDICATE")):
            print("   ", l)
    print("    git log --oneline:")
    for l in subprocess.run(["git", "-C", str(lane), "log", "--oneline"], capture_output=True, text=True).stdout.splitlines():
        print("      ", l)
    fz = subprocess.run(["git", "-C", str(lane), "log", "--diff-filter=A", "--format=%H", "--reverse",
                          "--", "plans/round53-c1-freeze.json"], capture_output=True, text=True).stdout.split()[0]
    old = subprocess.run(["git", "-C", str(lane), "show", f"{fz}:plans/round53_c1_classify.py"],
                         capture_output=True, text=True).stdout
    print("    classifier sha AT the freeze commit:", mod.hashlib.sha256(old.encode()).hexdigest())
    print("    classifier sha in the working tree :", mod.sha256_file(cl))
    print("    -> classifier edited after the freeze commit:",
          mod.hashlib.sha256(old.encode()).hexdigest() != mod.sha256_file(cl))
    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    w1_w2("FROZEN", FROZEN, "mfroz")
    w1_w2("A1", A1, "ma1")
