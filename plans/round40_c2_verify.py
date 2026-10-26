#!/usr/bin/env python3
"""Round-40 C2 counter (coverage): the pinned Terminal-Bench 2.0 `db-wal-recovery` grader admitted as a
knowledge package with an executed offline probe (a sixth grader class: a binary database file pair — SQLite
main database plus an XOR-encrypted write-ahead log — whose graded output is a JSON export).

Frozen predicate (same sentence in plans/round-40-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round40_c2_verify.py --lane .` prints `checks=7 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.

Every input this counter reads that exists at the freeze is pinned here by digest: the spec template, the
gate, the probe, the frozen dry table and the seven captures. The checks V1-V7 are the round-39 counter's
(`plans/round39_c2_verify.py`), re-pointed at the round-40 package; no check is added or relaxed.

  V1 capture manifest: corpus/evidence/round40/tb2-db-wal-recovery/SHA256SUMS lists exactly the eight captured
     files at their frozen digests and every file's bytes match.
  V2 package gate: plans/pkg-spec-r40.json at its freeze digest and plans/pkg_gate.py at its freeze digest;
     `pkg_gate.py package --rerun --require-clean-tree` accepts the package that spec defines (the counter
     fills `receipt_sha256` with the digest of the receipt it finds, so P2 is a presence check and
     authenticity rests on P10, the fresh probe run byte-compared to the receipt).
  V3 anchor digests: each of the spec's rows has an 11-cell registry row whose anchor cell carries exactly
     one `sha256 <64 hex>` token, equal to that row's own spec pin (the token is bound to the capture its
     row names, not to any committed digest — round-37 closure routed item D3).
  V4 receipt: CASE lines whose ids equal the frozen case table in order, one summary line
     `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=<m>` that agrees with the CASE lines, and
     every `match=NO` case id named in the entry.
  V5 frozen probe: plans/db_wal_probe.py at its freeze digest and its `--dry` output byte-equal to
     corpus/evidence/round40/db-wal-dry-cases-freeze.txt (itself at its freeze digest).
  V6 census: `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` exits 0.
  V7 requirement map (round-37 closure routed item D2): the entry's `## Requirement map` table has exactly
     one row per frozen tag (the dry table's TAG lines), each row
     `| `instruction.md:<L>` | `<tag>` | <label> | <cases> |` with <L> the tag's frozen line; its label must
     equal the label DERIVED from every receipt case whose `violates=` set carries the tag — `enforced` iff
     all of them are observed `fail`, `unenforced` iff all are observed `pass`, `partly` otherwise — and the
     row must cite >=1 case id in backticks, every cited id being one of those violating cases. A label
     chosen from one convenient witness (round 37: `enforced` beside an observed-pass violating case) fails.
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

CAP = "corpus/evidence/round40/tb2-db-wal-recovery"
CAPTURES = {
    "Dockerfile": "63a260531c62f4ae72060db17f295c0aa03cfc6321f8162c324b7aa6b3f81302",
    "instruction.md": "5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26",
    "main.db": "68cb288eb29e76d814b4e7ee6887b37c415675e644f88173bc191348e290d119",
    "main.db-wal.encrypted": "68753bdce26196a53194260d001544cc6bb8f9f38e2f2f6826d09798e31e6e26",
    "solve.sh": "ed8530c94103bf19783a1d41bc63fe4db478cdd9629f22fee25c45a45699f5e8",
    "task.toml": "1cdc2c615e259bc10265efbe71b518332070c1c002e226566399e9788f18d0aa",
    "test.sh": "4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334",
    "test_outputs.py": "88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49",
}
SPEC_REL = "plans/pkg-spec-r40.json"
SPEC_SHA256 = "4af78f4fd888fbd6f80425633c32d8ae07627669e08aaf8c62c3868d85838e78"
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
PROBE_REL = "plans/db_wal_probe.py"
PROBE_SHA256 = "69af65dfe4e2ecab9aec534c68a0bb2b071faf845f09b9ccff4a92e213e19ff3"
DRY_REL = "corpus/evidence/round40/db-wal-dry-cases-freeze.txt"
DRY_SHA256 = "688f34750eeb0977026dc8d10e036d5a661297297f5d81ef81f79604347044f2"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")
MAP_ROW = re.compile(r"^\|\s*`instruction\.md:(\d+)`\s*\|\s*`([a-z0-9-]+)`\s*\|\s*(enforced|unenforced|partly)\s*\|(.*)\|\s*$")


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
    sp = pathlib.Path(work) / "pkg-spec-r40-effective.json"
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    with tempfile.TemporaryDirectory(prefix="k40-c2-", dir=a.work) as work:
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
