#!/bin/bash
# Re-run L1 battery commands. Counters are taken from the B tree; lane = my full clone (read-only use).
S=/fast/scratch/hyaku/kengaku-r90/CriticFalsify
LANE=$S/lane
B=$S/x-664435cf/plans
BASE=dcdd494ef4b4a6c0ae349ecb597527124ee54f91
PINREV=664435cfcb9419c4e8ac7828a55aec11a1f36ec4
mkdir -p $S/w-c1base $S/w-c1b $S/w-c2base $S/w-c2b $S/w-c3base $S/w-c3b $S/w-c3selftest $S/w-c2self
echo "## C1 counter at BASE (counter from B tree, rev=base)"; python3 $B/round90_c1_replay.py --lane $LANE --rev $BASE --work $S/w-c1base; echo "rc=$?"
echo "## C1 counter at B (rev=B)"; python3 $B/round90_c1_replay.py --lane $LANE --rev $PINREV --work $S/w-c1b; echo "rc=$?"
echo "## C2 checker at BASE"; python3 $B/round90_counter_pin.py --lane $LANE --rev $BASE --work $S/w-c2base; echo "rc=$?"
echo "## C2 checker at B"; python3 $B/round90_counter_pin.py --lane $LANE --rev $PINREV --work $S/w-c2b; echo "rc=$?"
echo "## C2 selftest"; python3 $B/round90_counter_pin.py --lane $LANE --rev $PINREV --work $S/w-c2self --selftest; echo "rc=$?"
echo "## C3 gate at BASE"; python3 $B/round90_burndown.py --lane $LANE --rev $BASE --work $S/w-c3base --freeze-round 90; echo "rc=$?"
echo "## C3 gate at B"; python3 $B/round90_burndown.py --lane $LANE --rev $PINREV --work $S/w-c3b --freeze-round 90; echo "rc=$?"
echo "## C3 selftest"; python3 $B/round90_burndown.py --lane $LANE --rev $PINREV --work $S/w-c3selftest --selftest; echo "rc=$?"
