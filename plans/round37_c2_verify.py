#!/usr/bin/env python3
"""Round-37 C2 counter (coverage): the pinned Terminal-Bench 2.0 `configure-git-webserver` grader admitted
as a knowledge package with an executed offline probe.

Frozen predicate (same sentence in plans/round-37-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round37_c2_verify.py --lane .` prints `checks=7 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.

  V1 capture manifest: corpus/evidence/round37/tb2-git-webserver/SHA256SUMS lists exactly the six captured
     files at their frozen digests and every file's bytes match.
  V2 package gate: `plans/pkg_gate.py package --rerun --require-clean-tree` accepts the package defined by
     plans/pkg-spec-r37.json (the frozen template; the counter fills `receipt_sha256` with the digest of
     the receipt it finds, so P2 is a presence check here and authenticity rests on P10, the fresh probe
     run byte-compared to the receipt). This brings the gate's quote-support clauses (every quote verbatim
     on its cited capture line, distinct, 3-25 words, >=8 lines) to C2: round 36's C2 counter checked
     shape only and admitted a junk package (round-36 spot-check, routed item 3).
  V3 anchor digests: each of S111-S113 has an anchor cell carrying `sha256 <64 hex>` equal to its spec pin,
     and no other sha256 token (round-36 spot-check routed item 1: S110's anchor digest lost a digit).
  V4 receipt: 22 CASE lines whose ids equal the frozen case table, a summary line
     `cases=22 observed_pass=<p> observed_fail=<f> mismatches=<m>` with p+f=22 that agrees with the CASE
     lines, and every `match=NO` case id named in the entry.
  V5 frozen probe: plans/git_webserver_probe.py at its freeze digest and its `--dry` table byte-equal to
     corpus/evidence/round37/git-webserver-dry-cases-freeze.txt (itself at its freeze digest).
  V6 census: `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` exits 0.
  V7 requirement map: the entry's `## Requirement map` table maps instruction.md lines to `enforced`,
     `unenforced` or `partly`, its ranges cover instruction.md lines 1-9, every row cites >=1 receipt case
     id in backticks, and the label agrees with the receipt: an `enforced` row cites a case observed `fail`,
     an `unenforced` row a case observed `pass`, a `partly` row one of each. (A filler entry whose quotes
     are verbatim but whose claims are not tied to the executed verdicts fails here.)
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

CAP = "corpus/evidence/round37/tb2-git-webserver"
CAPTURES = {
    "instruction.md": "62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97",
    "solve.sh": "c31cd92ecb1b357d8c0abcf4821717e83a1770cf58f028620cd0ee3e6b1e4c62",
    "task.toml": "ebb40d72f689512cbd90d865d88ef966b6665ab215544f9247b898b7fa94751b",
    "test.sh": "afafc3ffdaf911f7a93003c0746f217188099c174e5d3eb7dada17133df15895",
    "test_outputs.py": "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37",
    "verify.sh": "1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05",
}
SPEC_REL = "plans/pkg-spec-r37.json"
GATE_REL = "plans/pkg_gate.py"
PROBE_REL = "plans/git_webserver_probe.py"
PROBE_SHA256 = "63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf"
DRY_REL = "corpus/evidence/round37/git-webserver-dry-cases-freeze.txt"
DRY_SHA256 = "0095e59121a70a5fa6ec8c02ae4a1b30cb2c2b0f335c5e6ad62c650dca4b66f3"
NCASES = 22
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


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
    spec = json.loads((lane / SPEC_REL).read_text())
    spec["receipt_sha256"] = sha256(lane / spec["receipt"]) or "absent"
    sp = pathlib.Path(work) / "pkg-spec-r37-effective.json"
    sp.write_text(json.dumps(spec))
    r = subprocess.run([sys.executable, str(lane / GATE_REL), "package", "--root", str(lane), "--spec", str(sp),
                        "--rerun", "--require-clean-tree"], capture_output=True, text=True, timeout=900)
    for l in r.stdout.splitlines():
        print("    gate: " + l)
    return r.returncode == 0, f"gate_exit={r.returncode}"


def rows(lane):
    out = {}
    for line in (lane / "corpus/SOURCES.md").read_text().splitlines():
        m = SOURCE_ROW.match(line)
        if m:
            out.setdefault(m.group(1), []).append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def v3(lane):
    spec = json.loads((lane / SPEC_REL).read_text())
    reg, bad = rows(lane), []
    for sid, row in spec["rows"].items():
        found = reg.get(sid, [])
        if len(found) != 1 or len(found[0]) != 11:
            bad.append(f"{sid}:row")
            continue
        toks = re.findall(r"sha256\s+([0-9a-fA-F]+)", found[0][5])
        if toks != [row["sha256"]]:
            bad.append(f"{sid}:anchor_digest")
    return not bad, f"rows={len(spec['rows'])} bad={bad or 0}"


def v4(lane):
    spec = json.loads((lane / SPEC_REL).read_text())
    try:
        text = (lane / spec["receipt"]).read_text()
        entry = (lane / spec["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    frozen_ids = [l.split()[1] for l in (lane / DRY_REL).read_text().splitlines() if l.startswith("CASE ")]
    cases = [l for l in text.splitlines() if l.startswith("CASE ")]
    ids = [l.split()[1] for l in cases]
    obs = [re.search(r" observed=(pass|fail)\b", l) for l in cases]
    no = [l.split()[1] for l in cases if " match=NO " in l]
    summ = [SUMMARY.match(l) for l in text.splitlines() if SUMMARY.match(l)]
    bad = []
    if ids != frozen_ids or len(ids) != NCASES:
        bad.append("case ids differ from the frozen table")
    if len(summ) != 1:
        bad.append("summary line count != 1")
    else:
        n, p, f, m = map(int, summ[0].groups())
        cp = sum(1 for o in obs if o and o.group(1) == "pass")
        cf = sum(1 for o in obs if o and o.group(1) == "fail")
        if not (n == NCASES and p + f == NCASES and p == cp and f == cf and m == len(no)):
            bad.append("summary disagrees with the CASE lines")
    unnamed = [c for c in no if c not in entry]
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


def v7(lane):
    spec = json.loads((lane / SPEC_REL).read_text())
    try:
        text = (lane / spec["receipt"]).read_text()
        entry = (lane / spec["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    observed = {}
    for l in text.splitlines():
        m = re.match(r"^CASE (\S+) .* observed=(pass|fail)\b", l)
        if m:
            observed[m.group(1)] = m.group(2)
    sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    if not sec:
        return False, "no '## Requirement map' section"
    covered, bad, nrows = set(), [], 0
    for l in sec.group(1).splitlines():
        m = re.match(r"^\|\s*`instruction\.md:(\d+)(?:-(\d+))?`\s*\|\s*(enforced|unenforced|partly)\s*\|(.*)\|\s*$", l)
        if not m:
            if l.startswith("|") and "instruction.md:" in l:
                bad.append(f"unparsed row {l[:40]!r}")
            continue
        nrows += 1
        lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
        covered |= set(range(lo, hi + 1))
        cited = re.findall(r"`([a-z0-9-]+)`", m.group(4))
        verdicts = {observed.get(c) for c in cited}
        if not cited or None in verdicts:
            bad.append(f"instruction.md:{lo}: cites no case or an unknown case")
        elif m.group(3) == "enforced" and "fail" not in verdicts:
            bad.append(f"instruction.md:{lo}: enforced without a failing case")
        elif m.group(3) == "unenforced" and "pass" not in verdicts:
            bad.append(f"instruction.md:{lo}: unenforced without a passing case")
        elif m.group(3) == "partly" and verdicts != {"pass", "fail"}:
            bad.append(f"instruction.md:{lo}: partly without one passing and one failing case")
    missing = sorted(set(range(1, 10)) - covered)
    if missing:
        bad.append(f"instruction lines not mapped: {missing}")
    return not bad, f"rows={nrows} bad={bad or 0}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    with tempfile.TemporaryDirectory(prefix="k37-c2-", dir=a.work) as work:
        checks = [("V1", lambda: v1(lane)), ("V2", lambda: v2(lane, work)), ("V3", lambda: v3(lane)),
                  ("V4", lambda: v4(lane)), ("V5", lambda: v5(lane)), ("V6", lambda: v6(lane)),
                  ("V7", lambda: v7(lane))]
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
