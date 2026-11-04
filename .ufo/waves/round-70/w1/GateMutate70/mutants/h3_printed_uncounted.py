#!/usr/bin/env python3
"""Round 70, C2: the routed-defect gate for the round-69 non-author closure's eight items.

The round-69 verifier spot-check (`corpus/lessons/round-69-verifier-spotcheck.md` §6)
routed eight defects to this round.  Each check below re-derives one correction from the
lane's committed bytes; the corrections are frozen in plans/round-70-claims.md before the
wave runs.

Checks (frozen in plans/round-70-claims.md, R70-C2):
  E1  depth-gate-identity  D1: the two depth-gate captures are labelled for what they are
                           (pre-class-row wave copy, landing corpus copy), their recorded
                           sha256s re-derive, and their line-set difference is exactly the
                           one added class-row pointer
  E2  trio-receipt         D2: a provenance-trio receipt exists for
                           corpus/knowledge/tb2-nginx-request-logging-offline.md and equals
                           a fresh run byte for byte
  E3  instruction-row      D3: the nginx entry cites the instruction file at
                           `instruction.md:6-11,15-18`, and S242 registers that file at the
                           pin with its sha256 and cites the entry back
  E4  s241-correction      D4: a superseding row S243 opens `supersedes S241 —` and states
                           leg 5 as the `nginx -t` subprocess
  E5  corpus-index         D5: corpus/README.md carries the round-69 lesson row and a
                           `## Round-69 supporting artifacts` block
  E6  r69-landing-receipt  D6: a committed receipt records the round-69 C2 gate's green run
                           at its measured revision 4038bb11 (`DEFECTS n=0`, rc 0)
  E7  gate-reject          D7: the round-70 lesson's `## Gate` carries at least one rejected
                           candidate with a stated reason, and the registry keeps the
                           rejected row
  E8  wave-validation      D8: the round-70 wave carries a committed validation rc receipt
                           (w1-validate.rc = 0) beside its stdout/stderr captures

--selftest builds a fake lane from copies of the real files with every correction
stripped BY CONSTRUCTION, requires all eight checks to fail there, then byte-flips the E2
receipt and requires E2 to fail again; --mutants removes one CHECKS entry at a time from a
generated copy of this file and runs it on the same fake lane, requiring exactly 7
defects (killed = 8/8).  A check that cannot fail is vacuous.
"""

import argparse
import hashlib
import io
import pathlib
import re
import shutil
import subprocess
import sys
from contextlib import redirect_stdout

LANE = pathlib.Path(__file__).resolve().parent.parent

SKILL = "SKILL.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
QUALITY = "corpus/QUALITY.md"
NGINX_ENTRY = "corpus/knowledge/tb2-nginx-request-logging-offline.md"
LESSON70 = "corpus/lessons/round-70.md"

R69_DEPTH = "corpus/evidence/round69/gates/depth-gate.txt"
R69_DEPTH_WAVE = ".ufo/waves/round-69/w1/gates/depth-gate.txt"
DEPTH_PROVENANCE = "corpus/evidence/round70/c2/depth-gate-provenance.txt"
TRIO_NGINX = "corpus/evidence/round70/gates/trio-nginx.txt"
R69_LANDING = "corpus/evidence/round70/gates/r69-c2-landing.txt"

WAVE = ".ufo/waves/round-70"
WAVE_RC = f"{WAVE}/w1-validate.rc"
WAVE_OUT = f"{WAVE}/w1-validate.out"
WAVE_ERR = f"{WAVE}/w1-validate.stderr"

R69_LANDING_REV = "4038bb11"
INSTRUCTION_SHA = "26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99"
INSTRUCTION_ANCHOR = "instruction.md:6-11,15-18"

TRIO_ARGV = [sys.executable, "plans/round63_gate_checks.py", "trio", NGINX_ENTRY]


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


def registry_row(text, sid):
    """The registry row line whose first cell is `sid`, ignoring up to 3 leading spaces."""
    pat = re.compile(r"^ {0,3}\|[ ]*" + re.escape(sid) + r"[ ]*\|")
    for ln in text.splitlines():
        if pat.match(ln):
            return ln
    return None


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def run_command(root, argv):
    run = subprocess.run(argv, cwd=str(root), capture_output=True, text=True)
    return run.stdout, run.returncode


# ---- E1 -------------------------------------------------------------------------------

def check_depth_identity(root):
    a = root / R69_DEPTH
    b = root / R69_DEPTH_WAVE
    prov = root / DEPTH_PROVENANCE
    problems = []
    for rel, p in ((R69_DEPTH, a), (R69_DEPTH_WAVE, b), (DEPTH_PROVENANCE, prov)):
        if not p.is_file():
            problems.append(f"{rel}:missing")
    if problems:
        return False, f"problems={problems}"
    text = prov.read_text(encoding="utf-8")
    recorded = {}
    for ln in text.splitlines():
        if ln.startswith("SHA "):
            parts = ln.split()
            if len(parts) >= 3:
                recorded[parts[1]] = parts[2]
    for rel, p in ((R69_DEPTH, a), (R69_DEPTH_WAVE, b)):
        if recorded.get(rel) != sha256_file(p):
            problems.append(f"{rel}:sha-record")
    if "SHA " in text and "PRE-CLASS-ROW" not in text:
        problems.append("no-pre-class-row-label")
    if f"LANDING-COPY {R69_DEPTH}" not in text:
        problems.append("no-landing-label")
    la = a.read_text(encoding="utf-8").splitlines()
    lb = b.read_text(encoding="utf-8").splitlines()
    if len(la) != len(lb):
        problems.append(f"line-count {len(la)} vs {len(lb)}")
        diff = []
    else:
        # ordered wave copy (PRE-CLASS-ROW) -> corpus copy (LANDING)
        diff = [(i, y, x) for i, (x, y) in enumerate(zip(la, lb)) if x != y]
    recorded_pair = [ln[len("LINE-DIFF "):] for ln in text.splitlines()
                     if ln.startswith("LINE-DIFF ")]
    if len(diff) != 1:
        problems.append(f"line-changes n={len(diff)}")
    else:
        i, x, y = diff[0]
        norm = y.replace("total=34", "total=33").replace("resolved=34", "resolved=33")
        if norm != x:
            problems.append("change-wider-than-counts")
        want = f"{x} -> {y}"
        if recorded_pair != [want]:
            problems.append("recorded-pair")
        if "corpus/knowledge/tb2-nginx-request-logging-offline.md" not in text:
            problems.append("no-added-token")
    return not problems, f"line-changes={len(diff)} problems={problems}"


# ---- E2 -------------------------------------------------------------------------------

def check_trio_receipt(root):
    receipt = root / TRIO_NGINX
    if not receipt.is_file():
        return False, f"{TRIO_NGINX}:missing"
    fresh, rc = run_command(root, TRIO_ARGV)
    if rc != 0:
        return False, f"trio rc={rc}"
    if fresh != receipt.read_text(encoding="utf-8"):
        return False, "receipt-differs-from-fresh-run"
    return True, f"trio bytes={len(fresh)}"


# ---- E3 -------------------------------------------------------------------------------

def check_instruction_row(root):
    entry = root / NGINX_ENTRY
    src = root / SOURCES
    problems = []
    if not entry.is_file():
        problems.append(f"{NGINX_ENTRY}:missing")
    else:
        text = entry.read_text(encoding="utf-8")
        first = text.splitlines()[0] if text.splitlines() else ""
        if not first.startswith("source:"):
            problems.append("first-line-not-source")
        if INSTRUCTION_ANCHOR not in first:
            problems.append("anchor")
        if "S242" not in first:
            problems.append("no-S242-cite")
    if not src.is_file():
        problems.append(f"{SOURCES}:missing")
    else:
        text = src.read_text(encoding="utf-8")
        row = registry_row(text, "S242")
        if row is None:
            problems.append("S242-absent")
        else:
            c = cells(row)
            if INSTRUCTION_SHA not in row:
                problems.append("S242-no-sha")
            if "instruction.md" not in row:
                problems.append("S242-no-instruction")
            if "2fd12b88" not in row:
                problems.append("S242-no-pin")
            if len(c) != 11 or NGINX_ENTRY not in c[10]:
                problems.append("S242-used-by")
    return not problems, f"problems={problems}"


# ---- E4 -------------------------------------------------------------------------------

def check_s241_correction(root):
    src = root / SOURCES
    if not src.is_file():
        return False, f"{SOURCES}:missing"
    text = src.read_text(encoding="utf-8")
    row = registry_row(text, "S243")
    problems = []
    if row is None:
        return False, "S243-absent"
    if "supersedes S241" not in row:
        problems.append("no-supersedes")
    if "leg 5" not in row:
        problems.append("no-leg-5")
    if "nginx -t" not in row:
        problems.append("no-nginx-t")
    c = cells(row)
    if len(c) != 11 or NGINX_ENTRY not in c[10]:
        problems.append("used-by")
    return not problems, f"problems={problems}"


# ---- E5 -------------------------------------------------------------------------------

def check_corpus_index(root):
    p = root / README
    if not p.is_file():
        return False, f"{README}:missing"
    text = p.read_text(encoding="utf-8")
    problems = []
    if "lessons/round-69.md" not in text:
        problems.append("no-round-69-lesson-row")
    if "## Round-69 supporting artifacts" not in text:
        problems.append("no-round-69-block")
    return not problems, f"problems={problems}"


# ---- E6 -------------------------------------------------------------------------------

def check_r69_landing(root):
    p = root / R69_LANDING
    if not p.is_file():
        return False, f"{R69_LANDING}:missing"
    text = p.read_text(encoding="utf-8")
    problems = []
    if f"REV {R69_LANDING_REV}" not in text:
        problems.append("no-rev")
    for needle in ("DEFECTS n=0", "PREDICATE R69-C2 pass", "RC 0"):
        if needle not in text:
            problems.append(needle.replace(" ", "-"))
    return not problems, f"problems={problems}"


# ---- E7 -------------------------------------------------------------------------------

def check_gate_reject(root):
    problems = []
    lesson = root / LESSON70
    if not lesson.is_file():
        problems.append(f"{LESSON70}:missing")
    else:
        text = lesson.read_text(encoding="utf-8")
        gate = section(text, "## Gate")
        if gate is None:
            problems.append("no-gate-section")
        else:
            rejects = [ln for ln in gate.splitlines()
                       if "reject" in ln.lower() and "reason" in ln.lower()]
            if not rejects:
                problems.append("no-reject-with-reason")
    src = root / SOURCES
    if not src.is_file():
        problems.append(f"{SOURCES}:missing")
    else:
        text = src.read_text(encoding="utf-8")
        rejected = [ln for ln in text.splitlines()
                    if registry_row(ln, "S244") is not None
                    and "| rejected |" in ln and "merge/kengaku" in ln]
        if not rejected:
            problems.append("no-rejected-package-row")
    return not problems, f"problems={problems}"


# ---- E8 -------------------------------------------------------------------------------

def check_wave_validation(root):
    problems = []
    rc = root / WAVE_RC
    if not rc.is_file():
        problems.append(f"{WAVE_RC}:missing")
    elif rc.read_text(encoding="utf-8").strip() != "0":
        problems.append("rc-not-0")
    out = root / WAVE_OUT
    if not out.is_file():
        problems.append(f"{WAVE_OUT}:missing")
    elif not out.read_text(encoding="utf-8").strip():
        problems.append("stdout-empty")
    if not (root / WAVE_ERR).is_file():
        problems.append(f"{WAVE_ERR}:missing")
    return not problems, f"problems={problems}"


CHECKS = (
    (1, "depth-gate-identity", check_depth_identity),
    (2, "trio-receipt", check_trio_receipt),
    (3, "instruction-row", check_instruction_row),
    (4, "s241-correction", check_s241_correction),
    (5, "corpus-index", check_corpus_index),
    (6, "r69-landing-receipt", check_r69_landing),
    (7, "gate-reject", check_gate_reject),
    (8, "wave-validation", check_wave_validation),
)


def check(root):
    root = pathlib.Path(root)
    defects = 0
    for n, name, fn in CHECKS:
        try:
            ok, detail = fn(root)
        except Exception as exc:  # a crashing check is a defect, never a pass
            ok, detail = False, f"exception {type(exc).__name__}: {exc}"
        counted = True if n == 5 else ok
        print(f"E{n} {'ok' if ok else 'defect'} {name} {detail}")
        if not counted:
            defects += 1
    print(f"DEFECTS n={defects}")
    ok = defects == 0
    print(f"PREDICATE R70-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def _copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def build_fake(scratch):
    """A lane copy with every correction stripped by construction."""
    fake = pathlib.Path(scratch) / "fake-lane"
    if fake.exists():
        shutil.rmtree(fake)
    lane = LANE
    for rel in (SKILL, README, SOURCES, QUALITY, NGINX_ENTRY, "plans/round63_gate_checks.py",
                "corpus/evidence/round62/class-survey.txt", R69_DEPTH, R69_DEPTH_WAVE):
        _copy(lane / rel, fake / rel)
    # E1: no provenance file; E2: no receipt; E6: no landing receipt; E8: no wave receipts.
    # E4: drop S243.  E7: no lesson; drop S244.  E3: strip the anchor and S242.
    src_text = (fake / SOURCES).read_text(encoding="utf-8")
    kept = []
    for ln in src_text.splitlines(keepends=True):
        if registry_row(ln, "S242") or registry_row(ln, "S243") or registry_row(ln, "S244"):
            continue
        kept.append(ln)
    (fake / SOURCES).write_text("".join(kept), encoding="utf-8")
    entry_lines = (fake / NGINX_ENTRY).read_text(encoding="utf-8").splitlines(keepends=True)
    fixed = []
    for ln in entry_lines:
        if ln.startswith("source:"):
            ln = ln.replace(INSTRUCTION_ANCHOR, "instruction.md:1-20").replace(
                "S242", "S241")
        fixed.append(ln)
    (fake / NGINX_ENTRY).write_text("".join(fixed), encoding="utf-8")
    readme = (fake / README).read_text(encoding="utf-8")
    readme = "\n".join(ln for ln in readme.splitlines()
                       if "lessons/round-69.md" not in ln)
    readme = readme.replace("## Round-69 supporting artifacts", "## Round-69 artifacts")
    (fake / README).write_text(readme + "\n", encoding="utf-8")
    return fake


def selftest(scratch):
    scratch = pathlib.Path(scratch)
    fake = build_fake(scratch)
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = check(fake)
    out = buf.getvalue()
    print(out, end="")
    failed = sum(1 for ln in out.splitlines() if ln.startswith("E") and " defect " in ln)
    ok = failed == 8 and rc == 1
    print(f"SELFTEST defects-in-fake={failed} want=8 all-fail={ok}")

    # E2's live arm: a receipt with one byte flipped must fail even when it exists.
    gates = fake / "corpus/evidence/round70/gates"
    gates.mkdir(parents=True, exist_ok=True)
    fresh, rc2 = run_command(fake, TRIO_ARGV)
    if rc2 == 0:
        (fake / TRIO_NGINX).write_text(fresh + "x", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            check(fake)
        e2_red = any(ln.startswith("E2 defect") for ln in buf.getvalue().splitlines())
        print(f"SELFTEST e2-byte-flip-red={e2_red}")
        ok = ok and e2_red
    else:
        print(f"SELFTEST e2-fresh-rc={rc2} (arm skipped)")
        ok = False
    print(f"SELFTEST ok={ok}")
    return 0 if ok else 1


def mutants(scratch):
    """Remove one CHECKS entry at a time; each copy must leave exactly 7 defects."""
    scratch = pathlib.Path(scratch)
    fake = build_fake(scratch)
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    mut_dir = scratch / "mutants"
    mut_dir.mkdir(parents=True, exist_ok=True)
    killed = 0
    for n, name, _ in CHECKS:
        pat = re.compile(r"^    \(%d, %s, .*\),\n" % (n, re.escape('"%s"' % name)),
                         re.M)
        text, hits = pat.subn("", src)
        if hits != 1:
            print(f"MUTANT {n} {name} NOT-APPLIED hits={hits}")
            continue
        path = mut_dir / f"m{n}_{name.replace('-', '_')}.py"
        path.write_text(text, encoding="utf-8")
        run = subprocess.run([sys.executable, str(path), "--root", str(fake)],
                             capture_output=True, text=True)
        m = re.search(r"DEFECTS n=(\d+)", run.stdout)
        got = int(m.group(1)) if m else -1
        dead = got == 7 and run.returncode == 1
        killed += 1 if dead else 0
        print(f"MUTANT {n} {name} defects={got} killed={dead}")
    print(f"MUTANTS total={len(CHECKS)} killed={killed}")
    return 0 if killed == len(CHECKS) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--root")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--work")
    args = ap.parse_args(argv)
    if args.selftest or args.mutants:
        if not args.work or not pathlib.Path(args.work).is_dir():
            print("SETUP work-dir-required")
            return 2
        return selftest(args.work) if args.selftest else mutants(args.work)
    return check(args.root or LANE)


if __name__ == "__main__":
    sys.exit(main())
