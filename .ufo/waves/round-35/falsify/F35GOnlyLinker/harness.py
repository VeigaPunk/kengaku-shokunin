#!/usr/bin/env python3
"""F35GOnlyLinker falsify battery — fresh-content re-runs of round-35 entry findings 1 & 3.

Reuses the probe's own functions (components, fusion, back_translate, windows_ok,
run_grader) via importlib, so the grader path, digest guard, and tempfile dance are
byte-identical to the committed probe. Runs under `uv run --no-project --with
biopython==1.85`. New content: all-four G-only linkers, mixed lengths, upper bound,
and two *different codon encodings* (rotate = always 2nd-best window-scored codon;
cycle = strict rotation through the codon table); one-residue substitutions moved to
different positions in donor, and into acceptor/snap/dhfr/flag instead of donor.
"""
import importlib.util
import pathlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = LANE / "plans/tb2_grader_probe.py"
GRADER = LANE / "corpus/evidence/round35/tb2-eval/test_outputs.py"

spec = importlib.util.spec_from_file_location("tb2probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

src = GRADER.read_text()
parts = probe.components(src)
flag, donor, dhfr, acceptor, snap = parts
L = ["GGGGS"] * 4
print(f"components_aa={','.join(map(str, map(len, parts)))}")


def back_translate_rotate(aa):
    """Different codon choices: same window-scoring as the probe's balanced mode, but
    always take the 2nd-best codon (deterministic, window-safe, genuinely different)."""
    out = ""
    for res in aa:
        opts = sorted(probe.CODONS[res])
        if len(opts) == 1:
            out += opts[0]
            continue
        tail = out[-47:]

        def score(c):
            w = tail + c
            return (abs(probe.gc(w) / len(w) - 0.5), c)

        out += sorted(opts, key=score)[1]
    return out


def back_translate_cycle(aa):
    """Different codon choices: strict rotation through each residue's codon options."""
    out = ""
    i = 0
    for res in aa:
        opts = sorted(probe.CODONS[res])
        out += opts[i % len(opts)]
        i += 1
    return out


ENCS = {"balanced": lambda aa: probe.back_translate(aa, "balanced"),
        "rotate": back_translate_rotate,
        "cycle": back_translate_cycle}


def subst(aa, i):
    return aa[:i] + ("A" if aa[i] != "A" else "G") + aa[i + 1:]


def run(aa_seq, name, enc="rotate"):
    from Bio.Seq import Seq
    nt = ENCS[enc](aa_seq)
    assert str(Seq(nt).translate()) == aa_seq, f"{name}: encode/translate mismatch!"
    win = probe.windows_ok(nt.lower())
    obs, msg = probe.run_grader(str(GRADER), nt + "\n")
    print(f"case={name} enc={enc} observed={obs} assertion={msg!r} "
          f"nt={len(nt)} gcwin={'ok' if win else 'violated'}")
    return obs, msg, win


# ---- Finding 1: a G-only linker passes (fresh content) ----
run(probe.fusion(parts, ["GGGGG"] * 4), "f1-all4-gonly5")
run(probe.fusion(parts, ["GGGGG"] * 4), "f1-all4-gonly5-enc2", "cycle")
run(probe.fusion(parts, ["G" * 20] + L[1:]), "f1-gonly20-first")
run(probe.fusion(parts, ["G" * 20] * 4), "f1-gonly20-all4")
run(probe.fusion(parts, ["G" * 5, "G" * 9, "G" * 14, "G" * 20]), "f1-gonly-mixed")
run(probe.fusion(parts, ["G" * 5, "G" * 9, "G" * 14, "G" * 20]),
    "f1-gonly-mixed-enc2", "cycle")

# ---- Finding 3: one-residue subprotein errors ----
for pos in (10, 1, 130, len(donor) - 1):
    run(probe.fusion([flag, subst(donor, pos), dhfr, acceptor, snap], L),
        f"f3-donor-pos{pos}")
for pos in (0, 120, len(acceptor) - 1):
    run(probe.fusion([flag, donor, dhfr, subst(acceptor, pos), snap], L),
        f"f3-acceptor-pos{pos}")
for pos in (0, 30, len(snap) - 1):
    run(probe.fusion([flag, donor, dhfr, acceptor, subst(snap, pos)], L),
        f"f3-snap-pos{pos}")
for pos in (0, 90, len(dhfr) - 1):
    run(probe.fusion([flag, donor, subst(dhfr, pos), acceptor, snap], L),
        f"f3-dhfr-pos{pos}")
for pos in (0, 4, len(flag) - 1):
    run(probe.fusion([subst(flag, pos), donor, dhfr, acceptor, snap], L),
        f"f3-flag-pos{pos}")

# Same AA under balanced vs rotate encodings (codon-choice invariance).
for enc in ("balanced", "rotate"):
    run(probe.fusion([flag, subst(donor, 130), dhfr, acceptor, snap], L),
        f"f3-donor-pos130-{enc}", enc)
for enc in ("balanced", "rotate"):
    run(probe.fusion([subst(flag, 4), donor, dhfr, acceptor, snap], L),
        f"f3-flag-pos4-{enc}", enc)
print("done")
