#!/usr/bin/env python3
"""Round-46 C3 counter (coverage): the pinned Terminal-Bench 2.0 `polyglot-c-py` grader admitted as a
knowledge package with an executed offline probe.

The graded artefact is a **program**: one file `/app/polyglot/main.py.c` that each of two toolchains must
execute — `python3 /app/polyglot/main.py.c N` and `gcc /app/polyglot/main.py.c -o /app/polyglot/cmain`.
`tests/test_outputs.py` at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6` asserts, in this
order, (a) `os.listdir("/app/polyglot") == ["main.py.c"]` exactly (`:17-20`), (b) that `gcc` succeeds with
`check=True` (`:23-25`), and (c) for each of `[(42, "267914296"), (10, "55"), (0, "0")]` (`:27`) that BOTH
`stdout.strip()` values equal the expected string (`:30-46`). Three fixed points, no other N, no timing, no
source inspection. That is a third grader class this lane executes: a dual-runtime *program* verdict, not a
constant compare (round 44) and not a line-membership compare of a constant in a text file (round 45).

Frozen predicate (same sentence in plans/round-46-claims.md §C3 and in the receipt label):
  C3 passes iff `python3 plans/round46_c3_verify.py --lane .` prints `checks=13 defects=0`, then
  `PREDICATE C3 pass`, exit 0, measured on a clean clone of the landing tip.

Order rule (QUALITY Q30, plans/round-46-claims.md §C3): before the stage-2 freeze the probe runs only
`--dry`/stage-check; no seat executes a graded case of this task and no seat runs `plans/pkg_gate.py --rerun`
on the package. This counter's `V2` runs the gate WITH `--rerun` (P10 = a fresh probe run byte-compared), so V2
is a post-stage-2 leg: it is never run by a wave-1 seat and the base/filler controls here never reach it.

Legs (each prints one line; a leg that cannot run is a defect, never a pass):

  V1  capture manifest: corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS lists exactly the eight
      captured files at their frozen digests and every file's bytes match.
  V2  package gate: plans/pkg-spec-r46.json and plans/pkg_gate.py at their freeze digests;
      `pkg_gate.py package --rerun --require-clean-tree` accepts the package.
  V3  anchor digests: each spec row has exactly one 11-cell registry row whose anchor carries exactly its
      own `sha256` pin.
  V4  receipt: CASE ids equal the frozen dry table in order; one consistent summary line; the `regrade
      cases=N differ=` line accounts for every `regrade=DIFF:` CASE (a re-graded end state is reported, never
      judged: this grader's own `gcc -o cmain` makes its second run fail, so the observed passes carry
      `regrade=DIFF:F` by design); every `match=NO` case id named in the entry; `match=yes` only where
      predicted == observed.
  V5  frozen probe: plans/polyglot_c_py_probe.py at its freeze digest and its `--dry` output byte-equal to
      the frozen dry table (itself at its freeze digest).
  V6  census: `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` exits 0.
  V7  requirement map: one `## Requirement map` row per frozen tag, label DERIVED from the receipt.
  V8  order (QUALITY Q30): `plans/order_check.py --lane <lane> --claims plans/round-46-claims.md
      --receipt <spec receipt>` exits 0 and prints `ORDER RESULT PASS`.
  V9  content consistency: `## Case table` equal to the receipt; every spec row id outside the `source:`
      line; PROVINCE.md names `polyglot-c-py` and the entry file on one line; README `## Frontier` names it.
  V10 mechanism: `## Mechanism` rows per receipt case citing a frozen DECISIVE line with a >=2-word
      verbatim quote.
  V11 held-out predictor (hardened, see below): the entry's `## Predictor` defines `predict(files, source)`
      -> bool over `/app/polyglot` (the listing before compilation and the text of `main.py.c`, or None when
      no readable regular file of that name exists). The counter builds fresh end states per run, runs the
      CAPTURED grader on each inside bubblewrap, runs `predict` on each in a second sandbox, and requires
      0 disagreements plus non-vacuity (>=8 grader passes and >=8 grader fails).
  V12 anchor-line rule, re-implemented (not imported from plans/anchor_line_check.py): every row the spec
      names cites `:N "quote"`, its capture resolves by digest inside the package's capture dir, the quote
      sits on line N, a first `<file>:<a>-<b>` range holds N and does not pass the file's end, and a
      `(K words)` count matches; a defective row is repaired only by a defect-free row whose `teaches`
      opens `supersedes S0NN —` (QUALITY Q34).
  V13 filler package: the committed do-nothing package under plans/filler46/ (a right-shaped entry, rows,
      spec, dry table and receipt that establish nothing) must be caught by the package's own content legs.
      `V13` runs V3/V4/V6/V7/V9/V10/V12 against the filler and requires at least three of the substantive
      content legs (V3, V4, V7, V9, V10, V12) to print DEFECT — a missing-file or digest defect alone is
      not a discriminator, so the filler is shaped correctly and its defects are semantic.

V11 hardening (carried from `R45CritV11Bypass`, whose four verdict-changing predictors passed the round-45
lint). The round-45 evidence is that a fixed public state set is memorizable three ways: a call-order-indexed
table, an integer/shift feature key, and a verbatim tuple. Here:
  1. the state set is generated per run from `os.urandom` (decoy literals, padding, extra-file names) and the
     order is shuffled, so no call index and no fixed feature key survives a re-run;
  2. the predictor block is source-linted at most 4000 bytes, with the round-45 token set plus `>>`/`<<`
     refused (a bit table needs a shift), `{`/`}` refused (a verdict table needs a dict/set literal), the
     tokens `open`, `os.`, `sys.modules`, `subprocess`, `socket`, `pathlib`, `io.`, `shutil`, `hashlib`,
     `eval(`, `exec(`, `compile(` and the introspection climbs `__class__`, `__subclasses__`,
     `__builtins__`, `__globals__`, `__import__`, `__dict__`, `__mro__`, `getattr` refused, and `import`
     allowed only as `import re` / `from re import ...` (a source analyser needs regex; `re` cannot read a
     file). Bare `__name__` and `sys.stderr` are *not* refused: the analyser must be able to match the
     source's own `if __name__ ==` guard and stderr channel, and neither token reaches a file or a module;
  3. the 4000-byte cap plus (2) refuses a verbatim tuple of the state sources;
  4. V11 prints only the disagreement COUNT, never the mismatching state labels (round-45 section 5b).
The named limit stands: a predictor that open-codes the verdict table in a form small enough to pass review,
or a wrong-but-close heuristic that happens to agree on this family, is not distinguishable from a reader by
sample equivalence alone; non-author review of the admitted block stays part of admission.

Ground truth is never stored here: the state generator emits sources whose printed values it chooses, and
the verdict of every state is produced by executing the CAPTURED grader at run time.

`--filler` substitutes the plans/filler46/ package for the package under test, so this counter's rejection
of it is measurable before the real package exists (the three stage-2 controls run this way: base tree,
filler package, echo receipt). `--work DIR` is created if absent; the sandbox scratch lives inside it.
Exit 0 pass, 1 fail, 2 setup error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import random
import re
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round46/tb2-polyglot-c-py"
# The eight captures of the pinned task, digests measured by the round-46 capture seat
# (.ufo/waves/round-46/w1/R46ExecC3Capture.md §2) and re-checkable with `sha256sum -c SHA256SUMS`.
CAPTURES = {
    "Dockerfile": "2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a",
    "README.md": "591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881",
    "gitignore": "9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953",
    "instruction.md": "a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96",
    "solve.sh": "e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0",
    "task.toml": "d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea",
    "test.sh": "4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334",
    "test_outputs.py": "b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec",
}

PENDING = "<PIN:stage-2>"
SPEC_REL = "plans/pkg-spec-r46.json"
SPEC_SHA256 = PENDING                     # stage-2 pin: sha256 of plans/pkg-spec-r46.json
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"  # round-45 bytes, unedited
PROBE_REL = "plans/polyglot_c_py_probe.py"
PROBE_SHA256 = PENDING                    # stage-2 pin
DRY_REL = "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
DRY_SHA256 = PENDING                      # stage-2 pin
ORDER_REL = "plans/order_check.py"
CLAIMS_REL = "plans/round-46-claims.md"
TASK = "polyglot-c-py"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
FILLER_SPEC = "plans/filler46/pkg-spec-filler.json"
FILLER_DIR = "plans/filler46"
SUBSTANTIVE = ("V3", "V4", "V7", "V9", "V10", "V12")
FILLER_LEGS = ("V3", "V4", "V6", "V7", "V9", "V10", "V12")

SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")
REGRUN = re.compile(r"^regrade cases=(\d+) differ=(\d+)$")
MAP_ROW = re.compile(r"^\|\s*`instruction\.md:(\d+)`\s*\|\s*`([a-z0-9-]+)`\s*\|\s*(enforced|unenforced|partly)\s*\|(.*)\|\s*$")
CASE_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|\s*([PF-]+)\s*\|\s*(pass|fail)\s*\|.*\|\s*$")
MECH_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|\s*`([A-Za-z0-9_./-]+):(\d+)`\s*\|\s*“(.+?)”\s*\|\s*$")
TAG_LINE = re.compile(r"^TAG (\S+) (\S+)$")

# ---- V12's own anchor-line rule (re-implemented from the semantics of plans/anchor_line_check.py;
# that module is not imported, so a change to it cannot change what this counter certifies) ----------
AROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
AQUOTE = re.compile(r':(\d+)\s+"(.*?)"(?=\s*(?:\(\d+\s+words?\)|[;,]|$|\s+and\s))')
AWORDS = re.compile(r'\s*\((\d+)\s+words?\)')
ARANGE = re.compile(r'[\w./-]+\.[A-Za-z0-9]+:(\d+)-(\d+)')
ASHA = re.compile(r'sha256\s+`?([0-9a-f]{64})\b')
ASUPERSEDES = re.compile(r'^\s*supersedes\s+([^—]*)—')


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def ready(pin):
    return bool(pin) and not pin.startswith("<")


def text_or_none(p):
    try:
        return pathlib.Path(p).read_text()
    except (OSError, UnicodeDecodeError):
        return None


# ---- the package under test: the real spec tree, or the filler control package ---------------------

class Pkg:
    """Every path and pin a leg reads, resolved once. `pinned` is True only for the real package."""

    def __init__(self, lane, spec, spec_path, entry, receipt, dry, capdir, registry, readme,
                 pins=None, pinned=False, probe=None, claims=CLAIMS_REL, name="package"):
        self.lane = lane
        self.spec = spec
        self.spec_path = spec_path
        self.entry = entry
        self.receipt = receipt
        self.dry = dry
        self.capdir = capdir
        self.registry = registry
        self.readme = readme
        self.pins = pins
        self.pinned = pinned
        self.probe = probe
        self.claims = claims
        self.name = name

    def rel(self, path):
        try:
            return pathlib.Path(path).resolve().relative_to(self.lane).as_posix()
        except ValueError:
            return str(path)


def real_pkg(lane):
    if not ready(SPEC_SHA256):
        raise ValueError("spec pin pending: SPEC_SHA256 is a stage-2 placeholder")
    if sha256(lane / SPEC_REL) != SPEC_SHA256:
        raise ValueError(f"{SPEC_REL} is not at its freeze digest")
    s = json.loads((lane / SPEC_REL).read_text())
    return Pkg(lane, s, lane / SPEC_REL, lane / s["entry"], lane / s["receipt"], lane / DRY_REL,
               lane / s.get("capture_dir", CAP), lane / s.get("sources", "corpus/SOURCES.md"),
               lane / s["readme"], pins=CAPTURES, pinned=True, probe=lane / PROBE_REL)


def filler_pkg(lane):
    p = lane / FILLER_SPEC
    if not p.is_file():
        raise ValueError(f"{FILLER_SPEC} absent (the committed filler control package is missing)")
    s = json.loads(p.read_text())
    return Pkg(lane, s, p, lane / s["entry"], lane / s["receipt"], lane / s["dry"],
               lane / s["capture_dir"], lane / s["sources"], lane / s["readme"],
               pins=None, pinned=False, probe=None, claims=s.get("claims", CLAIMS_REL), name="filler")


# ---- legs ----------------------------------------------------------------------------------------

def manifest(capdir):
    text = text_or_none(pathlib.Path(capdir) / "SHA256SUMS")
    if text is None:
        return None, None
    listed, bad = {}, []
    for line in text.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([0-9a-f]{64})\s+\*?(\S+)$", line.strip())
        if not m:
            bad.append(line.strip()[:40])
            continue
        listed[m.group(2)] = m.group(1)
    return listed, bad


def v1(pkg):
    listed, bad = manifest(pkg.capdir)
    if listed is None:
        return False, f"manifest absent: {pkg.rel(pkg.capdir)}/SHA256SUMS"
    if bad:
        return False, f"unparsed manifest lines={bad[:2]}"
    want = pkg.pins if pkg.pins is not None else listed
    wrong = [n for n, d in want.items() if listed.get(n) != d or sha256(pathlib.Path(pkg.capdir) / n) != d]
    extra = sorted(set(listed) - set(want))
    return not wrong and not extra, f"listed={len(listed)} wrong={wrong or 0} extra={extra or 0}"


def v2(lane, pkg, work):
    if not pkg.pinned:
        return False, "filler mode: the gate is not run on the control package"
    if sha256(lane / GATE_REL) != GATE_SHA256:
        return False, "gate not at its round-45 freeze digest"
    s = dict(pkg.spec)
    s["receipt_sha256"] = sha256(pkg.receipt) or "absent"
    eff = pathlib.Path(work) / "pkg-spec-r46-effective.json"
    eff.write_text(json.dumps(s))
    # P10 picks its interpreter by `import Bio`; host python3 has none, so a bare run would fetch numpy +
    # biopython over the network and provision a managed CPython under ~/.cache/uv. The package's probe needs
    # neither, so a stub Bio on PYTHONPATH keeps the gate on host python3 and TMPDIR inside --work keeps its
    # scratch inside the envelope.
    stub = pathlib.Path(work) / "stubbio" / "Bio"
    stub.mkdir(parents=True, exist_ok=True)
    (stub / "__init__.py").write_text('version = "1.85"\n')
    env = dict(os.environ, TMPDIR=str(work),
               PYTHONPATH=str(stub.parent) + ((":" + os.environ["PYTHONPATH"]) if os.environ.get("PYTHONPATH") else ""))
    r = subprocess.run([sys.executable, str(lane / GATE_REL), "package", "--root", str(lane), "--spec", str(eff),
                        "--rerun", "--require-clean-tree"], capture_output=True, text=True, timeout=1800, env=env)
    for line in r.stdout.splitlines():
        print("    gate: " + line)
    return r.returncode == 0, f"spec=frozen gate=frozen gate_exit={r.returncode}"


def registry_rows(pkg):
    out = {}
    for line in (text_or_none(pkg.registry) or "").splitlines():
        m = SOURCE_ROW.match(line)
        if m:
            out.setdefault(m.group(1), []).append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def v3(pkg):
    reg, bad = registry_rows(pkg), []
    for sid, row in pkg.spec["rows"].items():
        found = reg.get(sid, [])
        if len(found) != 1 or len(found[0]) != 11:
            bad.append(f"{sid}:row")
            continue
        toks = re.findall(r"sha256\s+`?([0-9a-f]{64})", found[0][5])
        if toks != [row["sha256"]]:
            bad.append(f"{sid}:anchor_digest")
    return not bad, f"rows={len(pkg.spec['rows'])} bad={bad or 0}"


def dry_table(pkg):
    text = text_or_none(pkg.dry)
    if text is None:
        raise ValueError(f"dry table absent: {pkg.rel(pkg.dry)}")
    tags, cases = {}, []
    for line in text.splitlines():
        m = TAG_LINE.match(line.strip())
        if m:
            tags[m.group(1)] = m.group(2)
            continue
        p = line.split()
        if p and p[0] == "CASE":
            cases.append(p[1])
    return tags, cases


def receipt_cases(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=(pass|fail) observed=(pass|fail) .*?\bviolates=(\S*)", line)
        if m:
            out[m.group(1)] = (m.group(3), set(filter(None, m.group(4).split(","))))
    return out


def v4(pkg):
    try:
        text = (pkg.receipt).read_text()
        entry = (pkg.entry).read_text()
        _tags, frozen_ids = dry_table(pkg)
    except OSError:
        return False, "receipt, entry or frozen dry table absent"
    cases = [l for l in text.splitlines() if l.startswith("CASE ")]
    ids = [l.split()[1] for l in cases]
    parsed = receipt_cases(text)
    no = [l.split()[1] for l in cases if " match=NO " in l]
    summ = [SUMMARY.match(l) for l in text.splitlines() if SUMMARY.match(l)]
    bad = []
    if ids != frozen_ids or len(parsed) != len(ids):
        bad.append("case ids differ from the frozen table")
    if len(summ) != 1:
        bad.append("summary line count != 1")
    else:
        n, p, f, m = map(int, summ[0].groups())
        cp = sum(1 for o, _v in parsed.values() if o == "pass")
        cf = sum(1 for o, _v in parsed.values() if o == "fail")
        if not (n == len(frozen_ids) and p + f == n and p == cp and f == cf and m == len(no)):
            bad.append("summary disagrees with the CASE lines")
    # the receipt's own re-grade line must account for every `regrade=DIFF:` CASE (the probe reports, and does
    # not judge, a re-graded end state: polyglot-c-py's own `gcc -o cmain` makes the second grade fail, so all
    # seven observed passes carry `regrade=DIFF:F` by design - differ=7 is consistent, differ=0 would not be)
    reg = [REGRUN.match(l) for l in text.splitlines() if REGRUN.match(l)]
    diff_cases = [l.split()[1] for l in cases if re.search(r" regrade=DIFF:", l)]
    if len(reg) != 1:
        bad.append("regrade summary line count != 1")
    elif not (int(reg[0].group(1)) == len(ids) and int(reg[0].group(2)) == len(diff_cases)):
        bad.append(f"regrade line {reg[0].group(1)}/{reg[0].group(2)} vs CASE lines {len(ids)}/{len(diff_cases)}")
    unnamed = [c for c in no if f"`{c}`" not in entry]
    if unnamed:
        bad.append(f"mismatch cases not named in the entry: {unnamed}")
    # `match=yes` asserts predicted == observed; a line that claims a match while the two differ is a defect
    false_match = [l.split()[1] for l in cases
                   if " match=yes " in l and not re.search(r" predicted=(pass|fail) observed=\1 ", l)]
    if false_match:
        bad.append(f"match=yes on a mismatching case: {false_match}")
    return not bad, f"cases={len(ids)} mismatches_named={len(no) - len(unnamed)}/{len(no)} bad={bad or 0}"


def v5(lane, pkg):
    if not pkg.pinned:
        return False, "filler mode: no probe is pinned for the control package"
    if not ready(PROBE_SHA256) or not ready(DRY_SHA256):
        return False, "probe/dry pins pending (stage-2 placeholders)"
    if sha256(lane / PROBE_REL) != PROBE_SHA256 or sha256(pkg.dry) != DRY_SHA256:
        return False, "probe or dry table not at its freeze digest"
    r = subprocess.run([sys.executable, str(lane / PROBE_REL), "--lane", str(lane), "--dry"],
                       capture_output=True, text=True, timeout=120)
    same = r.returncode == 0 and r.stdout == pkg.dry.read_text()
    return same, f"probe=frozen dry_byte_equal={same}"


def v6(pkg):
    r = subprocess.run([CENSUS, "validate", "--file", str(pkg.registry)],
                       capture_output=True, text=True, timeout=300)
    return r.returncode == 0, f"census_exit={r.returncode} registry={pkg.rel(pkg.registry)}"


def derive(verdicts):
    if verdicts == {"fail"}:
        return "enforced"
    if verdicts == {"pass"}:
        return "unenforced"
    return "partly"


def v7(pkg):
    tags, _ids = dry_table(pkg)
    try:
        text = pkg.receipt.read_text()
        entry = pkg.entry.read_text()
    except OSError:
        return False, "receipt or entry absent"
    parsed = receipt_cases(text)
    sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    if not sec:
        return False, "no '## Requirement map' section"
    seen, bad = {}, []
    for line in sec.group(1).splitlines():
        m = MAP_ROW.match(line)
        if not m:
            if line.startswith("|") and "instruction.md:" in line:
                bad.append(f"unparsed row {line[:50]!r}")
            continue
        ln, tag, label, rest = m.group(1), m.group(2), m.group(3), m.group(4)
        seen[tag] = seen.get(tag, 0) + 1
        if tag not in tags:
            bad.append(f"{tag}: not a frozen tag")
            continue
        if tags[tag] != f"instruction.md:{ln}":
            bad.append(f"{tag}: line {ln} is not the frozen {tags[tag]}")
        violating = {cid: obs for cid, (obs, v) in parsed.items() if tag in v}
        if not violating:
            bad.append(f"{tag}: no receipt case violates it")
            continue
        want = derive(set(violating.values()))
        if label != want:
            bad.append(f"{tag}: labelled {label}, receipt derives {want}")
        cited = re.findall(r"`([a-z0-9_-]+)`", rest)
        if not cited or any(c not in violating for c in cited):
            bad.append(f"{tag}: cites no case or a case that does not violate it")
    missing = sorted(set(tags) - set(seen))
    dup = sorted(t for t, n in seen.items() if n > 1)
    if missing or dup:
        bad.append(f"tags missing={missing or 0} duplicated={dup or 0}")
    return not bad, f"rows={sum(seen.values())} tags={len(tags)} bad={bad or 0}"


def v8(lane, pkg):
    r = subprocess.run([sys.executable, str(lane / ORDER_REL), "--lane", str(lane), "--claims", pkg.claims,
                        "--receipt", pkg.rel(pkg.receipt)], capture_output=True, text=True, timeout=300)
    passed = r.returncode == 0 and "ORDER RESULT PASS" in r.stdout.splitlines()
    return passed, f"order_exit={r.returncode} result={'PASS' if passed else 'not-PASS'}"


def v9(pkg):
    try:
        text = pkg.receipt.read_text()
        entry = pkg.entry.read_text()
        province = (pkg.lane / "PROVINCE.md").read_text()
        readme = pkg.readme.read_text()
    except OSError:
        return False, "receipt, entry, PROVINCE.md or README absent"
    want = []
    for line in text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF-]+) ", line)
        if m:
            want.append((m.group(1), m.group(3), m.group(2)))
    bad = []
    sec = re.search(r"^## Case table\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    got = [CASE_ROW.match(l).groups() for l in sec.group(1).splitlines() if CASE_ROW.match(l)] if sec else []
    if not sec:
        bad.append("no '## Case table' section")
    elif not want or got != want:
        bad.append(f"case table rows={len(got)} receipt cases={len(want)} equal={got == want}")
    body = "\n".join(l for l in entry.splitlines() if not l.startswith("source:"))
    missing = [sid for sid in pkg.spec["rows"] if sid not in body]
    if missing:
        bad.append(f"row ids absent outside source lines: {missing}")
    name = pathlib.PurePosixPath(pkg.spec["entry"]).name
    if not any(TASK in l and name in l for l in province.splitlines()):
        bad.append("PROVINCE.md names the task and the entry on no line")
    fr = re.search(r"^## Frontier\n(.*?)(?=^## |\Z)", readme, re.S | re.M)
    if not fr or TASK not in fr.group(1):
        bad.append("README ## Frontier does not name the task")
    return not bad, f"case_rows={len(got)}/{len(want)} bad={bad or 0}"


# V10: the source lines that decide each frozen case (capture name -> 1-based line numbers), keyed by the
# probe's frozen case ids (round-46: 18 ids, reported by the spec seat). Stage-2 pin: the L1 re-reads these from
# the frozen captures against the probe's frozen case table; a case id present in that table but absent here is a
# DEFECT, never a pass.
DECISIVE = {
    "nop": {"test_outputs.py": (17, 18)},
    "oracle-solve-sh": {"solve.sh": (11, 12, 52)},
    "lookup-table": {"test_outputs.py": (27, 44)},
    "python-only": {"test_outputs.py": (24, 30)},
    "c-only": {"test_outputs.py": (30, 34, 37)},
    "extra-file": {"test_outputs.py": (17, 18)},
    "leftover-cmain": {"test_outputs.py": (17, 18)},
    "wrong-value": {"test_outputs.py": (44,)},
    "trailing-ws": {"test_outputs.py": (36, 43, 44)},
    "nonzero-exit": {"test_outputs.py": (30, 34, 37, 41)},
    "stderr-noise": {"test_outputs.py": (36, 43)},
    "n-parsed-differently": {"test_outputs.py": (27, 31)},
    "compile-warning": {"test_outputs.py": (24,)},
    "regrade-same-state": {"test_outputs.py": (27, 44)},
    "empty-file": {"test_outputs.py": (17, 18)},
    "dir-in-place": {"test_outputs.py": (18, 24)},
    "crlf-source": {"test_outputs.py": (24, 31)},
    "value-plus-line": {"test_outputs.py": (36, 43, 44)},
}
# DECISIVE's capture→line numbers are read off the captures pinned in CAPTURES.


def norm(t):
    return " ".join(t.split())


def v10(pkg):
    try:
        text = pkg.receipt.read_text()
        entry = pkg.entry.read_text()
    except OSError:
        return False, "receipt or entry absent"
    _tags, frozen_ids = dry_table(pkg)
    if sorted(DECISIVE) != sorted(frozen_ids):
        return False, "DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)"
    want = [l.split()[1] for l in text.splitlines() if l.startswith("CASE ")]
    sec = re.search(r"^## Mechanism\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    if not sec:
        return False, "no '## Mechanism' section"
    got = [MECH_ROW.match(l).groups() for l in sec.group(1).splitlines() if MECH_ROW.match(l)]
    bad = []
    if [g[0] for g in got] != want or not want:
        bad.append(f"mechanism rows={len(got)} receipt cases={len(want)} ids_equal={[g[0] for g in got] == want}")
    for cid, cap, line, quote in got:
        allowed = DECISIVE.get(cid, {}).get(cap, ())
        if int(line) not in allowed:
            bad.append(f"{cid}:{cap}:{line} not decisive")
            continue
        if pkg.pins is not None and cap in pkg.pins and sha256(pathlib.Path(pkg.capdir) / cap) != pkg.pins[cap]:
            bad.append(f"{cid}:{cap} capture not pinned")
            continue
        lines = text_or_none(pathlib.Path(pkg.capdir) / cap)
        if lines is None:
            bad.append(f"{cid}:{cap} capture unreadable")
            continue
        body = lines.splitlines()
        q = norm(quote)
        if len(q.split()) < 2 or int(line) > len(body) or q not in norm(body[int(line) - 1]):
            bad.append(f"{cid}:{cap}:{line} quote not on the line")
    return not bad, f"mechanism_rows={len(got)}/{len(want)} bad={bad or 0}"


def v12(pkg):
    """The package's rows under the line/range/words rule, with a digest-resolved capture."""
    rows = []
    for line in (text_or_none(pkg.registry) or "").splitlines():
        m = AROW.match(line)
        if m:
            rows.append((m.group(1), [c.strip() for c in line.strip().strip("|").split("|")], line))
    by_id = {}
    for sid, cells, line in rows:
        by_id.setdefault(sid, []).append((cells, line))
    idx = {}
    for f in sorted(pathlib.Path(pkg.capdir).iterdir()) if pathlib.Path(pkg.capdir).is_dir() else []:
        if f.is_file():
            idx.setdefault(sha256(f), []).append(f.name)
    info, bad = {}, []
    for sid, row in pkg.spec["rows"].items():
        found = by_id.get(sid, [])
        if len(found) != 1 or len(found[0][0]) != 11:
            bad.append(f"{sid}:row")
            continue
        cells, line = found[0]
        anchor = cells[5]
        quotes = list(AQUOTE.finditer(anchor))
        if not quotes:
            bad.append(f"{sid}:no_line_cited_quote")
            continue
        digests = ASHA.findall(line)
        names = idx.get(row["sha256"], [])
        if digests != [row["sha256"]] or names != [row["capture"]]:
            bad.append(f"{sid}:capture_unresolved capture={names or 0}")
            info[sid] = {"defects": ["capture_unresolved"], "supersedes": ASHA_SUP(cells)}
            continue
        body = (pathlib.Path(pkg.capdir) / row["capture"]).read_bytes().decode("utf-8", "replace")
        lines = body.split("\n")
        nlines = len(body.splitlines())
        rng = ARANGE.search(anchor)
        defects = []
        for m in quotes:
            n, q = int(m.group(1)), m.group(2).replace('\\"', '"')
            if not (1 <= n <= len(lines)) or q not in lines[n - 1]:
                defects.append("line")
            if rng:
                a, b = int(rng.group(1)), int(rng.group(2))
                if b > nlines or not (a <= n <= b):
                    defects.append("range")
            w = AWORDS.match(anchor, m.end())
            if w and int(w.group(1)) != len(q.split()):
                defects.append("words")
        info[sid] = {"defects": defects, "supersedes": ASHA_SUP(cells)}
        if defects:
            bad.append(f"{sid}:{','.join(sorted(set(defects)))}")
    repaired_by = {}
    for sid, d in info.items():
        if not d["defects"]:
            for old in d["supersedes"]:
                repaired_by.setdefault(old, sid)
    live = [s for s, d in info.items() if d["defects"] and s not in repaired_by]
    return not live, (f"rows={len(pkg.spec['rows'])} defective={len(bad)} live={len(live)}"
                      + (f" first={bad[0]}" if bad else ""))


def ASHA_SUP(cells):
    teaches = cells[6] if len(cells) >= 11 else ""
    m = ASUPERSEDES.match(teaches)
    return re.findall(r"S\d{3,}", m.group(1)) if m else []


# ---- V11: held-out predictor over generated end states ------------------------------------------

GRADER = "test_outputs.py"
MAIN = "main.py.c"
GRADER_FUNC = "test_fibonacci_polyglot"
EXPECTED = {"42": "267914296", "10": "55", "0": "0"}
POLY = '''#include <stdio.h>
#define polyglot_begin /*
import sys


def emit(k):
@@PY@@

if __name__ == "__main__":
    k = int(sys.argv[1])
@@CALL@@
    sys.exit(0)
"""
#define polyglot_mid */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    unsigned long n = strtoul(argv[1], NULL, 10);
@@C@@
    return 0;
}

#define polyglot_tail """
'''
PY_OK = "    if k == 42:\n        return 267914296\n    if k == 10:\n        return 55\n    return 0"
C_OK = ('    if (n == 42) printf("%llu\\n", 267914296UL);\n'
        '    else if (n == 10) printf("%llu\\n", 55UL);\n'
        '    else printf("%llu\\n", 0UL);')
PY_CALL = "    print(emit(k))"
PY_SYNTAX_ERROR = "    if k == 42\n        return 267914296\n    return 0"
PRED_SECTION = re.compile(r"^## Predictor\n(.*?)(?=^## |\Z)", re.S | re.M)
PRED_BLOCK = re.compile(r"^```python\n(.*?)^```\s*$", re.S | re.M)
PRED_LINT_TOKENS = ("{", "}", ">>", "<<", "open", "os.", "sys.modules", "subprocess", "socket", "pathlib",
                    "io.", "shutil", "hashlib", "sha256", "md5", "eval(", "exec(", "compile(",
                    "__class__", "__subclasses__", "__builtins__", "__globals__", "__import__", "__dict__",
                    "__mro__", "getattr", "globals", "locals", "states", ".json")
PRED_MAX_BYTES = 4000
IMPORT_OK = re.compile(r"^(?:import re|from re import [A-Za-z_, ]+)$")
BWRAP = "/usr/bin/bwrap"
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
SANDBOX_ENV = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
               "PYTHONDONTWRITEBYTECODE": "1"}


def lint_block(text):
    """A verdict table needs a dict/set literal, a bit shift, or a file read; a verbatim tuple needs bytes.

    `print(` is NOT refused: a source analyser must be able to match the source's own `print(` call, and the
    predict sandbox runs strictly after grading with no shared channel, so printing cannot leak a verdict.
    """
    hits = sorted({t for t in PRED_LINT_TOKENS if t in text})
    for line in text.splitlines():
        s = line.strip()
        if (s.startswith("import ") or s.startswith("from ")) and not IMPORT_OK.match(s):
            hits.append("import")
    if len(text.encode()) > PRED_MAX_BYTES:
        hits.append(f">{PRED_MAX_BYTES}bytes")
    return sorted(set(hits))


def polyglot(py_inner=PY_OK, py_call=PY_CALL, c_body=C_OK, eol="\n", tail=True):
    text = (POLY.replace("@@PY@@", py_inner).replace("@@CALL@@", py_call).replace("@@C@@", c_body))
    if eol != "\n":
        text = text.replace("\n", eol)
    if not tail:
        text = text.rstrip("\r\n")
    return text


def states():
    """Fresh end states per run (values, padding, names and order drawn from os.urandom)."""
    rng = random.Random(int.from_bytes(os.urandom(8), "big"))
    decoy_k = [rng.randrange(100, 900) for _ in range(3)]
    decoy_v = [rng.randrange(2, 99) for _ in range(3)]
    decoy_py = "    if k == %d:\n        return %d\n" % (decoy_k[0], decoy_v[0])
    banner = "    # state %s\n" % "".join(rng.choice("abcdefghijkmnpqrstuvwxyz") for _ in range(10))
    pad = " " * rng.randrange(1, 4)
    extra_name = "aux%s.txt" % "".join(rng.choice("0123456789abcdef") for _ in range(6))
    wrong42_py = PY_OK.replace("return 267914296", "return 267914297")
    wrong10_c = C_OK.replace("55UL", "56UL")
    three_literal = ("    if k == 42:\n        return 267914296\n    if k == 10:\n        return 55\n"
                     "    return 0")
    out = []

    def add(kind, files, source, dirs=()):
        out.append({"kind": kind, "files": list(files), "source": source, "dirs": list(dirs)})

    def mk(py_inner=PY_OK, py_call=PY_CALL, **kw):
        return polyglot(banner + py_inner, py_call, **kw)

    for _ in range(3):
        add("literal-ok", [MAIN], mk(decoy_py + three_literal))
        add("literal-ok-padded", [MAIN],
            mk(PY_OK, "    print(%semit(k)%s)" % (pad, pad),
                     c_body=C_OK.replace('printf("%llu\\n", 267914296UL)', 'printf(" %llu \\n", 267914296UL)')))
        add("literal-ok-trailing", [MAIN], mk(PY_OK, "    print(emit(k), end=\"\\n\\n\")"))
        add("literal-ok-crlf-source", [MAIN], mk(PY_OK, eol="\r\n"))
        add("literal-ok-no-eof-newline", [MAIN], mk(PY_OK, tail=False))
        add("wrong42", [MAIN], mk(wrong42_py))
        add("wrong10", [MAIN], mk(PY_OK, c_body=wrong10_c))
        add("zero-ignore-k", [MAIN], mk("    return 0", c_body='    printf("%llu\\n", 0UL);'))
        add("stderr-py", [MAIN], mk(PY_OK, "    print(emit(k), file=sys.stderr)"))
        add("stderr-c", [MAIN], mk(PY_OK, c_body=C_OK.replace("printf", "fprintf(stderr, ").replace(
            ");", "));")))
        add("float-py", [MAIN], mk(PY_OK, '    print("%d.0" % emit(k))'))
        add("float-c", [MAIN], mk(PY_OK, c_body='    printf("%.1f\\n", (double)267914296);\n'
                                                   '    printf("%.1f\\n", (double)55);\n'
                                                   '    printf("%.1f\\n", 0.0);'))
        add("no-print-py", [MAIN], mk(PY_OK, "    pass"))
        add("no-print-c", [MAIN], mk(PY_OK, c_body="    ;"))
        add("extra-file", [MAIN, extra_name], mk(PY_OK))
        add("stale-cmain", [MAIN, "cmain"], mk(PY_OK))
        add("wrong-name", ["main.py"], mk(PY_OK))
        add("dir-main", [MAIN], None, dirs=(MAIN,))
        add("c-syntax-error", [MAIN], mk(PY_OK, c_body='    printf("%llu\\n", );'))
        add("py-syntax-error", [MAIN], mk(PY_SYNTAX_ERROR))
    rng.shuffle(out)
    return out


GRADE_PY = r'''
import contextlib, importlib.util, io, json, os, shutil, sys
states = json.load(open("/states.json"))
ap = "/app/polyglot"
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
res = []
for st in states:
    shutil.rmtree(ap, ignore_errors=True)
    os.makedirs(ap)
    for d in st["dirs"]:
        os.makedirs(os.path.join(ap, d))
    if st["source"] is not None:
        with open(os.path.join(ap, "main.py.c"), "w", newline="") as f:
            f.write(st["source"])
    for name in st["files"]:
        p = os.path.join(ap, name)
        if not os.path.exists(p):
            with open(p, "w") as f:
                f.write("")
    ok = True
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            getattr(mod, TEST_FUNC)()
    except BaseException:
        ok = False
    res.append(ok)
print(json.dumps(res))
'''.replace("TEST_FUNC", repr(GRADER_FUNC))

PREDICT_PY = r'''
import json
states = json.load(open("/states.json"))
ns = {}
exec(compile(open("/predictor.py").read(), "predictor", "exec"), ns)
print(json.dumps([bool(ns["predict"](f, s)) for f, s in states]))
'''


def sandboxed(work, script, extra):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--ro-bind", str(work / "states.json"), "/states.json", "--ro-bind", str(work / script), "/run.py"]
    argv += extra + ["/usr/bin/python3", "/run.py"]
    r = subprocess.run(argv, env=SANDBOX_ENV, capture_output=True, text=True, timeout=1800,
                       stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        raise RuntimeError(f"{script} exit={r.returncode}: {r.stderr.strip()[-300:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def v11(pkg, work=None):
    try:
        entry = pkg.entry.read_text()
    except OSError:
        return False, "entry absent"
    grader = pathlib.Path(pkg.capdir) / GRADER
    if sha256(grader) != CAPTURES[GRADER]:
        return False, "grader capture not at its frozen digest"
    sec = PRED_SECTION.search(entry)
    blocks = PRED_BLOCK.findall(sec.group(1)) if sec else []
    if len(blocks) != 1:
        return False, f"'## Predictor' needs exactly one python block (found {len(blocks)})"
    lint = lint_block(blocks[0])
    if lint:
        return False, f"predictor lint tokens present: {','.join(lint)}"
    work = pathlib.Path(work or tempfile.mkdtemp(prefix="k46-c3-v11-")) / "v11"
    (work / "app").mkdir(parents=True, exist_ok=True)
    (work / "tests").mkdir(exist_ok=True)
    (work / "tests" / GRADER).write_bytes(grader.read_bytes())
    st = states()
    (work / "states.json").write_text(json.dumps(st))
    (work / "public.json").write_text(json.dumps([[s["files"], s["source"]] for s in st]))
    (work / "grade.py").write_text(GRADE_PY)
    (work / "predict.py").write_text(PREDICT_PY)
    (work / "predictor.py").write_text(blocks[0])
    graded = sandboxed(work, "grade.py", ["--bind", str(work / "app"), "/app",
                                          "--ro-bind", str(work / "tests"), "/tests"])
    (work / "states.json").write_text((work / "public.json").read_text())
    try:
        pred = sandboxed(work, "predict.py", ["--ro-bind", str(work / "predictor.py"), "/predictor.py"])
    except Exception as e:  # a predictor that crashes is a defect
        return False, f"predictor failed: {e}"
    if len(graded) != len(st) or len(pred) != len(st):
        return False, "result length mismatch"
    ndis = sum(1 for k in range(len(st)) if graded[k] != pred[k])
    npass, nfail = sum(graded), len(graded) - sum(graded)
    ok = not ndis and npass >= 8 and nfail >= 8
    # count only: the mismatching labels would let a table converge across re-runs
    return ok, f"states={len(st)} grader_pass={npass} grader_fail={nfail} disagree={ndis}"


# ---- V13: the filler control package -------------------------------------------------------------

def v13(lane, work):
    try:
        f = filler_pkg(lane)
    except (ValueError, OSError) as e:
        return False, f"filler package unusable: {e}"
    res = run_legs(lane, f, work, FILLER_LEGS, prefix="    filler: ")
    defects = [n for n, ok, _ in res if not ok]
    sub = [n for n in defects if n in SUBSTANTIVE]
    ok = len(sub) >= 3
    return ok, f"filler_checks={len(res)} defects={len(defects)} substantive={','.join(sub) or 0}"


# ---- driver --------------------------------------------------------------------------------------

def run_legs(lane, pkg, work, which, prefix=""):
    table = {
        "V1": lambda: v1(pkg),
        "V2": lambda: v2(lane, pkg, work),
        "V3": lambda: v3(pkg),
        "V4": lambda: v4(pkg),
        "V5": lambda: v5(lane, pkg),
        "V6": lambda: v6(pkg),
        "V7": lambda: v7(pkg),
        "V8": lambda: v8(lane, pkg),
        "V9": lambda: v9(pkg),
        "V10": lambda: v10(pkg),
        "V11": lambda: v11(pkg, work),
        "V12": lambda: v12(pkg),
        "V13": lambda: v13(lane, work),
    }
    out = []
    for name in which:
        try:
            ok, note = table[name]()
        except Exception as e:  # a check that cannot run is a defect, never a pass
            ok, note = False, f"error {type(e).__name__}: {e}"
        if prefix:
            print(f"{prefix}{name} {'ok' if ok else 'DEFECT'} {note}")
        else:
            print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
        out.append((name, ok, note))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="round-46 C3 counter (TB2 polyglot-c-py package)")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--filler", action="store_true",
                    help="measure the plans/filler46/ control package instead of the package under test")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="k46-c3-", dir=a.work) as work:
        if a.filler:
            which = FILLER_LEGS
            try:
                pkg = filler_pkg(lane)
            except (ValueError, OSError) as e:
                print(f"FILLER unusable: {e}")
                print(f"checks={len(which)} defects={len(which)}")
                print("PREDICATE C3 fail")
                return 1
        else:
            which = tuple(t for t in ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11",
                                     "V12", "V13"))
            try:
                pkg = real_pkg(lane)
            except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
                print(f"PACKAGE unreadable: {e}")
                defects = 0
                for name in which:
                    # the package is absent or unpinned: every leg that reads it defects; V13 reads only
                    # the filler package, so it is still measured
                    if name == "V13":
                        try:
                            ok, note = v13(lane, work)
                        except Exception as e2:
                            ok, note = False, f"error {type(e2).__name__}: {e2}"
                        if not ok:
                            defects += 1
                        print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
                    else:
                        defects += 1
                        print(f"{name} DEFECT package unreadable: {e}")
                print(f"checks={len(which)} defects={defects}")
                print(f"PREDICATE C3 {'pass' if defects == 0 else 'fail'}")
                return 0 if defects == 0 else 1
        res = run_legs(lane, pkg, work, which)
        defects = sum(1 for _n, ok, _note in res if not ok)
        print(f"checks={len(res)} defects={defects}")
        print(f"PREDICATE C3 {'pass' if defects == 0 else 'fail'}")
        return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
