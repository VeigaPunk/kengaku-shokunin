#!/usr/bin/env python3
"""Last direct checks against the FROZEN counter (a34838f) on fixtures; plus real-corpus index coverage.
  (a) two VALID prior-art rows for the same confirmed task -> accepted?
  (b) phenomenon-known: archive mentions only a SUBSTRING of a test name -> accepted?
  (c) report text mentions only a SUBSTRING of the task id -> accepted?
  (d) real captures: any indented `def test_` the AST index does not list?
  (e) single-element sweep -> rejected? (is the >=2 rule itself correct in code?)
"""
import importlib.util, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin").resolve()
sys.path.insert(0, str(LANE / "plans"))
import round53_c1_extract as EX  # noqa: E402

spec = importlib.util.spec_from_file_location("mfroz8", SCRATCH / "FROZEN_counter.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
T_RUN = "corpus/evidence/round53"


def sh(*a, cwd):
    subprocess.run(a, cwd=cwd, check=True, capture_output=True)


def build(root):
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
    g2 = b"def test_cx():\n    assert Path('/y').is_file()\n"
    ex = b"def test_z():\n    assert True\n"
    caps = {"t1/tests/test_outputs.py": g1, "t2/tests/test_outputs.py": g2, "tx/tests/test_outputs.py": ex}
    for rel, b in caps.items():
        if not rel.startswith("tx/"):
            w("corpus/evidence/round52/graders/" + rel, b, "wb")
    pop = {"tasks": {"t1": [], "t2": [], "tx": []}, "capture_population": {k.split("/")[0]: [k] for k in caps}}
    w("plans/round52-tasks.json", json.dumps(pop))
    w(f"{T_RUN}/pin-tree-2fd12b88.json", json.dumps({"blobs": [{"path": k, "sha": mod.blob_sha1(b)} for k, b in caps.items()]}))
    w(f"{T_RUN}/tests-index.json", json.dumps(EX.index(lane)))
    w("plans/round52_c1_grader_audit.py",
      "def classify_tests(body):\n    return [{'test': 'test_a', 'class': 'P0'}, {'test': 'test_b', 'class': 'P0'}, {'test': 'test_cx', 'class': 'P0'}]\n")
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
    w("plans/round53-c1-freeze.json", json.dumps({"classifier_sha256": mod.sha256_file(lane / "plans/round53_c1_classify.py"),
                                                  "author_seats": ["AuthorSeat"]}))
    sh("git", "-C", str(lane), "add", "-A", cwd=lane)
    sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze", cwd=lane)
    lab = {"t1::test_a": (["L1", "L2"], ["Y", "Y"]), "t1::test_b": (["L1", "L3"], ["N", "N"]),
           "t2::test_cx": (["L2", "L3"], ["Y", "Y"])}
    w(f"{T_RUN}/oracle-labels.json", json.dumps({"labels": {k: {"labelers": a, "labels": b} for k, (a, b) in lab.items()}}))
    sh("git", "-C", str(lane), "add", "-A", cwd=lane)
    sh("git", "-C", str(lane), "commit", "-q", "-m", "labels", cwd=lane)
    return lane, cfg, w


def evidence(lane, w, report_text="reader report: t2 test_cx reads Path('/y').is_file() presence only\n",
             archive_text="the grader test_cx merely checks the file exists and nothing more\n",
             pa_extra=None, quote="the grader test_cx merely checks the file exists and nothing more"):
    rp = ".ufo/waves/round-53/w2/ReaderSeat/report.md"
    w(rp, report_text)
    good = {"task": "t2", "test_id": "t2::test_cx", "quote": "assert Path('/y').is_file()", "reader": "ReaderSeat",
            "confirmed": True, "report": rp, "report_sha256": mod.sha256_file(lane / rp)}
    w(f"{T_RUN}/confirmations.json", json.dumps([good]))
    w(f"{T_RUN}/fetched/a.html", archive_text)
    w(f"{T_RUN}/fetched/s1.html", "unrelated page one\n")
    w(f"{T_RUN}/fetched/s2.html", "unrelated page two\n")
    sweep = [{"file": f"{T_RUN}/fetched/s1.html", "file_sha256": mod.sha256_file(lane / f"{T_RUN}/fetched/s1.html")},
             {"file": f"{T_RUN}/fetched/s2.html", "file_sha256": mod.sha256_file(lane / f"{T_RUN}/fetched/s2.html")}]
    pa = {"task": "t2", "verdict": "phenomenon-new", "url": "https://real.example.net/b",
          "fetched": f"{T_RUN}/fetched/a.html", "fetched_sha256": mod.sha256_file(lane / f"{T_RUN}/fetched/a.html"),
          "quote": quote, "sweep": sweep}
    if pa_extra:
        pa.update(pa_extra)
    w(f"{T_RUN}/prior-art.json", json.dumps([pa]))
    return pa


def pa_lines(lines):
    return [l for l in lines if l.startswith("PRIOR-ART") or "REJECTED" in l or l.startswith("CONFIRM")]


def main():
    root = Path(tempfile.mkdtemp(prefix="v8-", dir=str(SCRATCH)))

    print("=== (a) two VALID rows for the same confirmed task ===")
    lane, cfg, w = build(root / "a")
    pa = evidence(lane, w)
    row2 = dict(pa, url="https://real.example.net/c")
    row2["sweep"] = pa["sweep"]
    w(f"{T_RUN}/prior-art.json", json.dumps([pa, row2]))
    rc, lines = mod.verdict(lane, cfg)
    for l in pa_lines(lines):
        print("   ", l)

    print("=== (b) phenomenon-known: archive names only a SUBSTRING of the test id 'test_cx' ===")
    lane, cfg, w = build(root / "b")
    known = {"verdict": "phenomenon-known", "url": "https://real.example.net/k",
             "archive_text": "tracker note: test_cxyz asserts only that the file exists and nothing more\n"}
    pa = evidence(lane, w, archive_text=known["archive_text"],
                  quote="tracker note: test_cxyz asserts only that the file exists and nothing more")
    pa2 = dict(pa, verdict="phenomenon-known", url=known["url"])
    pa2.pop("sweep", None)
    w(f"{T_RUN}/prior-art.json", json.dumps([pa2]))
    rc, lines = mod.verdict(lane, cfg)
    for l in pa_lines(lines):
        print("   ", l)

    print("=== (c) reader report names only a SUBSTRING of the task id 't2' ===")
    lane, cfg, w = build(root / "c")
    evidence(lane, w, report_text="reader report: the t20 suite reads Path('/y').is_file() presence only\n")
    rc, lines = mod.verdict(lane, cfg)
    for l in pa_lines(lines):
        print("   ", l)

    print("=== (e) single-element sweep (code's >=2 rule) ===")
    lane, cfg, w = build(root / "e")
    pa = evidence(lane, w)
    pa["sweep"] = pa["sweep"][:1]
    w(f"{T_RUN}/prior-art.json", json.dumps([pa]))
    rc, lines = mod.verdict(lane, cfg)
    for l in pa_lines(lines):
        print("   ", l)

    print("=== (d) real captures: indented `def test_` lines vs the AST index (305) ===")
    idx = json.loads((LANE / f"{T_RUN}/tests-index.json").read_text())["tests"]
    indexed = {(t["file"], t["name"]) for t in idx}
    cap = LANE / "corpus/evidence/round52/graders"
    pat = re.compile(r"^[ \t]+(?:async[ \t]+)?def[ \t]+(test_\w*)", re.M)
    dropped = []
    for f in sorted({t["file"] for t in idx}):
        src = (cap / f).read_text(encoding="utf-8", errors="replace")
        for m in pat.finditer(src):
            if (f, m.group(1)) not in indexed:
                line = src[:m.start()].count("\n") + 1
                dropped.append((f, m.group(1), line))
    print(f"   indented test defs not in index: {len(dropped)}")
    for d in dropped[:12]:
        print("     ", d)
    print("   indexed tests total:", len(idx), " indexed with class:", sum(1 for t in idx if t["class"]))

    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
