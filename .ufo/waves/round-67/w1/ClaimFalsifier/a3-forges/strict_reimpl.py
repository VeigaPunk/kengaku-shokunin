#!/usr/bin/env python3
"""A3 scratch re-implementation of the frozen s1-s6 strict clauses (round-67-claims.md).

NOT the C2 deliverable: ClaimFalsifier-5 re-implements the clause set exactly as frozen, to test
which fixture fields the clause set binds. Cases G1-G5 only, per the claims text.
"""
import hashlib
import pathlib
import re
import sys

L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = L / "plans/round65_c1_sqlite_probe.py"
GRADER = L / "corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py"

# clause values are read from the committed probe bytes via import (side-effect free)
import importlib.util
_spec = importlib.util.spec_from_file_location("r65probe_committed", PROBE)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
PROBE_VERSION = _mod.PROBE_VERSION
GRADER_SHA256 = _mod.GRADER_SHA256
AMALG_SHA256 = _mod.AMALG_SHA256
FROZEN_VECTORS = {k: "/".join(v) for k, v in _mod.FROZEN_VECTORS.items()}
CASES = [c.name for c in _mod.CASES]
VER_RE = re.compile(r"\d+\.\d+(\.\d+)?")


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def strict_failures(text):
    f = []
    lines = text.splitlines()

    # s1: instrument header version equals PROBE_VERSION from the committed probe bytes
    hdr = next((l for l in lines
                if l.startswith("# instrument plans/round65_c1_sqlite_probe.py version=")), None)
    if hdr is None:
        f.append("s1 instrument-header-missing")
    else:
        v = hdr.rsplit("version=", 1)[1].strip()
        if v != PROBE_VERSION:
            f.append("s1 instrument-version %s != %s" % (v, PROBE_VERSION))

    # s2: GRADER sha equals the frozen sha AND the committed grader bytes carry it
    g = next((l for l in lines if l.startswith("GRADER ")), "")
    m = re.search(r"sha256=([0-9a-f]{64})", g)
    if not m:
        f.append("s2 grader-sha-missing")
    else:
        if m.group(1) != GRADER_SHA256:
            f.append("s2 grader-sha %s != %s" % (m.group(1), GRADER_SHA256))
        if not GRADER.exists() or sha256(GRADER) != GRADER_SHA256:
            f.append("s2 committed-grader-bytes-do-not-carry-the-sha")

    # s3: AMALG sha equals the frozen amalgamation sha
    a = next((l for l in lines if l.startswith("AMALG ")), "")
    m = re.search(r"sha256=([0-9a-f]{64})", a)
    if not m:
        f.append("s3 amalg-sha-missing")
    elif m.group(1) != AMALG_SHA256:
        f.append("s3 amalg-sha %s != %s" % (m.group(1), AMALG_SHA256))

    # s4: TOOLCHAIN gcc/gcov/bwrap not 'fabricated' and equal to CC/GCOV/BWRAP line tokens
    t = next((l for l in lines if l.startswith("TOOLCHAIN ")), "")
    tok = dict(kv.split("=", 1) for kv in t.split()[1:] if "=" in kv)
    cc = next((l for l in lines if l.startswith("CC ")), "")
    gc = next((l for l in lines if l.startswith("GCOV ")), "")
    bw = next((l for l in lines if l.startswith("BWRAP ")), "")
    cc_v = next((x for x in cc.split() if VER_RE.fullmatch(x)), None)
    gc_v = next((x for x in gc.split() if VER_RE.fullmatch(x)), None)
    bw_v = next((x for x in bw.split() if VER_RE.fullmatch(x)), None)
    for field, ref in (("gcc", cc_v), ("gcov", gc_v), ("bwrap", bw_v)):
        val = tok.get(field)
        if val is None or val == "fabricated":
            f.append("s4 toolchain-%s missing-or-fabricated" % field)
        elif ref is None:
            f.append("s4 no version token on %s line" % field.upper())
        elif val != ref:
            f.append("s4 toolchain-%s %s != %s-line %s" % (field, val, field.upper(), ref))
    # python is NOT cross-checked (named limitation in the claims text)

    # s5: RUN rc=0 + frozen driver; per-case NOBIND delta=0; BUILD/FILES/ENV present
    for case in CASES:
        run = next((l for l in lines if l.startswith("RUN %s " % case)), None)
        if run is None:
            f.append("s5 %s RUN-line-missing" % case)
        else:
            if "rc=0" not in run:
                f.append("s5 %s RUN rc!=0" % case)
            if 'driver="/usr/bin/python3 /ctl/driver.py"' not in run:
                f.append("s5 %s RUN driver-not-frozen" % case)
        nb = next((l for l in lines if l.startswith("NOBIND %s " % case)), None)
        if nb is None:
            f.append("s5 %s NOBIND-line-missing" % case)
        elif "delta=0" not in nb:
            f.append("s5 %s NOBIND delta!=0" % case)
        for prefix in ("BUILD %s " % case, "FILES %s " % case, "ENV %s " % case):
            if not any(l.startswith(prefix) for l in lines):
                f.append("s5 %s %s-line-missing" % (case, prefix.split()[0]))

    # s6: every VECTOR line equals the probe's frozen table
    declared = {}
    for l in lines:
        if l.startswith("VECTOR "):
            body = l[len("VECTOR "):]
            if "=" in body:
                name, vec = body.split("=", 1)
                declared[name] = vec
    for case in CASES:
        if case not in declared:
            f.append("s6 %s vector-line-missing" % case)
        elif declared[case] != FROZEN_VECTORS.get(case):
            f.append("s6 %s vector %s != frozen %s"
                     % (case, declared[case], FROZEN_VECTORS.get(case)))
    return f


def main():
    rc = 0
    for path in sys.argv[1:]:
        p = pathlib.Path(path)
        fails = strict_failures(p.read_text())
        for x in fails:
            print("CHECK defect: %s (%s)" % (x, p.name))
        print("strict-reimpl %s: %s" % (p.name, "ACCEPT" if not fails else "REFUSE"))
        if fails:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
