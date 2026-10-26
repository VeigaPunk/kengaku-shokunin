#!/usr/bin/env python3
"""Fixture matrix for anchor_digest_check.py — kengaku round 37, seat R37AnchorSweep.

Builds one shared clone of the lane per case under the scratch dir, prepares the case with plain file
edits plus index-only `git add` (never a commit, never a mutating command on the lane), runs the checker
and compares its output with the case's expectation.

Usage: python3 fixture_matrix.py --lane LANE --scratch DIR --captures DIR --checker FILE [--receipt FILE]
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys

ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMM = re.compile(r"^rows=(\d+) tokens=(\d+) defects=(\d+)$")
ANCHOR, TEACHES = 6, 7
S110_WRONG = "4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c"
S110_TRUE = "4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c"
S108_TRUE = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
FABRICATED = "deadbeef" * 8
ERRATUM = (
    "Erratum (round 37): S110 anchor sha256 " + S110_WRONG + " is 63 hex digits (the `0` before `ea0f` was "
    "dropped in transcription); the capture's digest is sha256 " + S110_TRUE +
    " (corpus/evidence/round36/tb2-regex-log/SHA256SUMS, instruction.md).\n"
)


def git(lane, *args):
    r = subprocess.run(["git", "-C", str(lane), *args], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {r.stderr.decode()[:300]}")
    return r.stdout.decode()


def clone(lane, dest):
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--shared", str(lane), str(dest)], check=True)
    top = git(dest, "rev-parse", "--show-toplevel").strip()
    if pathlib.Path(top).resolve() != dest.resolve():
        raise SystemExit(f"clone toplevel {top} != {dest}")
    return dest


def edit_row(lane, sid, fn):
    p = lane / "corpus/SOURCES.md"
    lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if m and m.group(1) == sid:
            body = line.rstrip("\n")
            cells = body.split("|")
            fn(cells)
            lines[i] = "|".join(cells) + "\n"
            p.write_text("".join(lines), encoding="utf-8")
            return
    raise SystemExit(f"no row {sid}")


def set_anchor(sid, new):
    def fn(cells):
        if cells[ANCHOR].count(S110_WRONG) + cells[ANCHOR].count(S108_TRUE) != 1:
            raise SystemExit(f"{sid}: anchor cell does not carry the expected token")
        cells[ANCHOR] = cells[ANCHOR].replace(S110_WRONG, new).replace(S108_TRUE, new)
    return fn


def add_erratum(lane):
    p = lane / "corpus/lessons/round-36.md"
    text = p.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    p.write_text(text + "\n" + ERRATUM, encoding="utf-8")


def retype_erratum(lane, new):
    p = lane / "corpus/lessons/round-36.md"
    text = p.read_text(encoding="utf-8")
    if S110_TRUE not in text:
        raise SystemExit("erratum not present")
    p.write_text(text.replace(S110_TRUE, new), encoding="utf-8")


def stage_captures(lane, captures):
    dest = lane / "corpus/evidence/round37/anchor-captures"
    dest.mkdir(parents=True, exist_ok=True)
    for f in sorted(captures.iterdir()):
        if f.is_file():
            shutil.copy2(f, dest / f.name)
    git(lane, "add", "--", "corpus/evidence/round37/anchor-captures")


def untracked_manifest(lane, digest):
    dest = lane / "corpus/evidence/round37/anchor-captures"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "SHA256SUMS.untracked").write_text(f"{digest}  fabricated.py\n", encoding="utf-8")


def run(checker, lane, ref):
    r = subprocess.run([sys.executable, str(checker), "--lane", str(lane), "--evidence-ref", ref],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def parse(stdout):
    defects = [l for l in stdout.splitlines() if l.startswith("DEFECT ")]
    summ = [SUMM.match(l) for l in stdout.splitlines() if SUMM.match(l)]
    classes = sorted({re.search(r"class=(\S+)", d).group(1) for d in defects})
    ids = sorted({d.split()[1] for d in defects})
    n = int(summ[0].group(3)) if summ else -1
    return n, classes, ids, len(summ)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--captures", required=True)
    ap.add_argument("--checker", required=True)
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    scratch = pathlib.Path(a.scratch).resolve()
    caps = pathlib.Path(a.captures).resolve()
    checker = pathlib.Path(a.checker).resolve()
    out, ok_all = [], True

    def case(cid, expect_ids, expect_classes, prep, ref, expect_code, expect_n=None):
        nonlocal ok_all
        root = clone(lane, scratch / "fx" / cid / "lane")
        prep(root)
        code, stdout = run(checker, root, ref)
        n, classes, ids, nsumm = parse(stdout)
        want = len(expect_ids) if expect_n is None else expect_n
        ok = (n == want and ids == sorted(expect_ids) and classes == sorted(expect_classes)
              and code == expect_code and nsumm == 1)
        ok_all = ok_all and ok
        out.append(f"CASE {cid} ref={ref} defects={n}/{want} ids={','.join(ids) or '-'} "
                   f"classes={','.join(classes) or '-'} exit={code} {'ok' if ok else 'WRONG'}")
        out.append(f"  expect ids={','.join(sorted(expect_ids)) or '-'} "
                   f"classes={','.join(sorted(expect_classes)) or '-'} exit={expect_code}")
        for line in stdout.splitlines():
            out.append("  | " + line)

    five = ["S070", "S072", "S073", "S074", "S110"]
    four = ["S070", "S072", "S073", "S074"]

    case("F0-lane-as-is", five, ["digest-short", "digest-unknown"], lambda l: None, "head", 1)
    case("F1-erratum-only", four, ["digest-unknown"], add_erratum, "head", 1)
    case("F2-erratum-plus-captures", [], [], lambda l: (add_erratum(l), stage_captures(l, caps)), "index", 0)
    case("C7-captures-staged-head-mode", four, ["digest-unknown"],
         lambda l: (add_erratum(l), stage_captures(l, caps)), "head", 1)
    case("M1-erratum-wrong-correction", ["S110"],
         ["digest-short", "erratum-digest-unresolved", "erratum-incomplete"],
         lambda l: (add_erratum(l), stage_captures(l, caps), retype_erratum(l, FABRICATED)), "index", 1, 3)
    case("M2-correction-not-in-manifest", ["S110"], ["digest-unknown", "erratum-incomplete"],
         lambda l: (add_erratum(l), stage_captures(l, caps), retype_erratum(l, FABRICATED),
                    edit_row(l, "S110", set_anchor("S110", FABRICATED))), "index", 1, 2)
    case("M3-s108-shortened", ["S108"], ["digest-short"],
         lambda l: (add_erratum(l), stage_captures(l, caps),
                    edit_row(l, "S108", set_anchor("S108", S108_TRUE[:-1]))), "index", 1)
    case("M4-s108-uppercase", ["S108"], ["digest-uppercase"],
         lambda l: (add_erratum(l), stage_captures(l, caps),
                    edit_row(l, "S108", set_anchor("S108", S108_TRUE.upper()))), "index", 1)

    def m5(l):
        add_erratum(l)
        stage_captures(l, caps)
        edit_row(l, "S110", set_anchor("S110", S110_TRUE))

        def teaches(cells):
            cells[TEACHES] = cells[TEACHES] + " sha256 " + S110_TRUE
        edit_row(l, "S110", teaches)

    case("M5-token-in-another-cell", ["S110"], ["token-outside-anchor"], m5, "index", 1)

    def c6(l):
        add_erratum(l)
        stage_captures(l, caps)
        edit_row(l, "S110", set_anchor("S110", FABRICATED))
        untracked_manifest(l, FABRICATED)
    case("C6-untracked-manifest-does-not-count", ["S110"], ["digest-unknown"], c6, "index", 1)

    # null: the F2 tree re-run must print the same thing (no state carried between runs).
    root = clone(lane, scratch / "fx" / "NULL" / "lane")
    add_erratum(root)
    stage_captures(root, caps)
    c1, o1 = run(checker, root, "index")
    c2, o2 = run(checker, root, "index")
    null_ok = (c1, o1) == (c2, o2) and c1 == 0
    ok_all = ok_all and null_ok
    out.append(f"CASE NULL-rerun identical={o1 == o2} exit={c1} {'ok' if null_ok else 'WRONG'}")

    for line in out:
        print(line)
    text = "\n".join(out) + "\n"
    if a.receipt:
        pathlib.Path(a.receipt).write_text(text, encoding="utf-8")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
