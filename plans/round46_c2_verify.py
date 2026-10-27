#!/usr/bin/env python3
"""Round-46 C2 counter (depth): the false detail round 45 landed is superseded and marked, not left standing.

Routed by `corpus/lessons/round-45-verifier-spotcheck.md` §2 (C2: "depth harmed — false detail and three
mislocated anchors landed and are left unmarked in `SOURCES.md` and the entry") and §5 items 1-2. The surface is
the corpus's line-level detail: SOURCES registry anchor cells that cite a line, a range and a word count, and the
`password-recovery` entry's `## Predictor`, `source:` ranges and errata. Base (the round-45 closure tip)
`64ba8385ea10af1b78d367dcb242b92d97062af7`.

Legs (each prints one line; a leg that cannot run is a defect, never a pass):

  A  anchor lines. `plans/anchor_line_check.py` (pinned) over the lane registry must print `live=0`: every
     captured row whose anchor cites `:N "quote"` has the quote on line N, a first `<file>:<a>-<b>` range that
     holds N and does not pass the file's end, and a correct `(K words)`; or the row is superseded (Q34) by a
     defect-free row. Also: every base row is still present with every cell except `status`, `recheck` and
     `used-by` byte-identical to the base revision (an in-place fix is a rule-2 defect, not a repair).
     Prints `A anchorline live=<n> repaired=<n> base_rows=<n> base_missing=<n> base_changed=<n>`.
  B  predictor. The entry's `## Predictor` block (exactly one ```python block, r45 lint rules) is run against the
     CAPTURED grader (`corpus/evidence/round45/tb2-password-recovery/test_outputs.py`, pinned) on the frozen
     newline state set below, both inside bubblewrap via the round-45 counter's own sandbox helpers (that file
     pinned). Requires disagree=0 and at least 4 grader passes and 4 grader fails.
     Prints `B predictor states=<n> grader_pass=<n> grader_fail=<n> disagree=<n>`.
  C  entry detail. Every `source:` line of `corpus/knowledge/tb2-password-recovery-grader.md` that cites a
     `lines <a>-<b>` or `:<a>-<b>` range names a row whose capture has at least b lines, and the entry carries a
     `## Errata (round 46)` section naming each of `lone-CR`, `S152`, `S153`, `S154`, `empty-file`.
     Prints `C entry source_ranges=<n> source_ranges_bad=<n> errata_marks=<k>/5`.
  D  gate red fixture. `plans/anchor_line_check.py --selftest` exits 0 (RED exit 1, GREEN exit 0, JUNK exit 1).
     Prints `D selftest exit=<rc>`.

Frozen predicate (same sentence in plans/round-46-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round46_c2_verify.py --lane .` prints `PINS total=3 mismatched=0`, then
  `A anchorline live=0` with `base_missing=0 base_changed=0`, `B predictor` with `disagree=0`, grader_pass>=4 and
  grader_fail>=4, `C entry` with `source_ranges_bad=0 errata_marks=5/5`, `D selftest exit=0`, then
  `checks=4 defects=0` and `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip (the clone
  needs the base revision in its history for leg A).

`--work DIR` holds the sandbox scratch (TMPDIR honoured otherwise). Exit 0 pass, 1 fail, 2 setup error.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import tempfile

BASE = "64ba8385ea10af1b78d367dcb242b92d97062af7"
ALC_REL = "plans/anchor_line_check.py"
R45_REL = "plans/round45_c2_verify.py"
GRADER_REL = "corpus/evidence/round45/tb2-password-recovery/test_outputs.py"
ENTRY_REL = "corpus/knowledge/tb2-password-recovery-grader.md"
PINS = {
    ALC_REL: "35d02dc55393bea18787e35cc2827cbab65f2d645b81a3c1946722065a4fdedf",
    R45_REL: "ab6825e34596ba71f59a184a59fd4e672fd22dcf4b892c511cae5ead2b104f50",
    GRADER_REL: "2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e",
}
MUTABLE = (7, 9, 10)  # status, recheck, used-by (0-based cell index)
ERRATA_HEAD = re.compile(r"^## Errata \(round 46\)\n(.*?)(?=^## |\Z)", re.S | re.M)
ERRATA_MARKS = ("lone-CR", "S152", "S153", "S154", "empty-file")
SOURCE_LINE = re.compile(r"^source:\s*(S\d{3,})\b(.*)$", re.M)
SRC_RANGE = re.compile(r"(?:lines\s+|:)(\d+)-(\d+)")
# Frozen newline state set (no verdict stored): C is the answer the captured grader embeds, D a decoy line.
STATE_SHAPES = (
    "C\rD",        # lone CR between two lines
    "D\rC",        # lone CR before the answer
    "D\n\rC",      # LF then CR
    "C\r",         # trailing lone CR
    "\rC",         # leading lone CR
    "C\r\r\nD",    # CR CR LF
    "D\r\rC",      # two lone CRs
    "D\r\nC\rD",   # CRLF then lone CR
    "C\r\n",       # CRLF control
    "D\r\nC\r\n",  # CRLF control
    "D\rD",        # lone CR, no answer
    "Cx\rD",       # answer prefix, lone CR
    "C\x0bD",      # vertical tab: not a universal newline (splitlines would split)
    "C\x0cD",      # form feed: not a universal newline
    "C\x85D",      # NEL: not a universal newline
    "C\u2028D",    # LINE SEPARATOR: not a universal newline
)
DECOY = "QQQQ1111RRRR2222SSSS333"


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def leg_a(lane, alc):
    lines = []
    rc, res = alc.check(lane, out=lines.append)
    if rc == 2:
        return False, "anchor_line_check setup error"
    live = len(res["live"])
    rep = len(res["repaired"])
    base_text = subprocess.run(["git", "-C", str(lane), "show", f"{BASE}:corpus/SOURCES.md"],
                               capture_output=True, text=True, check=True).stdout
    base = {sid: cells for sid, cells, _l in alc.parse_rows(base_text)}
    tip = {}
    for sid, cells, _l in alc.parse_rows((lane / "corpus/SOURCES.md").read_text()):
        tip.setdefault(sid, []).append(cells)
    missing = [s for s in base if s not in tip]
    changed = []
    for s, cells in base.items():
        if s not in tip:
            continue
        if len(tip[s]) != 1 or len(tip[s][0]) != len(cells) or any(
                tip[s][0][k] != cells[k] for k in range(len(cells)) if k not in MUTABLE):
            changed.append(s)
    ok = live == 0 and not missing and not changed
    return ok, (f"live={live} repaired={rep} base_rows={len(base)} base_missing={len(missing)}"
                f" base_changed={len(changed)}" + (f" first_changed={changed[0]}" if changed else ""))


def leg_b(lane, r45, work):
    entry = (lane / ENTRY_REL).read_text()
    sec = r45.PRED_SECTION.search(entry)
    blocks = r45.PRED_BLOCK.findall(sec.group(1)) if sec else []
    if len(blocks) != 1:
        return False, f"'## Predictor' needs exactly one python block (found {len(blocks)})"
    lint = r45.lint_block(blocks[0])
    if lint:
        return False, f"predictor lint tokens present: {','.join(lint)}"
    src = (lane / GRADER_REL).read_text()
    lits = sorted(set(re.findall(r'"([0-9A-Z]{23})"', src)))
    if len(lits) != 1:
        return False, f"expected one 23-char answer literal in the grader, found {len(lits)}"
    c = lits[0]
    states = [re.sub(r"[CD]", lambda m: c if m.group(0) == "C" else DECOY, s) for s in STATE_SHAPES]
    w = pathlib.Path(work) / "legb"
    (w / "app").mkdir(parents=True)
    (w / "tests").mkdir()
    (w / "tests" / "test_outputs.py").write_bytes((lane / GRADER_REL).read_bytes())
    (w / "states.json").write_text(json.dumps(states))
    (w / "grade.py").write_text(r45.GRADE_PY.replace('open(p, "w")', 'open(p, "w", newline="")'))
    (w / "predict.py").write_text(r45.PREDICT_PY)
    (w / "predictor.py").write_text(blocks[0])
    graded = r45.sandboxed(w, "grade.py", ["--bind", str(w / "app"), "/app", "--ro-bind", str(w / "tests"), "/tests"])
    try:
        pred = r45.sandboxed(w, "predict.py", ["--ro-bind", str(w / "predictor.py"), "/predictor.py"])
    except Exception as e:  # a predictor that crashes is a defect
        return False, f"predictor failed: {str(e)[:120]}"
    if len(graded) != len(states) or len(pred) != len(states):
        return False, "result length mismatch"
    dis = sum(1 for k in range(len(states)) if graded[k] != pred[k])
    npass = sum(graded)
    nfail = len(graded) - npass
    return (dis == 0 and npass >= 4 and nfail >= 4,
            f"states={len(states)} grader_pass={npass} grader_fail={nfail} disagree={dis}")


def leg_c(lane, alc):
    entry = (lane / ENTRY_REL).read_text()
    reg = {sid: (cells, line) for sid, cells, line in alc.parse_rows((lane / "corpus/SOURCES.md").read_text())}
    idx = alc.evidence_index(lane)
    n = bad = 0
    for m in SOURCE_LINE.finditer(entry):
        sid, rest = m.group(1), m.group(2)
        ranges = SRC_RANGE.findall(rest.split("—", 2)[-1] if "—" in rest else rest)
        if not ranges:
            continue
        row = reg.get(sid)
        caps = [r for h in alc.SHA_RE.findall(row[1]) for r in idx.get(h, [])] if row else []
        nl = len((lane / sorted(caps)[0]).read_bytes().decode("utf-8", "replace").splitlines()) if caps else 0
        for a, b in ranges:
            n += 1
            if not caps or int(b) > nl or int(a) > int(b):
                bad += 1
    er = ERRATA_HEAD.search(entry)
    marks = sum(1 for t in ERRATA_MARKS if er and t in er.group(1))
    return (bad == 0 and n > 0 and marks == len(ERRATA_MARKS),
            f"source_ranges={n} source_ranges_bad={bad} errata_marks={marks}/{len(ERRATA_MARKS)}")


def leg_d(lane):
    r = subprocess.run([sys.executable, str(lane / ALC_REL), "--selftest"], capture_output=True, text=True,
                       timeout=300)
    return r.returncode == 0, f"exit={r.returncode}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
    print(f"PINS total={len(PINS)} mismatched={len(mism)}" + (f" first={mism[0]}" if mism else ""))
    if ALC_REL in mism or R45_REL in mism:
        print("SETUP a pinned tool is not at its freeze digest", file=sys.stderr)
        print("PREDICATE C2 fail")
        return 1
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    alc = load(lane / ALC_REL, "kengaku_anchor_line_check")
    r45 = load(lane / R45_REL, "kengaku_r45_c2")
    defects = 0
    with tempfile.TemporaryDirectory(prefix="k46-c2-", dir=a.work) as work:
        for name, label, fn in (("A", "anchorline", lambda: leg_a(lane, alc)),
                                ("B", "predictor", lambda: leg_b(lane, r45, work)),
                                ("C", "entry", lambda: leg_c(lane, alc)),
                                ("D", "selftest", lambda: leg_d(lane))):
            try:
                ok, note = fn()
            except Exception as e:  # a leg that cannot run is a defect
                ok, note = False, f"error {type(e).__name__}: {str(e)[:160]}"
            defects += not ok
            print(f"{name} {label} {note} {'ok' if ok else 'DEFECT'}")
    good = defects == 0 and not mism
    print(f"checks=4 defects={defects + (1 if mism and not defects else 0)}")
    print(f"PREDICATE C2 {'pass' if good else 'fail'}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
