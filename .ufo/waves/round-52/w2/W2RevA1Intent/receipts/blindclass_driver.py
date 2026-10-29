import sys
sys.path.insert(0, sys.argv[1] + "/plans")
import round52_c1_grader_audit as c
from pathlib import Path
if sys.argv[2] == "blind":
    orig = c.classify
    c.classify = lambda body: ("V0", orig(body)[1])
rc = c.verdict(Path(sys.argv[1]))
print("RC", rc)
