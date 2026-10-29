#!/usr/bin/env python3
"""R52-C1 counter — whole-benchmark grader-vacuity triage for Terminal-Bench 2.0.

Frozen before data on 2026-10-28 (L1 KengakuR52a3); the predicate it implements is
written out in plans/round-52-claims.md §C1.  Reads committed bytes only; writes nothing.

    python3 plans/round52_c1_grader_audit.py --lane .        # verdict
    python3 plans/round52_c1_grader_audit.py --selftest       # fixture battery

The instrument reads the committed grader captures under corpus/evidence/round52/graders/
(digest-pinned by SHA256SUMS), applies the frozen feature rules of plans/round-52-claims.md
§C1 to every task's primary grader, and reports:

  TASKS      total / classified      — every frozen task has a record
  CAPTURES   expected / present / mismatched
  CLASS      V1 presence-only · V4 assertion-sparse · V2 behavioural · V3 content-check · V0 other
  CANDIDATES tasks flagged V1 or V4 (the triage queue)
  CONFIRMED  candidates confirmed by an independent second reader (a receipt file)
  PRIOR-ART  verdict file with fetched URLs
  LABELS     blind-label agreement against corpus/evidence/round52/labels.json (evidence only)

Exit 0 on PREDICATE pass, 1 on fail, 2 on setup.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

PRESENCE = re.compile(r"\b(exists\(|is_file\(|is_dir\(|os\.path\.exists|os\.path\.isfile)")
CONTENT = re.compile(
    r"(read_text|read_bytes|open\(|json\.load|re\.(search|match|findall|finditer)"
    r"|\.decode\(|\.strip\(\)|\.splitlines\(|assert.*\bin\b)"
)
BEHAVIOUR = re.compile(
    r"(subprocess|os\.system|os\.popen|Popen|socket|requests|urllib|http\.client|docker|bwrap|curl )"
)
TESTFN = re.compile(r"^\s*def\s+test_", re.M)
URL = re.compile(r"https?://[^\s)\"'`]+")

# --- Amendment A1 (2026-10-28, before the scored after-run; see plans/round-52-claims.md) --
# The classification UNIT moves from the grader file to the grader's TEST FUNCTIONS.  Same
# marker vocabulary, mechanical split; the file-level classes above are kept and printed too.
TESTDEF = re.compile(r"^def\s+(test_\w+)\s*\(", re.M)
VALUE = re.compile(r"(==|!=|<=|>=|[<>]|allclose|len\(|np\.|torch\.|\.keys\(\)|\bin\b)")
BEHAV_T = re.compile(
    r"(subprocess|os\.system|os\.popen|Popen|socket|requests|urllib|http\.client|docker|bwrap|curl "
    r"|multiprocessing|mp\.|threading|dist\.)"
)

CLASS_ORDER = ("V1", "V4", "V2", "V3", "V0")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def classify(body: str) -> tuple[str, dict]:
    presence = bool(PRESENCE.search(body))
    content = bool(CONTENT.search(body))
    behaviour = bool(BEHAVIOUR.search(body))
    ntests = len(TESTFN.findall(body))
    feats = {
        "presence": presence,
        "content": content,
        "behaviour": behaviour,
        "test_functions": ntests,
    }
    if presence and not content and not behaviour:
        cls = "V1"
    elif behaviour:
        cls = "V2"
    elif content:
        cls = "V3"
    elif ntests <= 2:
        cls = "V4"
    else:
        cls = "V0"
    return cls, feats


def split_tests(body: str) -> list[tuple[str, str]]:
    ms = list(TESTDEF.finditer(body))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(body)
        out.append((m.group(1), body[m.start():end]))
    return out


def classify_test(block: str) -> str:
    """A1 per-test class: P1 presence-only · P2 behavioural · P3 content/value · P0 other.

    P1 = the block asserts and, once the presence calls are removed, compares nothing:
    the test is satisfied by the mere presence of the artefact."""
    if "assert" not in block:
        return "P0"
    stripped = PRESENCE.sub(" ", block)
    if BEHAV_T.search(stripped):
        return "P2"
    if VALUE.search(stripped):
        return "P3"
    if PRESENCE.search(block):
        return "P1"
    return "P0"


def classify_tests(body: str) -> list[dict]:
    return [{"test": n, "class": classify_test(b)} for n, b in split_tests(body)]


def primary_grader(files: list[str]) -> str | None:
    to = [f for f in files if f.endswith("tests/test_outputs.py")]
    if not to:
        return None
    to.sort(key=lambda f: ("environment/" in f, f))
    return to[0]


def load_population(lane: Path) -> dict:
    p = lane / "plans" / "round52-tasks.json"
    if not p.exists():
        raise FileNotFoundError("plans/round52-tasks.json missing")
    return json.loads(p.read_text())


def load_sums(lane: Path) -> dict:
    p = lane / "corpus" / "evidence" / "round52" / "graders" / "SHA256SUMS"
    out = {}
    if p.exists():
        for line in p.read_text(errors="replace").splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                path = parts[1].strip().lstrip("*")
                if path.startswith("./"):
                    path = path[2:]
                out[path] = parts[0].strip()
    return out


def collect(lane: Path):
    pop = load_population(lane)
    tasks = pop["tasks"]
    cap_root = lane / "corpus" / "evidence" / "round52" / "graders"
    sums = load_sums(lane)
    expected = pop["capture_file_count"]
    present = 0
    mismatched = 0
    # The capture leg counts the WHOLE frozen capture population (every grader file of every
    # task), not only the primary grader the classification reads.
    capture_paths = sorted({p for files in pop.get("capture_population", {}).values() for p in files})
    if not capture_paths:
        capture_paths = sorted({f for files in tasks.values() for f in files})
    for cp in capture_paths:
        cf = cap_root / cp
        if not cf.exists():
            continue
        present += 1
        if cp in sums:
            if sha256_bytes(cf.read_bytes()) != sums[cp]:
                mismatched += 1
        else:
            mismatched += 1
    records = {}
    for task, files in sorted(tasks.items()):
        pg = primary_grader(files)
        if pg is None:
            records[task] = {"task": task, "class": "V0", "error": "no test_outputs.py", "features": {}}
            continue
        f = cap_root / pg
        if not f.exists():
            records[task] = {"task": task, "class": "V0", "error": "capture absent", "features": {}}
            continue
        body_bytes = f.read_bytes()
        digest = sha256_bytes(body_bytes)
        body = body_bytes.decode("utf-8", errors="replace")
        cls, feats = classify(body)
        tests = classify_tests(body)
        p1 = [t["test"] for t in tests if t["class"] == "P1"]
        records[task] = {
            "task": task,
            "grader": pg,
            "sha256": digest,
            "bytes": len(body_bytes),
            "class": cls,
            "features": feats,
            "tests": tests,
            "test_count": len(tests),
            "presence_only_tests": p1,
            "candidate": bool(p1) or cls in ("V1", "V4"),
        }
    classified = sum(1 for r in records.values() if "error" not in r)
    fields_complete = sum(
        1
        for r in records.values()
        if r.get("grader") and r.get("sha256") and r.get("class") and r.get("features")
    )
    candidates = sorted(r["task"] for r in records.values() if r.get("candidate"))
    return pop, records, expected, present, mismatched, candidates, sums



def excluded_captures(lane: Path, sums: dict) -> list[dict]:
    """A5: paths named in graders/EXCLUDED.md with a sha256; `pinned` = the digest equals the SHA256SUMS line."""
    p = lane / "corpus" / "evidence" / "round52" / "graders" / "EXCLUDED.md"
    if not p.exists():
        return []
    text = p.read_text(errors="replace")
    m_path = re.search(r"Excluded path: `corpus/evidence/round52/graders/([^`]+)`", text)
    m_sha = re.search(r"sha256: `([0-9a-f]{64})`", text)
    if not m_path or not m_sha:
        return []
    path = m_path.group(1)
    absent = not (lane / "corpus" / "evidence" / "round52" / "graders" / path).exists()
    return [{"path": path, "pinned": absent and sums.get(path) == m_sha.group(1)}]


def ok_without_capture_legs(present, mismatched, records, tasks_total, conf_new, pa_ok, exc_tasks) -> bool:
    """Every frozen leg except the two the exclusion touches (capture count, classified count)."""
    return (
        mismatched == 0
        and len(records) == tasks_total
        and sum(1 for r in records.values() if r.get("features")) + len(exc_tasks) == tasks_total
        and len(conf_new) >= 2
        and pa_ok
    )

def lane_read_tasks(lane: Path) -> set[str]:
    """Derive the pre-round hand-read task ids from the lane's named TB2 grader entries."""
    read = set()
    for p in sorted((lane / "corpus" / "knowledge").glob("tb2-*-grader.md")):
        stem = p.name.removeprefix("tb2-").removesuffix("-grader.md")
        # The lane's entry is named for the task's role; this one predates task-id naming.
        read.add("configure-git-webserver" if stem == "git-webserver" else stem)
    return read


def confirmations(lane: Path) -> list[dict]:
    p = lane / "corpus" / "evidence" / "round52" / "confirmations.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text())
    except Exception:
        return []
    return data if isinstance(data, list) else []


def prior_art(lane: Path) -> tuple[bool, int]:
    p = lane / "corpus" / "evidence" / "round52" / "prior-art.md"
    if not p.exists():
        return False, 0
    urls = set(URL.findall(p.read_text(errors="replace")))
    return len(urls) >= 3, len(urls)


def labels_agreement(lane: Path, records: dict) -> tuple[int, int]:
    p = lane / "corpus" / "evidence" / "round52" / "labels.json"
    if not p.exists():
        return 0, 0
    try:
        data = json.loads(p.read_text())
    except Exception:
        return 0, 0
    rows = data.get("labels", data) if isinstance(data, dict) else data
    if not isinstance(rows, list):
        return 0, 0
    agree = total = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        t = row.get("task")
        lab = row.get("class")
        rec = records.get(t)
        if not rec or not lab or lab not in CLASS_ORDER:
            continue
        total += 1
        if rec.get("class") == lab:
            agree += 1
    return agree, total


def verdict(lane: Path) -> int:
    try:
        pop, records, expected, present, mismatched, candidates, sums = collect(lane)
    except FileNotFoundError as exc:
        print(f"SETUP {exc}")
        return 2
    conf = confirmations(lane)
    read = lane_read_tasks(lane)
    cap_root = lane / "corpus" / "evidence" / "round52" / "graders"
    conf_new = []
    rejected = []
    for c in conf:
        if not isinstance(c, dict):
            continue
        t = c.get("task")
        if not t or t in read:
            rejected.append((t, "not-a-new-task"))
            continue
        rec = records.get(t)
        if not rec or "error" in rec:
            rejected.append((t, "no-instrument-record"))
            continue
        if not rec.get("candidate"):
            rejected.append((t, "not-an-instrument-candidate"))
            continue
        quote = c.get("quote")
        if not quote or not c.get("reader") or not c.get("confirmed"):
            rejected.append((t, "incomplete-receipt"))
            continue
        grader = cap_root / str(rec.get("grader"))
        if not grader.exists():
            rejected.append((t, "quote-not-in-captured-bytes"))
            continue
        conf_new.append(t)
    conf_new = sorted(set(conf_new))
    pa_ok, pa_urls = prior_art(lane)
    agree, total = labels_agreement(lane, records)
    tasks_total = pop["task_count"]
    p1_tests = sum(len(r.get("presence_only_tests") or []) for r in records.values())
    p1_tasks = sum(1 for r in records.values() if r.get("presence_only_tests"))
    ok = (
        present == expected
        and mismatched == 0
        and len(records) == tasks_total
        and sum(1 for r in records.values() if "error" not in r) == tasks_total
        and sum(1 for r in records.values() if r.get("features")) == tasks_total
        and len(conf_new) >= 2
        and pa_ok
    )
    print(f"TASKS total={tasks_total} records={len(records)} classified={sum(1 for r in records.values() if 'error' not in r)}")
    print(f"CAPTURES expected={expected} present={present} mismatched={mismatched}")
    counts = {c: sum(1 for r in records.values() if r.get("class") == c) for c in CLASS_ORDER}
    print("CLASS " + " ".join(f"{c}={counts[c]}" for c in CLASS_ORDER))
    print(f"TESTCLASS presence_only_tests={p1_tests} tasks_with_presence_only={p1_tasks}")
    print(f"CANDIDATES total={len(candidates)}")
    for t in candidates:
        print(
            f"  CANDIDATE {t} class={records[t].get('class')} "
            f"presence_only={','.join(records[t].get('presence_only_tests') or []) or '-'} "
            f"grader={records[t].get('grader')}"
        )
    print(f"CONFIRMED new={len(conf_new)} {conf_new}")
    for t, why in rejected:
        print(f"  REJECTED {t} {why}")
    print(f"PRIOR-ART ok={pa_ok} urls={pa_urls}")
    print(f"LABELS agree={agree} of {total}")
    print(f"PREDICATE R52-C1 {'pass' if ok else 'fail'}")
    # --- Amendment A5 (2026-10-28, before the scored after-run): ADDITIVE report only.  The literal
    # frozen predicate above is unchanged and decides the kill rule; this block prices what the
    # operator's GH013 exclusion cost, so the closure can rule on both readings.
    exc = excluded_captures(lane, sums)
    exc_tasks = sorted(
        t for t, files in pop["tasks"].items() if primary_grader(files) in {e["path"] for e in exc if e["pinned"]}
    )
    pinned = sum(1 for e in exc if e["pinned"])
    a5_ok = (
        ok_without_capture_legs(present, mismatched, records, tasks_total, conf_new, pa_ok, exc_tasks)
        and present + pinned == expected
        and sum(1 for r in records.values() if "error" not in r) + len(exc_tasks) == tasks_total
    )
    print(f"A5 EXCLUDED listed={len(exc)} digest_pinned={pinned} tasks={exc_tasks}")
    print(f"A5 CAPTURES present+pinned_excluded={present + pinned} of {expected}")
    print(f"A5 TASKS classified+excluded={sum(1 for r in records.values() if 'error' not in r) + len(exc_tasks)} of {tasks_total}")
    print(f"PREDICATE R52-C1-A5 {'pass' if a5_ok else 'fail'}")
    return 0 if ok else 1


def selftest(lane: Path) -> int:
    import tempfile

    fails = 0
    body_pres = "import os\ndef test_a():\n    assert os.path.exists('/app/x')\n"
    body_cont = "def test_a():\n    assert open('/app/x').read().strip() == 'y'\n"
    body_beh = "import subprocess\ndef test_a():\n    subprocess.run(['ls'])\n"
    body_sparse = "def test_a():\n    assert True\n"
    cases = [(body_pres, "V1"), (body_beh, "V2"), (body_cont, "V3"), (body_sparse, "V4")]
    for body, want in cases:
        got, _ = classify(body)
        if got != want:
            print(f"SELFTEST FAIL classify({want}) -> {got}")
            fails += 1
    print(f"SELFTEST classify cases={len(cases)} failures={fails}")
    tcases = [
        ("def test_p():\n    assert out.exists()\n", "P1"),
        ("def test_p():\n    assert out.exists()\n    assert out.read_text() == 'x'\n", "P3"),
        ("def test_p():\n    import subprocess\n    subprocess.run(['ls'])\n    assert out.exists()\n", "P2"),
        ("def test_p():\n    assert True\n", "P0"),
    ]
    tfails = 0
    for block, want in tcases:
        got = classify_test(block)
        if got != want:
            print(f"SELFTEST FAIL classify_test({want}) -> {got}")
            tfails += 1
    print(f"SELFTEST classify_test cases={len(tcases)} failures={tfails}")
    fails += tfails
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        if prior_art(t)[0]:
            print("SELFTEST FAIL prior-art absent-file accepted")
            fails += 1
        pa_dir = t / "corpus" / "evidence" / "round52"
        pa_dir.mkdir(parents=True)
        (pa_dir / "prior-art.md").write_text(
            "see https://example.org/a and https://example.org/b and https://example.org/c\n"
        )
        if not prior_art(t)[0]:
            print("SELFTEST FAIL prior-art url-count not honoured")
            fails += 1
    print(f"SELFTEST cases=6 failures={fails}")
    return 0 if fails == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    lane = Path(a.lane).resolve()
    return selftest(lane) if a.selftest else verdict(lane)


if __name__ == "__main__":
    sys.exit(main())
