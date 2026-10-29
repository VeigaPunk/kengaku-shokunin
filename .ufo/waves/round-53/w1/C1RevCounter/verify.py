#!/usr/bin/env python3
"""Consolidated defect verification against BOTH counter versions.

frozen  = plans/round53_c1_triage.py at commit a34838f (the version the frozen
          claims describe: "--selftest 22 cases").
A1      = the working-tree rewrite (mtime 2026-10-28 22:20) whose docstring calls
          itself "amendment A1".

Checks, each on a fixture whose PINS leg passes:
  V1  CONFIRM accepts a report path that is NOT under .ufo/waves/round-53/
  V2  CONFIRM accepts an ABSOLUTE report path outside the lane entirely
  V3  PRIOR-ART accepts a 'fetched' path that escapes corpus/evidence/round53/fetched/
  V4  PRIOR-ART accepts a quote that is NOT verbatim in the archive
  V5  PRIOR-ART quote word-count band is not enforced on the raw quote
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin").resolve()
SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
FROZEN = SCRATCH / "FROZEN_counter.py"
A1 = SCRATCH / "A1_counter.py"
sys.path.insert(0, str(LANE / "plans"))
import round53_c1_extract as EX  # noqa: E402


def sh(*a, cwd):
    subprocess.run(a, cwd=cwd, check=True, capture_output=True)


def build(root, mod):
    """Fixture that satisfies the FROZEN counter's PINS and FREEZE legs."""
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
           "            out[n.name] = 'P1' if 'read' not in ast.dump(n) and 'True' not in ast.dump(n) else 'P0'\n    return out\n")
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


def evidence(lane, mod, report_rel, pa_override=None, archive_text=None, quote=None):
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
          "sweep": [{"file": f"{mod.RUN_DIR}/fetched/s1.html", "file_sha256": mod.sha256_file(f / "s1.html")},
                    {"file": f"{mod.RUN_DIR}/fetched/s2.html", "file_sha256": mod.sha256_file(f / "s2.html")}]}
    if pa_override:
        pa.update(pa_override)
    if archive_text is not None:
        (f / "a.html").write_text(archive_text)
        pa["fetched_sha256"] = mod.sha256_file(f / "a.html")
    if quote is not None:
        pa["quote"] = quote
    (lane / f"{mod.RUN_DIR}/prior-art.json").write_text(json.dumps([pa]))
    return good, pa


def run_checks(tag, modpath):
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"m_{tag}", modpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print(f"\n########## {tag}  ({modpath}) ##########")
    root = Path(tempfile.mkdtemp(prefix=f"v-{tag}-", dir=str(SCRATCH)))

    # --- V1: report path not under .ufo/waves/round-53/ ---
    lane, cfg = build(root / "v1", mod)
    evidence(lane, mod, "corpus/ReaderSeat/report.md")
    rc, lines = mod.verdict(lane, cfg)
    conf = [l for l in lines if l.startswith("CONFIRM") or "REJECTED" in l]
    ok = any("new_confirmed=1" in l for l in conf)
    print(f"V1 report outside .ufo/waves/round-53/  -> {'ACCEPTED (defect)' if ok else 'rejected'}")
    for l in conf:
        print("     ", l)

    # --- V2: absolute report path outside the lane ---
    lane, cfg = build(root / "v2", mod)
    out = root / "v2" / "OUTSIDE" / "ReaderSeat" / "report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("reader report: t2 test_c reads Path('/y').is_file() presence only\n")
    evidence(lane, mod, str(out))
    rc, lines = mod.verdict(lane, cfg)
    conf = [l for l in lines if l.startswith("CONFIRM") or "REJECTED" in l]
    ok = any("new_confirmed=1" in l for l in conf)
    print(f"V2 ABSOLUTE report path outside the lane -> {'ACCEPTED (defect)' if ok else 'rejected'}")
    for l in conf:
        print("     ", l)

    # --- V3: fetched path escapes fetched/ ---
    lane, cfg = build(root / "v3", mod)
    secret = root / "v3" / "SECRET.txt"
    secret.write_text("the grader test_c merely checks the file exists and nothing more\n")
    rel = f"{mod.RUN_DIR}/fetched/" + "../" * 5 + "SECRET.txt"
    good, pa = evidence(lane, mod, ".ufo/waves/round-53/w2/ReaderSeat/report.md",
                        pa_override={"fetched": rel, "fetched_sha256": mod.sha256_file(secret)})
    rc, lines = mod.verdict(lane, cfg)
    pa_l = [l for l in lines if "PRIOR-ART" in l or "REJECTED" in l]
    accepted = any("rows=1" in l and "rejected=0" in l for l in pa_l)
    print(f"V3 fetched path escapes fetched/ -> {'ACCEPTED (defect)' if accepted else 'rejected'}")
    for l in pa_l:
        print("     ", l)
    print("      declared:", rel, "-> resolves to", (lane / rel).resolve())

    # --- V4: quote not verbatim ---
    lane, cfg = build(root / "v4", mod)
    arch = "the grader   test_c merely\nchecks the file exists and nothing more\n"
    good, pa = evidence(lane, mod, ".ufo/waves/round-53/w2/ReaderSeat/report.md",
                        archive_text=arch,
                        quote="the grader test_c merely checks the file exists and nothing more")
    rc, lines = mod.verdict(lane, cfg)
    pa_l = [l for l in lines if "PRIOR-ART" in l or "REJECTED" in l]
    accepted = any("rows=1" in l and "rejected=0" in l for l in pa_l)
    print(f"V4 quote not verbatim in archive -> {'ACCEPTED (defect)' if accepted else 'rejected'}")
    print("      archive:", repr(arch))
    print("      quote  :", repr(pa["quote"]))
    for l in pa_l:
        print("     ", l)

    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    run_checks("FROZEN", FROZEN)
    run_checks("A1", A1)
