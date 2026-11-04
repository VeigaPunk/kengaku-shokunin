#!/usr/bin/env python3
"""R82-C2 counter — the previous closure's routed defects are discharged, not restated.

Universe (derived, never listed): the routed ids of the NEWEST non-author spot-check by round number,
`corpus/lessons/round-<n>-verifier-spotcheck.md`, section `## 5. Routed defects`
(`- **V<n> · ...**` lines); the lane registry names them `R<round>-V<n>`.

A discharged id has exactly one row in `corpus/routed-findings.jsonl` with:
  status   `closed`
  source   `<spotcheck>:<line>` and that line carries the id
  close    a tracked path (or commit) that is NOT the spot-check itself and whose bytes carry the id
           AND the row's `evidence_literal` (the repair, not the routing)
  check    a shell command, run from the lane root (or from a materialised tree under `--rev`), that
           exits 0 exactly when the repair holds; a check that cannot fail (`true`, `:`, `exit 0`,
           empty) is `CHECK-TRIVIAL`
plus `corpus/README.md` indexes the spot-check file.

Frozen before data on 2026-11-04 (L1 KengakuR82); see plans/round-82-claims.md §R82-C2.

    python3 plans/round82_c2_closure_debt.py --lane .                  # verdict, worktree checks
    python3 plans/round82_c2_closure_debt.py --lane . --rev <rev>      # checks over a materialised tree
    python3 plans/round82_c2_closure_debt.py --selftest --work DIR
    python3 plans/round82_c2_closure_debt.py --mutants --work DIR
    python3 plans/round82_c2_closure_debt.py --control-presence --work DIR

Printed lines:
    UNIVERSE spotcheck=<path> ids=<n> [<csv>]
    DEBT <id> status=<s> close=<path|-> check=<present|absent>
    DEBT-TOTAL ids=<n> registered=<n> closed=<n> checks_passed=<n>
    INDEX <path> indexed=<yes|no>
    DEFECT <CODE> <detail>
    DEFECTS n=<n>
    TARGET ids=<n> closed=<n> checks_passed=<n> indexed=<yes|no>
    PREDICATE R82-C2 pass|fail
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tarfile
import io
from pathlib import Path

ROUTED = "corpus/routed-findings.jsonl"
README = "corpus/README.md"
SPOT_RE = re.compile(r"^corpus/lessons/round-(\d+)-verifier-spotcheck\.md$")
ID_LINE = re.compile(r"^- \*\*V(\d+) · ", re.M)
TRIVIAL = re.compile(r"^\s*(true|:|exit 0|echo .*|/bin/true)\s*$")
STATUSES = ("open", "closed", "refused", "blocked")
TIMEOUT = 600
BASE_REV = "a3a03ac31451e58f1742b9bccb73b72c2d90a95c"   # round-82 base (round-81 tip)


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else ""


def newest_spotcheck(root: Path) -> tuple[str, int, list[int]] | None:
    best = None
    for line in git(root, "ls-files").split():
        m = SPOT_RE.match(line)
        if not m:
            continue
        n = int(m.group(1))
        if best is None or n > best[1]:
            best = (line, n, [])
    if best is None:
        return None
    text = (root / best[0]).read_text(errors="replace")
    ids = [int(x) for x in ID_LINE.findall(text)]
    return best[0], best[1], ids


def load_rows(root: Path) -> dict[str, dict]:
    fp = root / ROUTED
    out = {}
    if not fp.is_file():
        return out
    for line in fp.read_text(errors="replace").split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id"):
            out[d["id"]] = d
    return out


def materialise(root: Path, rev: str, work: Path) -> Path:
    dst = Path(tempfile.mkdtemp(dir=work, prefix="tree-%s-" % rev[:8]))
    p = subprocess.run(["git", "-C", str(root), "archive", rev], capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("archive failed for %s" % rev)
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
        tf.extractall(dst)
    # include untracked-but-needed scratch (none) and keep the tree read-only for checks
    return dst


def run_check(cmd: str, cwd: Path, env_extra: dict | None = None) -> int:
    env = {k: v for k, v in os.environ.items() if not re.search(r"(TOKEN|KEY|SECRET|PASSWORD)", k, re.I)}
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True, timeout=TIMEOUT, env=env)
    return p.returncode


def evaluate(lane: Path, rev: str | None, work: Path | None = None) -> int:
    defects: list[tuple[str, str]] = []
    spot = newest_spotcheck(lane)
    if spot is None:
        print("SETUP no round-<<n>>-verifier-spotcheck.md in the tracked tree")
        return 2
    spot_path, spot_round, ids = spot
    prefix = "R%d-V" % spot_round
    print("UNIVERSE spotcheck=%s ids=%d %s" % (spot_path, len(ids),
          ",".join(prefix + str(i) for i in ids)))
    spot_lines = (lane / spot_path).read_text(errors="replace").split("\n")
    rows = load_rows(lane)
    seen_ids = []
    for line in (lane / ROUTED).read_text(errors="replace").split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id"):
            seen_ids.append(d["id"])
    for dup in sorted({x for x in seen_ids if seen_ids.count(x) > 1}):
        defects.append(("DUPLICATE-ROW", dup))
    root = lane
    cleanup = None
    if rev:
        if work is None:
            work = Path(tempfile.mkdtemp(prefix="r82c2-"))
        root = materialise(lane, rev, Path(work))
        cleanup = root
        # the checks are the INSTRUMENT, not evidence: the current checker runs against the older tree
        chk = lane / "plans/round82_c2_checks.py"
        if chk.is_file():
            (root / "plans").mkdir(parents=True, exist_ok=True)
            shutil.copy2(chk, root / "plans/round82_c2_checks.py")
        # the routed ledger itself comes from the measured tree
        rows = load_rows(root) or rows
    closed = checks_ok = registered = 0
    for i in ids:
        rid = prefix + str(i)
        r = rows.get(rid)
        if r is None:
            defects.append(("DEBT-UNREGISTERED", rid))
            print("DEBT %s status=- close=- check=absent" % rid)
            continue
        registered += 1
        st = r.get("status")
        close = (r.get("close") or "").strip()
        check = (r.get("check") or "").strip()
        lit = (r.get("evidence_literal") or "").strip()
        print("DEBT %s status=%s close=%s check=%s" % (rid, st, close or "-", "present" if check else "absent"))
        if st not in STATUSES:
            defects.append(("STATUS", "%s %r" % (rid, st)))
        if st != "closed":
            defects.append(("NOT-CLOSED", rid))
            continue
        closed += 1
        src = r.get("source") or ""
        m = re.match(r"(.+):(\d+)$", src)
        if not m:
            defects.append(("SOURCE-SHAPE", rid))
        else:
            line_no = int(m.group(2))
            ok_src = 0 < line_no <= len(spot_lines) and ("V%d" % i) in spot_lines[line_no - 1]
            if not ok_src:
                defects.append(("SOURCE-LINE", rid))
        if close == spot_path or close.startswith(spot_path):
            defects.append(("CLOSE-NOT-REPAIR", rid))
        else:
            target = root / close.split()[0] if close else None
            if target is None or not target.is_file():
                defects.append(("CLOSE-UNRESOLVED", "%s %s" % (rid, close)))
            else:
                body = target.read_text(errors="replace")
                if rid not in body:
                    defects.append(("CLOSE-NO-ID", rid))
                if not lit:
                    defects.append(("EVIDENCE-LITERAL-EMPTY", rid))
                elif lit not in body:
                    defects.append(("CLOSE-NO-EVIDENCE", "%s literal=%r" % (rid, lit)))
        if not check or TRIVIAL.match(check):
            defects.append(("CHECK-TRIVIAL", rid))
            continue
        try:
            rc = run_check(check, root)
        except subprocess.TimeoutExpired:
            defects.append(("CHECK-TIMEOUT", rid))
            continue
        if rc == 0:
            checks_ok += 1
        else:
            defects.append(("CHECK-FAIL", "%s rc=%d" % (rid, rc)))
    readme = (root / README).read_text(errors="replace") if (root / README).is_file() else ""
    indexed = (spot_path in readme) or (Path(spot_path).name in readme)
    print("INDEX %s indexed=%s" % (spot_path, "yes" if indexed else "no"))
    if not indexed:
        defects.append(("INDEX-MISSING", spot_path))
    print("DEBT-TOTAL ids=%d registered=%d closed=%d checks_passed=%d" % (len(ids), registered, closed, checks_ok))
    for code, detail in defects:
        print("DEFECT %s %s" % (code, detail))
    print("DEFECTS n=%d" % len(defects))
    ok = not defects and len(ids) > 0
    print("TARGET ids=%d closed=%d checks_passed=%d indexed=%s" % (
        len(ids), closed, checks_ok, "yes" if indexed else "no"))
    print("PREDICATE R82-C2 %s" % ("pass" if ok else "fail"))
    if cleanup is not None:
        shutil.rmtree(cleanup, ignore_errors=True)
    return 0 if ok else 1


FIXTURE_SPOT = "corpus/lessons/round-77-verifier-spotcheck.md"
FIXTURE_REPAIR = "corpus/lessons/round-78.md"
FIXTURE_README = "| `lessons/round-77-verifier-spotcheck.md` | closure |\n"


def fixture(root: Path, ids=(1, 2), rows_mode="good", readme=FIXTURE_README,
            check_cmd="python3 plans/fxcheck.py u1", spot_name=None) -> None:
    (root / "corpus/lessons").mkdir(parents=True, exist_ok=True)
    spot = "corpus/lessons/round-77-verifier-spotcheck.md"
    lines = ["# spot", "", "## 5. Routed defects", ""]
    for i in ids:
        lines.append("- **V%d · a routed defect**" % i)
    (root / spot).write_text("\n".join(lines) + "\n")
    repair = "corpus/lessons/round-78.md"
    body = "\n".join("R77-V%d correction: counted." % i for i in ids)
    (root / repair).write_text(body + "\n")
    (root / "corpus/README.md").write_text(readme)
    (root / "plans").mkdir(exist_ok=True)
    (root / "plans/fxcheck.py").write_text(
        "import sys\nwant=sys.argv[1] if len(sys.argv)>1 else ''\n"
        "import pathlib\nbody=pathlib.Path('corpus/lessons/round-78.md').read_text()\n"
        "rid='R77-V'+(want[1:] if want.startswith('u') else '1')\n"
        "sys.exit(0 if rid in body and 'correction' in body else 1)\n")
    rows = []
    for i in ids:
        rows.append({"id": "R77-V%d" % i, "status": "closed",
                     "source": "%s:%d" % (spot, 4 + i), "close": repair,
                     "check": check_cmd.replace("u1", "u%d" % i),
                     "evidence_literal": "R77-V%d" % i})
    if rows_mode == "presence":
        rows = [{"id": "R77-V%d" % i, "status": "closed", "source": spot,
                 "close": spot, "check": "true", "evidence_literal": spot} for i in ids]
    if rows_mode == "dropped":
        rows = rows[:-1]
    if rows_mode == "status-open":
        rows[0]["status"] = "open"
    if rows_mode == "close-unresolved":
        rows[0]["close"] = "corpus/lessons/absent.md"
    if rows_mode == "check-trivial":
        rows[0]["check"] = "true"
    (root / ROUTED).write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def git_init(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=k", "-c", "user.email=k@k", "commit", "-qm", "fx"], check=True)


def selftest(work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    cases = [
        ("green", {}, 0),
        ("dropped-row", {"rows_mode": "dropped"}, 1),
        ("presence", {"rows_mode": "presence"}, 1),
        ("no-index", {"readme": ""}, 1),
        ("status-open", {"rows_mode": "status-open"}, 1),
        ("close-unresolved", {"rows_mode": "close-unresolved"}, 1),
        ("check-trivial", {"rows_mode": "check-trivial"}, 1),
    ]
    failures = reds = 0
    for name, kw, want in cases:
        root = Path(tempfile.mkdtemp(dir=work))
        fixture(root, **kw)
        git_init(root)
        rc = evaluate(root, None, work=work)
        shutil.rmtree(root, ignore_errors=True)
        if rc != 0:
            reds += 1
        if rc != want:
            failures += 1
            print("CASE %s FAIL want_rc=%d got_rc=%d" % (name, want, rc))
        else:
            print("CASE %s ok" % name)
    print("SELFTEST cases=%d red=%d failures=%d" % (len(cases), reds, failures))
    return 0 if failures == 0 else 1


def mutants(work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    M = [("dropped-row", {"rows_mode": "dropped"}), ("presence", {"rows_mode": "presence"}),
         ("no-index", {"readme": ""}), ("status-open", {"rows_mode": "status-open"}),
         ("close-unresolved", {"rows_mode": "close-unresolved"}),
         ("check-trivial", {"rows_mode": "check-trivial"})]
    killed = survived = 0
    for name, kw in M:
        root = Path(tempfile.mkdtemp(dir=work))
        fixture(root, **kw)
        git_init(root)
        rc = evaluate(root, None, work=work)
        shutil.rmtree(root, ignore_errors=True)
        if rc != 0:
            killed += 1
            print("MUTANT %s killed" % name)
        else:
            survived += 1
            print("MUTANT %s SURVIVED" % name)
    print("MUTANTS real=%d killed=%d survived=%d" % (killed + survived, killed, survived))
    return 0 if survived == 0 else 1


def control_presence(work: Path) -> bool:
    work.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(dir=work))
    fixture(root, rows_mode="presence")
    git_init(root)
    rc = evaluate(root, None, work=work)
    shutil.rmtree(root, ignore_errors=True)
    return rc != 0


def sensitivity(lane: Path, work: Path) -> int:
    """Every repair check must FAIL on the base tree with the round's rows overlaid."""
    work.mkdir(parents=True, exist_ok=True)
    tree = materialise(lane, BASE_REV, work)
    shutil.copy2(lane / "plans/round82_c2_checks.py", tree / "plans/round82_c2_checks.py")
    shutil.copy2(lane / ROUTED, tree / ROUTED)
    rows = load_rows(lane)
    spot = newest_spotcheck(lane)
    prefix = "R%d-V" % spot[1]
    failed = 0
    total = 0
    for i in spot[2]:
        rid = prefix + str(i)
        r = rows.get(rid) or {}
        cmd = (r.get("check") or "").strip()
        if not cmd:
            continue
        total += 1
        rc = run_check(cmd, tree)
        print("SENSITIVITY %s rc=%d %s" % (rid, rc, "fail-at-base (as required)" if rc != 0 else "PASSES-AT-BASE"))
        if rc != 0:
            failed += 1
    print("SENSITIVITY n=%d failed_at_base=%d" % (total, failed))
    shutil.rmtree(tree, ignore_errors=True)
    return 0 if failed == total and total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="R82-C2 closure-debt counter")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-presence", action="store_true")
    ap.add_argument("--sensitivity", action="store_true")
    a = ap.parse_args(argv)
    if a.sensitivity:
        if not a.work:
            print("SETUP --work required")
            return 2
        return sensitivity(Path(a.lane).resolve(), Path(a.work))
    if a.selftest or a.mutants or a.control_presence:
        if not a.work:
            print("SETUP --work required")
            return 2
        w = Path(a.work)
        if a.selftest:
            return selftest(w)
        if a.mutants:
            return mutants(w)
        lost = control_presence(w)
        print("CONTROL presence caught=%s target_reached=%s" % (lost, "False" if lost else "True"))
        return 0 if lost else 1
    return evaluate(Path(a.lane).resolve(), a.rev, Path(a.work) if a.work else None)


if __name__ == "__main__":
    sys.exit(main())
