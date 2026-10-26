#!/bin/bash
# usage: run.sh <GRADE_CWD> <outfile>
export GRADE_CWD=$1
cd /fast/scratch/hyaku/kengaku-r42/R42ScoutHarborCwd
python3 probe_cwd.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --work /fast/scratch/hyaku/kengaku-r42/R42ScoutHarborCwd/w > $2 2>&1; echo rc=$? >> $2
