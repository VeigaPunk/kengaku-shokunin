#!/usr/bin/env python3
"""Grader-class census survey (kengaku round 62, C1).

The planned-round-62 precondition (SCORECARD, planned round 62): an eighteenth
grader may only be claimed after a SURVEY PASS over the population classifies
the grader mechanisms already committed. This instrument is that survey,
mechanized: it reads the committed round-52 capture population and the
committed round-62 pin-tree capture, verifies every capture byte against the
pinned SHA256SUMS, classifies every committed ``test_outputs.py`` grader over
a frozen detector table, and prices the class census plus the executed-
coverage cross-tab the eighteenth-grader gate reads.

Population of record (all committed bytes, read-only):
  corpus/evidence/round52/graders/SHA256SUMS      184 pinned capture rows
  corpus/evidence/round52/graders/EXCLUDED.md     the one pinned-but-absent capture
  corpus/evidence/round52/graders/all_tasks.lst   the 89-task roster (the pin's dirs)
  corpus/evidence/round52/graders/executed17.lst  the 17 executed tasks
  corpus/evidence/round62/tb2-tree-2fd12b88.json  the live-opened pin tree capture (S226)
  corpus/evidence/round52/graders/**              the capture bytes themselves

Detector table (frozen here, before any scored run): a grader is a multi-label
member of every class whose regex occurs in its decoded text. The classes are
named by what they literally match, never by intent. Two expectations are
frozen for the real population and parameterized for the toys: the roster
holds 89 tasks (the pin tree's dir count), and the ``signal-delivery`` class
holds exactly one member, ``cancel-async-tasks`` (the round-59/61 surveys'
prose negative, re-derived mechanically here).

  CLASS-CENSUS roster=<n> tree-dirs=<n> sha256sums-rows=<n> captures-committed=<n>
          captures-unpinned=<n> sha-mismatch=<n> absent-pinned=<n>
          graders-classified=<n> unclassified=<n> classes=<k>
  POPULATION roster==tree=<bool> excluded-sha-pinned=<bool>
  CLASS <name> count=<n> members=<comma-joined or ->
  UNCLASSIFIED count=<n> members=<comma-joined or ->
  SENTINEL signal-delivery count=<n> member=<name or ->
  EXECUTED-COVERAGE executed=<n> classified=<n> classes-covered=<k>
          classes-uncovered=<names or ->
  DETERMINISM second-run-identical=<True|False>
  PREDICATE R62-C1 pass|fail
  CLASS-SURVEY-EXIT=<0|1|2>

Exit codes: 0 pass (every invariant holds) | 1 fail (the invariant lines are
printed: ``INVARIANT-FAIL <name>``) | 2 setup (a population input is missing
or unparsable -- never a vacuous pass).

Run as:
  python3 plans/round62_c1_class_survey.py --lane .            # census (read-only)
  python3 plans/round62_c1_class_survey.py --lane . --receipt PATH
  python3 plans/round62_c1_class_survey.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import tempfile

# ---------------------------------------------------------------- population

GRADERS_DIR = "corpus/evidence/round52/graders"
TREE_CAPTURE = "corpus/evidence/round62/tb2-tree-2fd12b88.json"
ROSTER_NAME = "all_tasks.lst"
EXECUTED_NAME = "executed17.lst"
SHA_NAME = "SHA256SUMS"
EXCLUDED_NAME = "EXCLUDED.md"
METADATA = {
    ROSTER_NAME,
    EXECUTED_NAME,
    "missing.lst",
    "unexec.lst",
    "unexec72.lst",
    SHA_NAME,
    EXCLUDED_NAME,
}
EXCLUDED_SHA_RE = re.compile(r"sha256:\s*`([0-9a-f]{64})`")
EXCLUDED_PATH_RE = re.compile(r"Excluded path:\s*`([^`]+)`")
SHA_ROW_RE = re.compile(r"^([0-9a-f]{64})  \./(.+)$")

# ------------------------------------------------------------ detector table

DETECTORS = [
    ("signal-delivery", r"\bsend_signal\s*\("),
    ("subprocess-exec", r"\bsubprocess\.(run|Popen|check_output|check_call|call)\s*\("),
    ("shell-exec", r"\bos\.popen\s*\(|\bos\.system\s*\(|\bcommands\.getoutput\s*\("),
    ("candidate-import", r"(?m)^\s*import\s+(attack|solution)\b|sys\.path\.append\s*\("),
    ("file-artifact", r"\.exists\(\)|\.read_text\(|\.read_bytes\(|\.is_file\(\)|\.is_dir\(\)|\bopen\s*\("),
    ("stdout-inspection", r"\.stdout\b"),
    ("numeric-band", r"pytest\.approx|math\.isclose|np\.allclose|\babs\([^()]*\)\s*[<>]"),
    ("crypto-credential", r"\bhashlib\b|\bsha1\b|\bsha256\b|\bmd5\b|\bopenssl\b|\bgpg\b|\bhmac\b"),
    ("network-service", r"\bsocket\.|\brequests\.(get|post)\b|\burllib\b|http\.client|\burlopen\b|localhost:[0-9]|127\.0\.0\.1"),
    ("timing-wall", r"time\.monotonic|time\.perf_counter|\belapsed\b|time\.time\("),
    ("filesystem-metadata", r"os\.stat\b|st_mode|os\.chmod|os\.geteuid|\bis_symlink|os\.path\.getsize|os\.path\.getmtime"),
    ("process-environment", r"os\.environ|/proc/"),
    ("git-plumbing", "[\"']git[\"']"),
    ("db-state", r"\bsqlite3\b|\bpostgres\b|\bmysql\b"),
    ("serialization-schema", r"json\.loads?\(|yaml\.safe_load|\btomllib\b|xml\.etree"),
    ("container-image", r"\bdocker\b|\bpodman\b"),
]
COMPILED = [(name, re.compile(pattern)) for name, pattern in DETECTORS]
CLASS_NAMES = [name for name, _ in DETECTORS]

# Frozen population expectations (main run); the selftest parameterizes both.
ROSTER_SIZE_EXPECTED = 89
SENTINEL_MEMBER_EXPECTED = "cancel-async-tasks"


def classify(text: str) -> list[str]:
    """Class names whose detector regex occurs in the decoded grader text."""
    return [name for name, pattern in COMPILED if pattern.search(text)]


# ------------------------------------------------------------------- engine

def read_lines(path: pathlib.Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def census_core(
    lane: pathlib.Path,
    roster_size_expected: int | None,
    sentinel_member_expected: str | None,
) -> tuple[list[str], list[str]]:
    """One census pass. Returns (lines, failed-invariant names). Never recurses."""
    graders = lane / GRADERS_DIR
    tree_path = lane / TREE_CAPTURE
    roster_path = graders / ROSTER_NAME
    executed_path = graders / EXECUTED_NAME
    sha_path = graders / SHA_NAME
    excluded_path = graders / EXCLUDED_NAME
    required = [roster_path, executed_path, sha_path, excluded_path]
    missing = [str(p) for p in required if not p.is_file()]
    if missing or not graders.is_dir() or not tree_path.is_file():
        missing.append("" if graders.is_dir() else str(graders))
        missing.append("" if tree_path.is_file() else str(tree_path))
        return (["SETUP missing-inputs: " + " ".join(m for m in missing if m),
                 "PREDICATE R62-C1 fail", "CLASS-SURVEY-EXIT=2"], ["SETUP"])

    roster = sorted(read_lines(roster_path))
    executed = sorted(read_lines(executed_path))
    sha_rows: dict[str, str] = {}
    for raw in read_lines(sha_path):
        match = SHA_ROW_RE.match(raw)
        if match is None:
            return (["SETUP unparsable-SHA256SUMS-row: " + raw,
                     "PREDICATE R62-C1 fail", "CLASS-SURVEY-EXIT=2"], ["SETUP"])
        sha_rows[match.group(2)] = match.group(1)
    excluded_md = excluded_path.read_text(encoding="utf-8")
    excluded_sha = EXCLUDED_SHA_RE.search(excluded_md)
    excluded_row = EXCLUDED_PATH_RE.search(excluded_md)
    if excluded_sha is None or excluded_row is None:
        return (["SETUP unparsable-EXCLUDED.md", "PREDICATE R62-C1 fail",
                 "CLASS-SURVEY-EXIT=2"], ["SETUP"])
    # EXCLUDED.md names the path repo-rooted; the SHA256SUMS row carries the
    # same path after the population prefix and the ./ marker.
    excluded_rel = excluded_row.group(1).split("round52/graders/", 1)[-1]

    tree = json.loads(tree_path.read_text(encoding="utf-8"))
    tree_dirs = sorted(entry["path"] for entry in tree["tree"] if entry.get("type") == "tree")

    # --- capture bytes: every file under graders/ outside the metadata set.
    all_files = sorted(p for p in graders.rglob("*") if p.is_file() and p.name not in METADATA)
    sha_mismatch = 0
    unpinned: list[str] = []
    for path in all_files:
        rel = path.relative_to(graders).as_posix()
        want = sha_rows.get(rel)
        if want is None:
            unpinned.append(rel)
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != want:
            sha_mismatch += 1
    pinned_paths = set(sha_rows)
    committed_rels = {p.relative_to(graders).as_posix() for p in all_files}
    absent_pinned = sorted(pinned_paths - committed_rels)

    # --- classify every committed grader.
    grader_files = sorted(p for p in all_files if p.name == "test_outputs.py")
    members: dict[str, list[str]] = {name: [] for name in CLASS_NAMES}
    unclassified_set: set[str] = set()
    for path in grader_files:
        task = path.relative_to(graders).as_posix().split("/", 1)[0]
        text = path.read_bytes().decode("utf-8", errors="replace")
        hits = classify(text)
        for name in hits:
            members[name].append(task)
        if not hits:
            unclassified_set.add(task)
    for name in CLASS_NAMES:
        members[name] = sorted(set(members[name]))
    unclassified = sorted(unclassified_set)

    covered = sorted(name for name in CLASS_NAMES if set(members[name]) & set(executed))
    uncovered = [name for name in CLASS_NAMES if name not in covered]

    lines: list[str] = []
    lines.append(
        "CLASS-CENSUS roster=%d tree-dirs=%d sha256sums-rows=%d captures-committed=%d "
        "captures-unpinned=%d sha-mismatch=%d absent-pinned=%d graders-classified=%d "
        "unclassified=%d classes=%d"
        % (len(roster), len(tree_dirs), len(sha_rows), len(all_files), len(unpinned),
           sha_mismatch, len(absent_pinned), len(grader_files), len(unclassified),
           len(CLASS_NAMES))
    )
    lines.append(
        "POPULATION roster==tree=%s excluded-sha-pinned=%s"
        % (str(roster == tree_dirs), str(excluded_sha.group(1) in set(sha_rows.values())))
    )
    for name in CLASS_NAMES:
        hits = members[name]
        lines.append("CLASS %s count=%d members=%s" % (name, len(hits), ",".join(hits) or "-"))
    lines.append("UNCLASSIFIED count=%d members=%s"
                 % (len(unclassified), ",".join(unclassified) or "-"))
    sentinel_count = len(members["signal-delivery"])
    sentinel_member = members["signal-delivery"][0] if sentinel_count == 1 else "-"
    lines.append("SENTINEL signal-delivery count=%d member=%s" % (sentinel_count, sentinel_member))
    lines.append(
        "EXECUTED-COVERAGE executed=%d classified=%d classes-covered=%d classes-uncovered=%s"
        % (len(executed),
           sum(1 for t in executed if any(t in members[n] for n in CLASS_NAMES)),
           len(covered), ",".join(uncovered) or "-")
    )

    invariants = [
        ("sha-mismatch", sha_mismatch == 0),
        ("captures-unpinned", len(unpinned) == 0),
        ("absent-pinned-is-excluded-only", absent_pinned == [excluded_rel]),
        ("excluded-absent", excluded_rel not in committed_rels),
        ("roster==tree", roster == tree_dirs),
        ("every-roster-task-has-grader-dir", all((graders / t).is_dir() for t in roster)),
        ("executed-subset-roster", set(executed) <= set(roster)),
        ("every-executed-grader-classified",
         all(any(t in members[n] for n in CLASS_NAMES) for t in executed)),
    ]
    if roster_size_expected is not None:
        invariants.append(("roster-count-%d" % roster_size_expected,
                           len(roster) == roster_size_expected))
    if sentinel_member_expected is not None:
        invariants.append(("sentinel-signal-unique-%s" % sentinel_member_expected,
                           sentinel_count == 1 and sentinel_member == sentinel_member_expected))
    failed = [name for name, ok in invariants if not ok]
    for name in failed:
        lines.append("INVARIANT-FAIL %s" % name)
    return lines, failed


def run_census(
    lane: pathlib.Path,
    roster_size_expected: int | None = ROSTER_SIZE_EXPECTED,
    sentinel_member_expected: str | None = SENTINEL_MEMBER_EXPECTED,
) -> tuple[list[str], int]:
    """Census + determinism leg (the core re-runs once; outputs must agree)."""
    lines1, failed1 = census_core(lane, roster_size_expected, sentinel_member_expected)
    if failed1 == ["SETUP"]:
        return lines1, 2
    lines2, failed2 = census_core(lane, roster_size_expected, sentinel_member_expected)
    identical = (lines1 == lines2 and failed1 == failed2)
    lines = list(lines1)
    lines.append("DETERMINISM second-run-identical=%s" % identical)
    verdict = "pass" if not failed1 and identical else "fail"
    code = 0 if verdict == "pass" else 1
    lines.append("PREDICATE R62-C1 %s" % verdict)
    lines.append("CLASS-SURVEY-EXIT=%d" % code)
    return lines, code


# ----------------------------------------------------------------- selftest

def selftest() -> int:
    """Toy battery: detector truth, sha-drift red, roster-drift red. rc/want printed."""
    results: list[tuple[str, int, int]] = []
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        pop = root / GRADERS_DIR
        toy_signal = pop / "toy-signal" / "tests"
        toy_pure = pop / "toy-pure" / "tests"
        toy_blank = pop / "toy-blank" / "tests"
        for d in (toy_signal, toy_pure, toy_blank):
            d.mkdir(parents=True)
        (toy_signal / "test_outputs.py").write_text(
            "import subprocess, signal\n"
            "def test_x():\n"
            "    p = subprocess.Popen(['true'])\n"
            "    p.send_signal(signal.SIGINT)\n",
            encoding="utf-8")
        (toy_pure / "test_outputs.py").write_text(
            "import json\n"
            "def test_y():\n"
            "    data = json.load(open('/app/result.json'))\n"
            "    assert abs(data['v'] - 1.0) < 0.01\n",
            encoding="utf-8")
        (toy_blank / "test_outputs.py").write_text("def test_z():\n    pass\n", encoding="utf-8")
        (pop / EXECUTED_NAME).write_text("toy-signal\n", encoding="utf-8")
        (pop / ROSTER_NAME).write_text("toy-signal\ntoy-pure\ntoy-blank\n", encoding="utf-8")
        for meta in ("missing.lst", "unexec.lst", "unexec72.lst"):
            (pop / meta).write_text("", encoding="utf-8")

        excluded_rel = "toy-excluded/tests/test_outputs.py"
        rows = []
        for p in sorted(pop.rglob("test_outputs.py")):
            rel = p.relative_to(pop).as_posix()
            rows.append("%s  ./%s" % (hashlib.sha256(p.read_bytes()).hexdigest(), rel))
        # the toy's one pinned-but-absent capture (the EXCLUDED.md analogue)
        rows.append("%s  ./%s" % ("1" * 64, excluded_rel))
        (pop / SHA_NAME).write_text("\n".join(rows) + "\n", encoding="utf-8")
        (pop / EXCLUDED_NAME).write_text(
            "- Excluded path: `corpus/evidence/round52/graders/%s`\n"
            "- sha256: `%s`\n" % (excluded_rel, "1" * 64), encoding="utf-8")
        tree = {"tree": [{"path": t, "type": "tree"} for t in
                         ["toy-signal", "toy-pure", "toy-blank"]], "truncated": False}
        tree_path = root / TREE_CAPTURE
        tree_path.parent.mkdir(parents=True, exist_ok=True)
        tree_path.write_text(json.dumps(tree), encoding="utf-8")

        # 1. toy-detect: green census over the toy population (roster=3,
        #    sentinel=toy-signal; the blank grader sits in UNCLASSIFIED honestly).
        lines, code = run_census(root, roster_size_expected=3,
                                 sentinel_member_expected="toy-signal")
        sig = [l for l in lines if l.startswith("SENTINEL ")]
        unc = [l for l in lines if l.startswith("UNCLASSIFIED ")]
        ok = (code == 0 and len(sig) == 1 and "count=1 member=toy-signal" in sig[0]
              and "count=1 members=toy-blank" in unc[0])
        print("SELFTEST toy-detect rc=%d want_rc=0 %s" % (code, "ok" if ok else "FAIL"))
        results.append(("toy-detect", code, 0))

        # 2. toy-sha-drift: flip one committed byte -> sha-mismatch invariant, exit 1.
        p = toy_pure / "test_outputs.py"
        p.write_text(p.read_text(encoding="utf-8") + "# drift\n", encoding="utf-8")
        lines, code = run_census(root, roster_size_expected=3,
                                 sentinel_member_expected="toy-signal")
        ok = (code == 1 and any(l.startswith("INVARIANT-FAIL sha-mismatch") for l in lines))
        print("SELFTEST toy-sha-drift rc=%d want_rc=1 %s" % (code, "ok" if ok else "FAIL"))
        results.append(("toy-sha-drift", code, 1))
        p.write_text(p.read_text(encoding="utf-8").replace("# drift\n", ""), encoding="utf-8")

        # 3. toy-roster-drift: roster names a task with no dir -> invariant, exit 1.
        (pop / ROSTER_NAME).write_text("toy-signal\ntoy-pure\ntoy-blank\ntoy-ghost\n",
                                       encoding="utf-8")
        lines, code = run_census(root, roster_size_expected=3,
                                 sentinel_member_expected="toy-signal")
        ok = (code == 1 and any(l.startswith("INVARIANT-FAIL every-roster-task-has-grader-dir")
                                for l in lines))
        print("SELFTEST toy-roster-drift rc=%d want_rc=1 %s" % (code, "ok" if ok else "FAIL"))
        results.append(("toy-roster-drift", code, 1))

    failed = [name for name, rc, want_rc in results if rc != want_rc]
    print("SELFTEST cases=%d failed=%d" % (len(results), len(failed)))
    if failed:
        print("SELFTEST fail")
        return 1
    print("SELFTEST pass (rc=0 want_rc=0)")
    return 0


# --------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="round-62 grader-class census survey")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    lines, code = run_census(pathlib.Path(args.lane))
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if args.receipt:
        receipt = pathlib.Path(args.receipt)
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(text, encoding="utf-8", newline="\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
