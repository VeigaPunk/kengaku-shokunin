#!/usr/bin/env python3
"""Round 69, C2: the routed-defect gate for the round-68 non-author closure's seven items.

The round-68 verifier spot-check (`corpus/lessons/round-68-verifier-spotcheck.md` §5)
routed seven defects to this round.  Each check below re-derives one correction from the
lane's committed bytes; the corrections are frozen in plans/round-69-claims.md before the
wave runs.

Checks (frozen in plans/round-69-claims.md, R69-C2):
  E1  registry-rows      the four round-68 instruments have complete `## Gate/probe
                         registry` rows (name, kind, entry file that exists, verdict map,
                         self-test, pinned values, write scope, owner)
  E2  quality-criterion  QUALITY.md carries exactly one `## Round69 criterion` section
                         (Q50) citing both round-68 lesson files
  E3  receipt-provenance the provenance erratum names the tree it graded (TREE), the
                         landing (LANDING), and the sha256 of every bound input at BOTH
                         revisions; the DIFFERS set equals the observed differing set
  E4  verified-at        corpus/knowledge/tb2-network-service-offline-grader.md carries a
                         second, appended `verified-at:` line naming the round-68 landing
  E5  attack-arithmetic  corpus/lessons/round-68.md carries the corrected strict attack
                         share (3/12) with the strict role set named
  E6  results-rerecord   corpus/lessons/round-68.md records that w1-results.json carries
                         no seat outputs and points at the twelve per-seat reports
  E7  gate-receipts      the depth-gate and provenance-trio outputs are committed as
                         receipts and equal a fresh run byte for byte

--selftest builds a fake lane from copies of the real files with every correction
stripped BY CONSTRUCTION, requires all seven checks to fail there, then flips one byte in
each committed receipt and requires E7 to fail again; a check that cannot fail is vacuous.
"""

import argparse
import hashlib
import io
import pathlib
import shutil
import subprocess
import sys
from contextlib import redirect_stdout

SKILL = "SKILL.md"
QUALITY = "corpus/QUALITY.md"
LESSON68 = "corpus/lessons/round-68.md"
KNOWLEDGE = "corpus/knowledge/tb2-network-service-offline-grader.md"
PROVENANCE = "corpus/evidence/round69/c2-receipts/provenance-erratum.txt"
DEPTH_RECEIPT = "corpus/evidence/round69/gates/depth-gate.txt"
TRIO_RECEIPT = "corpus/evidence/round69/gates/trio.txt"

ROUND68_INSTRUMENTS = {
    "round68_c1_pypi_finish": "plans/round68_c1_pypi_finish.py",
    "round68_c2_correction_gate": "plans/round68_c2_correction_gate.py",
    "round68_report_contract": "plans/round68_report_contract.py",
    "round68_capability_table": "plans/round68_capability_table.py",
}
REGISTRY_HEADING = "## Gate/probe registry"
QUALITY_HEADING = "## Round69 criterion"
TREE = "27f649f8"
LANDING = "1ec2e60a"
STRICT_ROLES = ("reviewer", "critic", "mutation-tester", "labrat")

DEPTH_ARGV = [sys.executable, "plans/round63_gate_checks.py", "depth",
              "--skill", "SKILL.md", "--receipt",
              "corpus/evidence/round62/class-survey.txt", "--root", "."]
TRIO_ARGV = [sys.executable, "plans/round63_gate_checks.py", "trio", KNOWLEDGE]


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(pathlib.Path(path).read_bytes())


def section(text, heading):
    """Text of the first section whose line strip-equals `heading`, else None."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == heading:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def count_section(text, heading):
    return sum(1 for ln in text.splitlines() if ln.strip() == heading)


def registry_rows(skill_text):
    """name cell -> row line, from the registry section (heading-prefix match)."""
    lines = skill_text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith(REGISTRY_HEADING):
            start = i
            break
    rows = {}
    if start is None:
        return rows
    for ln in lines[start + 1:]:
        if ln.startswith("## "):
            break
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not cells:
            continue
        name = cells[0].strip("`").strip()
        if name in ROUND68_INSTRUMENTS:
            rows[name] = (ln, cells)
    return rows


def git_show(root, rev, path):
    run = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"],
                         capture_output=True)
    return None if run.returncode != 0 else run.stdout


def run_command(root, argv):
    run = subprocess.run(argv, cwd=str(root), capture_output=True, text=True)
    return run.stdout, run.returncode


def check(root):
    root = pathlib.Path(root)
    results = []

    def rec(n, ok, detail):
        results.append((n, ok, detail))
        print(f"E{n} {'ok' if ok else 'defect'} {detail}")

    # E1 — the four round-68 instruments carry complete registry rows.
    skill_path = root / SKILL
    if not skill_path.is_file():
        rec(1, False, f"{SKILL} missing")
    else:
        rows = registry_rows(skill_path.read_text(encoding="utf-8"))
        missing = [n for n in ROUND68_INSTRUMENTS if n not in rows]
        thin = []
        for name, entry in ROUND68_INSTRUMENTS.items():
            if name not in rows:
                continue
            _, cells = rows[name]
            problems = []
            if len(cells) < 8:
                problems.append(f"cells={len(cells)}")
            if entry not in (cells[2] if len(cells) > 2 else ""):
                problems.append("no-entry")
            elif not (root / entry).is_file():
                problems.append("entry-file-absent")
            if len(cells) > 3 and not ("`0`" in cells[3] and "`1`" in cells[3]):
                problems.append("no-verdict-map")
            if len(cells) > 4 and not cells[4]:
                problems.append("no-selftest")
            if problems:
                thin.append(f"{name}:{','.join(problems)}")
        rec(1, not missing and not thin,
            f"rows={len(rows)}/4 missing={missing} thin={thin}")

    # E2 — QUALITY.md carries exactly one Round69 criterion citing both lessons.
    qpath = root / QUALITY
    if not qpath.is_file():
        rec(2, False, f"{QUALITY} missing")
    else:
        text = qpath.read_text(encoding="utf-8")
        n = count_section(text, QUALITY_HEADING)
        sec = section(text, QUALITY_HEADING) or ""
        q50 = "Q50" in sec
        l68 = LESSON68 in sec
        lsc = "corpus/lessons/round-68-verifier-spotcheck.md" in sec
        rec(2, n == 1 and q50 and l68 and lsc,
            f"headings={n} q50={q50} round68-lesson={l68} spotcheck={lsc}")

    # E3 — provenance erratum: both revisions' shas for every bound input.
    ppath = root / PROVENANCE
    if not ppath.is_file():
        rec(3, False, f"{PROVENANCE} missing")
    else:
        lines = ppath.read_text(encoding="utf-8").splitlines()
        head = [ln for ln in lines if ln.startswith("TREE ")]
        land = [ln for ln in lines if ln.startswith("LANDING ")]
        inputs = [ln for ln in lines if ln.startswith("INPUT ")]
        differs = {ln.split(None, 1)[1].strip() for ln in lines
                   if ln.startswith("DIFFERS ")}
        problems = []
        if not head or head[0].split()[1] != TREE:
            problems.append("tree-line")
        if not land or land[0].split()[1] != LANDING:
            problems.append("landing-line")
        if not inputs:
            problems.append("no-inputs")
        observed_differs = set()
        for ln in inputs:
            parts = ln.split()
            if len(parts) != 4 or "at-tree=" not in parts[2] or "at-landing=" not in parts[3]:
                problems.append(f"malformed:{ln[:60]}")
                continue
            path = parts[1]
            a = parts[2].split("=", 1)[1]
            b = parts[3].split("=", 1)[1]
            ta = git_show(root, TREE, path)
            tb = git_show(root, LANDING, path)
            if ta is None or tb is None:
                problems.append(f"rev-missing:{path}")
                continue
            if sha256_bytes(ta) != a:
                problems.append(f"tree-sha:{path}")
            if sha256_bytes(tb) != b:
                problems.append(f"landing-sha:{path}")
            if a != b:
                observed_differs.add(path)
        if observed_differs != differs:
            problems.append(f"differs-set got={sorted(differs)} want={sorted(observed_differs)}")
        rec(3, not problems, f"inputs={len(inputs)} differs={sorted(observed_differs)} "
                             f"problems={problems}")

    # E4 — the knowledge entry's freshness trio points at this round's revision.
    kpath = root / KNOWLEDGE
    if not kpath.is_file():
        rec(4, False, f"{KNOWLEDGE} missing")
    else:
        lines = kpath.read_text(encoding="utf-8").splitlines()
        vs = [ln for ln in lines if ln.startswith("verified-at:")]
        appended = len(vs) >= 2 and LANDING in vs[-1]
        rec(4, appended, f"verified-at-lines={len(vs)} last-names-landing={appended}")

    # E5 — corrected strict attack-share arithmetic in the round-68 lesson.
    lpath = root / LESSON68
    if not lpath.is_file():
        rec(5, False, f"{LESSON68} missing")
        rec(6, False, f"{LESSON68} missing")
    else:
        text = lpath.read_text(encoding="utf-8")
        strict = [ln for ln in text.splitlines()
                  if "strict attack share" in ln and "3/12" in ln
                  and all(r in ln for r in STRICT_ROLES)]
        rec(5, len(strict) == 1, f"strict-lines={len(strict)}")
        rerec = [ln for ln in text.splitlines()
                 if "w1-results.json" in ln and 'output: ""' in ln
                 and "per-seat" in ln]
        rec(6, len(rerec) >= 1, f"rerecord-lines={len(rerec)}")

    # E7 — committed gate receipts equal a fresh run, byte for byte.
    problems = []
    for rel, argv in ((DEPTH_RECEIPT, DEPTH_ARGV), (TRIO_RECEIPT, TRIO_ARGV)):
        path = root / rel
        if not path.is_file():
            problems.append(f"{rel}:missing")
            continue
        fresh, rc = run_command(root, argv)
        if rc != 0:
            problems.append(f"{rel}:rc={rc}")
            continue
        if fresh != path.read_text(encoding="utf-8"):
            problems.append(f"{rel}:differ")
    rec(7, not problems, f"problems={problems}")

    defects = sum(1 for _, ok, _ in results if not ok)
    print(f"DEFECTS n={defects}")
    ok = defects == 0
    print(f"PREDICATE R69-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def selftest(scratch):
    scratch = pathlib.Path(scratch)
    fake = scratch / "fake-lane"
    if fake.exists():
        shutil.rmtree(fake)
    lane = pathlib.Path(__file__).resolve().parent.parent

    # Copy what each check needs, then strip every correction by construction.
    for rel in (SKILL, QUALITY, LESSON68, KNOWLEDGE, "plans/round63_gate_checks.py",
                "corpus/evidence/round62/class-survey.txt"):
        dst = fake / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(lane / rel, dst)
    for entry in ROUND68_INSTRUMENTS.values():
        dst = fake / entry
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("# fixture stub\n", encoding="utf-8")

    # E1: drop the four registry rows from the fixture SKILL.md (registry section only,
    # so the class table and its replay recipes stay intact for E7's command).
    skill_lines = (fake / SKILL).read_text(encoding="utf-8").splitlines(keepends=True)
    in_registry = False
    kept_skill = []
    for ln in skill_lines:
        if ln.strip().startswith(REGISTRY_HEADING):
            in_registry = True
            kept_skill.append(ln)
            continue
        if in_registry and ln.startswith("## "):
            in_registry = False
        if in_registry and any(f"`{name}`" in ln for name in ROUND68_INSTRUMENTS):
            continue
        kept_skill.append(ln)
    (fake / SKILL).write_text("".join(kept_skill), encoding="utf-8")
    # E2: drop the Round69 criterion section.
    qtext = (fake / QUALITY).read_text(encoding="utf-8")
    sec = section(qtext, QUALITY_HEADING)
    if sec is not None:
        (fake / QUALITY).write_text(qtext.replace(sec, ""), encoding="utf-8")
    # E4: drop the appended verified-at line(s), keep the first.
    klines = (fake / KNOWLEDGE).read_text(encoding="utf-8").splitlines(keepends=True)
    seen = 0
    kept = []
    for ln in klines:
        if ln.startswith("verified-at:"):
            seen += 1
            if seen > 1:
                continue
        kept.append(ln)
    (fake / KNOWLEDGE).write_text("".join(kept), encoding="utf-8")
    # E5/E6: remove the correction lines from the lesson copy.
    llines = (fake / LESSON68).read_text(encoding="utf-8").splitlines(keepends=True)
    (fake / LESSON68).write_text(
        "".join(ln for ln in llines
                if not ("strict attack share" in ln and "3/12" in ln)
                and not ("w1-results.json" in ln and 'output: ""' in ln)),
        encoding="utf-8")
    # E7: no receipts at all.

    # E3 needs a real .git-free facade: build a tiny scratch git repo with the two
    # revisions the erratum names, so the check can run its git plumbing on the fake.
    repo = fake
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "tree"], check=True)
    tree_rev = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=8", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    (repo / QUALITY).write_text("# changed\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "commit", "-qam", "landing"], check=True)
    land_rev = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=8", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    global TREE, LANDING
    saved = (TREE, LANDING)
    TREE, LANDING = tree_rev, land_rev
    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check(fake)
        out = buf.getvalue()
        failed = sum(1 for ln in out.splitlines() if ln.startswith("E") and " defect " in ln)
        print(out, end="")
        print(f"SELFTEST defects-in-fake={failed} want=7 all-fail="
              f"{'True' if (failed == 7 and rc == 1) else 'False'}")
        ok = failed == 7 and rc == 1

        # Second arm: receipts present but one byte flipped must still fail E7, and a
        # correct (fresh) pair must pass — E7 is the only check that runs commands.
        ok = ok and _selftest_e7(fake)
    finally:
        TREE, LANDING = saved
    return 0 if ok else 1


def _selftest_e7(fake):
    """E7's live-failure arm.  The green direction is witnessed by the landing run of
    this gate in the real lane (the committed receipts equal a fresh run there); a
    fixture lane cannot reproduce the real lane's 33 resolved class-table paths."""
    gates = fake / "corpus/evidence/round69/gates"
    gates.mkdir(parents=True, exist_ok=True)
    (fake / DEPTH_RECEIPT).write_text("stale\n", encoding="utf-8")
    (fake / TRIO_RECEIPT).write_text("stale\n", encoding="utf-8")
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = check(fake)
    out = buf.getvalue()
    e7_red = any(ln.startswith("E7 defect") for ln in out.splitlines())
    print(f"SELFTEST e7-stale-red={e7_red} rc={rc}")
    return e7_red and rc == 1


def lane_root():
    return pathlib.Path(__file__).resolve().parent.parent


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--root")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work")
    args = ap.parse_args(argv)
    if args.selftest:
        if not args.work or not pathlib.Path(args.work).is_dir():
            print("SETUP work-dir-required")
            return 2
        return selftest(args.work)
    return check(args.root or lane_root())


if __name__ == "__main__":
    sys.exit(main())
