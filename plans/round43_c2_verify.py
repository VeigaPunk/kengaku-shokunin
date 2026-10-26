#!/usr/bin/env python3
"""Round-43 C2 counter (coverage): the pinned Terminal-Bench 2.0 `feal-differential-cryptanalysis` grader admitted as a
knowledge package with an executed offline probe (a ninth grader class: the graded artefact is an agent-authored Python
MODULE that the grader imports into its own interpreter and calls, beside the reference C extension `feal_in_c` whose
`get_keys()` holds the answer; the verdict is the pytest exit status tests/test.sh rewards).

Frozen predicate (same sentence in plans/round-43-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round43_c2_verify.py --lane .` prints `checks=10 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.

Every input this counter reads that exists at the freeze is pinned here by digest: the spec template, the gate,
the probe, the frozen dry table and the twelve captures. V1-V9 are the round-42 counter's
(`plans/round42_c2_verify.py`), re-pointed at the round-43 package (V9's case-table row carries one test letter:
the grader has one test); no V1-V9 check is relaxed. V10 is new (round-42 closure R5, `R42CritClaims` §1,
`F42CritV9`: V9 is a consistency check an informed filler passes by copying the receipt into the case table).

  V1 capture manifest: corpus/evidence/round43/tb2-feal-differential-cryptanalysis/SHA256SUMS lists exactly the
     twelve captured files at their frozen digests and every file's bytes match.
  V2 package gate: plans/pkg-spec-r43.json at its freeze digest and plans/pkg_gate.py at its freeze digest;
     `pkg_gate.py package --rerun --require-clean-tree` accepts the package that spec defines (the counter fills
     `receipt_sha256` with the digest of the receipt it finds, so P2 is a presence check and authenticity rests on
     P10, the fresh probe run byte-compared to the receipt).
  V3 anchor digests: each of the spec's rows has an 11-cell registry row whose anchor cell carries exactly one
     `sha256 <64 hex>` token, equal to that row's own spec pin.
  V4 receipt: CASE lines whose ids equal the frozen case table in order, one summary line
     `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=<m>` that agrees with the CASE lines, and every
     `match=NO` case id named in the entry.
  V5 frozen probe: plans/feal_probe.py at its freeze digest and its `--dry` output byte-equal to
     corpus/evidence/round43/feal-dry-cases-freeze.txt (itself at its freeze digest).
  V6 census: `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` exits 0.
  V7 requirement map: the entry's `## Requirement map` table has exactly one row per frozen tag, each row
     `| `instruction.md:<L>` | `<tag>` | <label> | <cases> |` with <L> the tag's frozen line and the label DERIVED
     from every receipt case whose `violates=` set carries the tag (`enforced` iff all observed `fail`,
     `unenforced` iff all observed `pass`, `partly` otherwise), citing >=1 violating case id.
  V8 order (QUALITY Q30): `plans/order_check.py --lane <lane> --claims plans/round-43-claims.md --receipt
     <spec receipt>` exits 0 and prints `ORDER RESULT PASS`.
  V9 content consistency (round-42 V9): (a) the entry has a `## Case table` section holding exactly one row per
     receipt CASE, in receipt order, `| `<cid>` | <test letter> | <observed verdict> | <text> |`, letter and
     verdict equal to the receipt's; (b) every spec row id occurs in the entry outside its `source:` line; (c)
     PROVINCE.md has a line naming both `feal-differential-cryptanalysis` and the entry's file name; (d) the
     `## Frontier` section of corpus/README.md names `feal-differential-cryptanalysis`.
  V10 mechanism (new; the content a receipt does not carry): the entry has a `## Mechanism` section holding exactly
     one row per receipt CASE, in receipt order, `| `<cid>` | `<capture>:<line>` | “<quote>” |`, where
     `<capture>:<line>` is one of the source lines DECISIVE (below, frozen here before the first probe run) lists
     for that case and `<quote>` is at least two words found verbatim (whitespace-normalised) on that captured line.
     The receipt names no source line, so a filler that copies the receipt cannot pass V10 without reading the
     captures (freeze control `claims/control-c2-informed-filler.txt`: the case table copied from a synthetic
     receipt and every case pointed at the assert line -> V10 DEFECT; the same mirror with decisive lines -> V10 ok).
     DECISIVE is the L1's reading of the captures at the freeze; a decisive line it omits is a limit of this
     counter, named, never widened after data.

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

CAP = "corpus/evidence/round43/tb2-feal-differential-cryptanalysis"
CAPTURES = {
    "Dockerfile": "c40553e4cf830b7cd075a79dca1a29f5267c45c63b1cedb275383f58af356a30",
    "README.md": "887407c78513837d93f02231998419a0ce9b0cc0a0c600ed86cd30df5cb24e7f",
    "feal.c": "bd4e9fb31e38073414d8a1930b2e67bc59eaee17e52f58133f781d297073e885",
    "feal.h": "d3ebd83bfbdb86f3543bda72a0693aabe478c6880ef78cb4a8e6c2e5a779759e",
    "feal.py": "23cc077b9dce176a3aa3078681d1c8dff8c1b7959556c9457db57036d2885dfe",
    "feal_module.c": "1ae1c8a31b099b5742b35a3d6b1b70a2509d8d13d79ab74535e038e9a3379363",
    "instruction.md": "b4093780b283e5c9838997769fb7bca090e3f4cbbd2d7cb275ba60cdfd722572",
    "setup.py": "d1d8f08966670ac8bfc1a9cfa8c16a6915eef2153a44ad6502daec2da83e08aa",
    "solve.sh": "6846dd2877aac95bc0b35a65c3b522403d21491407e02f07b7060ab4071a9620",
    "task.toml": "dcb9f2f15047eee0be15ca18c39c357f89187a94aae6baeff276221e2383eecb",
    "test.sh": "106c27394c96343c03b4fbac14faac85542bce6628bccc66a5fe036d77f72daf",
    "test_outputs.py": "585780e76d98094ad118d096f8c78f2281352dc9826e3687c4de152659631a3d",
}
SPEC_REL = "plans/pkg-spec-r43.json"
SPEC_SHA256 = "92289fa4f8c411bcc0ce340a3b38a711da4968265ec8ee9f647c4ddda9512577"
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
PROBE_REL = "plans/feal_probe.py"
PROBE_SHA256 = "17d694ba1ba53879f53a9589e2f7da80a4daf19fc518fe2d9c1c1c21d0910e9d"
DRY_REL = "corpus/evidence/round43/feal-dry-cases-freeze.txt"
DRY_SHA256 = "64699418dc62c7e775699a676f134fbe804413c1b0482afe3e756a77dd6e5c5b"
ORDER_REL = "plans/order_check.py"
CLAIMS_REL = "plans/round-43-claims.md"
TASK = "feal-differential-cryptanalysis"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")
MAP_ROW = re.compile(r"^\|\s*`instruction\.md:(\d+)`\s*\|\s*`([a-z0-9-]+)`\s*\|\s*(enforced|unenforced|partly)\s*\|(.*)\|\s*$")
CASE_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|\s*([PF])\s*\|\s*(pass|fail)\s*\|.*\|\s*$")
MECH_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|\s*`([A-Za-z0-9_.-]+):(\d+)`\s*\|\s*“(.+?)”\s*\|\s*$")


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
    sp = pathlib.Path(work) / "pkg-spec-r43-effective.json"
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
        cited = re.findall(r"`([a-z0-9_-]+)`", rest)
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
        m = re.match(r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF]) ", l)
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


# V10: the source lines that decide each frozen case (capture name -> 1-based line numbers), read by the L1 at the
# freeze from the captures pinned above. Keys equal the frozen dry table's case ids.
DECISIVE = {
    "nop": {"test_outputs.py": (24,)},                                   # import attack
    "oracle-solve-sh": {"solve.sh": (59, 63, 67, 68, 78, 90, 96)},      # 16-bit seed candidates, chosen pairs, filter
    "wrong-key": {"test_outputs.py": (30,)},                             # assert get_keys()[5] == stolen
    "oracle-off-by-one": {"test_outputs.py": (30,)},
    "return-str": {"test_outputs.py": (30,)},
    "cheat-import-get_keys": {"test_outputs.py": (23,), "feal_module.c": (25, 51)},  # /tests on sys.path; get_keys
    "cheat-always-equal": {"test_outputs.py": (30,)},                    # int == obj falls back to obj.__eq__
    "cheat-sysmodules-shadow": {"test_outputs.py": (24, 25)},            # attack imported before feal_in_c
    "cheat-patch-get_keys": {"test_outputs.py": (29, 30)},               # get_keys looked up after attack ran
    "cheat-exit-zero": {"test.sh": (17, 22, 25)},                        # reward = pytest exit status
    "cheat-clock-seed": {"feal.c": (60, 65, 66)},                        # srand(time(NULL)); 16-bit seeds
    "slow-oracle-45s": {"test_outputs.py": (29,), "task.toml": (22,)},   # untimed call; verifier timeout only
}


def norm(t):
    return " ".join(t.split())


def v10(lane):
    s = spec(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    _tags, frozen_ids = dry(lane)
    if sorted(DECISIVE) != sorted(frozen_ids):
        return False, "DECISIVE keys differ from the frozen case ids"
    want = [l.split()[1] for l in text.splitlines() if l.startswith("CASE ")]
    sec = re.search(r"^## Mechanism\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    if not sec:
        return False, "no '## Mechanism' section"
    got = [MECH_ROW.match(l).groups() for l in sec.group(1).splitlines() if MECH_ROW.match(l)]
    bad = []
    if [g[0] for g in got] != want or not want:
        bad.append(f"mechanism rows={len(got)} receipt cases={len(want)} ids_equal={[g[0] for g in got] == want}")
    capdir = lane / CAP
    for cid, cap, line, quote in got:
        allowed = DECISIVE.get(cid, {}).get(cap, ())
        if int(line) not in allowed:
            bad.append(f"{cid}:{cap}:{line} not decisive")
            continue
        if cap not in CAPTURES or sha256(capdir / cap) != CAPTURES[cap]:
            bad.append(f"{cid}:{cap} capture not pinned")
            continue
        lines = (capdir / cap).read_text().splitlines()
        q = norm(quote)
        if len(q.split()) < 2 or int(line) > len(lines) or q not in norm(lines[int(line) - 1]):
            bad.append(f"{cid}:{cap}:{line} quote not on the line")
    return not bad, f"mechanism_rows={len(got)}/{len(want)} bad={bad or 0}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="k43-c2-", dir=a.work) as work:
        checks = [("V1", lambda: v1(lane)), ("V2", lambda: v2(lane, work)), ("V3", lambda: v3(lane)),
                  ("V4", lambda: v4(lane)), ("V5", lambda: v5(lane)), ("V6", lambda: v6(lane)),
                  ("V7", lambda: v7(lane)), ("V8", lambda: v8(lane)), ("V9", lambda: v9(lane)), ("V10", lambda: v10(lane))]
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
