#!/bin/bash
S=/fast/scratch/hyaku/kengaku-r95/CriticClaims
T=afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239
mkdir -p $S/census-T $S/census-r94
python3 $S/lane/plans/round95_false_gate_census.py --lane $S/lane --rev $T --work $S/census-T > $S/census-T.txt 2>&1; echo "rc=$?" >> $S/census-T.txt
python3 $S/lane/plans/round95_false_gate_census.py --lane $S/lane --rev $T --work $S/census-r94 --counter $S/lane/plans/round94_c2_counter.py > $S/census-r94counter.txt 2>&1; echo "rc=$?" >> $S/census-r94counter.txt
echo DONE > $S/census.done
