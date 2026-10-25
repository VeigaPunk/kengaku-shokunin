#!/usr/bin/env python3
"""F35GOnlyLinker falsify battery v2 — fresh-content re-runs of round-35 findings 1 & 3.

Reuses the probe's functions (components, fusion, back_translate, windows_ok,
run_grader) via importlib. Every case is run under TWO codon encodings:
  balanced = the probe's deterministic greedy (control, already proven window-safe)
  variant  = same greedy objective but with a seeded random tie-break among equal
             codons; the seed is chosen so the whole construct still passes
             windows_ok (GC 30..70% in every 50-nt window); the per-position codon
             difference vs `balanced` is printed to prove the content is fresh.
"""
import importlib.util
import pathlib
import random

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


def back_translate_variant(aa, seed):
    rng = random.Random(seed)
    out = ""
    for res in aa:
        opts = sorted(probe.CODONS[res])
        if len(opts) == 1:
            out += opts[0]
            continue
        tail = out[-47:]

        def score(c):
            w = tail + c
            return (abs(probe.gc(w) / len(w) - 0.5), rng.random(), c)

        out += min(opts, key=score)
    return out


def find_variant(aa, max_seed=3000):
    """First seed whose encoding passes every GC window; report codon diff vs balanced."""
    bal = probe.back_translate(aa, "balanced")
    for seed in range(1, max_seed + 1):
        enc = back_translate_variant(aa, seed)
        if probe.windows_ok(enc.lower()):
            diff = sum(1 for b, e in zip(bal, enc) if b != e)
            return seed, enc, diff
    return None, None, None


def subst(aa, i):
    return aa[:i] + ("A" if aa[i] != "A" else "G") + aa[i + 1:]


def run(aa_seq, name, enc="balanced"):
    from Bio.Seq import Seq
    if enc == "balanced":
        nt = probe.back_translate(aa_seq, "balanced")
        diff = None
        seed = None
    elif enc == "variant":
        seed, nt, diff = find_variant(aa_seq)
        if nt is None:
            print(f"  [{name} variant: NO window-safe seed found in 3000 attempts]")
            return None, None, None
    else:
        raise ValueError(enc)
    if seed is not None:
        print(f"  [{name} variant seed={seed} codon_diff_vs_balanced={diff} "
              f"({diff}/{len(aa_seq)} residues differently encoded)]")
    assert str(Seq(nt).translate()) == aa_seq, f"{name}: encode/translate mismatch!"
    win = probe.windows_ok(nt.lower())
    obs, msg = probe.run_grader(str(GRADER), nt + "\n")
    print(f"case={name} enc={enc} observed={obs} assertion={msg!r} "
          f"nt={len(nt)} gcwin={'ok' if win else 'violated'}")
    return obs, msg, win


RES = []


def rec(aa_seq, name):
    for enc in ("balanced", "variant"):
        out = run(aa_seq, name, enc)
        if out[0] is not None:
            RES.append((name, enc) + out)


print("== finding 1: G-only linkers ==")
rec(probe.fusion(parts, ["GGGGG"] * 4), "f1-all4-gonly5")
rec(probe.fusion(parts, ["G" * 20] + L[1:]), "f1-gonly20-first")
rec(probe.fusion(parts, ["G" * 20] * 4), "f1-gonly20-all4")
rec(probe.fusion(parts, ["G" * 5, "G" * 9, "G" * 14, "G" * 20]), "f1-gonly-mixed")

print("== finding 3: one-residue subprotein errors ==")
for pos in (10, 1, 130, len(donor) - 1):
    rec(probe.fusion([flag, subst(donor, pos), dhfr, acceptor, snap], L),
        f"f3-donor-pos{pos}")
for pos in (0, 120, len(acceptor) - 1):
    rec(probe.fusion([flag, donor, dhfr, subst(acceptor, pos), snap], L),
        f"f3-acceptor-pos{pos}")
for pos in (0, 30, len(snap) - 1):
    rec(probe.fusion([flag, donor, dhfr, acceptor, subst(snap, pos)], L),
        f"f3-snap-pos{pos}")
for pos in (0, 90, len(dhfr) - 1):
    rec(probe.fusion([flag, donor, subst(dhfr, pos), acceptor, snap], L),
        f"f3-dhfr-pos{pos}")
for pos in (0, 4, len(flag) - 1):
    rec(probe.fusion([subst(flag, pos), donor, dhfr, acceptor, snap], L),
        f"f3-flag-pos{pos}")

f1 = [r for r in RES if r[0].startswith("f1")]
f3 = [r for r in RES if r[0].startswith("f3")]
order = [r for r in f3 if "order" in r[3]]
flagmsg = [r for r in f3 if "flag" in r[3] and "order" not in r[3]]
winbad = [r for r in RES if not r[4]]
print(f"SUMMARY f1_total={len(f1)} f1_pass={sum(1 for r in f1 if r[2]=='pass')} "
      f"f1_fail={sum(1 for r in f1 if r[2]=='fail')}")
print(f"SUMMARY f3_total={len(f3)} f3_order_message={len(order)} "
      f"f3_flag_message={len(flagmsg)} f3_other={len(f3)-len(order)-len(flagmsg)}")
print(f"SUMMARY gcwin_violated={len(winbad)} "
      f"({','.join(r[0] for r in winbad)})")
print("done")
