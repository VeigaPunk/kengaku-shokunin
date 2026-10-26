#!/usr/bin/env python3
"""probe_limits.py — F39AnchorFix: measure the three residual routes around the capture-unanchored leg.

L1: erratum laundering — fixture D (one token for two captures) + an append-only erratum line.
L2: provenance short-circuit — a row that names its URL capture *and* gains a PROVENANCE.md line for
    another capture; the URL capture never enters `per`.
L3: TOK-OUTSIDE detail text (token count includes tokens outside the anchor cell).
L4: SHA256SUMS-vs-bytes mismatches across corpus/evidence (manifest trust).
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
LANDED = str(LANE / "plans/anchor_digest_check.py")
FROZEN = sys.argv[2]
S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
S070 = "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd"
URL_RAW = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
           "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py")
ANCHOR_HEAD = " | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test_outputs.py:9-13"
LESSON = LANE / "corpus/lessons/round-38.md"
SOURCE = LANE / "corpus/SOURCES.md"
PROV = LANE / "corpus/evidence/round37/anchor-captures/PROVENANCE.md"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def restore(p, rel):
    p.write_bytes(subprocess.run(["git", "-C", str(LANE), "show", f"HEAD:{rel}"],
                                 capture_output=True).stdout)


def run(tool, verbose=False):
    r = subprocess.run([sys.executable, tool, "--lane", str(LANE)] + (["--verbose"] if verbose else []),
                       capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines(), r.stderr.strip()


def report(label, verbose=False):
    for name, tool in (("LANDED", LANDED), ("FROZEN", FROZEN)):
        rc, lines, err = run(tool, verbose)
        print(f"{name} exit={rc}")
        for l in lines:
            if l.startswith(("DEFECT", "rows=", "CAPTURES", "BIND")) and (
                    "S111" in l or l.startswith("rows=")):
                print(f"{name} | {l}")
        if err:
            print(f"{name} ! {err}")


def case_d(line):
    return line.replace(ANCHOR_HEAD, f" {URL_RAW}{ANCHOR_HEAD}").replace(S111, S108)


def case_a(line):
    return line.replace(S111, S108)


base = {p: sha(p) for p in (SOURCE, LESSON, PROV)}
try:
    print("==== L1a: D alone ====")
    t = SOURCE.read_text(encoding="utf-8")
    SOURCE.write_text("\n".join(case_d(l) if re.match(r"^ {0,3}\|\s*S111\s*\|", l) else l
                                for l in t.split("\n")), encoding="utf-8")
    report("D")
    restore(SOURCE, "corpus/SOURCES.md")

    print("\n==== L1b: D + erratum (cited_wrong = the row's current token, correction = its own capture digest) ====")
    SOURCE.write_text("\n".join(case_d(l) if re.match(r"^ {0,3}\|\s*S111\s*\|", l) else l
                                for l in t.split("\n")), encoding="utf-8")
    LESSON.write_text(LESSON.read_text(encoding="utf-8") +
                      f"\nErratum (round 37): S111 anchor sha256 {S108} is wrong; "
                      f"the correction is sha256 {S111}\n", encoding="utf-8")
    report("DER")
    restore(SOURCE, "corpus/SOURCES.md")
    restore(LESSON, "corpus/lessons/round-38.md")

    print("\n==== L1c: A + erratum (round-38 cross-row shape laundered) ====")
    SOURCE.write_text("\n".join(case_a(l) if re.match(r"^ {0,3}\|\s*S111\s*\|", l) else l
                                for l in t.split("\n")), encoding="utf-8")
    LESSON.write_text(LESSON.read_text(encoding="utf-8") +
                      f"\nErratum (round 37): S111 anchor sha256 {S108} is wrong; "
                      f"the correction is sha256 {S111}\n", encoding="utf-8")
    report("AER")
    restore(SOURCE, "corpus/SOURCES.md")
    restore(LESSON, "corpus/lessons/round-38.md")

    print("\n==== L2: provenance short-circuit — S111 row keeps its URL, gains a PROVENANCE.md line; token = the prov capture's digest ====")
    SOURCE.write_text("\n".join(
        (l.replace(S111, S070) if re.match(r"^ {0,3}\|\s*S111\s*\|", l) else l) for l in t.split("\n")),
        encoding="utf-8")
    PROV.write_text(PROV.read_text(encoding="utf-8") +
                    "| S111 | `S070-generate_test_data.py` | `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py` | `dce04686a56253aefba7b18a4fa0937cf1dc987b` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |\n",
                    encoding="utf-8")
    report("PROV", verbose=True)
    restore(SOURCE, "corpus/SOURCES.md")
    restore(PROV, "corpus/evidence/round37/anchor-captures/PROVENANCE.md")

    print("\n==== L3: TOK-OUTSIDE detail ====")
    mut = (lambda l: l.replace(ANCHOR_HEAD, f" {URL_RAW}{ANCHOR_HEAD}")
           .replace(f"; sha256 {S111}", "")
           .replace(f" {URL_RAW}{ANCHOR_HEAD}", f" {URL_RAW} sha256 {S111}{ANCHOR_HEAD}"))
    SOURCE.write_text("\n".join(mut(l) if re.match(r"^ {0,3}\|\s*S111\s*\|", l) else l
                                for l in t.split("\n")), encoding="utf-8")
    report("TOKOUT")
    restore(SOURCE, "corpus/SOURCES.md")
finally:
    for p, h in base.items():
        rel = p.relative_to(LANE).as_posix()
        restore(p, rel)
        assert sha(p) == h, rel
    dirty = subprocess.run(["git", "-C", str(LANE), "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    print(f"\nRESTORED all; status-lines={len(dirty.splitlines()) if dirty else 0}")

print("\n==== L4: SHA256SUMS entry vs file bytes ====")
paths = subprocess.run(["git", "-C", str(LANE), "ls-tree", "-r", "--name-only", "HEAD",
                        "--", "corpus/evidence"], capture_output=True, text=True).stdout.split()
bad = 0
for p in paths:
    d, _, b = p.rpartition("/")
    sums = f"{d}/SHA256SUMS"
    blobs = subprocess.run(["git", "-C", str(LANE), "cat-file", "--batch"],
                           input=("HEAD:" + p + "\nHEAD:" + sums + "\n").encode(),
                           capture_output=True).stdout
print("manifest check delegated to inline python below")
