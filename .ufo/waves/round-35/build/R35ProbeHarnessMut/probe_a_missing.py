#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `protein-assembly` grader (round 35, C1).

Loads the captured `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88) from the lane's committed
capture, refuses unless its SHA-256 equals the pinned digest, and runs its `test_gblock()` on a
frozen table of synthetic `/app/gblock.txt` contents. Each case names the `instruction.md`
requirement it exercises and a prediction (pass/fail) written from a static reading of the
grader BEFORE the first run. Output is deterministic; the C1 counter re-runs it and byte-compares
the committed receipt.

The grader imports Biopython; test.sh pins biopython==1.85. Run as:
  uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
This executes scoring code on synthetic inputs only: no model, no container, no task certification.
"""
import argparse
import hashlib
import importlib.util
import pathlib
import sys
import tempfile

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round35/tb2-eval/test_outputs.py"
GRADER_SHA256 = "44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582"

# Standard genetic code, codons grouped per amino acid (no stops: never emitted by the builder).
CODONS = {
    "A": ["gct", "gcc", "gca", "gcg"], "R": ["cgt", "cgc", "cga", "cgg", "aga", "agg"],
    "N": ["aat", "aac"], "D": ["gat", "gac"], "C": ["tgt", "tgc"], "Q": ["caa", "cag"],
    "E": ["gaa", "gag"], "G": ["ggt", "ggc", "gga", "ggg"], "H": ["cat", "cac"],
    "I": ["att", "atc", "ata"], "L": ["tta", "ttg", "ctt", "ctc", "cta", "ctg"], "K": ["aaa", "aag"],
    "M": ["atg"], "F": ["ttt", "ttc"], "P": ["cct", "ccc", "cca", "ccg"],
    "S": ["tct", "tcc", "tca", "tcg", "agt", "agc"], "T": ["act", "acc", "aca", "acg"],
    "W": ["tgg"], "Y": ["tat", "tac"], "V": ["gtt", "gtc", "gta", "gtg"],
}


def gc(s):
    return sum(c in "gc" for c in s)


def windows_ok(nt):
    """Independent re-statement of the grader's sliding rule: every full 50-nt window has 15..35 G/C."""
    return len(nt) >= 50 and all(15 <= gc(nt[i:i + 50]) <= 35 for i in range(len(nt) - 49))


def back_translate(aa, mode="balanced"):
    """Deterministic reverse translation. `balanced` keeps the running 50-nt window near 50% GC;
    `high` takes the max-GC codon for every residue (used to force a GC-window violation)."""
    out = ""
    for res in aa:
        opts = sorted(CODONS[res])
        if mode == "high":
            pick = max(opts, key=lambda c: (gc(c), c))
        else:
            tail = out[-47:]

            def score(c):
                w = tail + c
                return (abs(gc(w) / len(w) - 0.5), c)

            pick = min(opts, key=score)
        out += pick
    return out


def components(mod_src):
    """Pull the five literal components out of the grader source (same bytes the grader uses)."""
    ns = {}
    for line in mod_src.splitlines():
        s = line.strip()
        for name in ("flag_aa", "donor_aa", "dhfr_aa", "acceptor_aa", "snap_aa"):
            if s.startswith(name + " = "):
                ns[name] = s.split('"')[1]
    return [ns[n] for n in ("flag_aa", "donor_aa", "dhfr_aa", "acceptor_aa", "snap_aa")]


def fusion(parts, linkers):
    aa = parts[0]
    for lk, p in zip(linkers, parts[1:]):
        aa += lk + p
    return aa


def build_cases(parts):
    flag, donor, dhfr, acceptor, snap = parts
    L = ["GGGGS"] * 4
    valid_aa = fusion(parts, L)
    valid = back_translate(valid_aa)
    # High-GC stretch: re-code the first 40 residues of DHFR with max-GC codons, rest balanced.
    pre = fusion([flag, donor], L[:1]) + L[1]
    hi = back_translate(pre) + back_translate(dhfr[:40], "high") + back_translate(
        dhfr[40:] + L[2] + acceptor + L[3] + snap)
    mutant_donor = donor[:10] + ("A" if donor[10] != "A" else "G") + donor[11:]
    # (name, file bytes, prediction, instruction requirement exercised)
    return [
        ("valid-balanced", valid + "\n", "pass", "all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt"),
        ("uppercase", valid.upper() + "\n", "pass", "file holds only the sequence (case is not specified)"),
        ("no-trailing-newline", valid, "pass", "file holds only the sequence"),
        ("trailing-empty-line", valid + "\n\n", "fail", "No empty lines"),
        ("start-codon-prefixed", "atg" + valid + "\n", "fail", "no start codon / remove N-terminal Met"),
        ("stop-codon-appended", valid + "taa\n", "fail", "no stop codon"),
        ("linker-4aa", back_translate(fusion(parts, ["GGGS"] + L[1:])) + "\n", "fail", "linkers 5..20 aa"),
        ("linker-21aa", back_translate(fusion(parts, ["GGGGS" * 4 + "G"] + L[1:])) + "\n", "fail", "linkers 5..20 aa"),
        ("linker-20aa", back_translate(fusion(parts, ["GGGGS" * 4] + L[1:])) + "\n", "pass", "linkers 5..20 aa (upper bound inclusive)"),
        ("linker-non-gs", back_translate(fusion(parts, ["GGAGS"] + L[1:])) + "\n", "fail", "only GS linkers between subproteins"),
        ("linker-g-only", back_translate(fusion(parts, ["GGGGG"] + L[1:])) + "\n", "pass", "GS linkers (a G-only linker is not distinguished)"),
        ("n-terminal-linker", back_translate("GGGGS" + valid_aa) + "\n", "fail", "no GS linker on the N terminus"),
        ("c-terminal-linker", back_translate(valid_aa + "GGGGS") + "\n", "fail", "no GS linker on the C terminus"),
        ("donor-acceptor-swapped", back_translate(fusion([flag, acceptor, dhfr, donor, snap], L)) + "\n", "fail", "subprotein order"),
        ("donor-one-substitution", back_translate(fusion([flag, mutant_donor, dhfr, acceptor, snap], L)) + "\n", "fail", "donor matches its PDB sequence"),
        ("donor-repeated", back_translate(fusion([flag, donor, donor, dhfr, acceptor, snap], L + ["GGGGS"])) + "\n", "fail", "do not repeat a protein"),
        ("non-acgt-base", valid[:30] + "n" + valid[31:] + "\n", "fail", "gBlock is a DNA sequence"),
        ("gc-window-high", hi + "\n", "fail", "GC 30..70% in every 50-nt window"),
    ]


def run_grader(mod_path, content):
    spec = importlib.util.spec_from_file_location("tb2_protein_assembly_grader", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "gblock.txt"
        p.write_text(content)
        real = pathlib.Path
        mod.Path = lambda _arg: real(d) / "MUTATION-does-not-exist" / "gblock.txt"  # reads a nonexistent path
        try:
            mod.test_gblock()
            return "pass", "-"
        except AssertionError as e:
            return "fail", (str(e).splitlines() or ["AssertionError"])[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane)
    gpath = lane / GRADER_REL
    src = gpath.read_bytes()
    digest = hashlib.sha256(src).hexdigest()
    if digest != GRADER_SHA256:
        print(f"REFUSE grader digest {digest} != pinned {GRADER_SHA256}")
        return 2
    import Bio  # noqa: F401  (fail loudly if Biopython is absent)
    parts = components(src.decode())
    cases = build_cases(parts)
    lens = [len(p) for p in parts]
    max_nt = 3 * (sum(lens) + 4 * 20)
    print(f"grader={GRADER_REL} sha256={digest} pin={PIN} biopython={Bio.__version__}")
    print(f"components_aa={','.join(map(str, lens))} max_passing_nt={max_nt} cap_nt=3000")
    mism = 0
    npass = 0
    for name, content, pred, req in cases:
        obs, msg = run_grader(gpath, content)
        seq = content.strip()
        ok = obs == pred
        mism += not ok
        npass += obs == "pass"
        wins = "ok" if windows_ok(seq.lower()) else "violated"
        print(f"case={name} predicted={pred} observed={obs} match={'yes' if ok else 'NO'} "
              f"nt={len(seq)} gcwin={wins} assertion={msg!r} requirement={req!r}")
    print(f"cases={len(cases)} observed_pass={npass} observed_fail={len(cases) - npass} mismatches={mism}")
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
