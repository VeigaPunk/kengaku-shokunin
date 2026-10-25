#!/usr/bin/env python3
"""Independent checker for the pinned Terminal-Bench 2.0 `protein-assembly` grader
(round 35, wave 1, seat R35IndepGrader).

Re-implements the assertions of the captured
corpus/evidence/round35/tb2-eval/test_outputs.py (test_gblock) from an independent
reading: own codon-translation table (standard genetic code, table 1), own rolling
GC-window loop, own assertion-order dispatch. It does NOT import the grader, does NOT
import the probe's run_grader, and does NOT require Biopython.

The 18 case contents are generated with the probe's own build_cases/components
(imported from plans/tb2_grader_probe.py — the frozen table of synthetic gblock
contents). Each case is scored here and compared against the committed receipt's
`observed=` and `assertion=` fields.

Usage: python3 .ufo/waves/round-35/build/R35IndepGrader/indep.py
Exit 0 iff all 18 cases agree on pass/fail and first failing assertion class.
"""
import hashlib
import importlib.util
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GRADER = LANE / "corpus/evidence/round35/tb2-eval/test_outputs.py"
PROBE = LANE / "plans/tb2_grader_probe.py"
RECEIPT = LANE / "corpus/evidence/round35/tb2-grader-probe.txt"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_SHA256 = "44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582"

# ---------------------------------------------------------------------------
# Own translation table: standard genetic code (NCBI translation table 1).
# ---------------------------------------------------------------------------
TABLE = {
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


def translate(nt):
    """Own translation: floor(len/3) codons, table 1, '*' for stops, 'X' unknown.
    Case-insensitive, like the grader's translate (which runs on a lowercased gblock)."""
    nt = nt.lower()
    return "".join(TABLE.get(nt[i:i + 3], "X") for i in range(0, len(nt) - 2, 3))


def extract_components(src):
    """Own extraction of the five AA literals from the grader source (data, not logic)."""
    ns = {}
    for line in src.splitlines():
        s = line.strip()
        for name in ("flag_aa", "donor_aa", "dhfr_aa", "acceptor_aa", "snap_aa"):
            if s.startswith(name + " = \"") and name not in ns:
                ns[name] = s.split('"')[1]
    missing = [n for n in ("flag_aa", "donor_aa", "dhfr_aa", "acceptor_aa", "snap_aa")
               if n not in ns]
    if missing:
        raise SystemExit(f"[indep] could not extract components from grader source: {missing}")
    return [ns[n] for n in ("flag_aa", "donor_aa", "dhfr_aa", "acceptor_aa", "snap_aa")]


# ---------------------------------------------------------------------------
# Own re-implementation of test_gblock's assertions (same order, same messages).
# ---------------------------------------------------------------------------
def score(content, components):
    """Score one gblock file content.

    Returns (pass_bool, assertion_message). The message is exactly the first failing
    assertion's message, or '-' on pass — mirroring the grader's assertion order:
    lines count -> alphabet -> length -> fusion order -> flag start -> linkers
    (chars then length, per pair) -> C terminus -> GC windows.
    """
    lines = [ln.rstrip() for ln in content.splitlines()]
    if len(lines) != 1:
        return False, "Invalid number of lines in gblock.txt."
    gblock = lines[0].lower()
    if not re.fullmatch(r"[atcg]+", gblock):
        return False, "gBlock must contain only A, T, C, G."
    if len(gblock) > 3000:
        return False, "gBlock must be at most 3000 nucleotides."

    aa = translate(gblock)
    flag, donor, dhfr, acceptor, snap = components
    flag_idx = aa.find(flag)
    donor_idx = aa.find(donor)
    dhfr_idx = aa.find(dhfr)
    acceptor_idx = aa.find(acceptor)
    snap_idx = aa.find(snap)
    if not (flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx):
        return False, "Fusion protein must be in the order flag - donor - dhfr - acceptor - snap"
    if flag_idx != 0:
        return False, "Start of gBlock must match flag protein."
    for start, end in [
        (flag_idx + len(flag), donor_idx),
        (donor_idx + len(donor), dhfr_idx),
        (dhfr_idx + len(dhfr), acceptor_idx),
        (acceptor_idx + len(acceptor), snap_idx),
    ]:
        linker = aa[start:end]
        if not re.fullmatch(r"[GS]+", linker):
            return False, "Linker must only contain G and S amino acids."
        if not (5 <= len(linker) <= 20):
            return False, "Linker must be between 5 and 20 amino acids long."
    if snap_idx + len(snap) != len(aa):
        return False, "End of gBlock must match snap protein."

    # Own rolling GC window: G/C count per 50-nt window must stay in 15..35.
    gc_count = sum(c in "gc" for c in gblock[:50])
    if not (15 <= gc_count <= 35):
        return False, "GC content must be between 30 and 70% in all 50 nucleotide windows."
    for i in range(50, len(gblock)):
        gc_count += (gblock[i] in "gc") - (gblock[i - 50] in "gc")
        if not (15 <= gc_count <= 35):
            return False, "GC content must be between 30 and 70% in all 50 nucleotide windows."
    return True, "-"


# ---------------------------------------------------------------------------
# Receipt parsing.
# ---------------------------------------------------------------------------
CASE_RE = re.compile(r"^case=(\S+) .* observed=(\S+) .* gcwin=(\S+) "
                     r"assertion='(.*?)' requirement=")


def parse_receipt(text):
    cases = {}
    for line in text.splitlines():
        m = CASE_RE.match(line)
        if m:
            # store (observed, assertion, gcwin); caller unpacks in that order
            cases[m.group(1)] = (m.group(2), m.group(4), m.group(3))
    return cases


def main():
    grader_src = GRADER.read_bytes()
    digest = hashlib.sha256(grader_src).hexdigest()
    if digest != GRADER_SHA256:
        print(f"REFUSE grader digest {digest} != pinned {GRADER_SHA256}")
        return 2

    # Load the probe module solely for its frozen case table (build_cases/components).
    spec = importlib.util.spec_from_file_location("tb2_probe", PROBE)
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)

    mine = extract_components(grader_src.decode())
    theirs = probe.components(grader_src.decode())

    cases = probe.build_cases(mine)
    receipt = parse_receipt(RECEIPT.read_text())

    if set(receipt) != {c[0] for c in cases}:
        print(f"REFUSE case table diverges from receipt: "
              f"receipt_only={sorted(set(receipt) - {c[0] for c in cases})} "
              f"probe_only={sorted({c[0] for c in cases} - set(receipt))}")
        return 2

    n = 0
    n_pass = 0
    n_fail = 0
    disagreements = []
    header = (f"grader={GRADER.relative_to(LANE)} sha256={digest} pin={PIN} "
              f"independent=yes (own table, own window loop, own dispatch)")
    print(header)
    lens = [len(p) for p in mine]
    max_nt = 3 * (sum(lens) + 4 * 20)
    print(f"components_aa={','.join(map(str, lens))} max_passing_nt={max_nt} cap_nt=3000")
    for name, content, pred, req in cases:
        obs, obs_assertion, obs_gcwin = receipt[name]
        ok, msg = score(content, mine)
        n += 1
        if ok:
            n_pass += 1
        else:
            n_fail += 1
        same_pass = ("pass" if ok else "fail") == obs
        same_assertion = (msg == obs_assertion) if not ok else (msg == "-" and obs_assertion == "-")
        if not (same_pass and same_assertion):
            disagreements.append((name, obs, obs_assertion, ok, msg))
        print(f"case={name} predicted={pred} observed={obs} indep={'pass' if ok else 'fail'} "
              f"match={'yes' if same_pass and same_assertion else 'NO'} "
              f"assertion={msg!r} receipt_assertion={obs_assertion!r} requirement={req!r}")

    print(f"cases={n} observed_pass={n_pass} observed_fail={n_fail} disagreements={len(disagreements)}")
    for name, obs, obs_a, ok, msg in disagreements:
        print(f"DISAGREE case={name} receipt=({obs},{obs_a!r}) indep=({'pass' if ok else 'fail'},{msg!r})")
    return 0 if not disagreements else 1


if __name__ == "__main__":
    sys.exit(main())
