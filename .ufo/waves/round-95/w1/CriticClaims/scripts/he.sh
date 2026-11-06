#!/bin/bash
S=/fast/scratch/hyaku/kengaku-r95/CriticClaims
T=afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239
cd $S/ho
for n in HE1-comment-only HE2-local-rename; do
  python3 -I -B $S/lane/plans/round95_c2_counter.py --lane $S/lane --rev $T --work $S/ho/w-$n --tool-file $S/ho/$n.py > $S/ho/out-$n.txt 2>&1; echo "rc=$?" >> $S/ho/out-$n.txt &
done
python3 -I -B $S/lane/plans/round94_c2_counter.py --lane $S/lane --rev $T --work $S/ho/w-r94-honest > $S/ho/out-r94-honest-T.txt 2>&1; echo "rc=$?" >> $S/ho/out-r94-honest-T.txt
wait
echo HE-DONE > $S/ho/he.done
