import subprocess, os
LANE="/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/gate10"
proc = subprocess.run(["sh","-c","test -s $LANE/plans/round90-cases.json; echo rc=$?"],
                      capture_output=True, text=True, cwd=LANE,
                      env={"PATH":"/usr/bin:/bin", "HOME":LANE, "LANE":LANE})
print("cwd=gate10 env LANE=gate10 ->", proc.stdout.strip())
