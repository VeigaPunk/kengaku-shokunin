#!/usr/bin/env python3
"""Draft controls for the C2 counter's verdict-level surviving mutants (seat R42MutC2Counter).

Same shape as the freeze filler control (.ufo/waves/round-42/claims/c2_filler_control.py): import the
counter from <lane>/plans/round42_c2_verify.py, build scratch mirrors, call the counter's own
v-functions on them, and require a specific red/green verdict per mirror. Nothing in the lane is
written; every mirror lives under --work.

Groups (each kills the survivor class named in build/R42MutC2Counter.md):
  D1 v1 capture manifest   good + manifest-absent + malformed-line + extra-line + tampered-bytes
  D2 v2 gate invocation    freeze mirror (note prefix + gate P9/P10 lines + stdout shape),
                           tampered-spec (ValueError), tampered-gate (early return),
                           stubbed-gate receipt-present (effective-spec receipt_sha256),
                           CLI --work parent missing (no traceback)
  D3 v3 anchor rows        good + anchor-tampered + short-row + dup-row + 0-space + 4-space rows
  D4 v4 receipt            good + summary variants + matchNO named/unnamed + reordered ids +
                           second summary + tampered-dry (ValueError) + entry-absent note
  D5 v5 frozen probe       good + tampered-probe (early return; also kills the or->and pin gate)
  D6 v7 requirement map    good + wrong-label + wrong-line + missing-tag + dup-tag +
                           cite-nonviolating + no-section + unparsed-row + prose-line +
                           unknown-tag + no-violating-case + empty-cases-row
  D7 v8 order check        receipt-committed mirror (order PASS) - needs a lane whose HEAD has the
                           receipt committed (the landing tip or any later commit)
  D8 v9 surfaces           good + province-only-task + frontier-wrong + ids-only-in-source +
                           empty-receipt/empty-table + verdict-flipped-row + no-case-table +
                           readme-absent note
  D9 main exception path   bad-UTF-8 entry, main() in-process with v2 stubbed: V7/V9 must stay DEFECT

  python3 draft_c2_controls.py --lane <lane> --work <scratch> [--group D1,D2,...]
Exit 0 iff every expectation in every selected group holds.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

RECEIPT_REL = "corpus/evidence/round42/fibsqrt-probe.txt"
RECEIPT_SHA256 = "2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a"
SPEC_REL = "plans/pkg-spec-r42.json"
DRY_REL = "corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt"
PROBE_REL = "plans/fibsqrt_probe.py"
ENTRY_REL = "corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
README_REL = "corpus/README.md"
RAW = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/"
PINS = {  # spec row pins (equal to the counter's CAPTURES pins for these three files)
    "S125": ("test_outputs.py", "6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438"),
    "S126": ("instruction.md", "a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea"),
    "S127": ("sim.c", "700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173"),
}
SHA = lambda p: __import__("hashlib").sha256(pathlib.Path(p).read_bytes()).hexdigest()

fails = []
def check(group, case, cond, detail=""):
    tag = "ok" if cond else "DEFECT"
    if not cond:
        fails.append(f"{group}:{case}")
    print(f"CONTROL {group} {case} {tag} {detail}")

def load_counter(lane):
    spec_ = importlib.util.spec_from_file_location("c2counter", pathlib.Path(lane) / "plans/round42_c2_verify.py")
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    return mod

def receipt_text(lane):
    """The committed receipt: worktree, then HEAD:, then origin/master:. Digest-verified."""
    p = pathlib.Path(lane) / RECEIPT_REL
    text = None
    try:
        text = p.read_text()
    except OSError:
        for rev in ("HEAD", "origin/master"):
            r = subprocess.run(["git", "-C", str(lane), "show", f"{rev}:{RECEIPT_REL}"],
                               capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                text = r.stdout
                break
    if text is None:
        raise SystemExit(f"draft: receipt not obtainable from {lane}")
    import hashlib
    if hashlib.sha256(text.encode()).hexdigest() != RECEIPT_SHA256:
        raise SystemExit("draft: receipt copy is not at its committed digest")
    return text

def receipt_rows(text):
    rows = []
    for l in text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF]{3}) ", l)
        if m:
            rows.append((m.group(1), m.group(3), m.group(2)))
    return rows

def case_table(rows):
    return ("## Case table\n\n| case | tests | verdict | what |\n|---|---|---|---|\n"
            + "".join(f"| `{c}` | {t} | {v} | measured |\n" for c, t, v in rows))

def map_rows():
    return ("## Requirement map\n\n| frozen line | tag | label | cases |\n|---|---|---|---|\n"
            + "| `instruction.md:1` | `line-form` | unenforced | `lookup-28-comment-lines` |\n"
            + "| `instruction.md:9` | `last-32-lines` | unenforced | `lookup-28-reversed-lines` |\n"
            + "| `instruction.md:11` | `gates-file` | enforced | `no-gates-file` `gates-is-directory` |\n"
            + "| `instruction.md:11` | `line-limit` | enforced | `lookup-28-padded-32000` |\n"
            + "| `instruction.md:11` | `output-function` | partly | `nop` `lookup-28` |\n"
            + "| `instruction.md:12` | `example-208` | partly | `nop` `lookup-28` |\n"
            + "| `instruction.md:13` | `example-20000` | partly | `nop` `lookup-28` |\n")

def source_rows():
    out = []
    for sid, (cap, dig) in PINS.items():
        out.append(f"| {sid} | {RAW}{PINS[sid][0] if False else cap} | tb2 circuit-fibsqrt {cap} | A | 2026-10-26 "
                   f"| sha256 {dig} | teaches the {cap} grader surface and its checks | mined | 2026-10-26 "
                   f"| round-42 | {ENTRY_REL} |")
    return "\n".join(out) + "\n"

def mirror(work, name, files):
    m = pathlib.Path(work) / name
    shutil.rmtree(m, ignore_errors=True)
    for rel, text in files.items():
        p = m / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return m

def call(fn, *a):
    """Run a v-function, capturing stdout; return (ok, note, out, exc)."""
    buf = io.StringIO()
    exc = None
    try:
        with contextlib.redirect_stdout(buf):
            ok, note = fn(*a)
    except Exception as e:  # noqa: BLE001
        ok, note, exc = None, None, f"{type(e).__name__}: {e}"
    return ok, note, buf.getvalue(), exc

# ---------------------------------------------------------------- groups

def d1(lane, work, c2):
    real = pathlib.Path(lane) / "corpus/evidence/round42/tb2-circuit-fibsqrt"
    sums = (real / "SHA256SUMS").read_text()
    cap = "corpus/evidence/round42/tb2-circuit-fibsqrt"
    def build(name, sums_text, mutate=None):
        m = pathlib.Path(work) / name
        shutil.rmtree(m, ignore_errors=True)
        shutil.copytree(real, m / cap)
        (m / cap / "SHA256SUMS").write_text(sums_text)
        if mutate:
            mutate(m)
        return m
    a = build("d1a", sums)
    ok, note, _, _ = call(c2.v1, a)
    check("D1", "good", ok is True and note == "listed=9 bad=0 extra=0", note)
    b = build("d1b", sums)
    (b / cap / "SHA256SUMS").unlink()
    ok, note, _, _ = call(c2.v1, b)
    check("D1", "manifest-absent", ok is False and note == "manifest absent", note)
    c = build("d1c", sums + "\nxyz short\n")
    ok, note, _, _ = call(c2.v1, c)
    check("D1", "malformed-line", ok is False and note.startswith("unparsed manifest line"), note)
    d = build("d1d", sums + f"\n{SHA(real / 'README.md')} extra-file.txt\n")
    ok, note, _, _ = call(c2.v1, d)
    check("D1", "extra-line", ok is False and "extra-file.txt" in note, note)
    e = build("d1e", sums, mutate=lambda m: (m / cap / "README.md").write_text((real / "README.md").read_text() + "x"))
    ok, note, _, _ = call(c2.v1, e)
    check("D1", "tampered-bytes", ok is False and "bad=['README.md']" in note, note)

def d2(lane, work, c2):
    gate_text = (pathlib.Path(lane) / "plans/pkg_gate.py").read_text()
    spec_text = (pathlib.Path(lane) / SPEC_REL).read_text()
    # (a) freeze mirror as a plain dir: note prefix + gate P9/P10 lines + stdout shape
    s = c2.spec(lane)
    a = mirror(work, "d2a", {SPEC_REL: spec_text, "plans/pkg_gate.py": gate_text})
    ok, note, out, _ = call(c2.v2, a, work)
    shape = all(re.match(r"^(V\d |    gate: |checks=|PREDICATE )", l) for l in out.splitlines())
    check("D2", "freeze-note", ok is False and note.startswith("spec=frozen gate=frozen"), note)
    check("D2", "gate-p9-line", "gate: P9 " in out, "P9 line present")
    check("D2", "gate-p10-line", "gate: P10 DEFECT receipt unreadable" in out, "P10 line present")
    check("D2", "stdout-shape", shape and bool(out.strip()), "all lines prefixed")
    ok6, note6, out6, _ = call(c2.v6, lane)
    check("D2", "v6-quiet", ok6 is True and out6 == "", f"captured={out6[:40]!r}")
    # (f) tampered spec: v2 must raise ValueError (spec pin), not proceed
    f = mirror(work, "d2f", {SPEC_REL: spec_text.replace("round-42", "round-42X", 1),
                             "plans/pkg_gate.py": gate_text})
    ok, note, out, exc = call(c2.v2, f, work)
    check("D2", "tampered-spec", exc == "ValueError: spec template not at its freeze digest", str(exc))
    # (g) tampered gate: v2 must return False with the early-return note
    g = mirror(work, "d2g", {SPEC_REL: spec_text,
                             "plans/pkg_gate.py": gate_text + "\n# x\n"})
    ok, note, out, _ = call(c2.v2, g, work)
    check("D2", "tampered-gate", ok is False and note == "gate not at its freeze digest", note)
    # (ii) receipt present, gate stubbed: the effective spec must carry the real receipt digest
    real = receipt_text(lane)
    h = mirror(work, "d2h", {SPEC_REL: spec_text, "plans/pkg_gate.py": gate_text, s["receipt"]: real})
    orig = c2.subprocess.run
    c2.subprocess.run = lambda *ar, **kw: type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
    try:
        ok, note, out, _ = call(c2.v2, h, work)
    finally:
        c2.subprocess.run = orig
    eff = json.loads((pathlib.Path(work) / "pkg-spec-r42-effective.json").read_text())
    check("D2", "receipt-digest-filled", ok is True and eff["receipt_sha256"] == RECEIPT_SHA256, f"{eff['receipt_sha256'][:16]}…")
    # (w) CLI --work parent missing: no traceback on stderr (fresh parent every run)
    shutil.rmtree(pathlib.Path(work) / "nope", ignore_errors=True)
    r = subprocess.run([sys.executable, str(pathlib.Path(lane) / "plans/round42_c2_verify.py"),
                        "--lane", str(lane), "--work", str(pathlib.Path(work) / "nope" / "w")],
                       capture_output=True, text=True, timeout=300, env={"PATH": "/usr/bin", "TMPDIR": str(work)})
    check("D2", "work-parent-missing", "Traceback" not in r.stderr, r.stderr[-80:])
    # cli-shape: a full CLI run's stdout stays prefixed (kills capture_output=False leaks)
    r2 = subprocess.run([sys.executable, str(pathlib.Path(lane) / "plans/round42_c2_verify.py"),
                         "--lane", str(lane), "--work", str(pathlib.Path(work) / "wshape")],
                        capture_output=True, text=True, timeout=300, env={"PATH": "/usr/bin", "TMPDIR": str(work)})
    shp = all(re.match(r"^(V\d |    gate: |checks=|PREDICATE )", l) for l in r2.stdout.splitlines())
    check("D2", "cli-shape", r2.returncode == 1 and shp and r2.stdout.count("\n") >= 12, r2.stdout[-60:])

def d3(lane, work, c2):
    good = source_rows()
    spec_text = (pathlib.Path(lane) / SPEC_REL).read_text()
    a = mirror(work, "d3a", {SPEC_REL: spec_text, "corpus/SOURCES.md": good})
    ok, note, _, _ = call(c2.v3, a)
    check("D3", "good", ok is True and note == "rows=3 bad=0", note)
    b = mirror(work, "d3b", {SPEC_REL: spec_text, "corpus/SOURCES.md": good.replace(PINS["S125"][1], "0" + PINS["S125"][1][1:], 1)})
    ok, note, _, _ = call(c2.v3, b)
    check("D3", "anchor-tampered", ok is False and "S125:anchor_digest" in note, note)
    c = mirror(work, "d3c", {SPEC_REL: spec_text, "corpus/SOURCES.md": good.replace(" | mined | 2026-10-26 | round-42 |", " | mined |", 1)})
    ok, note, _, exc = call(c2.v3, c)
    check("D3", "short-row", (ok is False and "row" in note) or exc is not None, note or str(exc))
    d = mirror(work, "d3d", {SPEC_REL: spec_text, "corpus/SOURCES.md": good + good.splitlines()[0] + "\n"})
    ok, note, _, _ = call(c2.v3, d)
    check("D3", "dup-row", ok is False, note)
    e = mirror(work, "d3e", {SPEC_REL: spec_text, "corpus/SOURCES.md": "\n".join(l.lstrip() if l.startswith("| S125 ") else l for l in good.splitlines()) + "\n"})
    ok, note, _, _ = call(c2.v3, e)
    check("D3", "zero-space-row", ok is True, note)
    f = mirror(work, "d3f", {SPEC_REL: spec_text, "corpus/SOURCES.md": "\n".join("    " + l if l.startswith("| S125 ") else l for l in good.splitlines()) + "\n"})
    ok, note, _, _ = call(c2.v3, f)
    check("D3", "four-space-row", ok is False, note)

def d4(lane, work, c2):
    real = receipt_text(lane)
    spec_text = (pathlib.Path(lane) / SPEC_REL).read_text()
    dry_text = (pathlib.Path(lane) / DRY_REL).read_text()
    rows = receipt_rows(real)
    entry_min = "# tb2 circuit-fibsqrt grader\n\nsource: S125 x\nsource: S126 x\nsource: S127 x\n\nS125 S126 S127 pinned.\n"
    def entry_named(ids):
        return entry_min + "\n" + " ".join(f"`{c}`" for c in ids) + "\n"
    a = mirror(work, "d4a", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: real, ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, a)
    check("D4", "good", ok is True and note == "cases=16 mismatches_named=0/0 bad=0", note)
    def summ_swap(real, old, new):
        return real.replace(old, new, 1)
    b = mirror(work, "d4b", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: summ_swap(real, "observed_pass=7", "observed_pass=8"), ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, b)
    check("D4", "summary-p8", ok is False and "summary disagrees" in note, note)
    b2 = mirror(work, "d4b2", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: summ_swap(real, "observed_pass=7 observed_fail=9", "observed_pass=9 observed_fail=7"), ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, b2)
    check("D4", "summary-p9f7", ok is False and "summary disagrees" in note, note)
    b3 = mirror(work, "d4b3", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: real.replace(
        "cases=16 observed_pass=7 observed_fail=9 mismatches=0", "cases= observed_pass=7 observed_fail=9 mismatches=0", 1), ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, b3)
    check("D4", "summary-empty-n", ok is False and note == "cases=16 mismatches_named=0/0 bad=['summary line count != 1']", note)
    # (b4) synthetic 14 pass / 2 fail, summary agrees
    lines = real.splitlines()
    nflip = 0
    out = []
    for l in lines:
        if l.startswith("CASE ") and " observed=fail " in l and nflip < 7:
            l = l.replace(" observed=fail ", " observed=pass ", 1).replace("tests=PPF", "tests=PPP", 1).replace("tests=FFF", "tests=PPP", 1).replace("tests=PFF", "tests=PPP", 1).replace("tests=PFP", "tests=PPP", 1)
            nflip += 1
        out.append(l)
    b4r = "\n".join(out).replace("cases=16 observed_pass=7 observed_fail=9", "cases=16 observed_pass=14 observed_fail=2", 1) + "\n"
    b4 = mirror(work, "d4b4", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: b4r, ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, b4)
    check("D4", "summary-14-2", ok is True, note)
    # (c) match=NO unnamed / (d) named
    c_r = real.replace("CASE nop predicted=fail observed=fail", "CASE nop predicted=fail observed=fail", 1)
    c_r = real.replace("match=yes regrade=same violates=output-function,example-208,example-20000 -- the shipped",
                       "match=NO regrade=same violates=output-function,example-208,example-20000 -- the shipped", 1)
    c_r = c_r.replace("cases=16 observed_pass=7 observed_fail=9 mismatches=0", "cases=16 observed_pass=7 observed_fail=9 mismatches=1", 1)
    c = mirror(work, "d4c", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: c_r, ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, c)
    check("D4", "matchNO-unnamed", ok is False and "not named in the entry: ['nop']" in note, note)
    d = mirror(work, "d4d", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: c_r, ENTRY_REL: entry_named(["nop"])})
    ok, note, _, _ = call(c2.v4, d)
    check("D4", "matchNO-named", ok is True, note)
    # (e) reordered ids
    rl = real.splitlines()
    i0 = next(i for i, l in enumerate(rl) if l.startswith("CASE "))
    rl[i0], rl[i0 + 1] = rl[i0 + 1], rl[i0]
    e = mirror(work, "d4e", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: "\n".join(rl) + "\n", ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, e)
    check("D4", "ids-reordered", ok is False and "case ids differ" in note, note)
    # (f) tampered dry table: v4 must raise ValueError
    f = mirror(work, "d4f", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: real, ENTRY_REL: entry_min,
                             DRY_REL: (pathlib.Path(lane) / DRY_REL).read_text().replace("line-form", "line-formX", 1)})
    ok, note, _, exc = call(c2.v4, f)
    check("D4", "tampered-dry", exc == "ValueError: dry table not at its freeze digest", str(exc))
    # (g) second summary line
    g = mirror(work, "d4g", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: real + "cases=16 observed_pass=7 observed_fail=9 mismatches=0\n", ENTRY_REL: entry_min})
    ok, note, _, _ = call(c2.v4, g)
    check("D4", "two-summaries", ok is False and "summary line count != 1" in note, note)
    # (h2) receipt present, entry absent: exact early-return note
    h = mirror(work, "d4h", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: real})
    ok, note, _, _ = call(c2.v4, h)
    check("D4", "entry-absent-note", ok is False and note == "receipt or entry absent", note)

def d5(lane, work, c2):
    ok, note, _, _ = call(c2.v5, lane)
    check("D5", "good", ok is True and note == "probe=frozen dry_byte_equal=True", note)
    c = mirror(work, "d5c", {PROBE_REL: (pathlib.Path(lane) / PROBE_REL).read_text() + "\n# tampered\n",
                             DRY_REL: (pathlib.Path(lane) / DRY_REL).read_text()})
    ok, note, _, _ = call(c2.v5, c)
    check("D5", "tampered-probe", ok is False and note == "probe or dry table not at freeze digest", note)

def d6(lane, work, c2):
    real = receipt_text(lane)
    spec_text = (pathlib.Path(lane) / SPEC_REL).read_text()
    dry_text = (pathlib.Path(lane) / DRY_REL).read_text()
    base_entry = ("# tb2 circuit-fibsqrt grader\n\nsource: S125 x\nsource: S126 x\nsource: S127 x\n\n"
                  "S125 S126 S127 pinned.\n\n" + map_rows() + "\n" + case_table(receipt_rows(real)))
    prov = "# PROVINCE\n\n- circuit-fibsqrt: tb2-circuit-fibsqrt-grader.md\n"
    readme = "# corpus\n\n## Frontier\n\n- circuit-fibsqrt read\n"
    def m(name, entry_text, receipt=real):
        return mirror(work, name, {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: receipt, ENTRY_REL: entry_text,
                                   "PROVINCE.md": prov, README_REL: readme})
    a = m("d6a", base_entry)
    ok, note, _, _ = call(c2.v7, a)
    check("D6", "good", ok is True and note == "rows=7 tags=7 bad=0", note)
    b = m("d6b", base_entry.replace("| enforced | `no-gates-file`", "| unenforced | `no-gates-file`", 1))
    ok, note, _, _ = call(c2.v7, b)
    check("D6", "wrong-label", ok is False and "gates-file: labelled unenforced" in note, note)
    c = m("d6c", base_entry.replace("| `instruction.md:11` | `line-limit` |", "| `instruction.md:12` | `line-limit` |", 1))
    ok, note, _, _ = call(c2.v7, c)
    check("D6", "wrong-line", ok is False and "line-limit: line 12 is not the frozen" in note, note)
    d = m("d6d", base_entry.replace("| `instruction.md:1` | `line-form` | unenforced | `lookup-28-comment-lines` |\n", "", 1))
    ok, note, _, _ = call(c2.v7, d)
    check("D6", "missing-tag", ok is False and note == "rows=6 tags=7 bad=[\"tags missing=['line-form'] duplicated=0\"]", note)
    e = m("d6e", base_entry.replace("| `instruction.md:11` | `line-limit` | enforced | `lookup-28-padded-32000` |",
                                    "| `instruction.md:11` | `line-limit` | enforced | `lookup-28-padded-32000` |\n| `instruction.md:11` | `line-limit` | enforced | `lookup-28-padded-32000` |", 1))
    ok, note, _, _ = call(c2.v7, e)
    check("D6", "dup-tag", ok is False and note == "rows=8 tags=7 bad=[\"tags missing=0 duplicated=['line-limit']\"]", note)
    f = m("d6f", base_entry.replace("| `instruction.md:11` | `gates-file` | enforced | `no-gates-file` `gates-is-directory` |",
                                    "| `instruction.md:11` | `gates-file` | enforced | `lookup-28` |", 1))
    ok, note, _, _ = call(c2.v7, f)
    check("D6", "cite-nonviolating", ok is False and "gates-file: cites no case or a case that does not violate it" in note, note)
    g = m("d6g", base_entry.replace("## Requirement map\n", "## Requirement mapX\n", 1))
    ok, note, _, _ = call(c2.v7, g)
    check("D6", "no-section", ok is False and note == "no '## Requirement map' section", note)
    h = m("d6h", base_entry.replace("| `instruction.md:13` | `example-20000` | partly | `nop` `lookup-28` |",
                                    "| `instruction.md:13` | `example-20000` | partly | `nop` `lookup-28` |\n| `instruction.md:13` | `` | partly | `nop` |", 1))
    ok, note, _, _ = call(c2.v7, h)
    check("D6", "unparsed-row", ok is False and note.startswith('rows=7 tags=7 bad=["unparsed row '), note)
    i = m("d6i", base_entry + "\nsee instruction.md:11 for the limit\n")
    ok, note, _, _ = call(c2.v7, i)
    check("D6", "prose-line", ok is True, note)
    j = m("d6j", base_entry.replace("| `instruction.md:13` | `example-20000` | partly | `nop` `lookup-28` |",
                                    "| `instruction.md:13` | `example-2000` | partly | `nop` |", 1))
    ok, note, _, _ = call(c2.v7, j)
    check("D6", "unknown-tag", ok is False and "example-2000: not a frozen tag" in note, note)
    # (k) receipt where line-form is violated by no case; map row still present
    k_r = "\n".join(l.replace("violates=line-form,", "violates=").replace(",line-form", "") if "line-form" in l and l.startswith("CASE ") else l
                    for l in real.splitlines())
    k = m("d6k", base_entry, receipt=k_r)
    ok, note, _, _ = call(c2.v7, k)
    check("D6", "no-violating-case", ok is False and note == "rows=7 tags=7 bad=['line-form: no receipt case violates it']", note)
    n = m("d6n", base_entry.replace("| `instruction.md:13` | `example-20000` | partly | `nop` `lookup-28` |",
                                    "| `instruction.md:13` | `example-20000` | partly ||", 1))
    ok, note, _, _ = call(c2.v7, n)
    check("D6", "empty-cases-row", ok is False and "example-20000: cites no case or a case that does not violate it" in note, note)
    o = m("d6o", base_entry.replace("| `instruction.md:13` | `example-20000` | partly | `nop` `lookup-28` |",
                                    "| `instruction.md:13` | `example-20000` | partly | `` |", 1))
    ok, note, _, _ = call(c2.v7, o)
    check("D6", "empty-backtick-cite", ok is False and note.endswith("bad=['example-20000: cites no case or a case that does not violate it']"), note)
    h2 = mirror(work, "d6h2", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: real, "PROVINCE.md": prov, README_REL: readme})
    ok, note, _, _ = call(c2.v7, h2)
    check("D6", "entry-absent-note", ok is False and note == "receipt or entry absent", note)

def d7(lane, work, c2):
    ok, note, out, _ = call(c2.v8, lane)
    check("D7", "order-pass", ok is True and note == "order_exit=0 result=PASS", note)
    check("D7", "v8-quiet", out == "", f"captured={out[:60]!r}")

def d8(lane, work, c2):
    real = receipt_text(lane)
    spec_text = (pathlib.Path(lane) / SPEC_REL).read_text()
    rows = receipt_rows(real)
    body_ids = "\nS125 S126 S127 are the three pinned files.\n"
    good_entry = ("# tb2 circuit-fibsqrt grader\n\nsource: S125 x\nsource: S126 x\nsource: S127 x\n"
                  + body_ids + "\n" + case_table(rows))
    prov = "# PROVINCE\n\n- circuit-fibsqrt: tb2-circuit-fibsqrt-grader.md\n"
    readme = "# corpus\n\n## Frontier\n\n- circuit-fibsqrt read\n"
    def m(name, entry=good_entry, receipt=real, province=prov, rd=readme):
        return mirror(work, name, {SPEC_REL: spec_text, c2.spec(lane)["receipt"]: receipt, ENTRY_REL: entry,
                                   "PROVINCE.md": province, README_REL: rd})
    a = m("d8a")
    ok, note, _, _ = call(c2.v9, a)
    check("D8", "good", ok is True and note == "case_rows=16/16 bad=0", note)
    b = m("d8b", province="# PROVINCE\n\n- circuit-fibsqrt is covered\n")
    ok, note, _, _ = call(c2.v9, b)
    check("D8", "province-only-task", ok is False and "PROVINCE.md names the task and the entry on no line" in note, note)
    c = m("d8c", rd="# corpus\n\n## Frontier\n\n- nothing new\n")
    ok, note, _, _ = call(c2.v9, c)
    check("D8", "frontier-wrong", ok is False and "README ## Frontier does not name the task" in note, note)
    d = m("d8d", entry="# tb2 circuit-fibsqrt grader\n\nsource: S125 x\nsource: S126 x\nsource: S127 x\n\n" + case_table(rows))
    ok, note, _, _ = call(c2.v9, d)
    check("D8", "ids-only-in-source", ok is False and "row ids absent outside source lines" in note, note)
    e = m("d8e", entry="# e\n\nS125 S126 S127\n\n## Case table\n\n| case | tests | verdict | what |\n|---|---|---|---|\n",
          receipt="cases=16 observed_pass=7 observed_fail=9 mismatches=0\n")
    ok, note, _, _ = call(c2.v9, e)
    check("D8", "empty-receipt-empty-table", ok is False and "receipt cases=0" in note, note)
    f = m("d8f", entry=good_entry.replace("| `nop` | PPF | fail |", "| `nop` | PPF | pass |", 1))
    ok, note, _, _ = call(c2.v9, f)
    check("D8", "verdict-flipped-row", ok is False and "equal=False" in note, note)
    g = m("d8g", entry="# tb2 circuit-fibsqrt grader\n\nsource: S125 x\nsource: S126 x\nsource: S127 x\n\nS125 S126 S127 pinned.\n")
    ok, note, _, _ = call(c2.v9, g)
    check("D8", "no-case-table", ok is False and "no '## Case table' section" in note, note)
    p_ = m("d8p", entry=good_entry.replace("| `nop` | PPF | fail | measured |", "| `` | PPF | fail | x |", 1))
    ok, note, _, _ = call(c2.v9, p_)
    check("D8", "empty-id-row", ok is False and note == "case_rows=15/16 bad=['case table rows=15 receipt cases=16 equal=False']", note)
    h = mirror(work, "d8h", {SPEC_REL: spec_text, c2.spec(lane)["receipt"]: real, "PROVINCE.md": prov, README_REL: readme})
    ok, note, _, _ = call(c2.v9, h)
    check("D8", "entry-absent-note", ok is False and note == "receipt, entry, PROVINCE.md or README absent", note)

def d9(lane, work, c2):
    real = receipt_text(lane)
    spec_text = (pathlib.Path(lane) / SPEC_REL).read_text()
    dry_text = (pathlib.Path(lane) / DRY_REL).read_text()
    rows = receipt_rows(real)
    m = mirror(work, "d9a", {SPEC_REL: spec_text, DRY_REL: dry_text, c2.spec(lane)["receipt"]: real,
                             ENTRY_REL: "# bad\n\nS125 S126 S127\n\n" + case_table(rows),
                             "PROVINCE.md": "# PROVINCE\n\n- circuit-fibsqrt: tb2-circuit-fibsqrt-grader.md\n",
                             README_REL: "# corpus\n\n## Frontier\n\n- circuit-fibsqrt read\n"})
    (m / ENTRY_REL).write_bytes(b"# bad \xff\xfe entry\n")
    orig_v2 = c2.v2
    c2.v2 = lambda lane_, work_: (False, "stub")
    buf = io.StringIO()
    try:
        argv = sys.argv
        sys.argv = ["round42_c2_verify.py", "--lane", str(m)]
        with contextlib.redirect_stdout(buf):
            rc = c2.main()
    finally:
        sys.argv = argv
        c2.v2 = orig_v2
    out = buf.getvalue()
    v7 = re.search(r"^V7 (ok|DEFECT) (.*)$", out, re.M)
    v9 = re.search(r"^V9 (ok|DEFECT) (.*)$", out, re.M)
    check("D9", "badutf8-red", rc == 1 and v7 and v9 and v7.group(1) == "DEFECT" and v9.group(1) == "DEFECT"
          and "UnicodeDecodeError" in v7.group(2) and "UnicodeDecodeError" in v9.group(2),
          f"V7 {v7.group(1) if v7 else '?'} V9 {v9.group(1) if v9 else '?'}")

GROUPS = {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5, "D6": d6, "D7": d7, "D8": d8, "D9": d9}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", required=True)
    ap.add_argument("--group", default="all")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    c2 = load_counter(lane)
    want = list(GROUPS) if a.group == "all" else a.group.split(",")
    for g in want:
        GROUPS[g](lane, a.work, c2)
    print(f"DRAFT-CONTROLS groups={len(want)} failed={len(fails)} {fails or ''}")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
