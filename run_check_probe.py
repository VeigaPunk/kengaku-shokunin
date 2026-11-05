# Why did E10's check (test -s $LANE/...) exit 1? pwd & $LANE of run_check in a fresh dir
import subprocess, os
proc = subprocess.run(["sh","-c","echo LANE=$LANE; pwd; test -s $LANE/plans/round90-cases.json; echo rc=$?"],
                      capture_output=True, text=True,
                      env={"PATH":"/usr/bin:/bin", "HOME":"/tmp", "LANE":"/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/lane"})
print(proc.stdout, proc.stderr)
