#!/usr/bin/env python3
"""R52-C1 classifier — whole-benchmark grader-vacuity triage for Terminal-Bench 2.0.

Seat C1ExecClassifier (kengaku round 52, wave 1).  Standalone module implementing the
FROZEN classification rules of `plans/round-52-claims.md` §C1, verbatim.

The four marker regexes, the `def test_` count, the class order and the first-match
branch order are copied from the frozen counter `plans/round52_c1_grader_audit.py`
(`classify()`); `selftest()` and `--parity` prove the mirror is exact.

Frozen rules (claims file §C1), applied to the primary grader
`tests/test_outputs.py` bytes (`environment/tests/test_outputs.py` when the task has
no `tests/` grader):

    presence marker  exists( | is_file( | is_dir( | os.path.exists | os.path.isfile
    content marker   read_text | read_bytes | open( | json.load
                     | re.(search|match|findall|finditer) | .decode( | .strip()
                     | .splitlines( | assert.*\bin\b
    behaviour marker subprocess | os.system | os.popen | Popen | socket | requests
                     | urllib | http.client | docker | bwrap | curl
    test count       number of `def test_` lines

    V1  presence and not content and not behaviour   (artefact-presence only)
    V2  behaviour                                     (the grader executes something)
    V3  content                                       (the grader reads and compares)
    V4  no marker class applies and <= 2 test functions (assertion-sparse)
    V0  otherwise

    V1 and V4 are the triage queue (CANDIDATES).

Usage:
    python3 classify.py --captures DIR [--out records.json] [--histogram]
    python3 classify.py --selftest
    python3 classify.py --captures DIR --parity      # diff against the frozen counter

Writes nothing outside the paths given on the command line.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# FROZEN feature regexes — copied verbatim from plans/round52_c1_grader_audit.py
# ---------------------------------------------------------------------------
PRESENCE = re.compile(r"\b(exists\(|is_file\(|is_dir\(|os\.path\.exists|os\.path\.isfile)")
CONTENT = re.compile(
    r"(read_text|read_bytes|open\(|json\.load|re\.(search|match|findall|finditer)"
    r"|\.decode\(|\.strip\(\)|\.splitlines\(|assert.*\bin\b)"
)
BEHAVIOUR = re.compile(
    r"(subprocess|os\.system|os\.popen|Popen|socket|requests|urllib|http\.client|docker|bwrap|curl )"
)
TESTFN = re.compile(r"^\s*def\s+test_", re.M)

CLASS_ORDER = ("V1", "V4", "V2", "V3", "V0")
RULE_ORDER = ("V1", "V2", "V3", "V4", "V0")

FROZEN_COUNTER = Path("plans/round52_c1_grader_audit.py")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def classify(body: str) -> tuple[str, dict]:
    """Frozen §C1 classifier — mirror of the counter's `classify()` (first match wins)."""
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


def primary_grader(files: list[str]) -> str | None:
    """Frozen primary-grader selection — mirror of the counter's `primary_grader()`."""
    to = [f for f in files if f.endswith("tests/test_outputs.py")]
    if not to:
        return None
    to.sort(key=lambda f: ("environment/" in f, f))
    return to[0]


def load_population(path: Path) -> dict:
    pop = json.loads(path.read_text())
    for key in ("tasks", "task_count", "capture_file_count"):
        if key not in pop:
            raise KeyError(f"population {path} lacks {key!r}")
    return pop


def resolve_capture(captures: Path, task: str, pg: str) -> Path | None:
    """Locate the captured bytes of `pg` under `captures`.

    Primary layout (the fetch seat's layout):  <captures>/<population-path>
    Flat fallback:                            <captures>/<task_tests_test_outputs.py>
    """
    cand = captures / pg
    if cand.is_file():
        return cand
    flat = captures / pg.replace("/", "_")
    if flat.is_file():
        return flat
    return None


def classify_population(pop: dict, captures: Path) -> list[dict]:
    """One JSON record per task of the frozen population."""
    records: list[dict] = []
    for task, files in sorted(pop["tasks"].items()):
        pg = primary_grader(files)
        rec: dict = {"task": task}
        if pg is None:
            rec.update(
                {
                    "grader": None,
                    "sha256": None,
                    "bytes": None,
                    "features": {"presence": None, "content": None, "behaviour": None,
                                 "test_functions": None},
                    "class": None,
                    "candidate": False,
                    "status": "undecidable",
                    "reason": "no test_outputs.py in the task's grader file list",
                }
            )
            records.append(rec)
            continue
        rec["grader"] = pg
        src = resolve_capture(captures, task, pg)
        if src is None:
            rec.update(
                {
                    "sha256": None,
                    "bytes": None,
                    "features": {"presence": None, "content": None, "behaviour": None,
                                 "test_functions": None},
                    "class": None,
                    "candidate": False,
                    "status": "undecidable",
                    "reason": f"capture absent: {pg}",
                }
            )
            records.append(rec)
            continue
        raw = src.read_bytes()
        body = raw.decode("utf-8", errors="replace")
        cls, feats = classify(body)
        rec.update(
            {
                "sha256": sha256_bytes(raw),
                "bytes": len(raw),
                "features": feats,
                "class": cls,
                "candidate": cls in ("V1", "V4"),
                "status": "classified",
                "reason": None,
            }
        )
        records.append(rec)
    return records


def histogram(records: list[dict]) -> dict:
    return {c: sum(1 for r in records if r.get("class") == c) for c in CLASS_ORDER}


def decide_notes(records: list[dict]) -> list[dict]:
    """Rule cases worth a human eye (the rules are decidable, but these are the edges)."""
    notes = []
    for r in records:
        if r["status"] != "classified":
            notes.append({"task": r["task"], "class": None, "note": r["reason"]})
            continue
        f = r["features"]
        if r["class"] == "V1":
            notes.append({
                "task": r["task"], "class": "V1",
                "note": "presence marker only: artefact-presence is satisfiable; "
                        "no content read, no behaviour executed",
            })
        elif r["class"] == "V4" and f["test_functions"] <= 2:
            notes.append({
                "task": r["task"], "class": "V4",
                "note": f"no marker class applies and only {f['test_functions']} test "
                        f"function(s): assertion-sparse relative to the task instruction",
            })
        elif r["class"] == "V0":
            notes.append({
                "task": r["task"], "class": "V0",
                "note": "no marker class applies but the grader carries "
                        f"{f['test_functions']} test functions: not assertion-sparse, "
                        "so V4 does not apply",
            })
    return notes


def emit_sums(captures: Path, out: Path) -> int:
    """sha256sum-format digest list of the captures dir (paths relative to it)."""
    lines = []
    for p in sorted(captures.rglob("*")):
        if p.is_file() and p.name != "fetch-manifest.json":
            lines.append(f"{sha256_bytes(p.read_bytes())}  {p.relative_to(captures)}")
    out.write_text("\n".join(lines) + "\n")
    return len(lines)


def parity(lane: Path, captures: Path) -> int:
    """Prove the mirror is exact: diff this module's classify() against the frozen
    counter's classify() over every captured byte stream."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("frozen_counter", lane / FROZEN_COUNTER)
    if spec is None or spec.loader is None:
        print("PARITY cannot load frozen counter")
        return 2
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    n = diff = 0
    for p in sorted(captures.rglob("*")):
        if not p.is_file() or p.name == "fetch-manifest.json":
            continue
        body = p.read_bytes().decode("utf-8", errors="replace")
        a, fa = mod.classify(body)
        b, fb = classify(body)
        n += 1
        if a != b or fa != fb:
            diff += 1
            print(f"PARITY MISMATCH {p}: frozen={a}/{fa} mine={b}/{fb}")
    print(f"PARITY files={n} mismatches={diff}")
    return 0 if diff == 0 else 1


def selftest(lane: Path) -> int:
    """The counter's own fixture battery, plus rule-order and edge checks."""
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
    # branch-order edges: presence+content -> V3; presence+behaviour -> V2;
    # behaviour+content -> V2; no markers + 3 test fns -> V0; no markers + 2 -> V4.
    edges = [
        ("def test_a():\n    assert os.path.exists('/x') and open('/x').read()\n", "V3"),
        ("import os, subprocess\ndef test_a():\n    subprocess.run(['ls'])\n    os.path.exists('/x')\n", "V2"),
        ("import subprocess\ndef test_a():\n    subprocess.run(['ls'])\n    assert open('/x').read()\n", "V2"),
        ("def test_a():\n    assert 1\ndef test_b():\n    assert 2\ndef test_c():\n    assert 3\n", "V0"),
        ("def test_a():\n    assert 1\ndef test_b():\n    assert 2\n", "V4"),
    ]
    for body, want in edges:
        got, _ = classify(body)
        if got != want:
            print(f"SELFTEST FAIL edge({want}) -> {got}")
            fails += 1
    # parity against the frozen counter on the fixture bodies
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("frozen_counter", lane / FROZEN_COUNTER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for body, want in cases + edges:
            a, fa = mod.classify(body)
            b, fb = classify(body)
            if a != b or fa != fb:
                print(f"SELFTEST FAIL parity {want}: frozen={a} mine={b}")
                fails += 1
    except Exception as exc:  # pragma: no cover - frozen counter absent
        print(f"SELFTEST parity skipped: {exc}")
    print(f"SELFTEST cases={len(cases) + len(edges)} failures={fails}")
    return 0 if fails == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--captures", default=None, help="directory holding the captured graders")
    ap.add_argument("--population", default=None, help="frozen population json")
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/kengaku-shokunin")
    ap.add_argument("--out", default=None, help="where to write the per-task records json")
    ap.add_argument("--histogram", action="store_true")
    ap.add_argument("--notes", default=None, help="where to write the rule-edge notes json")
    ap.add_argument("--emit-sums", default=None, help="write a sha256sums file for the captures dir")
    ap.add_argument("--parity", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    lane = Path(a.lane).resolve()
    if a.selftest:
        return selftest(lane)

    if a.parity:
        if not a.captures:
            print("--parity needs --captures")
            return 2
        return parity(lane, Path(a.captures).resolve())

    if not a.captures:
        print("--captures DIR is required")
        return 2
    captures = Path(a.captures).resolve()
    pop_path = Path(a.population) if a.population else lane / "plans" / "round52-tasks.json"
    pop = load_population(pop_path)
    records = classify_population(pop, captures)

    hist = histogram(records)
    classified = sum(1 for r in records if r["status"] == "classified")
    undecidable = [r for r in records if r["status"] != "classified"]
    candidates = sorted(r["task"] for r in records if r["candidate"])

    print(f"POPULATION tasks={pop['task_count']} records={len(records)} classified={classified}")
    print(f"CAPTURES dir={captures} capture_files_expected={pop['capture_file_count']}")
    print("CLASS " + " ".join(f"{c}={hist[c]}" for c in CLASS_ORDER))
    print(f"CANDIDATES total={len(candidates)}")
    for t in candidates:
        rec = next(r for r in records if r["task"] == t)
        print(f"  CANDIDATE {t} class={rec['class']} grader={rec['grader']} "
              f"tests={rec['features']['test_functions']}")
    print(f"UNDECIDABLE total={len(undecidable)}")
    for r in undecidable:
        print(f"  UNDECIDABLE {r['task']} reason={r['reason']}")

    payload = {
        "population": str(pop_path),
        "captures": str(captures),
        "pin": pop.get("pin"),
        "task_count": pop["task_count"],
        "records": records,
        "histogram": hist,
        "candidates": candidates,
        "undecidable": [r["task"] for r in undecidable],
    }
    out = Path(a.out) if a.out else Path("records.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"RECORDS {out}")

    if a.notes:
        n = decide_notes(records)
        Path(a.notes).parent.mkdir(parents=True, exist_ok=True)
        Path(a.notes).write_text(json.dumps(n, indent=1) + "\n")
        print(f"NOTES {a.notes} entries={len(n)}")
    if a.emit_sums:
        n = emit_sums(captures, Path(a.emit_sums))
        print(f"SUMS {a.emit_sums} files={n}")
    return 0 if not undecidable else 1


if __name__ == "__main__":
    sys.exit(main())
