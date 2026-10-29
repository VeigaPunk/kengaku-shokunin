#!/usr/bin/env python3
"""Final two checks on the FROZEN counter:
  V9  ordering proof: classifier committed AFTER the labels, freeze file first
  V10 never-read: literal vs regex at BASE_TIP (already measured, re-assert)
  V11 the claims file's abbreviated sha vs the counter's full pin
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
FROZEN = SCRATCH / "FROZEN_counter.py"
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin").resolve()
sys.path.insert(0, str(SCRATCH))
sys.path.insert(0, str(LANE / "plans"))
import round53_c1_extract as EX  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("mfroz3", FROZEN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
T_RUN = "corpus/evidence/round53"


def sh(*a, cwd):
    subprocess.run(a, cwd=cwd, check=True, capture_output=True)


def build(root, classifier_last=False):
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
      "def classify_tests(body):\n    return [{'test': 'test_a', 'class': 'P0'}, {'test': 'test_b', 'class': 'P0'}, {'test': 'test_c', 'class': 'P0'}]\n")
    clf = ("import ast\n\ndef classify_source(src):\n    out = {}\n    for n in ast.parse(src).body:\n"
           "        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):\n"
           "           out[n.name] = 'P1' if 'read' not in ast.dump(n) and 'True' not in ast.dump(n) else 'P0'\n    return out\n")
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
    if classifier_last:
        # commit 1: the freeze file only, recording a sha of a classifier that does NOT exist yet
        w("plans/round53-c1-freeze.json", json.dumps({"classifier_sha256": "0" * 64, "author_seats": ["AuthorSeat"]}))
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze-first", cwd=lane)
        # commit 2: the labels
        w(f"{T_RUN}/oracle-labels.json", labtxt)
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "labels", cwd=lane)
        # commit 3: the classifier lands AFTER the labels
        w("plans/round53_c1_classify.py", clf)
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "classifier-last", cwd=lane)
        # commit 4: the freeze file updated to the real sha (classifier still "before" nothing)
        w("plans/round53-c1-freeze.json", json.dumps({"classifier_sha256": mod.sha256_file(lane / "plans/round53_c1_classify.py"),
                                                      "author_seats": ["AuthorSeat"]}))
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze-updated", cwd=lane)
    else:
        w("plans/round53_c1_classify.py", clf)
        w("plans/round53-c1-freeze.json", json.dumps({"classifier_sha256": mod.sha256_file(lane / "plans/round53_c1_classify.py"),
                                                      "author_seats": ["AuthorSeat"]}))
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "freeze", cwd=lane)
        w(f"{T_RUN}/oracle-labels.json", labtxt)
        sh("git", "-C", str(lane), "add", "-A", cwd=lane)
        sh("git", "-C", str(lane), "commit", "-q", "-m", "labels", cwd=lane)
    return lane, cfg


def main():
    root = Path(tempfile.mkdtemp(prefix="v9-", dir=str(SCRATCH)))
    print("=== V9: classifier committed AFTER the labels (freeze file first, then updated) ===")
    lane, cfg = build(root / "v9", classifier_last=True)
    rc, lines = mod.verdict(lane, cfg)
    print("   rc=", rc)
    for l in lines:
        if l.startswith(("FREEZE", "ORACLE", "PREDICATE")):
            print("     ", l)
    print("   git log --oneline:")
    for l in subprocess.run(["git", "-C", str(lane), "log", "--oneline"], capture_output=True, text=True).stdout.splitlines():
        print("      ", l)
    print("   => the classifier's FIRST commit is AFTER the labels' commit; FREEZE still says order=freeze-before-labels")

    print()
    print("=== V10: never-read, literal vs regex at BASE_TIP ===")
    r52_conf, texts = mod.never_read_blocklist(LANE, mod.CFG)
    pop = json.loads((LANE / "plans/round52-tasks.json").read_text())
    tasks = sorted(pop["tasks"])
    lit = {t for t in tasks if any(t in x for x in texts.values())}
    rgx = {t for t in tasks if mod.seen_before(t, texts)}
    print(f"   texts scanned: {len(texts)}  tasks: {len(tasks)}")
    print(f"   literal-seen: {len(lit)}   regex-seen: {len(rgx)}   delta: {sorted(lit ^ rgx)}")

    print()
    print("=== V11: the claims file's abbreviated sha vs the counter's full pin ===")
    claims = (LANE / "plans/round-53-claims.md").read_text()
    for frag in ["0230b68c", "96b47248", "579d567f", "7897c7330", "3269e74e", "dacf199dda"]:
        print(f"   claims contain {frag!r}: {frag in claims}")
    print("   counter pins:")
    print("     POP_SHA       ", mod.POP_SHA)
    print("     PIN_TREE_SHA  ", mod.PIN_TREE_SHA)
    print("     TESTS_INDEX_SHA", mod.TESTS_INDEX_SHA)
    print("     EXCLUDED_BLOB ", mod.EXCLUDED_BLOB)
    print("   claims' tail for tests-index: '579d567f…7897c7330'")
    print("   counter's tail for tests-index:", mod.TESTS_INDEX_SHA[-10:], " -> claims' tail is NOT a suffix:",
          mod.TESTS_INDEX_SHA.endswith("7897c7330"))
    print("   counter's tail for excluded blob:", mod.EXCLUDED_BLOB[-10:], "claims' tail 'dacf199dda' matches:",
          mod.EXCLUDED_BLOB.endswith("dacf199dda"))

    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
