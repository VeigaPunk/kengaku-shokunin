#!/usr/bin/env python3
"""Round-41 C2 counter (coverage): the pinned Terminal-Bench 2.0 `constraints-scheduling` grader admitted as a
knowledge package with an executed offline probe (a seventh grader class: the verdict is computed by a scheduling
model embedded in the grader — `_hard_ok`, `_overlap`, a minute-granularity scan — over three sha256-pinned
input calendars, and the graded artefact is a one-event ICS file).

Frozen predicate (same sentence in plans/round-41-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round41_c2_verify.py --lane .` prints `checks=8 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.

Every input this counter reads that exists at the freeze is pinned here by digest: the spec template, the
gate, the probe, the frozen dry table and the ten captures. V1-V7 are the round-40 counter's
(`plans/round40_c2_verify.py`), re-pointed at the round-41 package; no V1-V7 check is relaxed. V8 is new
(round-40 wave-2 `F40CritPlanNext` D9: a green round-40 run must not be re-filable as this round's evidence):
the receipt must be ordered after this freeze by the lane's own order gate.

  V1 capture manifest: corpus/evidence/round41/tb2-constraints-scheduling/SHA256SUMS lists exactly the ten captured
     files at their frozen digests and every file's bytes match.
  V2 package gate: plans/pkg-spec-r41.json at its freeze digest and plans/pkg_gate.py at its freeze digest;
     `pkg_gate.py package --rerun --require-clean-tree` accepts the package that spec defines (the counter
     fills `receipt_sha256` with the digest of the receipt it finds, so P2 is a presence check and
     authenticity rests on P10, the fresh probe run byte-compared to the receipt).
  V3 anchor digests: each of the spec's rows has an 11-cell registry row whose anchor cell carries exactly
     one `sha256 <64 hex>` token, equal to that row's own spec pin (the token is bound to the capture its
     row names, not to any committed digest — round-37 closure routed item D3).
  V4 receipt: CASE lines whose ids equal the frozen case table in order, one summary line
     `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=<m>` that agrees with the CASE lines, and
     every `match=NO` case id named in the entry.
  V5 frozen probe: plans/constraints_probe.py at its freeze digest and its `--dry` output byte-equal to
     corpus/evidence/round41/constraints-dry-cases-freeze.txt (itself at its freeze digest).
  V6 census: `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` exits 0.
  V7 requirement map (round-37 closure routed item D2): the entry's `## Requirement map` table has exactly
     one row per frozen tag (the dry table's TAG lines), each row
     `| `instruction.md:<L>` | `<tag>` | <label> | <cases> |` with <L> the tag's frozen line; its label must
     equal the label DERIVED from every receipt case whose `violates=` set carries the tag — `enforced` iff
     all of them are observed `fail`, `unenforced` iff all are observed `pass`, `partly` otherwise — and the
     row must cite >=1 case id in backticks, every cited id being one of those violating cases. A label
     chosen from one convenient witness (round 37: `enforced` beside an observed-pass violating case) fails.
  V8 order (QUALITY Q30; `F40CritPlanNext` D9): `plans/order_check.py --lane <lane> --claims
     plans/round-41-claims.md --receipt <spec receipt>` exits 0 and prints `ORDER RESULT PASS` — the receipt is
     first committed after the freeze commit that adds the claims file, and no freeze-time claims/ file shows
     the probe executed.

`--work DIR` is created if absent before the scratch directory is made inside it (the round-40 counter raised
FileNotFoundError on an absent --work: `corpus/lessons/round-40.md` §Mistakes, `F40CritPlanNext` D10(b)).

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

CAP = "corpus/evidence/round41/tb2-constraints-scheduling"
CAPTURES = {
    "Dockerfile": "7d9aba072a4a907229728b9739c8cf821fc2c98450babd64452682caf3759c84",
    "README.md": "d54a690970149e1216bd4fc066b45069c7948c13e3b1ef2a213a74342805f209",
    "alice_calendar.ics": "5a5d45804bffd339c2479d49e76fe817b38244d14d389afe1de583443808ecbc",
    "bob_calendar.ics": "c97e85dbcdd756758f8a80f4db5fd5c1dcacee79298e4d2262f46de5ff680b50",
    "carol_calendar.ics": "32a0f8687637df0a12b8e5c56d49c4192bc3e790856943632d70f237c7c1363b",
    "instruction.md": "342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6",
    "solve.sh": "802d81ec064fad3050bbade95a2f847ac24e0b7f80fa69b0bcee0347dc92fe77",
    "task.toml": "7b9842de16d74e8faf8c7c0aa03b0b81145941cb12dd322d81ae23fc48607250",
    "test.sh": "4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334",
    "test_outputs.py": "1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1",
}
SPEC_REL = "plans/pkg-spec-r41.json"
SPEC_SHA256 = "8e96421d91080d220cd8976abf62a1499b8a1bc92eb5d36eb0f55179b065d0dd"
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
PROBE_REL = "plans/constraints_probe.py"
PROBE_SHA256 = "8c471fbd0d83450793271d75fe3735a735226a725a73e0f16e02034e9d3c7242"
DRY_REL = "corpus/evidence/round41/constraints-dry-cases-freeze.txt"
DRY_SHA256 = "a656ce9b9adb4e88bb49b6a8a45064a8c4f459cffbbf76d70cca7f43a0c77a03"
ORDER_REL = "plans/order_check.py"
CLAIMS_REL = "plans/round-41-claims.md"
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
    sp = pathlib.Path(work) / "pkg-spec-r41-effective.json"
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
        if not (n == len(frozen_ids) and p + f == n and p == cp and f == cf):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="k41-c2-", dir=a.work) as work:
        checks = [("V1", lambda: v1(lane)), ("V2", lambda: v2(lane, work)), ("V3", lambda: v3(lane)),
                  ("V4", lambda: v4(lane)), ("V5", lambda: v5(lane)), ("V6", lambda: v6(lane)),
                  ("V7", lambda: v7(lane)), ("V8", lambda: v8(lane))]
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
