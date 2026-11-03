#!/usr/bin/env python3
"""Round 68, C2: the correction gate for the round-67 closure's five routed defects.

Each check verifies one dated correction landed where the round-68 claims doc freezes
it, re-deriving what the bytes allow (sha256 re-hashes, count re-derivations).  The
checks are calibration instruments: they catch a self-assessment (report, LOG,
registry) that does not match the observed repo state.

Checks (frozen in plans/round-68-claims.md, R68-C2):
  E1  erratum-sha      plans/round-67-claims.md carries exactly one
                       `## Erratum (round 68)` section naming BOTH the correct probe
                       sha 03793f4f... and the wrongly-cited 32bacf1d...
  E2  mutant-count     that section states `7 refused` and `1 accepted by design`
  E3  selftest-tally   corpus/evidence/round68/r67-probe-selftest.txt exists, carries
                       `PROBE sha256=03793f4f...`, a SELFTEST line and an rc= capture;
                       the gate re-hashes plans/round67_c1_pipeline_probe.py itself
  E4  registry-rows    SKILL.md has a round67_c1_pipeline_probe registry row and the
                       round65-c1-sqlite-probe row names --strict
  E5  before-value     the erratum names the true delta: `recipe-unexecuted` and
                       `executed 2 of 3`

--selftest builds a fake lane tree under the scratch root (copies of the real files,
corrections absent) and requires every check to FAIL there; a check that cannot fail
is vacuous and the gate refuses itself.
"""

import argparse
import hashlib
import io
import pathlib
import shutil
import sys
from contextlib import redirect_stdout

R67_PROBE_SHA = "03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e"
WRONG_SHA = "32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836"
ERRATUM_HEADING = "## Erratum (round 68)"
CLAIMS = "plans/round-67-claims.md"
TALLY = "corpus/evidence/round68/r67-probe-selftest.txt"
R67_PROBE = "plans/round67_c1_pipeline_probe.py"
SKILL = "SKILL.md"
A1_MUTANTS = "corpus/evidence/round67/pipe/a1-mutants.txt"


def sha256_file(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def erratum_section(text):
    """Return the text of the first `## Erratum (round 68)` section, else None."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == ERRATUM_HEADING:
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


REGISTRY_HEADING = "## Gate/probe registry (PROTOCOL §Gate standard)"


def registry_section(skill_text):
    """Return the registry section (heading to the next `## `), else the whole text."""
    lines = skill_text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == REGISTRY_HEADING:
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


def check(root):
    root = pathlib.Path(root)
    results = []

    def rec(n, ok, detail):
        results.append((n, ok, detail))
        print(f"E{n} {'ok' if ok else 'defect'} {detail}")

    # E1 — erratum section with both shas; the frozen clause says "exactly one"
    # `## Erratum (round 68)` heading, so the heading count is bound (amendment A1,
    # round-68 claims doc: the first-match read under-counted duplicates).
    claims = root / CLAIMS
    text = claims.read_text(encoding="utf-8") if claims.is_file() else ""
    n_headings = sum(1 for ln in text.splitlines() if ln.strip() == ERRATUM_HEADING)
    sec = erratum_section(text) if text else None
    if sec is None:
        rec(1, False, f"{ERRATUM_HEADING} section absent in {CLAIMS}")
    elif n_headings != 1:
        rec(1, False, f"{ERRATUM_HEADING} heading count {n_headings} (want exactly 1)")
    else:
        has_new = R67_PROBE_SHA in sec
        has_old = WRONG_SHA in sec
        rec(1, has_new and has_old,
            f"section present, correct-sha={has_new}, wrong-sha-named={has_old}")

    # E2 — mutant-count correction inside the same section.
    if sec is None:
        rec(2, False, "no erratum section")
    else:
        seven = "7 refused" in sec
        one = "1 accepted by design" in sec
        rec(2, seven and one, f"7-refused={seven}, 1-accepted-by-design={one}")

    # E3 — committed selftest tally, bound to the round-67 probe bytes.
    tally = root / TALLY
    probe = root / R67_PROBE
    probe_sha = sha256_file(probe) if probe.is_file() else ""
    hash_ok = probe_sha == R67_PROBE_SHA
    if not tally.is_file():
        rec(3, False, f"{TALLY} missing (probe re-hash {'ok' if hash_ok else 'MISMATCH'})")
    else:
        t = tally.read_text(encoding="utf-8")
        has_probe_line = f"PROBE sha256={R67_PROBE_SHA}" in t
        has_selftest = "SELFTEST" in t
        has_rc = "rc=" in t
        rec(3, has_probe_line and has_selftest and has_rc and hash_ok,
            f"probe-line={has_probe_line}, selftest-line={has_selftest}, "
            f"rc-capture={has_rc}, probe-rehash={'ok' if hash_ok else 'MISMATCH'}")

    # E4 — registry rows in SKILL.md's Gate/probe registry section.
    skill = root / SKILL
    if not skill.is_file():
        rec(4, False, f"{SKILL} missing")
    else:
        reg = registry_section(skill.read_text(encoding="utf-8"))
        if reg is None:
            rec(4, False, f"registry section absent ({REGISTRY_HEADING})")
        else:
            new_row = "round67_c1_pipeline_probe" in reg
            strict_row = False
            for ln in reg.splitlines():
                if "round65-c1-sqlite-probe" in ln:
                    strict_row = "--strict" in ln
                    break
            rec(4, new_row and strict_row,
                f"pipeline-row={new_row}, sqlite-row-strict={strict_row}")

    # E5 — the before-value correction inside the erratum section.
    if sec is None:
        rec(5, False, "no erratum section")
    else:
        before = "recipe-unexecuted" in sec
        after = "executed 2 of 3" in sec
        rec(5, before and after,
            f"recipe-unexecuted={before}, executed-2-of-3={after}")

    defects = sum(1 for _, ok, _ in results if not ok)
    print(f"DEFECTS n={defects}")
    ok = defects == 0
    print(f"PREDICATE R68-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def selftest(scratch):
    """Every check must FAIL on a fake lane tree that simulates the pre-correction
    state BY CONSTRUCTION (stripped erratum, stripped registry rows, no tally) —
    so the selftest stays valid before and after the corrections land."""
    scratch = pathlib.Path(scratch)
    fake = scratch / "fake-lane"
    if fake.exists():
        shutil.rmtree(fake)
    (fake / "plans").mkdir(parents=True)
    (fake / "corpus" / "evidence" / "round68").mkdir(parents=True)
    (fake / "corpus" / "evidence" / "round67" / "pipe").mkdir(parents=True)
    lane = lane_root()

    # claims doc with any erratum section stripped
    claims_text = (lane / CLAIMS).read_text(encoding="utf-8")
    sec = erratum_section(claims_text)
    if sec is not None:
        claims_text = claims_text.replace(sec, "")
    (fake / CLAIMS).write_text(claims_text, encoding="utf-8")

    # SKILL.md with the pipeline row dropped and --strict removed from the sqlite row
    skill_lines = (lane / SKILL).read_text(encoding="utf-8").splitlines(keepends=True)
    kept = []
    for ln in skill_lines:
        if "round67_c1_pipeline_probe" in ln:
            continue
        if "round65-c1-sqlite-probe" in ln:
            ln = ln.replace("--strict", "")
        kept.append(ln)
    (fake / SKILL).write_text("".join(kept), encoding="utf-8")

    # round-67 probe and a1-mutants copied as-is; no tally file is created
    for rel in (R67_PROBE, A1_MUTANTS):
        dst = fake / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(lane / rel, dst)

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = check(fake)
    out = buf.getvalue()
    failed = sum(1 for ln in out.splitlines() if ln.startswith("E") and " defect " in ln)
    print(out, end="")
    print(f"SELFTEST defects-in-fake={failed} want=5 all-fail={'True' if (failed == 5 and rc == 1) else 'False'}")
    return 0 if (failed == 5 and rc == 1) else 1


def lane_root():
    return pathlib.Path(__file__).resolve().parent.parent


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--root")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work")
    args = ap.parse_args(argv)
    if args.selftest:
        work = args.work
        if not work or not pathlib.Path(work).is_dir():
            print("SETUP work-dir-required")
            return 2
        return selftest(work)
    return check(args.root or lane_root())


if __name__ == "__main__":
    sys.exit(main())
