#!/usr/bin/env python3
"""C1RevSeriesIntent: apply the frozen R52-C1 marker rules (file-level V-classes AND
Amendment-A1 per-test P-classes, imported from the frozen counter itself) to the primary
grader of each of the 12 hand-read TB2 tasks. Read-only over the lane; writes stdout."""
import importlib.util
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location("ctr", LANE / "plans/round52_c1_grader_audit.py")
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

SERIES = [
    (35, "protein-assembly", "corpus/evidence/round35/tb2-eval/test_outputs.py"),
    (36, "regex-log", "corpus/evidence/round36/tb2-regex-log/test_outputs.py"),
    (37, "configure-git-webserver", "corpus/evidence/round37/tb2-git-webserver/test_outputs.py"),
    (38, "build-pmars", "corpus/evidence/round38/tb2-build-pmars/test_outputs.py"),
    (39, "git-leak-recovery", "corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py"),
    (40, "db-wal-recovery", "corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py"),
    (41, "constraints-scheduling", "corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py"),
    (42, "circuit-fibsqrt", "corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py"),
    (43, "feal-differential-cryptanalysis", "corpus/evidence/round43/tb2-feal-differential-cryptanalysis/test_outputs.py"),
    (44, "feal-linear-cryptanalysis", "corpus/evidence/round44/tb2-feal-linear-cryptanalysis/test_outputs.py"),
    (45, "password-recovery", "corpus/evidence/round45/tb2-password-recovery/test_outputs.py"),
    (46, "polyglot-c-py", "corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py"),
]

print("round task file_class feats per_test_classes")
for rnd, task, rel in SERIES:
    p = LANE / rel
    body = p.read_text(encoding="utf-8", errors="replace")
    cls, feats = ctr.classify(body)
    tests = ctr.classify_tests(body)
    pc = ",".join(f"{t['class']}" for t in tests)
    inq = "QUEUE" if cls in ("V1", "V4") else "-"
    print(f"r{rnd} {task} {cls} {inq} presence={int(feats['presence'])} content={int(feats['content'])} behaviour={int(feats['behaviour'])} ntests={feats['test_functions']} [{pc}]")
