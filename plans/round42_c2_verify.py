#!/usr/bin/env python3
"""Round-42 C2 counter (coverage): the pinned Terminal-Bench 2.0 `circuit-fibsqrt` grader admitted as a knowledge
package with an executed offline probe (an eighth grader class: the graded artefact is a DATA file — a gate list —
executed by a grader-owned simulator compiled at grading time, `tests/sim.c`, and scored on a fixed 28-row table
of inputs).

Frozen predicate (same sentence in plans/round-42-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round42_c2_verify.py --lane .` prints `checks=9 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.

Every input this counter reads that exists at the freeze is pinned here by digest: the spec template, the
gate, the probe, the frozen dry table and the nine captures. V1-V8 are the round-41 counter's
(`plans/round41_c2_verify.py`), re-pointed at the round-42 package; no V1-V8 check is relaxed. V9 is new
(round-41 closure R3, `R41CritClaims` D2: V1-V8 admitted a content-free 43-line filler entry).

  V1 capture manifest: corpus/evidence/round42/tb2-circuit-fibsqrt/SHA256SUMS lists exactly the nine captured
     files at their frozen digests and every file's bytes match.
  V2 package gate: plans/pkg-spec-r42.json at its freeze digest and plans/pkg_gate.py at its freeze digest;
     `pkg_gate.py package --rerun --require-clean-tree` accepts the package that spec defines (the counter
     fills `receipt_sha256` with the digest of the receipt it finds, so P2 is a presence check and
     authenticity rests on P10, the fresh probe run byte-compared to the receipt).
  V3 anchor digests: each of the spec's rows has an 11-cell registry row whose anchor cell carries exactly
     one `sha256 <64 hex>` token, equal to that row's own spec pin.
  V4 receipt: CASE lines whose ids equal the frozen case table in order, one summary line
     `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=<m>` that agrees with the CASE lines, and
     every `match=NO` case id named in the entry.
  V5 frozen probe: plans/fibsqrt_probe.py at its freeze digest and its `--dry` output byte-equal to
     corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt (itself at its freeze digest).
  V6 census: `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` exits 0.
  V7 requirement map: the entry's `## Requirement map` table has exactly one row per frozen tag, each row
     `| `instruction.md:<L>` | `<tag>` | <label> | <cases> |` with <L> the tag's frozen line and the label
     DERIVED from every receipt case whose `violates=` set carries the tag (`enforced` iff all observed
     `fail`, `unenforced` iff all observed `pass`, `partly` otherwise), citing >=1 violating case id.
  V8 order (QUALITY Q30): `plans/order_check.py --lane <lane> --claims plans/round-42-claims.md --receipt
     <spec receipt>` exits 0 and prints `ORDER RESULT PASS`.
  V9 content (round-41 closure R3): (a) the entry has a `## Case table` section holding exactly one row per
     receipt CASE, in receipt order, `| `<cid>` | <tests letters> | <observed verdict> | <text> |`, letters
     and verdict equal to the receipt's; (b) every spec row id occurs in the entry outside its `source:`
     line; (c) PROVINCE.md has a line naming both `circuit-fibsqrt` and the entry's file name; (d) the
     `## Frontier` section of corpus/README.md names `circuit-fibsqrt`. A filler entry that states no
     measured case, and a package whose PROVINCE/§Frontier surfaces were never written, fail V9 (freeze
     control `claims/control-c2-filler.txt`).

`--work DIR` is created if absent before the scratch directory is made inside it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round42/tb2-circuit-fibsqrt"
CAPTURES = {
    "Dockerfile": "780c23986778f3e5f842567868af30b1135ed095ca9449e1c90b7f0e0483d3d4",
    "README.md": "201f7c889dd6f73dd83ca078e347272b33720fa622f8c757ea6d5770453f4cbd",
    "gates.txt": "032786f94f16605767c62bb61ce4dbba7ab7d3f1046712c975f01c9a04b6ad29",
    "instruction.md": "a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea",
    "sim.c": "700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173",
    "solve.sh": "a4ffab4183815a0eb7646abc1de1fc67695014c060d7ff16e8bca9ec94385d0b",
    "task.toml": "9f5aa1f7ebbbcec90fd109121e9bd509af3cfff6b4cec701bd91947988f40972",
    "test.sh": "4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334",
    "test_outputs.py": "6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438",
}
SPEC_REL = "plans/pkg-spec-r42.json"
SPEC_SHA256 = "e836c425fec93421433f8dc6cb98e0f4ec00c0c8f0877145ee225d77ca710439"
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
PROBE_REL = "plans/fibsqrt_probe.py"
PROBE_SHA256 = "fc58bf3f1780aaefee9df1e635b01765d3fb5d9224f1958494df4e1b8ed061b3"
DRY_REL = "corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt"
DRY_SHA256 = "9ee60af69ba3dc9fb1585dbaeb33faef2e96c92977d555837565ce416f6898b5"
ORDER_REL = "plans/order_check.py"
CLAIMS_REL = "plans/round-42-claims.md"
TASK = "circuit-fibsqrt"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")
MAP_ROW = re.compile(r"^\|\s*`instruction\.md:(\d+)`\s*\|\s*`([a-z0-9-]+)`\s*\|\s*(enforced|unenforced|partly)\s*\|(.*)\|\s*$")
CASE_ROW = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|\s*([PF]{3})\s*\|\s*(pass|fail)\s*\|.*\|\s*$")


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def spec(lane):
    if sha256(lane / SPEC_REL) != SPEC_SHA256:
        raise ValueError("spec template not at its freeze digest")
    return json.loads((lane / SPEC_REL).read_text())


def dry(lane):
    if sha256(lane / DRY_REL) != DRY_SHA256:
        raise ValueError("dry table not at its freeze digest")
    text = (lane / DRY_REL).read_text()
    tags = {}
    cases = []
    for l in text.splitlines():
        p = l.split()
        if p and p[0] == "TAG":
            tags[p[1]] = p[2]
        elif p and p[0] == "CASE":
            cases.append(p[1])
    return tags, cases


def v1(lane):
    capdir = lane / CAP
    try:
        lines = [l for l in (capdir / "SHA256SUMS").read_text().splitlines() if l.strip()]
    except OSError:
        return False, "manifest absent"
    listed = {}
    for l in lines:
        m = re.match(r"^([0-9a-f]{64})\s+\*?(\S+)$", l.strip())
        if not m:
            return False, f"unparsed manifest line {l[:40]!r}"
        listed[m.group(2)] = m.group(1)
    bad = [n for n, d in CAPTURES.items() if listed.get(n) != d or sha256(capdir / n) != d]
    extra = sorted(set(listed) - set(CAPTURES))
    return not bad and not extra, f"listed={len(listed)} bad={bad or 0} extra={extra or 0}"


def v2(lane, work):
    s = spec(lane)
    if sha256(lane / GATE_REL) != GATE_SHA256:
        return False, "gate not at its freeze digest"
    s["receipt_sha256"] = sha256(lane / s["receipt"]) or "absent"
    sp = pathlib.Path(work) / "pkg-spec-r42-effective.json"
    sp.write_text(json.dumps(s))
    r = subprocess.run([sys.executable, str(lane / GATE_REL), "package", "--root", str(lane), "--spec", str(sp),
                        "--rerun", "--require-clean-tree"], capture_output=True, text=True, timeout=1800)
    for l in r.stdout.splitlines():
        print("    gate: " + l)
    return r.returncode == 0, f"spec=frozen gate=frozen gate_exit={r.returncode}"


def rows(lane):
    out = {}
    for line in (lane / "corpus/SOURCES.md").read_text().splitlines():
        m = SOURCE_ROW.match(line)
        if m:
            out.setdefault(m.group(1), []).append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def v3(lane):
    s = spec(lane)
    reg, bad = rows(lane), []
    for sid, row in s["rows"].items():
        found = reg.get(sid, [])
        if len(found) != 1 or len(found[0]) != 11:
            bad.append(f"{sid}:row")
            continue
        toks = re.findall(r"sha256\s+([0-9a-fA-F]+)", found[0][5])
        if toks != [row["sha256"]]:
            bad.append(f"{sid}:anchor_digest")
    return not bad, f"rows={len(s['rows'])} bad={bad or 0}"


def receipt_cases(text):
    out = {}
    for l in text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=(pass|fail) observed=(pass|fail) .*?\bviolates=(\S*)", l)
        if m:
            out[m.group(1)] = (m.group(3), set(filter(None, m.group(4).split(","))))
    return out


def v4(lane):
    s = spec(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    _tags, frozen_ids = dry(lane)
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
    unnamed = [c for c in no if f"`{c}`" not in entry]
    if unnamed:
        bad.append(f"mismatch cases not named in the entry: {unnamed}")
    return not bad, f"cases={len(ids)} mismatches_named={len(no) - len(unnamed)}/{len(no)} bad={bad or 0}"


def v5(lane):
    if sha256(lane / PROBE_REL) != PROBE_SHA256 or sha256(lane / DRY_REL) != DRY_SHA256:
        return False, "probe or dry table not at freeze digest"
    r = subprocess.run([sys.executable, str(lane / PROBE_REL), "--lane", str(lane), "--dry"],
                       capture_output=True, text=True, timeout=120)
    same = r.returncode == 0 and r.stdout == (lane / DRY_REL).read_text()
    return same, f"probe=frozen dry_byte_equal={same}"


def v6(lane):
    r = subprocess.run([CENSUS, "validate", "--file", str(lane / "corpus/SOURCES.md")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode == 0, f"census_exit={r.returncode}"


def derive(verdicts):
    if verdicts == {"fail"}:
        return "enforced"
    if verdicts == {"pass"}:
        return "unenforced"
    return "partly"


def v7(lane):
    s = spec(lane)
    tags, _ids = dry(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    parsed = receipt_cases(text)
    sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    if not sec:
        return False, "no '## Requirement map' section"
    seen, bad = {}, []
    for l in sec.group(1).splitlines():
        m = MAP_ROW.match(l)
        if not m:
            if l.startswith("|") and "instruction.md:" in l:
                bad.append(f"unparsed row {l[:50]!r}")
            continue
        line, tag, label, rest = m.group(1), m.group(2), m.group(3), m.group(4)
        seen[tag] = seen.get(tag, 0) + 1
        if tag not in tags:
            bad.append(f"{tag}: not a frozen tag")
            continue
        if tags[tag] != f"instruction.md:{line}":
            bad.append(f"{tag}: line {line} is not the frozen {tags[tag]}")
        violating = {cid: obs for cid, (obs, v) in parsed.items() if tag in v}
        if not violating:
            bad.append(f"{tag}: no receipt case violates it")
            continue
        want = derive(set(violating.values()))
        if label != want:
            bad.append(f"{tag}: labelled {label}, receipt derives {want}")
        cited = re.findall(r"`([a-z0-9-]+)`", rest)
        if not cited or any(c not in violating for c in cited):
            bad.append(f"{tag}: cites no case or a case that does not violate it")
    missing = sorted(set(tags) - set(seen))
    dup = sorted(t for t, n in seen.items() if n > 1)
    if missing or dup:
        bad.append(f"tags missing={missing or 0} duplicated={dup or 0}")
    return not bad, f"rows={sum(seen.values())} tags={len(tags)} bad={bad or 0}"


def v8(lane):
    s = spec(lane)
    r = subprocess.run([sys.executable, str(lane / ORDER_REL), "--lane", str(lane), "--claims", CLAIMS_REL,
                        "--receipt", s["receipt"]], capture_output=True, text=True, timeout=300)
    passed = r.returncode == 0 and "ORDER RESULT PASS" in r.stdout.splitlines()
    return passed, f"order_exit={r.returncode} result={'PASS' if passed else 'not-PASS'}"


def v9(lane):
    s = spec(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
        province = (lane / "PROVINCE.md").read_text()
        readme = (lane / s["readme"]).read_text()
    except OSError:
        return False, "receipt, entry, PROVINCE.md or README absent"
    want = []
    for l in text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF]{3}) ", l)
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
    missing = [sid for sid in s["rows"] if sid not in body]
    if missing:
        bad.append(f"row ids absent outside source lines: {missing}")
    name = pathlib.PurePosixPath(s["entry"]).name
    if not any(TASK in l and name in l for l in province.splitlines()):
        bad.append("PROVINCE.md names the task and the entry on no line")
    fr = re.search(r"^## Frontier\n(.*?)(?=^## |\Z)", readme, re.S | re.M)
    if not fr or TASK not in fr.group(1):
        bad.append("README ## Frontier does not name the task")
    return not bad, f"case_rows={len(got)}/{len(want)} bad={bad or 0}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="k42-c2-", dir=a.work) as work:
        checks = [("V1", lambda: v1(lane)), ("V2", lambda: v2(lane, work)), ("V3", lambda: v3(lane)),
                  ("V4", lambda: v4(lane)), ("V5", lambda: v5(lane)), ("V6", lambda: v6(lane)),
                  ("V7", lambda: v7(lane)), ("V8", lambda: v8(lane)), ("V9", lambda: v9(lane))]
        defects = 0
        for name, fn in checks:
            try:
                ok, note = fn()
            except Exception as e:  # a check that cannot run is a defect, never a pass
                ok, note = False, f"error {type(e).__name__}: {e}"
            defects += not ok
            print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
    print(f"checks={len(checks)} defects={defects}")
    print(f"PREDICATE C2 {'pass' if defects == 0 else 'fail'}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
