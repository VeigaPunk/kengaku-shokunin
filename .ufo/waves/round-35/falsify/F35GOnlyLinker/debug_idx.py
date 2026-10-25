#!/usr/bin/env python3
"""Print the find() indices and the order/start assertion outcomes for two one-residue
substitutions (flag vs donor) to show why the failing message differs."""
import importlib.util
import pathlib
from Bio.Seq import Seq

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = LANE / "plans/tb2_grader_probe.py"
GRADER = LANE / "corpus/evidence/round35/tb2-eval/test_outputs.py"

spec = importlib.util.spec_from_file_location("tb2probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

flag, donor, dhfr, acceptor, snap = probe.components(GRADER.read_text())
L = ["GGGGS"] * 4


def subst(aa, i):
    return aa[:i] + ("A" if aa[i] != "A" else "G") + aa[i + 1:]


for name, aa_seq in [
    ("flag-pos4", probe.fusion([subst(flag, 4), donor, dhfr, acceptor, snap], L)),
    ("donor-pos130", probe.fusion([flag, subst(donor, 130), dhfr, acceptor, snap], L)),
]:
    nt = probe.back_translate(aa_seq, "balanced")
    gaa = str(Seq(nt).translate())
    fi = gaa.find(flag)
    di = gaa.find(donor)
    hi = gaa.find(dhfr)
    ai = gaa.find(acceptor)
    si = gaa.find(snap)
    order = fi < di < hi < ai < si
    print(f"case={name}")
    print(f"  indices flag={fi} donor={di} dhfr={hi} acceptor={ai} snap={si}")
    print(f"  order_assertion_passes={order}")
    if order:
        print(f"  next_assertion_flag_idx_eq_0 -> {fi == 0}")
        print(f"  message_if_not = 'Start of gBlock must match flag protein.'")
    else:
        print(f"  message = 'Fusion protein must be in the order flag - donor - dhfr - acceptor - snap'")
