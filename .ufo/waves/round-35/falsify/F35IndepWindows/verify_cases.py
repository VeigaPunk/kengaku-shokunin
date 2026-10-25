#!/usr/bin/env python3
"""F35IndepWindows -- independent verification of tb2_grader_probe.build_cases.

Each case content is re-derived from build_cases(parts) (parts pulled from the captured
grader bytes).  For every case we independently compute:
  (a) translation with OUR OWN explicit 64-codon table (no use of probe CODONS),
  (b) min/max GC over every full 50-nt window,
  (c) the full set of violated grader requirements, compared with the case label's claim.

Findings = cases whose failure is confounded by a second (or third) violation.
"""
import os
import re
import sys
import pathlib

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRATCH = pathlib.Path(__file__).resolve().parent
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
sys.path.insert(0, str(SCRATCH))

import tb2_grader_probe as probe  # noqa: E402  (imported from scratch copy)

# ---------------------------------------------------------------- our own codon table
# Standard genetic code, written out explicitly (64 codons + stops -> '*', ambiguity -> 'X').
MY_CODONS = {
    "ttt": "F", "ttc": "F", "tta": "L", "ttg": "L",
    "tct": "S", "tcc": "S", "tca": "S", "tcg": "S",
    "tat": "Y", "tac": "Y", "taa": "*", "tag": "*",
    "tgt": "C", "tgc": "C", "tga": "*", "tgg": "W",
    "ctt": "L", "ctc": "L", "cta": "L", "ctg": "L",
    "cct": "P", "ccc": "P", "cca": "P", "ccg": "P",
    "cat": "H", "cac": "H", "caa": "Q", "cag": "Q",
    "cgt": "R", "cgc": "R", "cga": "R", "cgg": "R",
    "att": "I", "atc": "I", "ata": "I", "atg": "M",
    "act": "T", "acc": "T", "aca": "T", "acg": "T",
    "aat": "N", "aac": "N", "aaa": "K", "aag": "K",
    "agt": "S", "agc": "S", "aga": "R", "agg": "R",
    "gtt": "V", "gtc": "V", "gta": "V", "gtg": "V",
    "gct": "A", "gcc": "A", "gca": "A", "gcg": "A",
    "gat": "D", "gac": "D", "gaa": "E", "gag": "E",
    "ggt": "G", "ggc": "G", "gga": "G", "ggg": "G",
}


def my_translate(nt):
    out = []
    for i in range(0, len(nt) - 2, 3):
        c = nt[i:i + 3]
        if c in MY_CODONS:
            out.append(MY_CODONS[c])
        else:
            out.append("X")  # ambiguous/unknown codon (matches Biopython default)
    return "".join(out)


def gc(s):
    return sum(ch in "gc" for ch in s)


def window_stats(nt):
    mn, mx = 99, -1
    bad = 0
    if len(nt) >= 50:
        for i in range(len(nt) - 49):
            g = gc(nt[i:i + 50])
            mn = min(mn, g)
            mx = max(mx, g)
            bad += not (15 <= g <= 35)
    else:
        mn = mx = gc(nt)
    return mn, mx, bad


def extract_parts(src):
    ns = {}
    for m in re.finditer(r'^\s*(flag_aa|donor_aa|dhfr_aa|acceptor_aa|snap_aa)\s*=\s*"([^"]*)"', src, re.M):
        ns[m.group(1)] = m.group(2)
    return [ns[n] for n in ("flag_aa", "donor_aa", "dhfr_aa", "acceptor_aa", "snap_aa")]
def first_fail(lines, gblock, aa, idx, parts):
    """Replicates the grader's assertion ORDER to name the first failing assertion."""
    if len(lines) != 1:
        return "Invalid number of lines in gblock.txt."
    if not re.fullmatch(r"[atcg]+", gblock):
        return "gBlock must contain only A, T, C, G."
    if len(gblock) > 3000:
        return "gBlock must be at most 3000 nucleotides."
    flag, donor, dhfr, acceptor, snap = parts
    fi, di, hi, ai, si = idx
    if not (fi < di < hi < ai < si):
        return "Fusion protein must be in the order flag - donor - dhfr - acceptor - snap"
    if fi != 0:
        return "Start of gBlock must match flag protein."
    for start, end, which in [(fi + len(flag), di, "flag-donor"), (di + len(donor), hi, "donor-dhfr"),
                              (hi + len(dhfr), ai, "dhfr-acceptor"), (ai + len(acceptor), si, "acceptor-snap")]:
        linker = aa[start:end]
        if not re.fullmatch(r"[GS]+", linker):
            return "Linker must only contain G and S amino acids."
        if not (5 <= len(linker) <= 20):
            return "Linker must be between 5 and 20 amino acids long."
    if si + len(snap) != len(aa):
        return "End of gBlock must match snap protein."
    mn, mx, bad = window_stats(gblock)
    if bad:
        return "GC content must be between 30 and 70% in all 50 nucleotide windows."
    return "-"


def evaluate_case(name, content, parts):
    """Returns (violated-set, first-fail-message, window-stats, aa-len)."""
    flag, donor, dhfr, acceptor, snap = parts
    lines = content.splitlines()
    gblock = lines[0].lower() if lines else ""
    aa = my_translate(gblock)
    fi = aa.find(flag)
    di = aa.find(donor)
    hi = aa.find(dhfr)
    ai = aa.find(acceptor)
    si = aa.find(snap)
    idx = (fi, di, hi, ai, si)
    V = set()  # violated requirement ids
    # R1 exactly one line
    if len(lines) != 1:
        V.add("lines")
    # R2 alphabet
    if not re.fullmatch(r"[atcg]+", gblock):
        V.add("alphabet")
    # R3 length
    if len(gblock) > 3000:
        V.add("length")
    # R4 order (raw indices, as the grader computes them)
    if not (fi < di < hi < ai < si):
        V.add("order")
    # R5 flag at 0
    if fi != 0:
        V.add("flag0")
    # R6/R7 linkers (only well-defined when all five parts are found in order)
    if fi < di < hi < ai < si:
        for start, end in [(fi + len(flag), di), (di + len(donor), hi),
                           (hi + len(dhfr), ai), (ai + len(acceptor), si)]:
            linker = aa[start:end]
            if not re.fullmatch(r"[GS]+", linker):
                V.add("linkGS")
            if not (5 <= len(linker) <= 20):
                V.add("linklen")
    # R8 snap ends protein
    if si + len(snap) != len(aa):
        V.add("snapend")
    # R9 GC windows
    mn, mx, bad = window_stats(gblock)
    if bad:
        V.add("gcwin")
    return V, first_fail(lines, gblock, aa, idx, parts), (mn, mx, bad), len(aa)


# ------------------------------------------------------------------ load and align parts
src_bytes = (LANE / "corpus/evidence/round35/tb2-eval/test_outputs.py").read_bytes()
src = src_bytes.decode()
parts_mine = extract_parts(src)
parts_probe = probe.components(src)
if parts_mine != parts_probe:
    for i, (a, b) in enumerate(zip(parts_probe, parts_mine)):
        if a != b:
            print("DIFF idx=%d len_probe=%d len_mine=%d\n  probe=%r\n  mine =%r" % (i, len(a), len(b), a[:40], b[:40]))
    raise SystemExit(1)
parts = parts_mine
print("parts_aa=" + ",".join(map(str, map(len, parts))))

cases = probe.build_cases(parts)
print("cases=%d" % len(cases))

# optional Biopython cross-check
try:
    from Bio.Seq import Seq
    BIO = True
except Exception:
    BIO = False
    print("BIO=unavailable")

if BIO:
    # per-codon agreement over all 64 codons + N-ambiguity
    mism = 0
    for c1 in "atcg":
        for c2 in "atcg":
            for c3 in "atcg":
                codon = c1 + c2 + c3
                if my_translate(codon) != str(Seq(codon).translate()):
                    mism += 1
    for ncod in ("ana", "nnt", "tna"):
        if my_translate(ncod) != str(Seq(ncod).translate()):
            mism += 1
    print("codon_table_mismatches_vs_Biopython=%d" % mism)

expected = {
    "valid-balanced": set(), "uppercase": set(), "no-trailing-newline": set(),
    "trailing-empty-line": {"lines"}, "start-codon-prefixed": {"flag0"},
    "stop-codon-appended": {"snapend"}, "linker-4aa": {"linklen"},
    "linker-21aa": {"linklen"}, "linker-20aa": set(), "linker-non-gs": {"linkGS"},
    "linker-g-only": set(), "n-terminal-linker": {"flag0"},
    "c-terminal-linker": {"snapend"}, "donor-acceptor-swapped": {"order"},
    "donor-one-substitution": {"order"}, "donor-repeated": {"length"},
    "non-acgt-base": {"alphabet"}, "gc-window-high": {"gcwin"},
}

findings = []
for name, content, pred, req in cases:
    V, ff, (mn, mx, bad), aalen = evaluate_case(name, content, parts)
    exp = expected[name]
    isolated = (V == exp) and (len(V) <= 1)
    confounded = bool(V - exp) or (len(V) > 1 and len(exp) == 1)
    if confounded or not isolated:
        findings.append((name, sorted(V), sorted(exp), pred, ff))
    print("case=%-22s nt=%-5d aa=%-4d gc=(%d,%d) nbad=%-3d firstfail=%-55s "
          "violated=%s expected=%s pred=%-4s isolated=%s"
          % (name, len(content.strip()), aalen, mn, mx, bad, ff, sorted(V), sorted(exp), pred, isolated))

print("\nFINDINGS (failure confounded by an extra violation, or mismatch with claim):")
for name, V, exp, pred, ff in findings:
    print("  - %s: violated=%s expected=%s firstfail=%r" % (name, V, exp, ff))

n_find = len(findings)
print("\nn_findings=%d n_cases=%d isolated=%d" % (n_find, len(cases), len(cases) - n_find))
