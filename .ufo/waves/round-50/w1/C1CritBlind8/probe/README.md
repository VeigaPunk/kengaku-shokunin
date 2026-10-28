# Seat R50C1CritBlind8 reproduction kit — NOT production code

Nothing here is a lane artifact. `sealed/`, `substitutes/`, `probe/` are candidate code that the integrator (L1)
may copy into `plans/sealed50/`; `probe/mutants/fence_*.py` are *mutated copies of the tip fence*
(derived from the tip fence `57adce4a…`; see `../receipts/mutant-direction.txt` for digests) used only to witness kill directions, and must never
be treated as a fence candidate.

Rerun (lane clone at the measured tip `8acd0f83…`, work dir outside the lane):

```
python3 probe/drive.py --lane <lane-clone> --work <scratch>/w1 --mods C1CritBlind8/sealed
python3 probe/drive.py --lane <lane-clone> --work <scratch>/w2 --mods <seat>/probe/mods
python3 probe/drive.py --lane <lane-clone> --work <scratch>/w3 --mods C1CritBlind8/sealed \
        --fence <seat>/probe/mutants/fence_nochain.py
python3 probe/drive.py --lane <lane-clone> --work <scratch>/w4 --mods C1CritBlind8/substitutes \
        --fence <seat>/probe/mutants/fence_nopeel.py
```

The paths printed inside `../receipts/*.txt` are the scratch paths the runs were executed in; that scratch tree was
removed before yield. The driver is byte-identical to the one that produced the receipts.
