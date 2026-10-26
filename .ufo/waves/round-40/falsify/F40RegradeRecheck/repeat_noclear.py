"""F40RegradeRecheck secondary probe: is the sweep's deletion of the probe `ready` handshake
between the two gradings load-bearing for the cgw verdict?

Five independent build-once/grade-twice runs of cgw/static-file-no-git with `ready` NOT cleared
between the gradings (the sweep cleared it; this measures whether that reset changed anything).
"""
import pathlib
import sys

S = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(S))
import regrade2 as R  # noqa: E402

R.WORK.mkdir(parents=True, exist_ok=True)
R.MARKS.mkdir(parents=True, exist_ok=True)
probe = R.load_probe("git_webserver_probe")
cap = R.LANE / probe.CAP
same = 0
for k in range(1, 6):
    print(f"--- rep {k} ---")
    r = R.cgw(probe, cap, "static-file-no-git", clear_ready=False)
    same += bool(r)
print(f"REPEAT noclear runs=5 regrade_same={same} diff={5 - same}")
