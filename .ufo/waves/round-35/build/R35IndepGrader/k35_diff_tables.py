#!/usr/bin/env python3
"""Differential validation: my own translate() vs Biopython Seq.translate() (table 1).

Runs over the 18 probe case contents plus random DNA (length %3==0, standard bases,
stops included). Any divergence prints and exits 1.
"""
import importlib.util
import pathlib
import random
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = LANE / "plans/tb2_grader_probe.py"
INDEP = LANE / ".ufo/waves/round-35/build/R35IndepGrader/indep.py"

from Bio.Seq import Seq

# load my checker's translation table
spec = importlib.util.spec_from_file_location("indep_mod", INDEP)
indep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indep)

# load probe case contents
spec2 = importlib.util.spec_from_file_location("tb2_probe", PROBE)
probe = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(probe)
parts = probe.components((LANE / "corpus/evidence/round35/tb2-eval/test_outputs.py").read_text())
cases = probe.build_cases(parts)

seqs = [content.strip() for _, content, _, _ in cases]

random.seed(20261025)
alphabet = "acgt"
for _ in range(2000):
    n = 3 * random.randint(1, 100)
    seqs.append("".join(random.choice(alphabet) for _ in range(n)))

bad = 0
for s in seqs:
    mine = indep.translate(s)
    bio = str(Seq(s).translate())
    if mine != bio:
        print(f"DIVERGE len={len(s)} nt={s!r}")
        print(f"  mine={mine!r}")
        print(f"  bio ={bio!r}")
        bad += 1
        if bad >= 5:
            break
print(f"checked={len(seqs)} divergences={bad}")
sys.exit(1 if bad else 0)
